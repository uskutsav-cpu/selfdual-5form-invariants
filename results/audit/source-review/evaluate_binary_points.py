#!/usr/bin/env python3
"""Common integral binary points: exact CRT evidence, not reused dense points."""
import argparse,hashlib,json,time,sys
from pathlib import Path
import numpy as np
from source_scalar_oracle import blocks,source_values,form_from_coordinates
from evaluate_fresh_points import definitions,CHECKOUT,planned_value,graph_from_label,save
ROOT=Path(__file__).resolve().parent

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--primes',type=int,nargs='+',required=True)
    ap.add_argument('--seeds',type=int,nargs='+',required=True);args=ap.parse_args()
    directory=ROOT/'binary-points';directory.mkdir(exist_ok=True)
    files=[ROOT/'source_scalar_oracle.py',ROOT/'evaluate_fresh_points.py',Path(__file__),CHECKOUT/'src/sdinv/contract.py',CHECKOUT/'src/sdinv/modp.py',CHECKOUT/'src/sdinv/graphs.py']
    hashes={str(f.relative_to(ROOT.parent)):hashlib.sha256(f.read_bytes()).hexdigest() for f in files}
    defs=definitions()
    definitions_hash=hashlib.sha256(json.dumps(defs,sort_keys=True,separators=(',',':')).encode()).hexdigest()
    for p in args.primes:
        for seed in args.seeds:
            path=directory/f'p{p}-s{seed}.json'
            if path.exists():raise FileExistsError(path)
            started=time.monotonic();coords=np.random.default_rng(seed).integers(0,2,size=126).tolist()
            print('START binary',p,seed,flush=True)
            F=form_from_coordinates(coords,p);b=blocks(F,p);v=source_values(b,p)
            g={name:int(planned_value(graph_from_label(item['graph']),F,10,5,True,p)) for name,item in defs.items()}
            atlas8=[g[f'I8_{i}'] for i in range(1,7)]+[g['I4_1']**2%p]
            atlas10=[g[f'I10_{i}'] for i in range(1,13)]+[g['I4_1']*g['I6_1']%p,g['I4_1']*g['I6_2']%p]
            data={'prime':p,'seed':seed,'coordinates':coords,'coordinate_convention':'F_[0ijkl], sorted spatial tuples, common binary integers across primes; complement from F=*F; epsilon_0123456789=+1',
                  'atlas8':atlas8,'atlas10':atlas10,'selected8':v['primary8'][:5]+v['hatted8'][:1]+[g['I4_1']**2%p],**v,
                  'source_hashes':hashes,'definitions_sha256':definitions_hash,'seconds':time.monotonic()-started}
            save(path,data);print('DONE binary',p,seed,data['seconds'],flush=True)
if __name__=='__main__':main()
