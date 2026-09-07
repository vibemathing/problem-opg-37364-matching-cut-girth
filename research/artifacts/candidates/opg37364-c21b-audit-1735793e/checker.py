"""Exact, bounded candidate self-checks for frozen R10 C20/C21B/C22.
No third-party packages; no network, randomness, subprocesses, or proof admission.
Run via bounded_runner.py; input selects finite test ranges, not the theorem domain.
"""
from __future__ import annotations
import argparse
from collections import Counter, deque
from fractions import Fraction as Q
from itertools import combinations, combinations_with_replacement, permutations, product
from math import comb, factorial
import json
from pathlib import Path


def require(ok: bool, label: str) -> None:
    if not ok:
        raise AssertionError(label)


def choose(n: int, k: int) -> int:
    return comb(n, k) if 0 <= k <= n else 0


def coefficients(N: int, a: int, b: int) -> list[int]:
    return [choose(a, j) * choose(N-a, b-j) * factorial(b) * factorial(N-b)
            for j in range(min(a, b)+1)]


def convolve(a: list[int], b: list[int]) -> list[int]:
    out = [0] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def tuple_counts(N: int, a: int, b: int, q: int) -> list[int]:
    c = coefficients(N, a, b)
    t = [1]
    for r in range(q):
        t = convolve(t, c)
        require(sum(t) == factorial(N)**(r+1), 'recurrence normalization')
    return t


def bad_count(N: int, a: int, b: int, q: int) -> int:
    threshold = ((q-2)*(a+b)+1)//2
    return sum(tuple_counts(N, a, b, q)[threshold:])


def incidence(N: int, q: int, doubled_diagonal: bool = False) -> int:
    require(q >= 3, 'positive-part incidence requires q>=3')
    return sum((2 if (a != b or doubled_diagonal) else 1)
               * choose(N, a) * choose(N, b) * bad_count(N, a, b, q)
               for a in range(1, N+1) for b in range(a, N+1) if a+b <= N)


def edge_instances(tup: tuple[tuple[int, ...], ...], N: int) -> list[tuple[int, int]]:
    return [(u, N+p[u]) for p in tup for u in range(N)]


def crossing(edges: list[tuple[int, int]] | set[tuple[int, int]], mask: int) -> int:
    return sum(((mask >> u) ^ (mask >> v)) & 1 for u, v in edges)


def matching_colouring(n: int, edges: list[tuple[int, int]] | set[tuple[int, int]],
                      mask: int, nonempty: bool = True) -> bool:
    if nonempty and (mask == 0 or mask == (1 << n)-1):
        return False
    used: set[int] = set()
    for u, v in edges:
        if ((mask >> u) ^ (mask >> v)) & 1:
            if u in used or v in used:
                return False
            used.update((u, v))
    return True


def cycles(n: int, edges: list[tuple[int, int]], cutoff: int) -> list[frozenset[int]]:
    """Unoriented simple cycles of edge instances, length 2..cutoff inclusive."""
    adj: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for e, (u, v) in enumerate(edges):
        require(u != v, 'loop-free input')
        adj[u].append((v, e)); adj[v].append((u, e))
    found: set[frozenset[int]] = set()
    def visit(start: int, u: int, vertices: set[int], es: tuple[int, ...]) -> None:
        for v, e in adj[u]:
            if e in es:
                continue
            if v == start:
                if 2 <= len(es)+1 <= cutoff:
                    found.add(frozenset(es+(e,)))
            elif v > start and v not in vertices and len(es)+1 < cutoff:
                visit(start, v, vertices | {v}, es+(e,))
    for start in range(n):
        visit(start, start, {start}, ())
    return sorted(found, key=lambda c: (len(c), sorted(c)))


def vertices_of(c: frozenset[int], edges: list[tuple[int, int]]) -> set[int]:
    return {v for e in c for v in edges[e]}


def distances(n: int, edges: set[tuple[int, int]]) -> list[list[int]]:
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    ds = []
    for s in range(n):
        d = [n+1]*n; d[s] = 0; todo = deque([s])
        while todo:
            u = todo.popleft()
            for v in adj[u]:
                if d[v] == n+1:
                    d[v] = d[u]+1; todo.append(v)
        ds.append(d)
    return ds


def girth(n: int, edges: set[tuple[int, int]]) -> int:
    """n+1 represents infinite girth for simple graphs."""
    best = n+1
    adj: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        adj[u].append(v); adj[v].append(u)
    for s in range(n):
        d = [-1]*n; par = [-1]*n; d[s] = 0; todo = deque([s])
        while todo:
            u = todo.popleft()
            for v in adj[u]:
                if d[v] < 0:
                    d[v] = d[u]+1; par[v] = u; todo.append(v)
                elif par[u] != v:
                    best = min(best, d[u]+d[v]+1)
    return best


def degs(n: int, edges: set[tuple[int, int]]) -> list[int]:
    d = [0]*n
    for u, v in edges:
        d[u] += 1; d[v] += 1
    return d


def connected_without(n: int, edges: set[tuple[int, int]], deleted: int = -1) -> bool:
    remaining = set(range(n)) - {deleted}
    if not remaining:
        return True
    seen = {min(remaining)}; todo = list(seen)
    adj = [set() for _ in range(n)]
    for u, v in edges:
        if deleted not in (u, v):
            adj[u].add(v); adj[v].add(u)
    while todo:
        u = todo.pop()
        for v in adj[u]-seen:
            seen.add(v); todo.append(v)
    return seen == remaining


def two_connected(n: int, edges: set[tuple[int, int]]) -> bool:
    return n >= 3 and connected_without(n, edges) and all(
        connected_without(n, edges, v) for v in range(n))


def edge(u: int, v: int) -> tuple[int, int]:
    require(u != v, 'new edge not loop')
    return (min(u, v), max(u, v))


def switch(n: int, J: set[tuple[int, int]], u: int, v: int,
           x: int, y: int, g: int) -> set[tuple[int, int]]:
    require(edge(x, y) in J, 'switch removes existing edge')
    require(girth(n, J) >= g, 'switch original girth')
    d = distances(n, J)
    require(all(d[a][b] >= g-1 for a in {u, v} for b in {x, y}), 'current distances')
    new = (J - {edge(x, y)}) | {edge(u, x), edge(v, y)}
    require(len(new) == len(J)+1, 'switch edge increment')
    before, after = degs(n, J), degs(n, new)
    require(all(after[i] == before[i] + (i == u) + (i == v) for i in range(n)),
            'switch degree increments')
    require(girth(n, new) >= g, 'switch preserved girth')
    return new


def run_arithmetic(cfg: dict) -> dict:
    pairs = 0; normalization_stages = 0; slot_cases = 0
    for N in range(1, cfg['coefficient_N_max']+1):
        ps = list(permutations(range(N))) if N <= cfg['enumerate_single_N_max'] else None
        for a in range(N+1):
            for b in range(N+1):
                c = coefficients(N, a, b)
                require(sum(c) == factorial(N), 'one-permutation normalization')
                require(c == coefficients(N, b, a), 'preimage symmetry')
                if ps is not None:
                    direct = Counter(sum(p[u] < b for u in range(a)) for p in ps)
                    require(c == [direct[j] for j in range(min(a,b)+1)], 'direct coefficient count')
                for q in cfg['recurrence_q']:
                    t = tuple_counts(N, a, b, q)
                    require(len(t) == q*min(a,b)+1, 'finite support')
                    normalization_stages += q
                pairs += 1
        for b in range(N+1):
            for k in range(N+1):
                prob = Q(factorial(b), factorial(b-k)) / Q(factorial(N), factorial(N-k)) if k <= b else Q(0)
                require(prob <= Q(b, N)**k, 'without-replacement domination')
                slot_cases += 1
    brute = []
    for N, q in cfg['tuple_models']:
        ps = list(permutations(range(N))); Z = factorial(N)**q
        masks = [s for s in range(1, 1 << (2*N)) if s.bit_count() <= N]
        actual_incidence = 0; actual_union = 0
        hist = {(a,b): Counter() for a in range(N+1) for b in range(N+1)}
        for tup in product(ps, repeat=q):
            es = edge_instances(tup, N); nb = 0
            for s in masks:
                if crossing(es, s) <= 2*s.bit_count():
                    nb += 1
            actual_incidence += nb; actual_union += nb > 0
            for a, b in hist:
                hist[a,b][sum(p[u] < b for p in tup for u in range(a))] += 1
        for (a,b), h in hist.items():
            t = tuple_counts(N, a, b, q)
            require(t == [h[x] for x in range(len(t))], 'direct full tuple recurrence')
        expected_incidence = incidence(N, q)
        require(actual_incidence == expected_incidence, 'all-shore incidence equality')
        require(actual_union <= actual_incidence, 'union bound direction')
        brute.append({'N':N,'q':q,'tuples':Z,'incidence':actual_incidence,'union':actual_union})
    q = 24; N = 2
    alpha = incidence(N, q); bcount = bad_count(N,1,1,q)
    require((bcount, alpha) == (301,1204), 'C22 reference values')
    weighted_inc = weighted_union = overlap_weight = 0
    for h in range(q+1):
        tup = ((0,1),)*h + ((1,0),)*(q-h)
        es = edge_instances(tup, N)
        nb = sum(crossing(es,s) <= 2*s.bit_count() for s in range(1,16) if s.bit_count() <= N)
        weight = comb(q,h)
        weighted_inc += weight*nb; weighted_union += weight*(nb>0)
        multiplicity = Counter(es)
        require(max(multiplicity.values()) >= 3, 'overlapping 2-cycles forced')
        overlap_weight += weight
    require((weighted_inc, weighted_union, overlap_weight) == (1204,602,2**24), 'N2 orbit aggregation')
    require(incidence(2,24,True) == 2408 != alpha, 'diagonal mutation detected')
    require(Q(1,3) != Q(2,3)**2, 'same-permutation independence mutation detected')
    bound = 69984*Q(13,24)**19
    require(bound < Q(2,3), 'exact large-shore constant')
    require(69984*Q(4,25)**6*Q(13,24) == Q(3726508032,5859375000), 'C20 rational intermediate')
    identities = 0
    for T in range(1,41):
        for x in [Q(0),Q(1,100),Q(1,4),Q(2,3),Q(5,6)]:
            s = sum(a*x**a for a in range(1,T+1))
            require((1-x)**2*s == x-(T+1)*x**(T+1)+T*x**(T+2), 'finite sum identity')
            require((1-x)**2*s <= x, 'finite sum bound')
            identities += 1
    M=1000; theta=69984*Q(2,M)**19
    small = 4*theta/(1-theta)**2; tail = 24*Q(5,6)**M
    require(small < Q(1,20) and tail < Q(1,1000), 'small/large shore bounds')
    require(Q(1,20)+Q(1,1000)+Q(1,4000) == Q(41,800) < 1, 'strict good-tuple margin')
    parameter_cases = 0
    for g in range(3,cfg['g_arithmetic_max']+1):
        K=2*g; C=K*K*(96*K*K)**K; B=1+62*sum(61**j for j in range(g-2)); M=4*C; N=M*M
        require(M%2==0 and M>=max(1000,K,5*B+1) and N>5*B and N>=2*K, 'size and parity')
        require(40*N == 10240*g**4*(384*g*g)**(4*g), 'exact order')
        require(69984*Q(2,M)**19 < Q(1,100) and Q(C,N) <= Q(1,4000), 'uniform size bound')
        parameter_cases += 1
    for n in range(2,102,2):
        for m in range(11*n, 12*n):
            t=19*n; ng=n+t; mg=m+2*t
            require(2*mg+2 <= 5*ng and Q(2*mg,ng)<5, 'integer density deficit')
        require(Q(2*(12*n+38*n),20*n) == 5, 'omit-deficit endpoint mutation')
    return {'coefficient_pairs':pairs,'normalization_stages':normalization_stages,'slot_cases':slot_cases,
            'brute_models':brute,'N2_q24':{'orbit_types':25,'Z':2**24,'fixed_bad_shore':bcount,
            'incidence':alpha,'bad_tuple_union':weighted_union,'overlap_union':overlap_weight},
            'large_shore_bracket':{'numerator':bound.numerator,'denominator':bound.denominator},
            'finite_sum_cases':identities,'parameter_cases':parameter_cases,
            'mutations_detected':['diagonal_weight_two','incidence_equals_union','independent_slots','omit_overlap','omit_strict_seed_deficit']}


def run_cycles(cfg: dict) -> dict:
    tuples=0; intersecting_pairs=0; shared_edge_pairs=0; shared_path_pairs=0; deletion_cases=0
    for N,q in cfg['overlap_models']:
        for tup in product(list(permutations(range(N))), repeat=q):
            es=edge_instances(tup,N); cs=cycles(2*N,es,4); cvs=[vertices_of(c,es) for c in cs]
            overlap=False
            for i,j in combinations(range(len(cs)),2):
                if cvs[i] & cvs[j]:
                    overlap=True; union=cs[i]|cs[j]; vs=cvs[i]|cvs[j]
                    require(len(union)>=len(vs)+1, 'two distinct cycles excess')
                    require(len(union)<=10 and len(vs)<=10, 'K=2g catalogue bounds at g5')
                    intersecting_pairs += 1
                    if cs[i]&cs[j]: shared_edge_pairs += 1
                    if len(cs[i]&cs[j])>=2: shared_path_pairs += 1
            if not overlap:
                deleted={min(c) for c in cs}
                flat=[v for e in deleted for v in es[e]]
                require(len(flat)==len(set(flat)), 'short-cycle deletion is matching')
                kept=[e for i,e in enumerate(es) if i not in deleted]
                require(len(kept)==len(set(kept)), 'simplification removes parallels')
                require(not cycles(2*N,kept,4), 'all short cycles hit')
                for s in range(1,1<<(2*N)):
                    require(crossing(es,s)-crossing(kept,s)<=min(s.bit_count(),2*N-s.bit_count()), 'deleted crossing bound')
                deletion_cases += 1
            tuples += 1
    require(shared_edge_pairs>0 and shared_path_pairs>0, 'nonvacuous shared-path coverage')
    # Compatible and incompatible partial permutation patterns, counted directly.
    constraints=0
    for N in range(1,5):
        ps=list(permutations(range(N))); possible=list(product(range(N),repeat=2))
        for ecount in range(min(3,N)+1):
            for pairs in combinations(possible,ecount):
                compatible=len({u for u,v in pairs})==len(pairs)==len({v for u,v in pairs})
                expected=factorial(N-ecount) if compatible else 0
                actual=sum(all(p[u]==v for u,v in pairs) for p in ps)
                require(actual==expected,'partial permutation extension count')
                constraints += 1
    # Two four-cycles share just one vertex; a three-parallel-edge example shares edges.
    butterfly=[(0,3),(1,3),(1,4),(0,4),(0,5),(2,5),(2,6),(0,6)]
    cs=cycles(7,butterfly,4)
    require(len(cs)==2 and len(vertices_of(cs[0],butterfly)&vertices_of(cs[1],butterfly))==1,'shared-vertex control')
    require(len(cs[0]|cs[1])==8 and len(set(sum(([u,v] for u,v in butterfly),[])))==7, 'butterfly excess')
    parallel=[(0,1)]*3; cs=cycles(2,parallel,2)
    require(len(cs)==3, 'parallel 2-cycle identity')
    require(not matching_colouring(2,parallel,1) and matching_colouring(2,set(parallel),1), 'edge-instance mutation')
    require(len(cycles(4,[(0,1),(1,2),(2,3),(0,3)],4))==1, 'rotation/reversal not distinct cycles')
    require(crossing(parallel,1)-crossing(parallel[2:],1)==2>1,'nonmatching deletion mutation')
    # Positive short-cycle deletion control with nonempty deletion set.
    es=[(0,1),(0,1),(2,3),(3,4),(4,5),(2,5)]
    cs=cycles(6,es,4); deleted={min(c) for c in cs}; flat=[v for e in deleted for v in es[e]]
    require(len(deleted)==2 and len(flat)==len(set(flat)),'nonvacuous matching deletion')
    require(not cycles(6,[e for i,e in enumerate(es) if i not in deleted],4),'positive deletion girth')
    # A small positive all-cut seed, not a degree24 or arbitrary-girth witness.
    N=6; es={(u,N+v) for u in range(N) for v in range(N)}
    require(all(crossing(es,s)>2*s.bit_count() for s in range(1,1<<12) if s.bit_count()<=6),'K6,6 positive expansion')
    hp=es-{(0,6)}
    require(two_connected(12,hp),'extra-deletion positive two-connectivity')
    require(all(not matching_colouring(12,hp,s) for s in range(1,1<<12)),'extra-deletion no MC')
    require(all(crossing(hp,s)>=s.bit_count()+1 for s in range(1,1<<12) if s.bit_count()<=6),'extra-deletion cut margin')
    return {'tuples':tuples,'intersecting_cycle_pairs':intersecting_pairs,'shared_edge_pairs':shared_edge_pairs,
            'shared_path_pairs':shared_path_pairs,'disjoint_cycle_tuple_controls':deletion_cases,
            'partial_permutation_constraints':constraints,'positive_seed':'K6,6 minus one edge; g=3 control only',
            'mutations_detected':['drop_parallel_2_cycles','merge_edge_instances','duplicate_cycle_orientations','unbounded_deletion_degree']}


def run_graphs(cfg: dict) -> dict:
    local_graphs=0; switches=0; coincident=0
    for n in range(2,cfg['switch_graph_order_max']+1):
        pairs=list(combinations(range(n),2))
        for bits in range(1<<len(pairs)):
            J={p for i,p in enumerate(pairs) if bits>>i&1}; h=girth(n,J); ds=distances(n,J)
            for g in range(3,min(h,5)+1):
                for u,v in combinations_with_replacement(range(n),2):
                    for x,y in J:
                        if all(ds[a][b]>=g-1 for a in {u,v} for b in {x,y}):
                            switch(n,J,u,v,x,y,g); switches+=1; coincident+=u==v
            local_graphs += 1
    require(switches>0 and coincident>0,'nonvacuous local exchanges')
    # All hypotheses of B1 including N>5B; inclusion-maximal is not maximum.
    N=52; n=2*N; k=1; r=2; g=4; B=1+(r+k)*sum((r+k-1)**j for j in range(g-2))
    H={(0,N),(1,N)}
    F={edge(i,i+1) for i in range(2,N,2)} | {edge(i,i+1) for i in range(N,n,2)}
    require(N>5*B and (k*N)%2==0 and girth(n,H|F)>=g,'maximum-not-maximal fixture hypotheses')
    d=degs(n,F); ds=distances(n,H|F)
    legal=[(u,v) for P in (range(N),range(N,n)) for u,v in combinations(P,2)
           if d[u]<k and d[v]<k and ds[u][v]>=g-1]
    require(not legal and ds[0][1]==2,'inclusion maximal unsaturated fixture')
    Jnew=switch(n,H|F,0,1,2,3,g); Fnew=Jnew-H
    require(all(x==k for x in degs(n,Fnew)),'larger fully regular augmentation')
    # Coincident deficits at one vertex; all B1 size/parity assumptions hold.
    N=36; n=72; k=2; r=0; g=5; B=7
    F={edge(i,1+(i%35)) for i in range(1,36)} | {edge(i,36+(i-36+1)%36) for i in range(36,72)}
    require(N>5*B and (k*N)%2==0 and degs(n,F)[0]==0,'coincident fixture hypotheses')
    Fnew=switch(n,F,0,0,1,2,g)
    require(all(x==2 for x in degs(n,Fnew)),'coincident deficits filled')
    # Explicit cycles realizing each of the two path pairings, plus u=v.
    # Pairing one: old u-v edge and a separate five-cycle containing x-y.
    J={(0,1),(2,3),(3,4),(4,5),(5,6),(2,6)}
    Jnew=switch(7,J,0,1,2,3,5)
    require(girth(7,Jnew)==7,'pairing u-v / x-y')
    # Pairing two: paths u--y and v--x, joined by xy before the switch.
    J={edge(i,i+1) for i in range(9)}
    # u=0,y=4,x=5,v=9, both far paths have four edges.
    Jnew=switch(10,J,0,9,5,4,5)
    require(girth(10,Jnew)==10,'crossed pairing')
    # Current-distance mutation: distances in empty H would falsely license a triangle.
    J={(0,1),(1,2),(2,3)}
    mutated=(J-{(2,3)})|{(0,2),(3,4)}
    require(girth(5,J)==6 and girth(5,mutated)==3,'stale-distance mutation')
    require(11>5*2 and 11%2==1 and 2*(11//2)<11,'parity mutation')
    # Subdivide every subset of same-part artificial pairs of the immune K2,3 core.
    H={(u,v) for u in range(2) for v in range(2,5)}; pairs=[(0,1),(2,3),(2,4),(3,4)]
    subdivisions=0; colourings=0; old_split=0; old_mono=0
    require(two_connected(5,H),'control core two-connected')
    require(all(not matching_colouring(5,H,s) for s in range(1,31)), 'control core immune')
    for bits in range(16):
        F={p for i,p in enumerate(pairs) if bits>>i&1}; J=H|F; G=set(H); labels=[0,0,1,1,1]
        for u,v in sorted(F):
            w=len(labels); labels.append(1-labels[u]); G|={edge(u,w),edge(v,w)}
        n=len(labels)
        require(all(labels[u]!=labels[v] for u,v in G),'subdivision bipartition')
        require(two_connected(n,G),'subdivision two-connectivity')
        require(girth(n,G)>=girth(5,J),'subdivision girth projection')
        require(len(G)==len(H)+2*len(F) and n==5+len(F),'subdivision counts')
        for s in range(1,(1<<n)-1):
            valid=matching_colouring(n,G,s)
            require(not valid,'subdivision no MC')
            if s&31 not in (0,31):
                require(not matching_colouring(5,H,s&31),'old-split restriction rejects')
                old_split += 1
            else:
                old_mono += 1
            colourings += 1
        subdivisions += 1
    # Two subdivisions on an artificial pair always permit the two-new-vertex shore.
    G=set(H)|{(0,5),(5,6),(1,6)}
    require(matching_colouring(7,G,(1<<5)|(1<<6)), 'two-new-vertex mutation')
    require(matching_colouring(2,set(),1),'empty crossing accepted')
    require(not matching_colouring(1,set(),0) and not matching_colouring(1,set(),1),'K1 rejected')
    return {'local_graphs':local_graphs,'local_switches':switches,'coincident_switches':coincident,
            'global_size_controls':[{'r':2,'k':1,'g':4,'N':52,'B':10},{'r':0,'k':2,'g':5,'N':36,'B':7}],
            'pairing_cycle_lengths':[7,10],'subdivision_graphs':subdivisions,'colourings':colourings,
            'old_split_cases':old_split,'old_monochromatic_cases':old_mono,
            'mutations_detected':['inclusion_maximum_confusion','stale_H_distance','missing_parity','subdivide_artificial_twice','empty_shore_allowed']}


def main() -> None:
    parser=argparse.ArgumentParser(); parser.add_argument('--input',required=True); parser.add_argument('--mode',choices=['smoke','arithmetic','cycles','graphs'],required=True)
    args=parser.parse_args(); cfg=json.loads(Path(args.input).read_text())
    require(cfg['format']=='r10-c21b-finite-tests-v1','input format')
    if args.mode=='smoke':
        require(coefficients(2,1,1)==[1,1],'smoke exact coefficient')
        require(girth(3,{(0,1),(1,2),(0,2)})==3,'smoke girth')
        require(len(cycles(2,[(0,1),(0,1)],2))==1,'smoke parallel cycle')
        result={'smoke':'passed','arithmetic':'exact Python int and Fraction','third_party_packages':[]}
    else:
        result={'arithmetic':run_arithmetic,'cycles':run_cycles,'graphs':run_graphs}[args.mode](cfg)
    print(json.dumps({'format':'r10-c21b-bounded-observation-v1','verdict':'candidate_only','mode':args.mode,
          'status':'passed','scope':'Only the explicitly selected finite models and synthetic controls; not a universal proof or trusted verifier receipt.',
          'observations':result},sort_keys=True,indent=2))

if __name__=='__main__':
    main()
