from pathlib import Path
import hashlib, json

ROOT=Path(__file__).resolve().parents[1]/'repair-checkout'
changes=[]

def edit(f, pairs):
    p=ROOT/f
    before=s=p.read_text()
    for a,b in pairs:
        if a not in s:
            raise ValueError(f+' missing '+a[:100])
        s=s.replace(a,b)
    p.write_text(s)
    changes.append({'path':f,'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest()})

conditional_closure='''The rational fixed point is an equality for the recorded coordinate model.
Its interpretation as the polynomial reachable space requires that all
reconstructed target maps are polynomial identities and that the target list
and activation rules are complete for the stated flow. Held-out prime checks
do not establish these hypotheses. The minor proves the rank of the recorded
coordinate matrix; it does not supply the missing polynomial identities.'''

legacy_pairs=[
('Its internal structure is determined completely','Its archived coordinate structure is determined'),
('intersections and sums are certified.','intersections and sums refer to the archived coordinate model.'),
('over $\\mathbb{Q}$ (sections~\\ref{sec:czero} and~\\ref{sec:decomp}).','over $\\mathbb{Q}$ for the reconstructed coordinate matrices\n      (sections~\\ref{sec:czero} and~\\ref{sec:decomp}); their polynomial\n      interpretation has the audit hypotheses stated above.'),
('''This is exact over the rationals, not only modulo a prime: the published
coordinates were lifted''','''The following is exact for the reconstructed rational coordinate matrices,
not a proved identity of the published polynomials: the archived coordinates were lifted'''),
('''so a specific integer combination of four of the twelve published structures is
a multiple of a pure product.''','''so the reconstructed matrix proposes an integer polynomial identity for four
of the archived implemented structures and a pure product.'''),
('''Running the same fixed point in exact rational arithmetic removes the modular
admission test, and with it the gap.''','''Running the same fixed point in exact rational arithmetic removes the modular
admission test for the reconstructed coordinate model. It does not prove that
the reconstructed coordinates represent the intended polynomials.'''),
('''This is an equality and not a bound, because at a fixed point reached over
$\\mathbb{Q}$ no generated direction raises the rank over $\\mathbb{Q}$: the
reached span \\emph{is} $D_{10}$. No separate upper-bound argument is needed --- the
upper bound was an artefact of computing in $\\mathbb{F}_p$. As an independently''',conditional_closure+' As an independently'),
('''Where the spans agree, the agreement is established by two-way containment and
the change-of-basis matrix is fitted on the fitting samples only and then
validated on the holdout samples.''','''Where the evaluation spans agree, finite-sample two-way containment is
established and the change-of-basis matrix is fitted on the fitting samples
only and then validated on holdouts. Polynomial span equality requires an
additional identity argument beyond those samples.'''),
('''This is not an inference. Running the spinor enumeration''','''Within the enumerated candidate family, running the spinor enumeration'''),
('''they locate the missing direction precisely: it is not reachable by any
single-graph contraction.''','''they locate a direction missing from the enumerated port-graph family.
Extending that conclusion to every possible contraction requires proof that
the enumeration and ansatz exhaust the stated class.'''),
('''what makes this span equality rather than dimension agreement.''','''what establishes equality of the sampled evaluation spans. It does not by
itself prove the fitted identities as polynomials.'''),
('''direction that a port-graph-only family misses is not reachable by any
single-graph contraction of the invariant tensor, and the structured family does
not supply it either. That is a positive statement about where the invariant
lives, not merely an observation that two counts differ.''','''direction missed by the enumerated port-graph-only family is not supplied
by the enumerated structured family on those samples either. Exhaustiveness
of the candidate classes is a separate requirement for a universal statement.'''),
('''This changes what a theorist can do in a specific way. Previously, a candidate
degree-ten term could be compared against the published structures only, and if
it failed to match, nothing followed --- the published list was not known to be
complete or independent. Now any degree-ten invariant can be expanded in a
certified basis, its coefficients read off exactly, and its class in $Q_{10}$
computed. That is the difference between recognising a term and locating it.''','''The atlas provides explicit candidate coordinates for comparing degree-ten
terms. Identifying a fitted coordinate vector with a polynomial identity and
interpreting its class in $Q_{10}$ requires the coordinate and closure
hypotheses stated above. The source-transcription failure prevents using the
archived literature map as a classification of the published expressions.'''),
('''The degree-ten graded piece of the invariant ring of the ten-dimensional
self-dual five-form is now known exactly, together with its product, published,
graph-generator and stress-flow-reachable subspaces and all their intersections.
Every one of those dimensions is exact over $\\mathbb{Q}$, not merely modulo a
prime:''','''The archived degree-ten coordinate atlas records product, implemented-source,
graph-generator and stress-flow subspaces. Its reconstructed matrix dimensions
are exact over $\\mathbb{Q}$, while identification with the corresponding
polynomial spaces remains conditional:'''),
('''is $A_{10} = G_{10}\\oplus P_{10}$. The failure is concrete: the published span
meets the products in exactly one dimension over $\\mathbb{Q}$, generated by the
integer identity~\\eqref{eq:bpidentity}.''','''is $A_{10} = G_{10}\\oplus P_{10}$ for the atlas. In the archived coordinate
model the implemented-source span meets the products in one dimension over
$\\mathbb{Q}$. Equation~\\eqref{eq:bpidentity} is a sample-validated proposed
polynomial identity; the result is not assigned to corrected source formulas.'''),
]
for f in ['manuscript/main.tex','submission_candidate/main.tex']:
    edit(f,legacy_pairs)

jhep_pairs=[
('''The last equality deserves a word, because it is stronger than the modular
computation it replaced. Running the closure over $\\Q$ removes the modular
admission test that made the earlier figure a lower bound. At the fixed point no
further generated direction raises the rank over $\\Q$, so the reached span
\\emph{is} $\\Dten$ and its rank is an equality, not a bound. No separate
upper-bound argument is required.''',conditional_closure),
(r'T^{\mu}{}_{\mu} \;=\; (1 - c\,d)\,\langle F,F\rangle .',r'T^{\mu}{}_{\mu} \;=\; \bigl(1/(p-1)! - c\,d\bigr)\,\langle F,F\rangle .'),
('''the first term returns $\\langle F,F\\rangle$ up to the normalisation carried by
the factorial and the second returns''','''the first term returns $\\langle F,F\\rangle/(p-1)!$ with the displayed
definition of the pairing, and the second returns'''),
('''Read
modulo one such prime that coefficient is indistinguishable from a small
residue, and the fixed point would have been reported at the wrong dimension
with nothing in the output to indicate it.''','''A residue modulo one such prime does not uniquely determine that rational
coefficient. This does not imply that the modular matrix rank is wrong; large
coefficient height and a rank drop modulo a prime are different issues.'''),
('''This is a structural fact about the published''','''This is a fact about the archived reconstructed coordinate'''),
]
for f in ['manuscript/jhep/main.tex','manuscript/prd/main.tex']:
    edit(f,jhep_pairs)

edit('manuscript/prd_letter/main.tex',[
('''independent exact rational routine. No separate upper bound is needed: over $\\Q$
the modular admission test that made the predecessor a bound disappears, and at
the fixed point no further generated direction raises the rank, so the reached
span \\emph{is} $\\Dten$ and $\\dim_\\Q\\Dten=\\dimDtenQ$ is an equality.''','''independent exact rational routine. '''+conditional_closure),
('''Read modulo one such prime that coefficient is
indistinguishable from a small residue, and the fixed point would have been
reported at the wrong dimension with nothing in the output to indicate it.''','''A residue modulo one such prime does not determine that rational coefficient
uniquely. This does not imply that the modular rank is wrong: coefficient
height and exceptional-prime rank loss are separate issues.'''),
])

for base in ['manuscript/jhep','manuscript/prd']:
    edit(base+'/appendices/app_h_closure.tex',[
('''\\paragraph{Upper bound: why none is needed.}
Running the closure over $\\Q$ removes the modular admission test that made the
earlier figure a lower bound. At the fixed point, no further generated direction
raises the rank over $\\Q$; therefore the reached span \\emph{is} $\\Dten$, and
$\\dim_\\Q\\Dten = \\dimDtenQ$ is an equality. This is the substantive difference
between the present computation and its modular predecessor.''',r'\paragraph{Scope of the rational fixed point.}'+'\n'+conditional_closure),
])
    edit(base+'/appendices/app_i_gten.tex',[
(r'T^\mu{}_\mu = (1 - cd)\,\langle F,F\rangle .',r'T^\mu{}_\mu = \bigl(1/(p-1)! - cd\bigr)\,\langle F,F\rangle .'),
('''$\\langle F,F\\rangle$ up to normalisation''','''$\\langle F,F\\rangle/(p-1)!$ when the pairing is the unnormalised
component contraction'''),
('''degree two and first contributes at degree four.''','''degree two. In an even-degree expansion the first possible contribution is
quartic; a nonzero quartic contribution requires a separate calculation of the
interacting stress tensor.'''),
])
    edit(base+'/appendices/app_g_rank81.tex',[
('''candidates are algebraically independent: functional
independence at a generic point and algebraic independence are different
properties, and only the former is established here.''','''candidates are algebraically independent: there are more candidates than
the generic rank. In characteristic zero, a polynomial subfamily with a
nonzero maximal Jacobian minor is algebraically independent by the Jacobian
criterion. The certificate does not identify a generating set of the ideal
of polynomial relations among the entire candidate family.'''),
])
    edit(base+'/appendices/app_j_b10.tex',[
('''\\paragraph{The problem.}''','''\\paragraph{Archived source and proof scope.}
Here $B_{10}$ means the archived implemented-source coordinate span. Its
$J_{10}$--$J_{12}$ antisymmetrizers differ from the primary PDF and TeX source;
the numerical results below cannot be transferred to corrected formulas.
Reconstruction and finite holdouts validate sampled data, not polynomial
identities over $\\Q$. All intersection dimensions below are exact statements
about reconstructed matrices, conditional as polynomial-span statements.

\\paragraph{The problem.}'''),
('''This is the step that distinguishes a
reconstruction from a guess: rational reconstruction always returns
\\emph{something}, and only a prime outside the fit can tell you whether it
returned the right thing.''','''This checks the proposed reconstruction at one additional prime. Bounded
rational reconstruction can fail to find a candidate, and a successful finite
holdout does not establish a polynomial identity in characteristic zero.'''),
('''structural observation about the published choice''','''observation about the archived coordinate model'''),
])

(Path(__file__).parent/'legacy-detail-changes.json').write_text(json.dumps(changes,indent=2)+'\n')
print(json.dumps(changes,indent=2))
