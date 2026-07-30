"""Published degree-10 candidates from equation (4.24).

Source of record
----------------
Cederwall, Hutomo, Kuzenko, Lechner, Sorokin, "Some remarks on invariants",
J. Phys. A 59 (2026) 065203, doi:10.1088/1751-8121/ae3bb8, equation (4.24),
journal PDF page 17 (printed page 15). Cross-checked against
arXiv:2509.14350v2 PDF page 25.

Transcribed from a RENDERED image of the page, not from extracted text and not
from memory. The paper states that "the symmetrization and/or
anti-symmetrization of the indices within the red brackets is made upon the
anti-symmetrization within the black brackets"; that colour distinction is
invisible in the text stream, which is why the image was used.

Implementation status
---------------------
Only candidates whose index structure is unambiguous from the render are
implemented here. The remainder carry nested red/black bracket structures that
require a dedicated (anti)symmetrisation engine with the correct operation
ordering; they are deliberately NOT implemented rather than guessed.

    P10_01  tr M^5                                     IMPLEMENTED
    P10_02  (MM)M M N^(4125)                           IMPLEMENTED
    P10_03..P10_12                                     NOT IMPLEMENTED
"""

import numpy as np

from .modp import P, inv, mod_einsum
from .stress import (
    _raise_axes,
    composite_n4125,
    five_form_moment,
    matrix_trace_power,
)

SOURCE = {
    "paper": "Some remarks on invariants",
    "journal": "J. Phys. A 59 (2026) 065203",
    "doi": "10.1088/1751-8121/ae3bb8",
    "arxiv": "2509.14350v2",
    "equation": "(4.24)",
    "journal_pdf_page": 17,
    "arxiv_pdf_page": 25,
    "transcription_method": "rendered page image at 200 dpi",
}


def p10_01_trM5(five_form, mod=P, backend="optimized"):
    """I^(1)_10 = tr M^5."""
    _, mixed = five_form_moment(five_form, mod, backend)
    return int(matrix_trace_power(mixed, 5, mod) % mod)


def p10_02_mm_m_m_n4125(five_form, mod=P, backend="optimized"):
    """I^(2)_10 = (MM)_{mu1}^{nu1} M_{mu2}^{nu2} M_{mu3}^{nu3}
                  N^(4125)_{nu1 nu2 nu3}{}^{mu1 mu2 mu3}.

    composite_n4125 returns the all-lower 6-index tensor, so the last three
    indices are raised to match the source index placement.
    """
    _, mixed = five_form_moment(five_form, mod, backend)
    mm = (mixed @ mixed) % mod
    n = composite_n4125(five_form, mod, backend)
    n_raised = _raise_axes(n, (3, 4, 5), mod)
    # a=mu1 d=nu1, b=mu2 e=nu2, c=mu3 f=nu3 ; N indices (nu1,nu2,nu3,mu1,mu2,mu3)
    #
    # mod_einsum, NOT np.einsum. A bare int64 einsum over four operands with
    # entries up to p multiplies before summing: p^4 ~ 1.15e18 accumulated over
    # 10^6 terms wraps past 2^63 silently. That is the documented trap in this
    # repository's README and it was hit here first time; the homogeneity test
    # is what exposed it.
    out = mod_einsum("ad,be,cf,defabc->", [mm, mixed, mixed, n_raised], mod)
    return int(out % mod)


PUBLISHED_DEGREE10 = {
    "P10_01": {"source_label": "I^(1)_10", "formula": "tr M^5",
               "evaluator": p10_01_trM5, "implemented": True,
               "blocks": {"M": 5}},
    "P10_02": {"source_label": "I^(2)_10",
               "formula": "(MM)M M N^(4125)",
               "evaluator": p10_02_mm_m_m_n4125, "implemented": True,
               "blocks": {"M": 4, "N4125": 1}},
}

NOT_IMPLEMENTED = {
    f"P10_{i:02d}": "nested red/black bracket structure; needs an "
                    "(anti)symmetrisation engine with correct operation order"
    for i in range(3, 13)
}


def evaluate_implemented(five_form, mod=P, backend="optimized"):
    return {name: spec["evaluator"](five_form, mod, backend)
            for name, spec in PUBLISHED_DEGREE10.items()}
