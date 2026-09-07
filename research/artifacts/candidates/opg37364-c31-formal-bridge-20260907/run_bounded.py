"""Bounded local replay runner, not a repository verifier or admission action."""
from __future__ import annotations
import hashlib,json,os,platform,resource,selectors,signal,subprocess,sys,time
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def limits():
 resource.setrlimit(resource.RLIMIT_CPU,(35,35))
 resource.setrlimit(resource.RLIMIT_AS,(256*1024*1024,)*2)
 resource.setrlimit(resource.RLIMIT_FSIZE,(131072,)*2)

def main():
 mode=sys.argv[1]
 files={'replay':['replay.py','nd_kernel.py','core-extension.nd.json','no-cut-extension.nd.json','quantifier-bridge.nd.json'],
        'separate':['separate_audit.py'],
        'algebra':['algebra_replay.py','algebra-certificates.json']}
 if mode not in files:raise SystemExit(2)
 script=files[mode][0]
 started=time.time();begin=time.monotonic()
 env=dict(os.environ)
 for v in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS'):env[v]='1'
 data={'stdout':bytearray(),'stderr':bytearray()};error=None
 try:p=subprocess.Popen([sys.executable,'-S',script],stdout=subprocess.PIPE,stderr=subprocess.PIPE,env=env,preexec_fn=limits,start_new_session=True)
 except OSError as e:
  print(json.dumps({'started':False,'errno':e.errno}));return 1
 sel=selectors.DefaultSelector()
 for stream,name in [(p.stdout,'stdout'),(p.stderr,'stderr')]:
  os.set_blocking(stream.fileno(),False);sel.register(stream,selectors.EVENT_READ,name)
 while sel.get_map():
  if time.monotonic()-begin>40:error='wall_timeout'
  if error:
   os.killpg(p.pid,signal.SIGKILL);break
  for key,events in sel.select(.05):
   block=os.read(key.fileobj.fileno(),8192)
   if not block:sel.unregister(key.fileobj);continue
   data[key.data].extend(block)
   if len(data[key.data])>65536 or sum(map(len,data.values()))>131072:error='output_limit'
 rc=p.wait(timeout=2)
 for n,b in data.items():Path(mode+'.'+n+'.txt').write_bytes(bytes(b))
 record={'format':'r10-c31-bounded-execution-v1','verdict':'candidate_only',
 'runtime':{'implementation':platform.python_implementation(),'version':platform.python_version(),'binary_sha256':sha(sys.executable),'os':platform.system()},
 'started_at_unix':started,'elapsed_seconds':round(time.monotonic()-begin,6),
 'command':['python','-S',script],'input_sha256':{f:sha(f) for f in files[mode]},
 'runner_sha256':sha('run_bounded.py'),'exit_code':rc,'forced_stop':error,
 'limits':{'wall_seconds':40,'cpu_seconds':35,'address_space_bytes':268435456,'stdout_bytes':65536,'stderr_bytes':65536,'combined_output_bytes':131072,'thread_environment':1},
 'outputs':{n:{'path':mode+'.'+n+'.txt','bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()} for n,b in data.items()},
 'trust':'local generator-owned replay only; no trusted verifier/provider identity or attestation'}
 Path(mode+'.execution.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
 print(json.dumps({'mode':mode,'exit_code':rc,'forced_stop':error,'output_bytes':{k:len(v) for k,v in data.items()}}))
 return 0 if rc==0 and error is None else 1
if __name__=='__main__':raise SystemExit(main())
