"""Bounded, reproducible local finite-atlas run; no verifier authority."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, platform, resource, subprocess, sys, time
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'run-01'
LIMITS={'wall_seconds':40,'cpu_seconds':35,'memory_bytes':268435456,'output_bytes_per_stream':65536,'thread_environment':1}
def sha(b): return hashlib.sha256(b).hexdigest()
def caps():
    resource.setrlimit(resource.RLIMIT_CPU,(35,35))
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
    resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))
def main():
    OUT.mkdir(exist_ok=True)
    env=os.environ.copy()
    env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    rec={'format':'r10-c34-atlas-execution-v1','verdict':'candidate_only','started_at':datetime.now(timezone.utc).isoformat(),'python_version':platform.python_version(),'platform':platform.system(),'limits':LIMITS,'command':['python','-S','bijections.py','input.json'],'input_sha256':sha((ROOT/'input.json').read_bytes()),'code_sha256':sha((ROOT/'bijections.py').read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),'exit_code':None,'timed_out':False}
    start=time.monotonic()
    with (OUT/'output.json').open('wb') as stdout,(OUT/'stderr.txt').open('wb') as stderr:
        try:
            p=subprocess.run([sys.executable,'-S','bijections.py','input.json'],cwd=ROOT,env=env,stdout=stdout,stderr=stderr,preexec_fn=caps,timeout=40)
            rec['exit_code']=p.returncode
        except subprocess.TimeoutExpired:
            rec['timed_out']=True
    rec['elapsed_seconds']=round(time.monotonic()-start,6)
    for name in ['output.json','stderr.txt']:
        rec[name+'_sha256']=sha((OUT/name).read_bytes())
    rec['native_lean_invoked']=False
    rec['trusted_gate_verdict']=None
    (OUT/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
    print(json.dumps(rec,indent=2))
    raise SystemExit(0 if rec['exit_code']==0 else 2)
if __name__=='__main__':main()
