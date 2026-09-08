"""C32 pinned, bounded replay. A local build is not trusted repository admission.

Run with an installed native Lean and a populated, pinned Mathlib checkout:
  python -S replay.py --lean <lean-executable> --mathlib-dir <mathlib-checkout>
The C31 source directory is read only. All compilation occurs in a temporary
capsule. No dependency downloader, repository workflow or truth writer is run.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import os
from pathlib import Path
import platform
import re
import resource
import selectors
import shutil
import signal
import subprocess
import tempfile
import time
from datetime import datetime, timezone

ROOT = Path(__file__).resolve().parent
LIMITS = dict(wall_seconds=120, cpu_seconds=90, memory_bytes=4*1024**3,
              combined_output_bytes=262144, threads=1)
OLD_MODULES = ['R10.CompletionEquiv', 'R10.CompletionCardinality', 'R10.ProductCounts']
NEW_MODULES = ['R10.HitCounts', 'R10.HitProbability']
ALLOWED_AXIOMS = {'propext', 'Classical.choice', 'Quot.sound'}
ESCAPES = re.compile(r'\b(?:sorry|admit|axiom|unsafe|partial|extern|native_decide|implemented_by)\b|#eval|debug\.skipKernelTC')

def digest(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()

def file_digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda: f.read(1048576), b''):
            h.update(chunk)
    return h.hexdigest()

def strip_comments_strings(s: str) -> str:
    out, i, depth, string = [], 0, 0, False
    while i < len(s):
        pair = s[i:i+2]
        if depth:
            if pair == '/-': depth += 1; i += 2
            elif pair == '-/': depth -= 1; i += 2
            else: out.append('\n' if s[i] == '\n' else ' '); i += 1
        elif string:
            if s[i] == '\\': i += 2
            elif s[i] == '"': string = False; i += 1
            else: out.append('\n' if s[i] == '\n' else ' '); i += 1
        elif pair == '/-': depth = 1; out.append(' '); i += 2
        elif pair == '--':
            j = s.find('\n', i); i = len(s) if j < 0 else j
            out.append(' ')
        elif s[i] == '"': string = True; out.append(' '); i += 1
        else: out.append(s[i]); i += 1
    if depth or string:
        raise ValueError('unterminated source comment/string')
    return ''.join(out)

def command(argv: list[str], cwd: Path, env: dict[str, str]) -> dict:
    """Return raw bytes internally; sanitize only when serializing receipts."""
    r = dict(argv=argv, process_created=False, exit_code=None, stop_reason=None,
             stdout=b'', stderr=b'')
    start = time.monotonic()
    def caps():
        resource.setrlimit(resource.RLIMIT_AS, (LIMITS['memory_bytes'],)*2)
        resource.setrlimit(resource.RLIMIT_CPU, (LIMITS['cpu_seconds'],)*2)
    try:
        p = subprocess.Popen(argv, cwd=cwd, env=env, stdout=subprocess.PIPE,
                             stderr=subprocess.PIPE, start_new_session=True,
                             preexec_fn=caps)
    except OSError as e:
        r.update(stop_reason='process_not_started', errno=e.errno)
    else:
        r['process_created'] = True
        sel = selectors.DefaultSelector()
        buf = {'stdout':bytearray(), 'stderr':bytearray()}
        for f,n in [(p.stdout,'stdout'),(p.stderr,'stderr')]:
            os.set_blocking(f.fileno(), False); sel.register(f, selectors.EVENT_READ,n)
        total = 0
        while sel.get_map():
            if time.monotonic()-start > LIMITS['wall_seconds']:
                r['stop_reason']='wall_timeout'; break
            for key,_ in sel.select(0.05):
                b = os.read(key.fileobj.fileno(),8192)
                if not b: sel.unregister(key.fileobj); continue
                if total+len(b) > LIMITS['combined_output_bytes']:
                    r['stop_reason']='output_limit'; break
                buf[key.data].extend(b); total += len(b)
            if r['stop_reason']: break
        if r['stop_reason']:
            try: os.killpg(p.pid,signal.SIGKILL)
            except ProcessLookupError: pass
        try: r['exit_code']=p.wait(timeout=5)
        except subprocess.TimeoutExpired:
            os.killpg(p.pid,signal.SIGKILL); r['exit_code']=p.wait(timeout=5)
            r['stop_reason']='wait_timeout'
        sel.close()
        for n in buf: r[n]=bytes(buf[n])
    r['elapsed_seconds']=round(time.monotonic()-start,6)
    return r

def parse_axioms(text: str, expected: list[str]) -> dict[str,list[str]]:
    found={}
    for name, body in re.findall(r"'([^']+)' depends on axioms:\s*\[([^\]]*)\]",text,re.S):
        if name in found: raise ValueError('duplicate axiom output')
        found[name]=sorted(x.strip() for x in body.split(',') if x.strip())
    for name in re.findall(r"'([^']+)' does not depend on any axioms",text):
        if name in found: raise ValueError('duplicate axiom output')
        found[name]=[]
    if set(found)!=set(expected): raise ValueError('axiom output declaration mismatch')
    if any(set(xs)-ALLOWED_AXIOMS for xs in found.values()):
        raise ValueError('unexpected actual axiom')
    return found

def main() -> int:
    ap=argparse.ArgumentParser()
    ap.add_argument('--lean', default=shutil.which('lean') or 'lean')
    ap.add_argument('--mathlib-dir',type=Path)
    ap.add_argument('--c31-dir',type=Path,default=ROOT.parent/'opg37364-c31-native-lock-20260907')
    ap.add_argument('--output-dir',type=Path,default=ROOT/'replay-local')
    args=ap.parse_args()
    lock=json.loads((ROOT/'input-lock.json').read_text())
    output=args.output_dir.resolve(); output.mkdir(parents=True,exist_ok=True)
    # Do not overwrite any existing command receipt.
    record_path=output/'execution.json'
    if record_path.exists(): raise ValueError('choose a new output directory')
    record=dict(format='r10-c32-native-replay-v1',verdict='candidate_only',
                started_at=datetime.now(timezone.utc).isoformat(),
                python_version=platform.python_version(),platform=platform.system(),
                driver_sha256=file_digest(Path(__file__)),input_lock_sha256=file_digest(ROOT/'input-lock.json'),
                limits=LIMITS,commands=[],compiled_modules=[],actual_axioms=None,
                actual_toolchain_fingerprint=None,dependency_heads={},source_sha256={},
                trusted_attestation=None,trusted_gate_verdict=None,status='pending')
    masks={str(ROOT):'<c32>',str(args.c31_dir.resolve()):'<c31>',str(output):'<output>',
           str(Path.home()):'<home>'}
    if args.mathlib_dir: masks[str(args.mathlib_dir.resolve())]='<mathlib>'
    def clean(s):
        for a,b in sorted(masks.items(),key=lambda x:-len(x[0])): s=s.replace(a,b)
        return s
    def run(argv,cwd,env):
        r=command(argv,cwd,env)
        saved={k:v for k,v in r.items() if k not in {'stdout','stderr','argv'}}
        saved['argv']=[clean(x) if not (j==0 and Path(x).is_absolute()) else Path(x).name
                       for j,x in enumerate(argv)]
        for n in ('stdout','stderr'):
            raw=r[n]; safe=clean(raw.decode('utf-8','replace')).encode()
            name=f"command-{len(record['commands'])+1:03d}.{n}.txt"
            (output/name).write_bytes(safe)
            saved[n+'_raw_sha256']=digest(raw)
            saved[n+'_saved_sha256']=digest(safe)
            saved[n+'_locator']=name
            saved[n+'_sanitized']=safe!=raw
        record['commands'].append(saved)
        return r
    def finish(status,code):
        record['status']=status
        record['finished_at']=datetime.now(timezone.utc).isoformat()
        record_path.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
        print(json.dumps({'status':status,'verdict':'candidate_only',
                          'compiled_modules':record['compiled_modules']}))
        return code
    env=os.environ.copy()
    env.update(LEAN_NUM_THREADS='1',OMP_NUM_THREADS='1',OPENBLAS_NUM_THREADS='1')
    try:
        sources={}
        for rel,wanted in lock['c31_sources'].items():
            p=args.c31_dir/rel
            if file_digest(p)!=wanted: return finish('frozen_c31_hash_mismatch',2)
            sources[rel]=p
        for p in sorted((ROOT/'R10').glob('*.lean')): sources['R10/'+p.name]=p
        record['source_sha256']={r:file_digest(p) for r,p in sources.items()}
        record['escape_scan']={r:sorted(set(ESCAPES.findall(strip_comments_strings(p.read_text()))))
                               for r,p in sources.items()}
        if any(record['escape_scan'].values()): return finish('source_escape_block',2)
        version=run([args.lean,'--version'],ROOT,env)
        if not version['process_created']: return finish('missing_local_lean_process',2)
        if version['exit_code']!=0 or 'version 4.19.0' not in version['stdout'].decode():
            return finish('version_mismatch',2)
        gh=run([args.lean,'--githash'],ROOT,env)
        if gh['exit_code']!=0 or gh['stdout'].decode().strip()!=lock['lean_commit']:
            return finish('compiler_commit_unconfirmed',2)
        executable=Path(shutil.which(args.lean) or args.lean).resolve()
        lib=executable.parent.parent/'lib/lean/libleanshared.so'
        if not lib.is_file(): return finish('native_shared_library_unresolved',2)
        record['actual_toolchain_fingerprint']={
            'lean_executable_sha256':file_digest(executable),
            'libleanshared_sha256':file_digest(lib),
            'reported_commit':gh['stdout'].decode().strip()}
        if args.mathlib_dir is None: return finish('installed_mathlib_path_missing',2)
        m=args.mathlib_dir.resolve()
        packages={'mathlib':m}
        for name in lock['transitive_commits']:
            choices=[m/'.lake/packages'/name,m.parent/name]
            p=next((p for p in choices if (p/'.git').exists()),None)
            if p is None: return finish('dependency_checkout_missing:'+name,2)
            packages[name]=p
        expected={'mathlib':lock['mathlib_commit'],**lock['transitive_commits']}
        paths=[]
        for name,p in packages.items():
            masks[str(p)]='<dependency:'+name+'>'
            r=run(['git','-C',str(p),'rev-parse','HEAD'],ROOT,env)
            if r['exit_code']!=0 or r['stdout'].decode().strip()!=expected[name]:
                return finish('dependency_commit_mismatch:'+name,2)
            record['dependency_heads'][name]=r['stdout'].decode().strip()
            dirty=run(['git','-C',str(p),'diff','--quiet','HEAD','--'],ROOT,env)
            if dirty['exit_code']!=0: return finish('tracked_dependency_source_dirty:'+name,2)
            paths.append(str(p/'.lake/build/lib/lean'))
        with tempfile.TemporaryDirectory(prefix='r10-c32-') as temporary:
            capsule=Path(temporary); masks[str(capsule)]='<capsule>'
            src=capsule/'src'; out=capsule/'out'
            (src/'R10').mkdir(parents=True); (out/'R10').mkdir(parents=True)
            for rel,p in sources.items(): (src/rel).write_bytes(p.read_bytes())
            env['LEAN_PATH']=os.pathsep.join([str(out),*paths])
            def build(module):
                rel=module.replace('.','/')
                r=run([str(executable),'-j1','-o',str(out/(rel+'.olean')),rel+'.lean'],src,env)
                if r['exit_code']!=0: return False
                record['compiled_modules'].append({'module':module,'source_sha256':record['source_sha256'][rel+'.lean'],
                                                    'olean_sha256':file_digest(out/(rel+'.olean'))})
                return True
            for module in OLD_MODULES:
                if not build(module): return finish('c31_module_rejected:'+module,2)
            def audit(rel):
                r=run([str(executable),'-j1',rel],src,env)
                if r['exit_code']!=0: raise ValueError('axiom_command_failed:'+rel)
                expected=re.findall(r'^#print axioms (\S+)$',(src/rel).read_text(),re.M)
                return parse_axioms(r['stdout'].decode(),expected)
            record['actual_axioms']={'c31':audit('R10/AxiomAudit.lean')}
            for module in NEW_MODULES:
                if not build(module): return finish('c32_module_rejected:'+module,2)
            record['actual_axioms']['c32']=audit('R10/HitAudit.lean')
        return finish('local_slice_replayed_not_trusted_closure',0)
    except (OSError,ValueError,KeyError) as e:
        record['error_class']=type(e).__name__
        record['error_summary']=clean(str(e))
        return finish('replay_error',2)

if __name__=='__main__':
    raise SystemExit(main())
