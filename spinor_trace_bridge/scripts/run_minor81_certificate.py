"""Phase 4: freeze an explicit 81x81 minor certifying rank >= 81 over Q.

The logical point, which is worth stating because it makes the certificate much
cheaper than it first appears:

    to certify rank >= 81 we need the minor to be NONZERO, not its value.

The Jacobian is the reduction of a genuine integer matrix (the coordinate basis
is integral with entries in {-1,0,+1} and the sample point is an integer
combination of it).  For an integer matrix `M`,

    det(M) = 0  =>  det(M) = 0 (mod p)   for every p,

so a single prime at which the minor's determinant is nonzero proves the integer
determinant is nonzero, hence `rank_Q >= 81`.  No height bound, no Hadamard
estimate and no CRT reconstruction is required for the rank statement.  We
compute the determinant at several primes anyway, because agreement across
primes also guards against an indexing error in selecting the minor.

Two independent determinant routines are used and required to agree: a
fraction-free Bareiss elimination and a modular LU with explicit pivoting.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "spinor_trace_bridge" / "src"))

from sdbridge.candidates import (                      # noqa: E402
    RowCache, build_context, evaluate_all, load_schedule,
)
from sdbridge.modular import inv, rank as modrank      # noqa: E402
import sdbridge.spinor_invariants as si                # noqa: E402


def det_mod_lu(M: np.ndarray, p: int) -> int:
    """Determinant by modular Gaussian elimination with pivoting."""
    A = np.asarray(M, dtype=np.int64).copy() % p
    n = A.shape[0]
    det = 1
    for c in range(n):
        nz = np.nonzero(A[c:, c])[0]
        if nz.size == 0:
            return 0
        r = c + int(nz[0])
        if r != c:
            A[[c, r]] = A[[r, c]]
            det = (-det) % p
        piv = int(A[c, c]) % p
        det = det * piv % p
        ai = inv(piv, p)
        A[c] = A[c] * ai % p
        below = np.nonzero(A[c + 1:, c])[0]
        for k in below:
            rr = c + 1 + int(k)
            A[rr] = (A[rr] - A[rr, c] * A[c]) % p
    return det % p


def det_mod_bareiss(M: np.ndarray, p: int) -> int:
    """Determinant by fraction-free (Bareiss) elimination, carried out mod p.

    A genuinely different recurrence from the LU routine: it never divides by a
    pivot until the final step, so a mistake in one is very unlikely to be
    mirrored in the other.
    """
    A = np.asarray(M, dtype=np.int64).copy() % p
    n = A.shape[0]
    sign = 1
    prev = 1
    for k in range(n - 1):
        if A[k, k] % p == 0:
            nz = np.nonzero(A[k + 1:, k])[0]
            if nz.size == 0:
                return 0
            r = k + 1 + int(nz[0])
            A[[k, r]] = A[[r, k]]
            sign = -sign
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                A[i, j] = (A[i, j] * A[k, k] - A[i, k] * A[k, j]) % p
            A[i, k] = 0
        ip = inv(int(prev) % p, p)
        A[k + 1:, k + 1:] = A[k + 1:, k + 1:] * ip % p
        prev = int(A[k, k]) % p
    return (sign * int(A[n - 1, n - 1])) % p


def jacobian_at(p: int, seed: int, selection: Path, flop_limit: float,
                cache_dir: Path):
    si.MAX_CONTRACTION_FLOPS = flop_limit
    si._modular_contract.__defaults__ = (None, si.MAX_INTERMEDIATE_ELEMENTS,
                                         flop_limit)
    schedule = load_schedule(selection)
    ctx = build_context(p, seed=seed)
    cache = RowCache(cache_dir / f"rowcache_p{p}_s{seed}.json")
    J, schedule = evaluate_all(schedule, ctx, cache=cache, seed=seed)
    ids = [c.candidate_id for c in schedule if c.terminal_status == "evaluated"]
    return J, ids, schedule


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--archive", required=True)
    ap.add_argument("--seed", type=int, default=11)
    ap.add_argument("--select-prime", type=int, default=32749,
                    help="prime used to CHOOSE the pivot rows and columns")
    ap.add_argument("--verify-primes", default="32749,32719,32717,32713,32707")
    ap.add_argument("--flop-limit", type=float, default=1e11)
    ap.add_argument("--out", default=str(ROOT / "results" / "rank81" / "minor81_certificate.json"))
    args = ap.parse_args()

    selection = Path(args.archive).expanduser().resolve() / \
        "run_4_12_tensor_words_s96" / "selected_graphs.json"
    cache_dir = Path(args.out).parent
    verify = [int(x) for x in args.verify_primes.split(",") if x.strip()]

    # 1. choose the minor at one prime
    t0 = time.time()
    J, ids, schedule = jacobian_at(args.select_prime, args.seed, selection,
                                   args.flop_limit, cache_dir)
    from sdbridge.modular import rref
    R, cols = rref(J, args.select_prime)
    total = modrank(J, args.select_prime)
    rows, seen = [], np.zeros((0, J.shape[1]), dtype=np.int64)
    for i in range(J.shape[0]):
        trial = np.concatenate([seen, J[i:i + 1]], axis=0)
        if modrank(trial, args.select_prime) > seen.shape[0]:
            seen = trial
            rows.append(i)
        if len(rows) == total:
            break
    cols = list(cols[:total])
    print(f"selected {len(rows)} rows x {len(cols)} columns at p={args.select_prime} "
          f"(rank {total}) in {time.time()-t0:.0f}s", flush=True)

    report = {
        "schema": 1,
        "why_nonvanishing_suffices": (
            "The Jacobian is the reduction of an integer matrix, because the "
            "coordinate basis is integral with entries in {-1,0,+1} and the "
            "sample point is an integer combination of it. For an integer matrix, "
            "det = 0 implies det = 0 mod every prime. So a single prime with "
            "nonzero determinant proves the integer minor is nonzero and hence "
            "rank over Q is at least the size of the minor. No height bound, "
            "Hadamard estimate or CRT reconstruction is needed for that."),
        "why_several_primes_anyway": (
            "Agreement across primes also guards against an indexing error in "
            "selecting the minor, which a single prime would not catch."),
        "sample_seed": args.seed,
        "selection_prime": args.select_prime,
        "minor_size": len(rows),
        "row_indices_in_evaluated_order": rows,
        "row_candidate_ids": [ids[i] for i in rows],
        "column_indices": [int(c) for c in cols],
        "determinant_routines": ["modular LU with pivoting",
                                 "fraction-free Bareiss, carried out mod p"],
        "per_prime": {},
    }

    # 2. verify at every prime, rebuilding the Jacobian there
    for p in verify:
        t = time.time()
        Jp, idsp, _ = jacobian_at(p, args.seed, selection, args.flop_limit, cache_dir)
        # same candidates, same columns -- selected once, reused everywhere
        idx = [idsp.index(cid) for cid in report["row_candidate_ids"]
               if cid in idsp]
        if len(idx) != len(rows):
            report["per_prime"][str(p)] = {
                "error": "not every selected candidate evaluated at this prime",
                "available": len(idx)}
            print(f"[p={p}] SKIPPED: {len(idx)}/{len(rows)} candidates", flush=True)
            continue
        M = Jp[np.ix_(idx, cols)] % p
        d_lu = det_mod_lu(M, p)
        d_bar = det_mod_bareiss(M, p)
        entry = {
            "det_mod_p_lu": int(d_lu),
            "det_mod_p_bareiss": int(d_bar),
            "routines_agree": bool(d_lu == d_bar),
            "nonzero": bool(d_lu != 0),
            "minor_sha256": hashlib.sha256(np.ascontiguousarray(M).tobytes()).hexdigest(),
            "full_jacobian_rank_here": int(modrank(Jp, p)),
            "wall_seconds": round(time.time() - t, 1),
        }
        report["per_prime"][str(p)] = entry
        print(f"[p={p}] det={d_lu} agree={entry['routines_agree']} "
              f"nonzero={entry['nonzero']} rank={entry['full_jacobian_rank_here']} "
              f"({entry['wall_seconds']}s)", flush=True)
        Path(args.out).write_text(json.dumps(report, indent=1))

    good = [p for p, e in report["per_prime"].items()
            if e.get("nonzero") and e.get("routines_agree")]
    report["summary"] = {
        "primes_with_nonzero_minor": good,
        "n_primes_verified": len(good),
        "integer_minor_nonzero": len(good) > 0,
        "characteristic_zero_lower_bound": len(rows) if good else None,
        "statement": (
            f"An explicit {len(rows)}x{len(rows)} minor of the integral Jacobian has "
            f"nonzero determinant modulo {len(good)} distinct primes, hence is "
            f"nonzero over Z, hence rank_Q >= {len(rows)}." if good else
            "no prime certified the minor"),
    }
    Path(args.out).write_text(json.dumps(report, indent=1))
    print("done ->", args.out, json.dumps(report["summary"]), flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
