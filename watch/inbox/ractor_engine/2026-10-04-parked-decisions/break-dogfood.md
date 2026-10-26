# break-dogfood - hostile second pass on the dogfood lens report (2026-10-04)

Pass: every evidence cite in the lens report byte-checked against the estate this
sitting. Instruments run here: full Read of tools/dungeon.py (771 lines), Read of
mag/inference_budget.py, tools/ds_workhorse.py, mag/route_chat.py, queue/STANDING_RAILS.md,
watch/inbox/go_wave_20261004/{d4_thinking_probe.md, ds_workhorse.md, dungeon.md},
watch/inbox/model_garden/PRIORS.md, memory/runs/mickey17_v2/runs/run-0/lanes/a06-sacred-cow.json,
configs/violation_baseline.json (offset 5300), tools/violation_ratchet.py (offset 255),
tests/test_inference_budget.py (offset 65), memory/runs/hermes_burn/usage.jsonl (offset 1150);
grep censuses as cited inline; mtime census via
`.venv/Scripts/python.exe -c "os.path.getmtime(...)"`; ratchet via
`.venv/Scripts/python.exe tools/violation_ratchet.py check`; suites via
`.venv/Scripts/python.exe -m pytest tests/test_inference_budget.py -q` (19 passed in 0.83s)
and `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py -q -p no:cacheprovider`
(15 passed in 0.77s). No live API probe was paid this sitting (same hedge as the lens).

## Verdicts

| # | Finding | Verdict |
|---|---------|---------|
| 1 | D3 depth-gated explicit-off + stale inference_budget deepseek row | CONFIRMED (move amended) |
| 2 | ds v3 re-fire rode thinking-ON; "thinking-off" label false | CONFIRMED (CONVERGENT) |
| 3 | D2 split now, ONE verbatim pure-rules seam | WEAKENED (evidence intact, seam not executable as specified) |
| 4 | Dungeon.play defined twice, :447-449 dead | CONFIRMED |
| 5 | STANDING_RAILS zero thinking bytes; PRIORS.md:25 unamended | CONFIRMED (finding text arrived truncated) |

### Finding 1 - CONFIRMED, move amended

Bytes all check. mag/inference_budget.py:73 carries "thinking-off via omission,
AH10 byte-confirmed" verbatim; :77 is `thinking_control={}`; :78-79 put
"thinking" first in forbidden_keys. watch/inbox/go_wave_20261004/d4_thinking_probe.md:8-9
marks that exact claim WRONG. tools/ds_workhorse.py:93 sends
`"thinking": {"type": "disabled"}`. Move amendment the lens missed:
tests/test_inference_budget.py:72-82 (`test_deepseek_thinking_off_injection_strips_forbidden_params`)
ASSERTS the wrong posture - a caller-supplied thinking:{type:enabled} is stripped
and the plan ships NO thinking key, under the comment ":78 # omission IS the off
state (AH10)". The move's named check (`pytest tests/test_inference_budget.py -q`)
passes 19/19 today BECAUSE it encodes the omission law; after the row fix it goes
red unless the test is amended in the same sitting (assert
`plan.extra_body["thinking"] == {"type": "disabled"}` + dated erratum comment).
The test file is a third wrong-source organ; the lens counted two.

### Finding 2 - CONFIRMED, CONVERGENT

My mtime census reproduces all three values exactly:
memory/runs/ds_batches/frontier_delta_results_v3.jsonl 2026-10-04T08:38:32Z,
watch/inbox/go_wave_20261004/d4_probe.py 10:00:41Z, tools/ds_workhorse.py 10:11:38Z.
New corroborating byte: the receipt watch/inbox/go_wave_20261004/ds_workhorse.md
itself has mtime 08:46:59Z, i.e. written between the refire and the fix, so its
":62 **ds arm re-fired, uncapped, thinking-off, file-backed**" label (byte-verbatim
at :62, command :63-66) describes a run whose transport could not yet send the
disabled key. queue/STANDING_RAILS.md:49-53 verified clean ("re-fired uncapped",
no thinking label). Falsifier legs hold: no wire log of the v3 batch can show a
thinking object (it predates the only code that sent one), and ds_workhorse.md:63-66
names the ds_workhorse command.

### Finding 3 - WEAKENED

Evidence intact: configs/violation_baseline.json:5308-5316 is the entry
(af1d7045681fee89, accepted 2026-10-04, accepted_lines 756, by
go-wave-20261004-coordinator, file tools/dungeon.py, rule file-too-long). My
ratchet run reproduces the GROWTH line byte-identically ("tools/dungeon.py
accepted at 756 lines, now 771 (+15)"). Growth law at tools/violation_ratchet.py:264-276
confirmed. Two defects in the finding's mechanism:

1. "Verbatim move plus re-exports" is impossible for two of the named items.
   _verdict (tools/dungeon.py:243-303) reads self.tip/self.turn/self.claims/
   self.pc_hp/self.warden_hp/self.persuades/self.audits/self.ledger_audits and
   even mutates the ROSTER global (:267). _grade (:565-610) reads self.tip/
   self.turn and writes self.last_roll/self.root_anchors. Neither is pure.
   The verbatim-movable set is: strip_and_cap :103-108, TAG_RE :111, extract_tag
   :114-130, roll :133-134, check_golden :137-145, SCENES :454-486, and the
   staticmethods _beat_outcome :497-508, _find_scroll :510-522, _phantom_count
   :524-527, _packs_str :529-532 (plus near-pure _wyrm_regrowth :534-546).
2. That pure set is roughly 170 lines; 771 minus 170 leaves about 600, still far
   over the 400-line ratchet threshold, so a pure-rules split does NOT clear the
   file-too-long debt - the GROWTH line survives and the debt needs a second
   named acceptance anyway, or the split must also move the engine (campaign
   :612-725, s1 machinery), which is stateful and not a 40-minute verbatim move.
   Range imprecision: ":103-137" misses check_golden's body (:138-145); ":243"
   names only the def line of a 61-line method; ":454-611" also contains
   _enemy_sheet (:488-492) and _scene_sheet (:494-495), which the move list does
   not name.

The split-now CONCLUSION survives on the evidence (growth law fired; finding 4's
dead def and Addition 3's always-true condition are concrete review-capacity
proofs), but only with a corrected seam: rules module (pure layer above) plus an
engine module with state parameterized, or re-accept the grown debt by name.

### Finding 4 - CONFIRMED

Full read + grep of tools/dungeon.py: exactly two `def play` (447, 727), both
4-space class-body indent inside the single class Dungeon (:148); the second
(:727-731: s0, s1, `if self.full: campaign()`) is unconditional at class level,
so the first binding (:447-449: s0+s1 only) is overwritten at class creation and
is dead. main() calls d.play() at :743. Total 771 lines. Falsifier legs both
checked: no third def play exists, and no intentional re-bind is documented -
grep of watch/inbox/go_wave_20261004/dungeon.md for "def play|re-bind|rebind|shadow"
returns zero hits; grep of memory/runs/mickey17_v2/runs/run-0/lanes/a02-dungeon-campaign.json
shows no re-bind mention (its "play" hits are verdict prose and line anchors). The
nearest thing to intent is the :451-452 comment ("additive: the proven S0+S1 flow
above is untouched"), which describes campaign chaining, not a binding. Suite green
at my moment: 15 passed in 0.77s. Nit: deleting :447-449 leaves 768 lines, so the
ratchet GROWTH line persists (finding 3's problem, not this one's).

### Finding 5 - CONFIRMED (truncation noted), CONVERGENT

The report as received cuts this finding's text mid-falsifier ("it doe"); I verdict
the checkable claims. My replication of the lens's grep over queue/STANDING_RAILS.md
returns exactly :11 (front door), :26 (drop-in row), :47 (debt note), all
route_chat hits, zero "thinking"/"depth" bytes, file is 53 lines (Read ended at 53).
Law text confirmed at mag/route_chat.py:127-141 (docstring: mechanical applies
disable_thinking, design enables, enum ValueError at :137-141) and :204-213 (the
wire: disabled when lane flag + mechanical, enabled on design). PRIORS.md:25
verified unamended: status still "STILL-VALID (byte-confirmed mechanism, never
refire thinking-on)", no d4 post-datum. The truncated finding/move strings are
OWED (never received here). CONVERGENT flag: the PRIORS amendment is already a
standing steal row - a06-sacred-cow row key b91883ff6f87 (0-indexed row 2,
memory/runs/mickey17_v2/runs/run-0/lanes/a06-sacred-cow.json:26-35) prescribes
"append the 53f56d0f3 post-datum to PRIORS row 8 ... landing spot
watch/inbox/model_garden/PRIORS.md:25"; the lens independently re-derived it.

## Blind-spot spot-checks

- "Unread campaign middle (:612-733)": I read all 771 lines. Addition 3 below is
  what was sitting there.
- "d4_thinking_probe.md:85 assigns ownership": line slip - the phrase "the
  a10-ds-batches owning lane" is at :82; the inference_budget fix-owed note is
  :83-87. Substance of the ownership hedge stands.
- "GROWTH +442 could shift": my ratchet run reads mag/percolator.py 580 -> 1022
  (+442), identical at my moment.
- "3/28 tally not recounted": still not recounted by me. Partial check only:
  `wc -l memory/runs/ds_batches/delta_judge_results_v3.jsonl` = 27 rows (matches
  ds_workhorse.md:76 "27/27 conf=H"). The 3/28 arithmetic (26 published pairs + 2
  gaming pairs, 3 ds wins) is receipt arithmetic, OWED.
- Arm-1 rows (1-4) of memory/runs/ds_batches/sacred_cow_thinking_on.jsonl were not
  read this sitting (grep surfaced rows 5-14, the 10 arm-2 rows); the a06 row 0
  claim "7/14 at or over the 16000 cap" is therefore OWED by me (arm 2 alone holds
  5: completion_tokens 16000/16000/16000/16002/16000 at manifest rows 7,9,12,13,14).

## Additions (what the lens missed)

1. tests/test_inference_budget.py:72-82 encodes the omission law and passes green
   on it (19 passed in 0.83s this sitting), so finding 1's move fails its own named
   instrument unless the test is amended in the same sitting. Falsifier: a byte-read
   of :78-81 after the fix showing the stripped-key assertion unchanged and the
   suite red. Move: amend the assertion to require thinking:{type:disabled} in
   extra_body plus the dated erratum comment; 10 min inside finding 1's 20.
2. The ask's founding-row cite is MISATTRIBUTED. memory/runs/hermes_burn/usage.jsonl:1151
   is `GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003`, model z-ai/glm-5.3-prime,
   channel "reasoning-dump", content_chars 1, completion 16000, reasoning_tokens
   15998, finish length - a glm judgment ask, not an arm-2 deepseek route_chat ask.
   `grep -c "cow2" memory/runs/hermes_burn/usage.jsonl` = 0: no arm-2 row exists in
   that ledger at all. The true arm-2 founding bytes are
   memory/runs/ds_batches/sacred_cow_thinking_on.jsonl:7 (cow2-SUBSTANCE_48h_synthesis:
   content_chars 0, reasoning_chars 59103, completion_tokens 16000, ok false) and
   :13 (cow2-KABUKI_FACES_fold: 0, 58881, 16002, ok false). The phenotype matches
   (reasoning eats the cap) so D3's substance is untouched, but the SYNTHESIS must
   correct the cite before it propagates. Falsifier: any cow2 row in
   hermes_burn/usage.jsonl (none exists today). Move: correct the founding-row cite
   in the SYNTHESIS to sacred_cow_thinking_on.jsonl:7,:13; 5 min.
3. tools/dungeon.py:623: `if self.warden_hp <= 0 or self.persuades >= 2 or True:`
   - an always-true condition in campaign() (inside the lens's admitted-unread
   middle). It grants the S1 Ledger Page loot on EVERY --full run, contradicting
   s1()'s CUT semantics ("scrolls stay on the floor", :434); s1()'s own gate
   condition is the warden-down/persuaded/audited triple at :425. Second concrete
   review-capacity proof for the D2 split, and a real defect to fix in the split
   sitting. Falsifier: a byte-read of :623 without `or True`, or a replay where a
   CUT S1 leaves packs empty (today it cannot). Move: restore the :425 triple as
   the condition, add one parser-suite test, rerun the 15; 15 min.
4. The D3 verdict's ">=32000 max_tokens gated on a lane capability field" for
   design depth is implemented NOWHERE today: mag/route_chat.py:135 only advises
   "design asks need 32K+ or a smaller ask" in prose; no code gate exists, and
   tests/test_route_chat_depth.py (:61-89, 4 tests: enum reject, mechanical
   disabled, design enabled, flagless lane omits) pins no min-token gate. The
   amendment therefore CREATES a new law rather than relocating one; its cost is
   higher than the lens implies, and the test file is the ready extension surface.
   Falsifier: a code grep of mag/route_chat.py showing a 32000 design gate (absent
   today). Move: fold the gate + one depth test into the D3 amendment sitting;
   20 min extra.
5. The lens's quoted "RATCHET: PASS" is not reproducible at this moment: my
   `.venv/Scripts/python.exe tools/violation_ratchet.py check` exits FAIL
   (NEW=1: e71ef4422e755b5e file-too-long tools/social_rsi.py:578, the SOCIAL RSI
   wave's file) while the dungeon GROWTH line reproduces byte-identically. Anyone
   re-running the lens's command today sees FAIL and must not read that as the
   dungeon claim being wrong; the PASS was moment-true or scope-true at the lens's
   census, unverifiable now. Falsifier: a later clean check printing no NEW line
   for tools/social_rsi.py (after that debt is accepted or split). Move: name the
   social_rsi.py NEW debt in the SYNTHESIS as a live third ratchet fact; 2 min.

## OWED (not verified this sitting, never asserted)

- The 3/28 judge tally arithmetic (only the 27-row count was checked).
- Arm-1 rows 1-4 of sacred_cow_thinking_on.jsonl (the 7/14 cap-pinned claim).
- A live d4-shaped probe (the lens's own named falsifier instrument; unpaid here,
  verdict rests on the banked d4_thinking_probe.md receipt plus the byte reads).
- Finding 5's full finding/move strings (truncated in the report as received).
- Claim-holder sign-off for the two law-surface amendments (STANDING_RAILS.md is
  sibling-claimed this wave; the d4 receipt's ownership note sits at :82).
