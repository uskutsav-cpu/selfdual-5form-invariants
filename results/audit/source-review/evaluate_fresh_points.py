#!/usr/bin/env python3
"""Fresh source/graph values; accepts no old numerical witness input."""
import argparse
from contextlib import ExitStack
import hashlib,json,time,sys
from pathlib import Path
from unittest.mock import patch
import numpy as np
from source_scalar_oracle import blocks,source_values,form_from_coordinates,metric_axes,bracket
ROOT=Path(__file__).resolve().parent
CHECKOUT=ROOT.parent/'repair-checkout'
sys.path.insert(0,str(CHECKOUT/'src'))
from sdinv.contract import planned_value
from sdinv.graphs import graph_from_label
from sdinv import stress
from sdinv import published_degree8_invariants as pub8
from sdinv import published_degree10_invariants as pub10


def save(path,payload):
    path.write_text(json.dumps(payload,indent=2)+'\n')


def definitions():
    items=[]
    for filename in ('10d_order8.json','10d_order10.json'):
        items.extend(json.loads((CHECKOUT/'results'/filename).read_text())['generators'])
    return {i['id']:i for i in items if i['order']<=10}


def point(prime,seed,compare=False):
    start=time.monotonic();times={}
    coords=np.random.default_rng(seed).integers(0,prime,size=126).tolist()
    F=form_from_coordinates(coords,prime)
    b=blocks(F,prime);times['form_blocks']=time.monotonic()-start
    t=time.monotonic();v=source_values(b,prime);times['source_scalars']=time.monotonic()-t
    checks={}
    if compare:
        t=time.monotonic()
        checks['Q_ten_shuffles_equals_120_terms']=bool(np.array_equal(b['Q'],bracket(b['N'],(0,1,2,3,4),prime)))
        if not checks['Q_ten_shuffles_equals_120_terms']:raise AssertionError('shuffle projector mismatch')
        for name,fn in [('M',stress.five_form_moment),('N',stress.composite_n),('Q',stress.composite_n1050),('P',stress.composite_n4125)]:
            other=fn(F,prime)
            if name=='M':other=other[0]
            checks['block_'+name]=bool(np.array_equal(other,b[name]))
            if not checks['block_'+name]:raise AssertionError('independent block differs: '+name)
        with ExitStack() as stack:
            for module in (pub8,pub10):
                stack.enter_context(patch.object(module,'five_form_moment',lambda *a:(b['M'],metric_axes(b['M'],(1,),prime))))
                stack.enter_context(patch.object(module,'composite_n1050',lambda *a:b['Q']))
                stack.enter_context(patch.object(module,'composite_n4125',lambda *a:b['P']))
            got8=pub8.evaluate_basis(F,prime);gotH=pub8.evaluate_alternative_basis(F,prime)
            got10=pub10.evaluate_implemented(F,prime)
            checks['primary8']=got8==v['primary8'];checks['hatted8']=gotH==v['hatted8']
            checks['degree10']=list(got10.values())==v['degree10']
            if not all(checks.values()):
                raise AssertionError({'checks':checks,'got8':got8,'gotH':gotH,'got10':got10,'oracle':v})
        times['independent_implementation_comparison']=time.monotonic()-t
    t=time.monotonic();defs=definitions();g={}
    for name,item in defs.items():
        g[name]=int(planned_value(graph_from_label(item['graph']),F,10,5,True,prime))
    times['graph_scalars']=time.monotonic()-t
    g8=[g[f'I8_{i}'] for i in range(1,7)]+[g['I4_1']**2%prime]
    g10=[g[f'I10_{i}'] for i in range(1,13)]+[g['I4_1']*g['I6_1']%prime,g['I4_1']*g['I6_2']%prime]
    selected8=v['primary8'][:5]+v['hatted8'][:1]+[g['I4_1']**2%prime]
    return {'prime':prime,'seed':seed,'coordinates':coords,'coordinate_convention':'F_[0ijkl], sorted spatial tuples; complement by F=*F, epsilon_0123456789=+1',
            'graphs':g,'atlas8':g8,'atlas10':g10,'selected8':selected8,**v,'implementation_checks':checks,'seconds':times,'total_seconds':time.monotonic()-start}


def main():
    parser=argparse.ArgumentParser();parser.add_argument('--prime',type=int,required=True)
    parser.add_argument('--seeds',type=int,nargs='+',required=True);parser.add_argument('--compare',action='store_true')
    args=parser.parse_args()
    directory=ROOT/'fresh-points';directory.mkdir(exist_ok=True)
    hashes={str(f.relative_to(ROOT.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in [ROOT/'source_scalar_oracle.py',Path(__file__),CHECKOUT/'src/sdinv/published_degree10_invariants.py',CHECKOUT/'src/sdinv/published_degree8_invariants.py',CHECKOUT/'src/sdinv/stress.py',CHECKOUT/'src/sdinv/contract.py',CHECKOUT/'src/sdinv/modp.py']}
    for seed in args.seeds:
        path=directory/f'p{args.prime}-s{seed}.json'
        if path.exists():raise FileExistsError('fresh point already exists: '+str(path))
        print('START',args.prime,seed,flush=True)
        data=point(args.prime,seed,args.compare);data['source_hashes']=hashes
        save(path,data)
        print('DONE',args.prime,seed,data['seconds'],flush=True)

if __name__=='__main__':main()
