# Independent manual source transcription, frozen before implementation reads

Source: https://arxiv.org/html/2509.14350v2 and freshly downloaded original TeX/PDF https://arxiv.org/src/2509.14350v2, https://arxiv.org/pdf/2509.14350v2 . Manuscript v2 dated 29 January 2026. This is a manually authored transcription and derivation, not copied from repository code or old audit evidence. Original source is preserved separately. No frozen implementation or result file has yet been opened.

Conventions (equations 4.1, 4.4, 4.5; Appendix C): metric diag(-1,+1,...,+1), epsilon_0123456789=+1; F=*F. M_ab = F_aijkl F_b^ijkl with NO 1/4!; N_abc,def = F_abcij F_def^ij with NO 1/2!. All Einstein sums are over ordered component indices, not sorted index subsets. Antisymmetrization and symmetrization divide by p!; nested red operations are applied AFTER black operations. No complex conjugation is implied by a contraction.

I use Q[a b c d e;f] for the first-five-antisymmetric 1050 tensor N_[abc,de]f, and P[abc;def] for the 4125 tensor. Define T[abc;def]=Alt_def Q[abcde;f], and B[abcd;ef]=Alt_ef Q[abcde;f]. Since Q is antisymmetric in d,e, T=(Q[abcde;f]+Q[abcef;d]+Q[abcfd;e])/3. B=(Q[abcde;f]-Q[abcdf;e])/2. Q=Alt_first5 N is the normalization implied by the decomposition and C.13, C.23; P=N-5T-(9/28) Alt_abc Alt_def(g_ad g_be M_cf). The six-index trace subtraction has a normalized 3!x3! double antisymmetrizer, not a single determinant without division.

The compact scalar formulas below put every tensor component down. For each repeated dummy letter, insert exactly ONE inverse metric contraction joining its two occurrences. Thus in a diagonal frame every dummy index contributes its signature once. M2_ab=M_ac g^cd M_db. A multi-letter dummy such as A denotes four ordered, independently summed indices with four metrics. These conventions retain every upper/lower contraction in the source without visually mixing heights across nested brackets.

Degree 8 primary list:
(4.12) I1=tr((g^-1 M)^4); I2=M[a i]M[b j]M[c k]P[ijk;abc].
(4.13) I3=M[a b] Q[A a;b] Q[A c;d] M[c d].
(4.14) I4=Sym_abcd(Q[A a;b] Q[A c;d]) Q[B a;b] Q[B c;d]. Here both A and B stand for FOUR indices; Sym is the normalized full 24-term operation.
(4.15) I5=Alt_ij Alt_ab(M[i a]M[j b]) Q[A a;b]Q[A i;j].
(4.16) I6=M[i a]M[j b] Q[a b r s t;u] P[r s t;u i j].
P0=(tr((g^-1 M)^2))^2, the one degree-8 lower-product direction.

IMPORTANT source qualification: prose around (4.13)-(4.15) discusses subtracting all traces to identify irreps 660/770; displayed formulas do not write a trace-subtraction operator or its coefficients. The audit must distinguish literal displayed formulas from additional projected-irrep conventions. The claim of automatic total symmetry next to (4.13) must not be substituted for an independent check of what C.33 actually proves. Formula I4 explicitly has red Sym over FOUR free indices.

Degree 8 alternate list, reading first displayed definitions literally:
(4.18) H1=-T[abc;d r s]T[abc;d u v]T[u r l;m n o]T[s l m;v n o].
(4.19) H2= T[abc;d r s]T[abc;d u v]T[r l m;u n o]T[s l n;m o v]. Its second displayed equality is numbered (4.20) in the PDF/source because of an un-suppressed eqnarray line; the HTML collapses the first/second numbering.
(4.21) H3= T[abc;r s t]T[abc;u v w]T[r s l;m n u]T[t v m;l n w].
(4.22) H4= T[abc;r s t]T[abc;u v w]T[u r l;s m n]T[t v m;w l n].
(4.23) H5= T[u r a;b c d]T[s a b;v c d]T[s u l;m n o]T[v l m;r n o].
H6=I2, stated in prose after (4.23).

Displayed reductions requiring separate checks, not definitions to impose:
H1=1/3^4 * ((5/6)*K + (1/7200)*I1 - (70/1200^2)*P0).
H2=1/3^4 * (K + (1/240^2)*I1 - (1/(10*240^2))*P0).
K=B[A;r s]B[A;u v]Q[B r;s]Q[B u;v].
H5=-(5/6)H1 + 25/(4*9^3)I4 + x I1 + y P0, where source does not supply x,y.
The full basis transformation is expressly left uncomputed by the authors.

Degree 10 list in section 4.1.4, source labels I101-I1012. PDF has (4.24) on an otherwise blank eqnarray line following I10^(1); remaining entries are unnumbered. Cite section and superscript j, rather than inventing distinct equation numbers.
J1=tr((g^-1 M)^5).
J2=M2[a i]M[b j]M[c k]P[ijk;abc].
J3=M[a i]M[b j]M[c k]Q[a b c d e;f]Q[i j k d e;f].
J4=M2[a b]M[c d]Sym_abcd(Q[A a;b]Q[A c;d]).
J5=Alt_ij Alt_ab(M2[i a]M[j b])Q[A a;b]Q[A i;j].
J6=M2[i a]M[j b]Q[a b r s t;u]P[r s t;u i j].
J7=Q[r s t u v;a]M2[a b]Q[r s t c d;e]Q[u v b c e;d].
J8=Q[r s t u v;a]Alt_va(M[v w]M[a b])Q[r s t c d;e]Q[u w b c e;d]. Alt_va acts on the two M factors only and divides by 2.
J9=Sym_nrl(Q[A k;n]M[k m]Q[A r;l])Q[B m;n]Q[B r;l]. The red round brackets start at nu and end at lambda, so ONLY n,r,l are symmetrized (3!=6), not m or k.
J10=B[r s t u;a b]Q[r s t c d;e]Q[u i j c e;d]Q[A i;j]Q[A a;b]. The red antisymmetrizer is over a,b in the first Q only; it divides by 2.
J11=Q[r s t a b;c]Q[d e f a b;c]T[d e f;i j k]T[r s l;m n i]T[t j m;l n k].
J12=Q[r s t a b;c]Q[d e f a b;c]T[d e f;i j k]T[i r l;s m n]T[t j m;k l n].

The alpha-slot permutation c,e;d in J7,J8,J10 is intentional: the source's final Q has alpha1 alpha3 in its antisymmetric five slots and alpha2 in the final slot. J3,J11,J12 contract the same alpha-slot order between their first two Q factors. Source footnote 8 makes this distinction explicit already at degree 6.

The degree-10 source expressly describes these as possible candidates, not an established basis. Equation (4.2) supplies total degree-10 dimension 14 and a plethystic exponent 12. One must not conflate those dimensions with the rank of this particular displayed list or with its quotient modulo the two products of degrees 4 and 6. A 12x14 coordinate atlas alone would not prove a one-dimensional intersection; the rank of its 12 quotient-coordinate columns, together with full row rank and a genuine 14-element polynomial basis, would.

Procedure exception: bootstrap `pwd && ls -la` read only this newly created audit directory before wrapper use. Root then authorized ordinary reads of fresh audit command logs. All source-download/extraction/transcription commands and forthcoming computations are wrapped; no prior checkout, checkpoints, caches, or earlier-agent scientific analysis were read.
