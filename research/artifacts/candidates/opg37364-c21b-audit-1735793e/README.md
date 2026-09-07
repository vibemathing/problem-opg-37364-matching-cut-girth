# R10 C21B 固定候选审计包

`RESULT_CANDIDATE_READY / full-refutation-proof-drafted`；`verdict=candidate_only`。

本包针对仓库 revision `1735793e9f60d9d003e8948b350cfc09efd8a7ea` 的 C20 → C21A → C21B，以及 C22 计数接口。不是一次新构造路线，也不重复旧运输库存。`proof.md` 给出自包含常规证明，`audit-matrix.json` 分离 A–G 自然语言完成与受信检查 pending，`mutations.md` 列出主动攻击与精确负控制。

## 实际执行

本轮在 CPython 3.13.5、Linux 上实际运行四个主模式，并在独立子目录运行一次共享路径字段审计。仅 Python 标准库、整数及 Fraction；没有 Lean、SMT、谱程序、随机采样器或受信 verifier。首次 smoke 运行先检查基础原语，随后运行 arithmetic、cycles 和 graphs。

在本目录中使用 Linux Python 重放：

```sh
python3 bounded_runner.py smoke
python3 bounded_runner.py arithmetic
python3 bounded_runner.py cycles
python3 bounded_runner.py graphs
(cd overlap-path-audit && python3 bounded_runner.py cycles)
```

运行器对每个 checker 子进程实施：wall-time 40 秒、CPU 35 秒、地址空间 256 MiB、stdout/stderr 合计 128 KiB、单文件输出 128 KiB、线程环境设为 1。checker 不启动子进程、不开网络、不写外部文件。每个模式保存精简 JSON、空/有限 stderr、执行记录三个文件。重放会覆盖同名观察文件；保留本次记录时，应先在独立副本中重放，不要覆盖已冻结的来源记录。

补充程序明确区分“至少两条公共边”与“含两个相邻公共边的路径”，并以输入内 SHA-256 绑定主 checker；原始输出不被覆盖。

每个 `*.execution.json` 含实际开始/结束时间、Python 版本、资源限制、代码/输入/输出/runner SHA-256、退出状态、CPU/内存观测和局限。`manifest.sha256` 是全包内容校验，不是数学验收。

## 范围

小参数穷举、局部交换与 mutation 检查只验证指定的有限范围。没有执行真实巨大 N 的置换选择器，也没有从小 N 推出一般定理。一般证明必须逐段复核 `proof.md`。以 C22 的 N=2,q=24 为例，程序按 25 个类型的二项式权重精确聚合，并非直接枚举 16,777,216 个 tuples。

本包是当前用户明确要求的本地有界自检；没有调用仓库的工作流 dispatch 或扩大 fixture verifier 权限。repo Web connector 中的 command_execution 字段不被改写为本地受信工具授权。`best_verified_result=none`，`best_verified_candidate=none`，两个 admitted obligations 在受信状态上仍开放。

## 来源冻结与持久化

`frozen-inputs.json` 固定每份已读仓库文件的 revision 和 Git blob；对 C21A/B 额外重算原始字节 SHA-256 并匹配远端 blob。未重算的来源摘要如实标明 declared 或 not_recomputed。原始候选未修改。

本轮三次有界 GitHub 工具发现均未暴露写动作，最后的完整 48 项工具列表也无 branch/create/update/comment/merge 写接口；安装的 GitHub 插件已确认，且本地未安装 GitHub CLI。因此本包尚未写入 GitHub，未创建 branch、PR 或 Issue 评论。`checkpoint.json` 保存可继续的材料状态，而不是远端成功回执。下一次可写通道应先 fresh-read main/Issue #3，按唯一 candidate_id 去重，再构造单一 live packet；不要把这里没有建立的分支或 PR 当成现成事务。
