"""Copy authored audit evidence, preserving bytes and excluding cited works."""
from pathlib import Path
import hashlib
import json
import shutil
import shlex

A = Path(__file__).resolve().parents[1]
REPO = A / "repair-checkout"
OLD = A.parent / "independent-audit-20260907-01"


def copy(source, target):
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


for directory in ("math-review", "root-review"):
    for source in sorted((A / directory).glob("*")):
        if source.is_file() and source.suffix in {".py", ".json", ".md"}:
            copy(source, REPO / "results/audit" / directory / source.name)

# The original failed report is preserved byte-for-byte. Published paper
# PDFs, TeX, screenshots, raw retrieved full text and web responses stay local.
for name in ("INDEPENDENT_AUDIT.md", "STOP.json", "START.json", "COMMAND_INDEX.json", "COMMANDS.md", "run_command.py"):
    copy(OLD / name, REPO / "audit/20260907/phase01" / name)
for directory in ("math-review", "source-review", "literature-review"):
    for source in sorted((OLD / directory).glob("*")):
        if not source.is_file() or source.suffix not in {".py", ".json", ".md"}:
            continue
        if any(word in source.name for word in ("web-retrieval", "source-download")):
            continue
        copy(source, REPO / "audit/20260907/phase01" / directory / source.name)
for source in sorted((A / "literature-review").glob("*")):
    if source.is_file() and source.suffix in {".py", ".json", ".md", ".diff"}:
        if "retrieval-log" not in source.name and "metadata-log" not in source.name:
            copy(source, REPO / "audit/20260907/phase02/literature-review" / source.name)
copy(A / "run_command.py", REPO / "audit/20260907/phase02/run_command.py")

# Command records include the exact original working directories. No shell
# environment, credentials or cited full-paper downloads are copied here.
for phase, origin in (("phase01", OLD), ("phase02", A)):
    for directory in sorted((origin / "commands").iterdir()):
        metadata = directory / "command.json"
        if not metadata.is_file():
            continue
        record = json.loads(metadata.read_text())
        if record.get("status") != "completed":
            continue
        for name in ("command.json", "stdout.log", "stderr.log"):
            copy(directory / name, REPO / "audit/20260907" / phase / "commands" / directory.name / name)

records = []
commands_md = ["# Exact audit commands", "", "Original working directories are retained as evidence. Scientific scripts are preserved under results/audit/.", ""]
for phase, origin in (("phase01", OLD), ("phase02", A)):
    for path in sorted((origin / "commands").glob("*/command.json")):
        record = json.loads(path.read_text())
        if record.get("status") != "completed":
            continue
        for name, info in record["logs"].items():
            assert hashlib.sha256((path.parent / name).read_bytes()).hexdigest() == info["sha256"], path
        records.append({"phase": phase, "name": path.parent.name, **record})
        commands_md += [f"## {phase}/{path.parent.name}", "", f"Working directory: `{record['cwd']}`", "", "```sh", shlex.join(record['argv']), "```", "",
                        f"Exit: {record['exit_code']}; wall seconds: {record['seconds']:.6f}.", ""]
(REPO / "audit/20260907/COMMAND_INDEX.json").write_text(json.dumps({"schema": 1, "commands": records},indent=2)+"\n")
(REPO / "audit/20260907/COMMANDS.md").write_text("\n".join(commands_md))

manifest = []
for base in (REPO / "audit/20260907", REPO / "results/audit"):
    for path in sorted(base.rglob("*")):
        if path.is_file() and path.name != "EVIDENCE_MANIFEST.json":
            manifest.append({"path": str(path.relative_to(REPO)), "bytes": path.stat().st_size,
                             "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
for name in ("INDEPENDENT_AUDIT.md", "results/classification_validation.json"):
    path = REPO / name
    if path.is_file():
        manifest.append({"path": name, "bytes": path.stat().st_size,
                         "sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
(REPO / "audit/20260907/EVIDENCE_MANIFEST.json").write_text(json.dumps({"schema": 1, "files": manifest}, indent=2) + "\n")
print(f"Copied and hashed {len(manifest)} authored evidence files; cited full works excluded.")
