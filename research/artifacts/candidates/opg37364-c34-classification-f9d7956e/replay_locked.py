"""Replay C34 in an already installed, exactly pinned native environment.

No download, workflow dispatch, registry edit, or Evidence/Result operation.
The success path has NOT been exercised in the preparing runtime.
"""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, platform, re, resource
import selectors, signal, subprocess, time
from datetime import datetime, timezone
from source_scan import findings
ROOT=pathlib.Path(__file__).resolve().parent
LIMITS={'wall_seconds':120,'cpu_seconds':90,'address_space_bytes':4294967296,'combined_output_bytes':262144,'lean_threads':1}
LEAN_COMMIT='819816b2e0a3bf405af45ae5c7af2491d8f5bee6'
MATHLIB_COMMIT='0df444a360eaa60ab8c11dca51a86af692955474'
C31='research/artifacts/candidates/opg37364-c31-native-lock-20260907'
C32='research/artifacts/candidates/opg37364-c32-hit-count-7e7ade8b'
C33='research/artifacts/candidates/opg37364-c33-parallel22-2f13311d'
SOURCES={
 'R10/CompletionEquiv.lean':(C31,'6c8d34156e1204899e850fa8092aae3de4faf36e063f1d840c3819bfa7c778a6'),
 'R10/CompletionCardinality.lean':(C31,'4d347de4950eb71a129f9848af486e97037c70d76a03e09f1c581aa77f616352'),
 'R10/ProductCounts.lean':(C31,'0828d8f31eee2184980bd250d2074ba8f4190fd671beba17bea9c79c992b43fd'),
 'R10/HitCounts.lean':(C32,'113e5ccc4b1c39d3c8756a6355b9803f824276ca74e013086f20cfd623a308bc'),
 'R10/HitProbability.lean':(C32,'9a98f85b05e87c42bcb2a1676ae1ae3f0e67035f036c3ebf2f71af45f931041c'),
 'R10/Parallel22.lean':(C33,'6002875239b7bab2caa1186c96f4e63d010e72b1aa9ab00dcecd907ff0d2f822')}
def sha(b): return hashlib.sha256(b).hexdigest()
def hashfile(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1048576),b''): h.update(block)
    return h.hexdigest()
def caps():
    resource.setrlimit(resource.RLIMIT_AS,(LIMITS['address_space_bytes'],)*2)
    resource.setrlimit(resource.RLIMIT_CPU,(LIMITS['cpu_seconds'],)*2)
def run(argv,cwd,env,out,index,scrub):
    begin=time.monotonic(); buffers={'stdout':bytearray(),'stderr':bytearray()}
    rec={'argv':[scrub(x) for x in argv],'process_created':False,'exit_code':None,'stop_reason':None}
    try:
        p=subprocess.Popen(argv,cwd=cwd,env=env,stdout=subprocess.PIPE,stderr=subprocess.PIPE,preexec_fn=caps,start_new_session=True)
    except OSError as e:
        rec.update(stop_reason='process_not_created',errno=e.errno)
    else:
        rec['process_created']=True
        sel=selectors.DefaultSelector()
        for s,name in ((p.stdout,'stdout'),(p.stderr,'stderr')):
            os.set_blocking(s.fileno(),False);sel.register(s,selectors.EVENT_READ,name)
        while sel.get_map():
            if time.monotonic()-begin>LIMITS['wall_seconds']:
                rec['stop_reason']='wall_limit';break
            for key,_ in sel.select(.05):
                b=os.read(key.fileobj.fileno(),8192)
                if not b: sel.unregister(key.fileobj);continue
                if sum(map(len,buffers.values()))+len(b)>LIMITS['combined_output_bytes']:
                    rec['stop_reason']='output_limit';break
                buffers[key.data].extend(b)
            if rec['stop_reason']:break
        if rec['stop_reason']:
            try:os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError:pass
        try:rec['exit_code']=p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL);rec['exit_code']=p.wait();rec['stop_reason']='post_output_wait_limit'
        sel.close()
    text={}
    for name,b in buffers.items():
        text[name]=scrub(bytes(b).decode('utf-8','replace'))
        loc=f'command-{index:03d}.{name}.txt';(out/loc).write_text(text[name])
        rec[name]={'locator':loc,'raw_sha256':sha(bytes(b)),'saved_sha256':sha(text[name].encode()),'sanitized':text[name].encode()!=bytes(b)}
    rec['elapsed_seconds']=round(time.monotonic()-begin,6)
    return rec,text

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--repo-root',type=pathlib.Path,required=True)
    ap.add_argument('--mathlib-root',type=pathlib.Path,required=True)
    ap.add_argument('--lean',type=pathlib.Path,required=True)
    ap.add_argument('--output',type=pathlib.Path,required=True)
    a=ap.parse_args(); repo=a.repo_root.resolve();mathlib=a.mathlib_root.resolve();lean=a.lean.resolve();out=a.output.resolve()
    out.mkdir(parents=True,exist_ok=True);work=out/'work';(work/'R10').mkdir(parents=True,exist_ok=True)
    rec={'format':'r10-c34-native-replay-v1','verdict':'candidate_only','started_at':datetime.now(timezone.utc).isoformat(),'limits':LIMITS,'driver_sha256':hashfile(pathlib.Path(__file__)),'python_version':platform.python_version(),'commands':[],'compiled_modules':[],'actual_axioms':None,'actual_toolchain_fingerprint':None,'trusted_gate_verdict':None,'status':'pending','source_sha256':{}}
    def scrub(s):
        for p,tag in sorted([(str(repo),'<repository>'),(str(mathlib),'<mathlib>'),(str(lean),'<lean>'),(str(out),'<output>'),(str(ROOT),'<candidate>')],key=lambda x:-len(x[0])):s=s.replace(p,tag)
        return s
    def finish(status,code):
        rec['status']=status;rec['finished_at']=datetime.now(timezone.utc).isoformat()
        (out/'execution.json').write_text(json.dumps(rec,indent=2)+'\n')
        print(status);raise SystemExit(code)
    if not lean.is_file():finish('explicit_native_executable_not_present_no_compilation',2)
    env=os.environ.copy();env.update(OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1',LEAN_NUM_THREADS='1')
    def checked(argv):
        r,t=run(argv,work,env,out,len(rec['commands'])+1,scrub);rec['commands'].append(r)
        if r['exit_code']!=0 or r['stop_reason']:finish('first_command_failure',2)
        return t['stdout']
    version=checked([str(lean),'--version'])
    gh=checked([str(lean),'--githash']).strip()
    if '4.33.1' not in version or gh!=LEAN_COMMIT:finish('native_version_or_commit_mismatch',2)
    if checked(['git','-C',str(mathlib),'rev-parse','HEAD']).strip()!=MATHLIB_COMMIT:finish('mathlib_commit_mismatch',2)
    manifest=json.loads((mathlib/'lake-manifest.json').read_text())
    rec['mathlib_manifest_sha256']=hashfile(mathlib/'lake-manifest.json')
    paths=[work,mathlib/'.lake/build/lib/lean'];rec['dependency_heads']={}
    for package in manifest['packages']:
        dep=mathlib/'.lake/packages'/package['name']
        actual=checked(['git','-C',str(dep),'rev-parse','HEAD']).strip()
        if actual!=package['rev']:finish('transitive_commit_mismatch:'+package['name'],2)
        rec['dependency_heads'][package['name']]=actual;paths.append(dep/'.lake/build/lib/lean')
    env['LEAN_PATH']=os.pathsep.join(map(str,paths))
    rec['actual_toolchain_fingerprint']={'lean_binary_sha256':hashfile(lean),'githash':gh}
    shared=lean.parent.parent/'lib/lean/libleanshared.so'
    if shared.is_file():rec['actual_toolchain_fingerprint']['libleanshared_sha256']=hashfile(shared)
    for path,(prefix,digest) in SOURCES.items():
        b=(repo/prefix/path).read_bytes()
        if sha(b)!=digest:finish('frozen_source_digest_mismatch:'+path,2)
        (work/path).write_bytes(b);rec['source_sha256'][path]=digest
    for src in [ROOT/'ProjectionOnly.lean',*sorted((ROOT/'R10').glob('*.lean'))]:
        rel=src.relative_to(ROOT);(work/rel).parent.mkdir(parents=True,exist_ok=True)
        (work/rel).write_bytes(src.read_bytes());rec['source_sha256'][str(rel)]=hashfile(src)
    rec['escape_scan']={path:findings((work/path).read_text()) for path in rec['source_sha256']}
    if any(rec['escape_scan'].values()):finish('source_escape_token_rejected',2)
    # First compile exactly the projection in isolation, without C32 imports.
    projection=checked([str(lean),'-j1','ProjectionOnly.lean'])
    rec['compiled_modules'].append('ProjectionOnly')
    for path in [*SOURCES,'R10/C34Classification.lean','R10/C34IndexCardinalities.lean']:
        checked([str(lean),'-j1','-o',str(pathlib.Path(path).with_suffix('.olean')),path])
        rec['compiled_modules'].append(path)
    audits=checked([str(lean),'-j1','R10/C34AxiomAudit.lean'])
    blocks=re.findall(r"depends on axioms:\s*\[([^\]]*)\]",projection+'\n'+audits,re.S)
    zero=(projection+'\n'+audits).count('does not depend on any axioms')
    # One isolated projection plus fourteen audit queries, by source identity.
    if len(blocks)+zero!=15:finish('axiom_output_count_mismatch',2)
    rec['actual_axioms']=sorted({x.strip() for block in blocks for x in block.split(',') if x.strip()})
    if set(rec['actual_axioms'])-{'propext','Classical.choice','Quot.sound'}:finish('unexpected_axiom',2)
    finish('local_native_slice_success_unadmitted',0)
if __name__=='__main__':main()
