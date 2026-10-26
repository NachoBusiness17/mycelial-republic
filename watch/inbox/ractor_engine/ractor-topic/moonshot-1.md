# moonshot-1: the ractor that rode "undefined" (2026-10-02)

Lens: moonshot, ractor-engine run banking to `watch/inbox/ractor_engine/ractor-topic/`.
Moment of writing: 2026-10-02T01:52-01:56 EDT, all checks run this sitting unless marked
carried. No em-dashes. The topic under raction arrived as the literal string
"undefined"; this lane treats that fact as the finding, then rides the estate bytes
the run touched anyway.

## Finding 1: this run is a zombie and the engine cannot know it

The run fired with BOTH required args unbound. Evidence chain, each byte read this
sitting:

- My own ask carries "The topic under raction: undefined" verbatim, and banks to
  `watch/inbox/ractor_engine/ractor-topic/moonshot-1.md`.
- `.zcode/workflows/ractor-engine.dwf.ts:90`: `const SLUG = String(args.slug || "ractor-" + String(args.topic || "topic").slice(0, 24)...)`. The bank path `ractor-topic` is reachable only when BOTH `args.slug` and `args.topic` are absent. If topic had been the literal string "undefined", the slug would derive to `ractor-undefined`. The pair of facts pins it: both keys absent.
- The frontmatter declares both `required: true` (`ractor-engine.dwf.ts:34-37` slug, `:39-43` topic). The run fired anyway. The contract is decorative in this invocation path.
- `tools/workflow_gate.py:45-80`: G1-G7 are regexes over the script TEXT only. No check consumes args at submission. `memory/workflows/REGISTRY.jsonl` rows `2026-10-02T01:52:29Z` (draft) and `2026-10-02T05:48:34Z` (saved) both read `verdict: PASS` G1-G7 for this exact script. The gate certified a script that happily rides nothing.
- The engine body never guards: no throw on empty topic exists anywhere in `ractor-engine.dwf.ts:89-160`; line 141 logs "Riding N lenses on: " + String(args.topic) (inferred from code, log not observable from this seat).

So 8 lenses, 8 hostile breakers, a steering round, and a synthesis voice are burning
estate reads on the string "undefined", and the run will complete cleanly, publish a
primary artifact titled "Ractor: ractor-topic", and look like work.

Falsifier: an invocation transcript showing topic/slug were actually passed and the
harness dropped them in binding (moves the defect upstream; does not save the run),
or a run log line showing args.topic non-empty.

Move (one sitting, ~20 min): phase-0 fail-fast in the engine (`throw` when
`String(args.topic ?? "").trim()` is empty or "undefined") plus a G8 arg-guard
scenario card in `configs/workflow_gate_scenarios` minted from THIS run; then
amend/refire with a real topic.

## Finding 2: salvage without a validity gate amplifies the waste

Everything the engine checks is shape; nothing checks the run is about anything.

- Turn gates + report rows bank unconditionally (`ractor-engine.dwf.ts:165-206`): a dead run keeps banked work, and an invalid run keeps it just as faithfully.
- The receipt check is existence only (`:310-324`): `files.glob(OUT + "/SYNTHESIS.md").length > 0`, then `artifact.file(..., primary: true)`. A synthesis about "undefined" passes every gate on the path to the operator's screen.
- Gate G4 checks only that `report( x );` appears (`tools/workflow_gate.py:62-65`).
- Bonus, byte-read: BOTH registry rows for this engine carry `G6-receipts ok: false` soft-warn ("receipt mention lacks a dated stamp", per `tools/workflow_gate.py:86-88`, whose stamp RE wants a `fetched: YYYY-MM-DD` family line while the engine's date convention lives in the slug, `ractor-engine.dwf.ts:34-37`). The engine generates a soft signal about its own receipt law that nobody consumed before firing. Two instruments disagreeing, no adjudicator: the logic lens jacket (`ractor-engine.dwf.ts:116-117`) wearing its own jacket.

Falsifier: if this finding survives the hostile pass and the synthesis + artifact
description carry the unbound-topic notice verbatim, the damage is contained and the
falsifier fires in the good direction; the bad direction is a published SYNTHESIS.md
with no notice at all.

Move (~15 min): report a `{topic_bound: true/false}` validity row from phase 0 and
require the synthesis prompt (`:298-303`) and the artifact description (`:320-324`)
to carry it verbatim.

## Finding 3: the real burning edge the undefined topic obscured

Five scheduled tasks wear result=1 from their 10-01 fires and the wrapper fix has
not landed. Checks run 2026-10-02T01:52:53-04:00:

- `Get-ScheduledTaskInfo`: MagImproveDaily result=1 next 08:00, MagLeaveProtocolDaily result=1 next 08:00, MagCensusPatrolDaily result=1 next 08:30, MagFtsIndexDaily result=1 next 09:00, EstateWalkDaily result=1 next 09:15 (expected; pre-fix fire).
- `scripts/invisible_runner.vbs` mtime 09/30/2026 10:59:12, UNTOUCHED since the prior synthesis named its quoting defect; the quote-wrap + `shell.Run("cmd /c " & cmd)` is still at lines 21-27 in my read.
- `logs/census_patrol.log` mtime 09/30/2026 08:30:28, ends `[2026-09-30 08:30:02] END exit=1`: the 10-01 08:30:30 fire (LastRunTime confirms it fired) wrote ZERO bytes. The estate's count-truth instrument is entering its third dark day at 08:30 today.
- `logs/fts_index.log` mtime 09/30/2026 09:00:21, same dark-on-10-01 shape: the B2-465 FTS healer ("no START stamp for today means the surface is dark", AGENTS.md) has been dark a day too.
- Fresh count this sitting: `(Get-ChildItem tests -Filter test_*.py -Recurse -File | Measure-Object).Count` = 496, against the AGENTS.md census claim of 455 files (2026-09-30 census, 3,550 collected). +41 test files in ~31 hours with no instrument watching. Not run: pytest itself; 496 is a file count, not a collected census.

Falsifier: the 08:00-09:15 wave today landing green (exit=0 END lines in all four
logs) would disprove the unhealed-wrapper claim; a recount landing at 455 would kill
the drift claim.

Move (~45 min, before 08:00): execute the prior synthesis's move 1, swap the four
wrapper task actions to the smoke-proved direct `powershell -File` pattern
(EstateWalkDaily proves it: `logs/estate_walk_daily.log` ends `END 2026-10-02T00:37:54Z exit=0`,
mtime 10/01 20:46:30, my read), or fix the vbs quoting with the rc=7 probe; hand-fire
each; require an exit=0 END line per log. Then hand-run `census_patrol_daily.ps1` and
file the real census with attribution (496 vs 455).

## Finding 4: fixed-never-recorded is accelerating

In the hours since the prior ractor's synthesis, at least two more GAP_REGISTER rows
closed while the register itself has not moved.

- Rank 3 (citation lint): `githooks/pre-push:24-25` now reads `.venv/Scripts/python.exe tools/citation_lint.py check --changed || exit 1` (my read). The prior synthesis read it UNWIRED at 00:27 tonight ("grep citation_lint githooks/pre-push = 0 hits", `watch/inbox/ractor_engine/2026-10-01-dogfood-gaps/SYNTHESIS.md:22-23`), and the prior moonshot lane had seen NO tool on disk at all earlier that evening (`2026-10-01-dogfood-gaps/moonshot-1.md:13`). Nonexistent to wired inside ~6 hours.
- Rank 4 (ERRATA): absent at the synthesis's 00:29:50 check, exists by 00:33 (SYNTHESIS.md:25-26, carried).
- `watch/inbox/gap_analysis_20261001/GAP_REGISTER.md` mtime still 2026-10-01 18:41:58 (my check just now): the table that ranks those rows open has recorded nothing. AGENTS.md carries the wired gate (the a05-r2 paragraph), so conversion-by-reader works; conversion-by-ledger still does not exist. The prior synthesis predicted this exact repeat; it took under two hours to come true again.

Falsifier: a GAP_REGISTER.md or TICKET_LEDGER.md mtime newer than the closures with
status rows for ranks 3/4 kills "nothing records the fills"; evidence the closures
predate the synthesis's reads would kill the acceleration claim.

Move (~45 min, or 5 min for the small version): the prior moonshot lane's swing,
started at toy scale: append status/checked-at/checked-by to the 12 rows and record
tonight's closures with path receipts; or accept AGENTS.md as the recording surface
of record and stamp the register FROZEN with a pointer.

## Honest limits (blind spots)

- I cannot see the invocation site: who fired this run and with what args. Where the
  args were dropped (caller UI vs harness binding vs script defaults) is OWED. My
  zombie diagnosis is pinned to what reached MY seat, which is direct observation.
- I cannot see the other 7 lenses' outputs or the run log; claims about what the run
  will publish are derived from the script, not observed.
- 496 is a file count, not a pytest census; I did not run pytest this sitting.
- I did not reproduce the vbs quoting defect (no rc=7 probe run); the defect
  attribution rides the wrapper source plus the prior run's carried receipts.
- The intended topic, if any existed, is unknown to me; this ride substitutes the
  run's own failure as topic and the estate's live edge as ground.

## Steering round correction (2026-10-02 ~02:25 EDT, hostile pass verdict: weakened)

The hostile second pass killed three sub-claims of Finding 3. Re-checked against the
bytes this sitting; all three kills CONFIRMED, finding corrected:

1. "No instrument watching" was FALSE. My own run this sitting:
   `.venv/Scripts/python.exe tools/census_drift_patrol.py` prints
   `CENSUS-PATROL: ok - census 2d old of 7d bar, growth noted but inside the window
   (23 file(s) since census), disk 497 vs carrier 455 (instrument lag ... evidence only)`,
   `patrol exit=0`. The tripwire SEES the drift and passes it as evidence-only inside
   the window (`tools/census_drift_patrol.py:301-307` STALE = age > 7d AND grew;
   `:322-328` the inside-window evidence lines). The corrected claim: the drift is
   instrument-VISIBLE but UNENFORCED, and the only daily enforcer of the
   collected-count claim (MagCensusPatrolDaily's `--collect` deep check, the B2-246
   daily task) is itself one of the wrapper-dark tasks. The watcher of the watcher
   died; the tripwire it supervises cannot fail on collected drift by design.
2. "Third dark day" overcounted. 09-30 was red-but-LIVE (census_patrol.log ends
   `END exit=1`, a real run reporting drift); 10-01 was dark day ONE (task fired
   08:30:30 result=1, zero log bytes); today 08:30 would be dark day TWO.
3. fts and EstateWalk qualifiers. fts_index.log's last state is GREEN
   (`END exit=0` 09-30), so the shared 10-01 anomaly is precisely "task result=1
   with zero log bytes", not a shared color. EstateWalkDaily is the
   fixed-pending-test case: task action is DIRECT powershell -File (my action pull:
   `exec=powershell args=-NoProfile -ExecutionPolicy Bypass -File ...estate_walk_daily.ps1`),
   script green by hand smoke, its result=1 is the stale pre-fix fire, verdict at
   09:15 today. Exactly four tasks ride the wrapper (action pull this sitting:
   MagCensusPatrolDaily, MagFtsIndexDaily, MagImproveDaily, MagLeaveProtocolDaily,
   all `exec=wscript.exe ... invisible_runner.vbs`).

Count note (denominator law): the patrol's 497 counts tests/ rglob of BOTH
`test_*.py` and `*_test.py` (`census_drift_patrol.py:120,188-194`); my 01:52
Get-ChildItem counted `test_*.py` only and got 496. The +1 is glob scope, named per
the instrument-and-moment law.

The exit-code echo on my first patrol run printed empty (bash/powershell handoff);
re-ran in a pure PowerShell wrapper and captured `patrol exit=0`.

---

# moonshot-1, SECOND RIDE (2026-10-06 ~20:30 EDT): the topic arrived "undefined" AGAIN

The 10-02 receipt above diagnosed this exact run shape and named a cure. This section
is the 2026-10-06 lane's own ride; every check below ran this sitting, commands named
inline. Findings F0-F5, then blind spots.

## F0 CONVERGENT with the 10-02 receipt: the cure never landed and the run recurred

The 10-02 Finding 1 move was a phase-0 fail-fast on unbound topic plus a G8 arg-guard
card. Byte truth this sitting: `.zcode/workflows/ractor-engine.dwf.ts:85` still derives
SLUG from unbound args, `:143` still logs `String(args.topic)` with no guard, `:149`
and `:159` still inject it into lens asks; `configs/workflow_gate_scenarios/` carries
G1-G7 plus two G8 width cards and no arg-validity card. And this run's own gate row
minted minutes ago (`memory/workflows/REGISTRY.jsonl` tail: `2026-10-06T22:29:05Z
ractor-engine.dwf.ts PASS`) certified the guard-free engine again. No amendment row
records a rejection. The estate's fold-to-amendment machine, proven GROWS across the
ouroboros night, does not close the loop for a banked finding whose cure is a
`.zcode/workflows/` edit: the receipt banked, the move sat four days, the defect
re-fired identically, and the gate passed it twice. Falsifier: an amendment/rejection
row dated before 10-06 for this cure, or a guard in the engine bytes I misread.
Move (~20 min, one sitting): land the phase-0 throw + the arg-validity scenario card
from the 10-02 receipt, byte-identical move, executed this time.

## F1 the 10x: the 24/7 workhorse is rented while the local-sovereign actor is a three-piece skeleton with no weights

MagHermesBurn247 is live (my schtasks: Status Running, next 21:00 today) and banked
its proof fires on rented haiku: my sum over `memory/runs/hermes_burn/usage.jsonl` =
3,012 rows, $94.6422, matching `watch/inbox/HERMES_247_WIRED_20261006.md`'s $94.64
(H247_A2 $0.0233 + H247_A3 $0.0104 visible in my tail). The repo's own local actor is
verified skeleton: `llama_cpp 0.3.36` IS in the venv (my import probe); the bridge is
uncommitted (`mag/llama_cpp_bridge.py`, working-tree M); `configs/lane_profiles.yaml:17-21`
promises qwen2.5 7B Q4 "vram_fit: true"; my `find . -maxdepth 3 -name "*.gguf"` found
ZERO weights (scoped: repo root, depth 3); and the killer, `mag/selfplay_orchestrator.py:138`
constructs `bridge.LlamaCppBridge()` bare so `model_path` is None and `spawn_server`
(`mag/llama_cpp_bridge.py:65-67`) always returns `{"ok": False, "fallback": True}`;
nothing in the orchestrator reads lane_profiles (my grep: zero hits). The swing, named
by the estate's own QUEEN receipt (`watch/inbox/QUEEN_CHESS_LM_20261006.md:21`: small
seats welded to silent experts beat frontier): the 24/7 queue is the exact A/B bench.
One sitting: commit the bridge bytes, wire lane_profiles model_path through the
carrier as a local rung, download one gguf, fire one haiku-vs-local pair on the same
contract. The $180 meter then funds only premium judgment (402ing today per
HERMES_247_WIRED F1:21; receipt-reported, not re-verified, re-firing spends money).
Falsifier: a gguf census outside the repo (Ollama/HF caches) finding a local model
already carrying workhorse traffic.

## F2 the freshest receipt's F3 is false in its causal half on bytes that predate it

`watch/inbox/HERMES_247_WIRED_20261006.md:23` claims "the law is NOT riding
_system_for(model)". Byte truth: the no-em-dash line rides `_system_for` since commit
b2ca54422 (`tools/hermes_burn.py:181` "No em-dashes anywhere. Plain hyphens only.";
my `git log -S` hit, `git diff` empty, file mtime 2026-10-04 09:05). Yet A2's banked
output carries em-dashes: my U+2014 grep on
`watch/inbox/hermes_burn/H247_A2_TOKEN_CUE_FAMILY_TABLE.md` = 4 lines. Evidence half
true, causal half false: prompt law is present but non-binding on haiku output. The
receipt's named cure (append the law line to the system face) is a no-op already done.
Real cure: carrier-side post-parse em-dash lint plus one re-ask before banking,
extending the `_landed_skip` path (`tools/hermes_burn.py:218-238`), ~20 min one
sitting. CONVERGENT with the R5 communication lens' publish-time re-derivation law
(`state/NIGHT_LOOP_20261005.md:263-270`), violated within 12 hours by the estate's
newest receipt.

## F3 the self-play organ can bank Elo from a placeholder actor with no degraded flag

`mag/llama_cpp_bridge.py:7-8` promises a deterministic-placeholder fallback that
never crashes; the scorer leg has `_fallback_score` returning "0.5"
(`mag/selfplay_orchestrator.py:249`, used at :168); `SessionReport` (:67, :210/:221)
carries no actor_fallback/degraded field. A weightless run reports accuracy and Elo
as if a real actor played. CONVERGENT with the R5 meta-verdict's theater-risk row
(`state/NIGHT_LOOP_20261005.md:142-144`, theater concentrated in GREEN instruments).
Honest scope: static analysis only; I did not run a full session (the scorer leg
spends remote calls). Executable falsifier: run the orchestrator with no gguf and
check whether the report flags degradation (prediction: it does not). Move: add
`actor_fallback: bool` to SessionReport from spawn_server's fallback key, ~15 min.

## F4 three stashes are sole copies of six-figure-line sweeps in cache-only storage

My `git stash list`: 3 stashes on `mag/run-beta1-factory-build-audi-20260806T231709Z`.
My `git stash show --stat`: stash@{0} = 58 files, +622,692/-169,970 lines (rides the
GSD JOIN work whose one owed input is the operator's wallet address); stash@{1} =
42 files, +648,942/-741,306 lines. The shared-surface law (AGENTS.md) makes session
dirs cache-only; a stash is the purest cache-only store, one drop or pop-conflict
from gone. CONVERGENT three ways: R3's sibling-stash finding, `state/CURRENT.md`
owed row, `state/NIGHT_LOOP_20261005.md` next-loop target 3. Move: export each stash
diff to `watch/inbox/stash_vault_20261006/` plus a REDBOARD row, ~20 min. Falsifier:
a diff-vs-HEAD analysis showing the payloads fully redundant with committed bytes.

## F5 my census retires the R4 S2 no-clock claim; next-loop target 1 is built, only the proof is open

`state/NIGHT_LOOP_20261005.md:216-218` kept "no scheduled task carries zknot,
rib_boot, or warm boot" with the caveat "not re-censused beyond the lawpack task
this sitting". My census: `MagBootRegenDaily` exists, last ran 10-06 07:15, next
10-07 07:15, action = `scripts/boot_regen_daily.ps1`, and `mag/boot_regen.py:50-52`
chains all three organs (zknot, warm_boot, rib_boot). The R4 landing wave cured S2
hours before the verdict reporting it froze. The open half of next-loop target 1 is
the communication lens' unproven leg: no cheap seat shown booting on the fresh pack
(NIGHT_LOOP:259-262). Move: one sitting, boot one flash seat on today's pack, stamp
the inhalation proof.

## Blind spots (honest)

- I did not re-fire A1 (premium 402); re-verification spends money, claim stays
  receipt-reported.
- gguf search scoped to repo root depth 3; Ollama/HF caches not censused.
- The self-play session was not run end-to-end; F3 is static.
- I read 4 of ~50 last-48h receipts in depth (HERMES_247_WIRED, QUEEN_CHESS_LM,
  CURRENT.md, NIGHT_LOOP) and listed the rest; lenses on the AMENTI, K8S-fault, or
  stealth-mine threads would return disjoint findings.
- The topic field arrived literally "undefined" for the second time; I cannot see
  the invocation site, so deliberate re-ride vs unbound-args recurrence is
  undecidable from this seat. The guard's absence (F0) is decidable and decided.
- I did not verify stash payloads against HEAD for redundancy; the sole-copy risk
  rides the shared-surface law, not a diff analysis.

## HOSTILE SECOND PASS CORRECTION (2026-10-06, F1 verdicted weakened; correction re-derived this sitting)

The hostile pass killed F1's procurement frame and both kills CONFIRMED on my own
re-runs. (1) My "zero gguf in-repo" was depth-3 scope wearing a no-weights universal:
the untruncated census (`find . -name "*.gguf" -type f -not -path "./.git/*"`)
returns exactly 2 in-repo files, both 240-byte pytest fixtures
(agents/pytest-tmp-59508 and -60084, test_backend_tier_field_lands_0/tiny.gguf).
(2) My own falsifier fired: `ls` of the Ollama manifests shows
library/qwen2.5/ carrying 32b, 3b-instruct, 7b (60 blobs in the store), and the HF
cache holds unsloth/gemma-4-31B-it-GGUF and unsloth/Qwen3.5-4B-MTP-GGUF snapshots
(my find, head-truncated); and a real local session already ran today
(watch/inbox/ractor_engine/2026-10-06-stockfish-coding/operations.md:7: d13
self-play, 8 games, 5 correct, Elo 1033.1). "Download one gguf" is withdrawn.

What survives, sharpened (wiring and report honesty, not procurement):
- configs/lane_profiles.yaml is decorative: my grep for lane_profiles over
  mag/ tools/ scripts/ tests/ hits only tests/test_selfplay_orchestrator.py:157,168;
  zero production consumers.
- The 24/7 carrier cannot reach a local model at all: tools/hermes_burn.py:37,100
  refuse private/loopback/link-local IPs (the SSRF guard), so MagHermesBurn247 is
  remote-rental-only by construction; a local rung needs a sanctioned carrier path,
  never an SSRF bypass.
- The orchestrator default path is a garbage machine, byte-confirmed this sitting:
  main() builds the bare bridge (:138), play_one drops the bridge's fallback:True
  key at :154 (only "move" is read), and the scorer leg stamps BottleneckSample
  ok=True unconditionally at :170 even when flash_call threw and _fallback_score
  answered. CONVERGENT: the operations lens independently landed the same
  death-invisible scorer, dead-endpoint spawn (spawned server never queried,
  generation via 8 in-process Llama loads), and last-write-wins evidence clobber
  (operations.md F1/F2/F4, its :13 and :31).
- Carried, not re-verified by me: the hostile pass's exact byte sizes (18.8 GB
  gemma-4-31B, 3.0 GB Qwen3.5-4B, 154 GB Ollama store) and its operations.md:13
  line read; I verified the models' existence and read the receipt's own :7.

Corrected move (one sitting, ~45 min): fail-closed main() without model_path (no
fallback-branch creep), thread actor fallback + scorer exceptions into SessionReport
fields, commit the d13-proven bridge fixes with the evidence sha256 in the message
(operations.md:27). The carrier local rung is a separate sitting: it needs a
sanctioned loopback dispatch path, not an SSRF bypass.
New falsifier (fires the finding dead): a production .py consumer of
lane_profiles.yaml appears in grep, or the carrier gains a sanctioned local dispatch
leg, or play_one reads actor fallback into SessionReport and main() refuses to run
unconfigured.
