# OFFSITE BACKUP PLAN — audit fix #4 — 2026-09-30

**Status: DESIGN-COMPLETE, READY-TO-RUN. The medium is the operator's door —
pick one from §4 and run the 3 commands in §7.** Nothing is scheduled, nothing
has been run against any real repository (no medium chosen yet). This file is
the receipt for the fix; the executable half is `scripts/backup_offsite.ps1`.

Audit of record: `watch/inbox/MAG_SYSTEMS_DEEP_ANALYSIS_20260930.md`
- §18 (preparedness row 18): **Offsite backup = FAIL** — "only a same-disk
  bare repo; biography not listed in the pack."
- Fix table row 4: "back up biography, chain and knots offsite and **test a
  restore**" — encrypted snapshots (restic or borg) of `memory/biography`,
  `memory/seals`, `state`, `.env` to a second medium, plus a restore test that
  runs `_verify_chain_consistent` on the restored copy.
- §7: the same disk holds the estate, its only git remote, the biography
  backups and the essentials pack. One disk event = the truth core is gone.

## 1. The gap, re-verified today (bytes, not reports)

- `git remote -v` → `local → C:\Users\foste\Documents\projects\Mag-backup.git`
  — a bare repo on the **same physical disk** (audit §7; confirmed 2026-09-30,
  HEAD `f4e2c247f`). It protects against bad merges, not against the disk.
- `memory/biography` (the chain, tip, knots, residual DNA), `memory/seals`,
  `state/` and `.env` are gitignored (`.gitignore` lines 29/40/19) and are NOT
  in the 09-26 essentials-pack inclusion list (audit §18). **No confirmed
  off-machine copy of any of them exists.**
- The machine has exactly one drive: `C:` (1.19 TB used / 668 GB free). There
  is no second internal disk today.

## 2. Why restic

The audit allowed "restic or borg". Borg has no native Windows build (WSL
only); restic wins on this box:

- **Single static binary** (`restic.exe`, ~25 MB) — no installer, no runtime,
  winget package `restic.restic`.
- **Windows-native**; local, SFTP, and B2 backends all work from this host.
- **Client-side encryption** (AES-256, authenticated; the passphrase never
  leaves the machine) — this is what makes a cloud or laptop medium acceptable
  even though the set includes `.env` (live provider keys).
- **Dedup + zstd compression** — the set is text/JSON; daily snapshots share
  almost all chunks, so 7 days of history costs barely more than 1 day.
- **Snapshots, not mirrors** — point-in-time restore even after local
  corruption; `restic check` proves pack integrity.

## 3. The backup set (exact paths + sizes)

Sizes measured 2026-09-30 with `du -sb` / `find | wc -l` (audit §3.1 numbers
in parentheses where they differ — the audit's counts were taken earlier the
same day and the tree grows ~150 chain rows/day):

| # | Tag | Path | Files | Bytes | What it is |
|---|-----|------|-------|-------|------------|
| 1 | `biography` | `memory/biography` | 47,396 | 363,630,271 (~364 MB) | the truth core: `verkle_chain.jsonl` 6,073,046 B + `verkle_tip.json` + `latest.knot.json` + `knots/` 39.4 MB + `residual/` 150.0 MB (audit: 142.9 MB/4,016 files) + `derived/` 28.8 MB + `registry.jsonl` 6.1 MB + ~78 MB of internal tar/bak history (kept; dedup makes it ~free) |
| 2 | `seals` | `memory/seals` | 403 | 216,654,445 (~217 MB) | 20 seal dirs: frozen chain+tip+providers.yaml copies (audit §3.1: 206.6 MB) |
| 3 | `state` | `state` | 4,230 | 98,288,609 (~98 MB) | live boot/state docs, `CURRENT.md`, snapshots (gitignored) |
| 4 | `env` | `.env` | 1 | 5,868 | provider keys — restic-encrypted at rest; see the key-rotation caveat below |
| | | **total** | ~52,030 | **~679 MB** | first snapshot smaller after zstd+dedup; daily deltas tiny |

Caveats carried from the same audit (not this fix's scope, but they ride the
same bytes): `.env` and 20 tracked `providers.yaml` copies under seals hold
live keys — audit fix #1 (rotate the 7 keys) and #7 (untrack seals) remain
open. Encryption-at-rest makes the offsite copy safe to hold; **rotate the
keys anyway**.

## 4. The medium — operator's door, options laid out

Pick ONE repo URL (restic can `restic copy` snapshots to a second medium
later; no lock-in).

| Medium | Example `RESTIC_REPOSITORY` | Cost | Pros | Cons |
|---|---|---|---|---|
| **A. Second internal drive** | `D:\restic-mag` | $0 if a spare exists; **none installed today** — adding SATA/NVMe ≈ $50–100 + case work | fastest; zero new attack surface; always attached | same chassis: theft, fire, PSU surge kills both copies — the weakest "offsite"; a disk must be bought and fitted first |
| **B. USB SSD (1 TB)** | `E:\restic-mag` | ≈ $70–110 one-time (T7 class) | fast (USB3); **air-gapped between runs = best ransomware posture**; trivially portable | only counts as offsite if stored AWAY from the machine between runs; manual plug-in discipline (a stale backup is a silent backup) |
| **C. Laptop over Tailscale SSH** | `sftp:<user>@100.96.161.76:restic-mag` | $0 hardware | true off-machine TODAY: survives this box's disk loss; Tailscale already installed here (`C:\Program Files\Tailscale`); restic speaks SFTP so the laptop needs only an SSH server (Windows optional feature `OpenSSH.Server`, or sshd on Linux) — restic itself NOT needed on the laptop; repo path is relative to that user's home | laptop must be on + awake at backup time; one-time sshd enable on the laptop; throughput = LAN/DERP speed; laptop disk needs ≥ 2 GB free |
| **D. Backblaze B2 (cloud)** | `b2:mag-offsite-backup` | storage **$6/TB/mo** ($0.006/GB/mo) → today's ~0.7 GB ≈ **$0.005/mo**; 5 GB ≈ $0.03/mo. Downloads $0.01/GB, free up to 3× monthly average; API free tiers (2,500 Class A + 2,500 Class B/day) cover restic easily | only option that survives the room (fire/theft); automatic — no plug-in discipline; versioned, immutable-ish snapshots | account + application-key hygiene (audit fix #1/#3 law); first upload bound to home uplink; a third party holds ciphertext (acceptable: client-side encrypted — the key never leaves) |

Non-binding read of the trade: **C** is free and off-machine today; **D** is
offsite-today for cents; **B** is the best ransomware hedge but only counts if
stored away; **A** is convenience, not offsite. C+D or B+D later via
`restic copy` is cheap.

## 5. Retention policy — 7 days

`restic forget --keep-daily 7 --keep-last 1 --prune`

- one snapshot per day, kept for 7 distinct days;
- `--keep-last 1` floors it so a >7-day gap (holiday, laptop off) never leaves
  an empty repository;
- `--prune` reclaims space from forgotten snapshots.
- Ceiling ≈ 7 × 0.7 GB raw before dedup; in practice far less.

## 6. The script — `scripts/backup_offsite.ps1` (contract)

- Params: `-Repository` (or env `RESTIC_REPOSITORY`), `-Password` (or env
  `RESTIC_PASSWORD`; if neither, restic prompts interactively), `-Verify`,
  `-KeepTemp`.
- **Init-if-absent**: probes with `restic cat config`; exit 10 (repository
  does not exist) → `restic init`; any other nonzero → abort with cause.
- **Backup**: the four tagged sets of §3, one snapshot each (`--tag
  biography|seals|state|env`), then the §5 forget+prune.
- **`-Verify` mode — restore-test, not just backup** (the audit's law):
  1. `restic check` on the repo just written;
  2. `restic restore latest --tag biography` into a temp staging dir;
  3. sha256 diff-check: restored `verkle_chain.jsonl` + `verkle_tip.json`
     must be byte-identical to the live files;
  4. run the REAL gate — `.venv\Scripts\python.exe` imports
     `mag.verkle_knot`, points the module globals `CHAIN`/`TIP` at the
     restored files (both are read at call time, so the patch is sound), and
     calls `_verify_chain_consistent()` — the same function that gates every
     live append. PASS required, else the script exits nonzero.
- Password hygiene: `-Password` is scoped to the child restic processes only
  and scrubbed from the session env on exit; nothing is echoed.
- Boundary: the restic repo must never live inside the estate's git tree
  (keeps keys/ciphertext out of git — audit #1 law).

**Passphrase law (audit action #3 pattern):** the restic password becomes the
new single point of failure — lose it and the offsite copy is a brick, exactly
like the pack key was. Store a copy off-machine (password manager + printed
in the safe) BEFORE trusting the first green `-Verify`.

## 7. Runbook — the operator's 3 commands to go live

```powershell
# 1. Install restic (one-time)
winget install --id restic.restic
# confirm: restic version   (new terminal so PATH refreshes)

# 2. Go live on the chosen medium (init-if-absent + 4 tagged sets + 7-day retention)
powershell -ExecutionPolicy Bypass -File scripts\backup_offsite.ps1 -Repository '<repo-url-from-§4>'
# fresh repo: restic prompts for a NEW long passphrase — store it off-machine (§6 law)

# 3. Prove it (restore-test: chain gate runs against the RESTORED copy, must PASS)
powershell -ExecutionPolicy Bypass -File scripts\backup_offsite.ps1 -Repository '<repo-url>' -Verify
```

After green: re-run (2) daily-ish by hand at a quiet window (fleet crons run
08:00–09:00; `state/` files lock if a probe is mid-write). **Scheduling is an
operator call and is deliberately NOT done here** — mission law: design, do
not schedule. When you want it scheduled, wrap command (2) in a
`scripts/register_*_task.ps1` pattern the same way the census/FTS tasks do.

Disaster-restore quick reference:

```powershell
$env:RESTIC_REPOSITORY='<repo-url>'; $env:RESTIC_PASSWORD='<pass>'
restic snapshots                                   # pick an id
restic restore latest --tag biography --target C:\restore\mag
restic dump latest memory/biography/verkle_chain.jsonl   # single-file pull
```

## 8. Boundaries honored (mission law)

- NOT scheduled: no `schtasks`, no `Register-ScheduledTask`, no cron lane was
  created or modified.
- NOT run: no restic command was executed against any real local/remote
  repository; the `.ps1` was parse-checked only, and the §6 chain-gate
  mechanism was proven offline against the LIVE chain (read-only, no repo
  involved).
- The repo (this file) is the receipt; the autoseal hook registers the
  landing. `scripts/backup_offsite.ps1` sits outside the ratchet's `mag/` +
  `tools/` scope (no baseline impact).
