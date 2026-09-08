"""Independent infinitesimal Lorentz action, with no repository-module imports."""
from pathlib import Path
from itertools import combinations
import hashlib
import json

ROOT = Path(__file__).resolve().parents[1]
tuples = list(combinations(range(10), 5))
coordinate_tuples = [t for t in tuples if 0 in t]


def sign(seq):
    return (-1)**sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))


def eliminate(matrix,p):
    a = [[int(x)%p for x in r] for r in matrix]
    rank,cols,det = 0,[],1
    for c in range(len(a[0])):
        k = next((k for k in range(rank,len(a)) if a[k][c]),None)
        if k is None: continue
        if k!=rank: a[k],a[rank]=a[rank],a[k];det=-det
        v=a[rank][c];det=det*v%p; inv=pow(v,-1,p)
        for k in range(rank+1,len(a)):
            scale=a[k][c]*inv%p
            if scale:a[k]=[(x-scale*y)%p for x,y in zip(a[k],a[rank])]
        rank+=1;cols.append(c)
        if rank==len(a):break
    return rank,cols,det if rank==len(a) else 0


outputs=[]
for cell in json.loads((ROOT/'root-review/fresh_cells.json').read_text())['cells']:
    p=cell['prime']; amap=dict(zip(coordinate_tuples,cell['coordinates']))
    def component(ordered):
        if len(set(ordered))!=5:return 0
        canonical=tuple(sorted(ordered))
        parity=sign(ordered)
        if 0 in canonical:return parity*amap[canonical]%p
        complement=tuple(i for i in range(10) if i not in canonical)
        # Output-first epsilon convention, one negative metric in complement.
        return -parity*sign(canonical+complement)*amap[complement]%p
    full=[component(t) for t in tuples]
    witness=json.loads((ROOT/f'root-review/fresh-witness-p{p}.json').read_text())
    assert full==witness['selfdual_components']
    generators=[]; vectors=[]
    for i,j in combinations(range(10),2):
        # A^T eta + eta A = 0; rotations are antisymmetric, boosts symmetric.
        reverse=1 if i==0 else -1
        generators.append({'plane':[i,j], 'kind':'boost' if i==0 else 'rotation',
                           'entries':[[i,j,1],[j,i,reverse]]})
        vector=[]
        for t in tuples:
            total=0
            for slot,x in enumerate(t):
                if x==i:
                    replaced=list(t);replaced[slot]=j;total+=component(replaced)
                elif x==j:
                    replaced=list(t);replaced[slot]=i;total+=reverse*component(replaced)
            vector.append(total%p)
        # The entire tangent form must remain in the independently built +1 space.
        dmap={t:v for t,v in zip(tuples,vector) if 0 in t}
        for t,v in zip(tuples,vector):
            if 0 not in t:
                complement=tuple(x for x in range(10) if x not in t)
                assert v == -sign(t+complement)*dmap[complement]%p
        vectors.append([v for t,v in zip(tuples,vector) if 0 in t])
    rank,pivot_coordinates,det=eliminate(vectors,p)
    assert rank==45 and det!=0
    minor=[[r[c] for c in pivot_coordinates] for r in vectors]
    assert eliminate(minor,p)[2]==det
    for row in witness['jacobian']:
        for tangent in vectors:
            assert sum(a*b for a,b in zip(row,tangent))%p==0
    result={'prime':p,'seed':cell['seed'],'orbit_rank':rank,
            'generators':generators,'generator_rows_45x126':vectors,
            'minor_coordinate_indices':pivot_coordinates,'minor_45x45':minor,
            'minor_determinant_mod_p':det,'selfduality_of_all_45_tangents':True,
            'all_81_jacobian_rows_annihilate_all_45_tangents':True,
            'frozen_basis_file_sha256':witness['basis_file_sha256']}
    outputs.append(result)
    print(json.dumps({k:result[k] for k in ['prime','seed','orbit_rank','minor_determinant_mod_p']},indent=2),flush=True)
report={'passed':True,'implementation':'Pure Python signed components and infinitesimal matrix action; no repository imports; exact integer modular elimination.',
        'proof_scope':'Nonzero minor of the integral linear orbit-action matrix certifies generic orbit dimension45 in characteristic zero; invariance makes all invariant differentials annihilate those directions, giving generic bound126−45=81. This verifies an existing dimension argument, not rational generation or global separation.',
        'cells':outputs}
(ROOT/'root-review/orbit_tangent_certificate.json').write_text(json.dumps(report,indent=2)+'\n')
