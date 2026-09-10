"""Independent all-covariant transcription of arXiv:2509.14350v2.

No sdinv imports: signs, projectors, source words and binary contractions are
implemented here. Inputs are reduced after every binary contraction; float64
BLAS is used only when a nonnegative-integer dot product is provably <2**53.
The manually frozen pre-code source transcription is the formula authority.
"""
from functools import lru_cache
from itertools import permutations, combinations
from math import factorial, prod
import numpy as np
import opt_einsum as oe


def sign(order):
    return -1 if sum(a > b for i, a in enumerate(order) for b in order[i+1:]) % 2 else 1


def bracket(a, slots, p, antisym=True):
    out = np.zeros_like(a)
    for perm in permutations(slots):
        axes = list(range(a.ndim))
        for dest, src in zip(slots, perm): axes[dest] = src
        factor = sign(tuple(slots.index(x) for x in perm)) if antisym else 1
        out = (out + factor * a.transpose(axes)) % p
    return out * pow(factorial(len(slots)), -1, p) % p


def metric_axes(a, axes, p):
    out = a.copy()
    for axis in axes:
        sl = [slice(None)] * a.ndim; sl[axis] = 0
        out[tuple(sl)] = -out[tuple(sl)] % p
    return out


@lru_cache(maxsize=None)
def path_for(words, shapes, output):
    return tuple(oe.contract_path(words+'->'+output, *shapes, shapes=True, optimize='optimal')[0])


def contract(words, operands, p, output=''):
    terms = words.split(',')
    operands = [np.asarray(a, dtype=np.int64) % p for a in operands]
    # Every source dummy edge is explicitly contracted with exactly one metric.
    seen = set()
    for k, term in enumerate(terms):
        assert len(set(term)) == len(term), (words, term)
        operands[k] = metric_axes(operands[k], [i for i, c in enumerate(term) if c in seen], p)
        seen.update(term)
    dims = {c:n for term,a in zip(terms,operands) for c,n in zip(term,a.shape)}
    for contraction in path_for(words, tuple(a.shape for a in operands), output):
        assert len(contraction) == 2
        i,j = contraction
        rest = set(''.join(t for k,t in enumerate(terms) if k not in (i,j))) | set(output)
        joined = ''.join(dict.fromkeys(terms[i]+terms[j]))
        keep = ''.join(c for c in joined if c in rest)
        summed = prod(dims[c] for c in joined if c not in keep)
        bound = (p-1)**2 * summed
        if bound >= 2**63: raise OverflowError((words,bound))
        sub = terms[i]+','+terms[j]+'->'+keep
        work = prod(dims[c] for c in joined)
        if work >= 1_000_000 and bound < 2**53:
            raw = np.einsum(sub, operands[i].astype(float), operands[j].astype(float), optimize=True)
            a = np.rint(raw).astype(np.int64) % p
        else:
            a = np.einsum(sub, operands[i], operands[j], optimize=True) % p
        for k in sorted((i,j),reverse=True):
            terms.pop(k);operands.pop(k)
        terms.append(keep);operands.append(a)
    if terms[0] != output:
        operands[0] = np.einsum(terms[0]+'->'+output,operands[0]) % p
    return operands[0]


def form_from_coordinates(coords, p):
    """F_[0ijkl] are 126 free coordinates; complement fixed by F=*F."""
    F = np.zeros((10,)*5, dtype=np.int64)
    perm5 = [(v,sign(v)) for v in permutations(range(5))]
    for value,spatial in zip(coords,combinations(range(1,10),4)):
        I=(0,)+spatial; J=tuple(x for x in range(10) if x not in I)
        for base,x in ((I,int(value)%p),(J,sign(I+J)*int(value)%p)):
            for perm,sgn in perm5:
                F[tuple(base[k] for k in perm)] = sgn*x % p
    return F


def blocks(F,p):
    M = contract('aijkl,bijkl',[F,F],p,output='ab')
    N = contract('abcij,defij',[F,F],p,output='abcdef')
    # N is already antisymmetric in abc and de. The normalized first-five
    # projector is therefore the average over the ten (3,2) shuffles.
    Q=np.zeros_like(N)
    for head in combinations(range(5),3):
        tail=tuple(i for i in range(5) if i not in head)
        axes=head+tail+(5,)
        Q=(Q+sign(axes)*N.transpose(tuple(np.argsort(axes))))%p
    Q=Q*pow(10,-1,p)%p
    T=bracket(Q,(3,4,5),p)
    eta=np.diag([-1]+[1]*9).astype(np.int64)
    trace=np.einsum('ad,be,cf->abcdef',eta,eta,M)%p
    trace=bracket(bracket(trace,(0,1,2),p),(3,4,5),p)
    P=(N-5*T-(9*pow(28,-1,p)%p)*trace)%p
    return {'M':M,'N':N,'Q':Q,'T':T,'P':P}


def source_values(b,p):
    M,Q,T,P=b['M'],b['Q'],b['T'],b['P']
    C=lambda w,*a,output='':contract(w,a,p,output)
    M2=C('ac,cb',M,M,output='ab')
    mixed=metric_axes(M,(1,),p)
    acc=np.eye(len(M),dtype=np.int64);traces={}
    for k in range(1,6):
        acc=acc@mixed%p;traces[k]=int(np.trace(acc)%p)
    q=C('abcdmn,abcdrl',Q,Q,output='mnrl')
    sym=bracket(q,(0,1,2,3),p,antisym=False)
    mouter=np.einsum('ia,jb->iajb',M,M)%p
    wedge=bracket(bracket(mouter,(0,2),p),(1,3),p)
    i8=[traces[4],C('ai,bj,ck,ijkabc',M,M,M,P),C('ab,abcd,cd',M,q,M),
        C('abcd,abcd',sym,q),C('iajb,abij',wedge,q),C('ia,jb,abrstu,rstuij',M,M,Q,P)]
    hwords=['abcdrs,abcduv,urlmno,slmvno','abcdrs,abcduv,rlmuno,slnmov',
            'abcrst,abcuvw,rslmnu,tvmlnw','abcrst,abcuvw,urls mn,tvmwln'.replace(' ',''),
            'urabcd,sabvcd,sulmno,vlmrno']
    h8=[int(C(w,T,T,T,T)) for w in hwords];h8[0]=-h8[0]%p;h8.append(int(i8[1]))
    wedge2=bracket(bracket(np.einsum('ia,jb->iajb',M2,M)%p,(0,2),p),(1,3),p)
    split=bracket(np.einsum('vw,ab->vwab',M,M)%p,(0,2),p)
    j9=C('knrl,km',q,M,output='nmrl'); j9=bracket(j9,(0,2,3),p,antisym=False)
    B=bracket(Q,(4,5),p)
    i10=[traces[5],C('ai,bj,ck,ijkabc',M2,M,M,P),
         C('ai,bj,ck,abcdef,ijkdef',M,M,M,Q,Q),
         C('ab,cd,abcd',M2,M,sym),C('iajb,abij',wedge2,q),
         C('ia,jb,abrstu,rstuij',M2,M,Q,P),
         C('rstuva,ab,rstcde,uvbced',Q,M2,Q,Q),
         C('rstuva,vwab,rstcde,uwbced',Q,split,Q,Q),
         C('nmrl,mnrl',j9,q),
         C('abcdmn,abcxyz,dpqxzy,efghpq,efghmn',B,Q,Q,Q,Q),
         C('rstabc,defabc,defijk,rslmni,tjmlnk',Q,Q,T,T,T),
         C('rstabc,defabc,defijk,irlsmn,tjmkln',Q,Q,T,T,T)]
    return {'primary8':list(map(int,i8)),'hatted8':h8,'degree10':list(map(int,i10)),
            'traces':traces,'source_product8':traces[2]**2%p}
