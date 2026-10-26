# BREAK-COMMUNICATION (hostile second pass, 2026-10-10, moment 06:03-06:12Z)

Seat: break-communication. Target: communication.md (this directory), the
interaction-thesis lens. Method: every evidence cite re-run or re-read this
sitting; both falsifiers the lens left open were run to ground (the DB schema
enumeration and the tree-wide pairs census). Instruments banked beside this
file: _break_comm_census.py (raw reconciliation + message.data key census +
session provenance), _break_comm_census2.py (session-separated tape + meter
denominator audit). The DB opened mode=ro both times, per the zknot law. No
em-dashes.

## VERDICTS

### FINDING 1 (attention flood, cure never landed): CONFIRMED, strengthened by three corrections

Byte-checks that passed: `grep -c "probe-alarm" memory/attention.md` -> 128
(exact); append site read this sitting: mag/improve.py:552-556 still appends
one [priority][probe-alarm] line per probe run to the module ATTENTION_PATH
with no caller-root gate, and improve.py:538-543 is exactly how absolute
pytest-tmp refs enter production lines (the "isolated callers" fallback);
`git log --oneline --since=2026-10-02 -- mag/improve.py` shows one commit
only (6685db6bc PORT WAVE), no gate in it; the 2026-10-02 prior lens FINDING 2
(watch/inbox/ractor_engine/ractor-topic/communication.md:22-26) is cited
faithfully (115 count, 40-minute gate prescription). Falsifier CLOSED: my
`schtasks /Query /FO CSV | grep -i "dam|attention"` returned zero tasks, and
tools/attention_dam.py:1-20 (docstring read) is a ONE PASS classifier by
design, no cadence; no root gate exists in the bytes I read.

Three corrections, all of which make the flood worse, not better:
1. "115 of them point at pytest-tmp / %TEMP% roots" UNDERSTATES. My split:
   128 probe-alarm lines = 106 with pytest-tmp + 9 with Temp/suite-burn + 12
   with Temp/(wave5|ball2|ball3|final)_suite_confirm + 1 real. 127 of 128
   are temp-rooted. The lens's 115 was the file-wide pytest-tmp grep count
   (which includes 9 non-probe-alarm lines and misses the *_suite_confirm
   classes).
2. "The one real alarm in that class (QUOTA-DEAD cerebras... attention.md:14)
   is buried under test copies" is byte-wrong on which line is real.
   attention.md:14's own ref is agents/pytest-tmp-54164/... (a test copy).
   All 127 cerebras lines point at temp roots (my grep: zero cerebras lines
   with a production ref). The one production-rooted alarm in the file is
   the 2026-10-04 mlx-cluster/ollama/xai DOWN + QUOTA-DEAD nous line at
   attention.md:526 -> memory/improve/provider_health/2026-10-04.json, the
   same line the 10-06 second pass already named.
3. The count trajectory has an uncited midpoint. The prior-lens file the lens
   says it read in full contains a 2026-10-06 second pass (ractor-topic/
   communication.md:66-127) that counted 119 and classified 118 cerebras
   lines as byte-identical 09-26 fixture artifacts. Growth is 115 -> 119
   (10-06) -> 128 (10-10), monotonic; the "still filling" claim survives and
   sharpens. The convergence is x3 derivations, not x2.

### FINDING 2 (tape provenance-contaminated): CONFIRMED, quantification superseded upward

Reconciliation at my moment (06:03:49Z, window drift explains residuals):
raw 14,057 (lens) vs 14,009 (mine, coalesce-origin text-bearing; strict
origin incl. empty = 14,082); template drop 7,709/135 prefixes (lens) vs
7,666/129 (mine, the estate's own zknot_alarm.template_prefixes instrument
plus a raw-rule variant, identical results); dispatch openers 294 (lens) vs
291 (mine); both verbatim samples byte-present (1 occurrence each); shape
census reconciles exactly: lens 1,766 lowercase + 518 URL + 3,696 capitalized
+ 294 dispatch + ~74 other = 6,348 kept; mine 1,763 + 516 + 3,989 + 75 = the
same distribution (3,696 + 294 = 3,990 vs my 3,989).

Falsifier RESOLVED, and it cuts BOTH ways the lens allowed:
- message.data carries NO channel/dispatcher tag. Full key census over the
  14,009 rows: role, time, agent, model, contextSnapshot, semantics, anchor,
  tools, metadata (13,491), modelSelection, visibility (15), source (12),
  synthetic (12). No provenance field zknot ignores at message level.
- BUT the session table does: task_type + parent_id, the exact filter zknot
  itself applies at tools/zknot.py:119 (parent_id IS NULL AND task_type NOT
  IN child types), which the lens's census did NOT apply while citing zknot
  as the discipline's source. Sessions holding 30d real_user messages:
  6,496 total, of which 4,178 workflow_child + 2,255 subagent_child + 62
  interactive + 1 side_chat; 6,434 of 6,496 have a parent. 6,909 of the
  14,009 raw messages are child-session dispatch wearing the origin flag.
- The separated tape: top-level non-child 30d raw = 7,101 -> 3,199 after the
  template drop (the bulk-cron templates live almost entirely in child
  sessions) -> 3,186 after a dispatch blocklist (only 13 survivors). So the
  naive corpus overstates the human tape by ~4.4x, not the lens's >=2.2x,
  and the lens's blind-spot bracket ("~2-4k/30d") is resolved to 3,186-3,199.
- Consequence for the move: the proposed blocklist is nearly moot; the
  separation zknot already ships does almost all of it. The move survives,
  cheaper than budgeted.

### FINDING 3 (pairs banked one-sided): CONFIRMED, falsifier closed tree-wide with one partial fire

Byte-checks that passed: SKILL.md:85-89 quote verbatim ("with contrast
(wrong move vs corrected move, the MAX_DISTILL shape)"); scoped MAX_DISTILL
grep re-run -> at the lens's moment exactly 4 shape-description hits
(SKILL.md:88, SKILL.md.bak-20261003b:50, SKILL.md.bak-20261004a:50,
zai-reference/sections/10-receipted-from-vendor-docs:39; today's extra hits
are the lens's own file and siblings written after it); verb-genomes
"wrong move" -> 0 hits; registry.json = exactly 12 keys (LAW-1,3,4,6,7,8,9,
10,11,12,12-AMD-1,13); enforcement_trail.jsonl = 1,480 at the lens's moment
per its own citation, 1,490 at mine (06:0xZ, grew 02:55Z -> 05:13Z, last row
same class: LAW-9 "Ostrom-1 boundaries roster present"), drift-consistent;
LAWS_COMPILED_20261003.md = 20,748 bytes exact, and the 66 is the full
register (laws 21-66 as in-file rows, 1-20 as the table by reference, per
the file's own header); correction census 2,862 (lens, keyword list
unspecified) vs 2,661 (mine, named list banked in _break_comm_census.py),
same magnitude, method difference declared.

Falsifier closed: the tree-wide census the lens could not run, now run.
`git grep -l "wrong move"` over the full tracked tree = 23 files, every one
prose receipts/docs/skill cards/binaries (I opened the ambiguous ones:
astra_hold0 QA prompts and ractor-salon.txt are KV-cache essay prose;
DAY1_SKILLS_DOGFOOD.md:167 and RTFM_20260904.md:234 are MORE promises of the
shape, not rows); the 9 untracked files under memory/ contain zero "wrong
move" hits; MAX_DISTILL hits repo-wide are process history (the
corpus/training_materials/zai_trajectory_window_sample_20260905.txt:200 hit
is a cron prompt). NO pairs dataset exists in the tracked repo, absence now
tree-wide with instrument named, not scoped. Partial fire: one prose
contrast pair IS banked in memory/ outside the lens's scoped dirs,
memory/continuity/seat_memory_20260927/no-bulk-self-processing-law.md:14-17
(morning wrong formulation vs evening verbatim correction), and zknot
session cards carry (preceding ask, correction) adjacities (e.g.
memory/zknot/2026-09-25_sess_71c96bdc...md:31-32). Neither is a dataset; the
operational claim ("the pairs sit unmined in the tapes") survives.

### FINDING 4 (counterpart live, zknot meter = the local scoreboard): CONFIRMED, falsifier run and extinguished

All cites byte-verified: DAWN_REPORT_20261006.md item 4 verbatim order
"stop asking for xai reissue its not coming until i have money i do not";
RIB_LIVING_WEIGHTS_BY_NATURE.md:23-24 aphorism line; LATEST.md:3 meter line
byte-exact with internally consistent arithmetic (34+10=44 of 448 -> 98.2
per 1000; 68+24=92 of 748 -> 123); tools/zknot.py:35-44 WARN-only
WORSENED/BASELINE alarm legs as the docstring states.

The falsifier (meter denominator contaminated by dispatch) is now MEASURED:
the zknot-shaped 7d denominator (top-level, non-child, post-template,
>=5-prompt sessions) = 470 at my moment, reconciling with the card's 448 at
its earlier moment; dispatch-shaped messages inside that qualifier bucket =
2 of 470 (0.4 percent), and both samples ("burn the free lanes 24/7",
"Wave protocol: bounded ask/steps/token/show your word/headless") read as
operator voice themselves. The scoreboard does NOT need recalibration; the
finding's own 15-minute move is executed and passes. Also: zknot's meter
inherits the session filter at zknot.py:119, which is why it is clean; the
meter's cleanliness is itself evidence for Finding 2's session-join cure.

### FINDING 5 (curator-rung placement + classifier probe): CONFIRMED as cited, probe spec amended

Cites verified: state/CURRENT.md:39-44 holds exactly the ten named decisions
(GSTD wallets, bridge-vote GO, ESTATE_INDEX --apply, fleet retirement,
drift-board re-seal, stash policy, cage restart, census refresh, epoch
stamp, tip-witness PAT); zknot.py:16-18 deterministic no-LLM discipline as
quoted. One amendment from my census: the probe's dispatch.jsonl training
class is nearly empty at the top level (13 dispatch-shaped survivors in
30d), so "one trained on human.jsonl, one on dispatch.jsonl" as specified
would race against a 13-row class. The dispatch voice in volume lives in
the child-session bucket (6,909 raw messages) and the cooperative register
lives in the salon vault (19 + 22 files, counts matching economics.md
section 1 exactly). The classifier race should be re-specified as
human.jsonl vs child-session-dispatch.jsonl (rich) and/or salon-register
(the cooperative baseline moonshot-2.md also proposes). The hardware bound
holds: RIB_GPU_LADDER_20261001.md:5-6 names the estate box AMD RX 5600 XT
(RDNA1, gfx1010, no FP8 path, quant lane only), so scikit or gemma:2b-class
few-shot is the only weights-class shape that fits the local box; the 6GB
figure itself appears nowhere in estate bytes (the card name is the anchor;
the VRAM number stays ask-given, OWED).

## ADDITIONS (what the lens missed)

1. The deterministic separation already exists (zknot.py:119) and doubles
   the contamination number to ~4.4x. Detailed above; this is the single
   highest-value correction: the substrate pass is a session join the estate
   already ships, not a new blocklist.
2. The curated correction store OUTSIDE the repo: LAWS_COMPILED's own
   Sources section names "104 memory files typed feedback (operator
   corrections)" in ZMEM
   (C:/Users/foste/.zcode/cli/memories/projects/local_sovereign_agent-16821bdbdc2a3cf7/memory/).
   My census: the dir exists, 866 files today, 46 carry a feedback marker in
   their first 300 bytes, the feedback/ subdir holds 1 file. The 104 figure
   is stale or counts a deeper type field, but dozens of curated correction
   files ARE there. Finding 3's move has a head start the lens did not know:
   sample 5 of them (15 minutes) before mining the raw tape.
3. The estate's only in-code operator simulation is a rubber stamp:
   mag/harness.py:479-495, test_scenario_3, "# Simulate operator confirm"
   then status AUTHORIZED hardcoded. Byte-verified this sitting (found via
   moonshot-2.md's instrument log, confirmed in the source). This is the
   code-side exhibit for the thesis premise "the estate grades against
   cooperators only", stronger than any prose promise, and the communication
   lens never opened harness.py.
4. moonshot-2.md contradicts this lens on the pairs asset and the
   contradiction resolves in communication's favor: moonshot-2 FINDING 1(c)
   counts "the correction rubric with contrast pairs" as an estate
   ingredient; my tree-wide census shows the pairs are promised (SKILL.md,
   DAY1_SKILLS_DOGFOOD.md:167, RTFM_20260904.md:234) but never banked as
   rows. The synthesis must not inherit moonshot-2's (c).
5. moonshot-2 verified MIMESIS live (WebFetch on arxiv.org/abs/2610.09484:
   9B, 13 behavioral patterns, SOUL-Index 65.7, beats GPT-5.5-user-trained
   agents on nine unseen simulators), which the communication lens left
   untouched; its meter-as-scoreboard convergence with Finding 4 is a THIRD
   derivation (moonshot-2 FINDING 1d) and deserves the CONVERGENT flag.
6. Blind-spot resolutions for the record: BS1 resolved numerically (3,186
   human-tape ceiling; separated-tape shape census flips the register story:
   lowercase 1,755 dominates the true tape, capitalized 845, the machine
   briefs were overwhelmingly child-session); BS2 resolved (tree-wide
   census); BS3 resolved (salon vault = frontier verdict tables, cooperative
   register, not operator dyads; sample
   watch/salon_responses/astra_smoke_12/astra_smoke_12__cerebras-oss.md);
   BS5 anchored (RX 5600 XT named in the GPU-ladder rib); BS6 resolved
   (moonshot-2 read in full this pass). BS4 (read-receipts) stands
   unresolvable in bytes, unchanged.

## Honest residue

- The DB counts are moments, not constants (B2-216 law): lens ran earlier on
  10-10, I ran 06:03-06:06Z; deltas of tens of rows are window drift, and I
  say so wherever I compare.
- The 448-vs-470 meter reconciliation is approximate (different window ends
  and qualifier timing); a zknot --dry-run at the same instant would close it
  exactly; not run (mutates nothing but costs a sitting minute I did not
  spend).
- I did not content-validate the 46 feedback-marked ZMEM files (the 15-minute
  move names exactly that check).
- Whether child-session real_user messages ever contain genuinely
  operator-typed text (harness semantics quirk) is unexamined; if they do,
  the 3,186 ceiling undercounts. The zknot cards' child-session exclusion
  (zknot.py:51-52 per AGENTS.md) suggests the estate already treats them as
  invisible-by-design.
- No pytest/ratchet run by me; this file rides the pre-push gates at commit.
