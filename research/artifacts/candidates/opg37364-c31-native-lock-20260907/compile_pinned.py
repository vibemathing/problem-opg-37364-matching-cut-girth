"""Bounded native Lean replay; source resolution is not a successful build."""
from __future__ import annotations
import argparse, hashlib, json, os, pathlib, platform, re, resource
import selectors, shutil, signal, subprocess, sys, time
from datetime import datetime, timezone

ROOT = pathlib.Path(__file__).resolve().parent
LIMITS = {"wall_seconds": 120, "cpu_seconds": 90,
          "memory_bytes": 2147483648, "combined_output_bytes": 131072,
          "thread_environment": 1}
MODULES = ["R10.CompletionEquiv", "R10.CompletionCardinality", "R10.ProductCounts"]

def sha(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()

def run(argv: list[str]) -> dict:
    started = time.monotonic()
    result = {"argv": argv, "process_created": False, "exit_code": None,
              "stdout": "", "stderr": "", "stop_reason": None}
    def caps():
        resource.setrlimit(resource.RLIMIT_CPU, (90, 90))
        resource.setrlimit(resource.RLIMIT_AS, (2147483648, 2147483648))
    env = os.environ.copy()
    env.update(OMP_NUM_THREADS="1", OPENBLAS_NUM_THREADS="1", LEAN_NUM_THREADS="1")
    try:
        proc = subprocess.Popen(argv, cwd=ROOT, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, start_new_session=True,
                                preexec_fn=caps)
    except OSError as exc:
        result.update(stop_reason="process_not_started", errno=exc.errno)
    else:
        result["process_created"] = True
        sel = selectors.DefaultSelector()
        for stream, name in ((proc.stdout, "stdout"), (proc.stderr, "stderr")):
            os.set_blocking(stream.fileno(), False)
            sel.register(stream, selectors.EVENT_READ, name)
        buffers = {"stdout": bytearray(), "stderr": bytearray()}
        total = 0
        while sel.get_map():
            if time.monotonic() - started > LIMITS["wall_seconds"]:
                result["stop_reason"] = "timeout"
                break
            for key, _ in sel.select(0.05):
                part = os.read(key.fileobj.fileno(), 8192)
                if not part:
                    sel.unregister(key.fileobj)
                    continue
                if total + len(part) > LIMITS["combined_output_bytes"]:
                    result["stop_reason"] = "output_limit"
                    break
                total += len(part)
                buffers[key.data].extend(part)
            if result["stop_reason"]:
                break
        if result["stop_reason"]:
            try:
                os.killpg(proc.pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        result["exit_code"] = proc.wait(timeout=5)
        sel.close()
        for name, buf in buffers.items():
            result[name + "_raw_sha256"] = sha(bytes(buf))
            result[name] = bytes(buf).decode("utf-8", "replace").replace(str(ROOT), "<project>")
    result["elapsed_seconds"] = round(time.monotonic() - started, 6)
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--resolve", action="store_true",
                        help="allow the pinned Lake dependency download before replay")
    args = parser.parse_args()
    lock = json.loads((ROOT / "resolved-source-lock.json").read_text())
    sources = {p.relative_to(ROOT).as_posix(): sha(p.read_bytes())
               for p in sorted(ROOT.rglob("*.lean")) if ".lake" not in p.parts}
    source_text = "\n".join((ROOT / p).read_text() for p in sources)
    # This is a conservative textual control, not an axiom or kernel audit.
    escapes = sorted(set(re.findall(r"\b(?:sorry|admit|unsafe|axiom|native_decide|extern|implemented_by)\b|#eval", source_text)))
    record = {"format": "r10-c31-native-build-attempt-v1", "verdict": "candidate_only",
              "started_at": datetime.now(timezone.utc).isoformat(),
              "python_version": platform.python_version(), "platform": platform.system(),
              "driver_sha256": sha(pathlib.Path(__file__).read_bytes()),
              "source_sha256": sources, "source_lock_sha256": sha((ROOT / "resolved-source-lock.json").read_bytes()),
              "limits": LIMITS, "commands": [], "compiled_modules": [],
              "actual_toolchain_fingerprint": None, "actual_axioms": None,
              "trusted_gate_verdict": None, "status": "pending", "literal_escape_tokens": escapes}
    def finish(status: str, code: int) -> int:
        record["status"] = status
        text = json.dumps(record, indent=2, ensure_ascii=False) + "\n"
        (ROOT / "native-build-attempt.json").write_text(text)
        print(text, end="")
        return code
    if escapes:
        return finish("source_hygiene_block", 2)
    # The actual attempted command distinguishes ENOENT from a Lean rejection.
    version = run(["lake", "env", "lean", "--version"])
    record["commands"].append(version)
    if not version["process_created"]:
        record["available_native_tools"] = {x: bool(shutil.which(x)) for x in ("lean", "lake", "elan")}
        return finish("missing_native_toolchain", 2)
    if version["exit_code"] != 0 or "version 4.19.0" not in version["stdout"]:
        return finish("toolchain_version_rejected", 2)
    if lock["lean_commit"][:12] not in version["stdout"]:
        return finish("toolchain_commit_unconfirmed", 2)
    if args.resolve:
        update = run(["lake", "update"])
        record["commands"].append(update)
        if update["exit_code"] != 0:
            return finish("dependency_resolution_failed", 2)
    wanted = {"mathlib": lock["mathlib_commit"], **lock["transitive_commits"]}
    for name, commit in wanted.items():
        check = run(["git", "-C", ".lake/packages/" + name, "rev-parse", "HEAD"])
        record["commands"].append(check)
        if check["exit_code"] != 0 or check["stdout"].strip() != commit:
            return finish("dependency_commit_mismatch:" + name, 2)
    path_result = run(["lake", "env", "which", "lean"])
    record["commands"].append(path_result)
    if path_result["exit_code"] != 0:
        return finish("native_binary_unresolved", 2)
    native = pathlib.Path(path_result["stdout"].strip())
    if not native.is_file():
        return finish("native_binary_unavailable", 2)
    record["actual_toolchain_fingerprint"] = sha(native.read_bytes())
    for module in MODULES:
        build = run(["lake", "build", module])
        record["commands"].append(build)
        if build["exit_code"] != 0:
            return finish("module_build_failed:" + module, 2)
        record["compiled_modules"].append(module)
    audit = run(["lake", "env", "lean", "R10/AxiomAudit.lean"])
    record["commands"].append(audit)
    if audit["exit_code"] != 0:
        return finish("axiom_print_failed", 2)
    lists = re.findall(r"depends on axioms:\s*\[([^\]]*)\]", audit["stdout"], re.S)
    empty_lists = audit["stdout"].count("does not depend on any axioms")
    if len(lists) + empty_lists != 9:
        return finish("axiom_output_incomplete", 2)
    record["actual_axioms"] = sorted({x.strip() for xs in lists for x in xs.split(",") if x.strip()})
    if set(record["actual_axioms"]) - {"propext", "Quot.sound", "Classical.choice"}:
        return finish("unexpected_axioms", 2)
    return finish("local_native_slice_replayed_not_trusted_admission", 0)

if __name__ == "__main__":
    raise SystemExit(main())
