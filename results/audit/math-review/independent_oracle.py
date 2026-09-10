#!/usr/bin/env python3
"""Fresh graph-value/directional-derivative implementation; no sdinv imports.

Use opt_einsum for path selection ONLY. Perform the contractions explicitly by
reshaping pairs into matrices. Propagate a dual number F + epsilon*dF through
the forward computation (epsilon**2 = 0); there is no reverse-mode gradient.
Every matrix dot product has a checked integer bound below 2**53, so float64
BLAS operations on nonnegative reduced integer operands are exact. Reduction
after every product and every derivative addition keeps that bound invariant.
"""
import argparse
from collections import Counter
import hashlib
import itertools
import json
from pathlib import Path
import time

import numpy as np
import opt_einsum as oe

from independent_conventions import compact_form, parity, slot_records, TUPLES

ROOT = Path(__file__).resolve().parent
CHECKOUT = ROOT.parent / "frozen-checkout"
DIM = 10


def dense_form(coordinates, prime):
    tensor = np.zeros((10,) * 5, dtype=np.float64)
    for indices, value in zip(TUPLES, compact_form(coordinates, prime)):
        for ordered in itertools.permutations(indices):
            tensor[ordered] = parity(ordered) * value % prime
    return tensor


def terms(item):
    slots, raised = slot_records(item)
    labels = sorted({edge for group in slots for edge in group})
    mapping = {edge: k for k, edge in enumerate(labels)}
    return [[mapping[edge] for edge in group] for group in slots], raised


def plan(item):
    labels, raised = terms(item)
    equation = ",".join("".join(oe.get_symbol(k) for k in group) for group in labels) + "->"
    path, info = oe.contract_path(equation, *[(10,)*5 for _ in labels], shapes=True, optimize="dp")
    working = [list(group) for group in labels]
    largest_output = 10**5
    largest_dot_terms = 1
    work = 0
    for pair in path:
        assert len(pair) == 2
        i, j = pair
        left, right = working[i], working[j]
        shared = set(left) & set(right)
        output = [k for k in left if k not in shared] + [k for k in right if k not in shared]
        work += 10**len(set(left) | set(right))
        largest_output = max(largest_output, 10**len(output))
        largest_dot_terms = max(largest_dot_terms, 10**len(shared))
        for k in sorted(pair, reverse=True):
            working.pop(k)
        working.append(output)
    assert working == [[]]
    return {"id": item["id"], "path": [list(p) for p in path],
            "largest_output_elements": largest_output,
            "largest_dot_terms": largest_dot_terms,
            "forward_dual_multiply_terms": 3*work,
            "float64_exact_bound_at_largest_prime": largest_dot_terms * (32749-1)**2,
            "three_output_arrays_bytes": 3 * largest_output * 8}


def modular_dot(left, right, prime, counters):
    assert left.shape[1] == right.shape[0]
    bound = left.shape[1] * (prime - 1)**2
    assert bound < 2**53, ("STOP: exact float64 bound unavailable", bound)
    counters["dot_products"] += 1
    counters["largest_dot_bound"] = max(counters["largest_dot_bound"], bound)
    product = left @ right
    assert np.all(np.isfinite(product))
    assert np.all(product >= 0) and np.all(product <= bound)
    # This does not claim approximate arithmetic: every exact partial sum is
    # an integer no larger than the guard above, and is representable exactly.
    return np.remainder(product, prime)


def pair_contract(left, right, prime, counters):
    labels_a, value_a, derivative_a = left
    labels_b, value_b, derivative_b = right
    common = [label for label in labels_a if label in labels_b]
    free_a = [label for label in labels_a if label not in common]
    free_b = [label for label in labels_b if label not in common]
    order_a = [labels_a.index(label) for label in free_a + common]
    order_b = [labels_b.index(label) for label in common + free_b]
    shape_a = (DIM**len(free_a), DIM**len(common))
    shape_b = (DIM**len(common), DIM**len(free_b))
    a = value_a.transpose(order_a).reshape(shape_a)
    da = derivative_a.transpose(order_a).reshape(shape_a)
    b = value_b.transpose(order_b).reshape(shape_b)
    db = derivative_b.transpose(order_b).reshape(shape_b)
    output = free_a + free_b
    value = modular_dot(a, b, prime, counters)
    derivative = np.remainder(modular_dot(da, b, prime, counters)
                              + modular_dot(a, db, prime, counters), prime)
    return output, value.reshape((DIM,)*len(output)), derivative.reshape((DIM,)*len(output))


def evaluate(item, coordinate_vector, direction, prime, selected_plan, counters):
    form = dense_form(coordinate_vector, prime)
    tangent = dense_form(direction, prime)
    labels, raised = terms(item)
    signs = np.array([-1] + [1]*9, dtype=np.float64)
    working = []
    for group, variance in zip(labels, raised):
        a, da = form.copy(), tangent.copy()
        # Deliberately place metric signs at the incoming (larger endpoint)
        # slot, as printed formulas do; production places them at the tail.
        for axis, is_raised in enumerate(variance):
            if is_raised:
                shape = [1] * 5
                shape[axis] = 10
                a = np.remainder(a * signs.reshape(shape), prime)
                da = np.remainder(da * signs.reshape(shape), prime)
        working.append((group, a, da))
    for i, j in selected_plan["path"]:
        new = pair_contract(working[i], working[j], prime, counters)
        for k in sorted([i, j], reverse=True):
            working.pop(k)
        working.append(new)
    assert len(working) == 1 and working[0][0] == []
    return int(working[0][1]), int(working[0][2])


def independent_direction(prime, seed):
    # Stateless hash-derived residues, independent of the repository RNG.
    return [int.from_bytes(hashlib.sha256(f"independent-direction|{prime}|{seed}|{k}".encode()).digest(), "big") % prime
            for k in range(126)]


def arithmetic_selftest():
    counters = Counter()
    prime = 32749
    a = np.array([[prime-1, prime-2, 11111], [12345, 23456, 0]], dtype=np.float64)
    b = np.array([[prime-1, 1], [prime-2, 2345], [22222, 3333]], dtype=np.float64)
    observed = modular_dot(a, b, prime, counters).astype(np.int64).tolist()
    expected = [[sum(int(a[i, k])*int(b[k, j]) for k in range(3)) % prime for j in range(2)] for i in range(2)]
    assert observed == expected
    # Realistic maximum-size scalar dot is also checked against Python bigint.
    a = np.arange(100000, dtype=np.int64).reshape(1, -1) % prime
    b = np.arange(99999, -1, -1, dtype=np.int64).reshape(-1, 1) % prime
    expected = sum(int(x)*int(y) for x, y in zip(a.ravel(), b.ravel())) % prime
    assert int(modular_dot(a.astype(np.float64), b.astype(np.float64), prime, counters)[0, 0]) == expected


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--profile", action="store_true")
    parser.add_argument("--cell", type=int, default=0)
    parser.add_argument("--limit", type=int, default=81)
    args = parser.parse_args()
    items = json.loads((CHECKOUT / "results/rank81_basis.json").read_text())["invariants"]
    plans = [plan(item) for item in items]
    if args.profile:
        summary = {"plans": plans,
                   "total_forward_dual_multiply_terms_per_cell": sum(p["forward_dual_multiply_terms"] for p in plans),
                   "max_three_output_arrays_bytes": max(p["three_output_arrays_bytes"] for p in plans),
                   "max_float64_bound": max(p["float64_exact_bound_at_largest_prime"] for p in plans)}
        (ROOT / "oracle_profile.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps({k: v for k, v in summary.items() if k != "plans"}, indent=2))
        return
    arithmetic_selftest()
    witness = json.loads((CHECKOUT / "results/rank81_certificate.json").read_text())["witnesses"][args.cell]
    prime, seed = witness["prime"], witness["seed"]
    direction = independent_direction(prime, seed)
    counters = Counter()
    result = {"prime": prime, "seed": seed, "cell_index": args.cell,
              "direction": direction, "implementation": "independent forward dual-number graph contraction",
              "repository_imports": False, "records": [], "status": "RUNNING"}
    destination = ROOT / f"oracle_cell{args.cell}_limit{args.limit}.json"
    for index, (item, selected_plan) in enumerate(zip(items[:args.limit], plans)):
        start = time.monotonic()
        observed_value, observed_derivative = evaluate(item, witness["coordinates"], direction, prime, selected_plan, counters)
        expected_value = witness["values"][index]
        expected_derivative = sum(int(g)*h for g, h in zip(witness["jacobian"][index], direction)) % prime
        passed = observed_value == expected_value and observed_derivative == expected_derivative
        record = {"index": index, "id": item["id"], "observed_value": observed_value,
                  "stored_value": expected_value, "observed_directional_derivative": observed_derivative,
                  "stored_J_dot_direction": expected_derivative,
                  "seconds": time.monotonic() - start, "passed": passed}
        result["records"].append(record)
        result["arithmetic_counters"] = dict(counters)
        destination.write_text(json.dumps(result, indent=2) + "\n")
        print(json.dumps(record), flush=True)
        assert passed, f"STOP: independent oracle mismatch for {item['id']} at {prime}/{seed}"
    result["status"] = "PASS"
    result["checked_graphs"] = len(result["records"])
    destination.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"status": "PASS", "prime": prime, "seed": seed,
                      "checked_graphs": len(result["records"]), "arithmetic_counters": dict(counters)}), flush=True)


if __name__ == "__main__":
    main()
