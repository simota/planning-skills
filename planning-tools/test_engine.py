#!/usr/bin/env python3
"""Offline checks of engine.conforms(): no engine is spawned.

`make engines` needs the CLIs installed; this does not, so the validator that
stands between an engine's answer and a verdict is exercised on every run.
"""
from __future__ import annotations

import json
import os
import signal
import subprocess
import sys
import tempfile
import threading
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.dont_write_bytecode = True
import engine                                       # noqa: E402
import refute                                       # noqa: E402

OBJ = {"type": "object"}
UNION = {"oneOf": [{**OBJ, "properties": {"k": {"const": "a"}}, "required": ["k"]},
                   {**OBJ, "properties": {"k": {"const": "b"}}, "required": ["k"]}]}

# (schema, value, conforms?)
CASES = [
    (engine.strict(refute.SCHEMA), {"refuted": False, "reason": "r", "what_would_settle_it": "s"}, True),
    (engine.strict(refute.SCHEMA), {"refuted": "false", "reason": "r", "what_would_settle_it": "s"}, False),
    (engine.strict(refute.SCHEMA), {"refuted": True, "reason": "r", "what_would_settle_it": "s", "x": 1}, False),
    (engine.strict(engine.SELFTEST), {"ok": True}, True),
    (UNION, {"k": "a"}, True),
    (UNION, {"k": "c"}, False),
    ({"enum": [1]}, True, False),
    ({"enum": [[1]]}, [True], False),
    ({"const": {"a": 1}}, {"a": 1.0}, True),
    ({"type": "integer"}, True, False),
    ({"type": "integer"}, 1.0, True),                # JSON's 1.0 is an integer
    ({"type": "integer"}, 1.5, False),
    # strict() closes schemas, not the values a const holds.
    (engine.strict({**OBJ, "properties": {"m": {"const": {"type": "object"}}}}),
     {"m": {"type": "object"}}, True),
    ({"not": {"const": 1}}, 1, False),
    ({"type": "array", "minItems": 1, "items": {"type": "string"}}, [], False),
    ({"type": "array", "items": False}, [1], False),
    ({"properties": {"x": False}}, {"x": 1}, False),
    ({"type": "string", "maxLength": 2}, "abc", False),
    ({"type": "number", "minimum": 0}, -1, False),
    # A nullable object is still an object: closed, so an extra key fails.
    (engine.strict({"type": ["object", "null"], "properties": {"a": {"type": "string"}}}),
     {"a": "x", "b": 1}, False),
    (engine.strict({"type": ["object", "null"], "properties": {"a": {"type": "string"}}}),
     None, True),
]

# Schemas this check must refuse to judge rather than pass.
REFUSED = [
    ({"format": "date"}, "x"),
    ({"type": "array", "items": [{"type": "string"}]}, [5]),
    ({"properties": {"a": {}}, "additionalProperties": {"type": "string"}}, {"b": 5}),
    ({"type": "int"}, 1),
    ({"type": "string", "pattern": "^x"}, "x"),       # ECMA-262, not Python's re
    ({"type": "string", "pattern": "\\p{L}"}, "x"),
    ({"type": ""}, 5),
    ({"type": []}, 5),
    ({"type": [["x"]]}, "a"),
]

# Schemas run() must refuse before asking: strict() closes every object for
# codex, and closing one the caller left open on purpose asks a different
# question — a map comes back `{}` and passes. (schema, what the engine says)
RUN_REFUSED = [
    ({**OBJ, "additionalProperties": {"type": "string"}}, {}),
    ({**OBJ, "properties": {"m": {**OBJ, "additionalProperties": True}}}, {"m": {}}),
    ({"type": ["object", "null"], "additionalProperties": True}, {}),
]

# What an engine prints that is not JSON, though Python's json reads it: a NaN
# passes every `minimum` and `maximum`, so it must not reach conforms() at all.
NOT_JSON = ['{"n": NaN}', '{"n": Infinity}', '{"n": -Infinity}']


def _alive(pidfile: Path) -> bool:
    """Whether the pid recorded in `pidfile` is still a running process."""
    if not pidfile.exists():
        return False
    pid = int(pidfile.read_text())
    for _ in range(20):                              # killing is not instant
        try:
            os.kill(pid, 0)
        except ProcessLookupError:
            return False
        try:
            state = Path(f"/proc/{pid}/stat").read_text().split(") ", 1)[-1]
        except FileNotFoundError:
            return False                             # reaped between the two looks
        except OSError:
            state = ""                               # no /proc: kill(0) decides
        if state.startswith("Z"):
            return False                             # dead, waiting to be reaped
        time.sleep(0.1)
    os.kill(pid, 9)                                  # leave no stray behind
    return True


def spawn_cases() -> list[str]:
    """What reaches an engine and what comes back, with a stub for the engine."""
    bad = []
    with tempfile.TemporaryDirectory() as tmp:
        # A byte that is not UTF-8 is that engine's problem, never a crash.
        try:
            r = engine._spawn("stub", [sys.executable, "-c",
                                       "import sys; sys.stdout.buffer.write(b'\\xff{}')"],
                              Path(tmp), "")
            if "\ufffd" not in r.stdout:
                bad.append(f"spawn: undecodable byte came back as {r.stdout!r}")
        except Exception as e:                       # noqa: BLE001 — any escape is the bug
            bad.append(f"spawn: undecodable output raised {type(e).__name__}: {e}")
        # A claim the OS cannot pass as an argument (a NUL byte, as agy's argv
        # carries the prompt) is that engine's error, not a crash of the run.
        try:
            engine._spawn("stub", [sys.executable, "-c", "pass", "a\x00b"], Path(tmp), "")
            bad.append("spawn: an argument with a NUL byte was accepted")
        except engine.EngineError:
            pass
        except Exception as e:                       # noqa: BLE001
            bad.append(f"spawn: a NUL byte raised {type(e).__name__}: {e}")
        # A timed-out engine is stopped whole: a launcher's own child must not
        # outlive the run, still spending tokens on a prompt nobody reads.
        pidfile = Path(tmp) / "child.pid"
        launcher = ("import subprocess, sys; "
                    "p = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(60)']); "
                    f"open({str(pidfile)!r}, 'w').write(str(p.pid)); p.wait()")
        timeout, engine.TIMEOUT = engine.TIMEOUT, 2
        try:
            engine._spawn("stub", [sys.executable, "-c", launcher], Path(tmp), "")
            bad.append("spawn: a hung engine was not timed out")
        except engine.EngineError:
            pass
        finally:
            engine.TIMEOUT = timeout
        if not pidfile.exists():
            bad.append("spawn: the launcher never recorded its child; the timeout case tested nothing")
        elif _alive(pidfile):
            bad.append("spawn: a timed-out engine's child process is still running")
        # Interrupted while waiting (Ctrl-C, any exception): the engine is in its
        # own session, so nothing but this harness will ever stop it.
        selfpid = Path(tmp) / "self.pid"
        sleeper = (f"import os, time; open({str(selfpid)!r}, 'w').write(str(os.getpid())); "
                   "time.sleep(60)")

        class Interrupted(Exception):
            pass

        def interrupt(*_):
            raise Interrupted
        old = signal.signal(signal.SIGALRM, interrupt)
        signal.setitimer(signal.ITIMER_REAL, 1.0)
        try:
            engine._spawn("stub", [sys.executable, "-c", sleeper], Path(tmp), "")
            bad.append("spawn: the interrupt never arrived")
        except Interrupted:
            pass
        finally:
            signal.setitimer(signal.ITIMER_REAL, 0)
            signal.signal(signal.SIGALRM, old)
        if not selfpid.exists():
            bad.append("spawn: the interrupted engine never started; that case tested nothing")
        elif _alive(selfpid):
            bad.append("spawn: an interrupted engine is still running")
        # Terminated (a cancelled job signals the harness's group, which no longer
        # holds the engine): the engine goes down with the harness.
        for sig in (signal.SIGTERM, signal.SIGHUP):
            selfpid.unlink(missing_ok=True)
            killer = threading.Timer(1.0, os.kill, (os.getpid(), sig))
            killer.start()
            try:
                engine._spawn("stub", [sys.executable, "-c", sleeper], Path(tmp), "")
                bad.append(f"spawn: {sig.name} never arrived")
            except SystemExit:
                pass
            finally:
                killer.cancel()
            if not selfpid.exists():
                bad.append(f"spawn: the {sig.name} case's engine never started; it tested nothing")
            elif _alive(selfpid):
                bad.append(f"spawn: the engine outlived a {sig.name} to the harness")
        # Terminated while the engine is being started: the signal must still
        # take the engine down, not only the harness.
        selfpid.unlink(missing_ok=True)
        real_popen = engine.subprocess.Popen

        def popen_then_term(*a, **k):
            p = real_popen(*a, **k)
            for _ in range(50):                      # until the engine has started
                if selfpid.exists():
                    break
                time.sleep(0.05)
            os.kill(os.getpid(), signal.SIGTERM)
            time.sleep(0.2)                          # let the handler run in here
            return p
        engine.subprocess.Popen = popen_then_term
        try:
            engine._spawn("stub", [sys.executable, "-c", sleeper], Path(tmp), "")
            bad.append("spawn: a SIGTERM during start-up never arrived")
        except SystemExit:
            pass
        finally:
            engine.subprocess.Popen = real_popen
        if not selfpid.exists():
            bad.append("spawn: the start-up case's engine never started; it tested nothing")
        elif _alive(selfpid):
            bad.append("spawn: the engine outlived a SIGTERM that arrived while it started")
        # A descendant that left the group still holds the output pipes; the
        # timeout must still return on time rather than wait for it.
        escapee = ("import subprocess, sys; "
                   "subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(6)'], "
                   "start_new_session=True); import time; time.sleep(60)")
        timeout, engine.TIMEOUT = engine.TIMEOUT, 1
        start = time.monotonic()
        try:
            engine._spawn("stub", [sys.executable, "-c", escapee], Path(tmp), "")
        except engine.EngineError:
            pass
        finally:
            engine.TIMEOUT = timeout
        if time.monotonic() - start > 4:
            bad.append(f"spawn: a timeout took {time.monotonic() - start:.1f}s, waiting on "
                       "a descendant that left the engine's group")
    # claude gets no tools and no MCP servers; a denylist misses what it omits.
    seen: list[list[str]] = []

    def fake(eng, argv, cwd, stdin=None):
        seen.append(argv)
        return subprocess.CompletedProcess(argv, 0, '{"structured_output": {"ok": true}}', "")
    real, engine._spawn = engine._spawn, fake
    try:
        engine._ask("claude", "p", engine.strict(engine.SELFTEST))
    finally:
        engine._spawn = real
    argv = seen[0] if seen else []
    i = argv.index("--tools") if "--tools" in argv else -1
    if i < 0 or argv[i + 1] != "" or "--strict-mcp-config" not in argv:
        bad.append(f"claude is not run with --tools \"\" --strict-mcp-config: {argv}")
    return bad


def main() -> int:
    bad = []
    for i, (schema, value, ok) in enumerate(CASES):
        why = engine.conforms(schema, value)
        if (why is None) != ok:
            bad.append(f"case {i}: expected {'pass' if ok else 'fail'}, got {why!r}")
    for i, (schema, value) in enumerate(REFUSED):
        try:
            why = engine.conforms(schema, value)
        except engine.EngineError:
            continue
        bad.append(f"refused {i}: judged instead of refusing ({why!r})")
    real = engine._spawn
    for i, (schema, answer) in enumerate(RUN_REFUSED):
        out = json.dumps({"structured_output": answer})
        engine._spawn = lambda eng, argv, cwd, stdin=None, out=out: \
            subprocess.CompletedProcess(argv, 0, out, "")
        try:
            got = engine.run("claude", "p", schema)
            bad.append(f"run refused {i}: answered {got!r} to a schema it rewrote")
        except engine.EngineError:
            pass
        finally:
            engine._spawn = real
    for i, body in enumerate(NOT_JSON):
        try:
            got = engine._parse("stub", body)
            bad.append(f"not json {i}: {body} was read as {got!r}")
        except engine.EngineError:
            pass
    bad += spawn_cases()
    for b in bad:
        print("FAIL:", b)
    if bad:
        return 1
    print(f"conforms: {len(CASES)} judged, {len(REFUSED)} refused; "
          f"run: {len(RUN_REFUSED)} refused; {len(NOT_JSON)} non-JSON answers refused; "
          "spawn: 9 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
