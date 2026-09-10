"""Collect actual logged verifier outcomes and check untouched originals."""
import hashlib
import json
from pathlib import Path

own = Path(__file__).resolve().parent
phase = own.parent
manifest = json.loads((own / "negative-tests/manifest.json").read_text())
for filename, expected in manifest["authoritative_sha256_before"].items():
    assert hashlib.sha256(Path(filename).read_bytes()).hexdigest() == expected
expected_exits = {
    "math_verify_exact_source_certificate": 0,
    "math_portable_all_saved_evidence": 0,
    "math_portable_source_only": 0,
    "math_negative_source_integer": 1,
    "math_negative_canonical_map": 1,
}
commands = {}
for name, expected_exit in expected_exits.items():
    command = json.loads((phase / "commands" / name / "command.json").read_text())
    assert command["exit_code"] == expected_exit
    commands[name] = {k: command[k] for k in ["exit_code", "seconds", "logs"]}
assert 'exact_integer_numerator_evaluations' in (phase / "commands/math_negative_source_integer/stderr.log").read_text()
assert 'canonical degree8 map differs from exact certificate' in (phase / "commands/math_negative_canonical_map/stderr.log").read_text()
result = {
    "status": "PASS",
    "certificate_sha256": json.loads((own / "source_crt_independent_verification.json").read_text())["certificate_sha256"],
    "wrapper_sha256": hashlib.sha256((phase / "repair-checkout/scripts/verify_independent_audit.py").read_bytes()).hexdigest(),
    "commands": commands,
    "negative_test_assertions": {
        "changed_integer_rejected": True,
        "changed_canonical_coefficient_rejected": True,
        "authoritative_originals_unchanged": True,
        "negative_tests_use_isolated_copies": True,
    },
    "scope": "Low-cost saved-evidence algebra, consistency, and hashes; no tensor recomputation or independent Hilbert-series derivation."
}
(own / "portable_verification_results.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
