"""Correctness gates. Run these before trusting any 10D number."""
import sys, os, numpy as np, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sdinv.modp import P, ALT_P, mod_einsum, RankSieve
from sdinv.forms import (to_dense, random_form, metric_signs, check_star_squared,
                         selfdual_projector)
from sdinv.graphs import enumerate_graphs
from sdinv.contract import _slot_plan, _signed, value, jacobian_row, build_basis_flat


def _ops(M, Fd, PD, mod):
    slots, tails = _slot_plan(M, PD)
    s = metric_signs(Fd.shape[0], True) % mod
    sub = ",".join("".join(x) for x in slots) + "->"
    return sub, [_signed(Fd, tails[v], s, mod) for v in range(M.shape[0])]


@pytest.mark.parametrize("n", [2, 4, 6])
def test_mod_einsum_matches_exact_bigint(n):
    """THE critical test. int64 overflow in einsum silently produces wrong
    numbers that look completely plausible. This caught three real bugs."""
    D, PD, mod = 6, 3, P
    Fd = to_dense(random_form(D, PD, np.random.default_rng(7), mod), D, PD, mod)
    for M in enumerate_graphs(n, PD):
        sub, ops = _ops(M, Fd, PD, mod)
        exact = int(np.einsum(sub, *[o.astype(object) for o in ops])) % mod
        assert int(mod_einsum(sub, ops, mod)) == exact


def test_contractions_are_lorentz_invariant():
    """Rotation by the 3-4-5 triple, exact over F_p. If a contraction is not
    invariant, the metric orientation is wrong and rank bounds are void."""
    D, PD, mod = 6, 3, P
    inv5 = pow(5, mod - 2, mod)
    c, s = (3 * inv5) % mod, (4 * inv5) % mod
    R = np.eye(D, dtype=np.int64)
    R[1, 1] = c; R[1, 2] = s; R[2, 1] = (-s) % mod; R[2, 2] = c
    Fd = to_dense(random_form(D, PD, np.random.default_rng(7), mod), D, PD, mod)
    Fr = np.einsum("ia,jb,kc,abc->ijk", R, R, R, Fd, optimize=True) % mod
    for n in [2, 4, 6]:
        for M in enumerate_graphs(n, PD):
            assert value(M, Fd, D, PD, True, mod) == value(M, Fr, D, PD, True, mod)


def test_6d_reproduces_five_invariants():
    """Elamaran-Ferko-Scarlett arXiv:2512.23750: 5 invariants, 1,2,1,1."""
    D, PD, mod = 6, 3, P
    Fd = to_dense(random_form(D, PD, np.random.default_rng(11), mod), D, PD, mod)
    B = build_basis_flat(D, PD, None, mod)
    sieve, pattern = RankSieve(B.shape[0], mod), []
    for n in [2, 4, 6, 8]:
        before = sieve.rank
        for M in enumerate_graphs(n, PD):
            sieve.add(jacobian_row(M, Fd, B, D, PD, True, mod))
        pattern.append(sieve.rank - before)
    assert sieve.rank == 5 and pattern == [1, 2, 1, 1]


def test_10d_selfduality_wellposed():
    assert check_star_squared(10, 5, True, P) == 1
    Pr = selfdual_projector(10, 5, True, P)
    assert np.array_equal((Pr @ Pr) % P, Pr % P)
    s = RankSieve(Pr.shape[1], P)
    for r in Pr:
        s.add(r)
    assert s.rank == 126


def test_10d_quadratic_invariant_vanishes():
    """F ^ F = 0 for odd-degree forms; self-duality gives F ^ *F = F ^ F,
    so F.F = 0 identically. Free correctness check on the projector."""
    Pr = selfdual_projector(10, 5, True, P)
    Fv = (Pr @ random_form(10, 5, np.random.default_rng(1), P)) % P
    Fd = to_dense(Fv, 10, 5, P)
    M = enumerate_graphs(2, 5, max_mult=5)[0]
    assert value(M, Fd, 10, 5, True, P) == 0
