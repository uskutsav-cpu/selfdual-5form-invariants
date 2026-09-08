"""Seal post-build logs and sidecar without changing the tested ZIP payload."""
from pathlib import Path
import hashlib
import json
import shlex
import shutil
import zipfile

A = Path(__file__).resolve().parents[1]
REPO = A / "repair-checkout"
OLD = A.parent / "independent-audit-20260907-01"
audit = REPO / "audit/20260907"
extraction = json.loads((A / "release-review/extraction.json").read_text())
names = ["repaired-portable-extract-and-hashes", "repaired-portable-full-pytest",
         "repaired-portable-independent-certificates", "repaired-portable-octic-cli",
         "repaired-portable-decic-cli"]
checks = []
for name in names:
    directory = A / "commands" / name
    record = json.loads((directory / "command.json").read_text())
    assert record["status"] == "completed" and record["exit_code"] == 0
    for filename, info in record["logs"].items():
        assert hashlib.sha256((directory / filename).read_bytes()).hexdigest() == info["sha256"]
    checks.append({"name": name, **record})
archive = REPO / "release/classification/rank81-graph-classification.zip"
assert hashlib.sha256(archive.read_bytes()).hexdigest() == extraction["archive_sha256"]
with zipfile.ZipFile(archive) as z:
    manifest = json.loads(z.read("manifest.json"))
    for entry in manifest["files"]:
        content = z.read(entry["path"])
        assert content == (REPO / entry["path"]).read_bytes()
        assert content == (A / "portable-repaired" / entry["path"]).read_bytes()
        assert hashlib.sha256(content).hexdigest() == entry["sha256"]
report = {"schema": 1, "passed": True, "archive_sha256": extraction["archive_sha256"],
          "manifest_entries_verified": extraction["manifest_entries"],
          "tests_passed": 30, "tests_skipped": 0, "tests_failed": 0,
          "post_test_payload_unchanged": True, "checks": checks,
          "graph_recomputation_scope": extraction["graph_recomputation_evidence"],
          "unchanged_graph_engine_and_frozen_witnesses": extraction["unchanged_graph_engine_and_frozen_witnesses"],
          "source_identity_assumptions": "Published Hilbert upper bounds7/14 and analytic tensor invariance; no independent Hilbert derivation.",
          "metadata_scope": "Post-build sidecar intentionally outside ZIP to avoid circular hashing. Full historical suites and raw command logs are in the Git repository."}
(archive.parent / "PORTABLE_VERIFICATION.json").write_text(json.dumps(report,indent=2)+"\n")

def copy(source, target):
    target.parent.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(source,target)

body = OLD / "INDEPENDENT_AUDIT.md"
delivered = A.parent.parent / "outputs/INDEPENDENT_AUDIT.md"
assert delivered.read_bytes().startswith(body.read_bytes())
assert hashlib.sha256(delivered.read_bytes()).hexdigest() == "52d3b5d58e02d0d3c9774938cd1bcc5078c1f94bf008ad66ca7f86f633d6db47"
copy(body, audit / "phase01/ORIGINAL_REPORT_BODY.md")
copy(delivered, audit / "phase01/INDEPENDENT_AUDIT.md")
(audit / "phase01/REPORT_PROVENANCE.json").write_text(json.dumps({
    "body_sha256": hashlib.sha256(body.read_bytes()).hexdigest(),
    "delivered_report_sha256": hashlib.sha256(delivered.read_bytes()).hexdigest(),
    "difference": "The originally delivered report appends the exact command appendix to the unchanged original failure-report body. Both are preserved."},indent=2)+"\n")

for source in (A / "release-review").glob("*"):
    if source.is_file():
        copy(source, audit / "phase02/release-review" / source.name)
for source in (A / "literature-review").glob("*"):
    if source.is_file() and source.suffix in {".py", ".json", ".md", ".diff"}:
        if "retrieval-log" not in source.name and "metadata-log" not in source.name:
            copy(source, audit / "phase02/literature-review" / source.name)
records = []
readable = ["# Exact audit commands", "", "Original working directories are evidence; setup/edit commands with stdin are qualified in INDEPENDENT_AUDIT.md.", ""]
for phase, origin in (("phase01", OLD), ("phase02", A)):
    for path in sorted((origin / "commands").glob("*/command.json")):
        record = json.loads(path.read_text())
        assert record["status"] == "completed", path
        for filename, info in record["logs"].items():
            assert hashlib.sha256((path.parent / filename).read_bytes()).hexdigest() == info["sha256"]
        for filename in ("command.json", "stdout.log", "stderr.log"):
            copy(path.parent / filename, audit / phase / "commands" / path.parent.name / filename)
        records.append({"phase":phase,"name":path.parent.name,**record})
        readable += [f"## {phase}/{path.parent.name}","",f"Working directory: `{record['cwd']}`","","```sh",shlex.join(record['argv']),"```","",f"Exit: {record['exit_code']}; wall seconds: {record['seconds']:.6f}.",""]
(audit / "COMMAND_INDEX.json").write_text(json.dumps({"schema":1,"commands":records},indent=2)+"\n")
(audit / "COMMANDS.md").write_text("\n".join(readable))
entries = []
for base in (audit, REPO / "results/audit"):
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.name != "EVIDENCE_MANIFEST.json" and "__pycache__" not in path.parts:
            entries.append({"path":str(path.relative_to(REPO)),"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
for name in ("INDEPENDENT_AUDIT.md", "results/classification_validation.json", "release/classification/PORTABLE_VERIFICATION.json"):
    path=REPO/name
    entries.append({"path":name,"bytes":path.stat().st_size,"sha256":hashlib.sha256(path.read_bytes()).hexdigest()})
(audit / "EVIDENCE_MANIFEST.json").write_text(json.dumps({"schema":1,"files":entries},indent=2)+"\n")
print(json.dumps({"portable_passed":True,"portable_tests":30,"archive_sha256":report['archive_sha256'],"command_records":len(records),"evidence_files":len(entries)},indent=2))
