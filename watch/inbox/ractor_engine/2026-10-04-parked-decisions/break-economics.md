# break-economics.md - hostile second pass on the economics lens

Pass: byte-checked every cite in watch/inbox/ractor_engine/2026-10-04-parked-decisions/
economics.md against the estate, re-ran the named checks at the scale named,
and fired the one measurement the lens left OWED. Every number below was read
or run THIS sitting (2026-10-04, break pass, dwfrun-837aac0c actor), cited
path:line or command:output. No em-dashes. Anything not verified is OWED.

## Verdict summary

- finding 1 (D3 explicit-off verdict): CONFIRMED. All 9 primary cites
  byte-exact. Falsifier leg 1 (400 on the thinking key) tested by me and
  dead on the Nous GLM lane. One numeric erratum found (4/10 vs 3/10, below).
- finding 2 (mislabeled thinking-off in ds_workhorse.md item 6): CONFIRMED.
  Falsifier byte-tested through git history, not just the d4 receipt.
  CONVERGENT: I re-derived it independently from version control.
- finding 3 (D2 accept-the-debt-standing): CONFIRMED. All cohort numbers
  reproduce byte-exact; two census additions found (a 4th live consumer the
  lens missed; percolator is active burn, not churn).

## Finding 1: D3 explicit-off verdict - CONFIRMED

Byte-checked, all exact:
- memory/runs/hermes_burn/usage.jsonl:1151 = GALA_DD_SELFSTEAL_PRIME_JUDGMENT_20261003,
  z-ai/glm-5.3-prime, completion_tokens 16000, reasoning_tokens 15998,
  finish_reason "length", content_chars 1, cost_usd 0.2502604, ok true.
- usage.jsonl:1152 = STAGE_B, cost_usd 0.2137336. Pair = $0.4639940. Detail
  the lens missed: STAGE_B itself carried 9826 reasoning tokens with finish
  "stop", so the $0.46 pair paid 25824 reasoning tokens total. The
  double-burn framing is stronger than the lens wrote it.
- watch/inbox/go_wave_20261004/d4_thinking_probe.md:53-62: arms 18 / 2-no-block
  / 12 sanity, $0.00007 (lines 26-28). Exact.
- mag/route_chat.py:204: `if lane_cfg.get("disable_thinking") and depth ==
  "mechanical":` with the a06/a08 comment at 205-211. Exact. Depth enum now
  validated (mag/route_chat.py:137-141, raises ValueError), so the a06
  "enum unvalidated" negative is cured in the same file the amendment targets.
- configs/providers.yaml disable_thinking census REPRODUCED by my own yaml
  walk: 28 providers total, exactly 3 carriers (openrouter :223, deepseek
  :371, deepseek_overmind :401). The hermes/nous block (~:150-169) has no
  flag and carries the mechanism comment "Reasoning models burn thinking out
  of max_tokens: size calls up or content dies" (~:157). Exact.
- tools/hermes_burn.py:112-117: wire body is exactly {model, messages,
  max_tokens}. No thinking key. Exact.
- tools/ds_workhorse.py:93: `"thinking": {"type": "disabled"}` with the dated
  d4-probe comment at 86-92. Exact.
- a06-sacred-cow.json line 20 (row bd72a67f4a56): the 2-3x budget-confounded
  claim. Exact.

NUMERIC ERRATUM (hostile catch): economics.md says "arm 2 banked 2/10
zero-content at the 16000 cap plus 4/10 cap-pinned (a06 line 9-20 census)"
and "6/10 degraded arm-2 asks". a06's line 10 carries only 2 ok:false
zero-content and "7/14 rows pinned at or over"; it gives no arm-2 split. I
counted the manifest myself (memory/runs/ds_batches/sacred_cow_thinking_on.jsonl,
14 rows, venv python): at/over 16000 = 7/14 exact (2 arm-1: SESSION_FINDINGS_dig,
WIRE_PLAN; 5 arm-2), of which arm-2 contentful = 3 (SUBSTANCE_play_findings
16000/10161, THE_ROOM_REMEMBERS 16000/30010, SEASON_design 16000/2293), not
4. The 4th only appears by silently including cow2-SUBSTANCE_gaming_corpus at
15893 (93 tokens UNDER cap), which a06's own "at or over" definition
excludes. So strict: 3/10 cap-pinned, 5/10 degraded, not 4/10 and 6/10. The
finding survives (2/10 zero-content exact; arm 2 majority-degraded under
either reading), but the fold must not bank 4/10 or 6/10 as byte-backed.

Falsifier leg 1 TESTED THIS SITTING (the lens's OWED 1, closed): fired the
probe through the front door, 2 ping arms on lane=nous,
model=z-ai/glm-5.3-prime, max_tokens 512, ask "Reply with the single word:
pong" (mirror of the d4 ask):
- Arm A, body_extra {"thinking": {"type": "disabled"}}, depth=mechanical ->
  HTTP 200, "pong", 19 prompt / 42 completion, finish stop. Banked row
  memory/runs/route_chat/usage.jsonl 2026-10-04T11:10:31Z (key_env
  HERMES_API_KEY_2).
- Arm B, omission -> 200, "pong", 19/46, finish stop. Banked row
  2026-10-04T11:10:48Z.
Result: NO 400; the Nous gateway accepts the top-level disabled key. The
falsifier is dead on the carrier that produced the $0.46 burn. Cost: 88
tokens total, ping-scale (route_chat banks no cost_usd field, so the dollar
figure is unbanked; far under the $0.10 cap). Caveat honestly stated: a
one-word ask elicits no thinking on either arm (42 vs 46 completion tokens),
so GLM prime's omission-default on judgment-shaped asks remains OWED (needs
a judgment-scale arm, ~$0.25 at the :1151 shape, not a ping).
Note: first probe attempt without model= raised "no model for lane nous"
(the nous block carries models list, no default_model); the exception banked
its row (route_chat.py:155-160, everything-banks) at 11:10:12Z. Firing the
probe needs explicit model= on this lane.

Falsifier leg 2 (judged equal-budget A/B, ON beats OFF on mechanical): not
run, not runnable from a break pass; stays the live falsifier. The estate
still has zero judged thinking-OFF quality data (the lens said this; finding
2 is why).

## Finding 2: ds_workhorse.md item 6 mislabel - CONFIRMED

- watch/inbox/go_wave_20261004/ds_workhorse.md:62: "ds arm re-fired, uncapped,
  thinking-off, file-backed" byte-exact; carrier `python -m tools.ds_workhorse
  run` at :63-66; capped 0/26 at :72; "ds 3/28 total" at :82. Exact.
- queue/STANDING_RAILS.md:49-53 carries the re-fire receipt with "re-fired
  uncapped" (the lens's read: the rails wording is fine, ds_workhorse.md's
  "thinking-off" is the false half). Exact.
- d4_thinking_probe.md consequence 1 (:78-82) names the ds arm ON-by-omission.
  Exact.
- No erratum in ds_workhorse.md item 6: I read lines 50-169; the headline is
  unamended. Exact.
- Falsifier byte-tested through git (independent instrument, so this finding
  is CONVERGENT across two carriers): `git show
  d349ce7d2:tools/ds_workhorse.py | grep -in thinking` -> hits at lines 6,
  12, 32, 82, 86, ALL comments/docstring, none in the ask() body dict. The
  re-fire commit's wire carried no thinking key. The false law's origin is
  commit e00fe8ffc ("thinking-off by construction" in its message); the fix
  landed in aa7d5e8c0. No pre-refire commit shows the explicit key. The
  falsifier does not flip.
Move (erratum line in ds_workhorse.md item 6, append-never-rewrite) stands as
written.

## Finding 3: D2 accept-the-debt-standing - CONFIRMED

Ran `./.venv/Scripts/python.exe tools/violation_ratchet.py check` this
sitting. All 8 GROWTH lines reproduce byte-exact, including "GROWTH claim
af1d7045681fee89: tools/dungeon.py accepted at 756 lines, now 771 (+15)" and
mag/percolator.py 580->1022 (+442). Acceptance row verified:
configs/violation_baseline.json:5308-5313, accepted 2026-10-04,
accepted_lines 756, by go-wave-20261004-coordinator. Exact.
- TREE-MOVED NOTE: my run reads scope=1405 and RATCHET: FAIL, NEW unregistered
  file-too-long tools/social_rsi.py:578 (the SOCIAL RSI v0 commit 1336eed87
  landed 10:48Z after the lens's sitting). The lens's "PASS, scope=1404" was
  true at its moment and is stale on the current tree. This does not touch
  the D2 logic (dungeon's row is unchanged) but the coordinator must
  baseline-update social_rsi.py by name or split it before the next push.
- dungeon.py structure: 771 lines (my count), exactly one class (:148),
  dead play() at :447 shadowed by play() at :727 (both in the class body;
  Python last-binding rule). Seam arithmetic direction verified: helpers
  :488-611 + campaign :612-726 + play2 :727-771 = 284 lines; removing that
  block leaves 487 > 400, and even a campaign-only seam (160 lines) leaves
  611 > 400. Two-seam conclusion holds.
- Importer census reproduced: tests/test_burn_id_uniqueness.py:19 (`from
  tools import dungeon, tavern`) and tests/test_dungeon_parser.py are the
  only live importers; my full-tree grep hits only attic/, corpus/,
  dist_audit/ and agents/pytest-tmp copies; zero mag/ or main.py importers.
- pytest re-ran: tests/test_dungeon_parser.py = 13 passed in 0.80s; + tests/
  test_burn_id_uniqueness.py = 15 passed in 0.94s (the ask's "15 in under a
  second" reproduced). tests/test_dungeon_parser.py:9-17 header confirms the
  14 S4 PC fixtures replayed by the file's 13 tests. Exact.
- CENSUS ADDITION 1 (lens missed a live consumer): tools/prepush_golden_vector.py
  byte-pins dungeon.py structure at pre-push (DEFAULT_TARGET =
  "tools/dungeon.py" at :43; scenes-dict and win-gate anchors from blob
  a7d7d313d at :7-13). I ran it this sitting: "GOLDEN-VECTOR: ok - 11/11
  golden tokens" on the current 771-line file. Any future split must
  re-anchor this tripwire; that cost lands on the flip-condition price and
  further supports keep-now.
- CENSUS ADDITION 2 (lens's "subprocess cron" importer is imprecise): no
  repo file I scanned (tools/*.py, scripts/*, mag/*.py, main.py, queue/,
  configs/) contains a spawn string for dungeon.py; tavern.py does not spawn
  it (only a comment mention) and no scripts/*.ps1 names it. The hourly cron
  is documented at queue/STANDING_RAILS.md:32 only; the invocation lives
  outside the repo (scheduled task or manual). Immaterial to the verdict.
- Percolator history (closes the lens's OWED 5): git line counts by commit:
  b2cbb5810 (09-30) = 580 -> 3c83da5b0 (10-02 FILL-BALL) = 745 -> af9aa05f6
  (10-03 BUILD-IT-ALL) = 1022. Two growth events in three days = active
  burn, not one-time landing churn. STRENGTHENS the keep-verdict: dungeon's
  +15 is cohort noise and percolator is the real split candidate.
- mag/route_chat.py = 273 lines (economics receipt) exact.

## Closes on the lens's OWED list

- OWED 1 (funded-lane 400 / GLM wire shape): CLOSED for acceptance by my 2-arm
  probe above (no 400 on Nous GLM). OPEN for GLM omission-default on
  judgment-shaped asks (ping asks elicit no thinking; needs a paid
  judgment-scale arm).
- OWED 2 (manifest count): CLOSED. My count: 14 rows, 4/10 arm split exact,
  2 zero-content exact, 7/14 at/over exact, arm-2 contentful cap-pinned 3
  (not 4).
- OWED 3 (post-gate hermes_burn census): CLOSED. 985 post-gate rows (after
  2026-10-03T19:30Z; the substance gate is tools/hermes_burn.py:375-377, "the
  substance gate", whose own comment cites the 19:25:23Z row as founding
  datum), 273 ok:false all transport-class (0-token), ZERO hollow-class rows
  (no post-gate row with completion >= 8000 and starved content; the only 3
  high-completion rows are content-rich). The founding case has not recurred
  on that carrier; residual burn rate on it is zero measured.
- OWED 4 (10-15x magnitude): stays OWED (direction-only, per the d4 receipt's
  own out-of-scope note; providers.yaml:367-370 "12 tok vs 120 tok" is an
  08-03 one-ask figure).
- OWED 5 (percolator edit history): CLOSED as active burn (above).

## What the break pass adds that the lens missed

1. The probe result (finding 1 section): the D3 move's first leg is done and
   banked; the fold inherits a de-risked flip.
2. providers.yaml:219-222: the estate already carries a measured case where
   explicit-off does not WORK (openrouter/auto IGNORES thinking:{type:disabled},
   raw probe 2026-08-24, in-config comment; "Flag kept: harmless, helps
   non-/auto models"). The amendment text should carry one caveat clause:
   unconditional SENDING is safe everywhere measured; off-STATE on
   openrouter/auto comes from budget-sizing, not the key.
3. The current-tree ratchet is red on NEW unregistered tools/social_rsi.py:578
   (scope=1405, FAIL). Needs baseline-update by name or a split, orthogonal
   to D2.
4. STAGE_B's own 9826 reasoning tokens (usage.jsonl:1152): the pair paid
   25824 reasoning tokens, so the $0.464 is if anything understated as a
   thinking-tax exhibit.
5. The arm-2 numeric erratum (4/10 -> 3/10 strict, 6/10 -> 5/10 strict).
6. prepush_golden_vector.py as a 4th live dungeon consumer (re-anchor cost on
   any split), currently green 11/11.
7. Percolator is a two-event active grower, not churn.

## Ractor-facing one-liners

- D3: explicit thinking:{type:disabled} on the wire for every depth=mechanical
  ask, carried by each carrier; depth=design the only ON path; falsifier 1
  measured dead on Nous GLM this sitting (banked rows 11:10:31Z/11:10:48Z),
  falsifier 2 (judged A/B) remains live; losing law surface is
  queue/STANDING_RAILS.md Law 1's "per-lane call laws" clause (:10-12),
  amendment text in economics.md:72-78 plus the openrouter/auto caveat.
- D2: accept the debt standing (accepted by name go-wave-20261004-coordinator,
  violation_baseline.json:5308); flip conditions as economics.md:178-185, plus
  any split must re-anchor tools/prepush_golden_vector.py.

## OWED by this pass

- GLM prime omission-default on a judgment-shaped ask (paid arm, ~$0.25).
- Dollar cost of my 2 probe arms (route_chat banks no cost_usd; 88 tokens total).
- The dungeon hourly cron spawn location (outside this repo's scanned files).

Receipt discipline: no file edited outside this bank; probe fired only
through mag.route_chat (front door, dormant gate, endpoint fence intact);
no subprocess spawns from Python (win32 CREATE_NO_WINDOW law not exercised;
all commands ran via the Bash tool directly).
