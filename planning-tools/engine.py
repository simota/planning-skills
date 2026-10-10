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
back a verdict from the very engine that was supposed to be excluded. `--running`
is required, and absent it this stops.

**A checker that did not run is not a checker that passed.** Every failure path
here raises. Nothing returns a default verdict, nothing degrades to "assume
fine": an engine missing from PATH, an engine that starts and produces no
parseable object, a response that does not match the schema — each is an error
with the engine's own words attached, because the alternative is a green run
that verified nothing.

Engine quirks, re-checked by `make engines` rather than dated:

* `codex exec` rejects a schema without `additionalProperties: false`, at every
  level. Schemas are normalised here so callers write ordinary JSON Schema.
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
import pathlib
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


def strict(schema: dict) -> dict:
    """Every object closed, which is what codex requires and agy tolerates."""
    if not isinstance(schema, dict):
        return schema
    out = {k: strict(v) if isinstance(v, dict) else v for k, v in schema.items()}
    if out.get("type") == "object":
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


def conforms(schema: dict, value, at: str = "$") -> str | None:
    """The first way `value` breaks `schema`, or None. Types, required keys,
    enums and combinators — enough to refuse a malformed verdict, no dependency.

    The engines claim to enforce the schema themselves; this is not trusting
    that, because a wrong-shaped answer read as a verdict is a verdict nobody gave.
    """
    if not isinstance(schema, dict):
        return None
    want = schema.get("type")
    if want:
        types = want if isinstance(want, list) else [want]
        # bool is an int in Python; a JSON true is not a number.
        if not any(isinstance(value, _TYPES.get(t, object))
                   and not (t in ("number", "integer") and isinstance(value, bool))
                   for t in types):
            return f"{at} is {type(value).__name__}, schema wants {want}"
    if "enum" in schema and value not in schema["enum"]:
        return f"{at} is {value!r}, not one of {schema['enum']}"
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
    if isinstance(value, list) and isinstance(schema.get("items"), dict):
        for i, v in enumerate(value):
            why = conforms(schema["items"], v, f"{at}[{i}]")
            if why:
                return why
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
    why = conforms(strict(schema), got)
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
            # No prompt argument: `-p` reads it from stdin. Without a shell or a
            # file tool, a claim that says "run this" has nothing to run it with.
            argv = ["claude", "-p", "--output-format", "json",
                    "--json-schema", json.dumps(schema),
                    "--disallowedTools", "Bash,Edit,Write,MultiEdit,NotebookEdit,WebFetch"]
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
    try:
        r = subprocess.run(argv, capture_output=True, text=True, timeout=TIMEOUT,
                           cwd=cwd, input=stdin if stdin is not None else "")
    except FileNotFoundError:
        raise EngineError(f"{engine} is not on PATH") from None
    except subprocess.TimeoutExpired:
        raise EngineError(f"{engine} did not answer within {TIMEOUT}s") from None
    except OSError as e:                 # E2BIG for an oversized argv, among others
        raise EngineError(f"{engine} could not be started: {e}") from None
    # A failed run that still printed an object is a failed run.
    if r.returncode != 0:
        raise EngineError(f"{engine} exited {r.returncode}.\n{_tail(r)}")
    return r


def _parse(engine: str, body: str) -> dict:
    stripped = body.strip()
    try:
        got = json.loads(stripped)
        if isinstance(got, dict):
            return got
    except ValueError:
        pass
    for line in reversed(stripped.splitlines()):
        try:
            got = json.loads(line)
        except ValueError:
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
    ap.add_argument("--running", help="the engine running this harness — required, never guessed")
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
        engine = a.engine or other_than(a.running)
        if a.running and engine == a.running:
            raise EngineError(f"{engine} is the engine running this; "
                              "a verdict from it is not a check")
        got = run(engine,
                  pathlib.Path(a.prompt_file).read_text(encoding="utf-8"),
                  json.loads(pathlib.Path(a.schema).read_text(encoding="utf-8")))
    except EngineError as e:
        print(f"{a.engine or 'checker'}: {e}", file=sys.stderr)
        return 1
    print(json.dumps(got, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
