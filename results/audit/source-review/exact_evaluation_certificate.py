#!/usr/bin/env python3
"""Bounded integer CRT and exact unisolvent source/graph evaluation certificate.

The polynomial implication is explicitly relative to the published invariant-space
upper bounds dim degree8<=7 and dim degree10<=14, and source invariance. This
script establishes the exact finite evaluation matrices, their ranks, the maps,
and the intersection algebra; it does not independently derive a Hilbert series.
"""
import argparse,hashlib,json,math
from fractions import Fraction as F
from pathlib import Path
from fit_fresh_maps import rank,solve,matmul,inverse,nullspace,reduce_matrix
ROOT=Path(__file__).resolve().parent
PRIMES=[32749,32719,32693,32713,32717,32771,32779]
SEEDS=list(range(202609073000,202609073014))
D8=[1,336,100,240000,400,3360]+[810000]*5+[336]
D10=[1,336,100,2400,400,3360,1000,2000,60000,200000,2700000,2700000]


def bounds():
    M,Q,P=3024,42,1224
    b8=[M**4*10**4,M**3*P*10**6,M**2*Q**2*10**8,Q**4*10**12,M**2*Q**2*10**8,M**2*Q*P*10**8]+[Q**4*10**12]*5+[M**3*P*10**6]
    b10=[M**5*10**5,M**4*P*10**7]+[M**3*Q**2*10**9]*3+[M**3*Q*P*10**9]+[M**2*Q**3*10**11]*2+[M*Q**4*10**13]+[Q**5*10**15]*3
    return {'coordinate_absolute_bound':1,'block_absolute_bounds':{'M':M,'N':Q,'Q':Q,'T':Q,'B':Q,'P':P},
      'block_derivation':{'M':'4!*C(9,4)=3024 nonzero ordered contraction summands, each absolute value<=1',
      'N':'7*6=42 ordered pairs disjoint from a fixed nonzero triple; each summand absolute value<=1',
      'Q_T_B':'normalized antisymmetric averages of N, Q, Q respectively cannot increase maximum absolute component',
      'P':'42+5*42+(9/28)*3024=1224; both trace projectors are normalized'},
      'block_denominators':{'M':1,'N':1,'Q':10,'T':30,'B':20,'P':336},
      'denominator_derivation':{'Q':'N already antisymmetric abc and de, so first-five antisym is ten signed (3,2) shuffles divided by10',
      'T':'Q antisymmetric in last-block first two slots; normalized last-three antisym is three signed terms divided by3, denominator30',
      'B':'normalized last-pair antisym divides Q by2, denominator20',
      'P':'N-5T-(9/28)*Alt3Alt3(g*g*M); 5T denominator6, trace term denominator28*36/9=112; lcm(6,112)=336'},
      'degree8':{'denominators':D8,'scalar_absolute_bounds':b8,'integer_numerator_absolute_bounds':[d*b for d,b in zip(D8,b8)],'external_dummy_index_counts':[4,6,8,12,8,8]+[12]*5+[6],'graph_absolute_bound':10**20,'denominator_lcm':math.lcm(*D8)},
      'degree10':{'denominators':D10,'scalar_absolute_bounds':b10,'integer_numerator_absolute_bounds':[d*b for d,b in zip(D10,b10)],'external_dummy_index_counts':[5,7,9,9,9,9,11,11,13,15,15,15],'graph_absolute_bound':10**25,'denominator_lcm':math.lcm(*D10)},
      'graph_bound_derivation':'A degree-d complete contraction has5*d/2 metric edges, each with10 choices; diagonal metric coefficients and binary F components have absolute value<=1. Products obey the same total edge bound.'}


def prime(p):return p>=2 and all(p%k for k in range(2,math.isqrt(p)+1))

def crt_integer(residues,ps,bound):
    x=0;m=1
    for a,p in zip(residues,ps):x+=m*((a-x)*pow(m,-1,p)%p);m*=p
    assert m>2*bound,('insufficient CRT modulus',m,bound)
    if x>m//2:x-=m
    assert abs(x)<=bound,('recovered numerator outside rigorous bound',x,bound)
    assert all(x%p==a%p for a,p in zip(residues,ps))
    return x


def serialize(a):return [[str(x) for x in row] for row in a]

def build():
    bs=bounds();assert all(prime(p) for p in PRIMES) and len(set(PRIMES))==len(PRIMES)
    modulus=math.prod(PRIMES);allpoints=[];evidence=[]
    for seed in SEEDS:
        points=[]
        for p in PRIMES:
            path=ROOT/'binary-points'/f'p{p}-s{seed}.json';data=json.loads(path.read_text())
            assert data['prime']==p and data['seed']==seed and set(data['coordinates'])<=set((0,1))
            if points:assert data['coordinates']==points[0]['coordinates']
            points.append(data);evidence.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest()})
        allpoints.append(points)
    integer={};exact={}
    for degree,keys in [(8,['atlas8','all8']),(10,['atlas10','degree10'])]:
        b=bs[f'degree{degree}']
        for key in keys:
            source=key.startswith('all') or key=='degree10'
            ds=b['denominators'] if source else [1]*(7 if degree==8 else 14)
            nums=b['integer_numerator_absolute_bounds'] if source else [b['graph_absolute_bound']]*len(ds)
            rows=[]
            for points in allpoints:
                vals=[x['primary8']+x['hatted8'] if key=='all8' else x[key] for x in points]
                rows.append([crt_integer([row[j]*ds[j]%p for row,p in zip(vals,PRIMES)],PRIMES,nums[j]) for j in range(len(ds))])
            integer[key]=rows;exact[key]=[[F(x,d) for x,d in zip(row,ds)] for row in rows]
    A8,A10=exact['atlas8'],exact['atlas10'];B8,B10=exact['all8'],exact['degree10']
    assert rank(A8)==7 and rank(A10)==14
    full8=solve(A8,B8,None);map10=solve(A10,B10,None)
    map8=full8[:5]+full8[6:7]+[[F(int(i==6)) for i in range(7)]]
    inv8=inverse(map8)
    assert matmul(A8,list(zip(*full8)))==B8
    assert matmul(A10,list(zip(*map10)))==B10
    assert matmul(map8,inv8)==[[int(i==j) for j in range(7)] for i in range(7)]
    productbasis=[[F(int(i==j)) for i in range(14)] for j in [12,13]]
    source_rank=rank(map10);union_rank=rank(map10+productbasis)
    relations=nullspace(list(zip(*(row[:12] for row in map10))))
    witnesses=[];product_vectors=[]
    for relation in relations:
        v=matmul([relation],map10)[0];assert not any(v[:12])
        if rank(product_vectors+[v[12:]])>len(product_vectors):
            product_vectors.append(v[12:])
            witnesses.append({'source_combination':list(map(str,relation)),'product_coefficients':list(map(str,v[12:]))})
    assert len(witnesses)==source_rank+2-union_rank
    # All dense phase02 evidence remains an independent crosscheck, not a premise.
    checks=[]
    for path in sorted((ROOT/'fresh-points').glob('*.json')):
        point=json.loads(path.read_text());p=point['prime']
        for matrix,atlas,target in [(full8,'atlas8','all8'),(map10,'atlas10','degree10')]:
            want=point['primary8']+point['hatted8'] if target=='all8' else point[target]
            got=[sum(x*y for x,y in zip(row,point[atlas]))%p for row in reduce_matrix(matrix,p)]
            assert got==want,(str(path),target)
        checks.append({'path':str(path.relative_to(ROOT)),'sha256':hashlib.sha256(path.read_bytes()).hexdigest(),'passed':True})
    theorem='Given dim invariant_degree8<=7 and dim invariant_degree10<=14 over Q, and that the transcribed contractions are invariant polynomials on the stated self-dual representation, exact rank7/rank14 graph evaluation matrices establish graph bases. Evaluation is injective on each invariant space (and an isomorphism onto its image), so the exact solved matrices give polynomial identities. Hilbert upper bounds and source invariance are premises, not inferred from finite sampling.'
    common={'schema':3,'status':'exact evaluation certificate, conditional on published Hilbert dimensions 7 and 14, and analytic invariance of source contractions','source_reading':'literal-red-brackets-2026-09-07','frozen_base_commit':'2b7663bbf5a06d1340973434f195a84ae2773e8f','proof_scope':theorem,'certificate':'results/audit/source-review/exact-source-evaluation-certificate.json'}
    d8={**common,'degree':8,'literature_basis':['T8_1','T8_2','T8_3','T8_4','T8_5','H8_1'],'graph_basis':[f'I8_{i}' for i in range(1,7)],'product':'I4_1^2','matrix_convention':'Rows express [T8_1,...,T8_5,H8_1,I4_1^2] in [I8_1,...,I8_6,I4_1^2]',
       'literature_to_graph':serialize(map8),'graph_to_literature':serialize(inv8),'product_correction':[str(row[6]) for row in inv8[:6]],'exact_6x6_without_products':not any(row[6] for row in inv8[:6]),'all_displayed_literature_to_graph':serialize(full8),'all_displayed_order':['T8_'+str(i) for i in range(1,7)]+['H8_'+str(i) for i in range(1,7)],'verified':True}
    d10={**common,'degree':10,'literature_basis':[f'P10_{i:02d}' for i in range(1,13)],'graph_and_product_basis':[f'I10_{i}' for i in range(1,13)]+['I4_1*I6_1','I4_1*I6_2'],'matrix_convention':'T_i=sum_j matrix_12x14[i][j]*atlas_j','matrix_12x14':serialize(map10),'published_span_rank':source_rank,'product_span_rank':2,'union_rank':union_rank,'intersection_rank':source_rank+2-union_rank,'primitive_quotient_rank':union_rank-2,'product_intersection_witnesses':witnesses,'verified_reconstruction':True}
    from evaluate_fresh_points import definitions
    defs=definitions()
    invariant_argument='F is restricted to its self-dual representation. M,N,Q,T,B,P are tensor contractions, normalized index permutations, and invariant-metric products. Every displayed scalar pairs each index exactly once with an inverse metric, hence is an invariant homogeneous polynomial; each M,N,Q,T,B,P factor has degree2 in F. The metric and oriented self-dual restriction are preserved by the connected Lorentz group, whose complexification yields the SO(10,C) invariant space used by the cited Hilbert bound.'
    certificate_sources=[ROOT/'source_scalar_oracle.py',ROOT/'evaluate_binary_points.py',ROOT/'evaluate_fresh_points.py',Path(__file__),ROOT/'fit_fresh_maps.py',ROOT/'manual-transcription-preimplementation.md']
    dense_holdout=[json.loads(f.read_text()) for f in sorted((ROOT/'fresh-points').glob('p32771-s*.json'))]
    d8['primitive_quotient_matrix_6x6']=serialize([row[:6] for row in inv8[:6]])
    d8['holdout_prime']=32771
    d8['prime_witnesses']={'32771':{'prime':32771,'samples':[{'seed':p['seed'],'coordinates':p['coordinates'],'graphs':p['atlas8'],'tensors':p['selected8']} for p in dense_holdout]}}
    d8['literature_source']={'paper':'Some remarks on invariants','arxiv':'2509.14350v2','url':'https://arxiv.org/html/2509.14350v2#S4.SS1.SSS3','selected_equations':['4.12','4.12','4.13','4.14','4.15','4.18']}
    d8['source_qualification']='Literal displayed contractions are used. Irrep trace-subtraction prose does not supply an additional projector in those formulas. H8_2 first definition is4.19; its following reduction is4.20.'
    d10['literature_source']={'paper':'Some remarks on invariants','arxiv':'2509.14350v2','url':'https://arxiv.org/html/2509.14350v2#S4.SS1.SSS4','equation':'4.24','source_labels':['I10'+str(i) for i in range(1,13)]}
    cert={**common,'invariance_argument':invariant_argument,'graph_definitions':defs,'audit_source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in certificate_sources},'primes':PRIMES,'modulus':modulus,'seeds':SEEDS,'coordinates':[ps[0]['coordinates'] for ps in allpoints],'bounds':bs,'exact_integer_numerator_evaluations':integer,'exact_rational_evaluations':{k:serialize(v) for k,v in exact.items()},'ranks':{'atlas8':7,'atlas10':14,'source8_selected':rank(map8),'source8_primary':rank(full8[:6]),'source8_hatted':rank(full8[6:]),'source8_primary_with_product':rank(full8[:6]+[map8[-1]]),'source8_hatted_with_product':rank(full8[6:]+[map8[-1]]),'source10':source_rank,'source10_primitive_quotient':union_rank-2,'product_intersection':source_rank+2-union_rank},'point_evidence':evidence,'dense_modular_crosschecks':checks,'maps':{'degree8':d8,'degree10':d10}}
    for filename,data in [('exact-source-evaluation-certificate.json',cert),('order8_change_of_basis_exact.json',d8),('order10_change_of_basis_exact.json',d10)]:
        (ROOT/filename).write_text(json.dumps(data,indent=2)+'\n')
    print(json.dumps({'ranks':cert['ranks'],'modulus':modulus,'crosschecks':len(checks),'intersection_witnesses':witnesses,'max_numerator_bound':max(bs['degree10']['integer_numerator_absolute_bounds'])},indent=2))


def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bounds-only',action='store_true');ap.add_argument('--pilot-rank',action='store_true');args=ap.parse_args()
    if args.bounds_only:
        data={'primes':PRIMES,'primality':[prime(p) for p in PRIMES],'modulus':math.prod(PRIMES),'bounds':bounds()};assert all(data['primality'])
        (ROOT/'exact-evaluation-bounds.json').write_text(json.dumps(data,indent=2)+'\n');print(json.dumps(data,indent=2))
    elif args.pilot_rank:
        pts=[json.loads((ROOT/'binary-points'/f'p{PRIMES[0]}-s{s}.json').read_text()) for s in SEEDS]
        r8=rank([p['atlas8'] for p in pts],PRIMES[0]);r10=rank([p['atlas10'] for p in pts],PRIMES[0]);print('binary pilot ranks:',r8,r10);assert(r8,r10)==(7,14)
    else:build()
if __name__=='__main__':main()
