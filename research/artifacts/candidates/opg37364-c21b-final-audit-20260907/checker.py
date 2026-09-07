"""Second generator-owned C21B audit. Exact finite controls, not a verifier."""
from __future__ import annotations
import argparse, itertools as it, json, math
from collections import Counter, deque
from fractions import Fraction as Q
from pathlib import Path

TESTS = 0

def check(p: bool, label: str) -> None:
    global TESTS
    TESTS += 1
    if not p:
        raise AssertionError(label)

def choose(n: int, k: int) -> int:
    return math.comb(n, k) if 0 <= k <= n else 0

def fall(n: int, k: int) -> int:
    return math.prod(range(n-k+1, n+1)) if k <= n else 0

def coeff(n: int, a: int, b: int) -> list[int]:
    # Image-set enumeration, dual to the archived preimage formula.
    return [choose(b,j)*choose(n-b,a-j)*math.factorial(a)*math.factorial(n-a)
            for j in range(min(a,b)+1)]

def power(c: list[int], q: int) -> list[int]:
    a = [1]
    for r in range(q):
        b = [0]*(len(a)+len(c)-1)
        for i,x in enumerate(a):
            for j,y in enumerate(c): b[i+j] += x*y
        a = b
        check(sum(a)==sum(c)**(r+1), 'convolution normalization')
    return a

def edges_of(tup: tuple[tuple[int,...],...], n: int) -> list[tuple[int,int]]:
    return [(u,n+p[u]) for p in tup for u in range(n)]

def boundary(edges: list[tuple[int,int]], mask: int) -> int:
    return sum(((mask>>u)^(mask>>v))&1 for u,v in edges)

def adj(n: int, edges) -> list[set[int]]:
    a=[set() for _ in range(n)]
    for u,v in edges: a[u].add(v);a[v].add(u)
    return a

def distance(n: int, edges, s: int, t: int):
    a=adj(n,edges);d={s:0};queue=deque([s])
    while queue:
        u=queue.popleft()
        if u==t:return d[u]
        for v in a[u]:
            if v not in d:d[v]=d[u]+1;queue.append(v)
    return math.inf

def girth(n: int, edges):
    es=set(tuple(sorted(e)) for e in edges)
    return min((1+distance(n,es-{(u,v)},u,v) for u,v in es), default=math.inf)

def connected(n: int, edges, deleted=None) -> bool:
    alive=set(range(n))-{deleted}
    if not alive:return False
    a=adj(n,edges);s=next(iter(alive));seen={s};queue=[s]
    for u in queue:
        for v in a[u]&alive:
            if v not in seen:seen.add(v);queue.append(v)
    return seen==alive

def two_connected(n: int, edges) -> bool:
    return n>=3 and connected(n,edges) and all(connected(n,edges,x) for x in range(n))

def mc(n: int, edges, mask: int, nonempty=True) -> bool:
    if nonempty and mask in (0,(1<<n)-1):return False
    used=set()
    for u,v in edges:
        if ((mask>>u)^(mask>>v))&1:
            if u in used or v in used:return False
            used.update((u,v))
    return True

def has_mc(n: int, edges) -> bool:
    return any(mc(n,edges,s) for s in range(1,(1<<n)-1))

def instance_cycles(edges: list[tuple[int,int]], g: int):
    # Enumerate connected 2-regular edge-instance subsets, not oriented walks.
    out=[]
    for k in range(2,min(g,len(edges)+1)):
        for ids in it.combinations(range(len(edges)),k):
            deg=Counter(v for i in ids for v in edges[i])
            if any(x!=2 for x in deg.values()):continue
            es=[edges[i] for i in ids];a={v:set() for v in deg}
            for u,v in es:a[u].add(v);a[v].add(u)
            seen={next(iter(a))};queue=list(seen)
            for u in queue:
                for v in a[u]:
                    if v not in seen:seen.add(v);queue.append(v)
            if len(seen)==len(a):out.append((frozenset(ids),frozenset(seen)))
    return out

def arithmetic(nmax: int):
    coefficient_cases=tuple_cases=0
    for n in range(1,nmax+1):
        perms=list(it.permutations(range(n)))
        for a in range(n+1):
            for b in range(n+1):
                c=coeff(n,a,b)
                observed=Counter(sum(p[u]<b for u in range(a)) for p in perms)
                check(c==[observed[j] for j in range(len(c))], 'image-set count')
                check(c==coeff(n,b,a),'inversion symmetry')
                check(c==[choose(a,j)*choose(n-a,b-j)*math.factorial(b)*math.factorial(n-b)
                          for j in range(len(c))], 'preimage bridge')
                check(sum(c)==math.factorial(n),'coefficient mass')
                for q in (1,2,3,24):power(c,q)
                coefficient_cases+=1
        if n<=3:
            for q in (1,2,3):
                incidence=union=0
                for tup in it.product(perms,repeat=q):
                    es=edges_of(tup,n);count=0
                    for s in range(1,1<<(2*n)):
                        if s.bit_count()<=n and boundary(es,s)<=2*s.bit_count():count+=1
                    incidence+=count;union+=bool(count);tuple_cases+=1
                formula=0
                # General-q test includes single-part shores when q<=2.
                for a in range(n+1):
                    for b in range(n+1):
                        if not 1<=a+b<=n:continue
                        counts=power(coeff(n,a,b),q)
                        bad=sum(x for t,x in enumerate(counts) if q*(a+b)-2*t<=2*(a+b))
                        formula+=choose(n,a)*choose(n,b)*bad
                check(formula==incidence,'all-shore incidence equality')
                check(union<=incidence,'projection inequality')
    for n in range(1,13):
        for b in range(n+1):
            for k in range(n+1):
                check(fall(b,k)*n**k<=b**k*fall(n,k),'without replacement')
    fixed=sum(choose(24,j) for j in range(22,25));incidence=4*fixed
    union=sum(choose(24,j) for j in range(25) if j<=2 or j>=22)
    check((fixed,incidence,union)==(301,1204,602),'N2 q24 exact aggregation')
    check(Q(69984)*Q(13,24)**19<Q(2,3),'uniform bracket')
    check(Q(69984)*Q(4,25)**6*Q(13,24)==Q(3726508032,5859375000),'rational witness')
    for m in (1000,1001,1002,2000):
        theta=Q(69984)*Q(2,m)**19
        check(theta<Q(1,100),'small bracket')
        check(4*theta/(1-theta)**2<Q(1,20),'small-shore sum')
        check(24*Q(5,6)**m<Q(1,1000),'large-shore tail')
    for t in range(1,41):
        for x in (Q(0),Q(1,100),Q(2,3),Q(5,6)):
            s=sum((a*x**a for a in range(1,t+1)),Q(0))
            check((1-x)**2*s==x-(t+1)*x**(t+1)+t*x**(t+2),'finite sum')
    check(Q(1,20)+Q(1,1000)+Q(1,4000)==Q(41,800)<1,'strict good count')
    for g in range(3,21):
        k=2*g;c=k*k*(96*k*k)**k;m=4*c;b=1+62*sum(61**j for j in range(g-2))
        check(m>=max(1000,k,5*b+1) and m%2==0,'explicit size and parity')
        check(40*m*m==10240*g**4*(384*g*g)**(4*g),'prescribed order')
    return dict(coefficient_cases=coefficient_cases,enumerated_tuples=tuple_cases,
                q24_N2=dict(fixed_shore=fixed,incidences=incidence,bad_union=union),
                strict_failure_bound='41/800')

def patterns():
    n=3;q=2;perms=list(it.permutations(range(n)));tuples=list(it.product(perms,repeat=q))
    universe=list(it.product(range(q),range(n),range(n)));tested=0
    for e in range(4):
        for pat in it.combinations(universe,e):
            counts=[];compatible=True
            for color in range(q):
                pairs=[(u,v) for c,u,v in pat if c==color];counts.append(len(pairs))
                compatible &= len({u for u,v in pairs})==len(pairs)==len({v for u,v in pairs})
            expected=math.prod(math.factorial(n-x) for x in counts) if compatible else 0
            actual=sum(all(t[c][u]==v for c,u,v in pat) for t in tuples)
            check(actual==expected,'coloured partial-bijection extension');tested+=1
    pairs=shared_edges=shared_paths=0
    tuple_count=0
    for n,q in ((1,3),(2,3),(2,4),(3,3)):
        perms=list(it.permutations(range(n)))
        for tup in it.product(perms,repeat=q):
            tuple_count+=1;es=edges_of(tup,n);cs=instance_cycles(es,5)
            for (a,av),(b,bv) in it.combinations(cs,2):
                if not av&bv:continue
                check(len(a|b)>=len(av|bv)+1,'two-cycle excess including common edges')
                check(len(a|b)<=10 and len(av|bv)<=10,'catalogue size')
                common=a&b;pairs+=1;shared_edges+=bool(common)
                path=any(set(es[i])&set(es[j]) for i,j in it.combinations(common,2))
                shared_paths+=bool(path)
    check(shared_edges>0 and shared_paths>0,'nonvacuous shared-path coverage')
    return dict(extension_patterns=tested,cycle_tuples=tuple_count,
                intersecting_cycle_pairs=pairs,shared_edge_pairs=shared_edges,
                adjacent_shared_edge_path_pairs=shared_paths)

def graph_controls():
    exchanges=coincident=0
    for n in (4,5):
        possible=list(it.combinations(range(n),2))
        for bits in range(1<<len(possible)):
            es={e for i,e in enumerate(possible) if (bits>>i)&1}
            old_g=girth(n,es)
            for g in (3,4,5):
                if old_g<g:continue
                for x,y in es:
                    centers=[u for u in range(n) if u not in (x,y)]
                    for u,v in it.combinations_with_replacement(centers,2):
                        if any(distance(n,es,a,b)<g-1 for a in (u,v) for b in (x,y)):continue
                        new=(es-{(x,y)})|{tuple(sorted((u,x))),tuple(sorted((v,y)))}
                        check(len(new)==len(es)+1 and girth(n,new)>=g,'current-J exchange')
                        exchanges+=1;coincident+=u==v
    # Inclusion-maximal but not maximum: true N>5B and parity premises.
    n=104;N=52;H={(0,52),(1,52)};F={(i,i+1) for i in range(2,52,2)}|{(i,i+1) for i in range(52,104,2)}
    check(N>5*(1+3*(1+2)) and N%2==0,'k1 full hypotheses')
    check(distance(n,H|F,0,1)==2,'blocked direct addition')
    F2=(F-{(2,3)})|{(0,2),(1,3)}
    check(all(len(a)==1 for a in adj(n,F2)) and girth(n,H|F2)>=4,'k1 saturation by switch')
    N=18;F={(i,i+1) for i in range(1,17)}|{(1,17)}
    check(N>5*3 and (2*N)%2==0,'k2 coincident full hypotheses')
    F2=(F-{(8,9)})|{(0,8),(0,9)}
    check(all(len(a)==2 for a in adj(N,F2)) and girth(N,F2)==18,'coincident repair')
    # Even-degree synthetic seed, only testing the deletion/cut bridge.
    n=12;Y={(u,v) for u in range(6) for v in range(6,12)}
    D={(u,u+6) for u in range(6)};H=Y-D;H2=H-{(0,7)}
    for s in range(1,1<<n):
        size=s.bit_count()
        if size>n//2:continue
        check(boundary(list(Y),s)>=2*size+2,'even q6 auxiliary margin')
        check(boundary(list(H),s)>=size+2,'matching deletion margin')
        check(boundary(list(H2),s)>=size+1,'one-extra-edge margin')
    check(two_connected(n,H2) and not has_mc(n,H2),'synthetic seed connectivity and no MC')
    # K3,3 is a small immune core; all 64 same-part augmentations are tested.
    core={(u,v) for u in range(3) for v in range(3,6)}
    art=list(it.combinations(range(3),2))+list(it.combinations(range(3,6),2));colourings=0
    for bits in range(1<<len(art)):
        fs=[e for i,e in enumerate(art) if (bits>>i)&1];J=core|set(fs);G=set(core)
        for i,(u,v) in enumerate(fs):G|={(u,6+i),(v,6+i)}
        total=6+len(fs)
        check(two_connected(total,G) and girth(total,G)>=girth(6,J),'subdivision girth/connectivity')
        parts={u:0 if u<3 else 1 for u in range(6)}
        for i,(u,v) in enumerate(fs):parts[6+i]=1-parts[u]
        check(all(parts[u]!=parts[v] for u,v in G),'subdivision bipartite')
        for s in range(1,(1<<total)-1):
            check(not mc(total,G,s),'all-shore subdivision control');colourings+=1
    return dict(local_exchanges=exchanges,coincident_exchanges=coincident,
                full_size_saturation_controls=2,subdivision_graphs=64,nonconstant_colourings=colourings)

def mutations():
    results=[]
    def record(name, assertion, data):
        check(assertion,name);results.append(dict(id=name,detected=True,control=data))
    record('M01-replacement-slots',Q(fall(2,2),fall(4,2))!=Q(2,4)**2,dict(actual='1/6',mutant='1/4'))
    record('M02-incidence-as-union',1204>602,dict(incidence=1204,union=602))
    es=[(0,1)]*3;cs=instance_cycles(es,3)
    record('M03-omit-parallel-two-cycles',len(cs)==3 and all(a[1]&b[1] for a,b in it.combinations(cs,2)),dict(two_cycles=3,mutant_cycles=0))
    es=[(0,2),(1,2),(0,3),(1,3),(0,4),(1,4)];cs=instance_cycles(es,5)
    record('M04-omit-shared-paths',len(cs)==3 and all(len(a[0]&b[0])==2 for a,b in it.combinations(cs,2)),dict(graph='K2,3',shared_path_length=2))
    record('M05-unbounded-deletion-degree',boundary([(0,1),(0,2)],1)>1,dict(shore=[0],deleted=[[0,1],[0,2]]))
    es={(0,1),(1,2),(2,3)};new=(es-{(2,3)})|{(0,2),(3,4)}
    record('M06-initial-H-distance',girth(5,es)==math.inf and girth(5,new)==3,dict(H=[],J=sorted(es),new_edges=[[0,2],[4,3]],g=4))
    record('M07-missing-parity',17>5*2 and 17%2==1,dict(N=17,k=1,B=2,degree_sum=17))
    es={(i,i+1) for i in range(1,17)}|{(1,17)};new=(es-{(8,9)})|{(0,8),(0,9)}
    record('M08-forbid-coincident-centres',sum(len(a)<2 for a in adj(18,es))==1 and all(len(a)==2 for a in adj(18,new)),dict(u=0,v=0,old_cycle_length=17,new_cycle_length=18))
    es={(i,i+1) for i in range(5)};new=(es-{(2,3)})|{(0,2),(3,5)}
    record('M09-ignore-one-new-edge-cycles',girth(6,new)==3 and not connected(6,new),dict(J=sorted(es),added=[[0,2],[5,3]],triangles=[[0,1,2],[3,4,5]]))
    core={(u,v) for u in range(3) for v in range(3,6)};G=core|{(0,6),(1,6)}
    record('M10-ignore-opposite-new-vertex',not mc(7,G,1<<6),dict(old_core_colour=0,new_vertex_colour=1,crossing_degree=2))
    n=26;m=12*n;t=19*n;ng=n+t;mg=m+2*t
    record('M11-weak-five-endpoint',2*mg==5*ng and not 2*mg+2<=5*ng,dict(seed_vertices=n,seed_edges=m,final_vertices=ng,final_edges=mg))
    record('M12-collapse-edge-instances',mc(2,{(0,1)},1) and not mc(2,[(0,1),(0,1)],1),dict(parallel_edges=2,distinct_neighbours=1))
    core={(u,v) for u in (0,1) for v in (2,3,4)};G=(core-{(0,2)})|{(0,5),(5,6),(2,6)}
    record('M13-subdivide-core-twice',not has_mc(5,core) and mc(7,G,(1<<5)|(1<<6)),dict(subdivided_edge=[0,2],matching_cut_shore=[5,6]))
    core={(u,v) for u in range(3) for v in range(3,6)}
    record('M14-allow-empty-shore',mc(6,core,0,False) and not mc(6,core,0,True),dict(mask=0))
    a={(0,1),(1,2),(2,3),(3,4),(4,5),(0,5)};b={(0,1),(1,6),(3,6),(3,4),(4,7),(0,7)};common=a&b
    record('M15-shared-edges-not-path',len(common)==2 and not any(set(e)&set(f) for e,f in it.combinations(common,2)),dict(common_edges=sorted(common)))
    record('M16-single-new-neighbour',mc(7,core|{(0,6)},1<<6),dict(new_vertex=6,only_old_neighbour=0))
    return results

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--input',required=True);args=ap.parse_args()
    spec=json.loads(Path(args.input).read_text());check(spec['version']==1,'input version')
    result={'verdict':'candidate_only','purpose':'second exact finite self-check; no universal or trusted verdict',
            'arithmetic':arithmetic(spec['coefficient_N_max']),'patterns':patterns(),
            'graphs':graph_controls(),'mutations':mutations()}
    result['assertions']=TESTS;print(json.dumps(result,sort_keys=True,indent=2))

if __name__=='__main__':main()
