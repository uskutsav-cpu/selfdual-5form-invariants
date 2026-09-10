from pathlib import Path
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parents[1] / 'repair-checkout'
CHANGES = []

def save(path, before, after):
    if before == after:
        return
    path.write_text(after)
    CHANGES.append({'path': str(path.relative_to(ROOT)),
                    'before_sha256': hashlib.sha256(before.encode()).hexdigest(),
                    'after_sha256': hashlib.sha256(after.encode()).hexdigest()})

def replace(text, before, after):
    assert before in text, before[:150]
    return text.replace(before, after)

p = ROOT / 'paper/manuscript.tex'
before = s = p.read_text()
s = replace(s, r'An explicit graph basis and exact Jacobian certificates', r'Explicit graph invariants and exact Jacobian certificates')
s = replace(s, '''characteristic-zero independence witness. The construction completes the
functional-independence problem, with the known generic quotient dimension
as upper bound. It does not determine all polynomial generators or syzygies.''', '''characteristic-zero independence witness when its entries are verified as
derivatives of the specified contractions. Together with the generic quotient
dimension from the literature, this gives a maximal generically independent
family. It does not determine all polynomial generators or syzygies.''')
s = replace(s, '''here re-evaluates those functions at new points.
''', '''here re-evaluates those functions at new points.
Graph enumeration and tensor-network contraction followed by numerical linear
algebra are established methods for tensor invariants: see
Elamaran, Ferko and Scarlett \\cite{elamaran}, whose six-dimensional three-form
study leaves the ten-dimensional chiral five-form application for future work.
We make no claim of priority for this method or for an 81-invariant family.
''')
s = replace(s, '''Disconnected contractions are products. The quadratic contraction vanishes
on this self-dual space.''', '''Disconnected contractions are products. The quadratic contraction vanishes
on this self-dual space: $F\\wedge\\star F=F\\wedge F=0$, since $F$ has odd
degree, so its metric norm vanishes. Complete contraction with the invariant
metric proves Lorentz invariance of each graph polynomial.''')
s = replace(s, '''The remaining two degree-twelve primitive polynomial directions belong to
the larger homogeneous inventory and are not included in the 81-function
Jacobian.''', '''The inherited inventory labels two further degree-twelve directions as
primitive polynomial directions; they are not included in the 81-function
Jacobian. That label requires the separate homogeneous-space evidence below.''')
s = replace(s, '''If a saved determinant is nonzero modulo $p$, the corresponding integer
determinant polynomial is not identically zero. Its nonvanishing defines a
nonempty Zariski-open set in characteristic zero on which these 81
polynomials are algebraically independent. Invariance and the known generic
quotient dimension supply the matching upper bound. These are generic local
coordinates; neither global orbit separation nor polynomial generation of
the entire ring follows.''', '''Suppose the recorded entries have been verified as the Jacobian of the
specified integral graph polynomials at the recorded point. A nonzero minor
modulo $p$ then proves that the corresponding integer determinant polynomial
is not identically zero. In characteristic zero the Jacobian criterion gives
algebraic independence of these 81 polynomials, and their differentials are
independent on the nonempty Zariski-open locus where that minor is nonzero.
Invariance and the cited generic quotient dimension supply the matching upper
bound. On a regular local quotient this gives local coordinates. It proves
neither global orbit separation, generation of the invariant field by rational
functions in this list, nor polynomial generation of the entire ring.''')
s = replace(s, '''The homogeneous-space dimensions through degree twelve are
$1,2,7,14,72$.''', '''The homogeneous-space dimensions reported in equation (4.2) of
\\cite{cederwall} through degree twelve are $1,2,7,14,72$.
These representation-theoretic counts are an external input here.''')
s = replace(s, '''directions. Polynomial-space evidence uses gradients concatenated at several
points; the functional Jacobian uses one point. These are separate sieves.''', '''directions. A rank-72 concatenated evaluation proves independence of that
homogeneous list only after the evaluated polynomial rows are verified; the
matching Hilbert coefficient supplies completeness. This inherited computation
is separate from the 81-function certificate. Polynomial-space evidence uses
gradients concatenated at several points; the functional Jacobian uses one
point. These are separate sieves. The prose of section 4.1.4 of
\\cite{cederwall} says 64 new degree-twelve directions, inconsistent with its
equation (4.2), which has exponent 62. The inventory here uses the latter;
we do not treat the inconsistent prose as an additional verified count.''')
s = replace(s, '''\\cite{cederwall}, together with the hatted expression (4.18). The exact
machine-readable map includes the quartic-square product explicitly.''', '''\\cite{cederwall}, together with the hatted expression (4.18). The
machine-readable matrix has exact reconstructed rational entries and includes
the quartic-square product explicitly. Its interpretation as a polynomial
change of basis is supported by modular fits and fresh value holdouts;
these finite checks are not a proof of every proposed polynomial identity.''')
s = replace(s, '''At degree ten the repository's implemented readings of the twelve published
candidates span a twelve-dimensional space whose intersection with the
two-dimensional product space has dimension one in the reconstructed
coordinate matrix. Thus a claimed invertible $12\\times12$ identification
with the graph primitive complement would be incorrect for those readings.
The delivered map has twelve rows and fourteen atlas columns and records
the source-reading qualifications. Rational reconstruction and fresh modular
holdouts are strong checks on these maps, but finite samples alone do not
prove a characteristic-zero polynomial identity. These qualifications do not
affect the graph-only nonzero-minor proof.''', '''The archived degree-ten map concerns the repository's implemented readings,
whose reconstructed $12\\times14$ coordinate matrix has rank twelve and
intersection dimension one with the two-dimensional product subspace.
A source audit found that the antisymmetrizers in the archived implementations
of candidates $J_{10}$--$J_{12}$ differ from the primary PDF and TeX source.
Consequently these matrix ranks cannot be attributed to the twelve published
expressions. Any repaired source map must be identified by its own formula
registry and fresh evaluation artifacts; the archived atlas is not silently
reinterpreted as that map. The archived degree-ten regeneration reads stored
per-prime coordinates and checks rational reconstruction against a held-out
stored prime; it performs no fresh tensor evaluations. Even fresh finite
holdouts would not by themselves prove characteristic-zero polynomial
identities. This source-transcription failure concerns the literature map;
the graph-only nonzero-minor argument has separate inputs.''')
s = replace(s, '''\\texttt{--recompute} mode repeats the graph evaluations. These modes are
reported separately.''', '''\\texttt{--recompute} mode repeats the graph evaluations with the production
evaluator. This recomputation does not by itself constitute an independent
implementation of the derivative. These modes are reported separately.''')
s = replace(s, '''and genuine Lorentz boosts. The final graph selection is checked under both
a spatial rotation and a boost; neither uses floating-point tolerances.''', '''and genuine Lorentz boosts. The final graph selection is checked under both
a spatial rotation and a boost at the recorded finite-field point; neither uses
floating-point tolerances. These are implementation checks at specified inputs,
while invariance itself follows from the complete-contraction definition.''')
s = replace(s, r'\end{thebibliography}', '''\\bibitem{elamaran} A. Elamaran, C. Ferko and S. Scarlett,
\\emph{Machine Learning Invariants of Tensors}, Phys. Rev. D 114 (2026) 026016,
\\href{https://doi.org/10.1103/ny3m-drnj}{doi:10.1103/ny3m-drnj},
\\href{https://arxiv.org/abs/2512.23750}{arXiv:2512.23750}.
\\end{thebibliography}''')
save(p, before, s)

# Older drafts retain their numerical artifacts as archived results. A visible
# scope statement prevents them from being read as newly audited publications.
status = r'''
\paragraph{Audit scope and inherited results.}
This draft retains numerical tables and identities from the archived computation;
it is not an overall audit-pass statement. In this draft, $B_{10}$ and any
``published span'' computed from that archive refer only to the implemented
source readings. A source audit found that the archived antisymmetrizers of
$J_{10}$--$J_{12}$ differ from the primary PDF and TeX source. No conclusion
about the span of the published expressions follows from that archived map.
Repaired formulas require a separately identified registry and fresh map.
Exact rational arithmetic proves statements about reconstructed coordinate
matrices; their interpretation as polynomial maps, flow closure, or identities
requires the corresponding polynomial identities and activation rules to be
valid. Modular fits and finite holdouts are evidence for those inputs, not a
proof of them. Accordingly, the numerical flow and intersection statements
below are statements about the archived coordinate model, conditional as
statements about invariant-polynomial spaces. Finite common-sample comparisons
establish equality of evaluation spans, with polynomial span equality subject
to the same qualification. The graph Jacobian nonzero-minor argument is
separate: verified derivatives of integral graph polynomials give a
characteristic-zero rank lower bound. No priority claim is made.
'''

abstract = r'''We record the archived degree-ten invariant atlas for the self-dual
five-form in ten dimensions, its reconstructed rational coordinate matrices,
and an exact modular Jacobian witness for generic functional rank at least
eighty-one. The matching generic upper bound is inherited from the literature.
The archived atlas, stress-flow closure and quotient have reported dimensions
fourteen, eleven and three. Their interpretation as polynomial-space results
requires valid polynomial coordinate maps and flow activation rules; finite
modular fits and holdouts alone do not prove these inputs. The archived
literature map also uses source readings whose final three antisymmetrizers
differ from the primary source, so its reported product intersection cannot
be assigned to the published expressions. The graph Jacobian certificate uses
separate contractions. The body retains the legacy numerical evidence with
these qualifications; it does not claim a completed audit or priority.
'''

files = ['manuscript/main.tex','submission_candidate/main.tex',
         'manuscript/jhep/main.tex','manuscript/prd/main.tex',
         'manuscript/prd_letter/main.tex','manuscript/prl/main.tex']
for f in files:
    p=ROOT/f
    before=s=p.read_text()
    if r'\abstract{%' in s:
        s=re.sub(r'\\abstract\{%.*?\n\}', lambda m:'\\abstract{%\n'+abstract+'}', s, count=1, flags=re.S)
    else:
        s=re.sub(r'\\begin\{abstract\}.*?\\end\{abstract\}',lambda m:'\\begin{abstract}\n'+abstract+'\\end{abstract}',s,count=1,flags=re.S)
    s=replace(s, r'\maketitle', '\\maketitle\n'+status)
    s=s.replace('An exact degree-ten classification of local invariants of the', 'An archived degree-ten atlas of local invariants of the')
    s=s.replace('Exact degree-ten invariants of a self-dual five-form', 'An archived degree-ten atlas of a self-dual five-form')
    s=s.replace(r'Three local interactions of the ten-dimensional self-dual five-form\\'+ '\n'+ '       that no stress-tensor flow generates', r'An archived stress-flow quotient for the self-dual five-form')
    s=s.replace('The science below is complete and certified; the venue judgement is not.', 'The scientific claims below have the audit qualifications stated above.')
    # Direct logical and normalization corrections, independent of computed ranks.
    s=s.replace('A count of generators, not of functions.', 'A count of homogeneous invariant polynomials, including products; it is not by itself a count of minimal generators.')
    s=s.replace('so exactly two functional relations hold among functions that\nare pairwise distinct as polynomials. Both are degree-twelve phenomena:', 'so there are two excess candidate directions at the generic differential level;\nno two explicit polynomial relations are identified by that rank statement.\nThe excess appears at degree twelve:')
    s=s.replace(r'T^\mu{}_\mu=(1-cd)\,\langle F,F\rangle,',r'T^\mu{}_\mu=\bigl(1/(p-1)!-cd\bigr)\,\langle F,F\rangle,')
    s=s.replace('trace, so $\\operatorname{Tr}(\\tau)$ first contributes at field degree four.', 'trace. In an even-degree interaction expansion, the trace can first\ncontribute at degree four; nonvanishing at that degree is a separate input.')
    s=s.replace('for every improvement coefficient. Hence $\\operatorname{Tr}\\tau$ first\ncontributes at field degree four.', 'for every coefficient of the displayed metric-norm term. In an even-degree\ninteraction expansion, $\\operatorname{Tr}\\tau$ can first contribute at field\ndegree four; the argument does not establish a nonzero quartic term.')
    if f in ('manuscript/jhep/main.tex','manuscript/prd/main.tex'):
        s=s.replace(r'\begin{theorem}[Exact degree-ten reachability]'+'\n'+r'\label{thm:reach}'+'\nOver the rationals,',r'\begin{theorem}[Conditional interpretation of the archived closure]'+'\n'+r'\label{thm:reach}'+'\nAssume the archived coordinate maps are polynomial identities and the\nrecorded target list and activation rules describe the stated flow completely.\nThen its exact rational fixed point gives')
        s=s.replace(r'\label{thm:bp}'+'\n'+r'$\dim_\Q',r'\label{thm:bp}'+'\nFor the archived reconstructed coordinate matrices (not the corrected\npublished expressions),\n'+r'$\dim_\Q')
    if f=='manuscript/prd_letter/main.tex':
        s=s.replace(r'\label{thm:main}'+'\nOver the rationals,',r'\label{thm:main}'+'\nAssuming valid polynomial coordinate maps, a complete target list, and the\nrecorded activation rules, the archived rational coordinate model gives')
    save(p,before,s)

(Path(__file__).parent/'manuscript-changes.json').write_text(json.dumps(CHANGES,indent=2)+'\n')
print(json.dumps(CHANGES,indent=2))
