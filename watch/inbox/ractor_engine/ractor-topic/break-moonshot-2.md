# BREAK-MOONSHOT-2 (hostile second pass) on lens moonshot-2, 2026-10-02

Schema: ractor.secondpass.v1 · lane: break-moonshot-2 of ractor-engine fire (bank ractor-topic) ·
every check below was executed this sitting; command outputs quoted verbatim. No em-dash bytes.

## Verdicts

### Finding 1: the engine rode the literal topic "undefined" - CONFIRMED

Every cite byte-checked against .zcode/workflows/ractor-engine.dwf.ts:
- slug `required: true` at :38, topic `required: true` at :43 (the lens's "38-43" range is exact).
- The slug fallback `args.slug || "ractor-" + String(args.topic || "topic")...` is at :90, and it
  fired: the bank folder on disk is `watch/inbox/ractor_engine/ractor-topic/` (directory listing).
- The ask interpolation `String(args.topic)` is at :147.
- `grep -n "throw" .zcode/workflows/ractor-engine.dwf.ts` returns exactly one hit:
  `202:          throw e;` (the catch-path rethrow). No arg validation throw exists anywhere.
- RACTORSWARM_MAP_20261001.md:30 carries the security jacket row ending
  "gates that test only themselves" verbatim.

Runtime proof the lens could not cite and I can: my own break-agent persona (engine :232
interpolates `String(args.topic)` into `break-` agents too) carries the literal text
"The topic: undefined". The null topic reached every agent class, not just lens riders.

Condition the lens dropped: its falsifier ("if the facade strips args, validation is dead code")
does not actually threaten the fix. A script-side guard on the observed value fires whether or
not the facade transforms args, and the fallback at :90 firing proves the script sees args
(undefined values included). The falsifier only changes attribution, not the move.

### Finding 2: the wiring ratchet - WEAKENED (substance stands, numbers do not reproduce)

I reran the lens's exact command:
`grep -rlE 'chat/completions|/v1/|api.openai|api.deepseek|api.anthropic|openrouter' mag/ tools/ --include='*.py' | wc -l`
gives **188**, not the lens's 187. The census's own count at its moment is 182
(WIRING_DEBT_CENSUS_20261001.md:155). Three sittings, three numbers: the count is a moving
target on a hot tree and the "187" is not a stable fact.

"imported by 6 of the 187" overstates: only 3 files actually import the organ
(tools/code_swarm.py:44, tools/hermes_burn.py:59, tools/model_garden.py:56, all
`from mag.inference_budget import ...`); the other 3 of the 6 grep hits are comment/docstring
mentions (tools/overmind_brain.py:5, mag/inference_budget.py itself, tools/overmind_loop.py).
Mention is not import. The census quote "one-shot probes make up much of the remainder" is at
:158, not the lens's cited :161.

What survives byte-checked: the census cure cite is verbatim at WIRING_DEBT_CENSUS_20261001.md
:166-167 ("wire the ~10 STANDING carriers ... file the two dead-probe exempt classes by name"),
and the ratchet plumbing exists (githooks/pre-push:10 runs `tools/violation_ratchet.py check
--changed`, :25 runs `tools/citation_lint.py check --changed`). The disease and the
ratchet-shaped cure stand; the specific counts in the evidence do not.

### Finding 3: claims as bytes, prose as render - CONFIRMED (strongest finding of the batch)

Byte-checked: tools/census_drift_patrol.py:83 is `CARRIER_LINE_RE = re.compile(r"^[ \t]*[-*][
\t]*\*\*Tests:\*\*", re.MULTILINE)` pinning the AGENTS.md bullet grammar (:82 is the pinning
comment); :98 carries "live in three hand-copied places while the live AGENTS.md bullet
refreshes" verbatim (B2-274 ownership law, :97-110). The B2-249 carrier shape law ("rewording
the claim breaks the gate instead of silently rephrasing it") is present at AGENTS.md:27 inside
the Tests bullet. WIRING_DEBT_CENSUS_20261001.md:62-64 carries the REFUTED sub-claim and the
index_fold cite verbatim; the quoted "KILLS the lost-update race structurally" line is at
scripts/index_fold_host.mjs:5 with the mechanism at :6-8 (one line off on the quote, same
block, tolerable).

Live corroboration from this sitting: my own endpoint-count drift (182 census / 187 lens /
188 mine, three moments) is finding 3's thesis demonstrated inside finding 2's evidence while
I was breaking it. Counts stored as prose rot between sittings; only instrument re-runs are
truth.

Condition the lens dropped: the patrol's OWNERSHIP LAW (tools/census_drift_patrol.py:101-110)
froze the regression vectors and forbids auto-syncing them to the live bullet. A
render-from-ledger move that rewrites the bullet must keep the frozen vectors hand-owned, or
the ledger fights the estate's own fixture-freeze law.

### Finding 4: the U+F03A junk path at repo root - CONFIRMED, upgraded

Byte-checked: `git ls-tree -r HEAD --name-only | grep lane_a12` reproduces
`"C\357\200\272UsersfosteAppDataLocalTemplane_a12_commits.txt"`; `ls -la` reads 46,808 bytes,
Oct 1 18:33; watch/inbox/NIGHT_CLOSE_20261002.md:18-19 carries "the mangled lane_a12 temp
artifact stayed staged as the coordinator left it" verbatim.

Upgrades from this sitting:
- The lens's blind spot 4 (codepoint ambiguity) is CLOSED: `os.listdir` via the repo venv
  prints `'C\uf03aUsersfosteAppDataLocalTemplane_a12_commits.txt'` - the on-disk name carries
  U+F03A (0xEF 0x80 0xBA), not a plain colon.
- The falsifier was TESTED, not left hypothetical: `grep -rn "lane_a12_commits"` across watch/,
  memory/, corpus/, docs/ finds only the lens's own moonshot-2.md:54. No pre-existing receipt
  cites the in-tree path, so relocate + `git rm --cached` breaks no cite today.
- "No gate checks filename provenance" is verified by reading githooks/pre-push in full: 12
  blocks (ratchet, citation lint, config seal, description_pin, freshness, census patrol,
  checkbox, caption ledger, refold, workflow scenarios, rule parity, secret gate), every one
  content-only. The junk-path class is genuinely uncovered.

### Finding 5: the return meter - WEAKENED (spend half solid, join half fails on measurement)

Byte-solid: watch/inbox/NIGHT_CLOSE_20261002.md:52-56 carries $5.5208 (43 rows hermes_burn),
$3.4746 (725 rows model_garden), $8.9954 total, and AGENTS.md:35 carries the descent falsifier
("ledger grew but no rib/pack/receipt carries a frontier contribution forward = spend theater")
verbatim. cost_usd is present in every row of both ledgers (measured below).

The join half fails the measurement the lens admitted it never ran:
- memory/runs/hermes_burn/usage.jsonl: 236 rows, all 236 with cost_usd, **0 with corr_id**.
  Full key set: channel, completion_tokens, cost_usd, id, model, ok, prompt_tokens,
  reasoning_tokens, refused, ts, turn.
- memory/runs/model_garden/usage.jsonl: 725 rows, all 725 with cost_usd, **0 with corr_id**
  (keys include finish, model_family, refire, series, via, wall_s; no corr_id).
The proposed fold joins "corr_id to landed receipts" but the join key exists in neither
ledger. The move needs carrier schema work first, and "45 min" is no longer the honest cost.

And the CROSS-RACTOR cite names the wrong commit: `git log --grep="63 pct of day spend"
--format="%h %s"` resolves to **43f50ed71** (WAVE24 DAY 1), not HEAD 0c9d72a06. 0c9d72a06's
message body is 2,303 bytes and its only "pct" hit is "7.1pct agreement" (OVERMIND HOUR).
The figure is real, but the lens cited HEAD without checking it; salon_mine/m01.md:80 had the
attribution right.

## Additions (what the lens missed)

1. BLAST RADIUS UNDERSTATED: the undefined topic also rode the break agents (ractor-engine
   .dwf.ts:232) and the synthesis voice (:299). This run's SYNTHESIS.md triangulates survivors
   on a null topic; my own persona text is the runtime proof. The fix must guard before phase 1,
   which the lens's "top of file" move already does.
2. args.lenses IS THE SAME PROSE CONTRACT: :138-140 silently filters unknown lens ids with no
   error - a typo'd lens id ("securty") shrinks the swarm invisibly, and an empty array is
   conflated with the default at :138. Finding 1's guard should cover all three args.
3. THE GATE CERTIFICATION GAP: engine :12 claims "workflow_gate PASS digest 5253afd2d68d
   G1-G7", but the gate's required-field check (tools/workflow_gate.py:167-173) validates
   scenario-card fields, and no gate scenario covers runtime arg validation. A certified gate
   passed a null-topic fire: the certification tests script shape, not arg discipline. Falsifier:
   a gate scenario that fires the engine with topic absent and expects a fail-closed refusal
   would close it.
4. RETURN-METER JOIN KEY MEASURED ABSENT (0/236 and 0/725): the honest sequencing is schema
   first (add corr_id to tools/hermes_burn.py and tools/model_garden.py fire paths, backfill
   nothing), fold second. Revised cost: ~75 min, not 45.
5. CROSS-LENS TIE: the 182/187/188 endpoint-count drift across three sittings is finding 3's
   thesis demonstrated inside finding 2's evidence. The wiring ratchet's baseline should be
   generated by the same instrument run that gates, never hand-copied, or it inherits the rot.

## Not run this sitting

No pytest suite, no gate end-to-end, no CreateWorkflow: same as the lens declared. My checks
are grep, git, file reads, and two venv python one-liners (filename codepoints, usage.jsonl
key coverage). The facade-side arg handling named in finding 1's falsifier is outside this
repo and remains unverified by both passes.

Filed by break-moonshot-2, ractor-engine fire of 2026-10-02. No em-dash bytes.

---

# BREAK-MOONSHOT-2 second pass, 2026-10-06 fire (appended below the 2026-10-02 pass, same convention as moonshot-2.md)

Hostile second pass on the 2026-10-06 moonshot-2 report, the fire that again rode topic
"undefined". Transmission note: the report JSON handed to this breaker truncates mid-finding-4
("(ok=true ledger"); findings 5 and 6 were verdictable only because the lens's own bank file
carries them (moonshot-2.md:161-181). Live receipt I can cite and the lens could not: this
breaker's own system prompt this fire opens "The topic: undefined Laws:" - the run I sit
inside rode the null again. Every check below was executed this sitting; commands and outputs
quoted. No pytest, no census, no ratchet, no seat boot was run; nothing here substitutes for
the suite and no test counts are claimed. No em-dash bytes.

## Verdicts

### Finding 1 (undefined topic again) - CONFIRMED, sharpened
- Bytes re-verified: topic required:true at .zcode/workflows/ractor-engine.dwf.ts:32;
  interpolation "The topic under raction: " + String(args.topic) at :149 (also :159, :237,
  :312); my grep -n undefined = exactly 3 lines (:87, :168, :215), matching the claimed
  count of 3; grep -c throw = 1 (:207, the salvage-catch rethrow, not a guard). Full
  362-line read: no topic validation anywhere.
- Prior spec confirmed: watch/inbox/ractor_engine/ractor-topic/moonshot-2.md:24-28.
- SHARPENING: "the engine bytes unchanged" is false as words, true as substance. The file
  is gitignored (.gitignore:200; git check-ignore hit) and untracked (git ls-files
  .zcode/workflows/ = the-gala.dwf.ts only), so no git baseline exists; but in-file stamps
  prove the file WAS amended between fires: :39 carries "ractor R1 fleet amendment
  2026-10-05" and :302-309 is the cross-run fold-gate block (commit 55cdaaa4f wired the
  ractor-engine synthesis voice prompt law). The amendment economy reached this file twice;
  the guard still did not ship. The finding is stronger for this, not weaker.
- Undischarged: missing-arg vs literal string "undefined" render identically through
  String(); the run record is unreachable from this seat (ListWorkflowRuns returned
  workflow_introspection_unavailable, capability gap, verbatim). The 10-02 falsifier (log
  args at line 1 on the next fire, read what arrives) is still the discharge and still
  nobody has run it. Cure note: the banked spec (non-empty, not "undefined"/"null", min
  length) covers both shapes, so the guard is safe either way.

### Finding 2 (selfplay fallback-blind) - CONFIRMED, strengthened; falsifier discharged by me
- All cites byte-checked: mag/selfplay_orchestrator.py:165-168 (except to _fallback_score),
  :170 (unconditional BottleneckSample ok=True), :249-251 (return "0.5"; lens range 249-252
  covers), :154 (move-only unpack), :179 (elo.update(reward if correct else 0.0));
  mag/llama_cpp_bridge.py:160-166 and :190-196 (fallback dicts ok:False/fallback:True); the
  uncommitted-diff confession found by my own grep of git diff HEAD -- mag/llama_cpp_bridge.py
  ("so the bridge silently rode its fallback path for three full probe runs");
  memory/runs/selfplay/evidence_latest.json: my grep -c fallback = 0 and avg_actor_ms 3472.6.
- CITE NIT: the 0.5-as-fix banking is at watch/inbox/selfimp/imp002.md:22 ("added static
  method returning \"0.5\" neutral score"), not :31 as cited (:31 is the "## Bottleneck
  measurement" header). Content real, anchor off.
- FALSFIER DISCHARGED (I ran it): patched mag.lane_runner.flash_call to raise, ran one
  play_one on m001. Verbatim output: "SAMPLE actor 0.0 True ''" and "SAMPLE scorer 0.0 True
  ''" - ok=True on a leg that never ran; no session shape prints scorer ok=False. The
  prediction held exactly.
- ADDITION (stronger than the finding): the ACTOR sample also reads ok=True on a fully
  synthetic session (actor_move was the literal placeholder {"fallback_move":
  "7ef43975", "confidence": 0.0}) because the bridge fallback RETURNS a dict instead of
  raising, so _measure (mag/selfplay_orchestrator.py:116-125) stamps ok=True. Both legs
  read green on a dead session. The CONTAMINATED banner must gate on the actor fallback
  flag too, not just scorer status.
- BLAST RADIUS: the synthetic 0.5 reaches Elo only when correct=True (:179 falls to 0.0
  otherwise); my probe: reward 0.5, correct False, Elo took 0.0 (984.0 after one update
  from 1000). Contamination is bounded to the correct-answer subset; still real.
- CONVERGENT tag justified: state/NIGHT_LOOP_20261005.md:143 carries "13 dead fleet fires
  under LastTaskResult 0" verbatim.

### Finding 3 (law pack half-proven) - CONFIRMED in full
- Reproduced: my run printed 1583 and header "[compile v0.4 2026-10-06, weight=recency x
  shape, counts are provenance only]" (the lens's quoted header truncates after the date;
  nit).
- Both named amendments ride the rendered pack: my greps "POST-DATUM in out" = True and
  "MOUNTED AT BOOT in out" = True. The amendment renders with spaces (flash field,
  memory/corpus/quantized_thought/instructions_flash.jsonl row 5: "AMENDMENT (2026-10-05,
  R4b ouroboros move 6): MOUNTED AT BOOT"); the lens wrote it hyphenated. My first probe
  for the hyphenated form returned False and would have produced a false correction had I
  not re-checked the spaced form.
- Seam: def _quantized_laws at mag/context_pack.py:436, wired into the pack build at :1048
  ("quantized_laws": _quantized_laws()), so any seat whose boot builds a context pack
  inhales it; the falsifier narrows to seat classes whose path never builds one.
- Falsifier source verified: state/NIGHT_LOOP_20261005.md:260-262 ("no cheap seat has yet
  been shown booting on the fresh pack (seat inhalation, not compile coverage, is the
  falsifier for 'propagated')").
- Seat-side leg: still OWED; I booted no seat either.

### Finding 4 (Hermes live, one-key picker) - CONFIRMED, move re-scoped by the estate's own bytes
- Ledger byte-verified: my tail -3 memory/runs/hermes_burn/usage.jsonl shows exactly the two
  rows: H247_A2_TOKEN_CUE_FAMILY_TABLE 2026-10-06T23:55:08Z cost 0.0233 and
  H247_A3_QUEEN_WELD_MAP_DRAFT 2026-10-06T23:55:27Z cost 0.0104, both
  anthropic/claude-haiku-4.5, ok=true; pair sums 0.0337 as claimed.
- Picker: tools/hermes_burn.py:83-93 returns the first non-empty of (HERMES_API_KEY_2,
  HERMES_API_KEY_1); my grep "402" over the file hits only the :84 comment, zero 402
  handling code. No per-ask failover, confirmed.
- SHARPENING: the move (flip key on premium 402 and remember) presumes the other key holds
  premium credits. The estate's own bytes say neither does as of their last receipts:
  :84-85 (2026-10-01 probe: key 1 402s on premium anthropic SKUs, key 2 carries the
  credits) and commit a3d9d614d F1 ("key2 premium credits aged out - haiku workhorse rung
  is the 24/7 shape today, premium needs top-up or per-ask cross-key failover amendment").
  The live branch is therefore the finding's own falsifier branch: double-402 detection +
  memory/attention.md alert, premium top-up operator-gated. I fired no paid probe to
  re-test credits.

### Finding 5 (three stashes) - CONFIRMED and upgraded to byte level (the lens asserted message-level only)
- git stash list: exactly three stashes on mag/run-beta1-factory-build-audi-20260806T231709Z,
  bases ebcd2583d / 23d76bb71 / e0ff8cec0 as the lens listed.
- My git stash show --stat: stash@{0} = 58 files, +622,692/-169,970 (incl.
  tools/workflow_gate.py +232, tools/mickey17_v2_fold.py +175, mag/claims_verify.py +259,
  5 test files, watch/inbox/PACK_OFFLOAD.jsonl +196, watch/inbox/STEALTH_MINED_FINDINGS.jsonl
  +26). stash@{1} = 42 files, +648,942/-741,306, including dashboard/data/ESTATE_INDEX.jsonl
  and watch/ESTATE_INDEX/ESTATE_INDEX.jsonl as binary 2,523,006,985 -> 4,150,418,528 bytes.
  stash@{2} = 96 files, +47,952/-3,169, incl. watch/inbox/PACK_OFFLOAD.jsonl +4,384.
- Loss risk is no longer message-level: dropping any stash destroys six-figure line deltas,
  and stash@{1} holds a 4.1GB index. The 40-minute land-or-drop move is underpriced for
  stash@{1}.
- CORRECTION: "stash@{0} carrying the operator-gated GSTD join" is message-echo; that
  sentence is git stash list's display of the BASE commit ebcd2583d's subject. My grep of
  the stash@{0} diff for gstd hits catalog index rows (GSTD_INCORPORATION_PLAN seal paths),
  not join code; the join attribution is unverified at byte level.
- ADDITION: PACK_OFFLOAD.jsonl, the file this lens's own blind spot called unread, exists
  inside the stashes (uncommitted rows in all three); the floor is reachable via
  git stash show -p stash@{N} -- watch/inbox/PACK_OFFLOAD.jsonl without touching the tree.

### Finding 6 (P0 gate skipped, gate healthy) - CONFIRMED with one unsupported sub-claim
- Verified: githooks/pre-commit:1-13 is the P0 secrets gate (exec
  tools/precommit_secret_check.py); git config core.hooksPath = githooks; my probe
  bash githooks/pre-commit exited 0 today (same result as the lens).
- The admission is at watch/inbox/selfimp/imp002.md:52 ("Pre-commit hook broken (path
  resolution C:\c\... on MSYS) - bypassed with --no-verify; files manually verified
  clean"); the lens cited :49-52, which covers it.
- UNSUPPORTED: "the skip also bypassed the pre-push ratchet and citation gates for that
  commit." git commit --no-verify bypasses pre-commit and commit-msg hooks only; pre-push
  is a separate hook event at push time, and the cited receipt discloses only a commit-time
  bypass. No byte this sitting shows the push was also --no-verify. Strike the sub-claim or
  re-source it.
- The harness-context defect (C:\c\... under the ZCode harness's own git execution context)
  remains untestable from this seat, exactly as the lens said; my direct-path exit 0 does
  not clear it.

## Additions

1. ACTOR-LEG GREEN-ON-DEAD (finding 2 strengthened): probe proof above; a fully synthetic
   session reads ok=True on BOTH legs. Falsifier: a bridge that raises on fallback, or a
   sample stamped from the returned dict's ok field, would flip actor ok to False. Move:
   extend the CONTAMINATED banner to the actor fallback flag (+5 min on the same 30-min
   edit).
2. STASH BYTE CENSUS (finding 5 upgraded): the three --stat counts above. Falsifier: stash
   diffs that reduce to empty against history. Move: land-or-label each with byte counts
   attached, 90 min (repriced from the lens's 40).
3. PRE-PUSH EXTENSION UNSUPPORTED (finding 6): imp002.md:52 names only a commit-time
   bypass. Falsifier: a push-time --no-verify record (enforcement trail or FIRE_LEDGER row)
   would re-source it. Move: strike or re-source, 10 min.
4. ENGINE-FILE PROVENANCE (finding 1): the standing engine's only durability is the
   gitignored disk copy plus the saved-workflow registry (ListSavedWorkflows shows
   ractor-engine with topic required, no guard concept). Falsifier: a force-tracked
   baseline (git add -f) would make git the baseline. Move: when the guard amendment lands,
   stamp it in-file like :39 does ("topic guard amendment 2026-10-06") so the next break
   pass can date the cure, 2 min inside the 15-min cure.
5. REGISTRY NIT: the saved ractor-engine's moonshots default carries a stray carriage
   return (ListSavedWorkflows: default "2\r"; Number("2\r") === 2, harmless today, a CRLF
   save artifact). Falsifier: registry re-save renders "2". Move: clean on the same amend,
   1 min.

## Checks not run

pytest / census / ratchet (AGENTS.md law: nothing substitutes; no verdict above rests on a
substituted check), seat boot (finding 3's open leg), the harness-context git probe (finding
6), the R4 S5 orphan re-census, a paid 402 probe (never from a break lane), run-record
introspection (ListWorkflowRuns returned workflow_introspection_unavailable). The flash
jsonl has 12 rows (my grep -c .); I did not audit the other 11.

Filed by break-moonshot-2, second pass on the 2026-10-06 fire. No em-dash bytes.
