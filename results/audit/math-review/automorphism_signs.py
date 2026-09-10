#!/usr/bin/env python3
"""Exhaustive weighted-graph automorphisms and induced alternating-slot signs.

Independent constraint backtracking, no graph-library or production imports.
Every partial assignment preserves all already assigned adjacency entries;
all valid vertex permutations are visited exactly once.
"""
from collections import Counter
import json
from pathlib import Path
import time

from efficient_oracle import items81,relabel

ROOT=Path(__file__).resolve().parent


def automorphisms(matrix):
    n=len(matrix)
    signatures=[tuple(sorted(row)) for row in matrix]
    assignment={}
    used=set()
    def visit():
        if len(assignment)==n:
            yield [assignment[i] for i in range(n)]
            return
        best_vertex=None
        best_domain=None
        for vertex in range(n):
            if vertex in assignment:continue
            domain=[target for target in range(n) if target not in used and signatures[vertex]==signatures[target]
                    and all(matrix[vertex][old]==matrix[target][new] for old,new in assignment.items())]
            if not domain:return
            if best_domain is None or len(domain)<len(best_domain):
                best_vertex,best_domain=vertex,domain
        for target in best_domain:
            assignment[best_vertex]=target
            used.add(target)
            yield from visit()
            used.remove(target)
            del assignment[best_vertex]
    yield from visit()


def main():
    records=[]
    for item in items81():
        start=time.monotonic()
        signs=Counter()
        permutations=[]
        for permutation in automorphisms(item["adjacency_matrix"]):
            same,sign=relabel(item,permutation)
            assert same["graph"]==item["graph"]
            signs[sign]+=1
            permutations.append({"permutation":permutation,"induced_sign":sign})
        assert signs[-1]==0,(item["id"],"negative automorphism sign",signs)
        record={"id":item["id"],"automorphism_count":sum(signs.values()),"positive_count":signs[1],
                "negative_count":signs[-1],"automorphisms":permutations,"seconds":time.monotonic()-start}
        records.append(record)
        (ROOT/"automorphism_sign_results.json").write_text(json.dumps({"records":records,"complete":len(records)==81},indent=2)+"\n")
        print(json.dumps({k:v for k,v in record.items() if k!="automorphisms"}),flush=True)


if __name__=="__main__":main()
