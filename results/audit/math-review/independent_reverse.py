"""Independent reverse adjoints over the separately authored forward engine.

This module never imports production code, its projection, its tree planner,
or its rank routine. It uses a fresh opt_einsum path and our guarded binary
dot kernel. Repeated tensor copies are kept as distinct leaves in the tape;
their adjoints are added only when pulling back to the common input form.
"""
import itertools
import numpy as np

from independent_conventions import COORDINATES, POSITIONS, TUPLES, star_image, parity
from independent_oracle import terms, plan, modular_dot


def sparse_coordinate_pullback():
    indices, signs = [], []
    for k in COORDINATES:
        pair, pair_sign = star_image(TUPLES[k])
        column_indices, column_signs = [], []
        for sorted_indices, sign in [(TUPLES[k],1),(pair,pair_sign)]:
            for permuted in itertools.permutations(sorted_indices):
                flat=0
                for i in permuted:
                    flat=10*flat+i
                column_indices.append(flat)
                column_signs.append(sign*parity(permuted))
        indices.append(column_indices)
        signs.append(column_signs)
    return np.array(indices,dtype=np.int64),np.array(signs,dtype=np.int64)


PULLBACK_INDICES,PULLBACK_SIGNS=sparse_coordinate_pullback()


def reverse_gradient(engine,item,selected_plan=None):
    assert not engine.dual
    selected_plan=selected_plan or plan(item)
    labels,raised=terms(item)
    nodes=[]
    active=[]
    for group,variance in zip(labels,raised):
        identity,arrays=engine.initial(variance)
        nodes.append({"operand":(group,identity,arrays),"variance":variance})
        active.append(len(nodes)-1)
    for i,j in selected_plan["path"]:
        left,right=active[i],active[j]
        combined=engine.contract_pair(nodes[left]["operand"],nodes[right]["operand"])
        nodes.append({"operand":combined,"left":left,"right":right})
        for k in sorted([i,j],reverse=True):active.pop(k)
        active.append(len(nodes)-1)
    assert len(active)==1
    p=engine.prime
    adjoints={active[0]:np.array(1.0)}
    for index in range(len(nodes)-1,len(raised)-1,-1):
        node=nodes[index]
        la,_,aa=nodes[node["left"]]["operand"]
        lb,_,bb=nodes[node["right"]]["operand"]
        common=[label for label in la if label in lb]
        free_a=[label for label in la if label not in common]
        free_b=[label for label in lb if label not in common]
        oa=[la.index(label) for label in free_a+common]
        ob=[lb.index(label) for label in common+free_b]
        a=aa[0].transpose(oa).reshape(10**len(free_a),10**len(common))
        b=bb[0].transpose(ob).reshape(10**len(common),10**len(free_b))
        c=adjoints.pop(index).reshape(10**len(free_a),10**len(free_b))
        da=modular_dot(c,b.T,p,engine.stats).reshape((10,)*len(la)).transpose(np.argsort(oa))
        db=modular_dot(a.T,c,p,engine.stats).reshape((10,)*len(lb)).transpose(np.argsort(ob))
        # A contraction tree has each occurrence exactly once, even when the
        # forward cache happened to reuse an equal array at multiple nodes.
        assert node["left"] not in adjoints and node["right"] not in adjoints
        adjoints[node["left"]]=da
        adjoints[node["right"]]=db
    gradient=np.zeros((10,)*5,dtype=np.float64)
    metric=np.array([-1]+[1]*9,dtype=np.float64)
    for leaf,variance in enumerate(raised):
        g=adjoints[leaf]
        for axis,flag in enumerate(variance):
            if flag:
                shape=[1]*5
                shape[axis]=10
                g=np.remainder(g*metric.reshape(shape),p)
        gradient=np.remainder(gradient+g,p)
    compact=(gradient.ravel()[PULLBACK_INDICES].astype(np.int64)*PULLBACK_SIGNS).sum(axis=1)%p
    scalar=int(nodes[-1]["operand"][2][0])
    return scalar,[int(x) for x in compact]
