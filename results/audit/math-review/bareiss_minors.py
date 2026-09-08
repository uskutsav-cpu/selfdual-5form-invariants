#!/usr/bin/env python3
"""Independent integer determinants of the frozen stored Jacobian minors.

No repository imports or finite-field elimination routines are used. Lift the
stored residues to integers, evaluate their determinant with exact Bareiss
division, and reduce the final integer modulo the advertised prime.
"""
import hashlib
import json
from pathlib import Path
import time

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT.parent / "frozen-checkout/results/rank81_certificate.json"
EXPECTED = {(32749, 20260907): 20345, (32749, 20260908): 30761,
            (32719, 20260907): 1653, (32719, 20260908): 2167}


def bareiss(matrix):
    a = [list(map(int, row)) for row in matrix]
    n = len(a)
    assert n and all(len(row) == n for row in a)
    prior = 1
    sign = 1
    swaps = 0
    for k in range(n - 1):
        if not a[k][k]:
            pivot_row = next((i for i in range(k + 1, n) if a[i][k]), None)
            if pivot_row is None:
                return 0, swaps
            a[k], a[pivot_row] = a[pivot_row], a[k]
            sign = -sign
            swaps += 1
        pivot = a[k][k]
        for i in range(k + 1, n):
            for j in range(k + 1, n):
                quotient, remainder = divmod(a[i][j] * pivot - a[i][k] * a[k][j], prior)
                assert remainder == 0, (k, i, j, "inexact Bareiss division")
                a[i][j] = quotient
            a[i][k] = 0
        prior = pivot
    return sign * a[-1][-1], swaps


def main():
    assert bareiss([[0, 2], [3, 4]])[0] == -6
    assert bareiss([[1, 2], [2, 4]])[0] == 0
    assert bareiss([[6, 1, 1], [4, -2, 5], [2, 8, 7]])[0] == -306
    data = json.loads(SOURCE.read_text())
    rows = []
    for witness in data["witnesses"]:
        key = witness["prime"], witness["seed"]
        columns = witness["pivot_columns"]
        assert len(columns) == len(set(columns)) == 81
        jacobian = witness["jacobian"]
        assert len(jacobian) == 81 and all(len(row) == 126 for row in jacobian)
        assert all(0 <= x < key[0] for row in jacobian for x in row)
        minor = [[row[c] for c in columns] for row in jacobian]
        started = time.monotonic()
        determinant, swaps = bareiss(minor)
        residue = determinant % key[0]
        row = {"prime": key[0], "seed": key[1], "dimension": 81,
               "pivot_columns": columns, "integer_determinant": str(determinant),
               "integer_determinant_digits": len(str(abs(determinant))),
               "row_swaps": swaps, "determinant_mod_p": residue,
               "expected_mod_p": EXPECTED[key],
               "stored_mod_p": witness["determinant_mod_p"],
               "seconds": time.monotonic() - started}
        rows.append(row)
        (ROOT / "bareiss_results.json").write_text(json.dumps({
            "certificate_sha256": hashlib.sha256(SOURCE.read_bytes()).hexdigest(),
            "implementation": "exact integer fraction-free Bareiss, final reduction only",
            "results": rows}, indent=2) + "\n")
        print(json.dumps(row), flush=True)
        assert residue == EXPECTED[key] == witness["determinant_mod_p"], "STOP: determinant mismatch"
    assert set((r["prime"], r["seed"]) for r in rows) == set(EXPECTED)


if __name__ == "__main__":
    main()
