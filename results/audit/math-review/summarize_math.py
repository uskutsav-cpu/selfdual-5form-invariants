#!/usr/bin/env python3
"""Assemble completed audit observations from this run's evidence only."""
import hashlib
import json
from math import isqrt
from pathlib import Path

ROOT=Path(__file__).resolve().parent
read=lambda name:json.loads((ROOT/name).read_text())
bareiss=read("bareiss_results.json")
fresh_minors=read("fresh_minor_bareiss_results.json")
conventions=read("conventions_results.json")
dual=read("fresh_dual_comparison.json")
reverse=read("reverse_gradient_results.json")
polynomial=read("degree12_polynomial_gradient_certificate.json")
autos=read("automorphism_sign_results.json")
signs=read("permutation_sign_results.json")
interpolation=read("interpolation_derivative_results.json")
assert all(d.get("status")=="PASS" for d in [conventions,dual,reverse,polynomial,interpolation])
assert autos["complete"] and signs["complete"]
prime_checks={p:all(p%d for d in range(2,isqrt(p)+1)) for p in [32719,32749,50021]}
assert all(prime_checks.values())
summary={"status":"PASS: independent mathematical checks in assigned scope",
         "independent_trial_division_prime_checks":prime_checks,
         "frozen_commit":"2b7663bbf5a06d1340973434f195a84ae2773e8f",
         "stored_minor_residues":[{"prime":r["prime"],"seed":r["seed"],"determinant_mod_p":r["determinant_mod_p"]} for r in bareiss["results"]],
         "fresh_independent_minor_residues":[{"prime":r["prime"],"seed":r["seed"],"determinant_mod_p":r["determinant_mod_prime"]} for r in fresh_minors["cells"]],
         "fresh_dual_cells":[{"prime":c["prime"],"seed":c["seed"],"graph_values":len(c["rows"]),"directional_derivatives":len(c["rows"])} for c in dual["cells"]],
         "independent_reverse_primary_graph_rows":sum(len(c["records"]) for c in reverse["cells"]),
         "full_production_graph_row_comparisons":162,"full_production_jacobian_entry_comparisons":162*126,
         "extra_degree12_forward_dual_comparisons":4,
         "polynomial_certificates":[{"prime":f["prime"],"points":len(f["points"]),"rank":f["rank"],
              "shape":[len(f["stacked_gradient"]),len(f["stacked_gradient"][0])],
              "minor_determinant_mod_prime":f["determinant_mod_prime"],
              "point_seeds":[p["seed"] for p in f["points"]]} for f in polynomial["fields"]],
         "automorphism_graphs":len(autos["records"]),
         "exhaustive_automorphisms":sum(r["automorphism_count"] for r in autos["records"]),
         "negative_automorphisms":sum(r["negative_count"] for r in autos["records"]),
         "numeric_graph_relabelings":len(signs["records"]),
         "numeric_negative_relabeling_signs":sum(r["numeric_induced_sign"]==-1 for r in signs["records"]),
         "numeric_odd_slot_permutations":len(signs["records"]),
         "structural_adjacent_vertex_swaps":sum(len(r["adjacent_swap_checks"]) for r in signs["records"]),
         "exact_interpolation_derivatives":[r["id"] for r in interpolation["records"]],
         "independence_limit":"Independent programs, Hodge/slots, planner, forward dual derivatives, reverse tape and sparse pullback; shared NumPy/BLAS primitives and shared custom forward kernel between independent forward/reverse methods.",
         "scope_limit":"Graph-only mathematical checks. Does not repair or certify the frozen disputed literature transcription, full invariant ring, global orbit separation or novelty."}
(ROOT/"MATH_SUMMARY.json").write_text(json.dumps(summary,indent=2)+"\n")
lines=["# Independent mathematical audit — completed continuation", "",
       "Frozen target: `2b7663bbf5a06d1340973434f195a84ae2773e8f`. All assigned graph-only mathematical checks below passed in the fresh phase02 environment. This does not change the failed phase01 source-transcription finding or certify that disputed literature mapping.","",
       "| Check | Completed observation |", "|---|---|"]
lines += [f"| Stored 81×81 minors | Independent integer Bareiss residues: {', '.join(str(r['determinant_mod_p']) for r in bareiss['results'])}. |",
          f"| Fresh independent 81×81 minors | Bareiss on independently recomputed rows: {', '.join(str(r['prime']) + ': ' + str(r['determinant_mod_prime']) for r in fresh_minors['cells'])}. |",
          "| Fresh forward-dual oracle | 81 values and 81 directional derivatives agree at each of two fresh points, primes 50021 and 32749. |",
          "| Independent reverse rows | All 162 selected full 126-entry rows agree with production and independent forward dual; four additional I12_61/I12_62 rows agree with independent forward dual. |",
          "| Conventions | Independent star²=+1, dimension 126, integral direction hash, all 81 ordered formulas/edge placements/topologies pass. |",
          f"| Automorphism signs | All {summary['exhaustive_automorphisms']} automorphisms across 81 graphs enumerated; zero negative induced signs. |",
          f"| Relabeling / odd-slot signs | 81 numerical graph relabelings, 81 numerical odd slot swaps, and {summary['structural_adjacent_vertex_swaps']} structural adjacent-vertex swaps/inverses pass. |",
          "| Value-only derivative interpolation | Exact finite-field interpolation checks one representative each at degrees 4, 6, 8, 10, 12. |","",
          "## Degree-twelve homogeneous polynomial space","",
          "Each matrix has 72 rows: ten explicit lower-product polynomials and 62 connected graph polynomials. Gradients at distinct points within one prime are concatenated horizontally; different primes are never mixed.","",
          "| Prime | Fresh points | Matrix | Rank | Independent integer-minor residue |", "|---:|---:|---|---:|---:|"]
for field in summary["polynomial_certificates"]:
    lines.append(f"| {field['prime']} | {field['points']} | {field['shape'][0]}×{field['shape'][1]} | {field['rank']} | {field['minor_determinant_mod_prime']} |")
lines += ["", "The nonzero stacked-gradient minors independently prove linear independence of the 72 homogeneous polynomials over characteristic zero. This lower bound is separate from functional rank 81. It does not assert algebraic independence of 72 degree-twelve polynomials, a complete invariant-ring presentation, or the literature upper bound itself.", "",
          "## Reproduction and limits", "",
          "`METHOD.md` gives derivations, algorithms, arithmetic bounds and independence qualifications. `SCRIPT_PROVENANCE.json` discloses the authorized reuse of independently authored script source; all numerical results, environments and intermediates are fresh. Command records in `../commands/math_*/` contain exact arguments, working directories, runtimes, exits and stdout/stderr hashes.", "",
          "`MATH_SUMMARY.json` contains exact counts and seeds. `degree12_polynomial_gradient_certificate.json` preserves full 72×252 matrices, fresh coordinates, all point gradients, pivot columns, complete integer determinants and residues. `reverse_gradient_results.json` and `fresh_dual_comparison.json` preserve derivative comparisons. `permutation_sign_results.json`, `automorphism_sign_results.json`, and `interpolation_derivative_results.json` preserve sign and interpolation evidence.", "",
          "The independent forward and reverse programs share this audit's custom forward contraction kernel. Both use NumPy/BLAS primitives, also used by production, with independently checked exact integer bounds below 2^53. No production evaluator, Hodge builder, tree planner, coordinate projector, rank sieve or verifier is imported by these independent programs. The edge records remain the specified frozen inputs; they were validated, not independently rediscovered. No 72-point value matrix is claimed: independently validated stacked gradients replaced that more expensive plan.", "",
          "The root's separate pure-Python orbit-action implementation was reviewed read-only for its sign conventions and lifting argument. Its 45 integral infinitesimal generators and nonzero modular orbit minor support generic orbit dimension 45. The global upper bound 126−45=81 uses tensor-contraction invariance, not sampled tangent annihilation alone. This branch did not duplicate that computation."]
(ROOT/"MATH_REPORT.md").write_text("\n".join(lines)+"\n")
print(json.dumps(summary,indent=2))
