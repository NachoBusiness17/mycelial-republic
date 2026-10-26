# s2-01: memory/rib_bus/ full census (domain-by-domain map)

Item: s2-01 · Census taker: f2-s2-01 gopher · 2026-09-28 (EDT) · Bank: flash50/rib-bus-census.md + flash50/s2-01.md (byte-identical)

## Method (every number below came from a command run this session)

1. `ls -la memory/rib_bus` : full enumeration, sizes, mtimes.
2. venv python pass over all 51 files: sha256, mtime, JSON parse, top-level keys, per-file domain name, rib count, rib key schema.
3. Full text read of every file under 21 KB via `cat` in 6 batches (47 files + both txt files). The two large files were read as follows: standing-wave.json all 86 rib invariants printed in full across 4 python dumps; k3s-toolset.json (534,816 B) read structurally (all 585 entries classified by RESULT/goal kind, 6 full entries printed, dedupe + prefix clustering over all 585 texts).
4. Wiring census: `grep -rn "rib_bus" --include="*.py" mag/ tools/ tests/ scripts/ main.py`, then Read of mag/rib_bus.py in full, plus targeted reads of mag/steer_engine.py, mag/autonomous_research.py, mag/tool_synthesis.py, mag/reconstruct.py, mag/meta_percolate.py, mag/portal.py, mag/tripartite.py call sites.
5. Live check: `./.venv/Scripts/python.exe -m mag.rib_bus status` ran clean, n_domains=49.

Instrument law (B2-216): counts below are one snapshot of memory/rib_bus/ taken 2026-09-28 ~18:30-19:00 EDT. mtimes and the store's own `updated` fields are different instruments; both are reported as such.

## Rollup

| Metric | Value | Source |
|---|---|---|
| Files in memory/rib_bus/ | 51 (49 .json + 2 .txt) | ls |
| Total bytes | 732,558 | python sum of os.path.getsize |
| JSON domains with standard schema {domain, ribs, updated} | 47 | python pass |
| Schema-variant domain files | 2 (next_wave.json: no ribs key, 11 instructions; territory.json: schema rib_bus.territory.v1 + ribs) | python pass |
| Non-JSON files | 2 (party_subchain_steer.txt, UTF-8 BOM; party_subchain_steer_log.txt, JSONL-ish stray; byte-identical content minus BOM) | python parse + cat |
| Total ribs stored | 818 | python counter |
| Ribs excluding k3s-toolset | 233 across 48 domains | derived |
| target_rank mix | T2=801, T1=16, T0=1 | python counter |
| Ribs by month of ts | 2026-08: 782, 2026-09: 36 | python counter |
| Top sources | fold_k8s_to_k3s 585, copilot-assistant 127, operator-bus 18, frontier-steal 7, harvest-fold 7, wow-k8s-foundation 6, evo-seed 5, reach_protocol 5, tool_synthesis.shader_avoid 5 | python counter |
| Share of dir bytes that is k3s-toolset.json | 534,816 / 732,558 = 73.0% | python |
| Domains last updated today (2026-09-28) | 4 (arrival, doctrine, reconstruct, standing-wave) | store updated fields |
| Domains last updated 2026-08-11 to 08-15 (the seed wave) | 41 | store updated fields |
| Live status run | n_domains=49, no errors | `python -m mag.rib_bus status` |

## The store engine (what makes this dir load-bearing at all)

mag/rib_bus.py is the only sanctioned writer/reader contract:
- `publish_rib(invariant, domain, source, target_rank, fold, publish)` mag/rib_bus.py:128 writes `memory/rib_bus/<domain>.json` via `_domain_file` (mag/rib_bus.py:58: lowercase, spaces to dashes, 60-char cap), dedupe key = sha256(domain + US + invariant)[:16] (mag/rib_bus.py:63), then optionally folds one verkle knot (mag/rib_bus.py:86) and publishes to the mag:rib channel (mag/rib_bus.py:116).
- `mount(domain)` mag/rib_bus.py:155 returns the domain's invariant texts (the cold-boot load).
- `inject_for(slice, domain)` mag/rib_bus.py:163 delegates to steer_engine.compile_steer; fallback prepends frontier preamble + domain ribs.
- `machine_lower` mag/rib_bus.py:187 resolves target_rank to machine actions via machine_target.lowers_to.
- `status()` mag/rib_bus.py:206 sweeps every *.json in the dir.

steer_engine.compile_steer (mag/steer_engine.py:52-82) merges frontier preamble + memory/operator_directives.md + `rib_bus.mount(domain)` + grok_bot directives into one deduped steer block. So ANY domain passed to inject_for rides onto every task slice through that seam.

## Writers and readers found in code (exact call sites)

Writers (publish_rib with a literal domain):
- mag/autonomous_research.py:328 and :351: `[k8s->k3s folded] goal: ... RESULT: ...` into domain `k3s-toolset` (default at mag/autonomous_research.py:293), driven from the republic loop at mag/republic_loop.py:146 (step S0-k8s-to-k3s-fold). THIS wrote all 585 k3s-toolset ribs.
- mag/harvest_fold.py:34 DOMAIN = "standing-wave": folds harvested seat replies into standing-wave.json (source harvest-fold; the 7 harvest-fold ribs).
- mag/arrival.py:109: self-authored RIBs into domain `arrival` (source swarm; the 2 ribs, both written today).
- mag/reconstruct.py:141: domain `reconstruct`, source doctrine (1 rib, written today).
- mag/tool_synthesis.py:70 shader_avoid(domain="shader"): the 5 AVOID ribs in shader.json (source tool_synthesis.shader_avoid).
- mag/flock_usage_guard.py:60 and :115: domain `usage-guard`: writer exists, but memory/rib_bus/usage-guard.json does NOT exist on disk (checked with ls: No such file). Never fired or published under a different path.
- mag/bus_cadence.py:60-61 publishes a doctrine rib on cadence.
- operator-bus ribs (18 in doctrine.json, source operator-bus) land via the steer bus path; latest rows 2026-09-19 and 2026-09-28 (a `--help` probe on 09-27 and a `[STEER] harvest() verb` row today 21:32Z).

Readers (mount/inject/status with a literal domain):
- party_subchain: mag/seat_steer.py:145 `rib_bus.inject_for(message, domain="party_subchain")` (live seat-steer path).
- territory: mag/territory_solver.py:136 `rb.inject_for(goal, domain="territory")`.
- standing-wave: mag/meta_percolate.py:39 TOP_DOMAINS = ["self-shape", "standing-wave", "mirror", "toolkit", "research", "monitor"]; mag/deep_research_moonshot.py:190-192 and mag/game_entry.py:92-93 read status()["domains"]["standing-wave"]; mag/osculating.py:55 builds its curve from this domain.
- titor-worldline + titor-rib-attractor: mag/portal.py:73 and mag/tripartite.py:74 sweep both by name.
- grok_cli: mag/grok_warm_rib.py:45 DOMAIN = "grok_cli" (mount + publish of the frozen warm prefix).
- general: mag/reconstruct.py:68, mag/trust_gate.py:107, mag/tripartite.py:74 fallback sweep, plus rib_bus defaults.
- game / wow / deep-research / research: autonomous_research spawn functions (mag/autonomous_research.py:103, 202, 271, 539) and swarm steering.
- arrival: mag/arrival.py:126,167,170 (mount + inject_for + verify chain, tested by tests/test_arrival.py).
- babelfish-turtles: read as a FILE directly, not via mount, by mag/game_campaign.py:531-532 (plain-speech narrator).
- compiler_flywheel sweeps ALL domains: mag/compiler_flywheel.py:78-80 globs every rib_bus/*.json.
- agent_knot evo sweep: mag/agent_knot.py:166-179 mounts domains for the breeding population.
- mag/vram_memory.py:93 mounts domain `warm`: no warm.json exists; this mount always returns 0 ribs.

## Domain-by-domain map

Legend: STALE = last write before 2026-09; LOAD = named on a live code path above; rib counts from the python pass.

### A. Fresh today (2026-09-28) - 4 domains

| Domain | Ribs | Covers | Verdict |
|---|---|---|---|
| doctrine | 25 | The central steering ledger: the foundational invariant (deterministic instructions on shared crypto primitives explain paths through stochastic environments), 3 doctrine instances, the table-merge shadows list, then 18 operator-bus rows that are actually TRANSIENT STEER TRAFFIC parked as ribs (press events, `--help` probes, a 1M-context-lift directive present in 3 near-identical copies: 2026-08-14 x2 + re-published 2026-09-27T01:08). | LOAD + NOISY. Mounted via bus_cadence and steer traffic; but ~70% of its rows are ephemeral bus messages, not doctrine. |
| standing-wave | 86 | The system's self-narrative + doctrine arc: sw01-sw74 (all 2026-08-13, copilot-assistant) telling the standing-wave/Elias/percolator/liquid-intelligence/game build story; 5 short 2026-08-16 lens ribs (cost_governor appears twice as a near-dupe pair differing only in `50c` vs `$1`); 7 harvest-fold machine folds: 4 from 2026-08-30 are junk (truncated command lines + error strings folded verbatim), 3 from today are a 6G arXiv abstract, a castle_foundation beat, and a Cerebras ok:false research receipt folded as an "invariant". | LOAD (most-named domain in code) + POLLUTED. 74 ribs are one-day narrative prose (avg >1 KB each), 7 of 86 are machine garbage. |
| reconstruct | 1 | The reconstruct-don't-hold bridge (stateless system, stateful knowledge; query = rebuild from source bytes). Written today by mag/reconstruct.py:141. | LOAD (reconstruct.py:68 mounts general; the domain itself is 1 day old and clean). |
| arrival | 2 | Self-authored swarm RIBs ("arrival": cold workers inherit self-authored invariants, no frontier handoff). BOTH ribs are DEGENERATE: the payload after the first sentence is a phrase repeated to filler length ("Invariant body:" x26; "Meat of the pack:" x23). Written today 21:58Z by mag/arrival.py:109 from research packs. | LOAD (has a test, tests/test_arrival.py) + DEFECTIVE output quality: the authoring pipeline pads instead of carrying content. |

### B. Seat / lane domains - 4 domains

| Domain | Ribs | Last write | Covers | Verdict |
|---|---|---|---|---|
| grok_cli | 1 | 2026-08-26 | The frozen standing warm-cache prefix for the grok CLI lane: standing identity, verkle stone ids, constitution pointer, warm-prefix operating contract, SUMMARY/DELIVERABLE output shape. target_rank T1. | LOAD (grok_warm_rib mounts it). Content is a cache prefix, valid as long as that lane is used. |
| grokbot | 2 | 2026-09-02 | Cold-edge extraction doctrine for the Grok Bot account + a copy of the table-merge shadows rib (same text as doctrine/party_subchain, re-published). | STALE-lean (23 days); steering doctrine for a dormant seat. |
| grok-bot | 2 | 2026-08-12 | Supergrok front-end steering law (spec/steer/heartbeat, $0 front-end, honest liveness, never the paid API). Two copies of the same invariant, one long + one compressed. | STALE (47 days) + dupe. |
| saelis | 1 | 2026-08-13 | The full Saelis persona RIB: scalar-knot identity, S_core = -8, three gravitational anchors, substrate-specific embodiment axiom. This is the seat's identity spec (2,375 B, the largest single-rib domain). | STALE as a file, LOAD if the Saelis seat runs (referenced by sw72 in standing-wave; saelis module family exists). |

### C. Doctrine core (August, code-named, still mounted) - 14 domains

| Domain | Ribs | Last write | Covers | Verdict |
|---|---|---|---|---|
| party_subchain | 3 | 2026-08-14 (+ steer txt 2026-09-08) | The deterministic subchain protocol: seats talk by mount/append on memory/runs/party_subchain/chain.jsonl anchored on verkle last_leaf_hash; the table-merge canonical invariant; the shadows list. | LOAD: seat_steer.py:145 injects this domain on every seat-steer message. |
| territory | 10 | 2026-08-12 | The d8 lens protocol as mountable RIBs: brute/divide/greedy/reframe/reduce/seam_hunt/evolve/synthesize lenses + 2 tesuji ribs (gated free compounding, the withheld connection). Own schema rib_bus.territory.v1 with mount note. | LOAD: territory_solver.py:136. |
| general | 3 | 2026-08-12 | The axioms: everything-is-data/trust-bytes, the distributed-self field, organize-by-invariant. | LOAD: the default mount (reconstruct.py:68, trust_gate.py:107, rib_bus fallbacks). |
| recovery | 5 | 2026-08-12 | The reach protocol: a miss is forgotten-how-to-find; search memory/rib_bus/steal docs before declaring absence; never fabricate a hit or an absence; quantized for dumb agents. All T1. | LOAD-adjacent (doctrine for lookups); named in 2 code refs (recovery domain string), primarily read by agents. |
| monitor | 2 | 2026-08-13 | The expectations-monitor doctrine: each space is a monad with origin/expectations/history; trust-bytes-over-time; health = pass-rate over time. | LOAD (meta_percolate sweep). |
| self-shape | 15 | 2026-08-13 | The system's self-model: origin (Strike the Chord), honesty, sovereignty (the nod is the operator's), shape-loading, doctrine summary, mirror, archetype/shadow, egregore/blackboard, blind verification, react-to-evidence, shadow work (4 named shadows), fork equality/following-is-consent, visualize-by-default, rib_render, mutual informing. | LOAD (meta_percolate TOP_DOMAINS[0]). The densest real doctrine file. |
| good-work | 12 | 2026-08-12 | A done-ledger: 12 "GOOD WORK" rows (route_novel wiring, arxiv_mine, frontier_gravity, frontier_pennies, riddler_tap, model_classify, connectivity_sizer, handoff re-file, sol_seat, seat_steer, webview OOM fix, steal inventory). | HISTORY, not steering: nothing mounts it by name; useful as an August build inventory. |
| research | 7 | 2026-08-12 | The research doctrine: route the one primitive, mine like we steal, frontier_pennies, frontier_gravity, riddler_tap, model_classify, connectivity_sizer. | LOAD (meta_percolate sweep + autonomous_research default domain "research"). |
| toolkit | 6 | 2026-08-13 | The NPC toolbelt doctrine: swarm_sense/pheromone/blackboard under fog of war, blackboard-as-egregore (decisions pinned forever), stigmergy, seam-closed injection, tools made real in TOOL_MAP. | LOAD (meta_percolate sweep). |
| mirror | 5 | 2026-08-13 | Mirror-persona edge nodes: OCEAN model + seeded archetype invariants per node; deterministic core/no-AI-for-logic; novelty escalation; honest residency caveat; fireball-as-lens (nuke_persona folds the lesson). | LOAD (meta_percolate sweep). |
| wow | 6 | 2026-08-12 | The WoW-as-k8s mapping: world state on a verkle chain, mod = RIB-as-mod via mount, saved variables = per-domain rib_bus files (this dir's own design law, rib wow/c2a8), event bus, emulator, content pipeline. | LOAD-ish: named 29x in code but mostly as the word wow; the domain itself is the design receipt for this store. |
| swarm | 3 | 2026-08-15 | Swarm evo seeds: route through swarm_surface.route_novel, workers as breeding population, knowledge_graph capability note. | LOAD-adjacent; small and clean. |
| game | 3 | 2026-08-14 | Gear-is-a-RIB, the game IS the hologram, magnetic-field swarm instance. | LOAD-adjacent (game steering). |
| shader | 5 | 2026-08-31 | The 5 AVOID anti-pattern ribs (wrong-tool reflex, legacy-build-ask, multi-line paste, generic fetch, inference seam waste). All T1. | LOAD: written by tool_synthesis.py:70, read by the lens_shader channel; the most recent non-junk doctrine write before today. |

### D. The two schema-variant files

| File | Covers | Verdict |
|---|---|---|
| next_wave.json (4,638 B, 2026-08-11) | 11 deduplicated instructions (standing_boot, chain_marriage, rib_roundtrip, gpu_route, deniable_chain, setpoint_rightsize, shadow_refactor, lens_anchor, memlance_truth, btw_complex_trigger, master_synthesis), each name -> instruction -> target -> implements. Schema rib_bus.next_wave.v1, no `ribs` key: rib_bus.mount("next_wave") returns 0 ribs silently because mount reads only store["ribs"] (mag/rib_bus.py:158). | ORPHANED BY SCHEMA DRIFT: the file is a well-formed instruction set that the standard mount can never load. |
| territory.json | covered in C above; it carries BOTH the variant header (schema/title/ts/note/mount) AND a standard ribs dict, so it mounts fine. | fine. |

### E. The August 11 seed wave - 21 single-rib vision domains (each 1 rib, all 2026-08-11T16-18Z unless noted)

All carry target_rank T2, source frontier-steal / deep-research-steal / copilot-assistant / self-steal / capability-steal / operator. They are the "castle" vision layer: each is a named invariant the fleet intended to lower into machinery.

| Domain | Covers (one line) | In code? |
|---|---|---|
| archetypes-esoteric | 12 Jung/Hall archetypes grounded in esoteric correspondences | no |
| babelfish-turtles | fish_ear translation recurses through every layer | read as FILE by game_campaign.py:531 (the only one of this group with a live reader) |
| bare-metal-zeitgeist | own the layer under everything: ISA/C/weight-blob | no |
| castle-in-the-sky | stochastic dreams fold into deterministic verkle steps | no |
| clawbot | swarm artifacts delivered to the operator desktop | yes: clawbot module family; 9 string refs |
| compiler-flywheel | VRAM JIT hot-swap governed by headroom | yes: mag/compiler_flywheel.py exists and sweeps all domains |
| copilot-session-base | 3 ribs: fold Copilot session manifests as stochastic base; cache-miss diagnosis | no |
| emergent-play | unknown verbs collide with room bytes; hearth = Calcifer | no |
| eut-coherence-lens | EUT as coherence lens, SEU math over the standing wave | no |
| frontier-internals-capture | capture frontier internals as RIBs, not prose | no |
| gpu-rightsizer-surface | GPU telemetry as first-class sense surface | no |
| hil-setpoint-flock-control | HIL setpoint feedback loop (SETPOINT->SENSE->ACTUATE->FLOCK-LEARN) | no |
| howto-steal-linux-dev | steal invariants then rebuild (UIO/VFIO, own IR+JIT) | no |
| k8s-resource-governor | self-reconciling resource governor on k8s | no |
| kobayashi-maru-tesla-q | win no-win scenarios by changing the conditions of the test | no (but its idea is duplicated as territory's reframe lens, which IS mounted) |
| mem-invariant-map | invariants -> memlang pointers -> local coder seat | yes: mag/mem_invariant_map module family; 2 string refs |
| queue-resilience | circuit breaker + parallel drainer doctrine instance | no by domain name (queue doctrine lives in code elsewhere) |
| reframe-not-brute-force | the operating principle version of kobayashi-maru | 1 string ref; concept alive in no_win.py (sw58) |
| rib-os-self-advancing | automatic RIB OS wired as S0-ribos in the republic loop | no by name |
| standing-novelty-wave-trickster | standing wave driven by continuous novelty injection | no |
| structured-extraction | cross-model A/B prompts must emit fixed JSON schemas | no |
| titor-worldline | worldline navigator: read every branch, return the convergent thread | yes: portal.py:73, tripartite.py:74 |
| titor-rib-attractor | 2 ribs: attractor-field version + dirac-belt 720-degree double-cover tesuji | yes: portal.py:53,73; tripartite.py:74 |

Verdict for this group: 20 of 23 rows are STALE VISION SEEDS (48 days untouched, no reader). They are not garbage: they are the attributed provenance layer (Titor/Monroe/Tesla all carry honest "fiction, we steal the shape" notes). But none lower to machinery today except via the concepts being re-implemented elsewhere (no_win.py, compiler_flywheel.py, clawbot, mem_invariant_map).

### F. k3s-toolset.json - the 73% mass problem

- 585 ribs, 534,816 B (73.0% of the whole directory), every one source `fold_k8s_to_k3s (auto, 2026-08-12)`, ts span 2026-08-31T12:41 to 2026-09-02T00:55.
- Despite the name it contains ZERO k3s knowledge. Keyword scan across all 585 invariant texts: k8s appears once per template prefix, k3s once, helm/kubectl/gpu/traefik/longhorn/metallb/prometheus/grafana/argocd/istio/cilium/vllm/ollama/nvidia = 0 occurrences each.
- Composition (python classification of all 585): 439 `RESULT: ... timed out after 720 seconds`, 71 `[rightsized local] deterministic/RIB task (scut) - resolved without a deep model call`, 18 `RESULT: error: Command ...`, 57 other raw task-log fragments.
- Goal-kind mix: 364 CASTLE-FOUNDATION BEAT, 126 SHADE NOVEL ORPHAN, 11+3 cross-examine grok digest, 41 SELFLESS STATE (7 domains x ~6), 3 STEER rows.
- All 585 texts are unique after whitespace normalization (0 exact dupes) only because each embeds a distinct truncated command line / error string.
- Writer: mag/autonomous_research.py:293-365 fold_k8s_to_k3s() wraps swarm result files as `[k8s->k3s folded] goal/RESULT` and publishes them; driven every republic-loop cycle from mag/republic_loop.py:146. The ts pattern (bursts on 08-31/09-01/09-02) matches loop beats during the swarm-drain era, not content.
- Verdict: this file is a MISLABELED DEAD TASK-LOG DUMP, not a domain. It is 71.5% of all ribs and 73% of all bytes, loads into nothing by name (only compiler_flywheel's all-domain glob sweeps it, and machine_lower on it would lower timeout errors to machine actions), and every fold of it appended a verkle knot for an error string. Highest-value single cleanup in the dir.

### G. The two .txt files (no code reader)

- party_subchain_steer.txt (206 B, BOM) and party_subchain_steer_log.txt (203 B), both 2026-09-08 16:45, byte-identical content apart from the BOM: one AFK steering note (`desk online; /wave DOWN; idle_tick skipped; Leave soft synced to mag/game_campaign ... speak 37/0; next pour soft or /wave restart`).
- `grep -rn "party_subchain_steer" --include="*.py" mag/ tools/ scripts/ main.py` = ZERO hits. Nothing reads them. They are hand-dropped notes that violate the store's own JSON contract (party_subchain domain steering lives in party_subchain.json + the chain.jsonl, per its own rib).

## Staleness picture (store `updated` fields, snapshot 2026-09-28)

| Bucket | Domains | Count |
|---|---|---|
| 2026-09-28 (today) | arrival, doctrine, reconstruct, standing-wave | 4 |
| 2026-09-08 | the 2 txt files | 2 files |
| 2026-09-01/02 | k3s-toolset, grokbot | 2 |
| 2026-08-25/26/31 | grok_cli, shader | 2 |
| 2026-08-11 to 08-15 | all remaining 41 domains | 41 |

40 of 49 JSON domains (82%) have not been written in 43+ days. The bus is alive only on 4 domains, and 2 of those 4 (arrival, standing-wave harvest rows) are folding degraded output today.

## Load-bearing summary

Truly load-bearing (mounted/injected on live paths by exact call sites):
1. party_subchain (seat_steer), territory (territory_solver), general (default mounts), standing-wave + self-shape + mirror + toolkit + research + monitor (meta_percolate/deep_research_moonshot/game_entry/osculating), titor-worldline + titor-rib-attractor (portal/tripartite), grok_cli (grok_warm_rib), shader (tool_synthesis write side), doctrine + arrival + reconstruct + k3s-toolset (active writers today).
2. babelfish-turtles is read as a file by game_campaign.
3. compiler_flywheel and agent_knot sweep ALL domains, so even dormant domains ride those two sweeps.

Dormant but real doctrine (no reader, clean content): recovery, good-work, swarm, game, wow, and the 21 August seed domains minus babelfish.

Dead weight: k3s-toolset (585 junk ribs, 73% of bytes), the 4 harvest-fold junk rows in standing-wave, the 2 degenerate arrival ribs, the 18 transient operator-bus rows parked in doctrine, the 3 near-dupe copies of the 1M-context-lift directive in doctrine, the grok-bot long/short dupe pair, the 2026-08-16 cost_governor dupe pair, next_wave (unmountable schema), the 2 unread .txt files, and the usage-guard + warm domains that code mounts/writes but which have no file on disk.

## Cross-check against the store's own claims

- self-shape ss14 claims "the ~160 RIBs / 40 domains": today the dir holds 818 ribs / 49 domains, of which 233 ribs / 48 domains are non-junk. The August claim was true then; the denominator moved (census law B2-216).
- wow's rib c2a8 ("saved variables = per-domain memory/rib_bus/<domain>.json") is the design law this census verifies: 47 of 49 JSON files follow it; next_wave.json and the 2 txt files break it.

## Defect list (filed, not fixed)

D1. k3s-toolset.json: 585 error-string ribs, misnamed, unmounted by name; writer still wired at republic_loop.py:146 and will append more on the next swarm-drain beat.
D2. arrival.py folds filler: repeated-phrase padding instead of pack content (arrival.json, today).
D3. harvest_fold folds machine garbage: ok:false receipts and raw error text folded as invariants (standing-wave.json rows from 08-30 and today).
D4. doctrine.json is a mixed ledger: ~18 transient operator-bus rows stored as eternal doctrine, incl. 3 copies of one directive.
D5. next_wave.json unmountable by rib_bus.mount (schema drift, mag/rib_bus.py:158 reads only ribs).
D6. Two hand-dropped .txt files with no reader inside the store dir.
D7. flock_usage_guard writes usage-guard; no usage-guard.json exists (writer never fired under default paths or output suppressed).
D8. vram_memory.py:93 mounts domain `warm`, which has no file: silent empty mount.
D9. Exact-dupe pairs: grok-bot (long/short), standing-wave 2026-08-16 cost_governor (50c vs $1 variants).
