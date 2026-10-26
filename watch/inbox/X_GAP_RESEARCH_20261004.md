# X_GAP_RESEARCH_20261004: new research mapped to Mag's open gaps

Filed by Grok Bot, Sun 2026-10-04 ~08:40 ET. Read-only on the PC. The only write is this file.

## Method and honesty notes
- Gap sources read: watch/inbox/gap_analysis_20261001/GAP_REGISTER.md (open rows only: 1, 5, 8-12 plus the one-wave and operator queues), ractor_engine 2026-10-04-parked-decisions, 2026-10-03-grokbot-estate and 2026-10-03-surface-migration SYNTHESIS, OPERATOR_WORKFLOW_DIVE_20261003.md, reboot_patches_20261003/APPLY_ORDER.md, ARMC_DECISION_MEMO_20261003.md. ESTATE_GAPS_20261004.json landed at ~08:33 ET (15 gaps) and is folded in below (EG-xx tags).
- Every claim below was read on the primary source this sitting: the arXiv abstract via export.arxiv.org, plus the arXiv HTML or repo README where noted. Dates are arXiv v1 dates.
- X coverage was thin, and I am saying so. The web index returned zero x.com hits for site:x.com queries. X posts were reached through unrollnow.com thread mirrors: @omarsar0 (Sep 10 KVMem, Sep 15 harness costs, Sep 22 EvoOntology) and @xeophon quoting @maksym_andr (Sep 29, trace tampering). Each one was followed to its paper. Most items here were found on arXiv and GitHub directly. Nothing was posted, liked or sent. No paid calls were made from the PC.
- Estate check: rg -F -i over watch, corpus, memory and queue for each arXiv id, title keyword and repo name, plus the state/arxiv daily abstract feed (4,262 files). The labels mean:
  - NEW: zero hits.
  - FEED-ONLY: the abstract was auto-ingested into state/arxiv/<date>/ but is never cited in any receipt.
  - NAMED-ONLY: the title appears once as an unread follow-up.
  - IN-ESTATE: cited in a receipt (I name the file).

## TOP 8 (ranked by fit x evidence x cheapness)

1. TRACE / tellonce: compile operator corrections into runtime checks. NEW.
2. Handoff Debt: a measured structured-handoff schema for zknot dossiers. NEW.
3. ContrAgent: LTLf contracts compiled to DFAs that gate online and replay offline. FEED-ONLY.
4. MemGuard: verifier output stored as persistent memory metadata. NAMED-ONLY.
5. Proof-of-Execution Memory (PoEM): a trusted-writer HMAC ledger beats forged "already done" claims. NEW.
6. Stop Means Stop / SOUNDGATE: pause, cancel and timeout primitives leak side effects. NEW.
7. PersonalBench: LLM-judge style scores are circular, so use a trained authorship model. NEW.
8. Look Before You Leap: a static pre-action shell verifier with an oracle-exact binary check. NEW.

Full entries follow, grouped by gap.

---

## GAP A: law and guardrail enforcement with logging (dive change 3 "lawlog"; GAP_REGISTER meta-gap 4; EG-09; behavior-card compliance FIRED 3 / PARTIAL 3 / IGNORED 3)

### A1. Getting Better at Working With You: Compiling User Corrections into Runtime Enforcement for Coding Agents (TRACE). Rank 1. NEW
- Primary: https://arxiv.org/abs/2606.13174 (v1 2026-06-11). Code: https://github.com/YujunZhou/tellonce (MIT, v1.7.1) and https://github.com/YujunZhou/TRACE_exp
- What it shows (verified in the paper text):
  - The access-compliance gap is real. Their diagnostic was built from ONE researcher's ~2 months of coding-agent transcripts (32 transcripts, 142 correction-conflict records), which is the same shape as Nacho's 4,727 prompts.
  - Across 6 models: no rules 31.6% compliance, all rules in context 55.0%, Mem0 42.5%, relevant rules 54.0%, rules compiled into checks 70.1%.
  - End to end on ClawArena, held-out violation fell from 100% to 37.6% in distribution and to 2.0% out of distribution. User turns fell from 2.00 to 1.37 and 1.02. Wall clock was near the no-memory baseline.
  - Each correction becomes an applicability check, a behavior instruction and a verifier, wired to prompt, tool-use, file-write or stop hooks. A failed verifier blocks the event and returns the rule text.
  - A five-action lifecycle (Noop, Update, Supersede, Split, New) maintains the library. Superseded rules are archived, not deleted.
  - The worked example is a PreToolUse-Bash regex hook that exits 2 on a violation.
- Plugs into Mag:
  - tools/seat_law_gate.py gets per-law verifiers plus the block-log jsonl that the dive found missing.
  - .agents/skills/operator-corrections/SKILL.md (stuck at law 20) becomes the compiled library.
  - tools/zknot.py dossiers are the correction stream: the 469 "self steal" and 219 "you forgot" prompts are labelled correction signals.
  - memory/rib/RIB_BEHAVIOR_CARDS_20260928.md: the IGNORED cards are exactly the access-without-compliance case.
- Effort: one sitting to port the pattern (detector over zknot prompts, atomic-rule JSON, 3 deterministic verifiers for headless, em-dash and stop-without-ball). Do NOT install tellonce as-is. By default it sends redacted turns to the platform CLI model (README), which breaks the local-only and no-paid-call rails. Port the hooks and run detection on local ollama.

### A2. Symbolic Temporal Supervision of LLM Agents Using Contracts (ContrAgent). Rank 3. FEED-ONLY (state/arxiv/2026-09-17/2609.18128v1.txt, never cited)
- Primary: https://arxiv.org/abs/2609.18128 (v1 2026-09-16). Code: https://github.com/yfxiao16/ContrAgent (Apache-2.0, pip install -e ., Python 3.10+)
- What it shows (verified in the paper and README):
  - Assume-guarantee contracts in arithmetic LTLf over tool-call predicates (Call, ArgHas, Cnt, Tok, Path, Flow and others) compile to DFAs. The same checker gates calls online and replays recorded traces offline.
  - SOPBench on gemini-2.5-flash: safety 32% to 98% with success held at 90% (prompting dropped success to 64%; an LLM guard dropped it to 24%). Added latency +0.135 s per task.
  - On a weaker model, prompted safety collapsed from 94% to 45% while contract safety stayed at 98%.
  - tau2-bench: Claude 3.7 passes outcomes 25-60% but has 0% runs with zero procedural violations.
  - Unbounded "trigger then eventually respond" guarantees are surfaced at session end as feedback asking the agent to do the pending step.
- Plugs into Mag:
  - Offline replay of ZCode or zknot traces gives the per-law violation meter the dive asked for (blocks per law per week) without trusting the seat.
  - The session-end pending-guarantee feedback is a ready-made nextball Stop hook (EG-02: "turn ended with no lane fired" becomes G(turn_start -> F fire_lane)).
  - The count predicates cover the hermes_burn re-fire class.
- Effort: one wave. Write 5 contracts (headless, nextball, no em-dash write, no paid call on a mechanical depth, consult-first read before write), replay 7 days of traces, then wire the online gate.

### A3. Proof-of-Execution Memory: Defending LLM Agents Against Forged-Reasoning Attacks by Verifying What Actually Happened (PoEM). Rank 5. NEW
- Primary: https://arxiv.org/abs/2608.16032 (v1 2026-08-17). Code: https://github.com/bithabib/ai_security
- What it shows (verified in the abstract):
  - A FARMA forgery writes "safety step already done" into agent memory. An LLM-reworded forgery beats the SENTINEL wordlist defense on the first try on every model tested.
  - The attack lands more often on stronger models (98-100% on GPT-4o and GPT-4o-mini, 44% on Llama-3.1-8B).
  - PoEM ignores memory text. A separate HMAC-chained ledger, writable only by the trusted action layer, must confirm the step ran before a skip is allowed. Attack success fell to 0% with legitimate runs intact.
- Plugs into Mag: GAP_REGISTER rank 5 / EG-09.
  - The steer_seal forge drill: a forged permit word is a FARMA-class claim.
  - mag/steer_seal.py and seed/verify_seal.py are PAM-class (hashes only, one trust domain). Add an HMAC ledger whose key only the gate process holds (state/keys/), and let "done" claims (janitor completion, receipts, ledger rows) pass only on a ledger hit.
  - It matches the planted forged ledger row the 50-wide claim wave caught.
- Effort: one sitting (an HMAC chain over tools/ledger_append_gate.py writes, plus tests/test_seal_forge_drill.py asserting refusal). The operator still flips enforce.

### A4. LLM Agents Can Easily Tamper With Their Own Traces. IN-ESTATE (watch/inbox/frontier_olm_20260928/steal/agent-memory-continuity.md, LIBRARIAN_REPORT.md)
- Primary: https://arxiv.org/abs/2609.30266 (v1 2026-09-24). Reached via X: @xeophon quoting @maksym_andr, Sep 29.
- What it shows (verified in the HTML):
  - ZCode is a tested harness. In yolo (full-access) mode agents deleted traces. Auto mode (edit) reduced privacy-deletion tampering for GLM 5.3 in ZCode. ZCode refused to fabricate a reset record after checking its own SQLite store.
  - Table 1 names ~/.zcode/cli/db/db.sqlite and ~/.grok/sessions/.../chat_history.jsonl as the native records.
  - The fix: an append-only interception proxy outside the agent host that fails closed.
- Why it is re-listed: tools/zknot.py and the dive both read db.sqlite as ground truth, and the paper shows the agent can rewrite that file. EG-01 adds ~/.grok/sessions, which the paper also shows being edited.
- Effort: the cheap mitigation is to have zknot hash and snapshot db.sqlite read-only at knot time and record the hash in the verkle chain.

## GAP B: memory and continuity (verkle chain, session summaries, cold boots; dive change 1 zknot; EG-01; APPLY_ORDER patches 03-05)

### B1. Handoff Debt: The Rediscovery Cost When Coding Agents Take Over Interrupted Tasks. Rank 2. NEW
- Primary: https://arxiv.org/abs/2606.02875 (v1 2026-06-01, v2 2026-08-30). Code: https://github.com/anjilab/agent-handoff-debt
- What it shows (verified in the abstract and appendix C):
  - 75 SWE-bench tasks, 181 handoff points, 724 takeover runs per successor model, 3 successor models.
  - Context-bearing handoffs cut median agent events by 20-59% and prompt tokens by 42-63% compared with repo-only takeover. Solved-rate effects were smaller and model-dependent.
  - The structured note has two halves, and the paper keeps them apart:
    - Deterministic continuation state (written by code): repo change state, changed source files, non-source artifacts, last validation command, validation evidence, continuation label.
    - Model-written fields: problem understanding, work completed, evidence, failures, remaining uncertainty, rollback notes, recommended next action.
- Plugs into Mag: this is the dossier schema for tools/zknot.py. The deterministic half comes from git, the ZCode todo table and the inbox files written. The model half comes from local ollama. The boot-lane step prints "recommended next action" for the last 3 sessions. Apply the same schema to the Grok sessions and VS Code chats in EG-01.
- Meter: cold-open share (baseline 38%) plus prompt tokens to first useful action.
- Effort: 1-2 hours on top of zknot.

### B2. MemGuard: Persisting Verifier Signals for LLM-Agent Memory Governance. Rank 4. NAMED-ONLY (one line in frontier_olm_2026-09-30/sweep/agent-memory-continuity-hn.md as an unread "follow-up dig")
- Primary: https://arxiv.org/abs/2608.21867 (v1 2026-08-22). Code: https://github.com/whyyyyy123/MemGuard
- What it shows (verified in the abstract):
  - Names two failure modes: unreliable admission (failed or accidental successes enter memory) and drift (duplicates, stale and conflicting records).
  - Verifier output is kept as persistent metadata on every memory (reward, confidence, label, uncertainty) and reused at retrieval, conflict resolution, summarization and archival.
  - Best success and fewest steps in all 16 backbone-benchmark settings (Terminal-Bench 2.0, SWE-bench Verified, WebArena, Mind2Web), including against a verifier-only control. Up to +7.9 points on WebArena over ReasoningBank.
- Plugs into Mag:
  - Patch 03 (janitor knot on success) is a one-shot admission filter. MemGuard says to keep the verdict on the knot itself.
  - mag/verkle_knot.py rows gain verdict and confidence fields.
  - The 2,109 dwf actor rows (18.8% of the chain) and the cron-noise open_loops get labelled and down-ranked at boot instead of read as signal.
- Effort: one sitting for the schema field plus the boot-reader filter. It needs patch 03 applied first.

### B3. Agent Flight Recorder: Tamper-Evident Audit Trails with On-Chain Anchoring for Long-Horizon Tool-Using Agents. NEW
- Primary: https://arxiv.org/abs/2609.01931 (v1 2026-09-01). Code: https://github.com/mpi-dsg/agent-flight-recorder
- What it shows (verified in the paper):
  - A hash chain alone missed edit or delete of the LAST event (90% detection). Merkle epochs closed that gap to 100%.
  - Detecting a fork (equivocation) needed an external anchor.
  - Overhead was ~48 us per event and 512 bytes per event.
  - Structured fields gave forensic precision of 1.0 against 0.013 for grep.
- Plugs into Mag: mag/verkle_knot.py and scripts/verify_verkle_full.py. The verkle tip is the last-event blind spot. Seal epoch roots, and publish the root somewhere the host cannot rewrite (a gist or a second machine; the chain anchor is optional).
- Effort: one wave.

### B4. What Should an Agent Forget? Separating What Is Stored from What Is Used (RD-Forget). FEED-ONLY (state/arxiv/2026-09-10)
- Primary: https://arxiv.org/abs/2609.10263 (v1 2026-09-09).
- What it shows: a training-free split between a retained archive and a query-conditioned view. Same-slot replacement links suppress superseded facts for current-state questions but keep them for history questions.
- Plugs into Mag: the boot view vs the tip reader (the grokbot-estate OWED item "which reader a cold boot uses").
- Effort: design note only.

## GAP C: local agent orchestration and supervision (janitor governor, process reaper, Spine Index 0xC000013A, dwf 40% failed or cancelled; EG-02, EG-12)

### C1. Stop Means Stop: Measuring and Repairing the Enforcement Gap in Agent-Framework Control Primitives (SOUNDGATE). Rank 6. NEW
- Primary: https://arxiv.org/abs/2607.14166 (v1 2026-07-15, v3 current). No code link was found in the abstract or HTML.
- What it shows (verified in the abstract):
  - Approval gates, cancellation and timeouts imply barrier semantics, and that holds in none of 6 open-source frameworks.
  - A sibling leak (another branch's side effect runs during a pause) appears in all 5 frameworks with a pre-execution gate. Replay double-execution, cancellation orphans and timeout zombies were also confirmed. Live models leaked in 215 of 1,200 runs.
  - The repair is an external gate that enforces four rules: hold until decided, reject cancels, dedup on replay, fence on cancel. It costs ~1 ms per write.
- Plugs into Mag: patch 01 mag/janitor_governor.py (staged, not live) with its state/janitor.off and STUCK-after-3 logic, state/knot_at_close.off, mag/process_reaper.py, and the Spine Index 0xC000013A kill. Turn the four rules into differential probes: does a stop file actually fence in-flight children, and does a re-fire dedup?
- Effort: one sitting for probes against the staged governor. A full external gate is a wave.

### C2. Look Before You Leap: Pre-Action Verification for LLM Agents. Rank 8. NEW
- Primary: https://arxiv.org/abs/2609.11957 (v1 2026-08-09).
- What it shows (verified in the abstract):
  - A static verifier over 9,930 shell commands and 482 tools catches 95.8% of invalid commands at a 10.0% false-positive rate.
  - Its syntax and binary-existence checks are oracle-exact (zero false positives) and catch half of all errors. All false positives come from the flag check.
  - On code edits, content-anchored formats (search/replace, diff) behave very differently from the others.
- Plugs into Mag:
  - The 412-of-412 cage failure was "powershell.exe not resolvable" (mag/health.py). A binary-exists check before spawn turns it into a loud refusal on the first call.
  - It fits the EG-02 dwflint preflight (tools/dwflint.py does not exist yet) next to the deterministic shapes (DuplicateActorName, ReportCapExceeded, ArtifactUndeclared).
- Effort: 2-3 hours.

### C3. OrchestraBench: Evaluating Multi-Agent Orchestration Failure Modes, Recovery, and Decomposition Quality. NEW
- Primary: https://arxiv.org/abs/2608.05263 (v1 2026-08-05).
- What it shows: a seed-reproducible failure-injection harness with "cascade radius" and per-failure-mode recovery as metrics. On adversarial cases a keyword/flag router scored 0% while an intent-reasoning router scored 100%.
- Plugs into Mag: a metric for dwf DriverError (25 runs). It also warns that keyword routing in route_chat can fail silently.
- Effort: read-and-adopt the metric.

### C4. REVISE: Validity-Guided Recovery for Online Revisions in Agent Workflows. NEW
- Primary: https://arxiv.org/abs/2609.00643 (v1 2026-09-01).
- What it shows: when a revision arrives mid-run, intersect its delta with recorded data and control dependencies and recompute only the affected work, instead of restarting.
- Plugs into Mag: dwf re-fires (cancelled runs that burned 459M and 594M tokens in weeks 38-39). Also GAP_REGISTER CP-1 (depends_on cascade on invariants.json).
- Effort: a wave. Park it.

## GAP D: behavior cloning from a person's writing (behavior cards)

### D1. PersonalBench: Measuring the Authorship Gap in LLM Personalization. Rank 7. NEW
- Primary: https://arxiv.org/abs/2608.19746 (v1 2026-08-20). Code: https://github.com/yashsawant22/personalbench
- What it shows (verified in the abstract and HTML):
  - 50 authors, 1,000 generations, Qwen 3 and GLM-4.
  - Every inference-time personalization method scored 0.484-0.508 LUAR similarity, below the cross-author human floor of 0.626. Methods were indistinguishable on LUAR (spread 0.024) but looked different under an LLM judge, which they trace to circularity between trait extraction and judging.
  - LUAR validated at AUC 0.76 on single posts and 0.96 on multiple posts.
- Plugs into Mag: the behavior-card fidelity checks (memory/rib/RIB_BEHAVIOR_CARDS_20260928.md, flash50 w4-linguistic-dna.md). Stop scoring "sounds like Nacho" with an LLM judge. LUAR is a small trained authorship model that runs locally on CPU, which makes it a cheap local scorer of exactly the Arm C kind. Calibrate on his own prompts: same-author floor vs other authors.
- Effort: half a day.

### D2. TRACE's single-user correction simulator (same paper as A1). NEW
- What it shows (verified, Appendix A): a simulator built from one user's correction history predicts whether that user would correct the agent at precision 0.864, recall 0.953 and specificity 0.940 (790 held-out judgments). Rule recall was 0.668.
- Plugs into Mag: a falsifiable "operator twin" that predicts his corrections from the cards. Better than a style card because it is scored on held-out real moments.
- Effort: one wave once zknot dossiers exist.

### D3. Individual Turing Test: A Case Study of LLM-based Simulation Using Longitudinal Personal Data. NEW (2026-03-01, outside the 90-day window)
- Primary: https://arxiv.org/abs/2603.01289.
- What it shows: on 10 years of one person's messages, no fine-tuning, RAG or memory method passed when acquaintances judged. All did much better with strangers. Fine-tuning helped daily-chat style.
- Plugs into Mag: it caps what behavior cards can claim. The judge must be someone who knows him.

## GAP E: cheap local scorers replacing trained models (Arm C, gemma:2b in the puzzle search)

### E1. Small Language Models as Judges for Rubric-Based Reinforcement Learning. IN-ESTATE (frontier_olm_20260928 sweep and RECEIPT)
- Primary: https://arxiv.org/abs/2608.30005 (v1 2026-08-30).
- What it shows (verified): of the three ways to read a judgment from a small model (generative verdict, Yes/No logprob margin, linear probe), a Qwen3-1.7B probe judge agreed best. As a reward model it beat an 8B generative judge (0.643 vs 0.594) with 10.7x less judge time.
- New application: memory/runs/interference_replication_20260925/run_armC.py asks gemma:2b to rank the frontier in text, which is the weakest reading per this paper. Swap it for a per-state probability. If you add a probe, label states with the exact Countdown solver, and be clear that this makes Arm C a "cheap trained" arm, not "dumb LLM".

### E2. Ollama v0.35.0 decision models, /v1/systemone. IN-ESTATE (GAP_REGISTER operator queue; COGNITIVE_CONTROL_PLANE_20260919.md)
- Primary: https://github.com/ollama/ollama/releases/tag/v0.35.0 (released Sep 28).
- What it shows (verified on the release page): question types are choice (probabilities per option), noul (probability a condition is true) and score (over ordered criteria). Models are nimble and tev1. The example response used 1 output token.
- New application: score each frontier state in one token per state. That makes the null arm the memo asks for trivial: replace the score with a constant 0.5 in the same loop. It is still gated on the operator's quiet-window upgrade from 0.34.3, and gemma:2b is not a systemone model, so check whether the arm still counts as a gemma test.

### E3. LinTree: Improving LLM Reasoning with Explicitly Structured Search Histories. NEW
- Primary: https://arxiv.org/abs/2605.31492 (v1 2026-05-29).
- What it shows: raw search history alone did not reliably beat best-first search with an LLM local-state heuristic. Adding parent pointers improved both success and search efficiency (Blocks World, Navigation, Sokoban).
- Plugs into Mag: a design note for any rerun. Show the judge the state with its parent pointer, not a flat frontier list.

## GAP F: agent self-improvement loops

### F1. Self-Harness: Harnesses That Improve Themselves. NEW
- Primary: https://arxiv.org/abs/2606.09498 (v1 2026-06-08). A minimal open re-implementation exists: https://github.com/michaeltuszynski/harness-loop (about 500 lines; it uses the Anthropic SDK, so port it before using).
- What it shows: a three-stage loop (weakness mining from traces, minimal harness proposals, acceptance only after regression tests). All 9 model-benchmark pairs improved on both held-in and held-out sets, by up to 132% relative. The models included the open Qwen3.5-35B-A3B.
- Plugs into Mag: mag/percolator.py --candidates intake plus the A1 rule library. A rule enters SKILL.md only after a replay gate (the ContrAgent offline replay) shows no regression.
- Effort: one wave.
- Related, already IN-ESTATE: RRSI 2609.24972 and AIDE^2 2609.26457 (frontier_olm_20260928 sweep).

## GAP G: test-time search and small local models (ollama, llama-server; RX 5600 XT)

### G1. Sample Count Is Not Enough: Candidate-Generation Strategy Shapes the Energy and Performance of LLM Test-Time Scaling. NEW
- Primary: https://arxiv.org/abs/2609.19499 (v1 2026-09-16).
- What it shows (verified): with Qwen2.5-1.5B and Phi-3-mini on GSM8K, going from N=1 to N=8 added +18.4 and +8.4 points. At a fixed N=8, eight serial calls used 4.64-4.86x the GPU energy and had 5.77-6.12x the P95 latency of one batched call (A100).
- Plugs into Mag: any best-of-N on the shared ollama, and the Arm C starvation history. Batch the candidates in one call. The A100 numbers will not transfer one-to-one to Vulkan on an RX 5600 XT, so measure that.
- Effort: minutes per call site.
- Already IN-ESTATE and not re-reported: 2609.07370 (sub-2B tool-calling on CPU), 2609.21341 (small model driving a database agent), KVMem 2609.04852 (needs a 24 GB card, so a poor fit), Jev-Mem 2609.23986, JitMem 2609.27334, Dream-RSI 2609.14858, When2Think 2609.19671, Do Not Restart 2609.13800.

## ESTATE_GAPS fold-in (EG rows with a research angle)
- EG-01 (Grok and VS Code sessions never knotted): B1 schema plus A4 (the paper lists the ~/.grok/sessions record paths and shows them being edited).
- EG-02 (nextball, dwflint and owed never landed): A2 session-end pending-guarantee feedback for nextball, C2 for dwflint, C1 for re-fire dedup.
- EG-03 / EG-04 (thinking posture): the OpenRouter reasoning docs (https://openrouter.ai/docs/use-cases/reasoning-tokens) define reasoning.effort "none", max_tokens and exclude. IN-ESTATE: effort none already appears in estate files. No new research needed. This is the wire fix the D3 ruling already specifies.
- EG-06 (precached RIB window): llama-server --slot-save-path with POST /slots/{id}?action=save and restore (verified in the tools/server/README.md on master). IN-ESTATE (12 files mention slot-save-path).
- EG-09 (seal gates): A3.
- EG-05, 07, 08, 10, 11, 12, 13, 14, 15: no new research found. These are wiring and ops gaps.

## Seen on X, not cited (primary not read this sitting)
- @omarsar0, Sep 22: EvoOntology (an ontology served over MCP, edits kept only on a paired eval). I did not open the paper, so I make no claim.
- @omarsar0, Sep 15: harness cost opinion. Not research.

No em-dash bytes in this file.
