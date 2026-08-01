#!/usr/bin/env python3
"""Independent verification of G-10: the free stress tensor of a self-dual
five-form in D=10 is traceless, identically and off shell.

This script deliberately imports NOTHING from ``src/sdinv`` or from the
stress-flow production code.  It rebuilds the Hodge star, the self-duality
projector, the moment tensor M and the free stress tensor T = M/(2*4!) from
the definitions, in exact integer arithmetic, and contracts the trace.

Phase 3.4 of the JHEP execution plan.  Writes
``results/stress_flow/g10_trace_verification.json``.

The point of the exercise is that the result must not depend on:

  * the sign convention for epsilon (both are tested),
  * the choice of self-dual vs anti-self-dual channel (both are tested),
  * the real form -- Lorentzian (1,9) and split (5,5) are both tested,
  * the particular five-form sample (many random exact samples are tested).

Run:  python3 scripts/verify_g10_trace_independent.py
"""

from __future__ import annotations

import itertools
import json
import os
import random
import sys
from fractions import Fraction

D = 10
P_FORM = 5

# ---------------------------------------------------------------- signatures

SIGNATURES = {
    # name: tuple of eta^{mu mu}, mu = 0..9
    "lorentzian_1_9": (-1,) + (1,) * 9,
    "split_5_5": (-1,) * 5 + (1,) * 5,
    "euclidean_10_0": (1,) * 10,
}

FIVE_SETS = [frozenset(c) for c in itertools.combinations(range(D), P_FORM)]
FIVE_SORTED = [tuple(sorted(s)) for s in FIVE_SETS]
FOUR_SORTED = [tuple(c) for c in itertools.combinations(range(D), 4)]


def perm_sign(seq) -> int:
    """Sign of the permutation taking (0..9) to ``seq``. O(n^2), n = 10."""
    seq = list(seq)
    sign = 1
    for i in range(len(seq)):
        for j in range(i + 1, len(seq)):
            if seq[i] > seq[j]:
                sign = -sign
    return sign


def raise_factor(indices, eta) -> int:
    """Product of eta^{mu mu} over ``indices`` -- the cost of raising them."""
    out = 1
    for m in indices:
        out *= eta[m]
    return out


def hodge_star(lam, eta, eps_lower_sign):
    """(*L)_I = eps_{I,I^c} * (raising factor on I^c) * L_{I^c}.

    ``lam`` maps a sorted 5-tuple to a value.  ``eps_lower_sign`` is
    eps_{0 1 ... 9}, i.e. the fully-lowered epsilon, either +1 or -1.
    """
    out = {}
    full = set(range(D))
    for I in FIVE_SORTED:
        comp = tuple(sorted(full - set(I)))
        sign = eps_lower_sign * perm_sign(list(I) + list(comp))
        out[I] = sign * raise_factor(comp, eta) * lam[comp]
    return out


def star_squared_scalar(eta, eps_lower_sign):
    """Return c such that **L = c L on 5-forms, or None if not a multiple."""
    probe = {I: 0 for I in FIVE_SORTED}
    ratios = set()
    for base in FIVE_SORTED[:12]:
        for I in FIVE_SORTED:
            probe[I] = 0
        probe[base] = 1
        twice = hodge_star(hodge_star(probe, eta, eps_lower_sign), eta, eps_lower_sign)
        ratios.add(twice[base])
        for I in FIVE_SORTED:
            if I != base and twice[I] != 0:
                return None
    return ratios.pop() if len(ratios) == 1 else None


def moment_tensor(lam, eta):
    """M_{mu nu} = L_{mu r1..r4} L_nu^{r1..r4}, exact integers.

    The sum over ordered (r1..r4) equals 4! times the sum over sorted
    4-subsets, so M = 24 * sum_{R sorted} (raise R) * L_{mu R} L_{nu R}.
    """
    M = [[0] * D for _ in range(D)]
    for R in FOUR_SORTED:
        rs = set(R)
        rf = raise_factor(R, eta)
        avail = [m for m in range(D) if m not in rs]
        # L_{mu R} with mu prepended, then sorted
        vals = {}
        for m in avail:
            seq = [m] + list(R)
            key = tuple(sorted(seq))
            vals[m] = perm_sign_relative(seq, key) * lam[key]
        for mu in avail:
            vmu = vals[mu]
            if vmu == 0:
                continue
            for nu in avail:
                M[mu][nu] += rf * vmu * vals[nu]
    return [[24 * x for x in row] for row in M]


def perm_sign_relative(seq, target) -> int:
    """Sign of the permutation carrying ``seq`` to ``target`` (both same set)."""
    seq = list(seq)
    target = list(target)
    sign = 1
    for i in range(len(target)):
        j = seq.index(target[i], i)
        if j != i:
            seq[i], seq[j] = seq[j], seq[i]
            sign = -sign
    return sign


def trace(M, eta):
    """eta^{mu nu} M_{mu nu} = sum_mu eta^{mu mu} M_{mu mu}."""
    return sum(eta[m] * M[m][m] for m in range(D))


def random_form(rng, bound=9):
    return {I: rng.randint(-bound, bound) for I in FIVE_SORTED}


def project(lam, eta, eps_lower_sign, channel):
    """L +/- *L, an unnormalised (anti-)self-dual projection (valid when **=+1)."""
    star = hodge_star(lam, eta, eps_lower_sign)
    s = 1 if channel == "self_dual" else -1
    return {I: lam[I] + s * star[I] for I in FIVE_SORTED}


def check_duality(lam, eta, eps_lower_sign, channel):
    star = hodge_star(lam, eta, eps_lower_sign)
    s = 1 if channel == "self_dual" else -1
    return all(star[I] == s * lam[I] for I in FIVE_SORTED)


def main() -> int:
    rng = random.Random(20260801)
    report = {
        "phase": "3.4",
        "obligation": "G-10",
        "statement": (
            "The free stress tensor T = M/(2*4!) of a self-dual five-form in "
            "D=10 is identically traceless, off shell, from algebraic "
            "self-duality alone."
        ),
        "imports_production_code": False,
        "arithmetic": "exact integers",
        "star_squared": {},
        "samples": [],
        "summary": {},
    }

    n_samples = 24
    failures = []
    lorentzian_split_ok = []

    for sig_name, eta in SIGNATURES.items():
        for eps_lower_sign in (+1, -1):
            c = star_squared_scalar(eta, eps_lower_sign)
            key = f"{sig_name}|eps_lower={eps_lower_sign:+d}"
            report["star_squared"][key] = c
            if c != 1:
                # No real (anti-)self-dual forms in this real form; skip.
                continue
            for channel in ("self_dual", "anti_self_dual"):
                for k in range(n_samples):
                    lam = project(random_form(rng), eta, eps_lower_sign, channel)
                    if not check_duality(lam, eta, eps_lower_sign, channel):
                        failures.append({"where": key, "channel": channel,
                                         "sample": k, "why": "projection failed"})
                        continue
                    if all(v == 0 for v in lam.values()):
                        continue
                    M = moment_tensor(lam, eta)
                    trM = trace(M, eta)
                    # T = M / (2*4!); the trace scales, so vanishing is equivalent.
                    sym_ok = all(M[a][b] == M[b][a] for a in range(D) for b in range(D))
                    rec = {
                        "signature": sig_name,
                        "eps_lower_sign": eps_lower_sign,
                        "channel": channel,
                        "sample": k,
                        "trace_M": trM,
                        "trace_T": str(Fraction(trM, 48)),
                        "M_symmetric": sym_ok,
                        "M_nonzero": any(x for row in M for x in row),
                    }
                    if trM != 0 or not sym_ok:
                        failures.append(rec)
                    if k < 2:
                        report["samples"].append(rec)
                    if sig_name in ("lorentzian_1_9", "split_5_5"):
                        lorentzian_split_ok.append(trM == 0)

    report["summary"] = {
        "samples_tested": len(lorentzian_split_ok),
        "all_traces_vanish": all(lorentzian_split_ok) and not failures,
        "failures": failures[:10],
        "n_failures": len(failures),
        "real_forms_admitting_real_self_duality": [
            k for k, v in report["star_squared"].items() if v == 1
        ],
        "real_forms_without": [
            k for k, v in report["star_squared"].items() if v != 1
        ],
        "trace_starting_degree_of_Tr_tau": 4,
        "reason": (
            "Both Lambda-bilinear terms in Tr(T[V]) vanish by (anti-)self-duality "
            "(Lambda.Lambda = 0 and V_Lambda.V_Lambda = 0), leaving "
            "Tr(T) = -(10/4!)(V - (1/2) Lambda.V_Lambda). For V homogeneous of "
            "degree d, Lambda.V_Lambda = d V by Euler, so that bracket is "
            "(1 - d/2) V, which vanishes identically at d = 2 and is nonzero "
            "for d = 4. Hence Tr(tau) has no quadratic part and begins at "
            "degree four."
        ),
    }

    out = os.path.join("results", "stress_flow", "g10_trace_verification.json")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, "w") as fh:
        json.dump(report, fh, indent=2, sort_keys=True)

    s = report["summary"]
    print(f"star-squared by real form: {report['star_squared']}")
    print(f"samples tested (Lorentzian + split): {s['samples_tested']}")
    print(f"all free-stress traces vanish: {s['all_traces_vanish']}")
    print(f"failures: {s['n_failures']}")
    print(f"wrote {out}")
    return 0 if s["all_traces_vanish"] else 1


if __name__ == "__main__":
    sys.exit(main())
