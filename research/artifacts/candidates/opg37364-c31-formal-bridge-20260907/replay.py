"""Replay without importing the certificate generator or any prior checker."""
import copy,hashlib,json
from pathlib import Path
from nd_kernel import verify,Rejected,Kernel,sub

def run():
 p=Path('core-extension.nd.json');data=p.read_bytes();cert=json.loads(data)
 result=verify(cert)
 full_data=Path('no-cut-extension.nd.json').read_bytes()
 full_cert=json.loads(full_data)
 full_result=verify(full_cert)
 full_result['proof_sha256']=hashlib.sha256(full_data).hexdigest()
 full_result['goal_sha256']=hashlib.sha256(json.dumps(full_cert['goal'],separators=(',',':')).encode()).hexdigest()
 result['full_nonempty_shore_bridge']=full_result
 quant_data=Path('quantifier-bridge.nd.json').read_bytes()
 quant_cert=json.loads(quant_data)
 quant_result=verify(quant_cert)
 quant_result['proof_sha256']=hashlib.sha256(quant_data).hexdigest()
 result['quantifier_order_bridge']=quant_result
 tests=[]
 def reject(name,bad):
  try:verify(bad)
  except (Rejected,ValueError,IndexError,TypeError,KeyError):tests.append(name);return
  raise RuntimeError('undetected: '+name)
 bad=copy.deepcopy(cert);bad['goal']=['bot'];reject('forged_conclusion',bad)
 bad=copy.deepcopy(cert);bad['proof']=['axiom',cert['goal']];reject('undeclared_axiom',bad)
 bad=copy.deepcopy(cert);bad['proof']=['hyp','not_in_context'];reject('unbound_hypothesis',bad)
 bad=copy.deepcopy(cert);bad['proof']=['dne',['imp_i','h',cert['goal'],['hyp','h']]];reject('bad_double_negation',bad)
 bad=copy.deepcopy(cert);bad['proof']=['and_l',cert['proof']];reject('wrong_eliminator',bad)
 # There is no rule allowing an existential witness to escape its scope.
 bad={'format':cert['format'],'sorts':['V'],'signature':{'P':['V']},
      'goal':['imp',['ex','x','V',['atom','P','x']],['ex','x','V',['atom','P','x']]],
      'proof':['imp_i','h',['ex','x','V',['atom','P','x']],
               ['ex_e',['hyp','h'],'w','hw',['hyp','hw']]]}
 reject('existential_escape',bad)
 # Universal generalization may not capture a variable free in an assumption.
 bad={'format':cert['format'],'sorts':['V'],'signature':{'P':['V']},
      'goal':['all','x','V',['imp',['atom','P','x'],['all','x','V',['atom','P','x']]]],
      'proof':['all_i','x','V',['imp_i','h',['atom','P','x'],['all_i','x','V',['hyp','h']]]]}
 reject('universal_capture',bad)
 bad=copy.deepcopy(cert);bad['signature']['Col']=['V','V'];reject('cross_sort_confusion',bad)
 bad=copy.deepcopy(cert);bad['format']='unregistered-extra-rules';reject('format_rule_expansion',bad)
 bad=copy.deepcopy(cert);bad['extra_axioms']=[cert['goal']];reject('extra_axiom_field',bad)
 try:sub(['all','y','V',['atom','P','x']],'x','y')
 except Rejected:tests.append('capture_substitution')
 else:raise RuntimeError('capture accepted')
 # A valid small control exercises both disjunction branches.
 a=['atom','P'];b=['atom','Q'];goal=['imp',['or',a,b],['or',b,a]]
 good={'format':cert['format'],'sorts':[],'signature':{'P':[],'Q':[]},'goal':goal,
       'proof':['imp_i','h',['or',a,b],['or_e',['hyp','h'],'ha',['or_r',b,['hyp','ha']],'hb',['or_l',['hyp','hb'],a]]]}
 verify(good)
 result.update({'format':'r10-c31-nd-replay-v1','verdict':'candidate_only','proof_sha256':hashlib.sha256(data).hexdigest(),
                'goal_sha256':hashlib.sha256(json.dumps(cert['goal'],separators=(',',':')).encode()).hexdigest(),
                'negative_kernel_controls_rejected':tests,'positive_kernel_controls':1,
                'trusted_verified_scope':[],'native_lean_compilation':'not_started_missing_runtime',
                'warning':'This checker is generator-owned and unregistered. Its rule implementation and Lean export still require external review/replay.'})
 return result
if __name__=='__main__':
 try:print(json.dumps(run(),sort_keys=True,indent=2))
 except Exception as exc:
  print(json.dumps({'error_type':type(exc).__name__,'message':str(exc)}));raise SystemExit(1)
