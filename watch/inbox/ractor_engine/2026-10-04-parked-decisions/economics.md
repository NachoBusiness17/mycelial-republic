# economics.md - the EV-per-cost lens on the two parked decisions

Lens: economics (EV per minute, EV per token; kill cluster-class asks dressed
as one-sittings; price the free lane honestly; never hoard or burn without a
banked usage line). Every number below was read or run THIS sitting, cited
path:line or command:output. No em-dashes. Anything not verified is OWED.

## D3 VERDICT: explicit-off on the wire for depth=mechanical, carried by the carrier. Omission is never a posture.

One line: **the default thinking posture for arm-2/short-output asks is
explicit `thinking:{type:disabled}` sent unconditionally on every
depth=mechanical ask, by every carrier (route_chat, ds_workhorse,
hermes_burn); depth=design stays the only ON path; lane-config-gating is
demoted from law to capability-cache.**

The economics, measured this sitting:

1. The founding row IS the dollar leak, and it is a DOUBLE burn.
   memory/runs/hermes_burn/usage.jsonl:1151 = GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003,
   z-ai/glm-5.3-prime, 16000 completion tokens AT CAP, 15998 reasoning tokens,
   finish_reason "length", content_chars 1, cost_usd 0.2502604, banked ok:true.
   usage.jsonl:1152 (the next line) = the STAGE_B re-fire of the same
   judgment, $0.2137336. One judgment cost $0.4639940 because thinking-ON at
   cap produced a hollow answer that the meter called success. The re-fire
   was not an anomaly; it was the tax on the hollow.
2. The off switch is measured and nearly free. watch/inbox/go_wave_20261004/
   d4_thinking_probe.md table (3 arms, $0.00007 total): omitted key = 18
   reasoning tokens on a one-word ask; disabled = 2 completion tokens, no
   reasoning block in usage; enabled = 12 reasoning tokens (the sanity arm
   proving the param drives the state both ways). DeepSeek v4 thinks BY
   DEFAULT; omission resolves to ON.
3. Lane-config-gating (the current STANDING_RAILS Law 1 posture: "per-lane
   call laws", queue/STANDING_RAILS.md:11-12) measurably fails at 2 of the 3
   carriers that actually carry judgment traffic:
   - configs/providers.yaml carries disable_thinking on exactly 3 providers
     (lines 223 openrouter, 371 deepseek, 401 deepseek_overmind; census by
     venv python yaml walk this sitting). The lane that burned $0.46
     (hermes, glm-5.3-prime, providers.yaml ~154-168) has NO flag; its own
     comment knows the mechanism ("Reasoning models burn thinking out of
     max_tokens: size calls up or content dies") and chose budget-sizing,
     which pays for reasoning you never wanted.
   - tools/hermes_burn.py:112-117: the wire body is exactly {model,
     messages, max_tokens}. No thinking key exists in the carrier that
     produced the $0.46 burn. route_chat's depth law does not govern it
     (it is a registered self-call debt, queue/STANDING_RAILS.md:46-48).
   - tools/ds_workhorse.py rode ON-by-omission for every batch through the
     fix (now explicit at ds_workhorse.py:93 with the dated comment citing
     the d4 probe). The d4 probe consequence 1 names the v3 re-fire itself
     as ON-by-omission.
4. On MECHANICAL shapes the estate has zero banked quality evidence for
   thinking-ON anywhere: every quality datapoint cited for ON (arm-1 4/4,
   the "2-3x" claim) is design-shape, and a06-sacred-cow row 2 already
   showed the 2-3x is a budget-confounded length ratio (16000-token arm vs
   a 6000-char-cap baseline, memory/runs/mickey17_v2/runs/run-0/lanes/
   a06-sacred-cow.json line 20). What ON has on mechanical is a failure
   class: arm 2 banked 2/10 zero-content at the 16000 cap plus 4/10
   cap-pinned (same file, line 9-20 census), and the $0.46 double burn.

Falsifier (what would flip this verdict): a funded lane that REJECTS the
top-level thinking key with a 400, making explicit-off break more asks than
the hollow class costs (measured hollow cost so far: $0.464 + 6/10 degraded
arm-2 asks; measured off cost: 2 vs 21 tokens on one ask). The probe is
~$0.001 across the funded lanes and is the FIRST LEG of the move. Second
falsifier: a judged equal-budget A/B on a mechanical shape where ON beats
OFF on the register's own rubric (not length). If either lands, the off
default moves to a written per-lane capability field whose written default
is still disable.

Amendment text for the losing law surface (STANDING_RAILS.md Law 1; the
"per-lane call laws" clause loses to the depth-layer clause):

> 1. Default to the rails. A bespoke model-call path requires a written
> reason in its docstring. The front door is `mag.route_chat` (lane + goal;
> dormant gate; endpoint fence; depth-gated thinking: depth=mechanical sends
> thinking:{type:disabled} on the wire for every lane - omission is not the
> off state (d4 probe 2026-10-04,
> watch/inbox/go_wave_20261004/d4_thinking_probe.md); depth=design is the
> only enabled path and budgets 32K+; usage banked).

Plus one registered-debt line under REGISTERED DEBTS:

> - hermes_burn._call carries no thinking key: every glm/qwen prime ask
> rides vendor-default ON (measured: usage.jsonl:1151 $0.25 hollow at cap
> + :1152 $0.21 re-fire). Wire thinking:{type:disabled} behind a lane
> capability probe; one sitting.

For the a06-sacred-cow surface (append-never-rewrite: this file is the
erratum carrier, the row is cited not edited): the a06 verdict's "wire the
flag to lane policy" clause is the losing half. The d4 probe + the hermes
burn show lane-policy gating fails exactly where the flag is absent, which
is where the money burned. The gate moves to the depth layer; the lane flag
becomes a capability cache written from a measured 200, not the gate.

One-sitting move (~60 min): (a) probe the funded lanes with the disabled
key (~$0.001, 3 calls); (b) flip mag/route_chat.py:204 condition from
`lane_cfg.get("disable_thinking") and depth == "mechanical"` to
`depth == "mechanical"` with the probe results as the comment's evidence;
(c) add the same key in tools/hermes_burn.py:112 body behind the probe
result; (d) land the STANDING_RAILS amendment above; (e) extend
tests/test_route_chat_depth.py (exists, 4 passed in 0.61s this sitting)
with the unconditional-mechanical assertion.

## The mislabeled variable in a banked receipt (D3 evidence hygiene)

CONVERGENT with d4_thinking_probe.md consequence 1: watch/inbox/
go_wave_20261004/ds_workhorse.md item 6 headline reads "ds arm re-fired,
uncapped, thinking-off, file-backed" and scores 3/28 vs the capped 0/26.
The d4 probe names that exact batch as ON-by-omission (carrier: `python -m
tools.ds_workhorse run`, ds_workhorse.md:62-66; the ask() body fix landed
after, ds_workhorse.py:93). So 0/26 to 3/28 measures CAP REMOVAL with
thinking constant ON; it is NOT evidence for thinking-off quality. The
estate has NO judged quality measurement of thinking-OFF on any real ask;
the D3 posture rests on cost asymmetry plus the ON failure class, which is
sufficient for mechanical but must not be written as if a quality A/B
existed. STANDING_RAILS.md:49-53 cites this receipt (its "uncapped" wording
is fine; ds_workhorse.md's "thinking-off" is the false half). Falsifier: a
pre-refire commit showing the explicit thinking key on the v3 wire, or a
ds_workhorse.md erratum already landing (I found none in the file this
sitting). Move: one erratum line in ds_workhorse.md item 6 (~10 min),
landed with the D3 move above.

## D2 VERDICT: ACCEPT THE DEBT STANDING. Do not split dungeon.py this sitting.

One line: **keep the 756-line ratchet debt on tools/dungeon.py; spend the
sitting on the D3 wire fix (measured $0.46 leak) instead; fold two free
riders into the next dungeon touch: delete the dead shadowed play() at
dungeon.py:447 and stamp the campaign-seam split candidate into the
baseline note.**

The economics, measured this sitting:

1. The debt is already GOVERNED, not loose. B2-273 (tools/violation_ratchet.py
   :73-80) stamps accepted_lines into the claim and prints a GROWTH line on
   drift. The acceptance row carries "accepted_lines": 756
   (configs/violation_baseline.json, key af1d7045681fee89). My full-scope
   run `./.venv/Scripts/python.exe tools/violation_ratchet.py check`
   (scope=1404 files) printed:
   `GROWTH claim af1d7045681fee89: tools/dungeon.py accepted at 756 lines,
   now 771 (+15) - re-audit or re-accept by name`
   and RATCHET: PASS. The +15 (commit 72f1c58c7, the 3-strike void breaker,
   landed hours after acceptance) was caught by the meter exactly as
   designed. Accepted debt is a visible ledger fact, not a license.
2. The GROWTH ledger is a COHORT, and dungeon.py is its second-smallest
   member. The same run printed 8 grown files: mag/percolator.py 580 to
   1022 (+442), tools/env_contract.py +180, tools/concept_predictor.py
   +154, tools/duel_harness.py +120, tools/gps_mcp/ledger.py +112,
   mag/estate_bridge.py +102, tools/dungeon.py +15, tools/hermes_burn.py
   +6. Splitting the +15 member while percolator grows +442 un-split is
   misallocated attention. The cluster-class ask here is the cohort, not
   one file; if a split sitting is ever bought, it should price percolator
   first (no hourly-cron blast radius there).
3. The dangerous half is already seam-cut. The parser whose collapse voided
   a live campaign verdict is extracted into Dungeon._grade() and the
   replay net is green on MY runs this sitting:
   `pytest tests/test_dungeon_parser.py` = 13 passed in 1.23s (the 13
   functions replay the 14 logged S4 verdicts as in-file fixtures,
   tests/test_dungeon_parser.py:9-17); with tests/test_burn_id_uniqueness.py
   = 15 passed in 0.65s (the ask's "15 in under a second", reproduced).
   The engine split therefore protects code that has already stopped
   producing the bug class it was split to contain.
4. The split does not clear the rule in one seam. The campaign block
   (SCENES tables + campaign() + 6 helpers, roughly lines 453-731) is ~278
   lines; 771 minus 278 is ~493, still over the 400 rule. Clearing
   file-too-long needs the top tables too (ROSTER/DM_MODEL/WARDEN/
   INITIATIVE/SCENES, lines ~44-61 and ~453+): two seams, a bigger
   import/blast radius (hourly cron subprocess per STANDING_RAILS.md:32;
   importers census this sitting: tests/test_burn_id_uniqueness.py,
   tests/test_dungeon_parser.py, subprocess callers; zero mag/ or main.py
   importers, full-tree grep hit only attic/ and corpus/ archives), for
   zero measured dollar return against a $0.46 alternative spend.
5. Free rider found: tools/dungeon.py:447-449 `def play` is DEAD CODE,
   shadowed by the second `def play` at :727 in the same class body
   (Python keeps the last class-body binding; exactly one class exists,
   line 148). The go wave added the campaign play beside the old one
   instead of replacing it. ~5 minutes to delete inside the next dungeon
   edit; not worth its own sitting.

Flip conditions (falsifiers for the keep-verdict): (a) a second
collapse-class bug in dungeon.py within 2 waves (the parser collapse
already happened once; a repeat means the single-file shape breeds bugs
faster than the net catches); (b) the next substantive campaign edit
landing (the +129 go-wave edit pattern repeating) - split-while-touching
beats split-for-its-own-sake; (c) dungeon.py crossing ~+100 over accepted
(871+) or becoming the cohort's top grower. Any one of the three converts
this verdict to SPLIT in the following sitting.

## What I could not verify (OWED, not asserted)

- No live probe was fired this sitting: the 400-on-disabled-key wire risk
  is unmeasured outside deepseek; GLM prime's own thinking wire shape
  (does top-level thinking:{type:disabled} even parse on the z.ai/Nous
  gateway?) is unverified. The D3 move's first leg is that probe.
- I read the a06-sacred-cow.json rows and verdict byte-level via grep and
  venv json load, but did not open memory/runs/ds_batches/
  sacred_cow_thinking_on.jsonl myself; arm-2 counts (2/10 zero-content,
  4/10 cap-pinned) rest on a06's byte-quoted census plus the ask's framing,
  not my own count of the manifest.
- Post-gate hermes_burn rows (are hollow rows since the substance gate
  stamped ok:false?) were not censused; the $0.464 is pre-gate history.
- The "~10-15x cheaper" providers.yaml claim direction is confirmed by the
  probe (21 vs 2 tokens) but the magnitude was not re-measured (the d4
  receipt itself marks this out of scope).

## Receipts of record this sitting

- Read: d4_thinking_probe.md; a06-sacred-cow.json; STANDING_RAILS.md (full,
  53 lines); usage.jsonl:1149-1153; mag/route_chat.py:119-242;
  tools/ds_workhorse.py:76-101; tools/hermes_burn.py:106-125, 338-350;
  tools/dungeon.py (structure + lines 40-62, 440-460, 700-733);
  test_dungeon_parser.py header + fixtures; violation_ratchet.py:50-84;
  violation_baseline.json af1d7045681fee89; ds_workhorse.md items 1-6;
  providers.yaml (disable_thinking census + hermes lane block);
  state/CURRENT.md header.
- Ran: pytest tests/test_dungeon_parser.py (13 passed, 1.23s); pytest
  tests/test_dungeon_parser.py tests/test_burn_id_uniqueness.py (15 passed,
  0.65s); pytest tests/test_route_chat_depth.py (4 passed, 0.61s);
  violation_ratchet.py check --changed (PASS, scope=3) and check
  (PASS, scope=1404, 8 GROWTH lines); wc -l on dungeon.py (771),
  route_chat.py (273); disable_thinking lane census via venv python yaml.
