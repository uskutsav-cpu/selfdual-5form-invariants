"""Install the separately authored portable wrapper and current checker."""
import hashlib
import json
from pathlib import Path
import shutil

own = Path(__file__).resolve().parent
repo = own.parent / "repair-checkout"
target = repo / "scripts/verify_independent_audit.py"
if target.exists():
    raise RuntimeError("Refusing to overwrite an existing wrapper")
shutil.copyfile(own / "portable_wrapper_draft.py", target)
evidence = repo / "results/audit/math-review"
evidence.mkdir(parents=True, exist_ok=True)
files = ["verify_source_crt.py", "source_bound_review.py", "source_bound_review.json",
         "SOURCE_CRT_METHOD_REVIEW.md", "source_crt_independent_verification.json"]
for name in files:
    shutil.copyfile(own / name, evidence / name)
result = {str(path.relative_to(repo)): hashlib.sha256(path.read_bytes()).hexdigest()
          for path in [target] + [evidence / name for name in files]}
(own / "portable_installation.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
