"""Independently extract and bind the final portable payload before execution."""
from pathlib import Path
import hashlib
import json
import zipfile

A = Path(__file__).resolve().parents[1]
repo = A / "repair-checkout"
archive = repo / "release/classification/rank81-graph-classification.zip"
destination = A / "portable-repaired"
destination.mkdir(exist_ok=False)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    names = z.namelist()
    assert len(names) == len(set(names))
    assert all((destination / name).resolve().is_relative_to(destination.resolve()) for name in names)
    z.extractall(destination)
manifest = json.loads((destination / "manifest.json").read_text())
checks = []
for entry in manifest["files"]:
    path = destination / entry["path"]
    content = path.read_bytes()
    assert len(content) == entry["bytes"]
    assert hashlib.sha256(content).hexdigest() == entry["sha256"]
    assert content == (repo / entry["path"]).read_bytes(), entry["path"]
    checks.append(entry)
actual = {p.relative_to(destination).as_posix() for p in destination.rglob("*") if p.is_file()}
assert actual - {e["path"] for e in checks} == {"README.md", "manifest.json"}
checksum = hashlib.sha256(archive.read_bytes()).hexdigest()
assert (archive.parent / "SHA256SUMS").read_text().split()[0] == checksum
unchanged = []
for path in sorted((destination / "src/sdinv").glob("*.py")):
    rel = path.relative_to(destination)
    if path.name in {"published_degree8_invariants.py", "published_degree10_invariants.py"}:
        continue
    assert path.read_bytes() == (A / "frozen-checkout" / rel).read_bytes(), rel
    unchanged.append({"path": str(rel), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
for rel in ("scripts/verify_rank81.py", "results/rank81_basis.json", "results/rank81_certificate.json"):
    path = destination / rel
    assert path.read_bytes() == (A / "frozen-checkout" / rel).read_bytes()
    unchanged.append({"path": rel, "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
result = {"passed": True, "archive_sha256": checksum, "manifest_entries": len(checks),
          "all_payloads_match_repaired_repository": True, "files": checks,
          "unchanged_graph_engine_and_frozen_witnesses": unchanged,
          "graph_recomputation_evidence": "portable-frozen-recompute recomputed all four frozen cells with these identical graph modules and witnesses; corrected source modules are verified separately.",
          "unlisted_metadata": ["README.md", "manifest.json"],
          "metadata_coverage": "Both are covered by the full ZIP SHA256."}
(A / "release-review/extraction.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps({k:v for k,v in result.items() if k not in {"files", "unchanged_graph_engine_and_frozen_witnesses"}},indent=2))
