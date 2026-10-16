#!/usr/bin/env python3
"""Offline checks of engine.conforms(): no engine is spawned.

`make engines` needs the CLIs installed; this does not, so the validator that
stands between an engine's answer and a verdict is exercised on every run.
"""
from __future__ import annotations

import subprocess
import sys
import tempfile
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
    ({"not": {"const": 1}}, 1, False),
    ({"type": "array", "minItems": 1, "items": {"type": "string"}}, [], False),
    ({"type": "array", "items": False}, [1], False),
    ({"properties": {"x": False}}, {"x": 1}, False),
    ({"type": "string", "maxLength": 2}, "abc", False),
    ({"type": "number", "minimum": 0}, -1, False),
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
    bad += spawn_cases()
    for b in bad:
        print("FAIL:", b)
    if bad:
        return 1
    print(f"conforms: {len(CASES)} judged, {len(REFUSED)} refused; spawn: 2 cases")
    return 0


if __name__ == "__main__":
    sys.exit(main())
