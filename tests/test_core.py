"""Correctness gates. Run these before trusting any 10D number."""
import sys, os, numpy as np, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
from sdinv.modp import P, ALT_P, mod_einsum, RankSieve
from sdinv.forms import (to_dense, random_form, metric_signs, check_star_squared,
                         selfdual_projector)
from sdinv.graphs import enumerate_graphs, graph_label
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


def test_wl_hash_collides_on_regular_multigraphs():
    """WL is NOT a canonical form for these graphs.

    Every contraction graph here is valence-regular, which is the classic
    Weisfeiler-Lehman failure mode. At order 6 the WL hash merges 49 genuine
    isomorphism classes into 39 keys. enumerate_graphs keys its dict on
    canonical(), so a collision means `key not in out` is False for a
    NON-isomorphic graph and that candidate is dropped -- the rank can then
    only come out too low. This is the opposite of the harmless duplicate
    described in the module docstring.

    graphs.py avoids this at n <= EXACT_CANON_MAX_N by using the exact n!
    canonical form. This test pins the collision so that raising
    EXACT_CANON_MAX_N to cover order 8 is a deliberate, measured decision.
    """
    from sdinv.graphs import _canonical_wl, _canonical_exact, EXACT_CANON_MAX_N

    g6 = enumerate_graphs(6, 5, max_mult=4)
    assert len(g6) == 49, f"order 6 should have 49 classes, got {len(g6)}"

    exact = {_canonical_exact(M) for M in g6}
    wl = {_canonical_wl(M) for M in g6}
    assert len(exact) == 49, "exact canonicalisation must separate all 49"
    assert len(wl) < len(exact), "expected WL to collide on regular multigraphs"

    # Order 8 is enumerated with WL today, so its candidate set is not
    # provably complete. Any completeness claim at order 8 needs this raised.
    assert EXACT_CANON_MAX_N == 6, (
        "EXACT_CANON_MAX_N changed -- if it now covers order 8, delete the "
        "completeness caveat in run_10d.py and this assertion")


def test_10d_contractions_survive_a_lorentz_boost():
    """A ROTATION cannot catch a wrong metric placement; a BOOST can.

    If raised/lowered indices are assigned per-tensor rather than per-edge,
    an edge joining two same-placement vertices contracts with delta instead
    of eta. Under a pure rotation delta and eta agree on the spatial block,
    so the error hides. A boost mixes the timelike direction and exposes it.

    Over F_p a boost in the 0-1 plane is any (c, s) with c^2 - s^2 = 1:
    take c = (t + 1/t)/2, s = (1/t - t)/2 for invertible t.
    """
    D, PD, mod = 10, 5, P
    t = 7
    ti = pow(t, mod - 2, mod)
    half = pow(2, mod - 2, mod)
    c = ((t + ti) * half) % mod
    s = ((ti - t) * half) % mod
    assert (c * c - s * s) % mod == 1, "not a hyperbolic rotation"

    L = np.eye(D, dtype=np.int64)
    L[0, 0] = c; L[0, 1] = s; L[1, 0] = s; L[1, 1] = c

    eta = np.diag(metric_signs(D, True)).astype(np.int64) % mod
    assert np.array_equal((L.T @ eta @ L) % mod, eta % mod), "L is not in SO(1,9)"

    Pr = selfdual_projector(D, PD, True, mod)
    Fd = to_dense((Pr @ random_form(D, PD, np.random.default_rng(5), mod)) % mod,
                  D, PD, mod)
    Fr = np.einsum("ia,jb,kc,ld,me,abcde->ijklm", L, L, L, L, L, Fd,
                   optimize=True) % mod

    for M in enumerate_graphs(4, PD, max_mult=PD - 1):
        a = value(M, Fd, D, PD, True, mod)
        b = value(M, Fr, D, PD, True, mod)
        assert a == b, f"{graph_label(M)} is not boost invariant: {a} != {b}"


def test_order4_is_exactly_one_invariant():
    """All four order-4 graphs are the SAME invariant, rescaled.

    Order 4 in 10D admits exactly 4 connected valence-5 multigraphs. Their
    values are pairwise proportional with ratios 1, 1/2, 1/4, 1/6, so the
    Jacobian rank is 1 -- there is exactly ONE independent invariant at
    order 4, not two or three. Checked under both primes: a spurious
    proportionality would not survive a change of modulus.
    """
    D, PD = 10, 5
    expected = [1, 2, 4, 6]          # value_k = value_0 / expected[k]

    for mod in (P, ALT_P):
        Pr = selfdual_projector(D, PD, True, mod)
        graphs = enumerate_graphs(4, PD, max_mult=PD - 1)
        assert len(graphs) == 4, f"expected 4 order-4 graphs, got {len(graphs)}"

        seen = None
        for seed in (1, 2, 3):
            Fd = to_dense((Pr @ random_form(D, PD, np.random.default_rng(seed), mod))
                          % mod, D, PD, mod)
            vals = [value(M, Fd, D, PD, True, mod) % mod for M in graphs]
            assert vals[0] != 0
            ratios = [(v * pow(vals[0], mod - 2, mod)) % mod for v in vals]
            if seen is None:
                seen = ratios
            assert ratios == seen, "ratios drifted between random points"

        for r, d in zip(seen, expected):
            assert (r * d) % mod == 1, f"ratio {r} is not 1/{d} mod {mod}"

        sieve = RankSieve(build_basis_flat(D, PD, Pr, mod).shape[0], mod)
        basis = build_basis_flat(D, PD, Pr, mod)
        for M in graphs:
            sieve.add(jacobian_row(M, Fd, basis, D, PD, True, mod))
        assert sieve.rank == 1, f"order-4 rank should be 1, got {sieve.rank}"
