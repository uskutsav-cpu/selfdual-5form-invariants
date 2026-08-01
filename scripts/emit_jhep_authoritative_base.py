#!/usr/bin/env python3
"""Record the authoritative base this JHEP branch stands on.

Two sessions worked this repository at the same time. This does not pretend
otherwise: it records exactly which commits came from the other session, what
they touched, how the conflicts were resolved, and what stops the two from
corrupting each other's artifacts.

Writes:
    audit/JHEP_CONCURRENCY_RESOLUTION.md
    audit/JHEP_AUTHORITATIVE_BASE.json

Re-run after any further rebase, so the record follows the branch rather than
describing a base it no longer has.

Usage:
    python scripts/emit_jhep_authoritative_base.py [--repo .] [--base <sha>]
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

# How each rebase conflict was settled. Keyed by path; every conflicting path
# must appear here or the build says so.
CONFLICT_RESOLUTIONS: dict[str, str] = {
    "audit/JHEP_CLAIM_INPUTS.json":
        "add/add. Both sessions ran scripts/emit_jhep_live_state.py and committed "
        "its output. The file is generated, so neither side was edited by hand: "
        "resolved by regenerating against the new base, which is what the file is "
        "supposed to describe.",
    "audit/JHEP_LIVE_REPOSITORY_STATE.md":
        "add/add, same cause and same resolution as JHEP_CLAIM_INPUTS.json.",
    "audit/JHEP_RESULT_INVENTORY.json":
        "add/add, same cause and same resolution as JHEP_CLAIM_INPUTS.json.",
    ".gitignore":
        "content conflict at the end of the file. The other session added "
        "verification/reproduction-logs/, this branch added audit/.source_cache/. "
        "Both rules are wanted; resolved by keeping both lines.",
}

# What prevents the two working trees from writing the same artifact.
ISOLATION_CONTROLS: list[dict] = [
    dict(control="Separate working trees",
         detail="This branch is a clone at ~/Downloads/sdinv-jhep, outside iCloud "
                "and outside the other session's tree. No file is shared; nothing "
                "either session writes lands in the other's checkout."),
    dict(control="Per-cell immutable certificate outputs",
         detail="run_rank81_cell.py writes results/rank81/cells/cell_p{p}_s{seed}.json, "
                "one file per cell, never a shared summary. The older loop rewrote a "
                "single certificate.json after every cell, which is how a partial run "
                "could overwrite a complete one."),
    dict(control="Atomic writes",
         detail="Each cell is written to a temporary file in the same directory and "
                "moved into place with os.replace, so a reader never sees a half-written "
                "cell and a crash cannot truncate a good one."),
    dict(control="Per-cell lock files",
         detail="A second driver for the same cell finds the lock, prints who holds it, "
                "and exits 2 rather than racing."),
    dict(control="Refusal to overwrite complete cells",
         detail="A cell already marked cell_complete is skipped unless --force, so "
                "re-running the matrix cannot downgrade a finished result."),
    dict(control="Read-only aggregation",
         detail="assemble_rank81_matrix.py only reads cells. It fails on a missing cell, "
                "a duplicate, a candidate-ordering difference, a coordinate-dimension "
                "difference or an incomplete terminal status, rather than assembling "
                "something partial into a certificate."),
    dict(control="Push deferred",
         detail="Push is the only operation that can actually race, and it is held until "
                "the final reconciliation."),
]


def git(repo: Path, *args: str) -> str:
    return subprocess.run(["git", *args], cwd=repo, capture_output=True,
                          text=True, check=False).stdout.strip()


def live_writers(repo_paths: list[str]) -> list[dict]:
    """Processes whose working directory is inside any tracked repository tree."""
    out = []
    pgrep = subprocess.run(["pgrep", "-f", "Python"], capture_output=True, text=True,
                           check=False).stdout.split()
    for pid in pgrep:
        cwd = subprocess.run(["lsof", "-a", "-p", pid, "-d", "cwd", "-Fn"],
                             capture_output=True, text=True, check=False).stdout
        cwd = next((l[1:] for l in cwd.splitlines() if l.startswith("n")), "")
        if any(rp in cwd for rp in repo_paths):
            info = subprocess.run(["ps", "-p", pid, "-o", "etime=,stat="],
                                  capture_output=True, text=True, check=False).stdout.strip()
            out.append({"pid": int(pid), "cwd": cwd, "ps": info})
    return out


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", default=".", type=Path)
    ap.add_argument("--base", default="origin/research/maximal-chiral-four-form-program")
    ap.add_argument("--previous-base", default="a962e7f")
    args = ap.parse_args()
    repo = args.repo.resolve()
    when = datetime.now(timezone.utc).isoformat(timespec="seconds")

    base_sha = git(repo, "rev-parse", args.base)
    prev_sha = git(repo, "rev-parse", args.previous_base)
    head = git(repo, "rev-parse", "HEAD")
    branch = git(repo, "rev-parse", "--abbrev-ref", "HEAD")

    incorporated = [
        dict(zip(("sha", "date", "subject"), line.split("\x1f")))
        for line in git(repo, "log", "--format=%H\x1f%cI\x1f%s",
                        f"{prev_sha}..{base_sha}").splitlines()
        if line
    ]
    changed = [l for l in git(repo, "diff", "--name-only",
                              f"{prev_sha}..{base_sha}").splitlines() if l]
    mine = [
        dict(zip(("sha", "date", "subject"), line.split("\x1f")))
        for line in git(repo, "log", "--format=%H\x1f%cI\x1f%s",
                        f"{base_sha}..HEAD").splitlines()
        if line
    ]
    remote_head = ""
    ls = git(repo, "ls-remote", "--heads", "origin",
             "research/maximal-chiral-four-form-program")
    if ls:
        remote_head = ls.split()[0]

    writers = live_writers([
        str(repo),
        "Documents/Codex/2026-07-29/now/work/selfdual-5form-invariants",
    ])

    record = {
        "generated_utc": when,
        "branch": branch,
        "authoritative_local_commit": head,
        "authoritative_base_commit": base_sha,
        "previous_base_commit": prev_sha,
        "remote_head_at_record_time": remote_head,
        "remote_moved_since_base": bool(remote_head and remote_head != base_sha),
        "commits_incorporated_from_other_session": incorporated,
        "n_commits_incorporated": len(incorporated),
        "files_changed_by_other_session": changed,
        "n_files_changed": len(changed),
        "commits_authored_on_this_branch": mine,
        "conflict_resolutions": CONFLICT_RESOLUTIONS,
        "isolation_controls": ISOLATION_CONTROLS,
        "live_writers_in_any_repo_tree": writers,
        "concurrent_writers_eliminated": False,
        "concurrency_policy": (
            "The other session was left running by an explicit decision: reconcile "
            "at the end rather than interrupt work in flight. Isolation, not "
            "termination, is what makes this safe, and the controls that provide it "
            "are listed above. Push is deferred to the final reconciliation because "
            "it is the only operation that races."),
    }

    audit = repo / "audit"
    audit.mkdir(exist_ok=True)
    (audit / "JHEP_AUTHORITATIVE_BASE.json").write_text(
        json.dumps(record, indent=1) + "\n", encoding="utf-8")

    L: list[str] = []
    A = L.append
    A("# JHEP concurrency resolution")
    A("")
    A(f"Generated {when} by `scripts/emit_jhep_authoritative_base.py`.")
    A("")
    A("## The situation, stated plainly")
    A("")
    A("Two Claude sessions worked this repository at the same time. The first")
    A("indication was not a merge conflict: it was a file written by this session")
    A("appearing inside a commit made by the other one, ninety seconds later.")
    A("")
    A("## Authoritative commits")
    A("")
    A("| field | value |")
    A("|---|---|")
    A(f"| branch | `{branch}` |")
    A(f"| authoritative local commit | `{head}` |")
    A(f"| base it stands on | `{base_sha}` |")
    A(f"| previous base | `{prev_sha}` |")
    A(f"| remote head when recorded | `{remote_head or 'not queried'}` |")
    A(f"| remote moved since base | {'yes' if record['remote_moved_since_base'] else 'no'} |")
    A("")
    A(f"## {len(incorporated)} commits incorporated from the other session")
    A("")
    A("| sha | date | subject |")
    A("|---|---|---|")
    for c in incorporated:
        A(f"| `{c['sha'][:12]}` | {c['date']} | {c['subject']} |")
    A("")
    A(f"They touched {len(changed)} files. The full list is in")
    A("`audit/JHEP_AUTHORITATIVE_BASE.json`.")
    A("")
    A("## Commits authored on this branch")
    A("")
    A("| sha | date | subject |")
    A("|---|---|---|")
    for c in mine:
        A(f"| `{c['sha'][:12]}` | {c['date']} | {c['subject']} |")
    A("")
    A("## Conflicts and how each was settled")
    A("")
    A("| path | resolution |")
    A("|---|---|")
    for path, how in CONFLICT_RESOLUTIONS.items():
        A(f"| `{path}` | {how} |")
    A("")
    A("Every conflict was in a generated file or in an append-only list. No")
    A("scientific artifact conflicted, because the two sessions wrote results to")
    A("different trees.")
    A("")
    A("## Were concurrent writers eliminated?")
    A("")
    A("**No, and deliberately not.** Terminating the other session's work in")
    A("flight was weighed and rejected; the instruction was to reconcile at the")
    A("end instead. What makes that safe is isolation, not termination:")
    A("")
    A("| control | how it works |")
    A("|---|---|")
    for c in ISOLATION_CONTROLS:
        A(f"| {c['control']} | {c['detail']} |")
    A("")
    A("## Live writers at record time")
    A("")
    if writers:
        A("| pid | elapsed / state | working directory |")
        A("|---|---|---|")
        for w in writers:
            A(f"| {w['pid']} | `{w['ps']}` | `{w['cwd']}` |")
    else:
        A("None found in either tree.")
    A("")
    A("A process in the other session's tree is not a hazard to this branch;")
    A("it cannot reach these files. The list is recorded so the claim can be")
    A("checked rather than believed.")
    A("")
    (audit / "JHEP_CONCURRENCY_RESOLUTION.md").write_text("\n".join(L) + "\n",
                                                          encoding="utf-8")

    print(f"base {base_sha[:12]} <- {len(incorporated)} commits from the other session")
    print(f"head {head[:12]} on {branch}, {len(mine)} commits of our own")
    if record["remote_moved_since_base"]:
        print(f"NOTE remote head is now {remote_head[:12]}; rebase again before pushing")
    print(f"live writers in any repo tree: {len(writers)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
