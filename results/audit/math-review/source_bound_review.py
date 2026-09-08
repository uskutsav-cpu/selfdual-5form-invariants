#!/usr/bin/env python3
"""Independent exact denominator and magnitude checks for binary-point CRT.

No tensor computations and no source/repository-module imports.
"""
import json
from math import factorial,isqrt,lcm,prod,comb
from pathlib import Path

ROOT=Path(__file__).resolve().parent
primes=[32749,32719,32693,32713,32717,32771,32779]
assert len(primes)==len(set(primes))
assert all(all(p%d for d in range(2,isqrt(p)+1)) for p in primes)
modulus=prod(primes)
M=factorial(4)*comb(9,4)
N=7*6
Q=T=B=N
P=N+5*T+9*M//28
assert (9*M)%28==0 and M==3024 and P==1224
D10=[1,336,100,2400,400,3360,1000,2000,60000,200000,2700000,2700000]
derivedD10=[1,lcm(6,112),10**2,10**2*factorial(4),2**2*10**2,
            10*lcm(6,112),10**3,2*10**3,factorial(3)*10**4,
            2*10**5,10**2*30**3,10**2*30**3]
assert D10==derivedD10
# Each tuple is (#M factors, #Q/T/B factors, #P factors), with M2 and q expanded.
factors10=[(5,0,0),(4,0,1),(3,2,0),(3,2,0),(3,2,0),(3,1,1),
           (2,3,0),(2,3,0),(1,4,0),(0,5,0),(0,5,0),(0,5,0)]
def bound(factors,denominator):
    m,q,p=factors
    dummy_count=m+3*(q+p)
    return dummy_count,denominator*M**m*Q**q*P**p*10**dummy_count
rows10=[{"candidate":j+1,"clearing_denominator":d,"M_QTB_P_factor_counts":list(f),
         "summed_index_count":bound(f,d)[0],"cleared_absolute_bound":bound(f,d)[1]}
        for j,(f,d) in enumerate(zip(factors10,D10))]
D8=[1,336,100,240000,400,3360]
factors8=[(4,0,0),(3,0,1),(2,2,0),(0,4,0),(2,2,0),(2,1,1)]
rows8=[{"candidate":j+1,"clearing_denominator":d,"M_QTB_P_factor_counts":list(f),
        "summed_index_count":bound(f,d)[0],"cleared_absolute_bound":bound(f,d)[1]}
       for j,(f,d) in enumerate(zip(factors8,D8))]
hatted_bound=30**4*42**4*10**12
maximum=max([10**25,hatted_bound]+[r["cleared_absolute_bound"] for r in rows10+rows8])
assert maximum==2700000*42**5*10**15==352866326400000000000000000000
assert modulus>2*maximum
assert lcm(*D10)==37800000
assert all(d%p for p in primes for d in D10+D8+[30**4])
result={"status":"PASS","primes":primes,"all_primes_trial_division_verified":True,
        "prime_product":modulus,"maximum_cleared_absolute_bound":maximum,
        "twice_maximum_bound":2*maximum,"CRT_unique_signed_reconstruction":modulus>2*maximum,
        "integer_uniqueness_margin":modulus-2*maximum,"denominator_lcm_degree10":lcm(*D10),
        "blocks":{"F":1,"M":M,"N":N,"Q":Q,"T":T,"B":B,"P":P},
        "degree10":rows10,"degree8_primary":rows8,
        "degree8_hatted":{"H1_through_H5_denominator":30**4,"H1_through_H5_bound":hatted_bound,
                          "H6_denominator":336,"H6_bound":rows8[1]["cleared_absolute_bound"]},
        "graph_bound_degree10":10**25,"graph_bound_degree8":10**20,
        "source_quartic_square_bound":M**4*10**4,
        "assumptions":["Every coordinate is0or1 in the same integral self-dual convention.",
                       "Source definitions are normalized averages and the specified closed contractions.",
                       "Q is alternating in its first five slots, so T has denominator30.",
                       "Residue evaluations implement those fixed definitions exactly."]}
(ROOT/"source_bound_review.json").write_text(json.dumps(result,indent=2)+"\n")
print(json.dumps(result,indent=2))
