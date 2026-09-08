#!/usr/bin/env python3
"""Compare new exact maps to frozen maps only after new computation completes."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib
from fit_fresh_maps import rank
ROOT=Path(__file__).resolve().parent
oldroot=ROOT.parent/'frozen-checkout/results'
new8=json.loads((ROOT/'order8_change_of_basis_exact.json').read_text());new10=json.loads((ROOT/'order10_change_of_basis_exact.json').read_text())
old8=json.loads((oldroot/'order8_change_of_basis.json').read_text());old10=json.loads((oldroot/'order10_change_of_basis.json').read_text())
parse=lambda a:[[F(x) for x in row] for row in a]
assert parse(old8['literature_to_graph'])==parse(new8['literature_to_graph'])
assert parse(old8['graph_to_literature'])==parse(new8['graph_to_literature'])
assert old10['graph_and_product_basis']==new10['graph_and_product_basis']
a,b=parse(new10['matrix_12x14']),parse(old10['matrix_12x14'])
diff=[[x-y for x,y in zip(u,v)] for u,v in zip(a,b)]
rows=[i+1 for i,row in enumerate(diff) if any(row)]
assert rows==[10,11,12],rows
result={'comparison_only':'No frozen coefficients were used to compute the new maps. This comparison occurred after independent exact evaluation solve.',
        'frozen_map_sha256':{str(d):hashlib.sha256((oldroot/f'order{d}_change_of_basis.json').read_bytes()).hexdigest() for d in [8,10]},
        'exact_map_sha256':{str(d):hashlib.sha256((ROOT/f'order{d}_change_of_basis_exact.json').read_bytes()).hexdigest() for d in [8,10]},
        'octic_forward_inverse_product_correction_unchanged':True,'degree10_changed_rows':rows,'difference_corrected_minus_legacy':[[str(x) for x in row] for row in diff],
        'degree10_difference_rank':rank(diff),'degree10_primitive_difference_rank':rank([row[:12] for row in diff]),
        'corrected_ranks':{k:new10[k] for k in ['published_span_rank','primitive_quotient_rank','union_rank','intersection_rank']}}
(ROOT/'exact-versus-frozen-comparison.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:v for k,v in result.items() if k!='difference_corrected_minus_legacy'},indent=2))
