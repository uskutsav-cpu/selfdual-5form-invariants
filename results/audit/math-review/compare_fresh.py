#!/usr/bin/env python3
"""Compare saved new production rows to independently computed dual numbers.

This comparator itself imports no production module; production raw rows were
computed in a separate recorded root process. It only forms exact Python J*h.
"""
import json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
cells=json.loads((ROOT.parent/"root-review/fresh_cells.json").read_text())["cells"]
observed=json.loads((ROOT/"independent_fresh_results.json").read_text())
assert observed["complete"]
results=[]
for cell,independent in zip(cells,observed["cells"]):
    p=cell["prime"]
    source=ROOT.parent/f"root-review/fresh-witness-p{p}.json"
    production=json.loads(source.read_text())
    assert production["coordinates"]==cell["coordinates"] and production["seed"]==cell["seed"]
    rows=[]
    for i,(value,derivative) in enumerate(zip(independent["values"],independent["directional_derivatives"])):
        expected=sum(int(j)*int(h) for j,h in zip(production["jacobian"][i],cell["direction"]))%p
        row={"id":production["invariant_ids"][i],"independent_value":value,"production_value":production["values"][i],
             "independent_directional_derivative":derivative,"production_J_dot_direction":expected,
             "pass":value==production["values"][i] and derivative==expected}
        rows.append(row)
        assert row["pass"],row
    assert len(rows)==81
    results.append({"prime":p,"seed":cell["seed"],"rows":rows,"status":"PASS"})
(ROOT/"fresh_dual_comparison.json").write_text(json.dumps({"status":"PASS","cells":results},indent=2)+"\n")
print(json.dumps({"status":"PASS","cells":[{"prime":r["prime"],"seed":r["seed"],"values":81,"directional_derivatives":81} for r in results]},indent=2))
