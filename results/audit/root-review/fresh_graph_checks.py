"""Fresh production graph witnesses and independently constructed Lorentz tests.

This is not the independent derivative oracle: graph arithmetic and derivatives
come from the frozen production evaluator. Rank/determinant elimination and
Lorentz matrices/application are independently implemented here.
"""
from pathlib import Path
import hashlib
import json
import random
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "frozen-checkout/src"))
import numpy as np
from sdinv.certificate import context
from sdinv.contract import value_and_jacobian_row, planned_value
from sdinv.serialize import from_record


def elimination(matrix, p):
    a = [[int(x) % p for x in row] for row in matrix]
    rank, pivots, determinant = 0, [], 1
    for col in range(len(a[0])):
        pivot = next((i for i in range(rank, len(a)) if a[i][col]), None)
        if pivot is None:
            continue
        if pivot != rank:
            a[pivot], a[rank] = a[rank], a[pivot]
            determinant = -determinant
        value = a[rank][col]
        determinant = determinant * value % p
        inverse = pow(value, -1, p)
        for i in range(rank + 1, len(a)):
            scale = a[i][col] * inverse % p
            if scale:
                a[i] = [(x - scale*y) % p for x, y in zip(a[i], a[rank])]
        pivots.append(col)
        rank += 1
        if rank == len(a):
            break
    return rank, pivots, determinant if rank == len(a) else 0


def transform(form, matrix, p):
    # At most ten products of reduced residues <65521: safe exact int64 sum.
    for axis in range(5):
        form = np.moveaxis(np.tensordot(matrix, form, axes=(1, axis)), 0, axis) % p
    return form


def lorentz_matrices(seed, p):
    rng = random.Random(seed ^ 0x36A81B00D)
    result = []
    for kind in ["rotation", "rotation", "boost", "boost"]:
        while True:
            num = rng.randrange(1, 30)
            den = rng.randrange(num + 1, 60)
            divisor = den*den + num*num if kind == "rotation" else den*den - num*num
            if divisor % p:
                break
        ctop = den*den - num*num if kind == "rotation" else den*den + num*num
        c, s = ctop * pow(divisor, -1, p) % p, 2*num*den * pow(divisor, -1, p) % p
        i, j = rng.sample(range(1, 10), 2) if kind == "rotation" else (0, rng.randrange(1, 10))
        matrix = np.eye(10, dtype=np.int64)
        matrix[i, i], matrix[j, j] = c, c
        matrix[i, j], matrix[j, i] = s, (-s if kind == "rotation" else s) % p
        eta = np.diag([-1] + [1] * 9)
        assert np.array_equal(matrix.T @ eta @ matrix % p, eta % p)
        assert elimination(matrix.tolist(), p)[2] == 1
        assert s != 0
        result.append({"kind": kind, "plane": [i, j], "rational_parameter": [num, den],
                       "real_parameter_between_zero_and_one": 0 < num < den,
                       "matrix": matrix.tolist()})
    return result


def write(name, data):
    (ROOT / "root-review" / name).write_text(json.dumps(data, indent=2) + "\n")


manifest_bytes = (ROOT / "frozen-checkout/results/rank81_basis.json").read_bytes()
manifest = json.loads(manifest_bytes)
items = manifest["invariants"]
assert len(items) == 81
cells = json.loads((ROOT / "root-review/fresh_cells.json").read_text())["cells"]
witnesses = []
for cell in cells:
    p, seed = cell["prime"], cell["seed"]
    form, directions, compact = context(p, cell["coordinates"])
    rows, values, ranks = [], [], {}
    start = time.monotonic()
    for i, item in enumerate(items):
        value, row = value_and_jacobian_row(from_record(item["graph"]), form, directions,
                                           10, 5, True, p, max_memory_bytes=2*1024**3)
        assert sum(int(a)*int(b) for a,b in zip(row,cell["coordinates"])) % p == item["degree"] * int(value) % p
        rows.append(row.tolist())
        values.append(int(value))
        rank, pivots, det = elimination(rows, p)
        assert rank == i+1, (p,seed,item["id"],rank)
        ranks[str(item["degree"])] = rank
        if (i+1)%10 == 0 or i==80:
            print(f"prime {p} seed {seed}: rows {i+1}/81, rank {rank}", flush=True)
    minor = [[row[c] for c in pivots] for row in rows]
    assert elimination(minor, p)[2] == det != 0
    witness = {**cell, "basis_file_sha256": hashlib.sha256(manifest_bytes).hexdigest(),
               "invariant_ids": [i["id"] for i in items], "values": values,
               "selfdual_components": compact.tolist(), "jacobian": rows,
               "rank": rank, "pivot_columns": pivots, "determinant_mod_p": det,
               "cumulative_rank_by_degree": ranks, "seconds": time.monotonic()-start,
               "evaluation_method": "Frozen production value_and_jacobian_row; independent Python-integer elimination"}
    write(f"fresh-witness-p{p}.json", witness)
    witnesses.append(witness)
write("fresh_witnesses.json", {"witnesses": witnesses, "passed": True})

checks = []
for witness in witnesses:
    p, seed = witness["prime"], witness["seed"]
    form, _, _ = context(p, witness["coordinates"])
    for spec in lorentz_matrices(seed, p):
        transformed = transform(form, np.asarray(spec["matrix"],dtype=np.int64), p)
        matched = []
        for item, expected in zip(items, witness["values"]):
            actual = planned_value(from_record(item["graph"]), transformed, 10, 5, True, p,
                                   max_memory_bytes=2*1024**3)
            assert int(actual) == expected, (p,seed,spec,item["id"],expected,int(actual))
            matched.append(item["id"])
        checks.append({"prime":p,"seed":seed,**spec,"matched_ids":matched})
        print(f"prime {p}: {spec['kind']} plane {spec['plane']} parameter {spec['rational_parameter']}, all81 PASS", flush=True)
        write("fresh_lorentz_checks.json", {"passed":len(checks)==8,"checks":checks})
