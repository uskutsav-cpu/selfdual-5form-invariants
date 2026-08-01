"""The four selected `sd5_spinor_degree8_*` structured candidates, exact over F_p.

These are the remaining members of the selected 83 that are neither port graphs
nor tensor words.  They are built from two auxiliary tensors,

    Omega^{f g h i}   = I_{b c d e} F_{b f} F_{c g} F_{d h} F_{e i}      (degree 4)
    Theta_a{}^{f g h} = I_{a c d e} F_{c f} F_{d g} F_{e h}              (degree 3)

contracted back against the invariant tensor.  Each selected candidate is
homogeneous of degree 8 in F.

Derivatives are taken by exact modular interpolation rather than by the product
rule.  A degree-8 homogeneous polynomial restricted to a line, t -> I(F + tB),
is a degree-8 polynomial in t, so evaluating at nine distinct points and
interpolating recovers the linear coefficient --- which is the directional
derivative --- exactly.  No step size and no tolerance enter, and unlike a
hand-written product rule there is no per-candidate sign to get wrong.  The
result is checked against Euler homogeneity independently.
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import cached_property

import numpy as np

from . import conventions as C
from .modular import inv

try:
    import opt_einsum as _oe
except ImportError:  # pragma: no cover
    _oe = None

#: The four selected here; the other two of the family were not selected by the
#: archived run and are therefore not part of the scientific set.
SELECTED = ("sd5_spinor_degree8_2", "sd5_spinor_degree8_3",
            "sd5_spinor_degree8_4", "sd5_spinor_degree8_5")

DEGREE = 8


def _contract(spec: str, *ops, p: int) -> np.ndarray:
    """einsum mod p, reducing after EVERY pairwise step.

    Reducing only at the end silently overflows int64 and is the single easiest
    way to get a plausible-looking wrong answer here: with p ~ 2^15, a chain of
    four contractions reaches ~2^72 and wraps.  The first version of this file
    did exactly that, and it was caught by the homogeneity check below rather
    than by inspection -- which is why that check exists.

    Delegates to the same stepwise contractor the port-graph evaluator uses, so
    there is one implementation of this rule rather than two.
    """
    from .spinor_invariants import _modular_contract

    in_spec, _, out_spec = spec.partition("->")
    terms = in_spec.split(",")
    labels = {ch: i for i, ch in enumerate(sorted(set(in_spec.replace(",", ""))))}
    subs = [[labels[ch] for ch in term] for term in terms]
    out = [labels[ch] for ch in out_spec]
    result = _modular_contract([np.asarray(o, dtype=np.int64) % p for o in ops],
                               subs, p, output=out)
    return np.asarray(result) % p


@dataclass(frozen=True)
class StructuredDegree8:
    p: int = C.DEFAULT_PRIME

    @cached_property
    def I(self) -> np.ndarray:
        from .spinor_invariants import invariant_I
        return invariant_I(self.p)

    def omega(self, F: np.ndarray) -> np.ndarray:
        return _contract("bcde,bf,cg,dh,ei->fghi", self.I, F, F, F, F, p=self.p)

    def theta(self, F: np.ndarray) -> np.ndarray:
        return _contract("acde,cf,dg,eh->afgh", self.I, F, F, F, p=self.p)

    def values(self, F: np.ndarray) -> dict[str, int]:
        p = self.p
        F = np.asarray(F, dtype=np.int64) % p
        O = self.omega(F)
        T = self.theta(F)
        I = self.I
        Oa = (O - np.swapaxes(O, 1, 2)) % p
        Ia = (I - np.swapaxes(I, 1, 2)) % p
        out = {
            "sd5_spinor_degree8_1": _contract("abcd,efgh,abef,cdgh->", O, O, I, I, p=p),
            "sd5_spinor_degree8_2": _contract("abcd,efgh,abch,efgd->", O, O, I, I, p=p),
            "sd5_spinor_degree8_3": _contract("abcd,efgh,afgd,ebch->", Oa, Oa, Ia, Ia, p=p),
            "sd5_spinor_degree8_4": _contract("dxyz,duvw,pq,puyz,qxvw->", O, T, F, I, I, p=p),
            "sd5_spinor_degree8_5": _contract("dxyz,duvw,pq,pxyw,quvz->", O, T, F, I, I, p=p),
            "sd5_spinor_degree8_6": _contract("dxyz,duvw,pq,pxyu,qzvw->", O, T, F, I, I, p=p),
        }
        return {k: int(np.asarray(v).reshape(())) % p for k, v in out.items()}

    # -- exact directional derivative by interpolation -------------------------

    @cached_property
    def _linear_weights(self) -> tuple[list[int], list[int]]:
        """Lagrange weights extracting the t^1 coefficient from DEGREE+1 points.

        Nodes are t = 0, 1, ..., 8.  The weight on node j is the coefficient of
        t^1 in the j-th Lagrange basis polynomial, computed exactly over F_p.
        """
        p = self.p
        nodes = list(range(DEGREE + 1))
        weights = []
        for j, tj in enumerate(nodes):
            # basis poly L_j(t) = prod_{k != j} (t - t_k) / (t_j - t_k)
            coeffs = [1]                       # polynomial coefficients, low to high
            denom = 1
            for k, tk in enumerate(nodes):
                if k == j:
                    continue
                new = [0] * (len(coeffs) + 1)
                for i, c in enumerate(coeffs):
                    new[i] = (new[i] - c * tk) % p
                    new[i + 1] = (new[i + 1] + c) % p
                coeffs = new
                denom = denom * (tj - tk) % p
            weights.append(coeffs[1] * inv(denom, p) % p)
        return nodes, weights

    def directional_derivative(self, F: np.ndarray, B: np.ndarray,
                               names=SELECTED) -> dict[str, int]:
        """d/dt I(F + tB) at t = 0, exactly."""
        p = self.p
        nodes, weights = self._linear_weights
        F = np.asarray(F, dtype=np.int64) % p
        B = np.asarray(B, dtype=np.int64) % p
        acc = {n: 0 for n in names}
        for t, w in zip(nodes, weights):
            if w == 0:
                continue
            vals = self.values((F + t * B) % p)
            for n in names:
                acc[n] = (acc[n] + w * vals[n]) % p
        return acc

    def jacobian_rows(self, F: np.ndarray, basis: np.ndarray,
                      names=SELECTED) -> np.ndarray:
        """Rows = candidates in `names`, columns = basis directions."""
        p = self.p
        out = np.zeros((len(names), basis.shape[0]), dtype=np.int64)
        for r in range(basis.shape[0]):
            d = self.directional_derivative(F, basis[r], names)
            for i, n in enumerate(names):
                out[i, r] = d[n]
        return out % p

    def euler_check(self, F: np.ndarray, coeffs: np.ndarray,
                    basis: np.ndarray, names=SELECTED) -> dict:
        p = self.p
        rows = self.jacobian_rows(F, basis, names)
        vals = self.values(F)
        res = {}
        for i, n in enumerate(names):
            lhs = int(np.asarray(coeffs, dtype=np.int64) % p @ rows[i] % p)
            rhs = (DEGREE * vals[n]) % p
            res[n] = {"lhs": lhs, "rhs": rhs, "ok": lhs == rhs}
        return res
