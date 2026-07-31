#!/usr/bin/env python3
"""Independent reverse benchmark: recover Q10 from block topology alone.

Generation NEVER consults the published equation-(4.24) formulas or their
coordinate vectors. `sdinv.reverse_block_decomposition` does not import
`sdinv.published_degree10_invariants`, and this runner only loads the published
result AFTER the search, for comparison.

Usage:
    reverse_engineer_degree10_benchmark.py [--limit N] [--pilot]
"""
import argparse
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tests"))

from sdinv.exactmap import rank_mod
from sdinv.forms import selfdual_projector, to_dense, random_form
from sdinv.projection_checkpoint import ProjectionCheckpoint, peak_rss_mb
from sdinv.reverse_block_decomposition import (
    block_multisets, build_einsum, evaluate, generate_candidates, make_blocks,
    stream_candidates)
from solve_intrinsic_quotients import rref, project
from stress_flow_closure import closure_span
from test_M_only_quotients import registry_items, evaluate_atlas_element, solve_exact

CERT = ROOT / "results" / "stress_flow" / "certificates"
SEED8 = {4: ["I4_1"], 6: ["I6_2"], 8: ["I8_3", "I8_4", "I8_5", "I8_6"]}
FIT, HOLDOUT = 32749, 32717
R = ROOT / "results" / "intrinsic_candidates"
OUT = R / "degree10_reverse_benchmark.json"
CKPT = Path(os.environ.get("SDINV_CKPT_ROOT")
            or Path(os.environ.get("TMPDIR", "/tmp")) / "sdinv_ckpt") / "reverse10"


def sample(prime, seed):
    pr = selfdual_projector(10, 5, True, prime)
    return to_dense((pr @ random_form(10, 5, np.random.default_rng(seed), prime))
                    % prime, 10, 5, prime)


def atlas_context(prime):
    with (CERT / f"interacting_degree12_{prime}.json").open() as s:
        cert = json.load(s)
    _, bmap, span = closure_span(cert, SEED8, prime)
    names = bmap[10]
    ech, piv = rref(span[10], prime)
    free = [j for j in range(len(names)) if j not in set(piv)]
    return names, ech, piv, free


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--limit", type=int, default=400,
                    help="max candidates evaluated per block multiset")
    ap.add_argument("--max-topologies", "--topology-cap", dest="max_topologies",
                    type=int, default=60000,
                    help="raw-topology cap per sector; a sector that hits it "
                         "is reported truncated and is NOT exhausted")
    ap.add_argument("--sector", action="append", default=None,
                    help="restrict to a named sector, e.g. N1050+N1050+N1050"
                         "+N1050+N1050; repeatable")
    ap.add_argument("--shard-residue", type=int, default=0)
    ap.add_argument("--shard-modulus", type=int, default=1,
                    help="deterministic sharding on the CANONICAL key, so two "
                         "shards can never claim the same scalar and the union "
                         "over residues is exactly the unsharded set")
    ap.add_argument("--resume", action="store_true",
                    help="reuse checkpointed atlas and candidate evaluations")
    ap.add_argument("--stop-after-candidates", type=int, default=None)
    ap.add_argument("--stop-after-seconds", type=float, default=None)
    ap.add_argument("--max-rss-mb", type=float, default=None,
                    help="abort cleanly if resident memory exceeds this")
    ap.add_argument("--pilot", action="store_true",
                    help="stop after the first multiset that yields rank")
    args = ap.parse_args()

    started = time.time()
    items = registry_items()
    names, ech, piv, free = atlas_context(FIT)
    n_samples = len(names) + 8
    forms = [sample(FIT, 41000 + 11 * i) for i in range(n_samples)]

    atlas_sha = hashlib.sha256(json.dumps(names).encode()).hexdigest()[:32]
    store = ProjectionCheckpoint(
        CKPT / f"prime_{FIT}",
        {"atlas_sha256": atlas_sha, "degree": 10, "prime": FIT,
         "evaluator_version": "reverse-v1"})

    print(f"atlas {len(names)} columns, {n_samples} samples, prime {FIT}",
          flush=True)
    A = []

    for i, form in enumerate(forms):
        row = []
        for j, nm in enumerate(names):
            unit = store.load_unit(FIT, i, j, fingerprint=atlas_sha)
            if unit is None:
                t0 = time.time()
                val = evaluate_atlas_element(items[nm], items, form, FIT, {})
                store.save_unit(FIT, i, j, nm, val, time.time() - t0,
                                fingerprint=atlas_sha)
                row.append(int(val) % FIT)
            else:
                row.append(int(unit["value"]) % FIT)
        A.append(row)
        store.flush_manifest()
    print(f"atlas built in {time.time()-started:.0f}s", flush=True)

    # --- enumerate every sector first, then evaluate SAMPLE-OUTER ----------
    # Candidate-outer would rebuild the three quadratic blocks for every
    # (candidate, sample) pair, and the block build is ~4.4 s against ~150 ms
    # for one contraction -- thirty times the cost of the thing being measured.
    # Caching all samples' blocks instead would hold 22 x 16 MB, which this
    # machine does not have. Sample-outer builds each sample's blocks once and
    # sweeps every candidate against them.
    # STREAMED generation. The list form materialised every topology before
    # any filtering -- up to 30 000 dicts per sector, all live at once -- which
    # drove enumeration RSS to ~2.6 GB across 21 sectors. Streaming
    # canonicalises and discards immediately, so only compact canonical KEYS
    # accumulate; the same sector now peaks at ~33 MB.
    stats_all = {}
    plan = []
    wanted = set(args.sector) if args.sector else None
    for ms in block_multisets(5):
        label = "+".join(ms)
        if wanted and label not in wanted:
            continue
        t0 = time.time()
        kept, last = [], {}
        for topo, st in stream_candidates(
                list(ms), cap=args.max_topologies,
                shard_residue=args.shard_residue,
                shard_modulus=args.shard_modulus,
                max_candidates=args.limit):
            kept.append(topo)
            last = st
        stats = {
            "raw_topologies": last.get("raw", 0),
            "disconnected": last.get("disconnected", 0),
            "duplicate_canonical": last.get("duplicate", 0),
            "canonical": last.get("yielded", 0),
            "truncated": last.get("raw", 0) >= args.max_topologies,
            "enumeration_seconds": round(time.time() - t0, 1),
            "selected_for_evaluation": len(kept),
            "peak_rss_mb_after_sector": round(peak_rss_mb(), 1),
        }
        stats_all[label] = stats
        for topo in kept:
            try:
                spec, _ = build_einsum(list(ms), topo)
            except ValueError:
                continue
            plan.append({"multiset": list(ms), "label": label,
                         "topology": topo, "einsum": spec})
        print(f"  {label}: canon={stats['canonical']} "
              f"selected={len(kept)} truncated={stats['truncated']} "
              f"rss={stats['peak_rss_mb_after_sector']}MB "
              f"{stats['enumeration_seconds']}s", flush=True)
        if args.max_rss_mb and peak_rss_mb() > args.max_rss_mb:
            print(f"  ABORT: RSS {peak_rss_mb():.0f}MB exceeds "
                  f"--max-rss-mb {args.max_rss_mb}", flush=True)
            break
        if args.stop_after_candidates and len(plan) >= args.stop_after_candidates:
            break
        if args.stop_after_seconds and time.time() - started > args.stop_after_seconds:
            break

    print(f"\nevaluating {len(plan)} candidates on {n_samples} samples",
          flush=True)
    values = [[0] * n_samples for _ in plan]
    for i, form in enumerate(forms):
        t0 = time.time()
        blocks = make_blocks(form, FIT)
        for ci, cand in enumerate(plan):
            try:
                values[ci][i] = evaluate(cand["multiset"], cand["topology"],
                                         blocks, FIT)
            except Exception:
                values[ci][i] = None
        del blocks
        print(f"    sample {i+1}/{n_samples}  {time.time()-t0:.1f}s "
              f"rss={peak_rss_mb():.0f}MB", flush=True)

    quotient_rows, found, rank = [], [], 0
    per_label = {}
    for ci, cand in enumerate(plan):
        b = values[ci]
        acc = per_label.setdefault(cand["label"],
                                   {"evaluated": 0, "in_atlas_span": 0,
                                    "nonzero_quotient": 0})
        if any(v is None for v in b):
            continue
        acc["evaluated"] += 1
        x, ok = solve_exact(A, b, FIT)
        if not ok:
            continue
        acc["in_atlas_span"] += 1
        q = project(x, ech, piv, free, FIT)
        if not any(v % FIT for v in q):
            continue
        acc["nonzero_quotient"] += 1
        trial = quotient_rows + [q]
        nr = rank_mod(np.asarray(trial, dtype=np.int64) % FIT, FIT)
        if nr > rank:
            rank, quotient_rows = nr, trial
            found.append({"multiset": cand["multiset"], "einsum": cand["einsum"],
                          "quotient_vector": q, "rank_after": rank})
            print(f"    RANK {rank}/3 from {cand['label']}  {cand['einsum']}",
                  flush=True)
            if rank == 3:
                break
    for label, acc in per_label.items():
        stats_all.setdefault(label, {}).update(acc)

    payload = {
        "schema": 1,
        "independence": ("generation never imports or inspects "
                         "published_degree10_invariants or its coordinates"),
        "fit_prime": FIT,
        "atlas_columns": len(names),
        "dim_Q10": len(free),
        "recovered_rank": rank,
        "recovered_vectors": quotient_rows,
        "recovered_candidates": found,
        "per_multiset": stats_all,
        "limit_per_multiset": args.limit,
        "max_topologies": args.max_topologies,
        "runtime_seconds": round(time.time() - started, 1),
        "peak_rss_mb": round(peak_rss_mb(), 1),
    }
    OUT.write_text(json.dumps(payload, indent=1, sort_keys=True) + "\n")
    print(f"\nrecovered Q10 rank {rank}/{len(free)} in "
          f"{payload['runtime_seconds']}s, peak {payload['peak_rss_mb']} MB")
    print(f"wrote {OUT.name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
