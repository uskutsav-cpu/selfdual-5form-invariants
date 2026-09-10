#!/usr/bin/env python3
import argparse
from collections import Counter
import hashlib
import json
from math import comb
from pathlib import Path
import random
import secrets
import time

from bareiss_minors import bareiss
from efficient_oracle import PointEngine, items81, items12, relabel, products12
from independent_oracle import plan, arithmetic_selftest

ROOT = Path(__file__).resolve().parent
CELL_FILE = ROOT.parent / "root-review/fresh_cells.json"


def write(name, data):
    (ROOT / name).write_text(json.dumps(data, indent=2) + "\n")


def fresh():
    arithmetic_selftest()
    items = items81()
    plans = [plan(item) for item in items]
    cells = json.loads(CELL_FILE.read_text())["cells"]
    result = {"input_sha256": hashlib.sha256(CELL_FILE.read_bytes()).hexdigest(),
              "repository_imports": False, "method": "independent forward dual numbers", "cells": []}
    for ci, cell in enumerate(cells):
        p = cell["prime"]
        engine = PointEngine(cell["coordinates"], p, cell["direction"])
        record = {"prime": p, "seed": cell["seed"], "values": [], "directional_derivatives": [], "rows": []}
        result["cells"].append(record)
        for item, selected_plan in zip(items, plans):
            start = time.monotonic()
            value, derivative = engine.evaluate(item, selected_plan)
            row = {"id": item["id"], "value": value, "derivative": derivative, "seconds": time.monotonic()-start}
            record["values"].append(value)
            record["directional_derivatives"].append(derivative)
            record["rows"].append(row)
            record["engine_stats"] = dict(engine.stats)
            write("independent_fresh_results.json", result)
            print(json.dumps({"cell": ci, "prime": p, **row}), flush=True)
        record["complete"] = True
        write("independent_fresh_results.json", result)
    result["complete"] = True
    write("independent_fresh_results.json", result)


def signs():
    items = items81()
    cell = json.loads(CELL_FILE.read_text())["cells"][0]
    p = cell["prime"]
    fresh_result = json.loads((ROOT / "independent_fresh_results.json").read_text())["cells"][0]
    assert fresh_result["complete"]
    engine = PointEngine(cell["coordinates"], p)
    records = []
    for index, item in enumerate(items):
        n = item["degree"]
        structural = []
        candidates = []
        for i in range(n-1):
            permutation = list(range(n))
            permutation[i], permutation[i+1] = permutation[i+1], permutation[i]
            changed, sign = relabel(item, permutation)
            restored, backsign = relabel(changed, permutation)
            assert restored["graph"] == item["graph"] and sign * backsign == 1
            structural.append({"adjacent_vertices": [i, i+1], "induced_sign": sign})
            candidates.append((permutation, changed, sign))
        permutation, changed, sign = next((c for c in candidates if c[2] == -1), candidates[len(candidates)//2])
        # Check the sign cocycle under a further cyclic permutation.
        rotation = list(range(1,n)) + [0]
        twice, second_sign = relabel(changed, rotation)
        direct, composed_sign = relabel(item, [rotation[v] for v in permutation])
        assert twice["graph"] == direct["graph"] and sign*second_sign == composed_sign
        start = time.monotonic()
        observed = engine.evaluate(changed)[0]
        expected = sign * fresh_result["values"][index] % p
        assert observed == expected, (item["id"], "relabeling mismatch", observed, expected)
        # All 81 graphs also get a one-vertex odd slot swap (five-form sign).
        swapped = engine.evaluate(item, slot_permutations={0: [1,0,2,3,4]})[0]
        expected_swapped = -fresh_result["values"][index] % p
        assert swapped == expected_swapped, (item["id"], "slot-swap mismatch", swapped, expected_swapped)
        record = {"id": item["id"], "adjacent_swap_checks": structural,
                  "numeric_vertex_permutation": permutation, "numeric_induced_sign": sign,
                  "numeric_observed": observed, "numeric_expected": expected,
                  "odd_slot_swap_observed": swapped, "odd_slot_swap_expected": expected_swapped,
                  "sign_cocycle": True, "seconds": time.monotonic()-start}
        records.append(record)
        write("permutation_sign_results.json", {"prime": p, "seed": cell["seed"], "records": records,
                                                "engine_stats": dict(engine.stats), "complete": len(records)==81})
        print(json.dumps({k:v for k,v in record.items() if k != "adjacent_swap_checks"}), flush=True)


def interpolate():
    items = items81()
    indices = [0,2,3,9,21]
    cell = json.loads(CELL_FILE.read_text())["cells"][0]
    p = cell["prime"]
    fresh_result = json.loads((ROOT / "independent_fresh_results.json").read_text())["cells"][0]
    plans = {i:plan(items[i]) for i in indices}
    values = {i:[] for i in indices}
    for t in range(13):
        coordinates = [(a+t*h)%p for a,h in zip(cell["coordinates"],cell["direction"])]
        engine = PointEngine(coordinates,p)
        for index in indices:
            if t <= items[index]["degree"]:
                values[index].append(engine.evaluate(items[index],plans[index])[0])
        print(json.dumps({"interpolation_t":t,"evaluated_ids":[items[i]["id"] for i in indices if t<=items[i]["degree"]]}),flush=True)
    rows=[]
    for index in indices:
        n=items[index]["degree"]
        weights=[-sum(pow(j,-1,p) for j in range(1,n+1))%p]
        weights += [((-1)**(j+1))*comb(n,j)*pow(j,-1,p)%p for j in range(1,n+1)]
        derivative=sum(w*v for w,v in zip(weights,values[index]))%p
        expected=fresh_result["directional_derivatives"][index]
        assert derivative==expected,(items[index]["id"],"interpolation derivative mismatch",derivative,expected)
        rows.append({"id":items[index]["id"],"degree":n,"values_at_t_0_through_degree":values[index],
                     "exact_derivative_weights":weights,"interpolated_derivative":derivative,"dual_derivative":expected})
    write("interpolation_derivative_results.json",{"prime":p,"seed":cell["seed"],"records":rows,"status":"PASS"})
    print(json.dumps({"interpolation_derivatives":"PASS","graphs":len(rows)}),flush=True)


def add_row(pivots,row,prime):
    row=list(row)
    for col,old in pivots:
        scalar=row[col]
        if scalar:
            row=[(a-scalar*b)%prime for a,b in zip(row,old)]
    pivot=next((i for i,x in enumerate(row) if x),None)
    if pivot is None:
        return False
    inverse=pow(row[pivot],-1,prime)
    normalized=[x*inverse%prime for x in row]
    pivots.append((pivot,normalized))
    pivots.sort(key=lambda entry:entry[0])
    return True


def polynomial(count):
    prime=json.loads(CELL_FILE.read_text())["new_prime"]
    low=items81()[:9]
    high=items12()
    items=low+high
    plans=[plan(item) for item in items]
    seed=secrets.randbits(128)
    rng=random.Random(seed)
    points=[[rng.randrange(prime) for _ in range(126)] for _ in range(count)]
    columns=["I4_1^3","I6_1^2","I6_1*I6_2","I6_2^2"]+[f"I4_1*I8_{k}" for k in range(1,7)]+[x["id"] for x in high]
    result={"prime":prime,"seed":seed,"coordinate_generator":"Python random.Random(fresh secrets.randbits(128) seed), randrange(prime)",
            "coordinates":points,"columns":columns,"matrix":[],"sample_records":[],"complete":False}
    write(f"polynomial_rank_{count}.json",result)
    pivots=[]
    selected=[]
    for index,coordinates in enumerate(points):
        start=time.monotonic()
        engine=PointEngine(coordinates,prime)
        values=[engine.evaluate(item,selected_plan)[0] for item,selected_plan in zip(items,plans)]
        row=products12(values[:9],prime)+values[9:]
        assert len(row)==72
        result["matrix"].append(row)
        if add_row(pivots,row,prime):
            selected.append(index)
        record={"sample":index,"rank":len(pivots),"seconds":time.monotonic()-start,"engine_stats":dict(engine.stats)}
        result["sample_records"].append(record)
        result["rank"]=len(pivots)
        result["pivot_columns"]=[p for p,_ in pivots]
        result["independent_sample_rows"]=selected
        write(f"polynomial_rank_{count}.json",result)
        print(json.dumps(record),flush=True)
    result["complete"]=True
    if len(pivots)==72:
        determinant,swaps=bareiss([result["matrix"][i] for i in selected])
        result["integer_minor_determinant"]=str(determinant)
        result["determinant_mod_prime"]=determinant%prime
        assert result["determinant_mod_prime"]!=0
        result["status"]="PASS: 10 products + 62 connected graph polynomials linearly independent"
    else:
        result["status"]="BENCHMARK" if count<72 else "RANK_SHORTFALL"
    write(f"polynomial_rank_{count}.json",result)
    print(json.dumps({"status":result["status"],"rank":len(pivots),"prime":prime,"samples":count}),flush=True)


def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("mode",choices=["fresh","signs","interpolate","polynomial"])
    parser.add_argument("--samples",type=int,default=72)
    args=parser.parse_args()
    if args.mode=="fresh": fresh()
    elif args.mode=="signs": signs()
    elif args.mode=="interpolate": interpolate()
    elif args.mode=="polynomial": polynomial(args.samples)


if __name__=="__main__": main()
