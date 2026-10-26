# PREMIUM AUTOPSY - where premium was REAL vs THEATER, measured by replay (AUTOPSY-1)

- Lane: AUTOPSY-1 (THE PREMIUM AUTOPSY). Operator mission 2026-10-01: "we paid
  ~$35 for claude asks - do the same questions across our entire dumb surface,
  see what was actually useful, map those places using our systems."
- Instrument: REPLAY + CONVERGE + BYTE-VERIFY. 17 premium questions from the
  2026-10-01 hermes_burn night, re-fired byte-identically at a 6-family dumb
  parliament through tools/model_garden.py (the canonical runner; inference_budget
  recipes per family) plus one loopback deviation runner for local gemma4.
- Staging: memory/plans/premium_autopsy/<fam>/<QID>/ask.json (102 ask dirs);
  frozen right-sized evidence at watch/inbox/model_garden/premium_autopsy/evidence/
  with MANIFEST.json (contract sha256 per question, per-file sizing ledger).
- Outputs: watch/inbox/model_garden/PA-<QID>-<fam>.md (102 files). Ledger:
  memory/runs/model_garden/usage.jsonl rows id PA-* (102 rows, all ok).
- Budget cap $3: metered + list-rate estimated real-money spend $0.69 (details
  in COST MATH). No em-dash bytes in any file this lane authored; evidence
  copies preserve original bytes verbatim (head75+tail25 with banner), which
  includes original em-dashes inside pasted material - replies dumped as
  received (byte truth).

## THE PARLIAMENT AND ITS RAILS (one attempt per family per question)

| family | model | transport + recipe | fires | token truth | cost |
|---|---|---|---|---|---|
| zai | glm-5.3-flash (api.z.ai coding endpoint, ZAI_API_KEY_Pro) | recipe glm-5.3-flash: uncapped, thinking enabled + reasoning_effort low | 17/17 | 263,988 in / 30,506 out (cached-prefix server, pin=17 on probe) | $0.0203 metered |
| deepseek | deepseek-chat (api.deepseek.com, thinking OFF by omission, AH10 law) | recipe deepseek: small_floor 2000 / review_floor 8000 | 17/17 | 184,970 in / 20,774 out | $0.1336 metered (peak rates) |
| nous-kimi | moonshotai/kimi-k2 (Nous credits, HERMES_API_KEY_2) | recipe kimi: no thinking control | 17/17 | 135,816 in / 64,822 out | $0 banked (prepaid credits; ceiling $0.23 at OpenRouter list 0.57/2.30 per M) |
| nous-qwen | qwen/qwen3.8-max-prime (Nous credits) | recipe nous-primes: reasoning max_tokens 6000 (LESSIG rail, auto-injected) | 17/17 | 149,841 in / 71,289 out (token-hungriest lane) | $0 banked (prepaid credits) |
| xai | grok-4.7 (api.x.ai SD account, XAI_SD_API_KEY) | body_extra reasoning_effort low, max_tokens 12000 | 17/17 | 162,585 in / 35,804 out | $0 metered (unpriced in cost_rates); $0.54 est at list 2.0/6.0 per M |
| local | gemma4:latest (ollama 127.0.0.1:11434, scripts/premium_autopsy_local.py; fence NOT weakened, garden_battery_local.py pattern) | max_tokens 2048, ctx 8192 | 17/17 | server tail-keep at pin=4099 on big asks | $0 |

Zero refusals, zero EMPTY_REASONING burns, zero transport deaths across all 102
fires. Every remote reply landed in the CONTENT channel. Contrast: 7 of the 17
premium verdicts (S1, S2, S4, A1, B2, C1, LENS1) landed as reasoning-channel
salvage ("content channel empty" headers in watch/inbox/hermes_burn/*.md) -
the premium carrier's cap/transport disease, not a capability verdict.

## IDENTICAL-BYTES LAW (what the comparison is worth)

Per question, all 6 families received byte-identical CONTRACT text (sha256 in
MANIFEST.json, byte-copied from the original ask.json) and byte-identical
evidence bodies. Right-sizing (the 5W context-pack sizing laws applied to
replay): per-ask budget 42,000 chars, per-file cap min(14000, max(3500,
42000//n_files)), method head75+tail25 with an explicit banner naming original
size. Avg rendered body 27,646 chars/question vs the premium original's avg
~120K chars (S2surface original evidence 3.6MB -> 35.9K). Two honest
consequences, named: (1) the mesh answered over LESS evidence than premium saw
(where the mesh still matched, the match is conservative); (2) claims whose
bytes fell in a cut window are graded WINDOW-CUT, not as capability misses.
The system face differs per animal by carrier design (claritas face +
deterministic estate-law block, single-sourced from tools/hermes_burn._system_for).

## THE GRADE (claim-level convergence, code_swarm method: a premium core claim
is MATCHED when >= 2 families independently land the same core finding;
byte-verification per the ractor discipline ran against live repo bytes)

| # | Q | class | premium core claims (quotable) | mesh verdict | byte-verified notes |
|---|---|---|---|---|---|
| 1 | S1boot | boot audit | docs leak paths/creds; CURRENT_OBJECTIVE.md carried unchecked into every reply; warm boot stamps frozen brief fresh; compile_report staleness self-trusted; rib files sorted in by name | PARTIAL | mesh (ds, glm) matched the class: boot = loaders not checkers, ranked brief-poison / deployments.json SSRF primitive / chain-tip-read-unverified / warm_state pre-plant. Premium-only: CURRENT_OBJECTIVE, compile_report trust, rib sort-order. Premium's brief-timestamp claim is STALE against live bytes (mag/hermes_warm_boot.py:185-190 fixed to st_mtime before the ask) |
| 2 | S2surface | protocol audit | events log has no writer auth (forge any event); no prev_hash, replay/reorder fold; seq inflation wins last-register-wins; overwrite+re-register launders as hash refresh; class is free text | SURPASSED | matched by ds+glm+kimi+qwen (ds: replay-with-bumped-seq under nonce-gap noise with the b2_378 four-gaps-one-seq evidence; class trust-laundering Joint 1). Mesh-only: purpose-string prompt injection with in-evidence examples, INDEX.md read-first-unvalidated, env-redirect tripwire warning-only |
| 3 | S4verkle | crypto/protocol audit | LAG branch never checks root (interior rewrite + append launders); leaf_hash never recomputed from row content (other fields uncovered); os.kill(owner,0) can TerminateProcess the lock holder on Windows; duplicate-last-leaf = CVE-2012-2459; chain_repair find_bad_tail_index walks from HEAD and heals tampered last row | MATCHED | LAG-laundering proven from compare() bytes by glm+qwen+ds (tip_witness.py:109-127: LAG branch returns before any root compare). leaf_hash-coverage blindness + repair()-launders-tamper + tip-file trust boundary (AG5 admission) by ds (strongest single reply of the run). find_bad_tail head-walk named by qwen/ds. MISSED by all: os.kill(owner, 0) Windows semantics (bytes present in the frozen head slice, verkle_knot.py:171 - a clean capability miss) and the CVE number |
| 4 | S5stores | concurrency audit | re-entry self-deadlock is the worst hole (nested exclusive() hangs: RLock re-entry + second OS lock on own handle); timeout is dead code on both platforms; no lock ordering; os.replace visibility-atomic but no dir fsync; THE test = nested-exclusive threading test | PARTIAL | dead-timeout crisply by glm+grok (msvcrt loop never returns; flock blocks in kernel); lock-ordering by qwen+ds; fsync/durability by glm+grok+kimi; NFS/WSL split-brain by qwen+ds. The ranked-WORST find (re-entry self-deadlock) was missed by ALL 5 remote families (kimi 0, grok explicitly assumed "no nested exclusive") - premium-unique |
| 5 | S6docker | config/infra audit | 8765 published 0.0.0.0 (contradicts loopback claims); ./mag:/app/mag rw overmount = host persistence; .env into cage + /proc/self/environ; patch + theater list | SURPASSED | all core matched by every family; patch identical (127.0.0.1:8765:8765 + :ro). Mesh-only: MAG_BIND_HOST 0.0.0.0 (compose line 17), ./tools/gps_mcp rw with sqlite ledger, ./watch mounted into two services (two-writer cross-service) |
| 6 | S7mates | ops audit | dead mate invisible (empty .claim, no timeout by design, unbounded notice); key leak via verbatim log copy; heartbeat design + falsifier | MATCHED | dead-mate invisibility + unbounded latency by glm+qwen (+ds); key-leak env->log path by qwen; heartbeat scripts delivered by 4 families (ds, glm, qwen, kimi) |
| 7 | S8stealth | triage design | answer files overwritten per cycle (age rot); dedup absent; note-field contradiction flip; undead failures (gates.com x5); DIE/CLIMB/STOP DISPATCH semantics; verdicts must be state changes | MATCHED | rot+dedup with fresh byte rows (2026-10-02 overwrite pair) by qwen; climb-or-die semantics by all 5 remote; rib-contradiction resolution by qwen; undead gates.com rows by gemma4 alone (kept-tail luck, honest note) |
| 8 | DG1 | ML design | naive whole-parent MoE door DEAD (ensemble behind a gate, 6GB memory wall); prior art EXISTS (sherpa wrong: mergekit-moe, Branch-Train-MiX); 4-part win condition; MATE_MOE_v0 export spec; 2B-3B parents, E<=4, llama.cpp yes / DeepGEMM no | MATCHED | kill + ensemble reasoning by all; win conditions (sub-parent experts, per-capability routing, shared backbone) by ds+kimi; prior-art correction by kimi (Sparse Upcycling, Komatsuzaki 2022) + qwen (closest-prior-art named) - premium's named-tool recall (mergekit-moe, BTX) remains richer; sizing/runtime reasoning by ds |
| 9 | A1 | security spec | HMAC envelope (version/key_id/nonce/timestamp/payload/mac); replay = nonce store + freshness + session-target binding; safe-fail restrictive-honored-on-verify-fail; restrictive words may pass unsealed (asymmetric trust); machine-originated steer origin-tagged | MATCHED | HMAC envelope by ds+glm+qwen+grok (kimi: nonce/replay without HMAC); nonce/replay machinery by all 5; safe-fail by glm+grok; asymmetric-trust unsealed-STOP by grok alone; session-target binding nuance not replicated |
| 10 | B2 | code forensics | empty session_id hashes "" but stores "unknown"; command[:2000] then redact-expands -> stored[:2000] vs full-redacted basis mismatch; flagger/verify agree with each other, disagree with writer; docstring basis ("result") != code basis (result.output_excerpt) | PARTIAL | docstring-vs-code basis drift by qwen (quoted make_row bytes); pre/post-cutover coherence logic by glm (F1: redaction lands BEFORE hashing -> post-cutover rows coherent by construction); 929-pre-cutover clustering by qwen. The subtlest find (redaction-EXPANSION breaks stored-vs-basis) missed by all - premium-unique |
| 11 | C1 | research synthesis | census instrument cannot measure refusal (gemma:2b 0/60 safety refusals); Ollama has no activation-editing API (prompt-level reality); no GGUF export -> convert+quantize path, survival-across-Q4 open; steal-but-probe-first; dual-use + telemetry honesty | MATCHED | 0/60 instrument-blindness by 5 families; GGUF/quantize path + quantization-survival question by 6; activation/residual-stream limits by 6; baseline disagreement-with-evidence (refusal-direction cheaply removable contested) by glm; probe ordering by qwen+ds |
| 12 | D1 | doctrine roast | accuracy.md's landing gate is an existence check its own Incident 1 would pass; "no code touched" + "changes a contract" = proposal-as-landed (13th incident of its own class); 45-vs-40 rows no timestamps; truncated 16-hex labeled sha256 | PARTIAL | the adjudication CLASS held: ds verified/refuted/out-did the cheap seat by name with byte-fidelity (refuted-as-stated, verified-as-weaker-near-miss); qwen found the temporal split (landing-time gates cannot catch post-landing decay classes). Premium's specific line-pin set not replicated |
| 13 | D2 | adjudication | grep "sys.exit(1)" is blind (single sys.exit(main()) propagation); two return-1 sites (216 main read error, 298 run_scenarios empty dir); 7 total return sites | SURPASSED | grep-blindness + exit-site truth by glm+qwen (byte-verified this session: return 1 at 216/298, 7 return-[012] lines, one sys.exit at 334). MESH-ONLY, byte-verified: the docstring claim "every submission registers a row" is FALSIFIED - the OSError return-1 (line 297-298) fires BEFORE the registry append, and qwen adds the --no-register and --scenarios paths as no-row paths (3 total) |
| 14 | D3 | adjudication | L1 closes gate-side with residues (5-vs-7 sites; exit-1-soft label is report-not-bytes; callers unread; three-run falsifier unrun); existence-resolver catches placeholder ids but NOT wrong attribution; deleting UNVERIFIED clauses = report-into-doctrine | MATCHED | residue classes reproduced by glm+qwen (R1 counts, R2 callers-unread - "push" appears nowhere in the file, R3 mappings-wrong); qwen's 3-no-register-paths residue; report-vs-doctrine law restated |
| 15 | R1 | meta roast | leg ranking (LEDGER/OUROBOROS load-bearing, REVERSE-GPS proven-by-contrast, SHERPA/CHECKPOINT/CLARITAS/OPERATOR-PROXY ceremony, LANCE dead); the audit itself is stale on 2 claims (A1 returned content twice; DG1 fired); falsifier must watch marginal-artifact-per-dollar; SPEND GATE replacement | MATCHED | ranking convergent (glm + qwen landed the same load-bearing/ceremony/dead trichotomy from the same bytes); falsifier gap = post-deliverable cost per ask id by glm+qwen; stale-audit-claims engaged by glm+grok. Kill choice DIVERGES: premium kills LANCE, mesh kills OPERATOR-PROXY (4) - same evidence, defensible either way, honest divergence recorded |
| 16 | R2 | process roast | evidence[]-carries-ractor law not obeyed on the one refire (citation theater); DUEL2 "LANDED 14/14" = 14 blocked-on-missing-material refusals (ok:true = call-returned); 20-lane graveyard (one measured 8/14, 23 steals no tracker); TICKETS.jsonl redemption gate | MATCHED | citation-theater test by ds (positive: the S5 evidence-less->refire chain IS one redemption; negative: A1_ASSEMBLED predates final premium write, no send-back); metric-capture DUEL2 14/14 by grok+qwen+kimi; redemption-gate specs by all 5 |
| 17 | LENS1 | judgment/falsifier | none of the 3 process conditions measure correctness (ok:true = returned; refusals counted LANDED); sharper finish-line = pre-registered task + redemption + consumed credits; LANDED predicate definition; T1 audits are code review, not the stranger test | MATCHED | process-vs-correctness by ds+qwen+glm+kimi; the external-consumer finish line (a fresh seat must succeed on public outputs; credits redeemable by an external party) landed by 4 families, sourced from the sherpa jsonl's own falsifier-gap rows - the mesh found the premium's sharpest idea already present in the cheap evidence |

Counts: MATCHED 10 / PARTIAL 4 / MISSED 0 / SURPASSED 3 (question level).

## THE TWO LISTS

### ROUTE-CHEAP-FOREVER (mesh matched or surpassed; premium added nothing
material the mesh lacked)

1. CONFIG/INFRA AUDIT (compose, Dockerfile, mounts): S6 SURPASSED at ~$0.04
   per 6-family parliament vs $0.152 premium.
2. OPS-LIVENESS + TRIAGE DESIGN (S7, S8): MATCHED, heartbeats and climb-or-die
   rules delivered by 4-5 families.
3. PROTOCOL/LOG AUDIT where the answer is in the provided bytes (S2): SURPASSED
   (mesh found injection channels premium did not name).
4. DOCTRINE ROAST / PROCESS ADJUDICATION (D2, D3, R1, R2): matched or
   surpassed; glm's D2 docstring-falsification is a byte-verified mesh-only
   defect. This is the single biggest class of tonight's premium spend after
   A1.
5. FALSIFIER/JUDGMENT ON OUR OWN ARTIFACTS (LENS1): MATCHED; the sharpest
   prescription (external-consumer finish line) was recoverable from the cheap
   sherpa evidence by 4 families.
6. ML DESIGN KILL/WIN-CONDITION REASONING (DG1): MATCHED; only the named-tool
   prior-art recall (mergekit-moe, BTX) stayed premium-side, and kimi's Sparse
   Upcycling citation covered the correction class.
7. RESEARCH SYNTHESIS FROM PROVIDED EVIDENCE (C1): MATCHED by 5-6 families.

### JUSTIFIED-PREMIUM (only the frontier saw it; what exactly it saw)

1. RUNTIME-SEMANTICS SIMULATION of concurrent code (S5-class): premium mentally
   executed `with exclusive(p): with exclusive(p):` across POSIX flock and
   Windows msvcrt semantics and found the re-entry self-deadlock; 0/5 remote
   families found it (grok explicitly assumed no nesting). Same shape: S4's
   os.kill(owner, 0) TerminateProcess-on-Windows find (CPython + WinError 87),
   bytes in-window, missed by all.
2. LONG-TAIL INDEXICAL RECALL (CVE-2012-2459 by number against a duplicate-leaf
   Merkle; mergekit-moe / Branch-Train-MiX by name): the mesh corrected the
   same wrong claim with adjacent recall (Sparse Upcycling) but did not produce
   the two named priors.
3. MULTI-STEP CODE-STATE MUTATION TRACKING (B2-class): the redaction-EXPANSION
   vs truncation-order stored-vs-basis mismatch requires simulating string
   growth through three pipeline stages; all mesh families stopped at the
   docstring-vs-code basis drift one level up.

Pattern, one line: the mesh reads; the frontier SIMULATES. Every premium-unique
find of tonight is a claim about what code DOES when run (locks, kills, string
growth), not about what bytes SAY.

## COST MATH (what tonight's $35 would have cost as a dumb-mesh run)

- Premium ledger total (the night): $37.76 (memory/runs/hermes_burn/usage.jsonl,
  236 rows). The 17 replayed questions cost $30.40 premium (A1 alone $21.852 -
  the 49-fire driver disaster, not an ask-quality signal; ex-A1 the 16 asks
  cost $8.55).
- The same 17 questions as a 6-family dumb parliament: $0.69 real-money
  (deepseek $0.1336 + glm-flash $0.0203 metered + grok-4.7 $0.54 list-rate
  estimate) + Nous prepaid token truth (kimi 200.6K tok, ceiling $0.23;
  qwen-prime 221.1K tok, Nous credits) + gemma4 $0 local. All-in ceiling
  under $1.5.
- Ratio: the parliament covered 14/17 questions at MATCHED-or-better for ~2-4%
  of the premium dollars. The 3 premium-unique claim families cost $30.40 to
  learn tonight; routing them straight to premium (and everything else to the
  mesh) would have bought the same knowledge for roughly the A1 fire cost
  alone.
- Per-family per-question price of THIS run: glm $0.0012, deepseek $0.0078,
  grok $0.032 (est), kimi $0.013 (ceiling), qwen prepaid, gemma4 $0.

## RIB_MODEL_GARDEN_ROUTING FILL ROWS (self-steal leg; the map lands in the
routing systems we built; all cells moment 2026-10-01, instrument this receipt)

| family | capability-column | verdict | price-per-quality | condition | measured-by | moment |
|---|---|---|---|---|---|---|
| glm-5.3-flash (zai coding endpoint) | adversarial-review (18-40K-char estate replays) | WIN 17/17 content-channel, 10 questions mesh-convergent | $0.0012/ask metered | uncapped + thinking enabled + reasoning_effort low (recipe path; no hang at effort low, contradicting the cheapgrid1 effort-max hang on this endpoint) | this receipt + memory/runs/model_garden/usage.jsonl PA-*-glm53 | 2026-10-01 |
| deepseek-chat (v4.1-flash mapping) | adversarial-review + analysis at review shape | WIN: deepest single replies of the mesh (S4 repair-laundering chain, S2 injection channels, DG1 slices) | $0.0078/ask peak | thinking OFF by omission (AH10); review_floor 8000 held; long-form degradation did NOT bite at 27K-char avg bodies | same ledger PA-*-ds41 | 2026-10-01 |
| moonshotai/kimi-k2 (Nous) | adversarial-review + research synthesis | PARITY-to-WIN: solid on C1/A1/B2/R2, prior-art recall (Sparse Upcycling) | $0.013/ask ceiling (prepaid) | no thinking control; 64.8K completion tokens over 17 asks (verbose tier) | same ledger PA-*-kimik2 | 2026-10-01 |
| qwen/qwen3.8-max-prime (Nous) | adversarial-review + adjudication | WIN: systematic byte-pinned tables (S4 LAG proof, B2 basis drift, D3 3-path residue) | prepaid (token-hungriest: 71.3K completion) | LESSIG rail reasoning 6000 auto-injected; NO gopher disease at this shape (17/17 content) | same ledger PA-*-qwen38max | 2026-10-01 |
| grok-4.7 (api.x.ai SD) | adversarial-review at effort-low | WIN 17/17: unique asymmetric-trust find (A1), crisp timeout-dead-code (S5), stale-audit-claims (R1) | $0.032/ask est (2.0/6.0 per M) | reasoning_effort low + max_tokens 12000 + WHOLE-RESPONSE transport: the PRIORS streaming-only law did NOT bite at this effort/shape (17/17, ~1-2.5 min/ask) | same ledger PA-*-grok47 | 2026-10-01 |
| gemma4:latest (local ollama) | adversarial-review at 27K-char bodies | DNF-BY-WINDOW: ctx 8192 tail-keep cuts the CONTRACT (replies ask for it); usable only at small bodies (DG1 at 11.5K chars landed real content) and keeps-tail luck (S8 undead rows) | $0 | route via context_pack sizing (janitor 4800 chars), never raw replays | this receipt + scripts/premium_autopsy_local.py rows | 2026-10-01 |
| (class row) question-class routing | RUNTIME-SIMULATION column (locks/OS/CPython semantics) | premium-only: 0/5 mesh on S5 re-entry deadlock, 0/5 on os.kill(0) Windows | $0.42-1.72/ask premium vs mesh $0.17 total for nothing | route asks demanding execution-simulation to the funded frontier (opus/grok-4.7 high-effort), everything evidence-readable to the mesh | this receipt grade table | 2026-10-01 |

## ANIMAL OBSERVATIONS (filed to tools/animal_profiles.py observe, kind=verdict,
source=this receipt; the --distill leg picks them up)

Filed one row per family (glm53, ds41, kimik2, qwen38max, grok47, gemma4-local)
with the headline behavior: content-channel reliability at replay shape, price,
and the one find each contributed. See memory/behavioral/animals/garden_v1.jsonl
appends with source watch/inbox/model_garden/PREMIUM_AUTOPSY.md.

## FALSIFIER (this map's own)

- If a future 17-question replay at the same shape shows the mesh MISSING a
  claim class this map routes CHEAP (config audit, doctrine roast, falsifier
  design), the ROUTE-CHEAP-FOREVER list is wrong: amend it.
- If a premium ask in the RUNTIME-SIMULATION class comes back WITHOUT a
  mesh-missed simulation find (run the mesh control first), the
  JUSTIFIED-PREMIUM list is too wide: route that subclass down.
- If grok-4.7 whole-response DNFs at effort-low again (PRIORS row 12), tonight's
  17/17 was shape luck: restore the streaming-only rail in the rib row above.
- A1's $21.85 is a DRIVER bug (49 refires), not a model verdict; any cost
  comparison that counts A1 as ask-quality is void (R1's marginal-artifact
  falsifier, adopted here).

## HONEST LIMITS

- The mesh saw right-sized evidence (avg 27.6K chars vs premium's ~120K+): mesh
  misses on claims whose bytes were cut are WINDOW-CUT, and the two clean
  premium-unique misses named above (os.kill bytes in-window; re-entry logic
  fully in-window at 5,979 chars) are the real capability signal.
- One grading seat (this lane) did the claim convergence; no second blind
  grader. The code_swarm convergence bar (>= 2 families) is the mechanical
  guard, and every load-bearing MATCH/SURPASS row above names its families.
- gemma4's S8 "find" is tail-keep luck, banked as a condition note, not a
  capability claim.
- Premium verdict quality was itself degraded: 7/17 landed as reasoning-channel
  salvage. The autopsy grades FINDINGS, not polish; but any "premium writes
  better deliverables" claim is false tonight at these shapes.
