# BREAK-MOONSHOT-1 - hostile second pass on lens moonshot-1 (2026-10-03)

Break pass on `watch/inbox/ractor_engine/2026-10-03-surface-migration/moonshot-1.md`.
Every number below was read or computed THIS sitting; instruments named inline.
No pytest run (not asked of this pass). Zero em-dashes.

## INSTRUMENT NOTE

- The Bash tool here runs bash WITHOUT coreutils (ls/grep/wc/head all missing),
  so every census is a `.venv/Scripts/python.exe -c` run this sitting. No
  hand-copied counts. schtasks ran via subprocess with creationflags 0x08000000
  (CREATE_NO_WINDOW), per the win32 law.
- The usage ledger is LIVE: every count drifted upward between the lens's read
  and mine (minutes apart). Drift is noted per finding; none of it reverses a
  verdict.

## VERDICTS

### Finding 1 (named engine never fired on the rails): CONFIRMED, one citation corrected, one sharpening added

- My census (venv python over `memory/runs/hermes_burn/usage.jsonl` this
  sitting): 1,226 rows, $64.25 total; Nous-hosted anthropic SKUs $62.61
  (97.4 percent: opus 494 rows / $45.76, sonnet 315 / $7.65, fable 180 /
  $8.22, haiku 230 / $0.98); z-ai/glm-5.3-prime 7 rows / $1.64 (2.6 percent,
  BYTE-EXACT vs the lens); glm-5.3-max rows: 0. The lens read 1,152 / $64.05 /
  opus 447 - live-ledger drift, same shape.
- The lens's own falsifier, self-checked: `memory/runs/route_chat/usage.jsonl`
  exists, 6 rows, all deepseek-v4-flash, zero glm-5.3-max. Falsifier not fired.
- CITATION DEFECT: the lens cited "anthropic-only PRICING at
  tools/hermes_burn.py:97-102". Lines 97-102 are `_assert_public_endpoint`
  (the endpoint fence). The PRICING dict is `tools/hermes_burn.py:71-76` and IS
  anthropic-only. Claim survives on the corrected cite.
- SHARPENING the lens missed: the carrier structurally cannot fire the engine.
  `tools/hermes_burn.py:288-290` raises on any model not in PRICING, and
  PRICING carries only the four anthropic SKUs. The descent driver's paid
  carrier refuses glm-5.3-max BY CODE. The `configs/providers.yaml` nous lane
  roster (lines 159-162) names z-ai/glm-5.3-prime, qwen/qwen3.8-max-prime,
  fireworks/ember-1 - no glm-5.3-max (route_chat does not enforce roster
  membership, `mag/route_chat.py:116`, so an unlisted model is attemptable but
  unlisted). The lens's 45-min move costs a config + pricing edit FIRST.

### Finding 2 (cost headline 1.7x the ledger): CONFIRMED, byte-exact

- My join (register ids to ledger rows, this sitting): 14 ids in
  `watch/inbox/frontier_delta_register_20261003.json`, exactly 14 ledger rows,
  $7.74 total, prompt 375,948 / completion 310,288, per-ask $0.28-$0.78,
  fires-per-ask {1: 14}, avg 26,853 prompt / 22,163 completion. Every number
  in the finding reproduces byte-exact. $7.74/14 = $0.553/deliverable.
- `watch/inbox/DAY_SYNTHESIS_20260930.md:57` confirmed verbatim: the z.ai
  seat "has no local meter at all ... COST_TRUTH unknown #4".
- MINOR DEFECT: the register carries NO cost column at all (fields: id,
  frontier_chars/cites/unver, flash_chars/cites/unver, contract_parts), so the
  move "correct the Delta Register's cost column" should read "add one". Also
  no win/loss fields (the lens's own blind spot, confirmed).
- Flash-arm figures (9.5M seat tokens, ~582K per deliverable, 16x): recursive
  search of watch/inbox/**/*.md for "582K"/"9.5M"/"per deliverable" hits ONLY
  the sibling lens files themselves (economics.md, lineage.md, dogfood.md
  quote them as ask-given; lineage.md says "the 9.5M total is carried from the
  ask, not re-measured"). Stays OWED with instrument named.

### Finding 3 (steering organ drowned): CONFIRMED, numbers drifted UP, re-pay now priced

- `memory/attention.md` this sitting: 850 "INSTANCE-GUARD doubled-key alarm"
  lines of 1,178 total lines (72 percent of the alarm channel). Lens said 809;
  live-file drift upward.
- INSTRUMENT NOTE: the lens wrote "809 'doubled_key' alarm lines". The alarm
  text in the file is "doubled-key" with a HYPHEN (`tools/instance_guard.py:203`);
  a literal underscore grep of attention.md returns 0. Count real, quoted
  token loose.
- `TAVERN_r1_Maud Ashgrove`: EXACTLY 15 ledger rows on 2026-10-03, first clean
  at 11:41:31.113636Z, 14 flagged doubled_key - byte-exact vs the lens.
- Ledger: 1,226 rows vs 209 distinct (id,turn), 1,017 excess (lens: 1,152 /
  176 / 976). doubled_key=True rows: 850.
- `tools/instance_guard.py:191-213` confirmed byte-exact: doubled_key_check
  returns the row to bank flagged (line 213) or as-is (line 199), writes the
  alarm, never blocks. `tools/hermes_burn.py:149-156` banks flagged rows.
- NEW NUMBER the lens never priced: the 850 doubled rows cost $15.28
  re-paid - 23.8 percent of the entire $64.25 ledger, nearly 2x the whole
  frontier arm. The disease is a money bug, not just noise.

### Finding 4 (migration tried, BLOCKED in code): CONFIRMED, byte-exact

- `mag/seat_dispatch.py:141-162` verified line-by-line: zcode-cli entry,
  T1 VERDICT 2026-09-03 BLOCKED (lines 147-156), the three-item evidence chain
  (parser rejects documented flags; zod strips object-form model config;
  builtin:zai-coding-plan unresolvable outside the exe runtime), reopen routes
  named (Protocol app-server stdio client, or a CLI update).
- Vendored source confirmed on disk:
  `corpus/library/zcode-zai-org/repo/apps/zcode-cli/` lists real repo files
  (.dockerignore, .env.template, .husky, AGENTS.md, ...).
- Re-test census (string-level, my scope): zcode-cli/zcode.cjs mentions
  outside seat_dispatch live in mag/skill_lifecycle.py, tools/
  dispatch_landing_join.py, and 2026-09-03-era queue/handoff/zcode-cli/OUTBOX
  files. None read in full; none is plausibly a headless probe. "No byte since
  re-tests the block" survives a string census, not a full read.
- Falsifier NOT run: a headless zcode-cli ask costs a seat fire on the
  operator's account; needs operator GO like finding 1's move.

### Finding 5 (interactive residue is three jobs; interrupt law is scar tissue): CONFIRMED, every cite byte-checked

- `queue/STANDING_RAILS.md:17-18` (law 3, interrupts never cancel) and :49-50
  (judge-wave kill: "30/50 lanes landed, ~20 killed by the interrupt") both
  verified verbatim.
- `scripts/descent_driver.sh:25-29` verified: STOP path line 25, the
  `while [ ! -f "$STOP" ]` loop line 29. (The pidfile claim lock is at :13-23.)
- `watch/inbox/envelope_50w_20261003.md` verified: "50/50 agents returned
  their answer. ZERO surfaced 429/1302" (line 21), Task-agent width ceiling
  amended to 50 (lines 29-38), workflow children stay maxAttempts-0 (36-38).
- `watch/inbox/STANDING_WORKFLOWS_20261001.md` verified: fleet table lines
  11-22 (12 rows incl game-dig-*), offpeak DEAD for workflow children lines
  53-57 ("7/7 lanes buried with Turn execution failed").
- `tools/workflow_gate.py` = 334 lines EXACT. `memory/workflows/REGISTRY.jsonl`
  = 61 valid rows now (lens said 60; +1 live drift, last row registered
  2026-10-03T20:18:03Z, Wide-dig-the-Grok-bot-ecosystem.dwf.ts).
- Driver beats: `memory/runs/hermes_burn/driver.beat` 2,742 lines, last BEAT
  2026-10-03T20:32:58Z cycle=1678 (lens: past cycle 1676 - live drift, holds).
- `mag/mcp_server.py:4-6` verified: TOOL_MAP served natively to zcode, cursor,
  claude, codex, opencode (line 35: reuse tools.TOOL_MAP, single source).
- `watch/inbox/mag_rails_plugin_spec_20261003.md:10-12` verified: tool 1
  mag_route_chat wraps mag.route_chat, "the one door".
- `tools/tavern.py:37` verified verbatim: `from tools.hermes_burn import
  _bank, _call, _hermes_key, _now` - the self-call debt is real.
- Adoption census (my own walk, py/sh/ps1/cmd under mag/tools/scripts/tests):
  route_chat appears in EXACTLY ONE file, mag/route_chat.py - byte-exact match
  to the lens's grep claim.

## ADDITIONS (what the lens missed)

- A1 ENGINE UNFIREABLE AS CODE: `tools/hermes_burn.py:71-76` + `:288-290`
  (refuses non-anthropic models) and `configs/providers.yaml:159-162` (nous
  roster omits glm-5.3-max). The migration's named engine needs a PRICING/
  lane edit before ANY probe can run. Falsifier: a glm-5.3-max row landing
  without such an edit. Move: 2-line config edit + one route_chat fire under
  GO (60 min).
- A2 THE DOOR IS COST-BLIND AND TRIPWIRE-BLIND: `mag/route_chat.py:150-155`
  banks ts/lane/model/goal/key_env/tokens/ok - NO cost_usd and NO
  doubled_key_check (compare `tools/hermes_burn.py:153`, which calls the
  tripwire, and :379, which banks cost). The one-front-door surface cannot
  price itself, and the $15.28 re-fire waste pattern would migrate to it
  silently. Layer 4's dawn compiler would read a cost-blind ledger. Move:
  port cost + tripwire into route_chat._bank (30 min).
- A3 THE 8-5 SCORECARD RESTS ON AN UNBANKED AXIS, AND THE REGISTER'S OWN
  COLUMNS LEAN FLASH: computed from the register this sitting - citations
  split 5 flash / 5 frontier / 4 ties; frontier unver totals 186 vs flash 68
  (frontier outputs carry ~2.7x the unverified-cite load; WIRE_PLAN frontier
  cites 0/unver 6 vs flash 141 cites/12 unver; PARTYCHAT frontier unver 42).
  The judge-quality axis that produces 8-5 is banked nowhere. CONVERGENT: the
  sibling accuracy lens independently found the flash arm's per-deliverable
  meter "inconsistent by 26 percent"
  (`watch/inbox/ractor_engine/2026-10-03-surface-migration/accuracy.md:186`,
  also :16 and :43). Move: add cites/unver/cost columns to the register's
  win-rate row before any judge re-run (20 min).
- A4 THE AUTOMATION CENSUS IS QUERYABLE FROM THIS SEAT - the lens's blind
  spot 1 was instrument failure, not impossibility:
  `~/.zcode/v2/tasks-index.sqlite` table automations (19 rows) carries
  automation-b1ce1342-e449-... "Hourly arena cycle: dungeon + tavern + gwap
  bank, $25 daily cap" cron "0 * * * *" and automation-cac38363-e6a0-...
  "OLM mine daily burn 10:00" cron "0 10 * * *"; automation_runs (4,405 rows)
  shows b1ce1342 with 8 runs on 2026-10-03, 13:00-20:00Z, the FIRST failed and
  7 succeeded. The ask's "8 cycles today" is byte-backed, with a failure the
  ask and lens both missed. Move: fold the sqlite census into the dawn
  compiler as the headless-estate status feed (45 min).
- A5 THE NUL-FILE TRAP IS LIVE IN-REPO, UNMENTIONED: my walk found 43
  device-named files - `./nul` at repo root plus 42 under
  `agents/pytest-tmp-{3712,15628,25728,43956,44872,47224}/` (the stale
  pytest-tmp sweep residue). Win32 shells that redirect keep minting these;
  they resist plain delete and poison walks. A migration that runs MORE
  headless shells multiplies the trap. Move: scheduled \\?\-path sweep + a
  redirect lint in the rails (45 min).

## CROSS-CHECKS ON THE BLIND SPOTS

- schtasks rerun this sitting: 245 total Windows tasks, 16 hits for my
  Mag-family regex (mag-docker-watchdog + 15 Mag* tasks incl.
  MagCensusPatrolDaily, MagFtsIndexDaily, MagImproveDaily). The sibling
  dogfood lens's "21 scheduled tasks" used an unnamed filter; NOT confirmed by
  my instrument, not contradicted either (filter-dependent).
- Sibling lens bodies: I searched all of them via the flash-arm figure hunt
  and read accuracy.md's convergence lines; the other four bodies remain
  unread beyond grep fragments (same limitation the lens declared, narrowed).

## NOT RUN / OWED

- No pytest, no test suite, no build.
- No headless zcode-cli probe, no glm-5.3-max rail fire (both are paid/seat
  actions gated on operator GO).
- No full read of the five sibling lens bodies; no Hermes-dispatcher or portal
  balance audit.
- 9.5M / 582K / 16x flash-arm figures: no in-repo byte outside the sibling
  lens files carries them; ask-given, instrument named above.
- Universal claims in this pass are scoped to the censuses named: the zero
  glm-5.3-max claim covers the two ledgers I read plus the code paths cited;
  the nul census covers a full-tree walk pruned only of .git/.venv/
  node_modules/__pycache__.
