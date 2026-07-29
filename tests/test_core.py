"""Correctness gates. Run these before trusting any 10D number."""
import hashlib
import json
import sys, os, numpy as np, pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import sdinv.modp as modp
from sdinv.modp import P, ALT_P, mod_einsum, RankSieve
from sdinv.forms import (to_dense, random_form, metric_signs, check_star_squared,
                         selfdual_projector)
from sdinv.graphs import (canonical, enumerate_graphs, graph_from_label,
                          graph_label, load_graph_catalog, validate_graph)
from sdinv.contract import (_slot_plan, _signed, value, jacobian_row,
                            jacobian_row_amputated, build_basis_flat)

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
CATALOG = os.path.join(ROOT, "results", "10d_graph_catalog.json")
ORDER8_RESULT = os.path.join(ROOT, "results", "10d_order8.json")


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


def test_float_blas_path_is_exact(monkeypatch):
    """The accelerated float64 branch must still be exact finite-field math."""
    rng = np.random.default_rng(17)
    a = rng.integers(0, P, size=(5, 7, 3), dtype=np.int64)
    b = rng.integers(0, P, size=(3, 7, 4), dtype=np.int64)
    subscripts = "abc,cbd->ad"
    exact = np.einsum(
        subscripts, a.astype(object), b.astype(object)) % P
    monkeypatch.setattr(modp, "FLOAT_BLAS_MIN_WORK", 0)
    got = mod_einsum(subscripts, [a, b], P)
    assert np.array_equal(got, exact.astype(np.int64))


def test_reverse_jacobian_matches_amputated_oracle():
    D, PD, mod = 6, 3, P
    Fd = to_dense(
        random_form(D, PD, np.random.default_rng(23), mod), D, PD, mod)
    basis = build_basis_flat(D, PD, None, mod)
    for n in (2, 4, 6):
        M = enumerate_graphs(n, PD)[0]
        fast = jacobian_row(M, Fd, basis, D, PD, True, mod)
        oracle = jacobian_row_amputated(M, Fd, basis, D, PD, True, mod)
        assert np.array_equal(fast, oracle)


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


def test_exact_catalog_is_complete_and_collision_free():
    """The committed nauty catalog is exact at orders 4, 6, and 8."""
    with open(CATALOG) as stream:
        raw = json.load(stream)
    assert raw["generator"]["software"] == "nauty gtools 2.9.3"
    assert {n: raw["orders"][n]["count"] for n in ("4", "6", "8")} == {
        "4": 4,
        "6": 49,
        "8": 1689,
    }

    for order in (4, 6, 8):
        graphs = load_graph_catalog(CATALOG, order)
        certificates = set()
        for M in graphs:
            validate_graph(M, valence=5, max_mult=4)
            certificates.add(canonical(M))
        assert len(certificates) == len(graphs), (
            f"duplicate isomorphism class in order-{order} catalog")


def test_order8_basis_is_complete_under_two_primes():
    """Six new octic directions, matching the published Hilbert series.

    Cederwall et al. arXiv:2509.14350v2 give
      P(t) = 1 + t^4 + 2 t^6 + 7 t^8 + ...
    and factor it with (1-t^8)^-6. The seventh degree-8 scalar is I4^2,
    so six independent order-8 Jacobian directions are both necessary and
    sufficient for a complete octic generating set.
    """
    with open(ORDER8_RESULT) as stream:
        result = json.load(stream)
    generators = result["generators"]
    with open(CATALOG, "rb") as stream:
        assert hashlib.sha256(stream.read()).hexdigest() == (
            result["catalog_sha256"])
    assert [g["order"] for g in generators].count(8) == 6
    assert result["literature"]["new_generators"]["8"] == 6
    assert len(result["degree8_basis"]) == 7
    assert result["degree8_basis"][-1] == {
        "id": "I4_1^2",
        "kind": "composite",
        "expression": "I4_1^2",
    }
    for item in generators:
        catalog_graphs = load_graph_catalog(CATALOG, item["order"])
        assert graph_label(catalog_graphs[item["catalog_index"]]) == item["graph"]
    assert all(run["orders"]["8"]["rank"] == 9
               for run in result["runs"].values())

    D, PD = 10, 5
    for prime in (P, ALT_P):
        projector = selfdual_projector(D, PD, True, prime)
        Fd = to_dense(
            (projector @ random_form(
                D, PD, np.random.default_rng(20260727), prime)) % prime,
            D,
            PD,
            prime,
        )
        basis = build_basis_flat(D, PD, projector, prime)
        sieve = RankSieve(basis.shape[0], prime)
        increments = {4: 0, 6: 0, 8: 0}
        for item in generators:
            M = graph_from_label(item["graph"])
            assert sieve.add(jacobian_row(
                M, Fd, basis, D, PD, True, prime))
            increments[item["order"]] += 1
        assert increments == {4: 1, 6: 2, 8: 6}
        assert sieve.rank == 9


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
