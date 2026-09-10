#!/usr/bin/env python3
"""UNEXECUTED provenance replay only; no repository imports or tensor evaluations.
Run from any directory after authorization to resume evidence checking.
"""
from pathlib import Path
import hashlib
import json

ROOT = Path(__file__).resolve().parent
EVIDENCE = ROOT / "source-conflict-evidence.json"
assert hashlib.sha256(EVIDENCE.read_bytes()).hexdigest() == "c6416921df07c451275a3c27961e56bdafe5713909128cd6be32d923deaac2c7"
evidence = json.loads(EVIDENCE.read_text())
for relative, expected in evidence["hashes"].items():
    path = ROOT.parent / relative
    actual = hashlib.sha256(path.read_bytes()).hexdigest()
    if actual != expected:
        raise AssertionError((relative, expected, actual))
    print(f"SHA256 OK: {relative}")
for entry in evidence["source_excerpts"]:
    print(entry["text"])
for entry in evidence["frozen_code_excerpts"]:
    print(entry["text"])
print(evidence["scientific_limit"])
