"""Create isolated corruptions; never mutate authoritative evidence."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path

own = Path(__file__).resolve().parent
source = own.parent / "source-review"
repo = own.parent / "repair-checkout"
negative = own / "negative-tests"
negative.mkdir(exist_ok=True)

authoritative = [source / "exact-source-evaluation-certificate.json"] + [
    repo / f"results/order{degree}_change_of_basis.json" for degree in [8, 10]
]
hashes = {str(path): hashlib.sha256(path.read_bytes()).hexdigest() for path in authoritative}
cert = json.loads(authoritative[0].read_text())
cert["exact_integer_numerator_evaluations"]["atlas10"][0][0] += 1
(negative / "changed-integer-certificate.json").write_text(json.dumps(cert, indent=2) + "\n")

temporary_results = negative / "canonical-repo/results"
temporary_results.mkdir(parents=True, exist_ok=True)
for degree in [8, 10]:
    data = json.loads((repo / f"results/order{degree}_change_of_basis.json").read_text())
    if degree == 8:
        data["literature_to_graph"][0][0] = str(Fraction(data["literature_to_graph"][0][0]) + 1)
    (temporary_results / f"order{degree}_change_of_basis.json").write_text(json.dumps(data, indent=2) + "\n")
result = {"authoritative_sha256_before": hashes,
          "integer_mutation": "exact_integer_numerator_evaluations.atlas10[0][0] += 1",
          "canonical_mutation": "degree8 literature_to_graph[0][0] += 1",
          "originals_modified": False}
(negative / "manifest.json").write_text(json.dumps(result, indent=2) + "\n")
print(json.dumps(result, indent=2))
