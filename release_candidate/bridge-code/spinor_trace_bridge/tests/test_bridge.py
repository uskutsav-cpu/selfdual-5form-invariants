"""Certificates for the spinor/tensor bridge.

Everything here is exact over F_p at both of the trace side's primes.  No test
in this file has a tolerance, because no computation in the bridge has one.
"""

from __future__ import annotations

import itertools

import numpy as np
import pytest

from sdbridge import conventions as C
from sdbridge.bridge import BridgeMap, sorted_five_index_tuples
from sdbridge.clifford import (
    NullFrameClifford,
    basis_masks,
    dirac_gammas,
    null_metric,
    null_metric_inverse,
)
from sdbridge.covariance import covariance_report
from sdbridge.modular import matmul, rank, spans_equal
from sdbridge.signature import TransitionFrame, lorentzian_metric

PRIMES = [C.DEFAULT_PRIME, C.ALT_PRIME]


@pytest.fixture(scope="module")
def bridges():
    return {p: BridgeMap(p=p) for p in PRIMES}


# --- Clifford algebra --------------------------------------------------------

def test_null_frame_signature_is_split():
    """The oscillator frame's real form is (5,5), NOT Euclidean (10,0).

    This is the fact that unblocks the whole comparison: in signature (5,5) the
    Hodge star squares to +1 on five-forms, exactly as in Lorentzian signature,
    so real self-dual five-forms exist on the spinor side too.
    """
    G = [g.astype(float) for g in dirac_gammas()]
    eta = np.zeros((10, 10))
    for a in range(10):
        for b in range(10):
            anti = G[a] @ G[b] + G[b] @ G[a]
            c = anti[0, 0]
            assert np.allclose(anti, c * np.eye(32)), "anticommutator is not a multiple of 1"
            eta[a, b] = c / C.CLIFFORD_NORMALISATION
    w = np.linalg.eigvalsh(eta)
    pos, neg = int((w > 1e-9).sum()), int((w < -1e-9).sum())
    assert (pos, neg) == C.NULL_FRAME_REAL_SIGNATURE == (5, 5)
    # *^2 = (-1)^{p(d-p)} sign(det eta) = (-1)^25 * (-1) = +1
    assert ((-1) ** 25) * int(np.sign(np.linalg.det(eta))) == C.STAR_SQUARED_ON_FIVE_FORMS


@pytest.mark.parametrize("p", PRIMES)
def test_clifford_relation_exact(p):
    report = NullFrameClifford(p=p).verify()
    assert report["sigma_symmetric"]
    assert report["sigma_bar_symmetric"]
    assert report["clifford_relation"]


@pytest.mark.parametrize("p", PRIMES)
def test_chirality_split_is_sixteen_plus_sixteen(p):
    assert len(basis_masks(0)) == C.SPINOR_DIM
    assert len(basis_masks(1)) == C.SPINOR_DIM
    assert len(basis_masks(0)) + len(basis_masks(1)) == C.FULL_SPINOR_DIM


@pytest.mark.parametrize("p", PRIMES)
def test_gamma_trace_constraints_have_rank_ten(p):
    cl = NullFrameClifford(p=p)
    assert rank(cl.gamma_trace_constraints, p) == C.SPACETIME_DIM


@pytest.mark.parametrize("p", PRIMES)
def test_gamma_traceless_module_is_126(p):
    assert NullFrameClifford(p=p).gamma_traceless_basis.shape[0] == C.N_GAMMA_TRACELESS
    assert C.N_SYMMETRIC_SPINOR - C.SPACETIME_DIM == C.N_GAMMA_TRACELESS


@pytest.mark.parametrize("p", PRIMES)
def test_null_metric_is_its_own_stated_inverse(p):
    assert np.array_equal(
        matmul(null_metric(p), null_metric_inverse(p), p),
        np.eye(C.SPACETIME_DIM, dtype=np.int64))


@pytest.mark.parametrize("p", PRIMES)
def test_five_gamma_is_symmetric_in_spinor_indices(p):
    g5 = NullFrameClifford(p=p).gamma5
    for idx in list(g5)[:25]:
        assert np.array_equal(g5[idx], g5[idx].T % p)


# --- frame transition --------------------------------------------------------

@pytest.mark.parametrize("p", PRIMES)
def test_transition_is_an_exact_congruence(p):
    report = TransitionFrame(p=p).verify()
    assert report["congruence_exact"]
    assert report["L_invertible"]


@pytest.mark.parametrize("p", PRIMES)
def test_the_two_metrics_share_a_discriminant_class(p):
    """Congruence over F_p is possible precisely because of this."""
    from sdbridge.modular import is_square, inv
    dL = int(round(np.linalg.det(np.diag(np.array(C.LORENTZIAN_SIGNS, float)))))
    assert dL == -1
    # det eta_null = -2^{-10}; the ratio to -1 is a square, namely (2^{-5})^2
    ratio = inv(pow(2, 10, p), p) % p
    assert is_square(ratio, p)


@pytest.mark.parametrize("p", PRIMES)
def test_five_form_frame_round_trip(p):
    tf = TransitionFrame(p=p)
    rng = np.random.default_rng(11)
    tuples = sorted_five_index_tuples()
    from sdbridge.traceside import forms as tforms
    v = rng.integers(0, p, size=len(tuples))
    dense = tforms.to_dense(v, C.SPACETIME_DIM, C.FORM_DEGREE, mod=p)
    back = tf.five_form_to_lorentzian(tf.five_form_to_null(dense))
    assert np.array_equal(dense % p, back % p)


# --- self-duality ------------------------------------------------------------

@pytest.mark.parametrize("p", PRIMES)
def test_star_squares_to_plus_one_on_five_forms(p, bridges):
    from sdbridge.traceside import forms as tforms
    assert tforms.check_star_squared(10, 5, lorentzian=True, mod=p) == \
        C.STAR_SQUARED_ON_FIVE_FORMS


@pytest.mark.parametrize("p", PRIMES)
def test_selfdual_and_antiselfdual_each_have_dimension_126(p, bridges):
    b = bridges[p]
    assert b.selfdual_basis.shape[0] == C.N_SELFDUAL_COMPONENTS
    assert b.antiselfdual_basis.shape[0] == C.N_SELFDUAL_COMPONENTS
    assert 2 * C.N_SELFDUAL_COMPONENTS == C.N_FIVE_FORM_COMPONENTS


# --- the forward map ---------------------------------------------------------

@pytest.mark.parametrize("p", PRIMES)
def test_forward_kernel_is_exactly_antiselfdual(p, bridges):
    b = bridges[p]
    r = b.verify()
    assert r["antiselfdual_maps_to_zero"]
    assert r["kernel_dim"] == C.N_SELFDUAL_COMPONENTS
    assert r["kernel_equals_antiselfdual"], \
        "kernel has the right dimension but is not the anti-self-dual subspace"


@pytest.mark.parametrize("p", PRIMES)
def test_image_is_exactly_the_gamma_traceless_126(p, bridges):
    b = bridges[p]
    r = b.verify()
    assert r["image_dim"] == C.N_GAMMA_TRACELESS
    assert r["image_equals_gamma_traceless"], \
        "image has the right dimension but is not the gamma-traceless subspace"


@pytest.mark.parametrize("p", PRIMES)
def test_forward_rank_is_126_not_136(p, bridges):
    assert rank(bridges[p].forward_matrix, p) == C.N_GAMMA_TRACELESS


@pytest.mark.parametrize("p", PRIMES)
def test_gamma_trace_of_every_image_vanishes(p, bridges):
    b = bridges[p]
    cl = b.clifford
    rng = np.random.default_rng(5)
    for _ in range(5):
        c = rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS)
        F = matmul(c.reshape(1, -1), b.selfdual_basis, p).reshape(-1)
        S = b.forward(F)
        traces = matmul(cl.gamma_trace_constraints, S.reshape(-1, 1), p)
        assert np.all(traces % p == 0)


@pytest.mark.parametrize("p", PRIMES)
def test_sparse_hand_checkable_five_form(p, bridges):
    """A single-component five-form: its self-dual part must survive, and the
    anti-self-dual part of the same component must be annihilated."""
    b = bridges[p]
    v = np.zeros(C.N_FIVE_FORM_COMPONENTS, dtype=np.int64)
    v[0] = 1
    sd = matmul(v.reshape(1, -1), b.selfdual_projector.T, p).reshape(-1)
    asd = (v - sd) % p
    assert not np.all(b.forward(sd) % p == 0)
    assert np.all(b.forward(asd) % p == 0)


# --- inverse -----------------------------------------------------------------

@pytest.mark.parametrize("p", PRIMES)
def test_left_inverse_round_trips_on_selfdual_forms(p, bridges):
    assert bridges[p].verify()["round_trip_selfdual"]


@pytest.mark.parametrize("p", PRIMES)
def test_inverse_recovers_only_the_selfdual_part(p, bridges):
    """forward then inverse is the self-dual projector, not the identity."""
    b = bridges[p]
    rng = np.random.default_rng(3)
    for _ in range(4):
        v = rng.integers(0, p, size=C.N_FIVE_FORM_COMPONENTS)
        sd = matmul(v.reshape(1, -1), b.selfdual_projector.T, p).reshape(-1)
        assert np.array_equal(b.inverse(b.forward(v)) % p, sd % p)


# --- scaling and covariance --------------------------------------------------

@pytest.mark.parametrize("p", PRIMES)
def test_forward_is_linear_under_scaling(p, bridges):
    assert bridges[p].verify()["scaling_linear"]


@pytest.mark.parametrize("p", PRIMES)
def test_gl5_equivariance_with_determinant_character(p, bridges):
    report = covariance_report(bridges[p], n_group=2, n_samples=2, seed=99)
    assert report["equivariant_up_to_character"]
    for element in report["elements"]:
        assert element["chi_is_single_valued"]
        assert element["chi_equals_det"], \
            f"character {element['chi']} is not det(A) = {element['det_A']}"


# --- conventions are actually pinned ----------------------------------------

def test_conventions_match_the_frozen_trace_side():
    from sdbridge.traceside import forms as tforms, modp
    assert tuple(tforms.metric_signs(10, lorentzian=True)) == C.LORENTZIAN_SIGNS
    assert modp.P == C.DEFAULT_PRIME
    assert modp.ALT_P == C.ALT_PRIME


def test_there_are_252_five_form_components_and_136_symmetric_coordinates():
    assert len(sorted_five_index_tuples()) == C.N_FIVE_FORM_COMPONENTS
    assert len(list(itertools.combinations_with_replacement(range(16), 2))) == \
        C.N_SYMMETRIC_SPINOR


# --- full rotation-group equivariance ---------------------------------------

@pytest.mark.parametrize("p", PRIMES)
@pytest.mark.parametrize("n_reflections", [2, 4])
def test_equivariant_under_the_full_rotation_group(p, bridges, n_reflections):
    """Reflections generate the whole orthogonal group, so this closes the 20
    directions of so(10) that the GL(5) test does not reach."""
    from sdbridge.rotations import rotation_report
    report = rotation_report(bridges[p], n_elements=2, n_samples=2,
                             n_reflections=n_reflections, seed=41)
    assert report["equivariant_on_every_component"]
    for element in report["elements"]:
        assert element["scalar_single_valued"]
        assert element["scalar_matches_clifford_normalisation"], \
            "character is single-valued but is not the Clifford normalisation"


@pytest.mark.parametrize("p", PRIMES)
def test_reflection_in_a_null_vector_is_refused(p):
    from sdbridge.rotations import reflection_matrix
    with pytest.raises(ValueError):
        reflection_matrix(np.zeros(10, dtype=np.int64), p)
