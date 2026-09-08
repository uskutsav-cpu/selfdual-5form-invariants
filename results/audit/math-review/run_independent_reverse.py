#!/usr/bin/env python3
"""Validate independent reverse rows; certify degree12 polynomial rank."""
import json
from pathlib import Path
import random
import secrets
import time

from bareiss_minors import bareiss
from efficient_oracle import PointEngine,items81,items12,products12
from independent_oracle import plan
from independent_reverse import reverse_gradient
from run_independent_checks import add_row,write

ROOT=Path(__file__).resolve().parent
CELLS=json.loads((ROOT.parent/"root-review/fresh_cells.json").read_text())["cells"]


def polynomial_rows(low_values,low_rows,high_rows,p):
    q,a,b,*o=low_values
    gq,ga,gb,*go=low_rows
    combine=lambda terms:[sum(coef*row[j] for coef,row in terms)%p for j in range(126)]
    products=[combine([(3*q*q,gq)]),combine([(2*a,ga)]),combine([(b,ga),(a,gb)]),combine([(2*b,gb)])]
    products += [combine([(value,gq),(q,row)]) for value,row in zip(o,go)]
    return products+high_rows


def matrix_evidence(matrix,p):
    pivots=[]
    for row in matrix:add_row(pivots,row,p)
    columns=[c for c,_ in pivots]
    evidence={"rank":len(pivots),"pivot_columns":columns}
    if len(pivots)==72:
        minor=[[row[c] for c in columns] for row in matrix]
        det,swaps=bareiss(minor)
        residue=det%p
        assert residue
        evidence.update(integer_minor_determinant=str(det),determinant_mod_prime=residue,row_swaps=swaps)
    return evidence


def main():
    base=items81()
    all_items=base+items12()[60:]
    plans=[plan(item) for item in all_items]
    independent=json.loads((ROOT/"independent_fresh_results.json").read_text())
    assert independent["complete"]
    result={"implementation":"Independent reverse adjoint tape and direct sparse pullback, sharing independent forward kernel only", "cells":[]}
    polynomial={"method":"Stacked independently evaluated gradients of 10 products + 62 graph polynomials", "fields":[]}
    for ci,cell in enumerate(CELLS):
        p=cell["prime"]
        engine=PointEngine(cell["coordinates"],p)
        extra_dual=PointEngine(cell["coordinates"],p,cell["direction"])
        production=json.loads((ROOT.parent/f"root-review/fresh-witness-p{p}.json").read_text())
        output={"prime":p,"seed":cell["seed"],"coordinates":cell["coordinates"],"direction":cell["direction"],"records":[]}
        result["cells"].append(output)
        values=[]
        gradients=[]
        for i,(item,selected_plan) in enumerate(zip(all_items,plans)):
            start=time.monotonic()
            value,row=reverse_gradient(engine,item,selected_plan)
            tangent=sum(a*b for a,b in zip(row,cell["direction"]))%p
            assert sum(a*b for a,b in zip(row,cell["coordinates"]))%p==item["degree"]*value%p,(item["id"],"Euler")
            if i<81:
                if not (value==independent["cells"][ci]["values"][i]==production["values"][i]
                        and tangent==independent["cells"][ci]["directional_derivatives"][i]
                        and row==production["jacobian"][i]):
                    write("reverse_discrepancy.json",{"prime":p,"id":item["id"],"observed_value":value,
                          "observed_row":row,"observed_tangent":tangent,"production_value":production["values"][i],
                          "production_row":production["jacobian"][i],"independent_forward_value":independent["cells"][ci]["values"][i],
                          "independent_forward_tangent":independent["cells"][ci]["directional_derivatives"][i]})
                assert value==independent["cells"][ci]["values"][i]==production["values"][i],(item["id"],"value")
                assert tangent==independent["cells"][ci]["directional_derivatives"][i],(item["id"],"forward dual")
                assert row==production["jacobian"][i],(item["id"],"full production row")
            else:
                independent_value,independent_tangent=extra_dual.evaluate(item,selected_plan)
                assert value==independent_value and tangent==independent_tangent,(item["id"],"extra forward dual")
            record={"id":item["id"],"value":value,"jacobian_row":row,"J_dot_direction":tangent,
                    "checks":"Euler, independent forward dual, full production row" if i<81 else "Euler, independent forward dual",
                    "seconds":time.monotonic()-start}
            values.append(value)
            gradients.append(row)
            output["records"].append(record)
            output["engine_stats"]=dict(engine.stats)
            write("reverse_gradient_results.json",result)
            print(json.dumps({"prime":p,"id":item["id"],"checks":record["checks"],"seconds":record["seconds"]}),flush=True)
        output["complete"]=True
        write("reverse_gradient_results.json",result)
        rows=polynomial_rows(values[:9],gradients[:9],gradients[21:],p)
        assert len(rows)==72
        # This first point has all83 graph rows, including both final degree12
        # graphs; it is a single-field starting block, not a mixed-prime matrix.
        field={"prime":p,"points":[{"seed":cell["seed"],"coordinates":cell["coordinates"],
                                    "values":products12(values[:9],p)+values[21:]}],"stacked_gradient":rows}
        field.update(matrix_evidence(rows,p))
        polynomial["fields"].append(field)
        write("degree12_polynomial_gradient_certificate.json",polynomial)
        point_items=base[:9]+all_items[21:]
        point_plans=plans[:9]+plans[21:]
        while field["rank"]<72 and len(field["points"])<4:
            seed=secrets.randbits(128)
            rng=random.Random(seed)
            coordinates=[rng.randrange(p) for _ in range(126)]
            point={"seed":seed,"coordinates":coordinates,"coordinate_generator":"Python random.Random(fresh secrets.randbits(128) seed), randrange(prime)","records":[]}
            field["points"].append(point)
            write("degree12_polynomial_gradient_certificate.json",polynomial)
            point_engine=PointEngine(coordinates,p)
            point_values,point_rows=[],[]
            for item,selected_plan in zip(point_items,point_plans):
                start=time.monotonic()
                value,row=reverse_gradient(point_engine,item,selected_plan)
                assert sum(a*b for a,b in zip(row,coordinates))%p==item["degree"]*value%p
                point_values.append(value)
                point_rows.append(row)
                point["records"].append({"id":item["id"],"value":value,"jacobian_row":row,"seconds":time.monotonic()-start})
                write("degree12_polynomial_gradient_certificate.json",polynomial)
                print(json.dumps({"polynomial_prime":p,"point":len(field["points"])-1,"id":item["id"],"seconds":time.monotonic()-start}),flush=True)
            new_rows=polynomial_rows(point_values[:9],point_rows[:9],point_rows[9:],p)
            point["values"]=products12(point_values[:9],p)+point_values[9:]
            point["engine_stats"]=dict(point_engine.stats)
            field["stacked_gradient"]=[a+b for a,b in zip(field["stacked_gradient"],new_rows)]
            field.update(matrix_evidence(field["stacked_gradient"],p))
            write("degree12_polynomial_gradient_certificate.json",polynomial)
            print(json.dumps({"polynomial_prime":p,"points":len(field["points"]),"rank":field["rank"],"determinant_mod_prime":field.get("determinant_mod_prime")}),flush=True)
        assert field["rank"]==72,(p,"degree12 rank shortfall",field["rank"])
        field["status"]="PASS"
        write("degree12_polynomial_gradient_certificate.json",polynomial)
    result["status"]="PASS"
    polynomial["status"]="PASS"
    write("reverse_gradient_results.json",result)
    write("degree12_polynomial_gradient_certificate.json",polynomial)


if __name__=="__main__":main()
