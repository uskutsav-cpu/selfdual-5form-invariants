from pathlib import Path
import hashlib,json
root=Path(__file__).resolve().parents[1]/'repair-checkout'
p=root/'paper/manuscript.tex'
before=s=p.read_text()
a='''Invariance and the cited generic quotient dimension supply the matching upper
bound. On a regular local quotient this gives local coordinates. It proves
neither global orbit separation, generation of the invariant field by rational
functions in this list, nor polynomial generation of the entire ring.'''
b='''Invariance and the generic orbit dimension supply the matching upper bound.
The independent audit companion
\\path{root-review/orbit_tangent_certificate.json} records the 45 infinitesimal
Lorentz generators acting on the 126 integral self-dual coordinates, using a
separate signed-component implementation. Its $45\\times45$ minors are nonzero
at primes 50021 and 32749, with residues 5222 and 10852, respectively. The
orbit-action entries are integral linear polynomials in $A$, so the same
nonzero-minor lifting argument proves generic orbit dimension at least 45 in
characteristic zero. There are only 45 generators, hence the generic dimension
is exactly 45. Every invariant differential annihilates this tangent space,
giving the upper bound $126-45=81$. The companion additionally checks that all
81 computed Jacobian rows annihilate all 45 action rows at both points. This
supplies a direct witness for the generic dimension also cited in the literature.
On a regular local quotient the selected invariants give local coordinates.
Neither global orbit separation, generation of the invariant field by rational
functions in this list, nor polynomial generation of the entire ring follows.'''
assert a in s
s=s.replace(a,b)
p.write_text(s)
print(json.dumps({'path':str(p.relative_to(root)),'before_sha256':hashlib.sha256(before.encode()).hexdigest(),'after_sha256':hashlib.sha256(s.encode()).hexdigest()},indent=2))
