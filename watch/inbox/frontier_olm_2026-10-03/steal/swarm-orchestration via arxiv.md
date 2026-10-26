# STEAL CARD DRAFT (round 1): swarm-orchestration via arxiv

- Area: swarm-orchestration via arxiv
- Banked: 2026-10-03, frontier olm steal round 1, first draft (no prior critique)
- Inputs: 5 confirmed arxiv finds (confidence 1 each, overlap-checked NEW by the finder, full-text source-fetched 2026-10-03 per each find's own record). Quotes below are the finds' quoted lines; this seat took them as ask material and did not re-fetch the papers.
- Catalog spot-check run this seat: `rg -in "PANDA|Revisable World|2609.38482|2609.32802|DEALS" catalog/catalog.jsonl` returned only filename coincidences (`panda.svg` at catalog/catalog.jsonl:362586, and the case-insensitive substring "panda" inside the `ExpandableContent.tsx` rows at lines 344578, 344587, 346480), zero paper-title hits. The finds' NEW claims hold against the catalog bytes.

## The composite steal (one mechanism): salvage-first fault-tolerant fan-out

The mesh, not the child, is the retry strategy. Workflow children die clean by law (maxAttempts 0, zero adapter retries, AGENTS.md:33 fan-out width law) and recovery is carried by the fleet in four moves:

1. **Sibling takeover** (PANDA, https://arxiv.org/abs/2609.38482, find dated 2026-09-29). Find claim: "matches state-of-the-art accuracy at up to 8x the efficiency, and sustains 100% task completion under faults where existing systems fail", via redundancy plus replanning on a decentralized mesh. Port: the wave script's per-item loop catches a dead child and re-fires that item's ask from one sibling. The re-fired ask stays byte-identical for the cache (AGENTS.md:116: byte-identical asks for cache hits, amend-don't-resume).
2. **Re-derivation grounding** (https://arxiv.org/abs/2609.32802, find dated 2026-09-26). Find claim: "Grounding an inspector agent in that problem is worth +0.608 [+0.517, +0.700] to +0.358 over a blind one on four open-weight backbones served with thinking disabled." Post-fault salvage is set by re-derivability, not token presence: re-expose the ORIGINAL problem, do not forward the transcript. Port: the takeover ask carries the original item spec, never the dead child's partial output.
3. **Certified prefix inheritance** (https://arxiv.org/abs/2610.01160, find dated 2026-10-01). Find claim: "Combining fast invalidation with certified inheritance then lowers paired revision-to-successor TTFT by a median 17.1% over native abort and cold restart." Port: report() checkpoints (gate G4, tools/workflow_gate.py:17 and :62-63: "incremental report() inside the fan-out (work survives a dead run)") become version certificates; the amended run imports finished work by output hash and re-fires only what changed. The estate already holds the primitive (AGENTS.md:112: SaveWorkflow so reruns are amendments; every check registers a registry row).
4. **Tri-state fail diagnosis** (https://arxiv.org/abs/2609.38761, find dated 2026-09-30). Find claim: "a system can break one of its collective mechanisms, the rules that govern how agents route, admit, store, and act on shared information, and still return the right answer." Port: a gate FAIL row stops being one red verdict and names the broken collective mechanism (routing = dispatch shape per AGENTS.md:33; admission = the G-checks; storage = the salvage path), each verdict tri-state (supported / ruled out / unknown) per the tri-state doctrine named at .agents/skills/agent-harness/SKILL.md:3. Real FAIL rows with per-check ok flags exist to re-diagnose: memory/workflows/REGISTRY.jsonl lines 18, 20, 26, 36, 39.

## Find-by-find organ map

| Find | Estate organ fed | Concrete port move |
|---|---|---|
| PANDA (2609.38482) | gopher fleet (workflow children + queue/lanes: android_surface, bard_ledger, builder, day_work, economist, elder, forge, harvest, jev, night, prose, research, verified by `ls queue/lanes` this session) | dead-child catch in the fan-out loop re-dispatches the byte-identical item ask to one sibling; trust grading stays at the parent gate |
| Revisable World (2610.01160) | context pack + gopher fleet amend path | certify inherited prefixes by output hash so "imported" is a fact, not a hope; zero obsolete output is the acceptance test on the next amend |
| Re-derivability (2609.32802) | context pack + repair asks in the olm-mine fold (.agents/skills/frontier-mine/SKILL.md:3, fold step at :19-21) | salvage and repair asks carry the original item spec byte-identical, transcript discarded |
| DEALS (2609.33768, find dated 2026-09-27) | gopher fleet lanes | expertise-aware routing: tag each item with lane affinity, keep per-lane local queues, let a partially solved item resume on another lane's child carrying its report() prefix |
| Where Do MAS Fail (2609.38761) | percolator / law via the workflow registry | add a tri-state diagnosis block to FAIL rows naming routing vs admission vs storage as supported, ruled out, or unknown |

DEALS claim quote for the record: "process independent tasks concurrently within and across agents, and partially solved tasks can be resumed by other agents."

## The probe (one, falsifiable, cheap)

Sibling-takeover A/B on the next fan-out wave. Run the wave at max_concurrency 3 (standing law, AGENTS.md:33). The wave script logs every child death (429/1302) with its item id. Split the dead items: half get a one-sibling takeover firing the byte-identical original ask; half stay dead as control. Measure net completions added per arm and tokens spent. FALSIFIED IF the takeover children die at the same rate as the originals (zero net completions on the wave): that would prove mesh-side recovery does not survive this account's rolling-throughput cap, pin recovery to parent-side amend only, and strike the PANDA port from the estate. Cost: one wave, zero new infrastructure, log-only instrumentation.

## Verification ledger

Ran this seat (2026-10-03), with outputs:

- `rg -n "salvage" tools/workflow_gate.py` → :17 "G4 salvage report() fires inside the fan-out so work survives a dead run"; :62-63 ("G4-salvage", "incremental report() inside the fan-out (work survives a dead run)")
- `rg -n "maxAttempts|amend|SaveWorkflow|gopher" AGENTS.md` → :33 fan-out width law (workflow children maxAttempts 0, keep max_concurrency 3 or less); :112 gate checks + SaveWorkflow amendments + registry rows; :116 byte-identical asks for cache hits, amend-don't-resume
- `ls queue/lanes` → 12 lane dirs (android_surface, bard_ledger, builder, day_work, economist, elder, forge, harvest, jev, night, prose, research) + law_lattice.json
- `rg -n "tri-state|tristate" .agents/skills/agent-harness/SKILL.md` → :3 "tri-state claims" in the doctrine description
- `rg -n "FAIL|err" memory/workflows/REGISTRY.jsonl | tail -5` → FAIL rows at lines 18, 20, 26, 36, 39, each carrying per-check ok flags
- `rg -in "PANDA|Revisable World|2609.38482|2609.32802|DEALS" catalog/catalog.jsonl` → only filename coincidences, zero title hits (NEW claims confirmed)
- `rg -n "fold|olm-mine|steal-map" .agents/skills/frontier-mine/SKILL.md` → :3, :15, :19-21, :24 (olm-mine fire, fold, steal-map ritual)

Not run this seat: the paper fetches and fault-number verifications (the finds carry those as source-fetched 2026-10-03 with confidence 1; taken as ask material per the standard). No pytest run (the ask names no test target). OWED: none.
