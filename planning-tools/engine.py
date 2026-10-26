#!/usr/bin/env python3
"""Run a checker on an engine that did not produce the work.

`routes.yaml` defers every loop route's `checker` to run time, because all three
CLIs read the same SKILL.md and any of them may be the one running. This resolves
it: given the engine that is running, it picks one that is not.

    make engines                     every declared engine answers, or says why
    python3 planning-tools/engine.py --running claude --prompt-file p.txt --schema s.json

**The running engine is stated, never sniffed.** codex launched from inside
Claude Code inherits `CLAUDECODE` and `CLAUDE_CODE_*`, so a nested run reads as
its parent and any env heuristic silently mis-identifies it — which would hand
back a verdict from the very engine that was supposed to be excluded. A checker is
named or `--running` is given; with neither, this stops.

**A checker that did not run is not a checker that passed.** Every failure path
here raises. Nothing returns a default verdict, nothing degrades to "assume
fine": an engine missing from PATH, an engine that starts and produces no
parseable object, a response that does not match the schema — each is an error
with the engine's own words attached, because the alternative is a green run
that verified nothing.

Engine quirks, re-checked by `make engines` rather than dated:

* `codex exec` rejects a schema without `additionalProperties: false`, at every
  level. Schemas are normalised here so callers write ordinary JSON Schema; an
  object the caller opened on purpose is refused rather than closed.
* `agy --print` returns an envelope; the validated object is `structured_output`.
* `claude -p --json-schema` returns the same kind of envelope as agy; the
  validated object is `structured_output`, and `result` is only its text form.
  `is_error` in that envelope is a failed run even when the exit code is 0.

**The prompt is untrusted.** It carries claim text written by whoever made the
work, so every engine runs in a fresh empty directory, the prompt goes in on
stdin where the CLI reads it there (an argv entry is capped near 128 KiB and can
be read as a flag), and each engine is held to the narrowest mode it offers.
"""
from __future__ import annotations

import argparse
import json
import math
import os
import pathlib
import signal
import subprocess
import sys
import tempfile

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
H = yaml.safe_load((ROOT / "planning-registry" / "harness.yaml").read_text(encoding="utf-8"))
ENGINES = H.get("engines") or {}
TIMEOUT = 600


class EngineError(RuntimeError):
    """The engine did not answer. Never a verdict."""


# Keywords whose value is data, not a schema: closing an object found there
# would change which answers the schema accepts.
_VALUES = {"const", "default", "enum", "examples"}


def strict(schema: dict) -> dict:
    """Every object closed, which is what codex requires and agy tolerates."""
    if not isinstance(schema, dict):
        return schema
    out = {k: strict(v) if isinstance(v, dict) and k not in _VALUES else v
           for k, v in schema.items()}
    # `["object", "null"]` is an object too, and codex rejects it just as open.
    t = out.get("type")
    if t == "object" or (isinstance(t, list) and "object" in t):
        # Closing an object the caller opened on purpose — a map, an explicit
        # `true` — asks a different question, and the answer `{}` then passes.
        if out.get("additionalProperties", False) is not False:
            raise EngineError("schema opens an object with additionalProperties "
                              f"{out['additionalProperties']!r}; every object is closed "
                              "for codex, so this cannot be asked as written")
        out["additionalProperties"] = False
        out["properties"] = {k: strict(v) for k, v in (out.get("properties") or {}).items()}
    if isinstance(out.get("items"), dict):
        out["items"] = strict(out["items"])
    # An object reached only through a combinator is still an object codex rejects.
    for key in ("anyOf", "oneOf", "allOf", "prefixItems"):
        if isinstance(out.get(key), list):
            out[key] = [strict(s) for s in out[key]]
    return out


_TYPES = {"object": dict, "array": list, "string": str, "boolean": bool,
          "null": type(None), "number": (int, float), "integer": int}


# What conforms() checks, and what it may ignore. Any other keyword is refused
# rather than skipped: a constraint nobody checks reads as one that held.
_CHECKED = {"type", "enum", "const", "required", "properties", "additionalProperties",
            "items", "allOf", "anyOf", "oneOf", "not", "minLength", "maxLength",
            "minimum", "maximum", "minItems", "maxItems"}
# `pattern` is deliberately absent: JSON Schema patterns are ECMA-262, and
# Python's `re` both rejects valid ones (`\p{L}`) and accepts what they reject.
_ANNOTATIONS = {"$schema", "$id", "title", "description", "default", "examples",
                "$comment"}


def _is(value, t: str) -> bool:
    # bool is an int in Python; a JSON true is not a number.
    if isinstance(value, bool):
        return t == "boolean"
    # JSON has one number type: 1.0 is an integer, and json.loads reads it as a float.
    if t == "integer" and isinstance(value, float):
        return value.is_integer()
    return isinstance(value, _TYPES[t])


def _same(a, b) -> bool:
    """JSON equality: true is not 1, and 1 is 1.0 — at every depth."""
    if isinstance(a, bool) or isinstance(b, bool):
        return isinstance(a, bool) and isinstance(b, bool) and a == b
    if isinstance(a, list) and isinstance(b, list):
        return len(a) == len(b) and all(_same(x, y) for x, y in zip(a, b))
    if isinstance(a, dict) and isinstance(b, dict):
        return a.keys() == b.keys() and all(_same(a[k], b[k]) for k in a)
    return a == b


def conforms(schema: dict, value, at: str = "$") -> str | None:
    """The first way `value` breaks `schema`, or None — no dependency.

    The engines claim to enforce the schema themselves; this is not trusting
    that, because a wrong-shaped answer read as a verdict is a verdict nobody gave.
    A keyword, or a form of one, outside what this implements raises when the
    walk reaches it: a partial validator that passed what it could not check
    would be the green run that verified nothing. A subschema the value never
    reaches — an absent optional property — is not inspected.
    """
    if schema is True:
        return None
    if schema is False:
        return f"{at} is present where the schema allows nothing"
    if not isinstance(schema, dict):
        raise EngineError(f"schema at {at} is {type(schema).__name__}, not a schema")
    unknown = set(schema) - _CHECKED - _ANNOTATIONS
    # Forms of a checked keyword that this check does not implement either.
    if not isinstance(schema.get("items", {}), (dict, bool)):
        unknown.add("items (list form)")
    if not isinstance(schema.get("additionalProperties", False), bool):
        unknown.add("additionalProperties (schema form)")
    want = schema.get("type")
    if "type" in schema:
        named = want if isinstance(want, list) else [want]
        if not named:
            unknown.add("type []")
        for t in named:
            if not isinstance(t, str) or t not in _TYPES:
                unknown.add(f"type {t!r}")
    if unknown:
        raise EngineError(f"schema at {at} uses {sorted(unknown)}, which this "
                          "check does not implement; extend conforms() first")
    want = schema.get("type")
    if want:
        types = want if isinstance(want, list) else [want]
        if not any(_is(value, t) for t in types):
            return f"{at} is {type(value).__name__}, schema wants {want}"
    if "const" in schema and not _same(value, schema["const"]):
        return f"{at} is {value!r}, not {schema['const']!r}"
    if "enum" in schema and not any(_same(value, e) for e in schema["enum"]):
        return f"{at} is {value!r}, not one of {schema['enum']}"
    if isinstance(value, str):
        if len(value) < schema.get("minLength", 0):
            return f"{at} is shorter than {schema['minLength']}"
        if "maxLength" in schema and len(value) > schema["maxLength"]:
            return f"{at} is longer than {schema['maxLength']}"
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            return f"{at} is below {schema['minimum']}"
        if "maximum" in schema and value > schema["maximum"]:
            return f"{at} is above {schema['maximum']}"
    if isinstance(value, dict):
        for k in schema.get("required") or []:
            if k not in value:
                return f"{at} has no {k!r}"
        props = schema.get("properties") or {}
        for k, v in value.items():
            if k in props:
                why = conforms(props[k], v, f"{at}.{k}")
                if why:
                    return why
            elif schema.get("additionalProperties") is False:
                return f"{at} carries {k!r}, which the schema does not allow"
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            return f"{at} has fewer than {schema['minItems']} items"
        if "maxItems" in schema and len(value) > schema["maxItems"]:
            return f"{at} has more than {schema['maxItems']} items"
        if "items" in schema:
            for i, v in enumerate(value):
                why = conforms(schema["items"], v, f"{at}[{i}]")
                if why:
                    return why
    if "not" in schema and conforms(schema["not"], value, at) is None:
        return f"{at} matches a schema it must not"
    for s in schema.get("allOf") or []:
        why = conforms(s, value, at)
        if why:
            return why
    for key in ("anyOf", "oneOf"):
        alts = schema.get(key)
        if alts:
            ok = sum(conforms(s, value, at) is None for s in alts)
            if ok == 0 or (key == "oneOf" and ok > 1):
                return f"{at} matches {ok} of its {key} alternatives"
    return None


def run(engine: str, prompt: str, schema: dict) -> dict:
    """Ask `engine` for one object matching `schema`. Raises rather than guessing."""
    known = ENGINES.get("runs_on") or []
    if engine not in known:
        raise EngineError(f"{engine} is not one of {known}")
    got = _ask(engine, prompt, strict(schema))
    # Both, because neither contains the other: closing the objects under `not`
    # or in a `oneOf` alternative loosens what they exclude, so an answer the
    # caller's schema rejects can conform to the closed one.
    why = conforms(strict(schema), got) or conforms(schema, got)
    if why:
        raise EngineError(f"{engine} answered off-schema: {why}\n{json.dumps(got)[:400]}")
    return got


def _ask(engine: str, prompt: str, schema: dict):
    with tempfile.TemporaryDirectory(prefix="planning-engine-") as tmp:
        d = pathlib.Path(tmp)
        s = d / "schema.json"
        s.write_text(json.dumps(schema), encoding="utf-8")
        # Nothing to read or write where the engine starts: not this repo, not
        # the caller's project, not the schema beside it.
        cwd = d / "empty"
        cwd.mkdir()
        if engine == "codex":
            out = d / "answer.json"
            # `-` reads the prompt from stdin.
            argv = ["codex", "exec", "--output-schema", str(s), "-o", str(out),
                    "--sandbox", "read-only", "--skip-git-repo-check", "-"]
            r = _spawn(engine, argv, cwd, prompt)
            body = out.read_text(encoding="utf-8") if out.exists() else ""
            if not body.strip():
                raise EngineError(f"codex wrote no answer.\n{_tail(r)}")
            return _parse(engine, body)
        if engine == "claude":
            # No prompt argument: `-p` reads it from stdin. No tools at all and
            # no MCP servers: a denylist misses whatever it did not name (Read,
            # WebSearch, a user's MCP tools), so a claim that says "run this" or
            # "read that" has nothing to do it with. `--json-schema` still
            # answers through its own StructuredOutput tool.
            argv = ["claude", "-p", "--output-format", "json",
                    "--json-schema", json.dumps(schema),
                    "--tools", "", "--strict-mcp-config"]
            r = _spawn(engine, argv, cwd, prompt)
            return _structured(engine, _parse(engine, r.stdout), r, "subtype")
        if engine == "agy":
            # No sandbox flag is known for agy, and none is guessed at here; it
            # gets the empty directory only. `--print=` keeps the prompt one
            # token, so a prompt opening with `-` is not read as a flag.
            argv = ["agy", f"--print={prompt}", "--output-format", "json",
                    "--json-schema", str(s)]
            r = _spawn(engine, argv, cwd)
            return _structured(engine, _parse(engine, r.stdout), r, "status")
    raise EngineError(f"no invocation is known for {engine}")


def _structured(engine: str, envelope: dict, r: subprocess.CompletedProcess, state: str):
    if envelope.get("is_error"):
        raise EngineError(f"{engine} reported an error ({state} "
                          f"{envelope.get(state)!r}).\n{_tail(r)}")
    if "structured_output" not in envelope:
        raise EngineError(f"{engine} returned no structured_output "
                          f"({state} {envelope.get(state)!r}).\n{_tail(r)}")
    return envelope["structured_output"]


def _spawn(engine: str, argv: list[str], cwd: pathlib.Path,
           stdin: str | None = None) -> subprocess.CompletedProcess:
    # Armed before the engine exists, so no termination can slip between its
    # start and the cleanup that stops it; until it exists, a signal is only
    # noted, and acted on the moment there is an engine to stop.
    termination = _Termination()
    p = None
    try:
        try:
            # Decoded leniently and as UTF-8 whatever the locale: one stray byte
            # in an engine's output must surface as that engine's error, not as a
            # UnicodeDecodeError that takes the other engines' verdicts with it.
            # Its own session, so a timeout stops the whole engine: a CLI that is
            # a launcher for the real binary would otherwise leave it running.
            p = subprocess.Popen(argv, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE, text=True, encoding="utf-8",
                                 errors="replace", cwd=cwd, start_new_session=True)
        except FileNotFoundError:
            raise EngineError(f"{engine} is not on PATH") from None
        # E2BIG for an oversized argv; ValueError for one the OS cannot carry (a
        # NUL byte, an unpaired surrogate) — either is this engine's, not the run's.
        except (OSError, ValueError) as e:
            raise EngineError(f"{engine} could not be started: {e}") from None
        termination.arm()
        out, err = p.communicate(input=stdin if stdin is not None else "", timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        _kill_group(p)
        raise EngineError(f"{engine} did not answer within {TIMEOUT}s") from None
    except EngineError:
        raise
    except BaseException:
        # Ctrl-C, a termination, anything else: in its own session the engine
        # hears no signal meant for this harness, so it stops here or not at all.
        if p is not None:
            _kill_group(p)
        raise
    finally:
        termination.restore()
    r = subprocess.CompletedProcess(argv, p.returncode, out, err)
    # A failed run that still printed an object is a failed run.
    if r.returncode != 0:
        raise EngineError(f"{engine} exited {r.returncode}.\n{_tail(r)}")
    return r


class _Termination:
    """SIGTERM and SIGHUP end this process on the spot by default, skipping the
    cleanup that stops the engine — which, in its own session, never received
    them. While an engine runs they raise SystemExit instead; before it exists
    they are noted and raised once it does. Only the main thread may set
    handlers; elsewhere the defaults stay."""

    SIGNALS = (signal.SIGTERM, signal.SIGHUP)

    def __init__(self):
        self.armed, self.pending, self.previous = False, None, {}
        for sig in self.SIGNALS:
            try:
                self.previous[sig] = signal.signal(sig, self._handle)
            except ValueError:                  # not the main thread
                break

    def _handle(self, signum, _frame):
        if not self.armed:
            self.pending = signum               # no engine to stop yet
            return
        raise SystemExit(128 + signum)

    def arm(self):
        self.armed = True
        if self.pending is not None:
            raise SystemExit(128 + self.pending)

    def restore(self):
        for sig, handler in self.previous.items():
            signal.signal(sig, handler)
        if self.pending is not None and not self.armed:
            raise SystemExit(128 + self.pending)  # the engine never started


def _kill_group(p: subprocess.Popen) -> None:
    try:
        os.killpg(p.pid, signal.SIGKILL)
    except (ProcessLookupError, PermissionError):
        p.kill()
    # Reap the engine, then let go of its pipes: draining them would wait on any
    # descendant that left the group and still holds them open.
    p.wait()
    for pipe in (p.stdin, p.stdout, p.stderr):
        if pipe:
            pipe.close()


def _not_json(name: str):
    raise ValueError(f"{name} is not JSON")


def _finite(digits: str) -> float:
    """A number too large for a float, read as infinity: JSON has no such value."""
    value = float(digits)
    if math.isinf(value):
        raise ValueError(f"{digits} does not fit a float")
    return value


def _parse(engine: str, body: str) -> dict:
    # Python's json reads NaN and Infinity, which JSON does not have, and turns
    # 1e400 into infinity; a NaN passes every `minimum` and `maximum` conforms()
    # would hold it to, and an infinity is printed back as `Infinity`.
    # Nesting deeper than the parser recurses raises RecursionError, which is
    # not a ValueError: it is this engine's unreadable answer all the same.
    stripped = body.strip()
    try:
        got = json.loads(stripped, parse_constant=_not_json, parse_float=_finite)
        if isinstance(got, dict):
            return got
    except (ValueError, RecursionError):
        pass
    for line in reversed(stripped.splitlines()):
        try:
            got = json.loads(line, parse_constant=_not_json, parse_float=_finite)
        except (ValueError, RecursionError):
            continue
        if isinstance(got, dict):
            return got
    raise EngineError(f"{engine} printed nothing that parses as an object:\n{body[:400]}")


def _tail(r: subprocess.CompletedProcess) -> str:
    return "\n".join((r.stderr or r.stdout or "").strip().splitlines()[-6:])


def other_than(running: str) -> str:
    """An engine that is not the one running. Raises rather than falling back."""
    known = ENGINES.get("runs_on") or []
    if running not in known:
        raise EngineError(f"the running engine {running!r} is not one of {known}; "
                          "state it correctly rather than letting this guess")
    for candidate in known:
        if candidate != running:
            return candidate
    raise EngineError(f"{known} leaves nothing to check {running} with")


SELFTEST = {"type": "object", "properties": {"ok": {"type": "boolean"}},
            "required": ["ok"]}


def selftest() -> int:
    """Ask each declared engine for one object. Reachability, not correctness."""
    bad = 0
    for engine in ENGINES.get("runs_on") or []:
        try:
            got = run(engine, "Reply with ok=true and nothing else.", SELFTEST)
        except EngineError as e:
            print(f"  {engine}: UNAVAILABLE — {e}")
            bad += 1
            continue
        print(f"  {engine}: answered {got}")
    known = ENGINES.get("runs_on") or []
    print(f"engines reachable: {len(known) - bad}/{len(known)} of {known}   "
          f"any of them may be the one running")
    # Unreachable is reported, never fatal: a machine without one of these still
    # runs every other check, and a hook that fails on a missing CLI gets removed.
    return 0


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("engine", nargs="?", help="the checker; omit to resolve from --running")
    ap.add_argument("--running", help="the engine running this harness — never guessed; "
                    "required unless a checker is named")
    ap.add_argument("--prompt-file")
    ap.add_argument("--schema")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest or not (a.engine or a.running or a.prompt_file or a.schema):
        return selftest()
    if not (a.engine or a.running):
        # A prompt with no engine named was a check someone meant to run;
        # answering it with a reachability table would read as having done so.
        print("name the checker or pass --running; it is never guessed", file=sys.stderr)
        return 2
    if not (a.prompt_file and a.schema):
        print("need --prompt-file and --schema", file=sys.stderr)
        return 2
    try:
        prompt = pathlib.Path(a.prompt_file).read_text(encoding="utf-8")
        schema = json.loads(pathlib.Path(a.schema).read_text(encoding="utf-8"))
    except (OSError, ValueError, RecursionError) as e:
        # The caller's input, not the checker's answer: 1 would read as the
        # engine having failed to answer a question that was never asked.
        print(f"cannot read the prompt or schema: {e}", file=sys.stderr)
        return 2
    try:
        engine = a.engine or other_than(a.running)
        if a.running and engine == a.running:
            raise EngineError(f"{engine} is the engine running this; "
                              "a verdict from it is not a check")
        got = run(engine, prompt, schema)
    except EngineError as e:
        print(f"{a.engine or 'checker'}: {e}", file=sys.stderr)
        return 1
    print(json.dumps(got, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
