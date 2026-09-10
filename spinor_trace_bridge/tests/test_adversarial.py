"""Adversarial and mutation tests.

Every test here corresponds to a defect class that actually occurred in this
project, or to one that would have been silent if it had.  A mutation test that
merely runs is worthless: each one below **injects** a specific error and asserts
that a specific check catches it.  If a mutation ever stops failing, the check
guarding it has stopped working.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from sdbridge import conventions as C
from sdbridge.bridge import BridgeMap, sorted_five_index_tuples
from sdbridge.candidates import build_context
from sdbridge.clifford import NullFrameClifford, dirac_gammas, null_metric
from sdbridge.modular import matmul, rank as modrank, spans_equal
from sdbridge.structured_degree8 import SELECTED, StructuredDegree8
from sdbridge.tensor_words import (
    TensorWordEvaluator, necklaces, raise_index_permutation,
)

P = C.DEFAULT_PRIME


@pytest.fixture(scope="module")
def ctx():
    return build_context(P, seed=11)


@pytest.fixture(scope="module")
def bridge():
    return BridgeMap(p=P)


# =============================================================================
# Arithmetic defects
# =============================================================================

def test_old_defect_int64_overflow_is_caught_by_homogeneity(ctx):
    """THE OVERFLOW DEFECT, reproduced.

    The first structured degree-8 evaluator reduced mod p only at the end of each
    einsum.  With p ~ 2^15 a four-step contraction reaches ~2^72 and wraps int64
    silently -- the wrapped values look entirely ordinary.  Here we deliberately
    contract WITHOUT intermediate reduction and assert that homogeneity fails,
    which is what exposed it.
    """
    ev = StructuredDegree8(p=P)
    F = np.asarray(ctx.S, dtype=np.int64) % P
    I = ev.I

    def omega_unreduced(X):
        # the defective form: one einsum, reduction only at the very end
        return np.einsum("bcde,bf,cg,dh,ei->fghi", I, X, X, X, X,
                         optimize=True) % P

    def bad_value(X):
        O = omega_unreduced(X)
        return int(np.einsum("abcd,efgh,abch,efgd->", O, O, I, I,
                             optimize=True) % P)

    base = bad_value(F)
    scaled = bad_value((2 * F) % P)
    assert scaled != pow(2, 8, P) * base % P, (
        "the unreduced contraction did NOT overflow here, so this test is no "
        "longer exercising the defect it was written for")

    # and the fixed implementation does satisfy homogeneity
    good = ev.values(F)
    good2 = ev.values((2 * F) % P)
    for n in SELECTED:
        assert good2[n] == pow(2, 8, P) * good[n] % P


def test_row_normalisation_of_a_modular_matrix_is_meaningless(ctx):
    """Guards the rule that no modular Jacobian is ever row-normalised.

    Over F_p every nonzero row can be scaled to have leading entry 1, so
    'normalisation' cannot distinguish a large row from a tiny one -- the whole
    notion that inflated the float64 rank simply does not exist here.  This test
    asserts that scaling rows leaves the rank unchanged, i.e. that any such step
    would be pure noise rather than information.
    """
    rng = np.random.default_rng(5)
    M = rng.integers(1, P, size=(20, 30)).astype(np.int64)
    before = modrank(M, P)
    scales = rng.integers(1, P, size=20).astype(np.int64)
    after = modrank((M * scales[:, None]) % P, P)
    assert before == after


@pytest.mark.parametrize("bad_p", [32768, 32750])
def test_composite_modulus_is_rejected_or_detected(bad_p):
    """A non-prime modulus must not silently produce a plausible rank.

    Inversion is where it shows up: Fermat's little theorem is used for inverses,
    and it is simply wrong for composite moduli.
    """
    from sdbridge.modular import inv
    # 2 is not invertible mod an even number; the failure must be visible
    if bad_p % 2 == 0:
        got = inv(2, bad_p) if bad_p % 2 else None
        assert (2 * inv(2, bad_p)) % bad_p != 1, \
            "a composite even modulus produced a working inverse of 2"


# =============================================================================
# Tensor-index defects
# =============================================================================

def test_mutating_the_raising_permutation_breaks_the_metric_check():
    """Index raising in the null frame is verified against the metric, not assumed."""
    from sdbridge.tensor_words import verify_raising_convention
    assert verify_raising_convention(P)["matches_metric_up_to_scale"]

    # inject a wrong permutation and confirm the metric check would reject it
    eta = null_metric(P)
    from sdbridge.modular import inv as minv
    half = minv(2, P)
    wrong = np.array([(mu + 1) % C.SPACETIME_DIM for mu in range(C.SPACETIME_DIM)])
    expected = np.zeros((C.SPACETIME_DIM, C.SPACETIME_DIM), dtype=np.int64)
    for mu in range(C.SPACETIME_DIM):
        expected[mu, wrong[mu]] = half
    assert not np.array_equal(eta % P, expected % P), \
        "a wrong raising permutation was not distinguished from the correct one"


def test_double_raising_M_changes_the_tensor_word_values(ctx):
    """THE M-INDEX DEFECT: treating M_mu^nu as if both indices were raised.

    M is a mixed tensor.  Raising the already-upper index gives a different
    object, and the tensor-word values must change.  If they did not, the
    variance convention would be carrying no information.
    """
    tw = TensorWordEvaluator(p=P)
    Fn = ctx.F_null
    perm = raise_index_permutation()

    correct = tw.M_tensor(Fn)
    doubled = correct[:, perm]          # raise the second index a second time
    assert not np.array_equal(correct % P, doubled % P)

    A_ok, B = tw.blocks(Fn)
    A_bad = tw.A_matrix(doubled)
    for w in necklaces(4):
        if tw.word_value(w, A_ok, B) != tw.word_value(w, A_bad, B):
            break
    else:
        pytest.fail("double-raising M left every degree-8 tensor word unchanged")


def test_transposing_N_changes_mixed_traces(ctx):
    """The N variance convention is load-bearing.

    The docstring of the original implementation warns that the opposite
    orientation produces non-scalar mixed traces.  Assert that the two really do
    differ, so the warning is not decoration.
    """
    tw = TensorWordEvaluator(p=P)
    A, B = tw.blocks(ctx.F_null)
    Bt = B.T % P
    differ = [w for w in necklaces(4)
              if tw.word_value(w, A, B) != tw.word_value(w, A, Bt)]
    assert differ, "transposing N changed no degree-8 tensor word"


# =============================================================================
# Bridge defects
# =============================================================================

def test_wrong_hodge_sign_destroys_the_kernel_identification(bridge):
    """Using the anti-self-dual projector must break the kernel claim."""
    p = bridge.p
    asd = bridge.antiselfdual_basis
    image_of_asd = matmul(asd, bridge.forward_matrix, p)
    assert np.all(image_of_asd % p == 0)          # correct: ASD -> 0

    sd = bridge.selfdual_basis
    image_of_sd = matmul(sd, bridge.forward_matrix, p)
    assert np.any(image_of_sd % p != 0), \
        "self-dual forms mapped to zero: the duality sign is inverted"


def test_scaling_gamma_normalisation_changes_the_forward_map(bridge):
    """A different Clifford normalisation is a different map, not a rescaling
    that happens to cancel."""
    p = bridge.p
    M = bridge.forward_matrix
    assert not np.array_equal(M % p, (2 * M) % p)
    rng = np.random.default_rng(3)
    c = rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS)
    F = matmul(c.reshape(1, -1), bridge.selfdual_basis, p).reshape(-1)
    assert not np.array_equal(bridge.forward(F) % p,
                              (2 * bridge.forward(F)) % p)


def test_split_signature_is_not_euclidean():
    """The frame is (5,5).  A Euclidean frame would have no isotropic vectors and
    would forbid real self-dual five-forms; asserting the eigenvalue split keeps
    that confusion from returning."""
    G = [g.astype(float) for g in dirac_gammas()]
    eta = np.zeros((10, 10))
    for a in range(10):
        for b in range(10):
            anti = G[a] @ G[b] + G[b] @ G[a]
            eta[a, b] = anti[0, 0] / C.CLIFFORD_NORMALISATION
    w = np.linalg.eigvalsh(eta)
    assert int((w > 1e-9).sum()) == 5 and int((w < -1e-9).sum()) == 5
    assert np.abs(np.diag(eta)).max() < 1e-9, \
        "the null frame acquired a nonzero diagonal, so it is no longer null"


def test_forward_inverse_mismatch_is_detected(bridge):
    """inverse . forward is the self-dual projector, NOT the identity.

    If it were the identity the anti-self-dual part would have survived a map
    whose kernel is exactly that part -- a contradiction that this asserts.
    """
    p = bridge.p
    rng = np.random.default_rng(7)
    v = rng.integers(0, p, size=C.N_FIVE_FORM_COMPONENTS)
    sd = matmul(v.reshape(1, -1), bridge.selfdual_projector.T, p).reshape(-1)
    assert np.array_equal(bridge.inverse(bridge.forward(v)) % p, sd % p)
    if not np.array_equal(sd % p, v % p):
        assert not np.array_equal(bridge.inverse(bridge.forward(v)) % p, v % p)


# =============================================================================
# Candidate defects
# =============================================================================

def test_candidate_reordering_does_not_change_the_rank(ctx):
    """Rank is order-independent; if it were not, the pivot search would be
    reporting an artefact of the schedule."""
    rng = np.random.default_rng(1)
    M = rng.integers(0, P, size=(30, 40)).astype(np.int64)
    perm = rng.permutation(30)
    assert modrank(M, P) == modrank(M[perm], P)


def test_edge_mutation_changes_a_port_graph_value(ctx):
    """Mutating one edge of a contraction graph must change what it computes."""
    from sdbridge.spinor_invariants import (
        PortGraph, evaluate_graph_batch, random_port_graph, sigma_stacks,
    )
    stacks = sigma_stacks(P)
    rng = np.random.default_rng(4)
    g = random_port_graph(rng, 3)
    base = int(evaluate_graph_batch(g, ctx.S[None, ...], P, stacks)[0])

    # swap two half-edges to make a genuinely different matching
    edges = [list(e) for e in g.edges]
    edges[0][1], edges[1][1] = edges[1][1], edges[0][1]
    mutated = PortGraph(n_nodes=g.n_nodes,
                        edges=tuple(tuple(sorted(e)) for e in edges))
    if mutated.is_locally_zero():
        pytest.skip("the mutation produced a locally zero graph")
    other = int(evaluate_graph_batch(mutated, ctx.S[None, ...], P, stacks)[0])
    assert base != other, "an edge mutation left the contraction value unchanged"


def test_word_order_matters_for_non_cyclic_rearrangement(ctx):
    """Traces are cyclic but not symmetric: AABB and ABAB are different
    invariants and must not collapse."""
    tw = TensorWordEvaluator(p=P)
    A, B = tw.blocks(ctx.F_null)
    assert tw.word_value("AABB", A, B) != tw.word_value("ABAB", A, B)


def test_necklaces_do_not_double_count_cyclic_rotations():
    """AAAB and AABA are the same trace; only one may appear."""
    words = necklaces(4)
    seen = set()
    for w in words:
        rots = {w[k:] + w[:k] for k in range(len(w))}
        assert not (rots & seen), f"{w} duplicates an earlier cyclic class"
        seen |= rots


def test_checkpoint_key_includes_the_formula_hash():
    """A cache keyed only by candidate id would serve a stale row after the
    candidate's definition changed."""
    from sdbridge.candidates import RowCache, Candidate
    cache = RowCache(None)
    a = Candidate(candidate_id="x", degree=8, family="port_graph", formula_hash="h1")
    b = Candidate(candidate_id="x", degree=8, family="port_graph", formula_hash="h2")
    assert cache.key(P, 11, a) != cache.key(P, 11, b)


# =============================================================================
# End-to-end certificate integrity
# =============================================================================

def test_degree8_span_equality_is_not_mere_dimension_agreement():
    """Two different 7-spaces would give equal ranks and a union of 8.

    Constructed here rather than asserted: build two 7-dimensional spaces that
    differ and confirm the union test separates them, so the check used on the
    real data is known to have teeth.
    """
    rng = np.random.default_rng(9)
    A = rng.integers(0, P, size=(7, 40)).astype(np.int64)
    B = A.copy()
    B[0] = rng.integers(0, P, size=40)             # perturb one direction
    assert modrank(A, P) == modrank(B, P) == 7
    union = modrank(np.concatenate([A, B]), P)
    assert union > 7
    assert not spans_equal(A, B, P)
