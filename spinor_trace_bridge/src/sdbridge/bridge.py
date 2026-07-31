"""The five-form <-> spinor bridge, exact over F_p.

    S_{ab} = (1/5!) F_{mu1...mu5} (Gamma^{mu1...mu5})_{ab}

with F given in the trace side's Lorentzian orthonormal frame and Gamma built in
the spinor side's null frame; the frame transition is `signature.TransitionFrame`.

Because both antisymmetrisations are total, the 1/5! cancels against the sum over
orderings and the map is just the sum over sorted index tuples.  See
`conventions.FORWARD_NORMALISATION_DENOMINATOR`.

Nothing here is asserted.  `BridgeMap.verify()` establishes, at each prime:

  * the kernel is exactly the 126-dimensional anti-self-dual subspace;
  * the image is exactly the 126-dimensional gamma-traceless subspace;
  * the restriction to self-dual five-forms is an isomorphism onto that image;
  * the constructed left inverse reproduces the identity on the self-dual side.
"""

from __future__ import annotations

import itertools
from dataclasses import dataclass
from functools import cached_property

import numpy as np

from . import conventions as C
from .clifford import NullFrameClifford, symmetric_pairs
from .modular import matmul, rank, rref, nullspace, spans_equal
from .signature import TransitionFrame
from .traceside import forms as trace_forms


def sorted_five_index_tuples() -> list[tuple[int, ...]]:
    """The 252 sorted five-index tuples, in the trace side's own ordering."""
    return list(itertools.combinations(range(C.SPACETIME_DIM), C.FORM_DEGREE))


@dataclass(frozen=True)
class BridgeMap:
    """Forward map, left inverse and their certificates, at one prime."""

    p: int = C.DEFAULT_PRIME

    @cached_property
    def clifford(self) -> NullFrameClifford:
        return NullFrameClifford(p=self.p)

    @cached_property
    def frame(self) -> TransitionFrame:
        return TransitionFrame(p=self.p)

    # -- the forward map as an explicit 252 x 136 matrix ----------------------

    @cached_property
    def forward_matrix(self) -> np.ndarray:
        """Rows: the 252 Lorentzian five-form basis components.

        Columns: the 136 symmetric-spinor coordinates.  Row I is the image of
        the basis five-form whose only nonzero sorted component is I.
        """
        p = self.p
        tuples = sorted_five_index_tuples()
        g5 = self.clifford.gamma5
        out = np.zeros((len(tuples), C.N_SYMMETRIC_SPINOR), dtype=np.int64)
        pairs = symmetric_pairs()
        for r, I in enumerate(tuples):
            dense = trace_forms.to_dense(
                _unit_vector(len(tuples), r), C.SPACETIME_DIM, C.FORM_DEGREE, mod=p)
            null = self.frame.five_form_to_null(dense)
            S = np.zeros((C.SPINOR_DIM, C.SPINOR_DIM), dtype=np.int64)
            for J in tuples:
                coeff = int(null[J]) % p
                if coeff:
                    S = (S + coeff * g5[J]) % p
            out[r] = np.array([S[i, j] for (i, j) in pairs], dtype=np.int64) % p
        return out

    def forward(self, F_components: np.ndarray) -> np.ndarray:
        """Map a 252-vector of Lorentzian five-form components to 136 S-coordinates."""
        v = np.asarray(F_components, dtype=np.int64).reshape(-1) % self.p
        if v.shape[0] != C.N_FIVE_FORM_COMPONENTS:
            raise ValueError(f"expected {C.N_FIVE_FORM_COMPONENTS} components, got {v.shape[0]}")
        return matmul(v.reshape(1, -1), self.forward_matrix, self.p).reshape(-1)

    def traceside_dense(self, F_components: np.ndarray) -> np.ndarray:
        """Expand 252 sorted components into a dense antisymmetric (10,)*5 array."""
        return trace_forms.to_dense(
            np.asarray(F_components, dtype=np.int64) % self.p,
            C.SPACETIME_DIM, C.FORM_DEGREE, mod=self.p)

    def forward_matrix_form(self, F_components: np.ndarray) -> np.ndarray:
        """Same as `forward`, returned as a symmetric 16 x 16 matrix."""
        return self.clifford.coords_to_symmetric(self.forward(F_components))

    # -- self-dual / anti-self-dual, in the trace side's frozen convention ----

    @cached_property
    def selfdual_projector(self) -> np.ndarray:
        return trace_forms.selfdual_projector(
            C.SPACETIME_DIM, C.FORM_DEGREE, lorentzian=True, mod=self.p) % self.p

    @cached_property
    def antiselfdual_projector(self) -> np.ndarray:
        n = C.N_FIVE_FORM_COMPONENTS
        return (np.eye(n, dtype=np.int64) - self.selfdual_projector) % self.p

    @cached_property
    def selfdual_basis(self) -> np.ndarray:
        """126 x 252: a basis of the self-dual five-forms over F_p."""
        R, piv = rref(self.selfdual_projector, self.p)
        basis = R[:len(piv)]
        if basis.shape[0] != C.N_SELFDUAL_COMPONENTS:
            raise RuntimeError(f"self-dual subspace has dimension {basis.shape[0]}")
        return basis

    @cached_property
    def antiselfdual_basis(self) -> np.ndarray:
        R, piv = rref(self.antiselfdual_projector, self.p)
        basis = R[:len(piv)]
        if basis.shape[0] != C.N_SELFDUAL_COMPONENTS:
            raise RuntimeError(f"anti-self-dual subspace has dimension {basis.shape[0]}")
        return basis

    # -- the left inverse ----------------------------------------------------

    @cached_property
    def selfdual_image(self) -> np.ndarray:
        """126 x 136: images of the self-dual basis, a basis of the image."""
        return matmul(self.selfdual_basis, self.forward_matrix, self.p)

    @cached_property
    def left_inverse(self) -> np.ndarray:
        """136 x 252 matrix R with R applied to S returning the self-dual F.

        Built by inverting the 126 x 126 restriction and pushing back through the
        self-dual basis, so `left_inverse @ forward` is the self-dual projector.
        """
        from .clifford import _inverse_mod
        p = self.p
        # 126 columns of the image whose square submatrix is invertible
        _, sel = rref(self.selfdual_image, p)
        if len(sel) != C.N_SELFDUAL_COMPONENTS:
            raise RuntimeError(
                f"image has dimension {len(sel)}, not {C.N_SELFDUAL_COMPONENTS}; "
                "cannot build a left inverse")
        Minv = _inverse_mod(self.selfdual_image[:, sel], p)   # 126 x 126
        # S[sel] -> coefficients in the self-dual basis -> five-form components
        return (list(sel), matmul(Minv, self.selfdual_basis, p))

    def inverse(self, S_coords: np.ndarray) -> np.ndarray:
        """Recover the self-dual five-form whose image is S (252 components)."""
        sel, M = self.left_inverse
        v = np.asarray(S_coords, dtype=np.int64).reshape(-1) % self.p
        return matmul(v[sel].reshape(1, -1), M, self.p).reshape(-1)

    # -- certificates --------------------------------------------------------

    def verify(self) -> dict:
        p = self.p
        out: dict = {"prime": p}
        out["star_squared"] = trace_forms.check_star_squared(
            C.SPACETIME_DIM, C.FORM_DEGREE, lorentzian=True, mod=p)
        out["selfdual_dim"] = int(self.selfdual_basis.shape[0])
        out["antiselfdual_dim"] = int(self.antiselfdual_basis.shape[0])
        out["forward_rank"] = rank(self.forward_matrix, p)

        asd_image = matmul(self.antiselfdual_basis, self.forward_matrix, p)
        out["antiselfdual_maps_to_zero"] = bool(np.all(asd_image % p == 0))

        ker = nullspace(self.forward_matrix.T, p)  # left nullspace: rows killed
        out["kernel_dim"] = int(ker.shape[0])
        out["kernel_equals_antiselfdual"] = bool(
            spans_equal(ker, self.antiselfdual_basis, p))

        out["image_dim"] = rank(self.selfdual_image, p)
        out["image_equals_gamma_traceless"] = bool(
            spans_equal(self.selfdual_image, self.clifford.gamma_traceless_basis, p))

        # round trip on the self-dual side
        rng = np.random.default_rng(20260731)
        ok = True
        for _ in range(8):
            c = rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS)
            F = matmul(c.reshape(1, -1), self.selfdual_basis, p).reshape(-1)
            S = self.forward(F)
            back = self.inverse(S)
            if not np.array_equal(F % p, back % p):
                ok = False
        out["round_trip_selfdual"] = ok

        # scaling F -> cF
        c = 7
        F = matmul(
            rng.integers(0, p, size=C.N_SELFDUAL_COMPONENTS).reshape(1, -1),
            self.selfdual_basis, p).reshape(-1)
        out["scaling_linear"] = bool(np.array_equal(
            self.forward((c * F) % p), (c * self.forward(F)) % p))
        return out


def _unit_vector(n: int, k: int) -> np.ndarray:
    v = np.zeros(n, dtype=np.int64)
    v[k] = 1
    return v
