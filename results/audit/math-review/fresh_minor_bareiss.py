#!/usr/bin/env python3
"""Integer minors of newly independently recomputed full Jacobian rows."""
import json
from pathlib import Path
from bareiss_minors import bareiss

ROOT=Path(__file__).resolve().parent
reverse=json.loads((ROOT/"reverse_gradient_results.json").read_text())
assert reverse["status"]=="PASS"
rows=[]
for cell in reverse["cells"]:
    p=cell["prime"]
    production=json.loads((ROOT.parent/f"root-review/fresh-witness-p{p}.json").read_text())
    columns=production["pivot_columns"]
    matrix=[[row["jacobian_row"][column] for column in columns] for row in cell["records"][:81]]
    assert len(matrix)==81 and all(len(row)==81 for row in matrix)
    determinant,swaps=bareiss(matrix)
    residue=determinant%p
    record={"prime":p,"seed":cell["seed"],"pivot_columns":columns,"integer_determinant":str(determinant),
            "row_swaps":swaps,"determinant_mod_prime":residue,"root_determinant_mod_prime":production["determinant_mod_p"]}
    rows.append(record)
    assert residue and residue==production["determinant_mod_p"],record
    print(json.dumps({k:v for k,v in record.items() if k not in ["pivot_columns","integer_determinant"]}),flush=True)
(ROOT/"fresh_minor_bareiss_results.json").write_text(json.dumps({"status":"PASS","cells":rows},indent=2)+"\n")
