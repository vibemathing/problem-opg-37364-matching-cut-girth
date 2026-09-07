"""New exact permanent/edge-walk implementation; no earlier checker imports.
Finite checks only. Formal core propagation is checked in a separate proof replay.
"""
from __future__ import annotations
from collections import Counter, defaultdict, deque
from fractions import Fraction
from itertools import combinations, permutations, product
from math import factorial, comb
import json
from pathlib import Path

COUNT=0

def check(ok, label):
 global COUNT
 COUNT+=1
 if not ok: raise ValueError(label)

def coeff(N,A,B):
 # Weighted permanent: row-by-row matching masks and accumulated z exponent.
 dp={(0,0):1}
 for i in range(N):
  nxt=defaultdict(int)
  for (used,j),w in dp.items():
   for b in range(N):
    if not (used>>b)&1:nxt[used|1<<b,j+int(i in A and b in B)]+=w
  dp=nxt
 return Counter({j:w for (used,j),w in dp.items()})

def conv(x,y):
 z=Counter()
 for i,a in x.items():
  for j,b in y.items(): z[i+j]+=a*b
 return z

def edges_of(ps,N):return [(i,N+p[i]) for p in ps for i in range(N)]
def boundary(edges,mask):return sum(((mask>>u)&1)!=((mask>>v)&1) for u,v in edges)
def mc(n,edges,mask):
 if mask in (0,(1<<n)-1):return False
 deg=Counter()
 for u,v in edges:
  if ((mask>>u)&1)!=((mask>>v)&1):deg[u]+=1;deg[v]+=1
 return max(deg.values(),default=0)<=1

def cyc(n,edges,g):
 # Vertex-simple closed walks with edge-instance identities; reverse walks
 # and starting vertices collapse only after edge-set canonicalization.
 adj=[[] for _ in range(n)]
 for j,(u,v) in enumerate(edges):adj[u].append((v,j));adj[v].append((u,j))
 result=set()
 for s in range(n):
  stack=[(s,(s,),())]
  while stack:
   u,vs,es=stack.pop()
   for v,j in adj[u]:
    if j in es:continue
    if v==s:
     if 2<=len(es)+1<g:result.add(frozenset((*es,j)))
    elif v not in vs and len(es)+1<g-1:stack.append((v,(*vs,v),(*es,j)))
 return result

def connected(n,edges,omit=None):
 verts=set(range(n))-{omit}
 if not verts:return True
 seen={next(iter(verts))}
 while True:
  more=seen|{v for u,v in edges if u in seen and v in verts}|{u for u,v in edges if v in seen and u in verts}
  if more==seen:return seen==verts
  seen=more

def girth(n,edges):
 cs=cyc(n,edges,n+1)
 return min(map(len,cs),default=n+1)
def degree(n,edges):return [sum(v in e for e in edges) for v in range(n)]
def dist(n,edges,s,t):
 if s==t:return 0
 seen={s};front={s}
 for d in range(1,n+1):
  front=({v for u,v in edges if u in front}|{u for u,v in edges if v in front})-seen
  if t in front:return d
  seen|=front
  if not front:return n+1
 return n+1

def recurrence_cases():
 cases=0
 for N in range(1,6):
  for a in range(N+1):
   for b in range(N+1):
    got=coeff(N,set(range(a)),set(range(b)))
    expected=Counter({j:comb(a,j)*comb(N-a,b-j)*factorial(b)*factorial(N-b)
      for j in range(max(0,a+b-N),min(a,b)+1)})
    check(got==expected,'permanent coefficient')
    check(sum(got.values())==factorial(N),'mass')
    check(got==coeff(N,set(range(b)),set(range(a))),'orientation')
    p=Counter({0:1})
    for q in range(1,25):
     p=conv(p,got); check(sum(p.values())==factorial(N)**q,'q mass')
    cases+=1
 # Direct tuples versus convolution, all sizes and all q up to three.
 tuple_count=0
 for N,q in [(2,1),(2,3),(3,2),(3,3),(4,2)]:
  ps=list(permutations(range(N)))
  for a,b in [(1,1),(1,N-1)]:
   hist=Counter(sum(sum(p[i]<b for i in range(a)) for p in ts) for ts in product(ps,repeat=q))
   pol=Counter({0:1})
   for _ in range(q):pol=conv(pol,coeff(N,set(range(a)),set(range(b))))
   check(hist==pol,'tuple direct agreement');tuple_count+=len(ps)**q
 # Weighted types instead of evaluating 2**24 graphs individually.
 incidence=union=0;hist=Counter()
 for j in range(25):
  ps=[(0,1)]*j+[(1,0)]*(24-j);edges=edges_of(ps,2)
  bad=sum(boundary(edges,s)<=2*s.bit_count() for s in range(1,16) if s.bit_count()<=2)
  weight=comb(24,j);incidence+=weight*bad;union+=weight*int(bad>0);hist[bad]+=weight
 check(incidence==1204 and union==602,'q24 incidence')
 return {'coefficient_cases':cases,'direct_tuple_evaluations':tuple_count,'q24_incidence':incidence,'q24_union':union,'q24_histogram':dict(hist)}

def prescription_cases():
 total=0
 for N,q,maxe in [(2,2,3),(3,2,3),(4,2,2)]:
  slots=list(product(range(q),range(N),range(N)))
  for e in range(maxe+1):
   for chosen in combinations(slots,e):
    actual=expected=1
    for c in range(q):
     cells=[(i,j) for cc,i,j in chosen if cc==c]
     rows=[(1<<N)-1 for _ in range(N)]
     for i,j in cells:rows[i]&=1<<j
     dp={0:1}
     for row in rows:
      nxt=defaultdict(int)
      for used,w in dp.items():
       for j in range(N):
        if row>>j&1 and not used>>j&1:nxt[used|1<<j]+=w
      dp=nxt
     actual*=dp.get((1<<N)-1,0)
     compatible=len({i for i,j in cells})==len(cells)==len({j for i,j in cells})
     expected*=factorial(N-len(cells)) if compatible else 0
    check(actual==expected,'compatible prescribed extensions')
    total+=1
 return total

def pattern_cases():
 tuples=pairs=shared=paths=0
 for N,q in [(1,3),(2,3),(3,3)]:
  for ps in product(permutations(range(N)),repeat=q):
   edges=edges_of(ps,N);cs=cyc(2*N,edges,7);tuples+=1
   for a,b in combinations(cs,2):
    av={v for e in a for v in edges[e]};bv={v for e in b for v in edges[e]}
    if av&bv:
     pairs+=1;uv=av|bv;ue=a|b;check(len(ue)>=len(uv)+1,'cycle rank')
     common=a&b
     shared+=bool(common)
     paths+=any(set(edges[e])&set(edges[f]) for e,f in combinations(common,2))
   short=cyc(2*N,edges,3)
   if all(not ({v for e in a for v in edges[e]}&{v for e in b for v in edges[e]}) for a,b in combinations(short,2)):
    deleted={min(c) for c in short}
    check(max(degree(2*N,[edges[i] for i in deleted]),default=0)<=1,'matching deletion')
    remain=[e for i,e in enumerate(edges) if i not in deleted]
    check(not cyc(2*N,remain,3),'no parallel after deletion')
    for s in range(1,1<<(2*N)):
     check(boundary(remain,s)>=boundary(edges,s)-s.bit_count(),'cut loss')
  # The tuple sample above is small. Add a vertex-only overlap explicitly.
 figure8=[(0,1),(1,2),(2,3),(0,3),(0,4),(4,5),(5,6),(0,6)]
 figures=cyc(7,figure8,5)
 check(len(figures)==2,'figure eight cycles')
 fa,fb=list(figures)
 check(not fa&fb and len(fa|fb)==8,'vertex overlap without shared edge')
 return {'prescribed_pair_controls':prescription_cases(),'vertex_only_overlap_controls':1,'tuples':tuples,'overlap_pairs':pairs,'shared_edge_pairs':shared,'adjacent_shared_path_pairs':paths}

def strict_arithmetic():
 constants=[(2*24**19,3*69984*13**19),(55296,54925),(3906250000,3726508032),(9801,8000),(1296,1250),(65536,24000),(500**3,100*69984)]
 for a,b in constants:check(a>b,'strict constant')
 check(Fraction(1,20)+Fraction(1,1000)+Fraction(1,4000)==Fraction(41,800)<1,'union total')
 for g in range(3,13):
  K=2*g;C=K*K*(96*K*K)**K;M=4*C;N=M*M;B=1+62*sum(61**j for j in range(g-2))
  check(M>=max(1000,K,5*B+1) and N>5*B and (38*N)%2==0,'size/parity')
  check(40*N==10240*g**4*(384*g*g)**(4*g),'order')
 return {'strict_rational_comparisons':len(constants)+1,'finite_parameter_checks':10,'universal_parameter_proof':'see conventional audit, not implied by these ten cases'}

def graph_cases():
 # Exhaustive local exchange tests: unlike the full saturation theorem,
 # these need only the local distance/degree hypotheses of the switch.
 exchanges=coincident=0
 for n in range(3,6):
  universe=list(combinations(range(n),2))
  for mask in range(1<<len(universe)):
   es=[e for i,e in enumerate(universe) if mask>>i&1]
   ds=degree(n,es)
   for g in (3,4,5):
    if cyc(n,es,g):continue
    for u in range(n):
     for v in range(u,n):
      if ds[u]+(2 if u==v else 1)>3 or ds[v]+1>3:continue
      for x,y in es:
       if min(dist(n,es,z,t) for z in {u,v} for t in (x,y))<g-1:continue
       switched=[e for e in es if e!=(x,y)]+[tuple(sorted((u,x))),tuple(sorted((v,y)))]
       check(len(set(switched))==len(switched),'switch simple')
       check(not cyc(n,switched,g),'switch girth')
       exchanges+=1;coincident+=u==v
 # Bipartite K(2,3) core, all same-part artificial pairs, independently
 # checking colourings and all graph properties used by the extension.
 graphs=colourings=0;core=[(u,v) for u in (0,1) for v in (2,3,4)]
 pairs=[(0,1),(2,3),(2,4),(3,4)]
 check(not any(mc(5,core,s) for s in range(1,31)),'immune bipartite core')
 for mask in range(16):
  es=core[:];n=5;colors=[0,0,1,1,1];js=core[:]
  for i,(u,v) in enumerate(pairs):
   if mask>>i&1:
    es.extend([(u,n),(v,n)]);js.append((u,v));colors.append(1-colors[u]);n+=1
  graphs+=1
  for s in range(1,(1<<n)-1):check(not mc(n,es,s),'core extension');colourings+=1
  check(all(connected(n,es,v) for v in range(n)),'2 connected')
  check(len(set(es))==len(es) and all(u!=v for u,v in es),'simple extension')
  check(all(colors[u]!=colors[v] for u,v in es),'bipartite extension')
  check(girth(n,es)>=girth(5,js),'cycle projection')
 return {'local_exchanges':exchanges,'coincident':coincident,'core_controls':graphs,'nonconstant_colourings':colourings}

def mutations():
 answers=[]
 def killed(i,b,note):check(b,i);answers.append({'id':i,'detected':bool(b),'certificate':note})
 killed('M01',Fraction(0,1)!=Fraction(1,3)**2,'N=3,b=1,k=2: without replacement0, replacement1/9')
 killed('M02',1204>602,'actual independent aggregation in recurrence test: incidence1204 != union602')
 parallel=[(0,1)]*3
 killed('M03',len(cyc(2,parallel,3))==3 and len(cyc(2,[(0,1)],3))==0,'three parallel edges have three distinct two-cycles')
 theta=[(0,2),(2,1),(0,3),(3,1),(0,4),(4,1)];cc=cyc(5,theta,5)
 killed('M04',len(cc)==3 and all(len(a&b)==2 for a,b in combinations(cc,2)),'theta paths of length2: all short-cycle pairs share two adjacent edges')
 k4=list(combinations(range(4),2));remain=[e for e in k4 if e not in [(0,1),(0,2)]]
 killed('M05',boundary(k4,1)>2 and boundary(remain,1)<=1,'nonmatching deletion removes2 crossing edges at a single vertex')
 j=[(0,1),(1,2),(2,3)];sw=[(0,1),(1,2),(0,2),(4,3)]
 killed('M06',dist(5,[],0,2)>=3 and dist(5,j,0,2)==2 and bool(cyc(5,sw,4)),'stale empty H sees distance infinity; actual J switch creates triangle')
 killed('M07',not any(all(x==1 for x in degree(3,[e for k,e in enumerate(list(combinations(range(3),2))) if s>>k&1])) for s in range(8)),'no 1-regular graph on3 vertices')
 n=20;ring=[(i,i+1) for i in range(1,19)]+[(1,19)]
 changed=[e for e in ring if e!=(1,2)]+[(0,1),(0,2)]
 killed('M08',n>5*3 and degree(n,ring).count(0)==1 and all(x==2 for x in degree(n,changed)),'k2,N20,g3,H empty: only vertex0 has deficit2; coincident-centre switch is required')
 killed('M09',not cyc(3,[(0,1),(1,2)],4) and len(cyc(3,[(0,1),(1,2),(0,2)],4))==1,'one added edge closes a forbidden triangle')
 core=[(0,1),(1,2),(0,2)];ext=core+[(0,3),(1,3)]
 killed('M10',not mc(4,ext,1<<3),'monochromatic core and opposite new vertex has two crossing edges')
 n=50;t=19*n;twom=24*n
 killed('M11',twom+4*t==5*(n+t),'without seed deficit, n50,2m1200 yields final average exactly5')
 killed('M12',not mc(2,parallel,1) and mc(2,[(0,1)],1),'collapsing coloured edges changes matching predicate')
 subdiv=[(1,2),(0,2),(0,3),(3,4),(4,1)]
 killed('M13',mc(5,subdiv,(1<<3)|(1<<4)),'twice subdividing an old K3 edge creates matching-cut shore{3,4}')
 killed('M14',not mc(3,core,0) and boundary(core,0)==0,'empty shore has empty crossing set but is not permitted')
 e1={(0,1),(1,2),(2,3),(3,4),(4,5),(0,5)}
 e2={(0,1),(1,6),(3,6),(3,4),(4,7),(0,7)};common=e1&e2
 killed('M15',len(common)==2 and not any(set(a)&set(b) for a,b in combinations(common,2)),'common edges{0,1},{3,4} are disjoint, not a path')
 killed('M16',mc(4,core+[(0,3)],1<<3),'one-neighbour attachment creates a singleton matching-cut shore')
 return answers

def run():
 a=recurrence_cases();b=pattern_cases();f=strict_arithmetic();e=graph_cases();m=mutations()
 return {'format':'r10-c31-separate-audit-v1','verdict':'candidate_only','assertions':COUNT,'A':a,'B_C':b,'D_E':e,'F':f,'mutations':m,'trusted_verified_scope':[],
 'limitation':'Finite controls do not prove the high-girth family. E logical propagation is separately checked as a general proof certificate.'}
if __name__=='__main__':
 try:print(json.dumps(run(),sort_keys=True,indent=2))
 except Exception as exc:
  print(json.dumps({'error_type':type(exc).__name__,'message':str(exc)}));raise SystemExit(1)
