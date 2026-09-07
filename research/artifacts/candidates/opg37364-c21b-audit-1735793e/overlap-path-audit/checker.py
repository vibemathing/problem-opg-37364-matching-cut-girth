"""Supplemental finite check: separate two shared edges from an actual shared path."""
from pathlib import Path
from itertools import product, permutations, combinations
import argparse, hashlib, importlib.util, json
p=argparse.ArgumentParser();p.add_argument('--input',required=True);p.add_argument('--mode',required=True)
a=p.parse_args();assert a.mode=='cycles'
cfg=json.loads(Path(a.input).read_text())
source=Path(__file__).resolve().parent/cfg['dependency']
assert hashlib.sha256(source.read_bytes()).hexdigest()==cfg['dependency_sha256']
spec=importlib.util.spec_from_file_location('frozen_checker',source)
base=importlib.util.module_from_spec(spec);spec.loader.exec_module(base)
def shared_path(edges,common):
    # Two distinct edge instances must use three distinct vertices.
    return any(len(set(edges[e])|set(edges[f]))==3 for e,f in combinations(common,2))
records={'tuples':0,'intersecting_pairs':0,'two_or_more_shared_edges':0,'actual_shared_path_pairs':0,
         'nonadjacent_only_shared_edge_pairs':0}
for N,q in cfg['models']:
    for tup in product(list(permutations(range(N))),repeat=q):
        es=base.edge_instances(tup,N);cs=base.cycles(2*N,es,4)
        records['tuples']+=1
        for i,j in combinations(range(len(cs)),2):
            vi=base.vertices_of(cs[i],es);vj=base.vertices_of(cs[j],es)
            if vi&vj:
                records['intersecting_pairs']+=1
                assert len(cs[i]|cs[j])>=len(vi|vj)+1
                common=cs[i]&cs[j]
                if len(common)>=2:
                    records['two_or_more_shared_edges']+=1
                    if shared_path(es,common): records['actual_shared_path_pairs']+=1
                    else: records['nonadjacent_only_shared_edge_pairs']+=1
# K2,3 is a theta graph: each pair of its three 4-cycles shares a 2-edge path.
theta=[(u,v) for u in [0,1] for v in [2,3,4]]
cs=base.cycles(5,theta,4);assert len(cs)==3
for i,j in combinations(range(3),2):
    common=cs[i]&cs[j]
    assert len(common)==2 and shared_path(theta,common)
    assert len(cs[i]|cs[j])==6 and len(base.vertices_of(cs[i]|cs[j],theta))==5
assert records['actual_shared_path_pairs']>0
assert records['two_or_more_shared_edges']==records['actual_shared_path_pairs']+records['nonadjacent_only_shared_edge_pairs']
records['explicit_theta_shared_path_pairs']=3
print(json.dumps({'format':'r10-c21b-supplemental-observation-v1','verdict':'candidate_only','status':'passed',
 'dependency_sha256':cfg['dependency_sha256'],'observations':records,
 'interpretation':'The original shared_path_pairs field counts >=2 common edges only. The new adjacent-edge test gives an actual common path with three distinct vertices.',
 'scope':'Finite representation and checker-label audit only; not a universal proof or original-C21B counterexample.'},indent=2,sort_keys=True))
