"""Bounded local generator run; no registry or Evidence authority."""
import datetime as dt
import hashlib,json,os,platform,resource,subprocess,sys,time
from pathlib import Path

def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def caps():
    resource.setrlimit(resource.RLIMIT_CPU,(35,35))
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
    resource.setrlimit(resource.RLIMIT_FSIZE,(65536,65536))
    resource.setrlimit(resource.RLIMIT_CORE,(0,0))

def main():
    start=dt.datetime.now(dt.timezone.utc).isoformat();t=time.monotonic()
    env=dict(os.environ)
    for k in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS'):env[k]='1'
    forced=None
    with open('output.json','wb') as out,open('stderr.txt','wb') as err:
        try:
            p=subprocess.run([sys.executable,'checker.py','--input','input.json'],stdout=out,stderr=err,
                             timeout=40,env=env,preexec_fn=caps(),check=False)
            code=p.returncode
        except subprocess.TimeoutExpired:code=None;forced='wall_timeout'
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    record={'format':'r10-second-audit-execution-v1','verdict':'candidate_only',
      'role':'user-authorized local candidate-generator self-check; not a registered verifier',
      'command':['python3','checker.py','--input','input.json'],
      'started_at':start,'finished_at':dt.datetime.now(dt.timezone.utc).isoformat(),
      'elapsed_seconds':round(time.monotonic()-t,6),'exit_code':code,'forced_stop':forced,
      'runtime':{'implementation':platform.python_implementation(),'version':platform.python_version(),
                 'system':platform.system(),'third_party_packages':[]},
      'limits':{'wall_seconds':40,'cpu_seconds':35,'address_space_bytes':268435456,
                'per_stream_bytes':65536,'combined_output_bytes':131072,'threads':1,'checker_processes':1},
      'cpu_user_seconds':usage.ru_utime,'max_rss_kib':usage.ru_maxrss,
      'routing':'CPU: exact integers, rational arithmetic and bounded finite graph controls',
      'hashes':{p:sha(p) for p in ('checker.py','input.json','runner.py','output.json','stderr.txt')},
      'output_bytes':{p:Path(p).stat().st_size for p in ('output.json','stderr.txt')},
      'limitations':['Finite tests do not prove the all-girth theorem.','No theorem prover or scoped admission gate executed.',
                     'No general good tuple or huge regularization selector was generated.']}
    Path('execution.json').write_text(json.dumps(record,sort_keys=True,indent=2)+'\n')
    print(json.dumps(record,sort_keys=True,indent=2))
    if code!=0 or forced:raise SystemExit(1)
if __name__=='__main__':main()
