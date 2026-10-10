#!/usr/bin/env python3
"""Offline checks of engine.conforms(): no engine is spawned.

`make engines` needs the CLIs installed; this does not, so the validator that
stands between an engine's answer and a verdict is exercised on every run.
"""
from __future__ import annotations

import sys
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
    ({"type": "string", "pattern": "^x"}, "xy", True),
    ({"type": "string", "pattern": "^x"}, "yx", False),
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
    ({"type": "string", "pattern": "("}, "x"),
    ({"type": "string", "pattern": 5}, "x"),
    ({"type": ""}, 5),
    ({"type": []}, 5),
    ({"type": [["x"]]}, "a"),
]


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
    for b in bad:
        print("FAIL:", b)
    if bad:
        return 1
    print(f"conforms: {len(CASES)} judged, {len(REFUSED)} refused")
    return 0


if __name__ == "__main__":
    sys.exit(main())
