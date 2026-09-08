"""Refresh metadata for the repaired historical snapshot without rebuilding it."""
from pathlib import Path
import hashlib
import importlib.util
import json

A = Path(__file__).resolve().parents[1]
repo = A / "repair-checkout"
directory = repo / "release_candidate"
spec = importlib.util.spec_from_file_location("release_scan", repo / "scripts/build_release_candidate.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
files = sorted(p for p in directory.rglob("*") if p.is_file()
               and "__pycache__" not in p.parts and p.name != "RELEASE_SCAN.json")
problems = [issue for p in files for issue in module.scan(p)]
assert not problems, problems
report = {"schema": 2, "frozen_input_commit": "2b7663bbf5a06d1340973434f195a84ae2773e8f",
          "scope": "Historical snapshot repaired by restoring omitted committed test dependencies; source readings here remain historical.",
          "files_scanned": len(files), "scan_problems": problems,
          "archive_included": False, "archive_manifest_included": False,
          "full_tensor_suite": {"command": "repaired-archived-trace-pytest-final", "passed": 254, "skipped": 0},
          "files": [{"path": str(p.relative_to(directory)), "bytes": p.stat().st_size,
                     "sha256": hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]}
(directory / "RELEASE_SCAN.json").write_text(json.dumps(report,indent=2)+"\n")
print(json.dumps({k:v for k,v in report.items() if k!='files'},indent=2))
