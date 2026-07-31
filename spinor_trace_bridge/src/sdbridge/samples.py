"""The common-sample registry: one set of five-forms both sides evaluate at.

Four families, deliberately not all generic:

  sparse      one or two nonzero sorted components, then self-dual-projected.
              These are the samples a human can check by hand.
  structured  supported on a small index block, so several invariants coincide
              or vanish; these are where a wrong bridge normalisation shows up.
  generic     uniformly random over F_p.  Used for basis fitting.
  holdout     generic, but drawn from a disjoint seed stream and never used to
              fit anything.  Every claimed change-of-basis map is validated here.

Every sample is stored as its 252 sorted Lorentzian components, hashed, and
checked for self-duality before use.
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, asdict

import numpy as np

from . import conventions as C
from .modular import matmul


@dataclass(frozen=True)
class Sample:
    sample_id: str
    family: str
    prime: int
    components: tuple[int, ...]
    sha256: str

    def as_array(self) -> np.ndarray:
        return np.array(self.components, dtype=np.int64)

    def to_json(self) -> dict:
        d = asdict(self)
        d["components"] = list(self.components)
        return d


def _hash_components(v: np.ndarray, p: int) -> str:
    payload = json.dumps({"prime": p, "components": [int(x) for x in v]},
                         sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()


def _make(sample_id: str, family: str, v: np.ndarray, p: int) -> Sample:
    v = np.asarray(v, dtype=np.int64) % p
    return Sample(sample_id=sample_id, family=family, prime=p,
                  components=tuple(int(x) for x in v),
                  sha256=_hash_components(v, p))


def build_registry(bridge, n_generic: int = 40, n_holdout: int = 20,
                   n_structured: int = 8, seed: int = 20260731) -> list[Sample]:
    """Construct the registry.  Every sample is self-dual by construction."""
    p = bridge.p
    P = bridge.selfdual_projector
    n = C.N_FIVE_FORM_COMPONENTS
    samples: list[Sample] = []

    def project(v: np.ndarray) -> np.ndarray:
        return matmul(np.asarray(v, dtype=np.int64).reshape(1, -1) % p, P.T, p).reshape(-1)

    # sparse: single and double unit components, projected
    for k in range(6):
        v = np.zeros(n, dtype=np.int64)
        v[k * 37 % n] = 1
        pv = project(v)
        if np.any(pv):
            samples.append(_make(f"sparse-{k:02d}", "sparse", pv, p))
    for k in range(4):
        v = np.zeros(n, dtype=np.int64)
        v[k] = 1
        v[(k + 91) % n] = p - 1
        pv = project(v)
        if np.any(pv):
            samples.append(_make(f"sparse-pair-{k:02d}", "sparse", pv, p))

    # structured: support confined to five-index tuples drawn from a small block
    from .bridge import sorted_five_index_tuples
    tuples = sorted_five_index_tuples()
    rng = np.random.default_rng(seed)
    for k in range(n_structured):
        block = sorted(rng.choice(C.SPACETIME_DIM, size=7, replace=False).tolist())
        v = np.zeros(n, dtype=np.int64)
        for i, t in enumerate(tuples):
            if set(t).issubset(block):
                v[i] = int(rng.integers(1, p))
        pv = project(v)
        if np.any(pv):
            samples.append(_make(f"structured-{k:02d}", "structured", pv, p))

    # generic: fitting stream
    grng = np.random.default_rng(seed + 1)
    for k in range(n_generic):
        pv = project(grng.integers(0, p, size=n))
        samples.append(_make(f"generic-{k:03d}", "generic", pv, p))

    # holdout: disjoint seed stream, never used for fitting
    hrng = np.random.default_rng(seed + 90210)
    for k in range(n_holdout):
        pv = project(hrng.integers(0, p, size=n))
        samples.append(_make(f"holdout-{k:03d}", "holdout", pv, p))

    return samples


def verify_selfduality(bridge, samples: list[Sample]) -> dict:
    """Every sample must satisfy *F = F exactly.  Reports, does not assume."""
    p = bridge.p
    from .traceside import forms as tforms
    H = tforms.hodge_matrix(C.SPACETIME_DIM, C.FORM_DEGREE, lorentzian=True, mod=p) % p
    failures = []
    for s in samples:
        v = s.as_array()
        star = matmul(H, v.reshape(-1, 1), p).reshape(-1)
        if not np.array_equal(star % p, v % p):
            failures.append(s.sample_id)
    return {"n_samples": len(samples), "all_selfdual": not failures,
            "failures": failures}


def registry_hash(samples: list[Sample]) -> str:
    payload = json.dumps([s.to_json() for s in samples], sort_keys=True).encode()
    return hashlib.sha256(payload).hexdigest()
