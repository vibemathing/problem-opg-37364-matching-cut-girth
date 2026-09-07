"""Nonvacuous local cycle-pairing controls; no global selector is tested."""
import hashlib,json,runpy
from pathlib import Path
cfg=json.loads(Path('input.json').read_text())
parent=Path('../checker.py')
assert hashlib.sha256(parent.read_bytes()).hexdigest()==cfg['parent_sha256']
lib=runpy.run_path(str(parent));dist=lib['distance'];girth=lib['girth']
rows=[]
for g in cfg['girths']:
 for kind in ('uv_xy','uy_vx','coincident','one_new_edge'):
  u,v,x,y=(0,1,2,3) if kind!='coincident' else (0,0,1,2)
  es={tuple(sorted((x,y)))};n=max(u,v,x,y)+1
  def path(a,b,length):
   global n
   vertices=[a]+list(range(n,n+length-1))+[b];n+=length-1
   es.update(tuple(sorted(e)) for e in zip(vertices,vertices[1:]))
  if kind=='uv_xy':path(u,v,1);path(x,y,g-1);expected=g+2
  elif kind=='uy_vx':path(u,y,g-1);path(v,x,g-1);expected=2*g
  elif kind=='coincident':path(x,y,g-1);expected=g+1
  else:path(u,x,g-1);expected=g
  assert girth(n,es)>=g
  assert all(dist(n,es,a,b)>=g-1 for a in set((u,v)) for b in (x,y))
  j0=es-{tuple(sorted((x,y)))}
  assert dist(n,j0,x,y)>=g-1
  added={tuple(sorted((u,x))),tuple(sorted((v,y)))}
  new=j0|added
  assert len(new)==len(es)+1 and girth(n,new)==expected
  if kind=='one_new_edge':
   assert girth(n,new-{tuple(sorted((v,y)))})==g
  else:
   assert all(girth(n,new-{edge})>expected for edge in added)
  rows.append({'g':g,'case':kind,'order':n,'girth_after':expected})
print(json.dumps({'verdict':'candidate_only','controls':rows,'count':len(rows),
 'scope':'Local switch cycle classification only; not maximum-cardinality or all-girth existence verification.'},sort_keys=True,indent=2))
