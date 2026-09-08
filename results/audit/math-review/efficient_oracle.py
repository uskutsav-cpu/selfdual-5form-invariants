"""Independent cached value / forward-dual engine. No production imports.

The only cross-graph cache is bounded and lives inside a single PointEngine;
each point gets an entirely new engine. Cache keys encode the full sequence
of binary contraction permutations and input metric placements, never values
read from the frozen numerical certificates.
"""
from collections import Counter, OrderedDict
import copy
import json
from pathlib import Path
import re

import numpy as np

from independent_conventions import ROOT, CHECKOUT, parity, slot_records
from independent_oracle import dense_form, terms, plan, modular_dot


def items81():
    return json.loads((CHECKOUT / "results/rank81_basis.json").read_text())["invariants"]


def parse_label(label, name):
    head, body = label.split("[", 1)
    n = int(head[1:])
    edges = []
    for token in body[:-1].split(","):
        endpoints, count = token.split("^")
        i, j = map(int, endpoints.split("-")) if "-" in endpoints else map(int, endpoints)
        edges.append([i, j, int(count)])
    assert edges == sorted(edges)
    valences = [0]*n
    for i, j, m in edges:
        assert 0 <= i < j < n and 1 <= m <= 4
        valences[i] += m
        valences[j] += m
    assert valences == [5]*n
    return {"id": name, "degree": n, "graph": {"n": n, "edges": edges}}


def items12():
    entries = json.loads((CHECKOUT / "results/10d_order12.json").read_text())["degree12_basis"]
    items = [parse_label(row["graph"], row["id"]) for row in entries if row["kind"] == "connected_primitive"]
    assert len(items) == 62
    assert [i["graph"] for i in items[:60]] == [i["graph"] for i in items81() if i["degree"] == 12]
    return items


class PointEngine:
    def __init__(self, coordinates, prime, direction=None, cache_limit=256*1024**2):
        self.prime = prime
        self.dual = direction is not None
        self.form = dense_form(coordinates, prime)
        self.tangent = dense_form(direction, prime) if self.dual else None
        self.inputs = {}
        self.ids = {}
        self.cache = OrderedDict()
        self.cache_bytes = 0
        self.limit = cache_limit
        self.stats = Counter()

    def identify(self, descriptor):
        if descriptor not in self.ids:
            self.ids[descriptor] = len(self.ids)
        return self.ids[descriptor]

    def initial(self, raised, permutation=None):
        permutation = tuple(range(5)) if permutation is None else tuple(permutation)
        key = ("input", tuple(raised), permutation)
        identity = self.identify(key)
        if identity not in self.inputs:
            arrays = [self.form.transpose(permutation)]
            if self.dual:
                arrays.append(self.tangent.transpose(permutation))
            signs = np.array([-1] + [1]*9, dtype=np.float64)
            for axis, flag in enumerate(raised):
                if flag:
                    shape = [1]*5
                    shape[axis] = 10
                    arrays = [np.remainder(array * signs.reshape(shape), self.prime) for array in arrays]
            self.inputs[identity] = tuple(arrays)
        return identity, self.inputs[identity]

    def contract_pair(self, left, right):
        la, ida, aa = left
        lb, idb, bb = right
        common = [label for label in la if label in lb]
        free_a = [label for label in la if label not in common]
        free_b = [label for label in lb if label not in common]
        order_a = tuple(la.index(label) for label in free_a + common)
        order_b = tuple(lb.index(label) for label in common + free_b)
        result_labels = free_a + free_b
        result_id = self.identify(("pair", ida, idb, order_a, order_b, len(common)))
        if result_id in self.cache:
            self.stats["cache_hits"] += 1
            self.cache.move_to_end(result_id)
            return result_labels, result_id, self.cache[result_id]
        shape_a = (10**len(free_a), 10**len(common))
        shape_b = (10**len(common), 10**len(free_b))
        a = aa[0].transpose(order_a).reshape(shape_a)
        b = bb[0].transpose(order_b).reshape(shape_b)
        value = modular_dot(a, b, self.prime, self.stats)
        arrays = [value]
        if self.dual:
            da = aa[1].transpose(order_a).reshape(shape_a)
            db = bb[1].transpose(order_b).reshape(shape_b)
            arrays.append(np.remainder(modular_dot(da, b, self.prime, self.stats)
                                       + modular_dot(a, db, self.prime, self.stats), self.prime))
        arrays = tuple(array.reshape((10,)*len(result_labels)) for array in arrays)
        size = sum(array.nbytes for array in arrays)
        if size <= self.limit:
            while self.cache and self.cache_bytes + size > self.limit:
                _, evicted = self.cache.popitem(last=False)
                self.cache_bytes -= sum(array.nbytes for array in evicted)
            self.cache[result_id] = arrays
            self.cache_bytes += size
            self.stats["max_cached_bytes"] = max(self.stats["max_cached_bytes"], self.cache_bytes)
        return result_labels, result_id, arrays

    def evaluate(self, item, selected_plan=None, slot_permutations=None):
        labels, raised = terms(item)
        working = []
        slot_permutations = slot_permutations or {}
        for v, (group, variance) in enumerate(zip(labels, raised)):
            identity, arrays = self.initial(variance, slot_permutations.get(v))
            working.append((group, identity, arrays))
        selected_plan = selected_plan or plan(item)
        for i, j in selected_plan["path"]:
            combined = self.contract_pair(working[i], working[j])
            for k in sorted([i, j], reverse=True):
                working.pop(k)
            working.append(combined)
        assert len(working) == 1 and working[0][0] == []
        return tuple(int(array) for array in working[0][2])


def relabel(item, permutation):
    n = item["degree"]
    assert sorted(permutation) == list(range(n))
    edges = [[min(permutation[i], permutation[j]), max(permutation[i], permutation[j]), m]
             for i, j, m in item["graph"]["edges"]]
    new = {"id": item["id"] + "_permuted", "degree": n, "graph": {"n": n, "edges": sorted(edges)}}
    oldslots, _ = slot_records(item)
    newslots, _ = slot_records(new)
    sign = 1
    for v, oldgroup in enumerate(oldslots):
        mapped = [(min(permutation[i], permutation[j]), max(permutation[i], permutation[j]), k)
                  for i, j, k in oldgroup]
        induced = [mapped.index(edge) for edge in newslots[permutation[v]]]
        sign *= parity(induced)
    return new, sign


def products12(low_values, prime):
    q, a, b, *octic = low_values
    assert len(octic) == 6
    return [q**3 % prime, a*a % prime, a*b % prime, b*b % prime] + [q*x % prime for x in octic]
