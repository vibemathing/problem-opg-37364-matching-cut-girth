"""Exact coefficient certificates for universal nonnegative-slack inequalities.
The translation from graph hypotheses to slack variables is audited separately.
"""
import hashlib,json
from pathlib import Path

def plus(a,b):
 r=dict(a)
 for m,c in b.items():r[m]=r.get(m,0)+c
 return {m:c for m,c in r.items() if c}
def mul(a,b):
 r={}
 for x,c in a.items():
  for y,d in b.items():
   z=tuple(sorted((*x,*y)));r[z]=r.get(z,0)+c*d
 return {m:c for m,c in r.items() if c}
def polynomial(x,vs):
 if type(x)==int:return {():x} if x else {}
 if isinstance(x,str):
  if x not in vs:raise ValueError('unknown polynomial variable')
  return {(x,):1}
 if not isinstance(x,list) or len(x)!=3:raise ValueError('expression shape')
 op=x[0];a=polynomial(x[1],vs)
 if op=='pow':
  if type(x[2])!=int or not 0<=x[2]<=8:raise ValueError('power bound')
  p={():1}
  for _ in range(x[2]):p=mul(p,a)
  return p
 b=polynomial(x[2],vs)
 if op=='+':return plus(a,b)
 if op=='-':return plus(a,{m:-c for m,c in b.items()})
 if op=='*':return mul(a,b)
 raise ValueError('operator')
def run():
 raw=Path('algebra-certificates.json').read_bytes();cert=json.loads(raw);res=[]
 for c in cert['certificates']:
  d=plus(polynomial(c['right'],c['nonnegative_variables']),{m:-v for m,v in polynomial(c['left'],c['nonnegative_variables']).items()})
  if c['relation']=='eq':ok=not d
  elif c['relation']=='lt':ok=all(v>=0 for v in d.values()) and d.get((),0)>0
  elif c['relation']=='le':ok=all(v>=0 for v in d.values())
  else:raise ValueError('relation')
  if not ok:raise ValueError('failed certificate '+c['id'])
  res.append({'id':c['id'],'difference_coefficients':[[list(m),v] for m,v in sorted(d.items())]})
 return {'format':'r10-c31-polynomial-replay-v1','verdict':'candidate_only','input_sha256':hashlib.sha256(raw).hexdigest(),'certificates':res,
         'domain':'each named variable is a nonnegative integer; no bounded substitution test',
         'limitation':'formal coefficient criterion is generator-owned; graph-to-slack premise mapping and native Lean replay are not supplied by this script'}
if __name__=='__main__':
 try:print(json.dumps(run(),sort_keys=True,indent=2))
 except Exception as e:print(json.dumps({'error_type':type(e).__name__,'message':str(e)}));raise SystemExit(1)
