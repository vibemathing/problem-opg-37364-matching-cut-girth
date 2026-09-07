"""Bounded local runner; records observations, never a registered verifier receipt."""
from __future__ import annotations
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import resource
import selectors
import subprocess
import sys
import time

WALL_SECONDS = 40
CPU_SECONDS = 35
MEMORY_BYTES = 256 * 1024 * 1024
OUTPUT_CAP = 131072
THREADS = 1


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def limits() -> None:
    resource.setrlimit(resource.RLIMIT_AS, (MEMORY_BYTES, MEMORY_BYTES))
    resource.setrlimit(resource.RLIMIT_CPU, (CPU_SECONDS, CPU_SECONDS))
    resource.setrlimit(resource.RLIMIT_FSIZE, (OUTPUT_CAP, OUTPUT_CAP))
    resource.setrlimit(resource.RLIMIT_NOFILE, (64, 64))
    resource.setrlimit(resource.RLIMIT_CORE, (0, 0))


def run(mode: str) -> dict:
    cwd = Path(__file__).resolve().parent
    env = dict(os.environ)
    env.update({'PYTHONDONTWRITEBYTECODE':'1', 'PYTHONHASHSEED':'0',
                'OMP_NUM_THREADS':'1', 'OPENBLAS_NUM_THREADS':'1', 'MKL_NUM_THREADS':'1'})
    command = [sys.executable, 'checker.py', '--input', 'input.json', '--mode', mode]
    started = datetime.now(timezone.utc).isoformat()
    before_usage = resource.getrusage(resource.RUSAGE_CHILDREN)
    start = time.monotonic()
    proc = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, preexec_fn=limits)
    sel=selectors.DefaultSelector()
    assert proc.stdout is not None and proc.stderr is not None
    sel.register(proc.stdout,selectors.EVENT_READ,'stdout'); sel.register(proc.stderr,selectors.EVENT_READ,'stderr')
    data={'stdout':bytearray(),'stderr':bytearray()}; stopped=None
    while sel.get_map():
        if time.monotonic()-start > WALL_SECONDS:
            stopped='wall_timeout'; proc.kill()
        for key,_ in sel.select(timeout=0.05):
            chunk=os.read(key.fileobj.fileno(),8192)
            if not chunk:
                sel.unregister(key.fileobj)
                continue
            used=len(data['stdout'])+len(data['stderr'])
            data[key.data].extend(chunk[:max(0,OUTPUT_CAP-used)])
            if used+len(chunk)>OUTPUT_CAP:
                stopped='output_cap'; proc.kill()
    code=proc.wait(timeout=2); elapsed=time.monotonic()-start
    usage=resource.getrusage(resource.RUSAGE_CHILDREN)
    stdout=bytes(data['stdout']); stderr=bytes(data['stderr'])
    (cwd/f'{mode}.output.json').write_bytes(stdout)
    (cwd/f'{mode}.stderr.txt').write_bytes(stderr)
    record={
      'format':'r10-c21b-candidate-execution-v1','verdict':'candidate_only',
      'execution_role':'candidate-generator local self-check, not registered verifier',
      'authorization':'The current user explicitly requested bounded exact-integer and synthetic controls. No GitHub workflow dispatch, registry privilege, or truth write is performed.',
      'runtime':{'implementation':platform.python_implementation(),'version':platform.python_version(),
                 'system':platform.system(),'third_party_packages':[]},
      'mode':mode,'started_at':started,'finished_at':datetime.now(timezone.utc).isoformat(),
      'command':['python3','checker.py','--input','input.json','--mode',mode],
      'limits':{'wall_seconds':WALL_SECONDS,'cpu_seconds':CPU_SECONDS,'address_space_bytes':MEMORY_BYTES,
                'combined_stdout_stderr_bytes':OUTPUT_CAP,'threads':THREADS,'file_size_bytes':OUTPUT_CAP,
                'process_count':'one checker process; checker launches no children','produced_files_max':3},
      'routing':{'device':'CPU','reason':'Small finite graph controls and exact arbitrary-precision integer arithmetic; no floating-point or GPU calculation.'},
      'elapsed_seconds':round(elapsed,6),'cpu_user_seconds':round(usage.ru_utime-before_usage.ru_utime,6),
      'max_rss_kib':usage.ru_maxrss,'exit_code':code,'forced_stop':stopped,
      'code_sha256':sha((cwd/'checker.py').read_bytes()),'runner_sha256':sha(Path(__file__).read_bytes()),
      'input_sha256':sha((cwd/'input.json').read_bytes()),'stdout_sha256':sha(stdout),'stderr_sha256':sha(stderr),
      'stdout_bytes':len(stdout),'stderr_bytes':len(stderr),
      'limitations':['Finite tests do not establish the universal A-G statements.',
                     'No Lean, SMT, mathematical-admission policy, or independent trust domain is invoked.',
                     'No enormous permutation-selector or regularization-selector instance was generated.']}
    (cwd/f'{mode}.execution.json').write_text(json.dumps(record,indent=2,sort_keys=True)+'\n')
    print(json.dumps(record,indent=2,sort_keys=True))
    if code or stopped:
        print(stderr.decode('utf-8','replace'))
        raise SystemExit(1)
    return record

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('mode',choices=['smoke','arithmetic','cycles','graphs'])
    run(p.parse_args().mode)
