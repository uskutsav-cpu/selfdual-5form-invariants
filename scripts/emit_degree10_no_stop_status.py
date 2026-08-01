import json, hashlib
from datetime import datetime, timezone
from pathlib import Path
repo = Path("/Users/swethasunilkumar/Downloads/sdinv-jhep")
src = json.loads((repo / "verification/spinor_degree10_no_stop.json").read_text())
when = datetime.now(timezone.utc).isoformat(timespec="seconds")
by_deg = {d["degree"]: d for d in src["degrees"]}
rec = {
 "generated_utc": when,
 "final_status": "NOT REQUIRED FOR THE MANUSCRIPT CLAIMS",
 "production_run_launched": False,
 "why_not_launched": [
   "the machine is committed to the rank-certificate matrix and the standing "
   "instruction is not to start additional expensive computation",
   "even completed it would licence a claim this manuscript does not make",
 ],
 "terminal_status_by_degree": {
   str(d): {"stopped_by": by_deg[d]["stopped_by"],
            "final_rank": by_deg[d].get("final_rank", by_deg[d].get("partial_rank_reached")),
            "hilbert_target": by_deg[d].get("hilbert_target", by_deg[d].get("target")),
            "attempted_unique_graphs": by_deg[d].get("attempted_unique_graphs"), "note": by_deg[d].get("note")}
   for d in sorted(by_deg)},
 "degrees_searched_out": [d for d in sorted(by_deg)
                          if by_deg[d]["stopped_by"] == "candidate_exhaustion"],
 "degree10_stopped_by": by_deg[10]["stopped_by"],
 "strongest_claim_a_completed_run_would_licence":
   "EXHAUSTIVE WITHIN THE DEFINED FINITE GRAMMAR",
 "why_span_equality_does_not_need_it": (
   "dim_Q A10 = 14 is structural; the tensor side saturates it; the spinor "
   "family reaches 14 on the common sample with containment both ways and "
   "holdout validation. Both spans therefore equal A10, and any further "
   "grammar element is a degree-10 invariant already inside A10, so it cannot "
   "enlarge the span."),
 "argument_scope_limit": (
   "This works at degree 10 only because the tensor side saturates the full "
   "atlas there. It does not licence the same move at a degree where the "
   "tensor enumeration is itself incomplete."),
 "forbidden_claims": [
   "the degree-10 spinor grammar is exhausted",
   "the enumeration is complete at degree 10",
   "the spinor family is minimal, unique or canonical",
   "completeness of the invariant ring",
 ],
 "scope_document": "docs/DEGREE10_NO_STOP_SCIENTIFIC_CLAIM.md",
 "source_artifact": "verification/spinor_degree10_no_stop.json",
 "source_sha256": hashlib.sha256(
     (repo / "verification/spinor_degree10_no_stop.json").read_bytes()).hexdigest(),
}
out = repo / "results/degree10"
out.mkdir(parents=True, exist_ok=True)
(out / "no_stop_terminal.json").write_text(json.dumps(rec, indent=1) + "\n")
print("status:", rec["final_status"])
print("searched out:", rec["degrees_searched_out"], "| degree 10:", rec["degree10_stopped_by"])
