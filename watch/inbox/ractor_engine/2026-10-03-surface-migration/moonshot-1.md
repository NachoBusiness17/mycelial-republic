# MOONSHOT-1 - surface migration raction (2026-10-03, lens moonshot)

Jacket: no sacred cows. ZCode, the interactive seat, and this ractor's own
existence are on the table. Every number below was read or computed this
sitting (commands named inline) or is marked ask-given / OWED. Zero em-dashes.

## THE VERDICT

**Hybrid, inverted from the obvious: the migration is real but its object is
wrong. The estate should not migrate its primary surface to Hermes-launched
headless chairs; it should complete the RAILS as the surface and demote every
chair, interactive seat included, to a client of one door.** The rails already
run the estate unattended (descent driver beats past cycle 1676, hourly arena,
21 scheduled tasks per the sibling dogfood census); what still lives only in
the interactive seat is three measurable jobs: operator-GO authorization,
width-50 Task transport, and the ZCode-native standing workflow fleet. Migrate
the steering into the rails; keep the chair for those three; onboard headless
chairs only through `mag.route_chat` so fences and banking are inherited by
construction. "Migrate to headless" is the wrong sentence; "make the door the
surface" is the right one.

## WHAT I PERSONALLY RAN THIS SITTING

- Ledger census (venv python over `memory/runs/hermes_burn/usage.jsonl`):
  1,152 rows, 176 distinct (id,turn), 976 excess rows, $64.05 total,
  $62.41 anthropic SKUs (opus 447 rows / $45.65; fable $8.22; sonnet $7.59;
  haiku $0.95), z-ai/glm-5.3-prime 7 rows / $1.64 (2.6%), and ZERO rows for
  glm-5.3-max or any GLM-5.3-max engine.
- Delta-ask cost census: the 14 register ids
  (`watch/inbox/frontier_delta_register_20261003.json`) match exactly 14
  ledger rows, 1 fire each, $7.74 total ($0.28-$0.78 per ask; avg 26.9K
  prompt + 22.2K completion tokens). The ask-given "~$13" is 1.7x the bytes.
- Alarm census: `memory/attention.md` carries 809 doubled-key alarm lines;
  `TAVERN_r1_Maud Ashgrove` has 15 paid fires on 2026-10-03 (first clean at
  11:41:31Z, then 14 doubled). The tripwire stamps and alarms but never
  blocks (`tools/instance_guard.py:191-213` returns the row to bank).
- Adoption census: `grep -rln route_chat mag tools scripts tests` returns
  ONLY `mag/route_chat.py`. The one-front-door law landed today with zero
  call sites; tavern still imports `_bank/_call` straight from
  `tools/hermes_burn.py` (`tools/tavern.py:37`).
- Vendored-source check: `corpus/library/zcode-zai-org/repo/apps/zcode-cli/`
  exists (repo root with apps/, harness/ siblings confirmed by ls).
- Read whole: `state/CURRENT.md`, `queue/STANDING_RAILS.md`,
  `mag/route_chat.py`, `scripts/descent_driver.sh`,
  `tools/instance_guard.py`, `watch/inbox/mag_rails_plugin_spec_20261003.md`,
  `watch/inbox/STANDING_WORKFLOWS_20261001.md`,
  `watch/inbox/envelope_50w_20261003.md`,
  `watch/inbox/burn_claims_50wide_20261003.md`,
  `watch/inbox/DAY_SYNTHESIS_20260930.md`, `mag/seat_dispatch.py:110-165`,
  `tools/dungeon.py` header, `tools/hermes_burn.py` header.

## FINDINGS

1. **The migration's named engine has never fired on the rails it would
   inherit (CONVERGENT with the economics lens's by-model census; my new cut
   is the zero-row result).** The rails' measured fuel is Nous-hosted claude
   SKUs, 97.5 percent of cash; glm-5.3-prime is 2.6 percent; glm-5.3-max is
   absent from the ledger entirely. The thesis sentence "GLM-5.3-max via the
   Nous API launching the standing workflows" names a configuration with no
   production row. Falsifier: any glm-5.3-max row in `usage.jsonl` or
   `memory/runs/route_chat/usage.jsonl` doing rail work breaks this. Move
   (45 min): fire one $0.5-class glm-5.3-max rail ask through route_chat
   under operator GO, bank the row, and only then argue the engine.

2. **The ask's cost headline is wrong against the ledger, and the correction
   strengthens the cash arm.** 14 frontier design asks cost $7.74 measured
   ($0.55 per deliverable), not "~$13" ask-given. Against the flash arm's
   ~582K seat-window tokens per deliverable (ask-given; no local meter for
   the z.ai seat exists, `DAY_SYNTHESIS_20260930.md:57` names it COST_TRUTH
   unknown #4), the frontier arm is far cheaper in its own currency than the
   ask claims. Migration math must run on measured rows, not rounded
   headlines. Falsifier: a second ledger carrying the missing $5.3 revives
   the $13 claim. Move (20 min): correct the register's cost column from
   `usage.jsonl` and re-state the crossover.

3. **The estate's steering organ is already drowned at headless scale.**
   809 doubled-key alarms sit in `memory/attention.md`; recurring rails reuse
   (id,turn) across cron cycles so every arena re-run trips the tripwire AND
   re-pays (15 fires of one tavern actor today), and the tripwire is
   ingest-side only, it never blocks a fire. A headless estate steers through
   this channel; migrated today, the dawn read is cry-wolf noise hiding real
   spend. Falsifier: a day with under 20 alarm lines while recurring rails
   re-fire breaks this. Move (1-2 h): cycle-unique rail ids plus a pre-fire
   skip for doubled (id,turn), and an alarm cap per hour in the dawn
   compiler.

4. **This exact migration was tried and is BLOCKED in code, not doctrine.**
   `mag/seat_dispatch.py:141-162` holds the 2026-09-03 T1 VERDICT on
   zcode-cli headless: parser rejects documented flags, the zod schema
   silently strips object-form model config, and builtin:zai-coding-plan
   resolves only inside the exe runtime. Named reopen routes: the Protocol
   app-server stdio client, or a CLI update shipping the runtime builder.
   The CLI source is vendored in-repo (`corpus/library/zcode-zai-org/repo/
   apps/zcode-cli/`). No byte since re-tests the block. Falsifier: one
   headless zcode-cli ask returning rc=0 with correct model routing breaks
   the BLOCKED verdict. Move (one morning): build the stdio probe against
   the vendored source; the result either reopens the headless chair or
   prices its true cost.

5. **The interactive seat's irreplaceable residue is three jobs, and the
   interrupt law is scar tissue that hides one of them.** Law 3
   "interrupts never cancel" (`queue/STANDING_RAILS.md:17-18`) was minted
   because an operator interrupt killed ~20 of 50 judge lanes (lines 49-50);
   it blesses unkillable spend instead of building the missing primitive,
   which already exists in miniature: the driver's STOP file
   (`scripts/descent_driver.sh:25-29`). Meanwhile the seat's unique value is
   measurable: only-operator-GO (the security lens's authorization gap),
   width-50 clean transport (`watch/inbox/envelope_50w_20261003.md`: 50/50,
   zero 429/1302), and the ZCode-native fleet (12 saved workflows on ZCode
   automations, gate 334 lines, registry 60 rows) that no headless chair
   carries; the offpeak plan already measured DEAD for workflow children
   (`STANDING_WORKFLOWS_20261001.md:53-57`). Falsifier: a headless rail
   wave with per-lane checkpoints that survives a hard interrupt losslessly
   retires law 3; a headless judge re-run matching interactive judge
   quality at lower cost migrates the judging job and shrinks the hybrid.
   Move (half a day): generalize DRIVER_STOP into one estate fence file
   every rail polls, then re-run the 20 killed judge lanes headless under
   it and score against the interactive 8-5 (ask-given scorecard; I could
   not re-derive 8-5 from the register JSON, which carries no win/loss
   fields: OWED).

## THE ARCHITECTURE (the 10x shape)

- Layer 0 policy: `configs/providers.yaml` lanes, dormant gates, per-lane
  laws. Unchanged.
- Layer 1 door: `mag.route_chat` becomes load-bearing. Today it has zero
  importers; the one-sitting sweep is tavern/dungeon/hermes_burn/grok_burn
  (the registered debts, `STANDING_RAILS.md:44-48`) plus the plugin/MCP
  handle (`mag_rails_plugin_spec_20261003.md`, `mag/mcp_server.py:1-45`
  already serves TOOL_MAP to zcode/cursor/claude/codex/opencode).
- Layer 2 rails: descent driver, ds_workhorse, arena, waves, each with an
  O_EXCL claim (landed) and the shared STOP fence (to build).
- Layer 3 chairs: the interactive ZCode seat keeps GO + width + the
  workflow fleet; opencode/hermes chairs onboard through the door; cron
  automations are just another client. No chair is primary; the door is.
- Layer 4 steering: dawn report compiled from ledgers with alarm caps, the
  Delta Register as the routing table, key balances polled from the portal
  (the estate has never measured the balance it budgets against,
  `DAY_SYNTHESIS_20260930.md:51`).

## BLIND SPOTS (honest)

- The ZCode automation ids (b1ce1342, cac38363) live outside the repo; I
  could not query them from this seat and rely on artifact corroboration
  (playground dirs, driver beats) plus the sibling dogfood lens's
  schtasks census, which I did not rerun.
- I ran no tests; every check is a byte, ledger, or grep census. The ask's
  "16x window tokens" and "582K per deliverable" figures remain ask-given,
  unverified by me; no local meter for the z.ai seat exists to verify them.
- The 8-5 judge scorecard is ask-given; the register JSON I read has no
  win/loss fields, so I could not re-derive or falsify it this sitting.
- I read only the heads of the five sibling lens files; deeper convergences
  or contradictions in their bodies are unseen.
- I did not audit Hermes-the-dispatcher, local Ollama surfaces, or the
  portal balance APIs; the Layer 4 steering design assumes instruments I
  have not priced.
- This ractor itself is a ZCode dynamic workflow: the fleet that audits the
  migration is ZCode-native, so my verdict carries an interest; the
  falsifier path (headless judge re-run) is also the test of my own chair.
