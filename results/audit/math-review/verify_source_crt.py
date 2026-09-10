#!/usr/bin/env python3
"""Independent bounded-CRT / unisolvence certificate verifier.

Only standard library plus this audit's independently authored integer
Bareiss determinant. No tensor evaluations, source fitting helpers, or
repository modules are imported. CRT uses the direct product formula.
"""
from fractions import Fraction as Q
import argparse
import hashlib
import json
from math import isqrt,prod,lcm
from pathlib import Path

from bareiss_minors import bareiss

ROOT=Path(__file__).resolve().parent
SOURCE=ROOT.parent/"source-review"
CERTIFICATE=SOURCE/"exact-source-evaluation-certificate.json"
REPOSITORY=ROOT.parent/"repair-checkout"
FROZEN_BASIS=ROOT.parent/"frozen-checkout/results/rank81_basis.json"
WRITE_RESULT=True


def recorded_path(filename):
    path=Path(filename)
    if path.parts[0]=="source-review":return SOURCE/Path(*path.parts[1:])
    if path.parts[0]=="repair-checkout":return REPOSITORY/Path(*path.parts[1:])
    if path.parts[0]=="math-review":return ROOT/Path(*path.parts[1:])
    raise ValueError(f"unrecognized recorded source root: {filename}")


def rational_matrix(matrix):return [[Q(x) for x in row] for row in matrix]


def multiply(a,b):
    assert len(a[0])==len(b)
    return [[sum(x*y for x,y in zip(row,column)) for column in zip(*b)] for row in a]


def row_basis(matrix):
    pivots=[]
    selected=[]
    for index,original in enumerate(matrix):
        row=list(map(Q,original))
        for col,basis in pivots:
            scale=row[col]
            if scale:row=[a-scale*b for a,b in zip(row,basis)]
        col=next((j for j,v in enumerate(row) if v),None)
        if col is None:continue
        scale=row[col]
        row=[x/scale for x in row]
        pivots.append((col,row))
        pivots.sort(key=lambda x:x[0])
        selected.append(index)
    return selected


def rank(matrix):return len(row_basis(matrix))


def centered_crt(residues,primes,bound):
    modulus=prod(primes)
    assert modulus>2*bound
    value=sum(a*(modulus//p)*pow(modulus//p,-1,p) for a,p in zip(residues,primes))%modulus
    if 2*value>modulus:value-=modulus
    assert abs(value)<=bound
    assert all(value%p==a for p,a in zip(primes,residues))
    return value


def parse_graph(label):
    head,body=label.split("[",1)
    n=int(head[1:]);edges=[]
    for token in body[:-1].split(","):
        pair,m=token.split("^")
        ends=pair.split("-") if "-" in pair else list(pair)
        assert len(ends)==2
        i,j=map(int,ends)
        assert 0<=i<j<n
        edges.append([i,j,int(m)])
    return {"n":n,"edges":sorted(edges)}


def main():
    if not __debug__:
        raise RuntimeError("verification requires Python without -O or PYTHONOPTIMIZE")
    cert=json.loads(CERTIFICATE.read_text())
    bounds=json.loads((ROOT/"source_bound_review.json").read_text())
    primes=cert["primes"]
    assert primes==bounds["primes"] and all(all(p%d for d in range(2,isqrt(p)+1)) for p in primes)
    modulus=prod(primes)
    assert modulus==cert["modulus"]==bounds["prime_product"]
    seeds=cert["seeds"]
    assert len(seeds)==len(set(seeds))==14
    assert len(cert["coordinates"])==14
    assert len({tuple(a) for a in cert["coordinates"]})==14
    assert all(len(a)==126 and all(type(x)is int and x in [0,1] for x in a) for a in cert["coordinates"])
    expectedD10=[r["clearing_denominator"] for r in bounds["degree10"]]
    expectedD8=[r["clearing_denominator"] for r in bounds["degree8_primary"]]+[810000]*5+[336]
    expectedB10=[r["cleared_absolute_bound"] for r in bounds["degree10"]]
    expectedB8=[r["cleared_absolute_bound"] for r in bounds["degree8_primary"]]+[bounds["degree8_hatted"]["H1_through_H5_bound"]]*5+[bounds["degree8_hatted"]["H6_bound"]]
    # Independently derive the numeric proof limits; the auxiliary bounds JSON
    # is checked evidence, not an authority that can silently loosen a bound.
    assert expectedD10==[1,336,100,2400,400,3360,1000,2000,60000,200000,2700000,2700000]
    assert expectedD8==[1,336,100,240000,400,3360]+[810000]*5+[336]
    factors10=[(5,0,0),(4,0,1),(3,2,0),(3,2,0),(3,2,0),(3,1,1),(2,3,0),(2,3,0),(1,4,0),(0,5,0),(0,5,0),(0,5,0)]
    factors8=[(4,0,0),(3,0,1),(2,2,0),(0,4,0),(2,2,0),(2,1,1)]+[(0,4,0)]*5+[(3,0,1)]
    derived=lambda factors,denoms:[d*3024**m*42**q*1224**r*10**(m+3*(q+r)) for (m,q,r),d in zip(factors,denoms)]
    assert expectedB10==derived(factors10,expectedD10)
    assert expectedB8==derived(factors8,expectedD8)
    for degree,denoms,limits in [(8,expectedD8,expectedB8),(10,expectedD10,expectedB10)]:
        section=cert["bounds"][f"degree{degree}"]
        assert section["denominators"]==denoms
        assert section["integer_numerator_absolute_bounds"]==limits
        assert section["denominator_lcm"]==lcm(*denoms)
        assert all(modulus>2*x for x in limits)
    points={};source_hashes={}
    assert len(cert["point_evidence"])==98
    for evidence in cert["point_evidence"]:
        path=SOURCE/evidence["path"]
        assert path.resolve().is_relative_to(SOURCE.resolve())
        assert hashlib.sha256(path.read_bytes()).hexdigest()==evidence["sha256"]
        point=json.loads(path.read_text())
        key=point["prime"],point["seed"]
        assert key not in points and key[0] in primes and key[1] in seeds
        assert point["coordinates"]==cert["coordinates"][seeds.index(key[1])]
        for filename,digest in point["source_hashes"].items():
            assert filename not in source_hashes or source_hashes[filename]==digest
            source_hashes[filename]=digest
            assert hashlib.sha256(recorded_path(filename).read_bytes()).hexdigest()==digest
        for keyname,size in [("atlas8",7),("atlas10",14),("primary8",6),("hatted8",6),("degree10",12)]:
            assert len(point[keyname])==size and all(type(x)is int and 0<=x<key[0] for x in point[keyname])
        assert point["selected8"]==point["primary8"][:5]+point["hatted8"][:1]+[point["atlas8"][6]]
        points[key]=point
    assert set(points)=={(p,s) for p in primes for s in seeds}
    definitions={}
    for filename in ["10d_order8.json","10d_order10.json"]:
        for item in json.loads((REPOSITORY/"results"/filename).read_text())["generators"]:
            if item["order"]<=10:definitions[item["id"]]=item
    definitions_hash=hashlib.sha256(json.dumps(definitions,sort_keys=True,separators=(",",":")).encode()).hexdigest()
    assert cert["graph_definitions"]==definitions
    for filename,digest in cert["audit_source_sha256"].items():
        assert hashlib.sha256((SOURCE/filename).read_bytes()).hexdigest()==digest
    assert all(point["definitions_sha256"]==definitions_hash for point in points.values())
    frozen={i["id"]:i for i in json.loads(FROZEN_BASIS.read_text())["invariants"]}
    for name,item in definitions.items():assert parse_graph(item["graph"])==frozen[name]["graph"]
    reconstructed={}
    exact={}
    configs=[("atlas8",[1]*7,[10**20]*7),("all8",expectedD8,expectedB8),
             ("atlas10",[1]*14,[10**25]*14),("degree10",expectedD10,expectedB10)]
    entries=0
    for key,denominators,limits in configs:
        matrix=[]
        for seed in seeds:
            row=[]
            for column,(denominator,limit) in enumerate(zip(denominators,limits)):
                residues=[]
                for p in primes:
                    point=points[p,seed]
                    values=point["primary8"]+point["hatted8"] if key=="all8" else point[key]
                    residues.append(values[column]*denominator%p)
                row.append(centered_crt(residues,primes,limit))
                entries+=1
            matrix.append(row)
        assert matrix==cert["exact_integer_numerator_evaluations"][key]
        rational=[[Q(value,denominator) for value,denominator in zip(row,denominators)] for row in matrix]
        assert rational==rational_matrix(cert["exact_rational_evaluations"][key])
        reconstructed[key]=matrix;exact[key]=rational
    determinant10,_=bareiss(reconstructed["atlas10"])
    assert determinant10!=0
    rows8=row_basis(exact["atlas8"])
    assert len(rows8)==7
    determinant8,_=bareiss([reconstructed["atlas8"][i] for i in rows8])
    assert determinant8!=0
    d8=cert["maps"]["degree8"];d10=cert["maps"]["degree10"]
    map8all=rational_matrix(d8["all_displayed_literature_to_graph"])
    map8=rational_matrix(d8["literature_to_graph"])
    inverse8=rational_matrix(d8["graph_to_literature"])
    map10=rational_matrix(d10["matrix_12x14"])
    assert len(map8all)==12 and all(len(row)==7 for row in map8all)
    assert len(map8)==len(inverse8)==7 and all(len(row)==7 for row in map8+inverse8)
    assert len(map10)==12 and all(len(row)==14 for row in map10)
    assert multiply(exact["atlas8"],list(zip(*map8all)))==exact["all8"]
    assert multiply(exact["atlas10"],list(zip(*map10)))==exact["degree10"]
    unit=[Q(0)]*6+[Q(1)]
    assert map8==map8all[:5]+map8all[6:7]+[unit]
    eye=[[Q(i==j) for j in range(7)] for i in range(7)]
    assert multiply(map8,inverse8)==multiply(inverse8,map8)==eye
    assert list(map(Q,d8["product_correction"]))==[row[6] for row in inverse8[:6]]
    assert d8["exact_6x6_without_products"]==(not any(row[6] for row in inverse8[:6]))
    product_basis=[[Q(i==j) for i in range(14)] for j in [12,13]]
    source_rank=rank(map10);quotient_rank=rank([row[:12] for row in map10]);union_rank=rank(map10+product_basis)
    intersection=source_rank+2-union_rank
    assert quotient_rank==union_rank-2
    assert (source_rank,quotient_rank,union_rank,intersection)==(d10["published_span_rank"],d10["primitive_quotient_rank"],d10["union_rank"],d10["intersection_rank"])
    witness_vectors=[]
    for witness in d10["product_intersection_witnesses"]:
        combination=list(map(Q,witness["source_combination"]))
        assert len(combination)==12
        vector=multiply([combination],map10)[0]
        assert not any(vector[:12]) and any(vector[12:])
        assert vector[12:]==list(map(Q,witness["product_coefficients"]))
        witness_vectors.append(vector[12:])
    assert rank(witness_vectors)==len(witness_vectors)==intersection
    expected_ranks={"atlas8":7,"atlas10":14,"source8_selected":rank(map8),"source8_primary":rank(map8all[:6]),
                    "source8_hatted":rank(map8all[6:]),"source8_primary_with_product":rank(map8all[:6]+[map8[-1]]),
                    "source8_hatted_with_product":rank(map8all[6:]+[map8[-1]]),"source10":source_rank,
                    "source10_primitive_quotient":quotient_rank,"product_intersection":intersection}
    assert cert["ranks"]==expected_ranks
    for filename,map_data in [("order8_change_of_basis_exact.json",d8),("order10_change_of_basis_exact.json",d10)]:
        assert json.loads((SOURCE/filename).read_text())==map_data
    result={"status":"PASS: independent exact CRT and finite-dimensional identity verification",
            "certificate_sha256":hashlib.sha256(CERTIFICATE.read_bytes()).hexdigest(),
            "point_files_verified":98,"reconstructed_integer_entries":entries,"modulus":modulus,
            "bound_maximum":max(expectedB10+expectedB8),"atlas10_integer_determinant":str(determinant10),
            "atlas8_independent_sample_rows":rows8,"atlas8_integer_minor_determinant":str(determinant8),
            "ranks":expected_ranks,"source10_union_rank":union_rank,"intersection_witness_count":len(witness_vectors),
            "definition_hash":definitions_hash,"graph_definitions_match_frozen_basis":True,
            "degree8_product_correction":[str(row[6]) for row in inverse8[:6]],
            "proof_premises":["Dimension of the full rational invariant space is at most7 in degree8 and14 in degree10.",
                              "The specified source contractions belong to those invariant spaces.",
                              "The recorded modular evaluations correctly implement the stated fixed programs."],
            "independence":"Direct-product CRT; independent Bareiss and Fraction row-echelon verification; no source fit helper or tensor recomputation.",
            "qualification":"Degree8 evaluation into Q^14 is injective, an isomorphism onto its7-dimensional image; degree10 evaluation is an isomorphism onto Q^14. Source-reading scope remains literal displayed formulas."}
    if WRITE_RESULT:
        (ROOT/"source_crt_independent_verification.json").write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps(result,indent=2))


if __name__=="__main__":
    parser=argparse.ArgumentParser()
    parser.add_argument("--math-dir",type=Path,default=ROOT)
    parser.add_argument("--source-dir",type=Path,default=SOURCE)
    parser.add_argument("--repository",type=Path,default=REPOSITORY)
    parser.add_argument("--frozen-basis",type=Path,default=FROZEN_BASIS)
    parser.add_argument("--no-write",action="store_true")
    parser.add_argument("--certificate",type=Path)
    args=parser.parse_args()
    ROOT=args.math_dir.resolve();SOURCE=args.source_dir.resolve();REPOSITORY=args.repository.resolve()
    FROZEN_BASIS=args.frozen_basis.resolve();CERTIFICATE=SOURCE/"exact-source-evaluation-certificate.json"
    if args.certificate is not None:CERTIFICATE=args.certificate.resolve()
    WRITE_RESULT=not args.no_write
    main()
