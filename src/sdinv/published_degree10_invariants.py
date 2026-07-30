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
    composite_n1050,
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


def p10_03_m3_n1050_n1050(five_form, mod=P, backend="optimized"):
    """I^(3)_10 = M_{mu1}^{nu1} M_{mu2}^{nu2} M_{mu3}^{nu3}
                  ( N_(1050)^{[mu1mu2mu3,a1a2]a3} N^(1050)_{[nu1nu2nu3,a1a2]a3} )

    All brackets in this candidate are BLACK, and `composite_n1050` already
    performs the five-index antisymmetrisation [abc,de], so no additional
    bracket program is required. Verified against the rendered source at
    400 dpi (journal p17).
    """
    _, mixed = five_form_moment(five_form, mod, backend)
    n_low = composite_n1050(five_form, mod, backend)
    n_up = _raise_axes(n_low, (0, 1, 2, 3, 4, 5), mod)
    # a=mu1 d=nu1, b=mu2 e=nu2, c=mu3 f=nu3, xyz = a1 a2 a3
    return int(mod_einsum(
        "ad,be,cf,abcxyz,defxyz->",
        [mixed, mixed, mixed, n_up, n_low], mod) % mod)


def p10_06_mm_m_n1050_n4125(five_form, mod=P, backend="optimized"):
    """I^(6)_10 = (MM)_{nu1}^{mu1} M_{nu2}^{mu2}
                  N^(1050)_{[mu1mu2rho1,rho2rho3]rho4}
                  N_(4125)^{rho1rho2rho3,rho4nu1nu2}

    Black brackets only; the five-index antisymmetrisation is already carried
    by composite_n1050. Verified against the 400 dpi render, journal p17.
    """
    _, mixed = five_form_moment(five_form, mod, backend)
    mm = (mixed @ mixed) % mod
    n1050 = composite_n1050(five_form, mod, backend)
    n4125 = composite_n4125(five_form, mod, backend)
    n4125_up = _raise_axes(n4125, (0, 1, 2, 3, 4, 5), mod)
    # (MM)_{nu1}^{mu1} -> [n1, m1];  N1050_{m1 m2 r1 r2 r3 r4}
    # N4125^{r1 r2 r3 r4 n1 n2}
    return int(mod_einsum(
        "am,bn,mnpqrs,pqrsab->",
        [mm, mixed, n1050, n4125_up], mod) % mod)


def p10_07_n1050_mm_n1050_n1050(five_form, mod=P, backend="optimized"):
    """I^(7)_10 = N^(1050)_{[rho1rho2rho3,rho4rho5]mu} (MM)^{mu}{}_{kappa}
                  ( N_(1050)^{[rho1rho2rho3,}{}_{a1a2]a3}
                    N_(1050)^{[rho4rho5kappa,a1a3]a2} )

    Black brackets only. Note the alpha ordering differs between the two inner
    N factors -- a1a2]a3 against a1a3]a2 -- which is carried by the einsum
    labels, not by any additional symmetrisation.
    """
    _, mixed = five_form_moment(five_form, mod, backend)
    mm = (mixed @ mixed) % mod
    n_low = composite_n1050(five_form, mod, backend)
    n_up = _raise_axes(n_low, (0, 1, 2, 3, 4, 5), mod)
    # N_{r1 r2 r3 r4 r5 mu} (MM)^{mu}{}_{k} N^{r1 r2 r3 a1 a2 a3}
    #                                        N^{r4 r5 k  a1 a3 a2}
    return int(mod_einsum(
        "pqrstm,mk,pqrxyz,stkxzy->",
        [n_low, mm, n_up, n_up], mod) % mod)


PUBLISHED_DEGREE10 = {
    "P10_01": {"source_label": "I^(1)_10", "formula": "tr M^5",
               "evaluator": p10_01_trM5, "implemented": True,
               "blocks": {"M": 5}},
    "P10_02": {"source_label": "I^(2)_10",
               "formula": "(MM)M M N^(4125)",
               "evaluator": p10_02_mm_m_m_n4125, "implemented": True,
               "blocks": {"M": 4, "N4125": 1}},
    "P10_03": {"source_label": "I^(3)_10",
               "formula": "M M M (N^(1050) N^(1050))",
               "evaluator": p10_03_m3_n1050_n1050, "implemented": True,
               "blocks": {"M": 3, "N1050": 2},
               "brackets": "black only; supplied by composite_n1050"},
    "P10_06": {"source_label": "I^(6)_10",
               "formula": "(MM) M N^(1050) N^(4125)",
               "evaluator": p10_06_mm_m_n1050_n4125, "implemented": True,
               "blocks": {"M": 3, "N1050": 1, "N4125": 1},
               "brackets": "black only"},
    "P10_07": {"source_label": "I^(7)_10",
               "formula": "N^(1050) (MM) (N^(1050) N^(1050))",
               "evaluator": p10_07_n1050_mm_n1050_n1050, "implemented": True,
               "blocks": {"M": 2, "N1050": 3},
               "brackets": "black only"},
}

NOT_IMPLEMENTED = {
    f"P10_{i:02d}": "nested red/black bracket structure; needs an "
                    "(anti)symmetrisation engine with correct operation order"
    for i in [4, 5, 8, 9, 10, 11, 12]
}

# Read off the 400 dpi render of eq (4.24), journal p17: which candidates
# carry RED brackets (and therefore need staged execution) and which are
# black-only (and therefore need only composite_n1050 / composite_n4125).
BRACKET_STAGES = {
    "P10_03": "black only", "P10_04": "RED present: (mu ... rho]lambda)",
    "P10_05": "black only", "P10_06": "black only",
    "P10_07": "black only", "P10_08": "black only",
    "P10_09": "RED present: (nu ... rho]lambda)",
    "P10_10": "black only (nested)", "P10_11": "black only (nested)",
    "P10_12": "black only (nested)",
}


def evaluate_implemented(five_form, mod=P, backend="optimized"):
    return {name: spec["evaluator"](five_form, mod, backend)
            for name, spec in PUBLISHED_DEGREE10.items()}
