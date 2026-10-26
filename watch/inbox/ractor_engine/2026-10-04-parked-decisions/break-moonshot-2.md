# break-moonshot-2 - the hostile second pass over lens moonshot-2 (2026-10-04)

Pass rule: every evidence cite in moonshot-2.md was re-checked against estate
bytes this sitting, with the exact command next to each result. I ran no paid
API call and no dungeon runtime smoke (both stay OWED, matching the lens's own
blind spots). No em-dashes. Instruments: Read, grep, stat, wc, venv python
censuses, pytest, tools/violation_ratchet.py check (full tree).

## Re-run census (what I executed this sitting)

1. `.venv/Scripts/python.exe -m pytest tests/test_dungeon_parser.py
   tests/test_burn_id_uniqueness.py -q` -> **15 passed in 1.09s** (lens read
   0.95s; pass count reproduces, the sub-second claim did not on my run).
2. `.venv/Scripts/python.exe -m pytest tests/test_route_chat.py
   tests/test_route_chat_banks.py tests/test_route_chat_depth.py
   tests/test_route_chat_fence.py -q` -> **15 passed in 3.66s** (lens 2.20s).
3. `.venv/Scripts/python.exe tools/violation_ratchet.py check` -> scope=1405
   files; hits=943; registered=942; NEW=1
   (`NEW e71ef4422e755b5e file-too-long: tools/social_rsi.py:578`), 8 GROWTH
   lines incl. `tools/dungeon.py accepted at 756 lines, now 771 (+15)` and
   `tools/hermes_burn.py accepted at 428 lines, now 434 (+6)` -> RATCHET: FAIL.
   Identical to the lens's instrument-4 output.
4. venv census of memory/runs/route_chat/usage.jsonl -> **15 rows** (lens: 11),
   0 with reasoning_tokens, 0 with depth; union keys = ts, lane, model, goal,
   key_env, prompt_tokens, completion_tokens, content_chars, finish_reason,
   ok, detail, error. The 4 new rows landed 11:10:12Z-11:31:45Z today (saelis
   RuntimeError x4, nous ok x2), i.e. after the lens's census moment. The
   invariant the finding needs (neither key banked) holds on all 15.
5. Byte read of memory/runs/hermes_burn/usage.jsonl:1151-1152 -> :1151
   content_chars 1, completion_tokens 16000, reasoning_tokens 15998, finish
   "length", cost_usd 0.2502604, ok true; :1152 STAGE_B cost_usd 0.2137336,
   finish stop. Exact match to the lens.
6. stat ordering -> frontier_delta_results_v3.jsonl 04:38:32 <
   d4_probe.py 06:00:41 < ds_workhorse.py 06:11:38 (all LOCAL -0400; the lens
   printed local times with Z suffixes). Ordering claim exact; units sloppy.
7. Sacred-cow manifest recount (cures the lens's blind spot 2):
   memory/runs/ds_batches/sacred_cow_thinking_on.jsonl = **14 rows, cow- 4 +
   cow2- 10**, exactly 2 ok:false, both content_chars 0 (completion 16000 and
   16002). The a06 row's numbers reproduce from the manifest itself.
8. Posture-field census (quantifier-law scope for "never banked a
   thinking-OFF batch score"): all 16 files in memory/runs/ds_batches/*.jsonl
   (234 rows) carry ZERO rows with any thinking or depth key; route_chat
   ledger ditto (15 rows). No banked row anywhere names a thinking posture.
9. Importer census (grep "tools.dungeon|tools import dungeon" over *.py,
   excluding .git/.venv/archives): live importers of tools.dungeon are
   exactly tests/test_burn_id_uniqueness.py:19 and
   tests/test_dungeon_parser.py:26. tools/prepush_golden_vector.py:43
   DEFAULT_TARGET = "tools/dungeon.py" (not an importer). Matches the lens.
10. Line cites read byte-wise: tools/dungeon.py:211, :297, :447-449, :623,
    :727-731, :565, :689; mag/route_chat.py:121-141, :204-213, :231-249;
    configs/providers.yaml:150-168, :219-223; tools/hermes_burn.py:71-78,
    :106-116; tests/test_route_chat_depth.py:83-89;
    configs/violation_baseline.json key af1d7045681fee89;
    githooks/pre-push:412-445; d4_thinking_probe.md:53-62, :78-81;
    ds_workhorse.md item 6; tools/ds_workhorse.py:76-94;
    a06-sacred-cow.json rows (keys e6baa31db6c0, ee225394e567, acdf3f8157fd);
    queue/STANDING_RAILS.md (all 53 lines).

## Verdicts

**F1 (D3 verdict: explicit-off, carrier-enforced, closed-loop) - CONFIRMED.**
Every cite byte-true: providers.yaml:219-223 carries the 2026-08-24
openrouter/auto ignore probe ("600 -> empty, 2000 -> content",
disable_thinking: true at :223); mag/route_chat.py:242-249 banks neither
reasoning_tokens nor depth (my census, 15/15 rows); the depth enum and wire
form are at route_chat.py:137-141 and :204-213. Two precision hits, neither
fatal: (a) the "depth=design ... at >=32000 max_tokens" clause is NOT current
code, grep finds 32K only in the docstring at route_chat.py:135, :212-213
enables thinking on design with no budget floor, so the 32K gate is part of
the amendment to land, not a restatement; (b) the ledger count is now 15, not
11 (drift, invariant holds). The openrouter-ignore leg rests on a 2026-08-24
banked comment, unprobed since (lens admits; stays OWED).

**F2 (the $0.46 double burn on the unswitched nous carrier) - CONFIRMED.**
usage.jsonl:1151/1152 byte-exact ($0.2502604 + $0.2137336 = $0.4639940,
matching economics.md:23); the nous block providers.yaml:150-168 carries no
disable_thinking key (full read; note :157 already documents the failure mode
"Reasoning models burn thinking out of max_tokens"); tools/hermes_burn.py:112-116
sends exactly {model, messages, max_tokens} (the lens wrote 112-117, one line
of overhang into `last = None`). Falsifier holds: no off switch exists on
that lane.

**F3 (the ds refire rode thinking-ON; 3/28 vs 0/26 measures the cap) -
CONFIRMED.** mtime ordering reproduces exactly (04:38:32 < 06:00:41 <
06:11:38); ds_workhorse.md:62-69 names `-m tools.ds_workhorse run` as the
refire carrier, so ask() rode omission; tools/ds_workhorse.py:86-93 now
sends the explicit disabled key with the dated erratum comment. The CONVERGENT
flag is genuine: communication.md:9-17 and :29 derive the identical
correction (including the same erratum text), economics.md:51/:117 and
dogfood.md:50-54 carry the posture and PRIORS legs. Two scope notes the
verdict should carry: (a) the refire rows bank model deepseek-chat (14/14,
my census) while the d4 probe measured deepseek-v4-flash, so "rode
thinking-ON" rides the v4-family default bridge (ds_workhorse.py:64 "v4.1-flash
mapping per provider docs"), not a deepseek-chat-specific probe; (b) "the
estate has never banked a thinking-OFF batch score" is an absence claim and
now has its instrument: 234 rows across 16 ds_batches files + 15 route_chat
rows, zero posture fields anywhere (my census #8). The ~$0.13 disambiguating
refire remains unspent (OWED, all passes).

**F4 (D2 verdict: split now, one seam, bury the dead generation) -
CONFIRMED.** All four artifact cites byte-true: :447-449 play() (s0+s1) is
shadowed by :727-731 play() (s0+s1+campaign); :623 `... or True:`; :211
`msg.get("content") or msg.get("reasoning") or ""` against the vendor field
reasoning_content documented at mag/route_chat.py:231-235 (dungeon imports
_call and PRICING from tools.hermes_burn at dungeon.py:38, so the openai_compat
carrier story applies; the dead fallback has no dungeon-side byte proving it
fired or never fired, that scoping stands); :297 getattr re-default is dead
because __init__ sets ledger_audits = 0 at :156 (note: :297 increments with a
dead defensive default, "re-initializes" is loose wording, the lens calls it
minor and symptomatic, fair). Ratchet GROWTH line reproduces live (756 -> 771,
af1d7045681fee89, accepted 2026-10-04 by go-wave-20261004-coordinator,
configs/violation_baseline.json). 15/15 tests green on my run (1.09s). One
mechanism error in the lens's framing: the golden-vector scanner does not
"break silently" on a shrink-split. githooks/pre-push:427-440 wires it
WARN-ONLY: a token leaving tools/dungeon.py prints a named lost-tokens WARN
and the push proceeds; total silence only occurs if tools/dungeon.py ceases
to exist (the `if [ -f "$GGV_TARGET" ]` guard at githooks/pre-push:432 skips
with no output). See addition A1 for the two-copy re-point requirement.

**F5 (live ratchet FAIL, NEW=1 tools/social_rsi.py:578) - CONFIRMED.** My
full-tree run reproduces it identically this sitting (scope 1405, NEW=1,
RATCHET: FAIL). Live gate state, not stale bytes.

Blind-spot audit: all six stand as honest. Two are now cured or advanced by
this pass: blind spot 2 (manifest recount done, 14/4+10/2-ok:false, census #7)
and blind spot 3 is partially covered on file: a06-sacred-cow.json row
acdf3f8157fd records a live re-verification that the vendor guide's code
samples carry the thinking object exactly as route_chat sends it (48,088-byte
curl), which pins the wire SHAPE but is still not a z.ai/glm acceptance probe;
grep found no glm+thinking-key evidence in memory/runs/hermes_burn/usage.jsonl,
so that probe remains OWED. No live API probe was paid by this pass either.

## Additions (what the lens missed)

**A1. The golden-vector tripwire is double-anchored and WARN-ONLY.** The lens
named only tools/prepush_golden_vector.py:43. The pre-push hook carries its
own copy, GGV_TARGET=tools/dungeon.py at githooks/pre-push:429, inside a
WARN-ONLY block (:427 "this block NEVER exits nonzero"). A split must re-point
BOTH the tool constant and the hook variable, else every post-split push emits
a lost-tokens WARN (loud, non-blocking); silence happens only in the
file-vanishes case (:432 guard skips with no output). Falsifier: a split
sitting that re-points both and prints GOLDEN-VECTOR: ok on the new layout.
Move: +5 min inside the already-planned ~90 min split sitting.

**A2. The refire model is deepseek-chat, the probe's was deepseek-v4-flash.**
memory/runs/ds_batches/frontier_delta_results_v3.jsonl banks 14/14 rows model
deepseek-chat; d4_thinking_probe.md:21-22 names deepseek-v4-flash. "The arm
rode thinking-ON" rides the v4-family default bridge, not a direct probe of
the refire's model. Falsifier: a 2-arm omission probe on deepseek-chat
(~$0.00005) showing no reasoning_content. Move: fold the model name into the
ds_workhorse.md item 6 erratum text (~2 min), and the probe is optional.

**A3. The route_chat ledger moved under the lens: 11 -> 15 rows.** Four rows
landed 11:10:12Z-11:31:45Z today after the lens's census. The banked-neither
invariant holds on all 15 (my census #4), so F1 survives, but any D3
closed-loop move must re-census at landing on this moving tree. Move: none
beyond the planned _bank edit; name the moment in the landing receipt.

**A4. The 32K design floor is not in code.** grep of mag/route_chat.py finds
32K only in the docstring (:135); :212-213 enables thinking on depth=design
with no max_tokens check. The D3 verdict's "requires max_tokens >= 32000" is
new behavior the amendment must add (one guard clause), not existing law.
Falsifier: the grep above. Move: include the floor guard in the ~75-min move
(+5 min) or strike the clause from the amendment text.

**A5. tools/hermes_burn.py is already past its own ratchet acceptance.**
GROWTH line in my run: accepted 428, now 434 (+6). F2's carrier edit lands in
a file already over its accepted count, so the edit should ride the same
sitting as a named re-accept (or the split that cures it), or pre-push shows
two GROWTH rows for one move. Move: 0 extra minutes, note only.

**A6. STANDING_RAILS.md carries no depth law at all, confirmed.** The brief's
"route_chat depth law in queue/STANDING_RAILS.md" does not exist (grep
depth|thinking over all 53 lines = 0 hits; route_chat appears only at :11,
:26, :46-48 as the migration debt and at :49-53 as the ds tally). The lens
already caught this (its amendment 2) and my read confirms it; the real
two-surface disagreement is PRIORS.md:25 row 8 ("never refire thinking-on")
vs route_chat's design door, both cited by the lens.

## Bottom line

Five findings, five CONFIRMED, zero killed, zero weakened below the
confirm bar; three carry precision riders (F1's 32K clause is proposed law,
F3's model bridge, F4's WARN-not-silent gate mechanics). The lens's D3
verdict (explicit-off, carrier-enforced, closed-loop, ledger-verified) and
D2 verdict (split now, one rules seam, bury the dead generation, re-point
both golden-vector anchors) both survive hostile byte-check and stand as the
ractor verdicts, with amendments A1-A4 folded into their move lists.
