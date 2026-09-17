# RV2 — MESH EXPLAIN FLEET (receipt-first, appended as work proceeds)

- **Wave lane:** wave_20260916 / RV2
- **Date:** 2026-09-16
- **Mission:** Fire the mesh (5 segments × 10 seeds, free lanes probe-first) to draft, per-lane, pieces of an explanation of OUR system written for a stranger who has his own system (Hive Operating Floor lineage: split bench, receipt check, software never crowns truth). No AI cult, no cargo culting — mechanism, not ceremony.
- **Driver pattern:** `wave_20260916/d23_salon50_night_20260916.py`
- **Interpreter:** `.venv\Scripts\python.exe` only. **$0:** free lanes only, never zai paid walls.
- **Segments:**
  1. Append-only ledger (what/why corrections are new rows/the one thing it cannot do) — 100w
  2. Receipt-first work (why receipt before work; worth of a dead session's partial receipt) — 100w
  3. Pre-registered falsifiers (why commit threshold before data) — 100w
  4. Amendment obligation (why every cycle amends a rule or names why none) — 100w
  5. Outside reader (why a non-you must be able to replay the tape alone) — 100w
- **FOLD target:** per segment — convergence + 2 clearest verbatim + 1 confusion to avoid.
- **Receipt ends with:** the five clearest explanations, stranger-facing-README ready.

## Embedded context (verbatim, ≤250 tokens)

> A solo-operated fleet: agents + free model lanes + a local 2B janitor + one human. Its laws: append-only hash-chained ledger (nothing edited, corrections are new rows); receipts written before work so dead sessions leave partial ore; pre-registered falsifiers with thresholds committed before data; software never mints a verdict — a person opens the file; every cycle must propose one amendment to its own rules or name why none; an outside reader (another model or a stranger) must be able to replay and audit from the tape alone. Tonight it killed its own favorite theory by pre-registered threshold and corrected its own arithmetic in the same session.

## Work log (appended as it happens)

- [t0] Receipt written BEFORE work. Wave-lane law held.
- [t1] Driver pattern read: `d23_salon50_night_20260916.py` (repo fanout plumbing, SSRF allowlist, probe-first, append-as-they-land, retry pass, Jaccard fold).
- [t2] Driver written: `wave_20260916/rv2_mesh_explain_fleet_20260916.py`. 5 segments x 10 seeds = 50 jobs; seed base 2026091650; temp ladder 0.2/0.7/1.2; question digest registered below. ALL z.ai lanes excluded pre-probe (paid-wall law, incl. zai-lite — burst lane, never a default carrier). Raw tape: `wave_20260916/rv2_explain_fleet/raw.jsonl` (durable shared-inbox root). Schema `rv2_explain.v1`.
- [t3] Firing probe next; live lanes decide the seed->lane map.

## Probe (READY ping, $0)

- **LIVE (8):** groq-oss, groq-oss20, cerebras-oss, cerebras-qwen, mistral-min8, or-union-alpha, or-ling3, or-nemotron
- **DEAD (429):** groq-qwen ("request too large"), mistral-small (rate limit 1300), or-glm52 (temporarily rate-limited)
- **NEVER CALLED (paid-wall law):** zai-47, zai-air, zai-lite
- **Note:** or-nemotron live but leaks reasoning preamble into content and took ~213 s on probe — kept for width; fold lane will trim.
- Seed->lane map: `lane = live[s % 8]`, temp = TEMPS[(s + seg) % 3], seg = s//10.

## Run

- **Fired:** 50/50 jobs, 8 live lanes, temp ladder 0.2/0.7/1.2, seed base 2026091650.
- **Pass 1:** 49/50 answered. Failure: s=5 (S1, or-union-alpha, HTTP 429).
- **Pass 2 (retry):** s=5 refired same seed map -> ok. **Final: 50/50 answered, 0 lost.** Every segment answered by all 8 lanes.
- **Tape:** `wave_20260916/rv2_explain_fleet/raw.jsonl` (51 rows: 50 pass-1 + 1 pass-2; failures preserved as rows). Summary: `rv2_explain_fleet/summary.json`. Console: `rv2_explain_fleet/run_console.log`.
- **Diversity (pairwise Jaccard mean):** S1 0.246 · S2 0.205 · S3 0.148 · S4 0.194 · S5 0.161 — lanes agree on mechanism, diverge on wording. Good fold material.
- **$0 held:** groq/cerebras/mistral/openrouter free lanes only. Zero z.ai calls (not even probe). No paid API. No git.

## FOLD (per segment: convergence + 2 clearest verbatim + 1 confusion to avoid)

Human fold lane opened every row of the tape; selection below is judgment, not software output.

### S1 — Append-only ledger

- **Convergence (all 8 lanes):** each row hash-chains to the previous, so any edit visibly breaks the chain; corrections are therefore NEW rows that reference the old one, because the old row is evidence of what was believed at decision time; the one thing it cannot do is erase/undo history. Five lanes added the deeper second limit: the ledger cannot make recorded claims TRUE — it records, it does not judge.
- **Clearest #1 (or-union-alpha, s=5):** "An append-only ledger stores events as ordered rows: inputs, commitments, actions, outputs, and corrections. Each row includes the previous row's hash; changing an earlier row breaks subsequent links. Keep copies or publish checkpoints elsewhere, because someone controlling storage can otherwise rewrite the chain. Corrections reference earlier rows instead of replacing them, preserving what was known when a decision happened. Write intent before execution so crashes leave evidence of unfinished work. Another reader can replay the sequence and check its consistency. The ledger cannot make recorded claims true: hashes protect traceability, not factual correctness. A person still evaluates evidence and conclusions."
- **Clearest #2 (mistral-min8, s=4):** "An append-only ledger is a sequence of immutable records, each signed by the previous one. New rows replace corrections—no in-place edits—so history stays intact. This lets anyone replay the chain from the start, proving nothing was erased or backdated. It's not about 'truth' but *reproducibility*: if the rules and data are in the tape, an outside reader can audit every step. The one thing it can't do is *un-do*. If a mistake is written, it stays—only new rows can fix it. This forces discipline: every change must be explicit, traceable, and auditable. No 'undo' button."
- **Confusion to avoid (groq-oss20, s=9):** trailing garble "it cannot delete or alter existing entries—only add new ones in practice today" — makes the limit sound practical, not structural. The packet must state the limit as STRUCTURAL (the hash chain breaks), never as "hard in practice." (Also: don't muddle the two limits — cannot-edit is physical, cannot-mint-truth is epistemic; state both as separate laws, as s=3/s=5 did cleanly.)

### S2 — Receipt-first work

- **Convergence (all 8 lanes):** the receipt (task ID, input hashes, thresholds, expected outputs) is written BEFORE execution so intent is durable and comparable against results — it prevents retroactive result-shaping. A dead session's partial receipt is NOT proof of success: it is a boundary/tombstone proving what was attempted, what inputs were locked, and where the chain stopped — enabling resume or audit without reconstructing intent from memory.
- **Clearest #1 (or-ling3, s=14):** "Write the receipt first because it locks intent before execution drifts. The hash commits to inputs, constraints, and thresholds while the session is still coherent. If the session dies mid-work, the partial receipt is salvageable ore: it proves what was attempted, what inputs were locked, and where the chain broke. Another agent or the human can resume from that exact state or audit the gap without reconstructing intent from memory. It turns abandoned work into recoverable data rather than lost context. The mechanism is simple: pre-commit, then act. The receipt is the anchor; the partial receipt is the map back."
- **Clearest #2 (cerebras-qwen, s=19):** "Receipt-first is not permission; it's a checkpoint before nondeterministic spend. Writing task ID, input hash, method, budget, threshold, expected artifacts, and failure action before work turns a run into a testable contract. Context, seed, and lanes can change mid-flight, but the receipt freezes what work meant by done. If the session dies, the partial receipt still names the state: outputs saved, cache keys, intermediate hashes, unmet checks, and the next safe primitive to replay. It lets an outside reader distinguish abandoned evidence from clean completion and decide whether to resume, fork, or discard it without trusting a later log entry."
- **Confusion to avoid (cerebras-oss, s=18):** drifts into billing — "charge the operator only for the declared effort" — and garbles its ending ("in future audits only"). The receipt is an AUDIT BOUNDARY, not an invoice or a backup. Several lanes (e.g., groq-oss20 s=17, "protects against data loss") slid toward backup framing; the packet must not.

### S3 — Pre-registered falsifiers

- **Convergence (all 8 lanes):** after seeing data, the number you accept always slides toward sparing the theory, and you cannot feel it happening from inside; committing threshold + measurement method to the ledger BEFORE data turns the kill decision into arithmetic rather than judgment; the row ORDER (falsifier row before data row) lets an outsider verify the goalposts never moved.
- **Clearest #1 (or-union-alpha, s=21):** "A falsifier is a written claim: kill the theory if metric X crosses T. You commit T before running the data because afterward you'll move it. The number you'd accept post-hoc is always the number that spares the theory, and you can't feel that happening from inside. So write the threshold, its measurement method, and the kill date to the ledger first. When data arrives, comparison is arithmetic, not judgment — no negotiation. It cost me my favorite theory tonight; the mechanism did its job. Without pre-commitment, falsifiers are just intentions with better branding."
- **Clearest #2 (or-ling3, s=22):** "You commit the threshold before seeing data because the moment you look, your brain starts rationalizing. Pre-registered falsifiers fix the rejection criterion upfront: 'if X happens, I abandon this theory.' Once data arrives, you can't shift the bar. It turns a belief into a bet with a fixed losing condition. The ledger records the threshold as a row before the result row, so the audit tape shows you didn't move the goalposts. The mechanism is simple: lock the falsification condition, then let the data try to kill the theory. If it survives, you know you didn't cheat."
- **Confusion to avoid (groq-oss20, s=25):** redefines falsifiers as "error patterns a system declares it will tolerate up to a fixed count" — an anomaly budget, not a falsifier. A falsifier is a pre-committed KILL CONDITION on a claim, not a tolerance setting. (Lane artifact worth noting: or-nemotron s=23 burned its whole answer inside a leaked reasoning dump — width-only, never README material.)

### S4 — Amendment obligation

- **Convergence (all 8 lanes):** static rules drift silently; forcing every cycle to amend one rule OR name why none converts stasis into an auditable claim instead of a silent default — both branches land as ledger rows, so outsiders can later audit why nothing changed; this fights ossification WITHOUT forcing churn.
- **Clearest #1 (cerebras-qwen, s=35):** "The amendment rule forces the runtime to confront drift. A fleet that only executes fixed rules accumulates edge cases, stale defaults, and silent failures. Each cycle must either change a rule or produce a reason, turning no change into a testable claim. That claim enters the ledger, allowing later replay to ask whether it was sound when fresh data or new failure modes made it stale. This blocks ritual maintenance. If you cannot justify the current rule, change it. If you can, you have recorded an explicit check for invalidation. The fleet becomes a self-auditing instrument, not a static shrine."
- **Clearest #2 (or-union-alpha, s=37):** "At cycle close, require a ledger row proposing one rule amendment or explaining why none is warranted. The row links to receipts, names the failure or friction, and states what the proposed change should improve and how to falsify that expectation. A human accepts or rejects it; accepted changes govern future cycles, never reinterpret finished tests. This makes maintenance unavoidable without forcing churn. Otherwise failed runs accumulate as anecdotes while the same rules keep producing them. Explicit abstention preserves stable rules and exposes avoidance. Append everything so outsiders can distinguish learning from quietly moving thresholds after seeing the actual results."
- **Confusion to avoid (mistral-min8, s=36):** "if no rule changes, the system's capacity to adapt decays" — entropy framing that reads as CHANGE FOR ITS OWN SAKE. The law is amend OR name why none; "none, because…" is a first-class outcome, and forced churn is the failure mode the abstention branch exists to prevent.

### S5 — Outside reader

- **Convergence (all 8 lanes):** if only the operator can reconstruct what happened, the audit depends on the operator's memory and honesty — the tape exists precisely so it doesn't; replay by a non-you recomputes receipts, thresholds, and verdicts from the artifact alone and either reproduces the outcome or surfaces a defect as a public fact; hidden state is the thing replay exists to expose.
- **Clearest #1 (mistral-min8, s=44):** "The tape is the only proof. If *you* control the replay, you can lie—edit, omit, or retroactively justify. An outside reader forces you to build a system where every step is *visible* and *unalterable*. Their ability to audit means the ledger's integrity isn't trust in *you*, but in the rules you've locked into the chain. If the tape can't be replayed without you, it's just a logbook. If it can, the system's logic survives you. That's why falsifiers are pre-registered: to let strangers verify the rules were followed, not just that you *said* they were."
- **Clearest #2 (cerebras-qwen, s=43):** "A stranger replaying the tape checks that your fleet is computationally closed. If inputs, hashes, pre-registered falsifiers, thresholds, model outputs, ledger rows, and janitor traces can be reconstructed without you, defects become public facts instead of private opinions. The reader recomputes receipts, verifies which lane produced each claim, tests failed-theory thresholds, and searches for hidden state that makes a correction look like luck. That separation matters because it moves trust from your memory to the artifact. It puts each claim in a locatable file as evidence alone. If audit survives away from the operator, the rules are mechanical, not cultural."
- **Confusion to avoid (groq-oss, s=40):** "the pre-registered falsifier list proves that any deletion was authorized" — false and dangerous: append-only means there ARE no deletions; nothing "authorizes" one. Replay validates PROCESS, not truth — never claim the tape certifies correctness. (Best extra caveat, or-union-alpha s=45: "hashes detect changes but cannot reconstruct missing files" — the reader needs the artifacts, not just the hashes.) (Lane artifact: or-nemotron s=47 again leaked raw reasoning into content.)

## FIVE CLEAREST — README-ready

One per segment, verbatim from the tape (lane in parens), ordered as a stranger would build:

**1. The append-only ledger** (or-union-alpha, s=5)
An append-only ledger stores events as ordered rows: inputs, commitments, actions, outputs, and corrections. Each row includes the previous row's hash; changing an earlier row breaks subsequent links. Keep copies or publish checkpoints elsewhere, because someone controlling storage can otherwise rewrite the chain. Corrections reference earlier rows instead of replacing them, preserving what was known when a decision happened. Write intent before execution so crashes leave evidence of unfinished work. Another reader can replay the sequence and check its consistency. The ledger cannot make recorded claims true: hashes protect traceability, not factual correctness. A person still evaluates evidence and conclusions.

**2. Receipt-first work** (or-ling3, s=14)
Write the receipt first because it locks intent before execution drifts. The hash commits to inputs, constraints, and thresholds while the session is still coherent. If the session dies mid-work, the partial receipt is salvageable ore: it proves what was attempted, what inputs were locked, and where the chain broke. Another agent or the human can resume from that exact state or audit the gap without reconstructing intent from memory. It turns abandoned work into recoverable data rather than lost context. The mechanism is simple: pre-commit, then act. The receipt is the anchor; the partial receipt is the map back.

**3. Pre-registered falsifiers** (or-union-alpha, s=21)
A falsifier is a written claim: kill the theory if metric X crosses T. You commit T before running the data because afterward you'll move it. The number you'd accept post-hoc is always the number that spares the theory, and you can't feel that happening from inside. So write the threshold, its measurement method, and the kill date to the ledger first. When data arrives, comparison is arithmetic, not judgment — no negotiation. It cost me my favorite theory tonight; the mechanism did its job. Without pre-commitment, falsifiers are just intentions with better branding.

**4. The amendment obligation** (cerebras-qwen, s=35)
The amendment rule forces the runtime to confront drift. A fleet that only executes fixed rules accumulates edge cases, stale defaults, and silent failures. Each cycle must either change a rule or produce a reason, turning no change into a testable claim. That claim enters the ledger, allowing later replay to ask whether it was sound when fresh data or new failure modes made it stale. This blocks ritual maintenance. If you cannot justify the current rule, change it. If you can, you have recorded an explicit check for invalidation. The fleet becomes a self-auditing instrument, not a static shrine.

**5. The outside reader** (mistral-min8, s=44)
The tape is the only proof. If *you* control the replay, you can lie—edit, omit, or retroactively justify. An outside reader forces you to build a system where every step is *visible* and *unalterable*. Their ability to audit means the ledger's integrity isn't trust in *you*, but in the rules you've locked into the chain. If the tape can't be replayed without you, it's just a logbook. If it can, the system's logic survives you. That's why falsifiers are pre-registered: to let strangers verify the rules were followed, not just that you *said* they were.

## Amendment proposed (the fleet's own law, applied to this wave)

- **Proposal:** mesh drivers should tag lanes whose content is a leaked reasoning dump (observed: or-nemotron on s=23, s=47) at call time — e.g. a `leaked_reasoning: true` row flag — so fold lanes can filter width-only material mechanically instead of by eye. Cheap, falsifiable (compare fold-selection error rate before/after).
- **Otherwise none:** driver pattern (d23 -> rv2) needed no change; it worked unmodified.

## Close

- Mission complete: 5 segments x 10 seeds = 50/50 answered across 8 live free lanes, $0, no z.ai contact, no git. Receipt written first, appended throughout. Tape + summary filed under `wave_20260916/rv2_explain_fleet/`. Fold done by hand from the full tape.

## Results

(pending — appended per segment)

## FOLD

(pending)

## FIVE CLEAREST — README-ready

(pending)
