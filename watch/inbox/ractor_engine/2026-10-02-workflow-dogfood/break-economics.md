# BREAK-ECONOMICS (hostile second pass on lens economics) - 2026-10-02-workflow-dogfood

Pass run this sitting (moment 2026-10-04T03:5x-04:2xZ, inside Ractor-dogfood-workflows,
dwfrun id ...3397f570bf0b, running). Target: `economics.md` in this folder (the lens's
banked write-up; the ask's JSON truncated its finding 4 and omitted finding 5, both
recovered from the banked file and verdicted here).

## INSTRUMENTS RUN THIS SITTING (all commands executed by me)

1. Read-only sqlite census, rerun of the lens's own instrument:
   `.venv/Scripts/python.exe` over `file:C:/Users/foste/.zcode/cli/db/db.sqlite?mode=ro`,
   `PRAGMA table_info(dwf_run)`, full `SELECT` of all 138 rows ordered by time_created,
   status sums, per-name detail, sha1 grouping of script_text, and
   `difflib.SequenceMatcher` ratios of run scripts against the 19 saved files in
   `.zcode/workflows/`. Scripts at `%TEMP%/break_econ_census_hostile.py`,
   `break_econ_dump_all.py`, `break_econ_hashmatch.py`, `break_econ_fuzzymatch.py`,
   `break_econ_ratios.py`, `break_econ_engines.py`, `break_econ_args_diff.py`.
2. `ListSavedWorkflows` (harness tool): 19 saved project workflows this sitting.
3. Reads: `watch/inbox/OPERATOR_WORKFLOW_DIVE_20261003.md` (full),
   `watch/inbox/STANDING_WORKFLOWS_20261001.md` (full),
   `watch/inbox/envelope_50w_20261003.md` (full),
   `watch/inbox/ractor_engine/2026-10-03-surface-migration/break-economics.md:95-112`,
   `memory/workflows/REGISTRY.jsonl` (75 rows), the four claimed olm-mine consumer
   files (grep with line hits), the five `frontier_olm_*` RECEIPT.md files (grep),
   `economics.md` (the lens's write-up, full).
4. Git: `git log --format=%H %s -1 04f83c0b9`, `git show 04f83c0b9 --stat --format=%B`
   (grep dogfood|48h|errat: zero hits), same for 0c9d72a06.
5. `grep -ril "the-50" watch/inbox --include="*.md"` (the-50 receipt sweep).

## LIVE-FLEET DELTA since the lens's 02:40Z snapshot

The census moved under me exactly as the lens warned: lifetime total 5,073,302,554
(lens) -> 5,110,926,683 (my first read) -> 5,111,562,181 seconds later; the three
running rows (OLM 1003-retry 144.8M, Gap-analysis-evening 20.7M, Ractor-dogfood-workflows
14.6M) are still banking. Dead rows are frozen at 58 / 1,084,080,208 (nothing new died).

## VERDICTS

### Finding 1 (dead-attempt tax 1.08B / 21.4 percent, 58 of 138 rows, first-fire shape, dwflint move): CONFIRMED

My census reproduces the lens's numbers to the byte: failed 35 (510,663,324) +
cancelled 23 (573,416,884) = 58 rows, 1,084,080,208 tokens; at the lens's total that is
21.37 percent (their 21.4 checks), at mine 21.21 percent. 138/58 = 2.38 ("every 2.4
fires buys one dead row" checks). CONVERGENT with the dive as claimed:
`OPERATOR_WORKFLOW_DIVE_20261003.md:27` (54 of 134, 40 percent) and `:81` (week 38
459M + week 39 594M = 1.05B). Shape rows verified individually: Frontier OLM mine is
exactly 2F+1C (36.3M F, 120.1M F, 199.1M C on 09-29); game digs 34 rows, 643,862,449
tokens, 5 completed / 29 dead (85.3 percent) - the lens's 643.9M is exact. Nit: "54 of
134" sits at dive line 27, not section 4, and the dive's own section 4 split (35/75 +
19/58) sums to 54 of 133 - the dive is internally inconsistent by one row; the lens
quoted the headline. Nit 2: "first-fire tax" holds for the mega-fanouts but the daily
olm-mine burns completed first-fire clean on 10-01/02/03 (single rows, no dead
predecessors); the tax concentrates in new-script bringups, above all the game-dig
veins. Does not change the verdict or the dwflint move (dive `:145-149`, 2-3h,
target under 15 percent - all verified).

### Finding 2 (5 of 12 have one-or-zero fires; the-50's saved script zero recorded fires; retire 4, fleet 8): CONFIRMED, and SHARPENED

Every count byte-reproduces from my full 138-row dump: drop-dig 1 fire
(Localfirst-steal-wave completed 41,860,718 on 10-01 08:56 - the "41.9M, 10-01" checks);
librarian-expedition 2 rows, 1 clean (cancelled 0 + completed 37,569,179); tree-doctrine-dig
1 fire 106,564,604 on 09-25 18:59, never re-fired; salon-mine exactly 6 attempts, 1 clean
(Salon-vault-stragglers completed 66,293,099); the-50 both fires 09-19 145,082,193 +
09-25 54,839,322, all predate the saved script's gate PASS at
`memory/workflows/REGISTRY.jsonl:17` (ts 2026-09-26T05:36:09Z, digest 181043acdc31).
Absence claims hold on the named instruments: zero the-50 rows post-09-26 in dwf_run
(full history read), and my `grep -ril "the-50" watch/inbox --include="*.md"` returns
only 09-26..09-28 THE-50-PROGRAM-era files, no post-09-26 receipt naming the saved
workflow as fire instrument. `envelope_50w_20261003.md:6-10` verifies the Task-agent
claim (the lens's "lines 5-8" cite under-covers by two lines; the sentence ends at
line 10). `STANDING_WORKFLOWS_20261001.md:21` still lists the-50 in the proven column.
SHARPENED by my script census (below): it is worse than "dormant" for mickey17-v2 -
the saved scripts of the-50, mickey17-v2, and the-gala have likely NEVER fired as-saved.

### Finding 3 (olm-mine the only proven recurring EV; 1,168.2M / 23 percent; cron signature; 4 consumers; never a banked usage line): CONFIRMED

All 9 run-rows verified; sum reproduces to 1,168.2M at the lens's moment (36,322,202 +
120,100,565 + 199,092,495 + 115,615,679 + 131,039,216 + 133,353,713 + 146,739,138 +
156,495,961 + ~129.4M retry), = 23.03 percent of the 5,073,302,554 lifetime. Per-day
numbers exact (133.4 / 146.7 / 156.5M; retry now 144.8M). Cron signature: time_created
14:01Z (10-01), 14:04Z (10-02), 14:01Z (10-03) - nit: the lens says "fires at 14:01Z on
10-01/02/03"; 10-02 was 14:04Z. Matches `STANDING_WORKFLOWS_20261001.md:11`
(automation-cac38363). All four consumer files grep-verified this sitting:
`watch/inbox/fillball/percolator-candidates.md:29,45-46`,
`watch/inbox/librarian_exp/cited-missing.md:10,81-82`,
`watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:10-11,77`,
`watch/inbox/gala_20260925/fillball-1001_RECEIPT.md:45-46,69,72`.
"Never carried a banked usage line": verified for frontier_olm_2026-10-01, -10-02,
-10-03, and -0928 RECEIPT.md (zero self-spend lines); nit: the 10-02 RECEIPT line 149
carries a usage.jsonl recount of the hermes_burn PAID ledger (a different ledger), a
hostile reader could misquote it as a usage line; the daily's own dwf spend is banked
nowhere in its receipts. The 09-30 folder's RECEIPT.md existence was not confirmed
(ls showed DIGEST/lens/register/percolator in the first 4 entries) - the "never" is
verified on 4 of 5 daily folders, instrument named.

### Finding 4 (ractor-engine the fleet's favorite customer; 6 fires in 72h; consumption 2 of 6; self-steal flat): WEAKENED (two cites fail byte-check), pattern stands

The 6-run list byte-verifies: Ractor-dogfood-gaps (failed 28,474,809 + completed
54,012,221), Dogfood-48h (44,0), Ouroboros-meta (63,371,741), surface-migration
("Ractor: the surface migration question", completed 49,810,504), Ractor-fleet-meta
(cancelled 0 - dated 10-03 22:37Z in the db, the lens says 10-04), Ractor-dogfood-workflows
(running, this run). Dive cite verifies: `OPERATOR_WORKFLOW_DIVE_20261003.md:78` does
cite `ractor_engine/2026-10-03-surface-migration/break-economics.md:103` (which exists;
nit: its line 103 is the A1-refire section, the dive's own tavern pointer is imprecise).
TWO FAILURES: (1) the ~324M figure does not reproduce - the named rows sum to 253,410,048
at the lens's snapshot, and no row set I tried reaches ~324.1M; same defect in the
lens's census table (mickey17 "~313M" vs my 333.5M over the 7 mickey17 rows). (2) The
second consumption cite is the WRONG HASH: `git show 04f83c0b9` (CONSENSUS GATE)
carries zero dogfood/48h/erratum text; the dogfood-48h erratum rides commit 0c9d72a06
(MODEL GARDEN NIGHT, via the AGENTS.md clippy carrier that strikes its "42 tests"
claim). So consumption is verified for 1 of 6 ractions by the lens's own evidence,
not 2 of 6. The self-steal cite is faithful to dive section 2 loop 1 (line 44, "91 to
102 (flat)") but the dive's raw meter at line 16 reads 91/92/130/89/102 - week 3 sits
at 130, outside the quoted band; the lens copied the dive's rounded summary. The
qualitative claim (meta-loop concentration, the 54.0M + 44.0M = 98M repeat pair, the
steering-rule move) stands.

### Finding 5 (the gap-analysis -> fill-ball loop exists in law, not code; manual handoffs; no saved chain): CONFIRMED

Timestamps byte-verify: Gap-analysis-100m 10-01 22:00Z completed, Librarian-gathering
10-01 22:54Z cancelled + 22:57Z completed, Fill-ball-one-sittings 10-02 03:51Z
completed, Fill-ball-amend failed 0-token 10-03 22:38Z. ListSavedWorkflows this
sitting: 19 saved, none chains the pair (falsifier not triggered). Sharpened by my
args_json read: Fill-ball-one-sittings args carry GAP_REGISTER-derived lanes
("GAP_REGISTER rank 2..."), so the handoff provably rode seat-held context between
three separate fires, exactly as the lens claims.

## WHAT THE LENS MISSED (additions)

### A1. The fleet is config, not code: 21 runs share one byte-identical engine

sha1 grouping of all 138 script_texts: script 82c6d8bc36 (21,527 bytes) ran 21 times
for 485.9M tokens under 17+ names: Localfirst-steal-wave (drop-dig), Spiking-wide-dig,
Librarian-gathering-expedition, all 6 salon rows, Fill-ball-one-sittings, Ouroboros-meta,
Hitler-dig, DD-selfsteal, Build-it-all, Wide-dig-Grok-bot, Fill-ball-amend, Music-ractor,
Lyric-workover, Vonnegut-final-cut. The script text contains ZERO topic tokens (no
"salon", "librarian", "Spiking", "localfirst", "PAM", "hitler", "ourob" anywhere);
identity lives entirely in args_json (every one passes division-B lanes - the ballroom
shape). Salon-vault-stragglers vs Librarian-gathering-expedition script ratio = 1.000.
The saved .dwf.ts files are 94-97 percent clones: salon vs librarian ratio 0.944
(48 diff lines, mostly the description strings), drop-dig vs wide-dig 0.949 (49 lines).
So the honest engine count is ~7 distinct script bodies across the 12 named workflows
(olm-mine 24,558; ballroom battery 21,527; ball v1 19,923; ractor-engine 14,346/14,858;
the-50 13,619; gap-analysis 21,221/25,550; mickey17 variants; tree-doctrine 28,804;
game veins ~8.6KB), not 12 or 19. The lens's "8 real standing entries" is directionally
right for the wrong reason: the fleet is one engine plus per-fire lane configs.
Falsifier: any two of those runs with differing engine logic, not just differing args.
Move: dwflint addition - hash the fired script, bank it on the run row, and let the
fleet table group by engine not by name, 1h.

### A2. Four saved scripts have never fired as-saved (stronger than the lens's retirement case)

Closest-ever fire ratios against the saved files: the-50.dwf.ts 0.839 (both its fires
are byte-identical to each other but are the pre-gate 13,619-byte version; the saved
18,831-byte gate-passed script has zero fires); mickey17-v2.dwf.ts 0.706 (the 09-25
v2.1 first fire, which predates the file's 09-26 16:33 mtime; the last mickey17-named
fire, Mickey17 Wave 3 09-28, is ratio 0.016 - a different program entirely);
the-gala.dwf.ts 0.750 (the 09-29 balls ran a 19,923-byte ancestor; the saved 22,814-byte
file was git-tracked only 10-01 14:22, "track the-gala.dwf.ts (O1 continuity cure)").
The lens retires these on "dormant/superseded"; the byte truth is never-fired-as-saved,
which makes the retirement pass even safer. Falsifier: a dwf_run whose script hash or
full-text ratio exceeds ~0.95 against any of the three current files. Move: fold into
the lens's own 30-minute retirement pass, +10 min.

### A3. The lens watched the 02:33-02:34Z re-gate sweep without identifying it

REGISTRY rows 64-75 are a full re-gate of all 12 named workflows at
2026-10-04T02:33:47Z-02:34:06Z, all PASS (a sibling lane in this run, most likely).
The lens's own growth arithmetic reconciles exactly: 81,244 - 68,840 = 12,404 bytes =
those 12 rows (12,392 bytes LF + 12 CRLF). Consequence: every retirement-description
amendment the lens proposes edits against fresh PASS rows from today, not stale ones.
Falsifier: none needed (positive finding). Move: none (already current).

### A4. REGISTRY carries a ghost gate row: PASS for a workflow that does not exist

`memory/workflows/REGISTRY.jsonl` has a PASS row for "Wide-dig-the-Grok-bot-ecosystem.dwf.ts"
at 2026-10-03T20:18:03Z, but `.zcode/workflows/` holds 19 files and none by that name.
Gate rows are checks, not saves - a REGISTRY PASS is not proof a fleet entry exists.
This also corrects the lens's census-table line "Grok-ecosystem 10-03 via a NEW script":
the Grok-ecosystem fire (failed 0 + completed 30,403,431) is in the SAME 82c6d8bc36
ballroom group as Spiking - same script, not a new one. Falsifier: the file appearing
on disk. Move: dwflint cross-check REGISTRY names against .zcode/workflows on every
gate run, 20 min.

### A5. The spent_tokens double-count worry is real: a concrete instance

The lens left resumed-run double-counting as blind spot 2, untested. Tested this
sitting: Salon-mine-20deep cancelled (10-02 01:09) and Salon-mine-20deep failed
(10-02 14:38) carry the IDENTICAL spent_tokens value 25,087,198 on both rows - the
resumed successor re-banked the parent's count, so row-sums double-count that 25.1M
(it is dead in both rows, inflating the 1.08B dead tax by ~0.5pp). Other resumed
pairs accumulate instead (Ractor-dogfood-gaps 28.5M -> 54.0M), so the defect is
per-family, not universal. Falsifier: adapter-side proof that both salon rows are
distinct token spend. Move: dedupe resumed children from EV sums (resumed_from is on
the row), 15 min inside dwflint.

## ERRATUM against the lens (byte-check failures, one line each)

1. Commit hash: the dogfood-48h erratum rides 0c9d72a06, not 04f83c0b9 (git show, zero
   dogfood/48h/errat matches in the latter).
2. Raction family total: named rows sum to 253.4M, not ~324M (also the census table's
   mickey17 ~313M vs 333.5M actual over its 7 rows).
3. Consumption 2 of 6 is really 1 of 6 on the lens's own evidence (item 1).
4. Self-steal "91-102 flat" hides the dive's own W3=130 (dive line 16 vs line 44).
5. "5th-largest single-run spend" for tree-doctrine (banked economics.md): it is ~12th
   overall / ~9th among completed (199.1, 172.2, 145.1, 139.7, 136.3, 133.4, 122.0,
   120.1, 115.6, 111.2, 106.9, then 106.6).
6. Nits: "fires at 14:01Z on 10-01/02/03" (10-02 was 14:04Z); Ractor-fleet-meta is
   10-03 22:37Z, not 10-04; "54 of 134" lives at dive line 27 and the dive's section 4
   split sums to 133; envelope cite is lines 6-10, not 5-8.

## NOT RUN (stated, not guessed)

- Task-agent fan-out census: the dive used the sessions table for it; I did not rerun
  that instrument, so the lens's blind spot 1 stands as adopted, not re-verified.
- Provider-bill audit of spent_tokens: not run (no bills in reach); A5 gives one
  internal-consistency instance only.
- bob-laptop and phone fires: absent from db.sqlite (dive caveat, adopted).
- frontier_olm_2026-09-30 RECEIPT.md existence: unconfirmed (ls truncation), so the
  "never a usage line" claim is verified on 4 of 5 daily folders.

## MINIMUM VIABLE FLEET (my restatement after the byte pass)

One ballroom battery (config per fire) + olm-mine (the only recurring, consumed line)
+ ractor-engine (rate-limited meta arm) + the-50's width role (already absorbed by
Task agents at width 50 per envelope_50w). Roughly 4 engines do everything the 19
saved entries claim; retirement of 4 (the-50, mickey17-v2, tree-doctrine-dig,
drop-dig) is safe, and the deeper move is saving lane-configs as args presets on ONE
battery, not as 12 script files.
