"""POSIX bounded launcher for the candidate-only C21B checks; no network."""
from __future__ import annotations
import hashlib
import json
import os
import platform
import resource
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
DIR = Path("research/artifacts/candidates")
CODE = DIR / "opg37364-c21b-audit-checker.py"
INPUT = DIR / "opg37364-c21b-audit-input.json"
OUTPUT = DIR / "opg37364-c21b-audit-output.json"
LOG = DIR / "opg37364-c21b-audit-execution.json"
STDERR = DIR / "opg37364-c21b-audit-stderr.txt"
LIMITS = {"wall_seconds":45,"cpu_seconds":40,"address_space_bytes":536870912,
          "stdout_bytes":65536,"stderr_bytes":65536,"threads":1}


def restrict() -> None:
    resource.setrlimit(resource.RLIMIT_CPU, (40,40))
    resource.setrlimit(resource.RLIMIT_AS, (536870912,536870912))
    resource.setrlimit(resource.RLIMIT_FSIZE, (65536,65536))
    resource.setrlimit(resource.RLIMIT_CORE, (0,0))


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    os.chdir(ROOT)
    env = os.environ.copy()
    env.update({"PYTHONHASHSEED":"0","OMP_NUM_THREADS":"1","OPENBLAS_NUM_THREADS":"1"})
    start = datetime.now(timezone.utc).isoformat(); tick = time.monotonic()
    timed_out = False
    with OUTPUT.open("wb") as out, STDERR.open("wb") as err:
        child = subprocess.Popen([sys.executable,str(CODE),str(INPUT)],stdout=out,stderr=err,
                                 env=env,preexec_fn=restrict)
        try:
            code = child.wait(timeout=45)
        except subprocess.TimeoutExpired:
            timed_out = True; child.kill(); code = child.wait()
    record = {"format":"bounded-generator-execution-v1","verdict":"candidate_only",
              "command":["python3",str(CODE),str(INPUT)],
              "launcher":str(DIR / "opg37364-c21b-audit-runner.py"),
              "code_sha256":digest(CODE),"launcher_sha256":digest(Path(__file__)),
              "input_sha256":digest(INPUT),"output_sha256":digest(OUTPUT),
              "stderr_sha256":digest(STDERR),"output_bytes":OUTPUT.stat().st_size,
              "stderr_bytes":STDERR.stat().st_size,"exit_code":code,"timed_out":timed_out,
              "limits":LIMITS,"started_at":start,"duration_seconds":round(time.monotonic()-tick,6),
              "python_version":platform.python_version(),"python_implementation":platform.python_implementation(),
              "python_build":platform.python_build(),"python_compiler":platform.python_compiler(),
              "dependencies":"Python standard library only",
              "runtime_lane":"User-requested local bounded checks, not a GitHub command-execution capability or a trusted registered verifier.",
              "limitations":"Finite controls only. No C20 selector at general size, Lean, SMT or universal theorem verification executed."}
    LOG.write_text(json.dumps(record,sort_keys=True,indent=2)+"\n")
    print(json.dumps({k:record[k] for k in ("exit_code","timed_out","duration_seconds","output_bytes","stderr_bytes","code_sha256","input_sha256","output_sha256")},indent=2))
    if code:
        print(STDERR.read_text()[-3000:])
        raise SystemExit(1)

if __name__ == "__main__":
    main()
