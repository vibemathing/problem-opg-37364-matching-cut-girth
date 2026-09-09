"""C35 offline successor replay using the frozen C34 bounded native runner.

Probe success is not Lean success. No network acquisition or repository write.
The native success path is untested until actual execution records say otherwise.
"""
import argparse, hashlib, importlib.util, json, os, pathlib, platform, re, shutil, sys
from datetime import datetime, timezone
ROOT=pathlib.Path(__file__).resolve().parent
C34="research/artifacts/candidates/opg37364-c34-classification-f9d7956e"
def sha(b): return hashlib.sha256(b).hexdigest()
def save(p,x): p.write_text(json.dumps(x,indent=2,ensure_ascii=False)+"\n")
def lean_code(text):
    out=[];depth=0;i=0
    while i<len(text):
        if depth:
            if text.startswith("/-",i):depth+=1;i+=2
            elif text.startswith("-/",i):depth-=1;i+=2
            else:i+=1
        elif text.startswith("/-",i):depth=1;i+=2
        elif text.startswith("--",i):
            j=text.find("\n",i);i=len(text) if j<0 else j
        else:out.append(text[i]);i+=1
    if depth:raise ValueError("unclosed comment")
    return "".join(out)
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--repo-root",type=pathlib.Path)
    ap.add_argument("--mathlib-root",type=pathlib.Path)
    ap.add_argument("--lean",type=pathlib.Path)
    ap.add_argument("--output",type=pathlib.Path,required=True)
    ap.add_argument("--probe-only",action="store_true")
    a=ap.parse_args();out=a.output.resolve();out.mkdir(parents=True,exist_ok=True)
    lock=json.loads((ROOT/"input-lock.json").read_text())
    rec={"format":"r10-c35-native-replay-v1","verdict":"candidate_only",
         "started_at":datetime.now(timezone.utc).isoformat(),
         "python_version":platform.python_version(),"platform":platform.system(),
         "driver_sha256":sha(pathlib.Path(__file__).read_bytes()),
         "input_lock_sha256":sha((ROOT/"input-lock.json").read_bytes()),
         "available_tools":{n:bool(shutil.which(n)) for n in ("lean","lake","elan")},
         "native_compiler_started":False,"commands":[],"compiled_modules":[],
         "actual_axioms":None,"actual_toolchain_fingerprint":None,
         "trusted_gate_verdict":None,"first_error":None}
    def finish(status,code):
        rec.update(status=status,driver_exit_code=code,finished_at=datetime.now(timezone.utc).isoformat())
        save(out/"execution.json",rec)
        print(json.dumps({"status":status,"native_compiler_started":rec["native_compiler_started"]}))
        return code
    rec["source_sha256"]={}
    rec["escape_scan"]={}
    for name,digest in lock["new_lean_sources"].items():
        data=(ROOT/name).read_bytes();rec["source_sha256"][name]=sha(data)
        if sha(data)!=digest:return finish("new_source_digest_mismatch:"+name,2)
        rec["escape_scan"][name]=re.findall(
            r"\b(?:sorry|admit|axiom|unsafe|native_decide|implemented_by|extern|run_tac)\b|#eval|#reduce",
            lean_code(data.decode("utf-8")))
    if any(rec["escape_scan"].values()):return finish("source_hygiene_block",2)
    if a.probe_only:return finish("probe_only_no_native_compilation",0)
    if not a.lean or not a.lean.is_file():return finish("explicit_native_environment_not_present",2)
    if not a.repo_root or not a.mathlib_root:return finish("explicit_locked_paths_required",2)
    repo=a.repo_root.resolve();mathlib=a.mathlib_root.resolve();lean=a.lean.resolve();legacy=repo/C34
    for path,digest in lock["frozen_files"].items():
        if sha((repo/path).read_bytes())!=digest:return finish("frozen_input_digest_mismatch:"+path,2)
    sys.path.insert(0,str(legacy))
    spec=importlib.util.spec_from_file_location("c34_native_replay",legacy/"replay_locked.py")
    runner=importlib.util.module_from_spec(spec);spec.loader.exec_module(runner)
    rec["limits"]=runner.LIMITS
    prior_argv=sys.argv[:];baseout=out/"c34";old_code=2
    sys.argv=[str(legacy/"replay_locked.py"),"--repo-root",str(repo),
              "--mathlib-root",str(mathlib),"--lean",str(lean),"--output",str(baseout)]
    try:
        try:runner.main()
        except SystemExit as e:old_code=e.code
    finally:sys.argv=prior_argv
    old=json.loads((baseout/"execution.json").read_text())
    rec["legacy_execution_sha256"]=sha((baseout/"execution.json").read_bytes())
    rec["native_compiler_started"]=any(c["process_created"] for c in old["commands"])
    rec["legacy_status"]=old["status"]
    rec["actual_toolchain_fingerprint"]=old["actual_toolchain_fingerprint"]
    if old_code!=0:
        bad=next((c for c in old["commands"] if c["exit_code"]!=0 or c["stop_reason"]),None)
        if bad:
            lines=[]
            for stream in ("stdout","stderr"):
                path=baseout/bad[stream]["locator"]
                if path.is_file():lines+=path.read_text().splitlines()
            rec["first_error"]=next((s for s in lines if "error:" in s),bad["stop_reason"])
            rec["first_failed_command"]=bad["argv"]
        return finish("stopped_at_frozen_dependency_error",2)
    work=baseout/"work"
    env=os.environ.copy();env.update(OMP_NUM_THREADS="1",OPENBLAS_NUM_THREADS="1",LEAN_NUM_THREADS="1")
    manifest=json.loads((mathlib/"lake-manifest.json").read_text())
    paths=[work,mathlib/".lake/build/lib/lean"]+[
        mathlib/".lake/packages"/p["name"]/".lake/build/lib/lean" for p in manifest["packages"]]
    env["LEAN_PATH"]=os.pathsep.join(map(str,paths))
    def scrub(s):
        for p,t in sorted([(str(repo),"<repository>"),(str(mathlib),"<mathlib>"),
                (str(lean),"<lean>"),(str(out),"<output>"),(str(ROOT),"<candidate>")],key=lambda x:-len(x[0])):
            s=s.replace(p,t)
        return s
    for name in lock["new_lean_sources"]:
        p=work/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes((ROOT/name).read_bytes())
    for name in ["R10/C35FiniteColors.lean","R10/C35WitnessEquiv.lean","R10/C35RankBridge.lean","R10/C35AxiomAudit.lean"]:
        argv=[str(lean),"-j1"]
        if "Audit" not in name:argv+=["-o",str(pathlib.Path(name).with_suffix(".olean"))]
        argv.append(name)
        r,t=runner.run(argv,work,env,out,len(rec["commands"])+1,scrub);rec["commands"].append(r)
        if r["exit_code"]!=0 or r["stop_reason"]:
            rec["first_failed_source"]=name
            rec["first_error"]=next((x for x in (t["stdout"]+"\n"+t["stderr"]).splitlines() if "error:" in x),r["stop_reason"])
            return finish("stopped_at_first_new_compiler_error",2)
        rec["compiled_modules"].append(name)
        if "Audit" in name:
            expected=re.findall(r"^#print axioms\s+(\S+)",(ROOT/name).read_text(),re.M)
            rec["actual_axioms"]={}
            for decl in expected:
                m=re.search(re.escape(decl)+r"'?\s+depends on axioms:\s*\[([^\]]*)\]",t["stdout"],re.S)
                if m:xs=[x.strip() for x in m.group(1).split(",") if x.strip()]
                elif re.search(re.escape(decl)+r"'?\s+does not depend on any axioms",t["stdout"]):xs=[]
                else:return finish("named_axiom_output_missing:"+decl,2)
                if set(xs)-{"propext","Classical.choice","Quot.sound"}:return finish("unexpected_axioms:"+decl,2)
                rec["actual_axioms"][decl]=xs
    return finish("native_slice_replayed_candidate_only",0)
if __name__=="__main__":raise SystemExit(main())
