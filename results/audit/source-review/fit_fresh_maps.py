#!/usr/bin/env python3
"""Fit only phase-02 point values; independent Python-int/Fraction elimination."""
import argparse,json,hashlib
from pathlib import Path
from fractions import Fraction
from math import isqrt,gcd
ROOT=Path(__file__).resolve().parent


def rref(matrix,p=None,pivot_columns=None):
    a=[[int(x)%p if p else Fraction(x) for x in row] for row in matrix]
    if not a:return a,[]
    piv=[];row=0
    for col in range(len(a[0]) if pivot_columns is None else pivot_columns):
        k=next((k for k in range(row,len(a)) if a[k][col]),None)
        if k is None:continue
        a[row],a[k]=a[k],a[row]
        factor=pow(a[row][col],-1,p) if p else 1/a[row][col]
        a[row]=[(x*factor)%p if p else x*factor for x in a[row]]
        for k in range(len(a)):
            if k==row or not a[k][col]:continue
            factor=a[k][col]
            a[k]=[(x-factor*y)%p if p else x-factor*y for x,y in zip(a[k],a[row])]
        piv.append(col);row+=1
        if row==len(a):break
    return a,piv


def rank(a,p=None):return len(rref(a,p)[1])


def solve(A,B,p):
    n=len(A[0]);m=len(B[0])
    a,piv=rref([list(x)+list(y) for x,y in zip(A,B)],p,pivot_columns=n)
    if len(piv)!=n:raise ValueError(('atlas rank failure',len(piv),n))
    if any(any(row[n:]) for row in a[n:]):raise ValueError('target outside atlas span')
    return [[a[j][n+i] for j in range(n)] for i in range(m)]


def matmul(A,B,p=None):
    return [[sum(x*y for x,y in zip(a,col))%p if p else sum(x*y for x,y in zip(a,col))
             for col in zip(*B)] for a in A]


def reduce_matrix(A,p):return [[int(Fraction(x).numerator*pow(Fraction(x).denominator,-1,p)%p) for x in row] for row in A]


def rational_reconstruct(xs,ps):
    residue=0;modulus=1
    for x,p in zip(xs,ps):
        residue+=modulus*((x-residue)*pow(modulus,-1,p)%p);modulus*=p
    residue%=modulus
    if not residue:return Fraction(0)
    limit=isqrt(modulus//2)
    previous,current=modulus,residue;old_t,t=0,1
    while current>limit:
        q=previous//current;previous,current=current,previous-q*current;old_t,t=t,old_t-q*t
    if not t:raise ValueError('rational reconstruction failed')
    answer=Fraction(current,t)
    if abs(answer.numerator)>limit or answer.denominator>limit or gcd(answer.denominator,modulus)!=1:
        raise ValueError('no bounded rational reconstruction')
    if any(answer.numerator*pow(answer.denominator,-1,p)%p!=x%p for x,p in zip(xs,ps)):
        raise ValueError('reconstruction residue mismatch')
    return answer


def inverse(A):
    n=len(A);R,piv=rref([list(row)+[int(i==j) for j in range(n)] for i,row in enumerate(A)],pivot_columns=n)
    if len(piv)!=n:raise ValueError('singular rational map')
    return [row[n:] for row in R]


def nullspace(A):
    R,piv=rref(A);n=len(A[0]);result=[]
    for free in (j for j in range(n) if j not in piv):
        v=[Fraction(int(j==free)) for j in range(n)]
        for i,k in enumerate(piv):v[k]=-R[i][free]
        result.append(v)
    return result


def process_prime(p):
    paths=sorted((ROOT/'fresh-points').glob(f'p{p}-s*.json'))
    points=[json.loads(path.read_text()) for path in paths]
    # At least 14 training rows and two independent holdouts for degree 10.
    if len(points)<16:raise ValueError(f'prime {p}: only {len(points)} points, require 16')
    fit=points[:14];holdout=points[14:]
    m8=solve([s['atlas8'] for s in fit],[s['selected8'] for s in fit],p)
    full8=solve([s['atlas8'] for s in fit],[s['primary8']+s['hatted8'] for s in fit],p)
    m10=solve([s['atlas10'] for s in fit],[s['degree10'] for s in fit],p)
    for point in points:
        for matrix,atlas,target in [(m8,'atlas8','selected8'),(m10,'atlas10','degree10')]:
            value=[sum(x*y for x,y in zip(row,point[atlas]))%p for row in matrix]
            if value!=point[target]:raise ValueError(('holdout failure',p,point['seed'],target))
    products=[[int(j==i) for j in range(14)] for i in [12,13]]
    mr=rank(m10,p);ur=rank(m10+products,p)
    record={'prime':p,'fit_seeds':[s['seed'] for s in fit],'holdout_seeds':[s['seed'] for s in holdout],
            'atlas8_rank':rank([s['atlas8'] for s in points],p),'atlas10_rank':rank([s['atlas10'] for s in points],p),
            'source8_selected_rank':rank(m8,p),'source8_primary_rank':rank(full8[:6],p),'source8_hatted_rank':rank(full8[6:],p),
            'matrix8':m8,'matrix8_all_displayed':full8,'matrix10':m10,'source10_rank':mr,'union_with_products_rank':ur,'product_intersection_rank':mr+2-ur,
            'source10_primitive_quotient_rank':ur-2,'holdouts_passed':True,
            'point_files':[{'file':str(f.relative_to(ROOT)),'sha256':hashlib.sha256(f.read_bytes()).hexdigest()} for f in paths]}
    (ROOT/f'fit-p{p}.json').write_text(json.dumps(record,indent=2)+'\n')
    print('PRIME',p,'ranks',record['source10_rank'],record['source10_primitive_quotient_rank'],record['product_intersection_rank'],flush=True)
    return record


def reconstruct(records,holdout_primes):
    ps=[r['prime'] for r in records]
    matrices={key:[[rational_reconstruct([rec[key][i][j] for rec in records],ps) for j in range(len(records[0][key][i]))] for i in range(len(records[0][key]))]
              for key in ['matrix8','matrix8_all_displayed','matrix10']}
    holdout=[]
    for p in holdout_primes:
        points=[json.loads(f.read_text()) for f in sorted((ROOT/'fresh-points').glob(f'p{p}-s*.json'))]
        if len(points)<3:raise ValueError('holdout prime requires three fresh points')
        for s in points:
            for key,atlas,target in [('matrix8','atlas8','selected8'),('matrix10','atlas10','degree10')]:
                matrix=reduce_matrix(matrices[key],p)
                if [sum(x*y for x,y in zip(row,s[atlas]))%p for row in matrix]!=s[target]:
                    raise ValueError(('rational map fresh-prime holdout failure',p,s['seed'],key))
        holdout.append({'prime':p,'seeds':[s['seed'] for s in points],'passed':True})
    A=matrices['matrix10'];products=[[Fraction(int(j==i)) for j in range(14)] for i in [12,13]]
    R=rank(A);U=rank(A+products)
    relations=nullspace(list(zip(*(row[:12] for row in A))))
    witnesses=[];product_vectors=[]
    for relation in relations:
        v=matmul([relation],A)[0]
        assert not any(v[:12])
        if rank(product_vectors+[v[12:]])>len(product_vectors):
            product_vectors.append(v[12:]);witnesses.append({'source_combination':list(map(str,relation)),'product_coefficients':list(map(str,v[12:]))})
    assert len(witnesses)==R+2-U
    proof_scope='Rational matrix ranks and inverse/intersection algebra are exact. Source-to-graph polynomial identities are supported by fresh modular point fits and disjoint point/prime holdouts, not a symbolic identity proof.'
    common={'schema':2,'status':'fresh validation observation, not a final scientific claim','frozen_base_commit':'2b7663bbf5a06d1340973434f195a84ae2773e8f','fitting_primes':ps,'fresh_prime_holdouts':holdout,'proof_scope':proof_scope}
    B=matrices['matrix8'];invB=inverse(B)
    d8={**common,'degree':8,'literature_basis':['T8_1','T8_2','T8_3','T8_4','T8_5','H8_1'],
        'graph_basis':[f'I8_{i}' for i in range(1,7)],'product':'I4_1^2',
        'matrix_convention':'literature_to_graph rows express [T8_1,...,T8_5,H8_1,I4_1^2] in [I8_1,...,I8_6,I4_1^2]',
        'literature_to_graph':[[str(x) for x in row] for row in B],'graph_to_literature':[[str(x) for x in row] for row in invB],
        'product_correction':[str(row[6]) for row in invB[:6]],'exact_6x6_without_products':not any(row[6] for row in invB[:6]),
        'all_displayed_literature_to_graph':[[str(x) for x in row] for row in matrices['matrix8_all_displayed']],
        'all_displayed_order':['T8_'+str(i) for i in range(1,7)]+['H8_'+str(i) for i in range(1,7)],
        'verified':True,'prime_witnesses':{str(r['prime']):r for r in records}}
    d10={**common,'degree':10,'source_reading':'literal-red-brackets-2026-09-07','literature_basis':[f'P10_{i:02d}' for i in range(1,13)],
         'graph_and_product_basis':[f'I10_{i}' for i in range(1,13)]+['I4_1*I6_1','I4_1*I6_2'],
         'matrix_convention':'T_i=sum_j matrix_12x14[i][j]*atlas_j','matrix_12x14':[[str(x) for x in row] for row in A],
         'published_span_rank':R,'product_span_rank':2,'union_rank':U,'intersection_rank':R+2-U,'primitive_quotient_rank':U-2,
         'product_intersection_witnesses':witnesses,'verified_reconstruction':True,'prime_witnesses':{str(r['prime']):r for r in records}}
    for degree,data in [(8,d8),(10,d10)]:
        (ROOT/f'order{degree}_change_of_basis_corrected.json').write_text(json.dumps(data,indent=2)+'\n')
    print('RATIONAL source10 ranks:',R,U-2,R+2-U,'intersection witnesses:',witnesses,flush=True)


def main():
    p=argparse.ArgumentParser();p.add_argument('--primes',type=int,nargs='+',required=True);p.add_argument('--holdout-primes',type=int,nargs='*',default=[]);p.add_argument('--reconstruct',action='store_true');args=p.parse_args()
    records=[process_prime(prime) for prime in args.primes]
    if args.reconstruct:reconstruct(records,args.holdout_primes)
if __name__=='__main__':main()
