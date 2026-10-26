# ESTATE BOARD - 2026-10-20 (CANON FRONT PAGE)

Every seat reads this first. One row per issue: duplicates are folded into a single canonical row. Written 2026-10-20 ~1:50 PM EDT by Grok Bot (executor), read-only except the one config pointer fix listed in (b).
Tiers: **V** = verified on disk / live today · **R** = older report (cited) · **I** = inference.
Sources: OCTOBER_MAP_GAP_20261020.md, STEAL_ESTATE_HARDENING_20261019.md, FISH_TANK_REMEDIATE_20261019.md, memory/attention.md, task logs read today. Commit batches: COMMIT_PLAN_20261020.md.

## (a) NEEDS NACHO - decisions + admin steps
| # | Ask (one line) | Exact command / choice | Tier |
|---|---|---|---|
| A1 | Fix the tip witness: 0 publishes since 09-30, 403 every day | Re-scope the GitHub PAT used by tools/tip_witness.py: fine-grained -> Account permissions -> **Gists: Read and write** (or classic PAT + `gist`). Then run `powershell -ExecutionPolicy Bypass -File scripts\tip_witness_daily.ps1` | V |
| A2 | Run the host lockdown (portproxy 8765, sshd tailnet-only, block LAN 8080/11434) | Elevated PowerShell: `powershell -ExecutionPolicy Bypass -File scripts\host_lockdown_fish_tank_20261019.ps1`. Then re-enable `127.0.0.1:8765:8765` in docker-compose.yml (parked 10-19) and run `docker compose up -d mag` **only when you choose** (that recreates mag-sovereign) | V |
| A3 | Close chain-folder write access + the etfag task | Elevated: `icacls memory\biography /remove:g *S-1-5-21-...` for CodexSandboxUsers + 5 SIDs (or regrant RX). Decide on AdjudicationBus: confirm it's yours, move it into the repo, or `Disable-ScheduledTask AdjudicationBus` | V |
| A4 | Choose an off-site backup target | Pick one: (1) another tailnet node over sftp, (2) USB drive, (3) B2. Then `scripts\backup_offsite.ps1 -Repository <target> -Verify` and keep the passphrase off-machine | V |
| A5 | Binary-tree v2: ship or park, plus a rename | Choose: **ship-as-verifier** (commit mag/bintree_v2.py + tests, verifier only) or **park** (leave untracked; note in the spec). Rename either way: live `chain_mode: v2` -> "append-only (v1.5)" or the bintree -> "chain v3/bintree" | V |
| A6 | GSTD PR #1: ping or withdraw | Open since 10-12, 22 commits, 0 comments, last update 10-15. Choose: ping the gstdcoin maintainers / close and offer as a disclosure / leave it. Also confirm whether the v8 cutover (10-14) stands against the 10-13 foundations ruling | V |
| A7 | Restore signing + prefix reseal | Restore 10-15 is UNSIGNED; Ratchet prefix-seal FAILs by design (n=12016 expected ab595c33). Choose: sign with seed_seal Ed25519 + deliberate re-seal, or leave red (then Estate Ratchet stays red daily) | V |
| A8 | Telegram token | Parked since >=10-14 on a revoked bot token. Mint a new token via BotFather and set it in the Hermes gateway config (you, not a seat), or rule Telegram retired | R |
| A9 | grokbot_counts_as_non_glm | `configs/seat_allowlist.json` quorum flag (default false; mag/proposals.py L285). Choose true (Grok Bot approvals count as non-GLM for quorum) or keep false | V |
| A10 | gstd-node :8080: rebind vs block | Compose files for gstd-node are gone. Choose: recreate it with `-p 127.0.0.1:8080:8080` (it will lose LAN peers), or keep the firewall block from A2. Also confirm gstd-node still reaches Ollama after the 10-19 loopback change (see W3) | V |
| A11 | Commit go-ahead | Approve COMMIT_PLAN_20261020.md batch by batch. Core organs (mag/leases.py, fleet_report.py, seat_handshake.py, proposals.py, ratchet.py) are **untracked**, so a fresh checkout lacks them | V |
| A12 | Pagefile balloon (63.95 GB) | A reboot returns it, or set a fixed-size pagefile (admin) | V |

## (b) A SEAT CAN DO IT NOW
### Red task triage (task results read 2026-10-20; one log read each)
| Task | Last run | Result | Log says | Class | Smallest fix |
|---|---|---|---|---|---|
| MagLongrunnerPatrolDaily | 10-20 08:45 | 1 | `No module named 'tools'` every day 10-17..10-20 (script runs `-m tools.longrunner_patrol` without cd to repo root) | **fix** | add `Set-Location $Root` before L16 in scripts/longrunner_patrol_daily.ps1 |
| MagHermesBurn247 | 10-20 13:36 | 0x800710E0 | Overlap refused (IgnoreNew, 72h limit); last real run 10-19: `FAIL NIGHT_ROTATION_20261019: KeyError('contract')`, 1 of 12 asks failed | **fix** | add the missing `contract` field to the NIGHT_ROTATION ask (or default it in tools/hermes_burn.py) |
| MagProbeCadence | 10-20 13:31 | 0x800710E0 | Beats ending exit=0; the code is overlap refusal only | **fine (benign)** | none; optionally document. Log is UTF-16 (mixed encoding) |
| MagCensusPatrolDaily | 10-20 08:30 | 1 | Findings: 5 unhealthy tasks + 2 fossil WARN (jev trail 740h, memory/improve/SEATS.md 381h) | **fix (findings)** | recompile SEATS.md; tombstone the jev trail |
| MagGapSentinelDaily | 10-20 08:15 | 1 | GROWTH: local_sovereign_agent +13.8 GiB/day (10-18->10-19) | **fix (finding)** | identify the 13.8 GiB writer (likely knots_attic / 838-row supersede + backups); W-row below |
| MagEstateSmithDaily | 10-20 09:05 | 1 | Alert: pagefile 63.95 GB > 40 GB | **blocked on Nacho** (A12) | reboot or fixed pagefile |
| Estate Ratchet | 10-20 09:45 | 1 | Ratchet debts (e.g. workflow_gate.py +84 lines) + PREFIX-SEAL FAIL (expected red) | **fix + blocked** | seat: accept/re-audit debts by name; Nacho: A7 |
| Estate KeyAudit | 10-20 09:57 | 1 | `mag.key_law --audit` exits 1 on any orphan/empty-critical key name (not opened; names-only tool) | **blocked on Nacho** | run the audit view in a seat (names only), then Nacho fills or retires the named keys |
| MagTipWitnessDaily | 10-20 09:30 | 2 | gist 403 | **blocked on Nacho** (A1) | - |
| MagDiskSmithDaily | 10-20 08:50 | 0x41306 | Terminated by the 30 min time limit (last prune row 10-18) | **fix** | raise ExecutionTimeLimit to PT2H, or scope the scan roots |
| MagLeaveProtocolDaily | 10-20 08:12 | still running (267009); prior 1 | mates.yaml named a missing tools/leave_protocol.py | **fixed (pointer)** | applied: see below. Re-check tomorrow's result |
| AdjudicationBus | 10-20 | 0 | runs from the etfag profile | **blocked on Nacho** (A3) | - |

**Config fix applied (reversible):** configs/mates.yaml L2 pointer `tools/leave_protocol.py` -> `tools/leave_dispatcher.py` (comment line; YAML parses). Backup: `configs/mates.yaml.bak_board_20261020`.
**Self-correction:** my 10-19 fish-tank patch had rewritten main.py CRLF->LF (a 10,988-line false diff). Restored CRLF today; `git diff --stat main.py` = 6 lines. Still LF-vs-CRLF in the index (not mine): mag/verkle_knot.py (2,770 false lines; the real change is 236). Fix before commit: renormalize EOL.

### Other seat work
- S1 Make RELIEF/boot read fleet notices and ACK them (only bob ACKs; N-20261019 has 0 ACKs) (V)
- S2 Test one gstd-node inference against loopback Ollama (W3) (I)
- S3 Build the chain_guard cure (see knots_attic 271,993 files; stale marker 09-26) once Nacho says GO (A7-adjacent) (V via attention.md)
- S4 Scheduled chain verify: call verify_verkle_full.py at the start of MagChainBackupDaily; on fail -> NOTICE (V gap)
- S5 Egress first-seen notice via MagProbeCadence (hardening #6) (I)
- S6 Pin deps (requirements.txt 18/18 unpinned; `opencode@latest`) (V)
- S7 Regenerate watch/LIBRARY/INDEX catalog (librarian last ran 10-17) (V)

## (c) WATCHING (canonical rows; duplicates folded)
| # | Canonical row | History folded in | Now | Tier |
|---|---|---|---|---|
| W1 | **8765 portproxy ghost** (0.0.0.0:8765 -> 127.0.0.1:8765, iphlpsvc) | "cured" 10-05; re-found 10-17 (self-replication steal), 10-19 (fish tank + compose park), 10-20 (night shift 8fbe72bbc). Owner tasks MagLabKit8765/MagPrivateOffice8765 both disabled = orphan rule | Still armed. Only A2 closes it; the dashboard port is parked in compose until then | V |
| W2 | **Ollama bind** | 10-09 set 0.0.0.0 for gstd-desktop's garden models; 10-17 flagged it as the worst fish tank; 10-19 set it to 127.0.0.1 (user env OLLAMA_HOST). Container -> host.docker.internal verified OK | Canon: **loopback**. Any seat needing LAN Ollama must take an `expose:lan` lease, not flip the env | V |
| W3 | gstd-node <-> Ollama after loopback | 10-19 change | Untested (S2) | I |
| W4 | Repo growth 13.8 GiB/day | GapSentinel 10-20 | Watch; find the writer | V |
| W5 | Chain honest again (13,137 rows refold, tip matches) | archaeologist cycle 10 (attention.md 10-20) | Keep honest; uncommitted fixes | V |
| W6 | Nous Beam free week 10-20..10-27 | 8a480ea6c | Burns down 10-27 | V |
| W7 | SAME BOOK program falsifier: stable ranking by 10-27 | c3cd7d6f0 | Due 10-27 | V |

## (d) DONE IN OCTOBER (short)
- Chain restore 12,016 rows (10-15) + test write fence + backup pin (a2ae802a6, 274a6b020) (V)
- Chain v2 append-only flip (10-17) + 5 append-only fixes applied 10-19 (uncommitted) (V)
- GSTD: audit, multi-node rail/drain/beacon, v8 cutover, soak 30/34 settled, PR #1 opened (V/R)
- Seats: grokbot-ghost, grokbot-mag, nacho enrolled (10-18) (V)
- Fleet notices channel (10-17); OpenCode notices ACK'd by bob (V)
- Fish tank: Ollama loopback, expose:lan lease, display_gate, cast --lan 8767, platform_kill --lan-expired, 18 tests (10-19) (V)
- Backup brain orchestration + daily chain backups green (V)
- Steals: Harness2, Telegram bus, roster swap, seats-as-harness, fish tank, estate hardening (V)


## Update 2026-10-20 evening - priority shift
- **Godot / game distribution: BACK-BURNERED** (per Nacho, 10-20).
- **P3 distribution = Hermes plugin.** v0 skeleton at watch\inbox\hermes_plugin_v0\ (native mag-estate: 4 read-only tools + 2 skills, validate/doctor PASS; portable mag-estate-door: estate-only MCP door, validate PASS). Details: STEAL_HERMES_PLUGIN_20261020.md. Honest read: SEAT_HONEST_READ_20261020.md.
- Blocker unchanged: untracked core organs + 281 modified + push hold (COMMIT_PLAN_20261020.md). Next: commit/push -> license/publish decision -> one external installer (P6).
