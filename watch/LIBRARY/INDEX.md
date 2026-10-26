# WATCH LIBRARY: INDEX (read this first)

## START HERE (canon, 2026-10-20)
- **[ESTATE_BOARD_20261020.md](ESTATE_BOARD_20261020.md)**: the front page. Needs Nacho / seat work + red-task triage / watching / October done
- [COMMIT_PLAN_20261020.md](COMMIT_PLAN_20261020.md): 9 ordered commit batches for the uncommitted October work (proposal; nothing committed)
- [OCTOBER_MAP_GAP_20261020.md](OCTOBER_MAP_GAP_20261020.md): the Oct 1-20 timeline + gap analysis
- Fleet NOTICE N-20261020-estate-board-canon: ACK it

Generated 2026-10-17 15:35 ET by `scripts/inbox_librarian.py`. The library is a **catalog**, not a move: every file stays at its path in `watch/inbox/`.
Cards live in [`catalog.jsonl`](catalog.jsonl) (one JSON card per file: path, size, effective_date, shelf, tier, rule or confidence, summary, family, supersedes, latest, needs_review, verified).

## Shelves

| shelf | what goes here | files | size | last 7 days | LATEST |
|---|---|---|---|---|---|
| **α CHAIN** | memory chain: chain restore, v2 bintree, verkle/merkle knots, biography, seals, rib vaults | 203 | 24.0 MB | 12 (0.1 MB) | [α_CHAIN/LATEST.md](α_CHAIN/LATEST.md) |
| **β GSTD** | GSTD/TON settlement: contracts, bridge, soak, A2A, gstdcoin mapping, money/revenue pages | 247 | 71.5 MB | 141 (0.4 MB) | [β_GSTD/LATEST.md](β_GSTD/LATEST.md) |
| **γ LANES** | model/provider lanes: free tiers, Hermes burn, burn waves, OpenRouter/DeepSeek/GLM/Gemini/Grok, quotas, width, gopher | 4,603 | 161.1 MB | 727 (71.7 MB) | [γ_LANES/LATEST.md](γ_LANES/LATEST.md) |
| **δ BOB** | bob + Antigravity primary-seat handoff and the work it spawned (asks, task bank, oracle hunt, ractor resolutions) | 31 | 0.2 MB | 16 (0.1 MB) | [δ_BOB/LATEST.md](δ_BOB/LATEST.md) |
| **ε DOCTRINE** | doctrine, laws, canon, constitution, Lilith, X intel/link drops, parables, essays, posts, research reading | 403 | 29.0 MB | 148 (17.3 MB) | [ε_DOCTRINE/LATEST.md](ε_DOCTRINE/LATEST.md) |
| **ζ OPS** | operations: patrols, receipts, triage, audits, census, backups, secret gate, mates protocol, tool state (.mimosa), logs | 2,668 | 2.21 GB | 419 (291.6 MB) | [ζ_OPS/LATEST.md](ζ_OPS/LATEST.md) |
| **ω ARCHIVE** | cold: effective date >30 days, media exports, dormant campaign folders (nothing in 14 days), frontier_olm day folders | 12,134 | 4.69 GB | 161 (6.5 MB) | [ω_ARCHIVE/LATEST.md](ω_ARCHIVE/LATEST.md) |
| **χ UNSORTED** | rules and model could not place it confidently (needs_review) | 3,245 | 128.3 MB | 266 (52.3 MB) | [χ_UNSORTED/LATEST.md](χ_UNSORTED/LATEST.md) |

## Hot and cold

- Total: 23,534 files, 7.31 GB.
- Hot (effective date within 7 days): 1,890 files, 440.1 MB.
- Cold (older than 30 days): 1,161 files, 140.7 MB.
- Archive shelf ω (cold + media exports + dormant folders): 12,134 files, 4.69 GB. See [ARCHIVE_PROPOSAL.md](ARCHIVE_PROPOSAL.md).
- Tiers: 19,946 rule cards, 197 per-file model cards, 2,995 folder-model cards, 396 pending (model budget ran out).
- needs_review: 1,969. Verified sample: 37 true / 23 false (method and accuracy: [VERIFICATION.md](VERIFICATION.md)).

## Resume / refresh

`python scripts\inbox_librarian.py --model-budget-min 30` continues where the last run stopped. It re-uses model_cache.jsonl, and it only sends files still marked tier `pending` plus new or changed files to the local model. Use `--no-model` for a rules-only refresh. Never schedule it while another seat is using Ollama heavily.

## Rule for new files (every seat)

1. **Name it with a shelf prefix**: `ALPHA_`/`CHAIN_`, `BETA_`/`GSTD_`, `GAMMA_`/`LANES_`, `DELTA_`/`BOB_`, `EPSILON_`/`DOCTRINE_`, `ZETA_`/`OPS_` (for example `CHAIN_V2_CATCHUP_20261018.md`). Keep the `YYYYMMDD` date in the name.
2. **Append one card** to `watch/LIBRARY/catalog.jsonl`, or just run `python scripts\inbox_librarian.py` (incremental: catalogs new or changed files, then refreshes every LATEST.md and this INDEX).
3. A repeating series (patrols, receipts, digests) keeps the same family name and a new date. The newest copy is marked `latest`, and older copies are reachable through `supersedes`.
4. Trust only cards with `verified: true` or tier `rule` for decisions. `needs_review` cards sit on χ until a human or seat re-shelves them.

## How tiers work

- **Tier 1 (rule, cheap decider):** a path-only rule for secret_gate_results/free_keys, then age >30d → ω, media/day-folder exports → ω, `.mimosa` tool state → ζ, filename-prefix rules, folder rules, dormant folder (nothing in 14d) → ω. The rule that fired is stored on the card.
- **Tier 2 (escalation, local Ollama only):** unplaced root files get path + first ~30 lines (key-like strings masked) → {shelf, summary, confidence}. Unmapped active folders are classified once per folder. Confidence < 0.6 → χ with needs_review.
- Sensitive files (.env, steps.jsonl, key/secret/token names, secret_gate_results/, free_keys*/) are classified by path only and never read.
- STEAL 2026-10-17: [STEAL_HARNESS2_20261017.md](STEAL_HARNESS2_20261017.md) - Google Harness2 (arXiv 2610.14224) mapped onto Mag organs; gaps = editor, paired probe, evidence-tied lessons.
- STEAL 2026-10-17: [STEAL_X_BRIEFS_20261017.md](STEAL_X_BRIEFS_20261017.md) - five X-post briefs verified; steals = anytime-valid e-process adoption rule for Harness2 paired probes, evidence_tier enum for fleet_report; LUPI/book/Dense4D/Penrose = no build.
- STEAL 2026-10-17: [STEAL_HANDOFF_CONTRACT_20261017.md](STEAL_HANDOFF_CONTRACT_20261017.md) - "Transmutable Link Dumps" handoff doc verified (7/7 sources real; tweprint rules misquoted); steals = verbatim uncapped HARD CONSTRAINTS block + constraints_sha on RELIEF (blocker-survives-compression test), coverage manifest + owned next_actions on RELIEF, claims merged with evidence_tier, X draft lint; url2llm/markurl = no.
- STEAL 2026-10-17: [STEAL_SELF_REPLICATION_DEFENSE_20261017.md](STEAL_SELF_REPLICATION_DEFENSE_20261017.md) - Anthropic Frontier Red Team self-replication brief verified (X/BC/TNW); defensive Mag map = wild Ollama/SSH/8765 portproxy + bob SSH/ADB organs + handshake off; steals = fleet kill on NOTICE/lab_ctl/revoked, bind-audit test, revocation drill.
- STEAL 2026-10-17: [STEAL_NOUS_FLEET_20261017.md](STEAL_NOUS_FLEET_20261017.md) - Anthropic shard pattern self-stealed as owner Nous army: true Rokus = COP/display only (not inference); reuse warm MCP + seat handshake + pheromones + fleet kill; keep brain on Ollama/GLM mates; PoC = display seats + COP JSON.

- STEAL 2026-10-17: [STEAL_NOUS_ARMY_SELFSTEAL_20261017.md](STEAL_NOUS_ARMY_SELFSTEAL_20261017.md) - corrective self-steal from Mag's own files + live ECP GET: 4 retail Rokus (Ultra 4660X .52/.149, Premiere+ 4630X .53, Stick 3500X .85), dev mode OFF on all, nothing of Mag runs on them; roku_channel never sideloaded and would exit/crash (empty Main, beacon schema drift); "Nous army" undefined in Mag files - Nous = Hermes/Nous-lane workers, Rokus = GSTD_DOGFOOD_PLAN display-fleet walls; corrects STEAL_NOUS_FLEET.
- STEAL 2026-10-17: [STEAL_SWARM_THIN_CLIENT_20261017.md](STEAL_SWARM_THIN_CLIENT_20261017.md) - operator design restated from Mag's own files: swarm = cheap phones/browser sessions (legs) + remote Nous/free-lane models (brain) + warm MCP surface (shared memory/attention), Rokus = walls; inventories built thin-client surfaces (cast_server /control /voice + remote_control, display.py, PWA, MagRemote, phonesalon, scrum_launch); gaps = no browser-reachable warm door, cast_server 8766 clash, no phone seat class; next build = warm proxy + swarm board on cast_server; corrects local-compute framing of STEAL_NOUS_FLEET/ARMY.
- STEAL 2026-10-17: [STEAL_TELEGRAM_FLEET_BUS_20261017.md](STEAL_TELEGRAM_FLEET_BUS_20261017.md) - Telegram fleet bus self-steal: the bridge already exists = Hermes gateway (Telegram platform configured, PARKED since >=10-14 on revoked token 8750925249; cron no_agent script->telegram delivery; hermes mcp serve messages_send/events_poll); mag/telegram_desk.py is an un-allowlisted public desk (not the bus); gstd_mirrors cited by SCRUM_SWARM not on disk; design = one private forum group (ALERTS/NOTICES/LEASES/PROPOSALS/REPORTS/TIP), token only in %LOCALAPPDATA%\hermes\.env TELEGRAM_BOT_TOKEN slot, smallest build = scripts/fleet_bus_digest.py run by a Hermes no_agent cron job; Grok Bot seats post indirectly via receipts.
- STEAL 2026-10-18: [STEAL_ROSTER_SWAP_20261018.md](STEAL_ROSTER_SWAP_20261018.md) - Roster Swap (AdventureNLearn Grok Bot template) self-stealed: YES-gated archive->verify->fold->label, never delete; Mag already has archive_guard manifest/verify/confirm, backup_chain verify, backup_brain inventory, auto_handoff, seat_allowlist revoke; gaps = app-side transcript export/routine list/rename + no seat-roster census; surprises: archive_guard PROTECTED regex refuses "transcript" at gate, no Grok Bot seats in seat_allowlist, mates.yaml cites missing tools/leave_protocol.py, backup_chain rmtree prunes; swap = keep Grok Bot + Mag, retire Research/New Bot/Archival/Refresh after manifest+verify (never gate); monthly read-only bloat check as a Grok Bot routine.
- STEAL 2026-10-18: [STEAL_SEATS_AS_HARNESS_20261018.md](STEAL_SEATS_AS_HARNESS_20261018.md) - "isn't this just our harness?" self-steal: yes in shape, no in wiring; every Grok Bot concept (seat, profile, memory, routine, skill, transcript, SendToAgent, retire) maps to a Mag organ (seat_allowlist/seat_handshake/seat_keygen/proposals/leases/fleet_report RELIEF/auto_handoff/leave_dispatcher/rib_bus) but zero grokbot rows exist and box agent-data is unread by Mag; smallest adapter = allowlist rows grokbot-<name> (SEAT_RE forbids colons) kind/model_family grokbot + per-seat key, retire = revoked:true + archive receipt, routines recorded not run (only box routine is disabled), skills = RIBs, YES = operator_seats approve; flags grok_bot.py name collision + non-GLM quorum power; corrects STEAL_ROSTER_SWAP (automation.json carries enabled).
- BUILD 2026-10-18: [GROKBOT_SEATS_ENROLLED_20261018.md](GROKBOT_SEATS_ENROLLED_20261018.md) - smallest adapter landed: grokbot-ghost (front_door, fp a0e5d4140c557bb5) + grokbot-mag (estate_brain, fp f2a3839e014cbf56) enrolled in configs/seat_allowlist.json (kind/model_family grokbot, keys host-side ~/.mag_seat); grokbot-research/newbot/archival/refreshbot = revoked keyless tombstones with archive receipt (tar sha256 283907df...); proposals.is_non_glm_seat counts grokbot as non-GLM only if quorum.grokbot_counts_as_non_glm (default false); SEAT_RE unchanged (already accepts hyphen ids); operator_seats left [] (Nacho needs own key); 74 tests pass; backups *.bak_grokseats_20261018.
- STEAL 2026-10-19: [STEAL_FISH_TANK_IOT_20261019.md](STEAL_FISH_TANK_IOT_20261019.md) - Darktrace 2017 casino fish tank (10GB to Finland via isolated-VPN IoT, caught by egress anomaly) self-stealed against Mag: fish tanks = wildcard binds 11434/22/8765 portproxy/8777 gstd_beacon/8080 gstd-node + untrusted Roku/phones on the same Private LAN; cast_guard already forbids LAN control (token, probe log, IP block); gaps = no host bind audit, beacon LAN-wide with no probe log, no egress notice, 8766 claimed by both mag-mcp and cast_server; smallest hang = untrusted-LAN-peer law + NOTICE rows + leased --lan exposure + platform_kill on expiry; live state Unproven (10-17 receipts only).
- BUILD 2026-10-19: [FISH_TANK_REMEDIATE_20261019.md](FISH_TANK_REMEDIATE_20261019.md) - Ollama->127.0.0.1 live; expose:lan lease + display_gate notices + platform_kill --lan-expired; cast --lan->8767; elevated host_lockdown script staged (portproxy 8765, sshd tailnet, 8080) -- 18 tests green
- STEAL 2026-10-19: [STEAL_ESTATE_HARDENING_20261019.md](STEAL_ESTATE_HARDENING_20261019.md) - assume-breach self-steal (read-only): tip witness dark since 10-18 (gist 403), all chain backups same disk + offsite unscheduled, memory/biography Modify ACL for CodexSandboxUsers + 5 SIDs, AdjudicationBus runs code from another profile (etfag), no scheduled chain verify, no egress notice, handshake off, factorio wildcard; NOTICE N-20261019-fish-tank-and-estate-hardening filed.
- MAP 2026-10-20: [OCTOBER_MAP_GAP_20261020.md](OCTOBER_MAP_GAP_20261020.md) - Oct 1-20 timeline from git (396 commits) + chain rows/day + receipts + crons + PR #1; gaps: tip witness 0 publishes ever, 253 tracked files uncommitted since 10-09, lockdown script not run, 10-14 red-cron set unchanged, offsite never started, bintree v2 untracked/name collision, PR #1 idle, notice ACKs bob-only, Ollama bind flipped by two seats.

- 2026-10-20 STEAL_HERMES_PLUGIN_20261020.md - Hermes plugin format (native + Agent Plugins v1), portable map, v0 at watch\inbox\hermes_plugin_v0 (tests pass)
- 2026-10-20 SEAT_HONEST_READ_20261020.md - verbatim seat honest read (supported/disputed/unproven; take = distribution P3)
