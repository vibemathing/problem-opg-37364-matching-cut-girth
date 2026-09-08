"""Bounded local generator check, never a trusted verification receipt."""
import hashlib, json, os, pathlib, platform, resource, selectors, shutil, signal, subprocess, sys, time
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parent
LIMITS={'wall_seconds':40,'cpu_seconds':35,'memory_bytes':268435456,'combined_output_bytes':131072,'threads':1}
def digest(b): return hashlib.sha256(b).hexdigest()
def caps():
    resource.setrlimit(resource.RLIMIT_CPU,(35,35))
    resource.setrlimit(resource.RLIMIT_AS,(268435456,268435456))
    resource.setrlimit(resource.RLIMIT_FSIZE,(131072,131072))
def main():
    name=sys.argv[1] if len(sys.argv)>1 else 'run-01'
    dest=ROOT/name
    dest.mkdir(exist_ok=False)
    r={'verdict':'candidate_only','status':'running','started_at':datetime.now(timezone.utc).isoformat(),
       'python_version':platform.python_version(),'platform':platform.system(),'limits':LIMITS,
       'argv':['python','-I','-S','parallel22.py','input.json'],
       'inputs':{p:digest((ROOT/p).read_bytes()) for p in ['parallel22.py','input.json','run_bounded.py']},
       'native_tools_found':{x:bool(shutil.which(x)) for x in ['lean','lake','elan']},
       'lean_compilation':'not_run_no_locked_environment_observed','actual_axioms':None,
       'trusted_gate_verdict':None}
    env=os.environ.copy(); env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    t=time.monotonic(); p=subprocess.Popen([sys.executable,'-I','-S','parallel22.py','input.json'],cwd=ROOT,env=env,
         stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True,preexec_fn=caps)
    sel=selectors.DefaultSelector(); bs={'stdout':bytearray(),'stderr':bytearray()}; reason=None
    for f,key in [(p.stdout,'stdout'),(p.stderr,'stderr')]:
        os.set_blocking(f.fileno(),False); sel.register(f,selectors.EVENT_READ,key)
    while sel.get_map():
        if time.monotonic()-t>40: reason='timeout'; break
        for key,_ in sel.select(.05):
            b=os.read(key.fileobj.fileno(),8192)
            if not b: sel.unregister(key.fileobj); continue
            if sum(map(len,bs.values()))+len(b)>131072: reason='output_limit';break
            bs[key.data].extend(b)
        if reason: break
    if reason:
        try: os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError: pass
    r['exit_code']=p.wait(timeout=5);r['stop_reason']=reason;r['elapsed_seconds']=round(time.monotonic()-t,6)
    for key,b in bs.items():
        raw=bytes(b); clean=raw.replace(str(ROOT).encode(),b'<candidate>')
        fn='output.json' if key=='stdout' else 'stderr.txt'
        (dest/fn).write_bytes(clean)
        r[key]={'locator':name+'/'+fn,'raw_sha256':digest(raw),'saved_sha256':digest(clean),'sanitized':raw!=clean,'bytes':len(clean)}
    r['status']='finite_controls_passed' if r['exit_code']==0 and reason is None else 'control_failure'
    (dest/'execution.json').write_text(json.dumps(r,indent=2,sort_keys=True)+'\n')
    print(json.dumps(r,sort_keys=True,indent=2))
    return 0 if r['status']=='finite_controls_passed' else 1
if __name__=='__main__': raise SystemExit(main())
