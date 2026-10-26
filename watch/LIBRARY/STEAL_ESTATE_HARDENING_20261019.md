# STEAL - Estate hardening, assume breach (self-steal) - 2026-10-19

prompt_genome_id: fleet/self_steal@v1 · SUBJECT: the whole estate on DESKTOP-7C70KSC · LENS: "infiltration is inevitable; the chain is why" (operator 2026-10-19)
Mode: READ-ONLY. No code changes, no git, no secrets read (key paths checked with icacls only), no paid calls, no mag-sovereign restart. Evidence collected 2026-10-19 17:20-17:35 EDT.

Tiers: **V** = verified on disk / live today · **R** = from an older report · **I** = inference.

## Verdict
The chain is tamper-evident only against a writer that doesn't hold the pen. Today the estate's *external* anchor (the gist tip witness) has been dark two days running. Every backup sits on the same C: disk, under a directory that sandbox accounts can Modify. So under assume-breach, a rewrite would currently go unnoticed: the backup faithfully copies the rewritten bytes, and nothing off-machine contradicts it. Leak-side, nothing watches outbound traffic, which is the casino signal. All fixes below hang on existing organs (tip_witness, backup_chain, verkle_knot._verify_chain_consistent, fleet_report notices, seat_handshake, cast_guard probe log, MagProbeCadence).

## Inventory (verified at bytes / live)
- scripts/tip_witness_daily.ps1 + logs: 2026-10-18 and 2026-10-19 09:30 `WITNESS: cannot verify: SCOPE - token cannot create gists (HTTP 403)`, exit 2 (MagTipWitnessDaily LastTaskResult=2)
- scripts/backup_chain.py: BACKUP_ROOT = memory/biography_backup (same repo, same disk), KEEP=7, prunes only verified-complete folders. Latest: biography_backup_20261017..19. MagChainBackupDaily 03:15 result=0
- scripts/backup_offsite.ps1: restic design, "Deliberately NOT scheduled". Only one fixed drive exists (C:, 299 GB free)
- icacls memory/biography: Modify (OI)(CI) for DESKTOP-7C70KSC\CodexSandboxUsers + 5 unresolved S-1-5-21-* SIDs (10 ACEs total)
- icacls ~/.mag_seat: SYSTEM, Administrators, foste only (good)
- Scheduled task AdjudicationBus (runs as foste, last 17:20 today, result 0) executes wscript + powershell -ExecutionPolicy Bypass from C:\Users\etfag\.zcode\workspace\default\ (a different user profile; Users/Everyone RX)
- No scheduled task invokes scripts/verify_verkle_full.py, verify_verkle_continuity.py or verify_knot_v2.py
- mag/seat_handshake.py L32 default off; scripts/container/mcp_tcp_bridge.py L165 default "off"; docker-compose.yml sets no MAG_SEAT_HANDSHAKE. MAG_SEAT_KEY_PATH is read in mag/seat_handshake.py, estate_bridge, scripts/seat_keygen.py, mcp_stdio_shim.py and proposals.py; whether the live seats export it is Unproven
- tests/conftest.py L112/L140: MAG_ALLOW_LIVE_WRITES fences tests only; no mag/ writer checks it
- Outbound (Get-NetTCPConnection, established, non-private): Hermes gateway (hermes python, `hermes_cli.main gateway run`) -> 162.159.133.234:443 (Discord/Cloudflare range); ZCode -> 47.246.22.228:443; com.docker.backend -> 3.64.42.180:443; Telegram; tailscaled; Grok Bot; chrome; steam; SearchApp
- Listeners (netstat): wildcard 22, 8080 (gstd-node), 8765 (portproxy), 27000/tcp + 34197/udp (cluster-factorio_0-1), 135/445/5357/7680 (Windows). Ollama is now 127.0.0.1:11434. mag-* compose ports are loopback
- tailscale serve: tailnet-only proxies to 127.0.0.1:8765 (443) and 127.0.0.1:9119 (8443)
- WSL: Ubuntu stopped, docker-desktop running
- requirements.txt: 18/18 lines unpinned (no ==). docker/autoclaw/Dockerfile L6 `npm install -g opencode@latest || ... || echo`
- ollama list: 11 models including hf.co/prism-ml/Ternary-Bonsai-2-27B-gguf (third-party GGUF) and custom athena-class:latest 32 GB / qwen-desk (Modelfile provenance Unproven)
- configs/mates.yaml L2 names tools/leave_protocol.py (file absent). MagLeaveProtocolDaily runs tools/leave_dispatcher.py, result=1 at 08:12 today

## Ranked findings (risk vs smallest fix)
| # | Finding | Tier | Smallest fix (existing organ) | Needs |
|---|---|---|---|---|
| 1 | The off-machine tip witness has been dark since at least 10-18 (gist 403). It is the only anchor that survives a writer rewrite | V | Re-scope the PAT (Gists: Read and write); the daily task then resumes the ratchet | **Nacho** (credential) |
| 2 | All chain backups are on the same disk inside the repo; offsite restic is never scheduled. A rewrite then backup copies the lie, and a disk loss takes everything | V | Pick a medium for backup_offsite.ps1 (Tailscale sftp to another node, or USB), then schedule it with -Verify weekly | **Nacho** (medium + passphrase) |
| 3 | memory/biography is Modify-able by CodexSandboxUsers + 5 unresolved SIDs, so sandboxed agents can rewrite chain files in place, beneath any lease | V | Change those ACEs to RX on memory/biography (writer = foste/container only); confirm which seat needs write first | **admin + Nacho** |
| 4 | AdjudicationBus runs, as foste every few minutes, code that lives in another profile (C:\Users\etfag\.zcode) with ExecutionPolicy Bypass. Whoever controls etfag controls foste | V | Confirm ownership; move the script into the repo/foste profile or disable the task | **Nacho** |
| 5 | No scheduled chain verify. backup_chain verifies copy == source, not that the source is honest; the verify only runs when a writer extends | V (schedule) / I (consequence) | Call `_verify_chain_consistent` / verify_verkle_full.py at the start of MagChainBackupDaily; on failure file a fleet_report NOTICE (category breach) and skip the prune | code pass (approved organs) |
| 6 | No egress notice (the casino signal). Live outbound includes Discord (Hermes gateway) and ZCode -> Alibaba-range hosts | V (talkers) / I (risk) | MagProbeCadence appends a daily egress snapshot (process, remote /24, bytes) to memory/security/; a first-seen destination writes a cast_probes-style NOTICE row | code pass |
| 7 | Seat handshake off by default, so any local process that reaches 127.0.0.1:8766/8001 speaks as any seat | V | Set MAG_SEAT_HANDSHAKE=warn in compose for mag-mcp (log-only), then enforce after a week | **Nacho** (compose edit; mag-mcp recreate) |
| 8 | Wildcard listeners left: factorio 27000/34197, plus 22/8080/8765 pending the admin script | V | Run scripts/host_lockdown_fish_tank_20261019.ps1 elevated; bind factorio to the tailnet IP or stop it when idle | **admin** |
| 9 | Supply chain: 18/18 deps unpinned; `opencode@latest` with silent `|| echo` fallback; third-party GGUF in Ollama | V | `pip freeze > requirements.lock`; pin the opencode version and drop the `|| echo`; note each model's source in a manifest | code pass |
| 10 | Stale law: mates.yaml points at the missing tools/leave_protocol.py; the leave task fails (exit 1). MAG_ALLOW_LIVE_WRITES fences tests only | V | Update the mates.yaml reference to leave_dispatcher; document that the fence covers tests only (rewrite verbs already need MAG_ALLOW_CHAIN_REWRITE) | code pass |

## Provenance
The chain, backup_chain (keep-7 + incomplete marker, fixing the earlier truncation bug), tip_witness (W3, 2026-09-30), offsite plan (2026-09-30 audit row 18), seat_handshake (2026-10-17 harness), fleet_report notices (2026-10-17), fish-tank remediation (today).

## Echo check
Same lesson as the 09-30 audit (row 18: no off-machine copy) and the 10-17 self-replication defense. **Three eras now say the anchor must live off this disk.** That repetition makes it load-bearing.

## Five bones
- Claims: the hash chain makes rewrites evident
- Proofs: _verify_chain_consistent at write time; tip witness gist (dark)
- Assumptions: the verifier's copy is out of reach of the writer. **Broken today**: the only copies sit on the same disk, with an ACL open to sandbox accounts
- Forbids: "the chain proves itself." A self-held chain proves only internal consistency
- Costs: an off-machine anchor needs a credential and a medium, and those are exactly the things a breach goes after

## Fold
- Law: an integrity anchor counts only if the writer can't reach it (off-disk, different credential)
- Organ: existing tip_witness + backup_offsite + backup_chain (verify-before-copy) + fleet_report NOTICE
- Shelf: assume-breach checklist = witness live? offsite last green? ACL on memory/biography? egress first-seen?
- Poetry: "a ledger that only you can read is a diary"

## Surprise
A scheduled task under foste executes code from **another Windows profile (etfag)** every few minutes. And the off-machine witness has been failing silently-but-logged for two days. It alerts into memory/attention.md, which sits on the same disk.

## Falsifiability / counters
Wrong if: a gist publish succeeded after 10-17, offsite restic snapshots exist, or the CodexSandboxUsers ACE is overridden by a deny. FORBIDS: treating local backups as tamper evidence. PAID RENT ON: tip_witness logs, icacls, schtasks, netstat.

## Receipt
watch/LIBRARY/STEAL_ESTATE_HARDENING_20261019.md: read-only self-steal. NOTICE N-20261019-fish-tank-and-estate-hardening filed via mag.fleet_report.file_report (seat grokbot-mag) into watch/receipts/.
