# THE STANDING WORKFLOWS 2026-10-01: nothing lives in the operator's head

Class: RECEIPT · Writer: zcode seat (standing-fleet lane) · Operator order:
"what other workflows can we put into practice standing so I don't have to
keep it in my head every time. Self steal."

## The fleet (all saved, gated, fire-by-name)

| name | fires when | args | proven |
|---|---|---|---|
| olm-mine | cron 10:00 DAILY (automation-cac38363) | slug=YYYY-MM-DD | 2 runs, 64/64 miners, 44 confirmed |
| gap-analysis | after any burst; weekly | slug, period? | 15/15 lanes, 75 rows, caught 4 live defects |
| fill-ball | immediately after gap-analysis | register, slug | 7/7 closed the register's top gaps same-night |
| ractor-engine | any decision/drop needing lenses | topic, slug, lenses?, moonshots? | dogfooded on real gaps first night |
| salon-mine | a transcript folder surfaces | folder, slug | 20-deep on the vault, 50+ rows before quota |
| librarian-expedition | weekly or citation-heavy burst | slug | 61 primaries landed, 90.6MB, doctrine minted |
| wide-dig | a heavyweight subject drops | topic, slug | SpikingBrain: 8 lenses, tweet deflated by primary |
| drop-dig | a landscape brief or multi-system paste | brief, systems, slug | localfirst: brief corrected, 14 register rows |
| mickey17-v2 | 50-wide artifact audits | topic, targets, width | gap-analysis ran on it |
| the-gala | multi-division waves | slug, lanes, width | 5 balls tonight, 50+ lanes danced |
| the-50 | THE 50 program relaunch | completed? | the original width engine |
| game-dig-* (5 veins) | a game-vein dig order | per-vein briefs | the original dig pattern |

## The standing loop (the cycle that runs itself)

1. DAILY: olm-mine (10:00 cron) + tapestry (09:15) + improve (08:00) +
   census (08:30) + FTS (09:00) - the cadence layer, all armed.
2. PER BURST: gap-analysis audits what the burst produced -> fill-ball lands
   the register's top one-sittings -> ractor-engine rides anything ambiguous.
3. PER DROP: drop-dig (light) or wide-dig (heavy) on the subject.
4. PER WEEK: librarian-expedition closes the offline-verification loop.
5. ON VAULT SURFACES: salon-mine mines the operator's own past thinking.

## The laws the fleet carries in every ask

Never fabricate (OWED, never asserted) - no em-dashes - cite path:line or
URL - byte-check before banking - hostile second pass before speaking -
receipt or it didn't happen - reports in deterministic order.

## What is NOT standing yet (named, one sitting each when needed)

- music-cut (style-spec + cutter pipeline) - proven once, save on second use
- night-close (the dawn consolidation) - currently the seat's ritual
- commit-queue (the serialized commit helper) - owed after 2 stale locks
- the citation-lint pre-push wiring - tool landed, hook line owed

## THE ROUTING LAW (2026-10-01, operator: "use deep seek like double width then quad"): 

AmendWorkflow(subagent_model=X) reroutes ANY running or parked workflow to ANY
route in the chain, mid-flight, cache importing everything finished. The chain:

1. account:zai-individual-coding-plan/GLM-5.3-Flash (the session seat)
2. account:zai-start-plan/GLM-5.3-Flash (fresh resets)
3. account:zai-offpeak-idle-plan/GLM-5.3-Flash (DISCOVERED 10-01 but
   MEASURED DEAD for workflows same night: 7/7 lanes buried with Turn
   execution failed - the plan exists but cannot serve workflow subagents;
   works for interactive chat only. Do not route workflows here.)
4. zai-api/GLM-5.3-Flash (API-key direct, no plan quota, untested)
5. DeepSeek API (ds_workhorse, $0.0043/ask, thinking-off, for MECHANICAL work)
6. local Ollama (gemma:2b etc, $0, for $0 probes and benches)

When a plan hits quota: AmendWorkflow(subagent_model=next_in_chain). Never
refire blind, never rebuild - the cache carries. The operator re-seats from
the GUI; the seat can also do it programmatically via AmendWorkflow.

DFHack flywheel: the same AmendWorkflow call with a revised script = drop-in
edits on the fly. The two together = DFHack for the swarm: reroute the
accounts AND edit the code, without stopping the run.
