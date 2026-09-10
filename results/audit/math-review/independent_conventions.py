#!/usr/bin/env python3
"""Conventions and graph audit with no imports from the frozen package."""
from collections import Counter
import hashlib
import itertools
import json
from math import comb, factorial
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
CHECKOUT = ROOT.parent / "frozen-checkout"
TUPLES = list(itertools.combinations(range(10), 5))
POSITIONS = {indices: k for k, indices in enumerate(TUPLES)}
COORDINATES = [k for k, indices in enumerate(TUPLES) if 0 in indices]


def parity(sequence):
    return (-1) ** sum(a > b for k, a in enumerate(sequence) for b in sequence[k + 1:])


def metric_product(indices):
    return -1 if 0 in indices else 1


def star_image(indices):
    complement = tuple(i for i in range(10) if i not in indices)
    return complement, parity(complement + indices) * metric_product(indices)


def directions():
    columns = []
    for k in COORDINATES:
        column = [0] * len(TUPLES)
        column[k] = 1
        other, sign = star_image(TUPLES[k])
        column[POSITIONS[other]] = sign
        columns.append(column)
    return [list(row) for row in zip(*columns)]


def compact_form(coordinates, prime):
    assert len(coordinates) == 126
    result = [0] * 252
    for a, k in zip(coordinates, COORDINATES):
        result[k] = int(a) % prime
        other, sign = star_image(TUPLES[k])
        result[POSITIONS[other]] = sign * int(a) % prime
    return result


def slot_records(item):
    n = item["degree"]
    slots = [[] for _ in range(n)]
    raised = [[] for _ in range(n)]
    for i, j, multiplicity in item["graph"]["edges"]:
        for k in range(1, multiplicity + 1):
            edge = (i, j, k)
            slots[i].append(edge)
            slots[j].append(edge)
            raised[i].append(False)
            raised[j].append(True)
    return slots, raised


def explicit_formula(item):
    slots, raised = slot_records(item)
    factors = []
    for edges, variance in zip(slots, raised):
        upper = [r"\mu_{%s,%s,%s}" % edge for edge, flag in zip(edges, variance) if flag]
        lower = [r"\mu_{%s,%s,%s}" % edge for edge, flag in zip(edges, variance) if not flag]
        # Incoming slots precede outgoing slots in the specified lexicographic order.
        assert variance == sorted(variance, reverse=True)
        factors.append("F" + ("^{" + " ".join(upper) + "}" if upper else "")
                       + ("_{" + " ".join(lower) + "}" if lower else ""))
    return r"\,".join(factors)


def json_digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(",", ":")).encode()).hexdigest()


def main():
    basis = json.loads((CHECKOUT / "results/rank81_basis.json").read_text())
    certificate = json.loads((CHECKOUT / "results/rank81_certificate.json").read_text())
    d = directions()
    assert len(TUPLES) == comb(10, 5) == 252
    assert len(COORDINATES) == comb(9, 4) == 126
    assert COORDINATES == list(range(126)) == certificate["coordinate_component_indices"]
    assert set(v for row in d for v in row) == {-1, 0, 1}
    assert d[:126] == [[int(i == j) for j in range(126)] for i in range(126)]
    for indices in TUPLES:
        other, sign = star_image(indices)
        back, back_sign = star_image(other)
        assert back == indices and sign * back_sign == 1
        # Swapping two disjoint blocks of five indices has parity (-1)^25.
        assert parity(other + indices) == -parity(indices + other)
    assert json_digest(d) == certificate["integral_directions_sha256"]
    for column in zip(*d):
        transformed = [0] * 252
        for k, value in enumerate(column):
            other, sign = star_image(TUPLES[k])
            transformed[POSITIONS[other]] = sign * value
        assert list(column) == transformed
    assert Counter(parity(p) for p in itertools.permutations(range(5))) == {-1: 60, 1: 60}
    graph_rows = []
    for item in basis["invariants"]:
        n = item["degree"]
        edges = item["graph"]["edges"]
        assert item["graph"]["n"] == n
        assert edges == sorted(edges)
        adjacency = [[0] * n for _ in range(n)]
        for i, j, m in edges:
            assert 0 <= i < j < n and type(m) is int and 1 <= m <= 4
            assert adjacency[i][j] == 0
            adjacency[i][j] = adjacency[j][i] = m
        assert adjacency == item["adjacency_matrix"]
        assert all(sum(row) == 5 for row in adjacency)
        reached = {0}
        while True:
            expanded = reached | {j for i in reached for j, m in enumerate(adjacency[i]) if m}
            if expanded == reached:
                break
            reached = expanded
        assert len(reached) == n
        slots, raised = slot_records(item)
        counts = Counter((edge, flag) for sl, rs in zip(slots, raised) for edge, flag in zip(sl, rs))
        assert all(count == 1 for count in counts.values())
        assert len(counts) == 5 * n
        assert all(counts[(edge, False)] == counts[(edge, True)] == 1 for edge, _ in counts)
        assert explicit_formula(item) == item["einstein_formula"]
        assert json_digest(item["graph"]) == item["formula_sha256"]
        graph_rows.append({"id": item["id"], "vertices": n,
                           "metric_factors": 5*n//2, "valences": [sum(row) for row in adjacency],
                           "loopless": True, "connected": True,
                           "one_upper_one_lower_each_edge": True, "ordered_formula_equal": True})
    assert len(graph_rows) == 81
    assert Counter(row["vertices"] for row in graph_rows) == {4: 1, 6: 2, 8: 6, 10: 12, 12: 60}
    witness_rows = []
    for w in certificate["witnesses"]:
        prime = w["prime"]
        f = compact_form(w["coordinates"], prime)
        assert f == w["selfdual_components"]
        norm = factorial(5) * sum(metric_product(indices) * value**2 for indices, value in zip(TUPLES, f)) % prime
        assert norm == 0
        assert w["invariant_ids"] == [item["id"] for item in basis["invariants"]]
        for item, value, row in zip(basis["invariants"], w["values"], w["jacobian"]):
            assert sum(a*b for a, b in zip(row, w["coordinates"])) % prime == item["degree"] * value % prime
        witness_rows.append({"prime": prime, "seed": w["seed"], "selfdual_components_equal": True,
                             "quadratic_norm": norm, "euler_rows": 81})
    output = {"status": "PASS", "repository_imports": False,
              "metric": [-1] + [1]*9, "signature_negative_positive": [1, 9],
              "star_squared_exponent": 5*(10-5)+1, "star_squared": 1,
              "ambient_dimension": 252, "selfdual_dimension": 126,
              "integral_directions_sha256": json_digest(d),
              "five_slot_permutation_parities": {"even": 60, "odd": 60},
              "graphs": graph_rows, "witnesses": witness_rows}
    (ROOT / "conventions_results.json").write_text(json.dumps(output, indent=2) + "\n")
    (ROOT / "independent_integral_directions.json").write_text(json.dumps(d, separators=(",", ":")) + "\n")
    print(json.dumps({k: v for k, v in output.items() if k != "graphs"}, indent=2))
    print("PASS: all 81 ordered formulas, connected loopless 5-valent graphs and edge variances verified")


if __name__ == "__main__":
    main()
