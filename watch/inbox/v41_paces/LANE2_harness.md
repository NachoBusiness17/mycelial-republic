# LANE 2/8 — HARNESS REPLICATION (V4.1-Flash across agent scaffolds)

Filed: 2026-09-10, zcode seat, triparty v41_paces wave.
Source: `docs/report_v1/sources/DeepSeek_V41_Flash_tech_report.pdf` (51 pp), section 5.3.4
+ Table 4 (p.34), evaluation setup 5.3.1 (p.32), Appendix B.1 (pp.46-47), Appendix B.2 (p.47).

---

## THE POINT

DeepSeek's own scaffold sweep (Table 4) shows V4.1-Flash peaking in the two MINIMAL
harnesses — mini-SWE (single bash tool) and DSH Minimal (single bash tool) — and
dipping in every heavy scaffold (Claude Code, Codex, OpenCode, Pi, DSH Standard/PTC).
The fleet hypothesis — "V4.1 Flash hits peak numbers inside our organs" — is
DIRECTIONALLY SUPPORTED but with a correction: the report itself frames this as
*robustness* (all configs within ~4.4 pts), not as heavy-harness failure. And our
organs are not *in* their minimal bucket — they are one notch BELOW it (zero tools,
stateless single-shot). To claim their minimal numbers we must add exactly one tool
and run multi-turn. Also load-bearing: DeepSeek themselves switch to the HEAVY
Claude Code harness for SEC-Bench Pro "specifically for its session compact design"
(5.3.1) — minimal wins peak pass-rate, heavy wins when context management is the job.

**Viral-post tri-state:** @zainhas's claim (47.6K views) "best in minimal, underperforms
in Claude Code/Codex" = SUPPORTED on ordering, OVERSTATED on magnitude (deltas at Max
effort: +4.4 pts DeepSWE, +2.6 pts TB2.1, mini-SWE vs Claude Code).

---

## THE 8-CONFIG TABLE (report Table 4, verbatim)

Max reasoning effort (100). Held constant across ALL configs: model checkpoint,
temperature 1.0, top-p 0.95, 1M-token context window, max_steps=500 model-generation
rounds, Linux containers, N=8 samples/task (DeepSWE v1.1), N=3 (Terminal-Bench v2.1),
TB2.1 offline. Claude Code row = v2.1.251 (4 versions tested; avg 68.9 / 87.8).

| # | Scaffold (version)            | DeepSWE v1.1 (Resolved %) | TB v2.1 (Pass@1 %) |
|---|-------------------------------|---------------------------|--------------------|
| 1 | Claude Code (v2.1.251)        | 69.8                      | 88.0               |
| 2 | Codex (v0.147.0)              | 65.6                      | 84.1               |
| 3 | OpenCode (v1.18.15)           | 65.5                      | 85.0               |
| 4 | Pi (v0.84.2)                  | 66.2                      | 86.1               |
| 5 | mini-SWE (mini_swe_v2, 04d809ce) | **74.2**               | 90.3               |
| 6 | DSH **Minimal**               | 72.6                      | **90.6**           |
| 7 | DSH Standard                  | 70.5                      | 85.8               |
| 8 | DSH PTC                       | 67.6                      | 85.8               |

Spread: minimal bucket beats worst scaffold by **8.7 pts** (DeepSWE) and **6.5 pts**
(TB2.1). Appendix B.2 adds: on TB2.1 at max effort the ordering is DSH Minimal >
mini-SWE > Claude Code — "scaffold choice matters at least as much as the effort tier
once the task is nearly saturated." On DeepSWE the minimal curves start LOWEST at low
effort and gain the MOST by effort 100 — the minimal-harness advantage is
effort-dependent, not constant.

---

## WHAT "MINIMAL HARNESS" MEANS PER THE REPORT

From 5.3.4 + B.1 ("We add no experimental system prompt"):

- **System prompt:** the scaffold's NATIVE prompt/task-template only — zero added
  experimental prompt. (Absolute sizes are NOT published — prompt-token claims are
  UNPROVEN; the structural claims below are SUPPORTED.)
- **Tool count:** Minimal = **exactly one tool** (bash). mini-SWE = one bash tool,
  a tool call REQUIRED every turn, finish via submission marker. Contrast: DSH
  Standard = full sdk profile, 26 initial function tools (incl. web search/fetch);
  DSH PTC = `run_code` TypeScript over 24 underlying tools; Pi = file+shell+3 search
  tools; OpenCode = shell+file+task delegation; Claude Code = full native SDK surface.
- **Context structure:** one flat append-only trajectory in a 1M window, 500
  generation rounds ceiling; no compaction layer credited in the minimal configs.
- **Interaction protocol:** model acts through the tool loop; the harness normalizes
  nothing but the trajectory schema (their DSec worker layer).

Minimal bucket, one line: **1 tool + native-short prompt + flat context + forced
act-every-turn loop.**

---

## OUR HARNESS SHAPE vs THEIR MINIMAL

What a V4.1-Flash call inside fleet organs actually is (measured, this repo):

| Dimension        | Their Minimal / mini-SWE            | Our organs                                    | Verdict |
|------------------|-------------------------------------|-----------------------------------------------|---------|
| Tools            | 1 (bash, forced each turn)          | **0** — `mag/ractor_vessels.py:69` calls `chat_provider(system, user)`, no tools param; `models/providers.py:250` chat_provider has no tools arg at all | we are SUB-minimal |
| Turns            | up to 500 rounds                    | 1, stateless per firing ("the mask is the memory, the steer is the moment") | sub-minimal |
| System prompt    | native scaffold, size unpublished    | header (~120 chars) + lens head capped 1800 chars + voice laws (~700) ≈ ≤2.6K chars ≈ ~650 tok | plausibly SHORTER than any of their 8 |
| Max_tokens       | long-horizon trajectories           | 200 (ractor fire)                             | different regime |
| Multi-turn tools | standard                            | exists but opt-in: `models/providers.py:568` `chat_messages(..., tools=None)` used by supervisor/agent_cli/desk organs; per-organ tool counts UNMEASURED (small by design) | bridge exists |
| Context window   | 1M                                  | lane-default                                  | match if lane permits |

**Would we sit in their minimal bucket?** No — we'd sit in an untested ZERO-tool,
single-turn bucket below it. Their own sweep never runs that arm. Two consequences:
1. For non-interactive tasks (strike generation, judging, folding) our shape is a
   clean subset of minimal — the minimal-harness peak is the best available proxy
   for our ceiling, and the hypothesis "peak numbers inside our organs" is testable
   exactly as the replication below.
2. For agentic (repo-surgery) tasks, zero tools cannot resolve any benchmark task;
   the honest claim is "our PROMPT scaffold + 1 bash tool ≈ their Minimal." The
   organ pattern (single file, stateless, append-only log) maps 1:1 onto mini-SWE's
   ~100-line loop — our replication arm can be one more organ.

---

## REPLICATION SPEC (our own run)

**Claim under test:** V4.1-Flash scored inside fleet-shaped harnesses lands within
noise of the report's minimal-bucket numbers (72.6-74.2 DeepSWE-class / 90.3-90.6
TB-class), i.e. our organs sit at the peak, not below it.

**Lane:** GOPHER (deepseek via `mag/fuel_feed.py` + `configs/` — keys never echoed,
never read into prompts). RACTOR lane is reserved for the zero-tool arm's smoke test.

**Held constant (mirror their protocol, report Note to Table 4):** one model
checkpoint; temperature 1.0; top-p 0.95; max context the lane allows (record actual);
max_steps 500 rounds for the tool arms; Linux container semantics via repo-local
sandbox; network OFF during task execution; git history stripped; build caches
purged before run (their anti-hack config, 5.3.1); N=3 samples/task minimum (their
TB setting), N=8 if lane budget allows (their DeepSWE setting).

**Arms — tasks identical, ONLY the harness changes:**
- **Arm A (their Minimal, replicated):** single `bash` tool via
  `chat_messages(tools=[bash_schema])`, tool call required every turn, finish on a
  `SUBMIT:` marker, system prompt = task description verbatim, nothing added.
- **Arm B (our organ shape):** zero-tool single-shot, ractor_vessels-style fire —
  system = task spec head, user = task + output contract, max_tokens 200-class.
  Runs only on tasks gradeable without environment interaction (the proxy suite's
  judgment rows).
- **Arm C (the bridge):** our organ scaffold (voice/spec header + lens head) PLUS
  exactly the one bash tool of Arm A. This is the arm the fleet hypothesis lives on.

**Task set:** repo-local proxy, TB-shaped — surgery tasks with fail-to-pass
verification points in this repo (cite_gate-style checks, canon_seal spot checks,
fold repairs), each with a deterministic verifier script. We cannot cheaply run
DeepSWE/TB2.1 proper on the lanes; per repo law the proxy is named as a proxy and
numbers are never compared 1:1 to Table 4 — only ARM vs ARM inside our run.

**Scoring:** pass@1 per arm per task, mean over N samples; record latency and
output tokens per trajectory (mirrors their Fig. 11 axes).

**Falsifiers (pre-registered, tesuji convention):**
- SUPPORTED if Arm C within 2 pts of Arm A on the proxy suite.
- DISPUTED (our shape costs points) if Arm A beats Arm C by >4 pts — then the
  fix is: strip the organ scaffold down to their native-prompt bareness, rerun.
- Sub-prediction from B.2: at LOW effort-equivalent settings Arm A may trail
  heavier scaffolds; test one low-budget pass before declaring anything.

**Logging:** raw rows to `memory/runs/v41_paces/` (schema `v41_paces.v1`: arm, task,
sample, pass, tokens, latency_ms, ts); verdict lands tri-state on the wave board;
this file is the only card. Build freeze respected: Arm A/C is ONE organ file
(~100 lines, mini-SWE-shaped) — spawn only on operator GO, per the launch law's
coldest-vertex gate.

**Tri-state ledger for this lane:**
- 8-config numbers + held-constant protocol: SUPPORTED (report Table 4, pp.34, 47).
- "Minimal = 1 tool, no added prompt, flat 1M context": SUPPORTED (B.1).
- Prompt token sizes per scaffold: UNPROVEN (not published anywhere in the report).
- "V4.1-Flash peaks in our organs": UNPROVEN until the spec above runs.
