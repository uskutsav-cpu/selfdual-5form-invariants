"""Exact linear algebra over F_p.

Why: invariant values span a huge dynamic range at high order, so float SVD
forces you to guess a rank tolerance. Over F_p, zero means zero.

p is chosen ~2^20 so that products fit comfortably in int64 during einsum
accumulation (product < 2^40, summed over <2^17 terms stays < 2^57).
Rank over F_p at a random point equals the true rank with probability
1 - O(degree/p). Re-run with ALT_P to confirm.
"""

import numpy as np

P = 32749  # prime, ~2^15 -- see the overflow guard in mod_einsum
ALT_P = 32719  # second prime for confirmation runs


def inv(a, p=P):
    """Modular inverse via Fermat."""
    return pow(int(a) % p, p - 2, p)


class RankSieve:
    """Streaming row-reduced basis over F_p.

    Feed it one Jacobian row at a time. Returns True if the row was
    independent of everything seen so far (i.e. a genuinely new invariant),
    False if it reduced to zero (i.e. you found a syzygy).

    Memory is O(rank * ncols), not O(ncandidates * ncols).
    """

    def __init__(self, ncols, p=P):
        self.p = p
        self.ncols = ncols
        self.rows = []   # reduced basis rows
        self.pivots = []  # pivot column of each basis row

    def add(self, row):
        row = np.asarray(row, dtype=np.int64) % self.p
        for r, pc in zip(self.rows, self.pivots):
            if row[pc]:
                row = (row - int(row[pc]) * r) % self.p
        nz = np.nonzero(row)[0]
        if len(nz) == 0:
            return False
        pc = int(nz[0])
        row = (row * inv(row[pc], self.p)) % self.p
        # back-substitute into existing rows to keep basis fully reduced
        for i, (r, q) in enumerate(zip(self.rows, self.pivots)):
            if r[pc]:
                self.rows[i] = (r - int(r[pc]) * row) % self.p
        self.rows.append(row)
        self.pivots.append(pc)
        return True

    @property
    def rank(self):
        return len(self.rows)


def mod_einsum(subscripts, operands, p=P):
    """einsum over F_p, contracting STRICTLY TWO AT A TIME with reduction
    after every step.

    Two traps this avoids, both of which produce wrong answers silently:

    1. OVERFLOW. np.einsum multiplies all operands before summing, so at
       order n the products reach p^n. Even asking numpy for an optimised
       path does not help -- for a symmetric contraction it will happily
       return a single step contracting all n operands at once. int64
       wraps with no warning and the result is garbage. We therefore never
       hand einsum more than two operands.

    2. MEMORY. Contracting in a bad order builds enormous intermediates
       (order 8 in 6D wanted 16 GiB). We greedily pick the pair whose
       result has the fewest free indices.

    An explicit guard asserts p^2 * (terms summed) stays inside int64.
    """
    ins, out = subscripts.split("->")
    terms = ins.split(",")
    ops = [np.asarray(o, dtype=np.int64) % p for o in operands]

    while len(ops) > 1:
        best = None
        for i in range(len(ops)):
            for j in range(i + 1, len(ops)):
                rest = set("".join(terms[k] for k in range(len(terms))
                                   if k not in (i, j))) | set(out)
                keep = [c for c in dict.fromkeys(terms[i] + terms[j])
                        if c in rest]
                # Cost of this pair is output size TIMES summed size, i.e.
                # the product over every index appearing in either operand.
                # Ranking by len(keep) alone minimises the intermediate but
                # not the work: a step can have a tiny output and still sum
                # ~1e9 terms, which passes the overflow guard below and then
                # runs for hours on numpy's scalar integer loop (there is no
                # BLAS for int64). Rank by work, break ties on output size so
                # the original memory behaviour is preserved.
                d = {}
                for t, o in ((terms[i], ops[i]), (terms[j], ops[j])):
                    for c, n in zip(t, o.shape):
                        d[c] = n
                work = 1
                for c in set(terms[i] + terms[j]):
                    work *= d[c]
                outsz = 1
                for c in keep:
                    outsz *= d[c]
                if best is None or (work, outsz) < (best[0], best[1]):
                    best = (work, outsz, i, j, keep)
        _, _, i, j, keep = best
        ti, tj, oi, oj = terms[i], terms[j], ops[i], ops[j]

        dims = {}
        for t, o in ((ti, oi), (tj, oj)):
            for c, n in zip(t, o.shape):
                dims[c] = n
        nterms = 1
        for c in set(ti + tj) - set(keep):
            nterms *= dims[c]
        if (p - 1) ** 2 * nterms >= 2 ** 63:
            raise OverflowError(
                f"int64 would overflow: p^2 * {nterms} summed terms. "
                f"Lower P in modp.py.")

        res = np.einsum(f"{ti},{tj}->{''.join(keep)}", oi, oj) % p
        for k in sorted((i, j), reverse=True):
            terms.pop(k)
            ops.pop(k)
        terms.append("".join(keep))
        ops.append(res)

    if terms[0] != out:
        ops[0] = np.einsum(f"{terms[0]}->{out}", ops[0]) % p
    return ops[0]
