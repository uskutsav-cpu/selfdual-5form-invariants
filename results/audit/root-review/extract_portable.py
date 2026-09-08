"""Extract the frozen portable archive and independently check all manifest hashes."""
from pathlib import Path
import hashlib
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
archive = ROOT / "frozen-checkout/release/classification/rank81-graph-classification.zip"
destination = ROOT / "portable-frozen"
destination.mkdir(exist_ok=False)
with zipfile.ZipFile(archive) as z:
    assert z.testzip() is None
    for name in z.namelist():
        assert (destination / name).resolve().is_relative_to(destination.resolve()), name
    z.extractall(destination)
manifest = json.loads((destination / "manifest.json").read_text())
checks = []
for item in manifest["files"]:
    payload = (destination / item["path"]).read_bytes()
    digest = hashlib.sha256(payload).hexdigest()
    assert digest == item["sha256"] and len(payload) == item["bytes"], item["path"]
    checks.append({"path":item["path"],"sha256":digest,"bytes":len(payload)})
listed = {i["path"] for i in checks}
actual = {p.relative_to(destination).as_posix() for p in destination.rglob('*') if p.is_file()}
unlisted = sorted(actual-listed)
assert set(unlisted) == {"manifest.json", "README.md"}, unlisted
result = {"passed":True,"archive_sha256":hashlib.sha256(archive.read_bytes()).hexdigest(),
          "verified_manifest_entries":len(checks),"checks":checks,
          "unlisted_files":unlisted,"manifest_coverage_limit":"README.md and manifest.json are not payload-hashed by the frozen manifest; archive hash covers both."}
(ROOT / "root-review/portable_manifest_verification.json").write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='checks'},indent=2))
