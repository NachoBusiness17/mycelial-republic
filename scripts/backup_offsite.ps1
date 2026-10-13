# scripts/backup_offsite.ps1  offsite backup for the Mag truth core (audit fix #4, 2026-09-30).
#
# Cause (receipt): MAG_SYSTEMS_DEEP_ANALYSIS_20260930 row 18 FAIL  the only git remote is a
# same-disk bare repo, and memory/biography (chain+tip+knots+residual), memory/seals, state/ and
# .env have NO confirmed off-machine copy. Fix table row 4 demands encrypted offsite snapshots
# PLUS a restore test that runs _verify_chain_consistent on the restored copy.
# Evidence it is fixed: design + runbook in watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md; a green
# -Verify run by the operator (restore -> byte diff -> chain gate on the RESTORED copy) is the proof.
#
# Deliberately NOT scheduled (mission law 2026-09-30): the operator picks the medium (see plan section 4)
# and the cadence. This script is ready-to-run; it never registers tasks and never ran against a
# real repository during design.
#
# Usage (from repo root or anywhere; the script self-locates the repo):
#   powershell -ExecutionPolicy Bypass -File scripts\backup_offsite.ps1 -Repository 'E:\restic-mag'
#   powershell -ExecutionPolicy Bypass -File scripts\backup_offsite.ps1 -Repository 'sftp:user@100.96.161.76:restic-mag'
#   powershell -ExecutionPolicy Bypass -File scripts\backup_offsite.ps1 -Repository 'b2:mag-offsite-backup' -Verify
#
# Repository comes from -Repository or env RESTIC_REPOSITORY. Password comes from -Password or
# env RESTIC_PASSWORD; if neither is given, restic prompts interactively (fine for manual runs).
# B2 media additionally need B2_APPLICATION_KEY_ID / B2_APPLICATION_KEY in the environment.
#
# PASSPHRASE LAW (audit action #3 pattern): the repo password is a single point of failure 
# store a copy off-machine (password manager + printed) before trusting a green -Verify.
[CmdletBinding()]
param(
    [Parameter()] [string]$Repository = $env:RESTIC_REPOSITORY,
    # Never logged, never echoed; scoped to child restic processes and scrubbed on exit.
    [Parameter()] [string]$Password,
    # Restore-test, not just backup: restic check + restore latest biography snapshot +
    # sha256 diff live-vs-restored + mag.verkle_knot._verify_chain_consistent on the RESTORED copy.
    [switch]$Verify,
    # Keep the restore staging dir for inspection instead of deleting it.
    [switch]$KeepTemp
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
Set-Location $Root
$VenvPy = Join-Path $Root '.venv\Scripts\python.exe'

if (-not $Repository) {
    throw "need -Repository (or env RESTIC_REPOSITORY). Medium not chosen yet  see watch/inbox/OFFSITE_BACKUP_PLAN_20260930.md section 4."
}
if (-not (Get-Command restic -ErrorAction SilentlyContinue)) {
    throw "restic not on PATH. Runbook step 1: winget install --id restic.restic (then open a new terminal)."
}
if ($Verify -and -not (Test-Path $VenvPy)) {
    throw "-Verify needs .venv\Scripts\python.exe (the mag.verkle_knot chain gate). Repair: powershell -ExecutionPolicy Bypass -File scripts\ensure_venv.ps1"
}

# The backup set  plan section 3 (sizes measured 2026-09-30). Order matters only for logging.
$Sets = @(
    @{ Tag = 'biography'; Path = 'memory/biography' },  # chain + tip + knots + residual (the truth core)
    @{ Tag = 'seals';     Path = 'memory/seals' },      # frozen chain/tip/providers copies
    @{ Tag = 'state';     Path = 'state' },             # live boot/state docs (gitignored)
    @{ Tag = 'env';       Path = '.env' }               # provider keys  encrypted at rest by restic
)

function Invoke-Restic {
    param([Parameter(Mandatory)][string[]]$ResticArgs)
    & restic @ResticArgs
    if ($LASTEXITCODE -ne 0) {
        throw "restic $($ResticArgs -join ' ') failed (exit $LASTEXITCODE)"
    }
}

# Scope env overrides to this run; restore whatever the session had on the way out.
$hadRepoEnv = Test-Path Env:\RESTIC_REPOSITORY
$oldRepoEnv = $env:RESTIC_REPOSITORY
$hadPassEnv = Test-Path Env:\RESTIC_PASSWORD
$oldPassEnv = $env:RESTIC_PASSWORD
$stage = $null

try {
    $env:RESTIC_REPOSITORY = $Repository
    if ($Password) { $env:RESTIC_PASSWORD = $Password }

    # --- init-if-absent: exit 10 == repository does not exist (restic documented exit code) ---
    & restic cat config *> $null
    if ($LASTEXITCODE -eq 10) {
        Write-Host "[init] repository absent - initializing $Repository"
        Write-Host "[init] NEW repo: restic will prompt for a passphrase. STORE A COPY OFF-MACHINE (passphrase law, plan section 6)."
        Invoke-Restic @('init')
    }
    elseif ($LASTEXITCODE -ne 0) {
        throw "cannot read repository config (exit $LASTEXITCODE): wrong URL, unreachable medium, or wrong password. See plan section 4."
    }

    # --- backup: one tagged snapshot per set ---
    foreach ($s in $Sets) {
        if (-not (Test-Path (Join-Path $Root $s.Path))) {
            throw "backup set missing on disk: $($s.Path) (plan section 3 table changed?)"
        }
        Write-Host "[backup] $($s.Path)  (tag: $($s.Tag))"
        Invoke-Restic @('backup', '--tag', $s.Tag, $s.Path)
    }

    # --- retention: 7 daily snapshots, keep-last floor so a >7d gap never empties the repo ---
    Write-Host '[forget] keep-daily 7 (+ keep-last 1 floor), prune'
    Invoke-Restic @('forget', '--keep-daily', '7', '--keep-last', '1', '--prune')

    Write-Host '[done] backup complete against' $Repository

    # --- -Verify: restore-test, not just backup (audit fix #4 law) ---
    if ($Verify) {
        Write-Host '[verify] restic check (repo integrity we just wrote)'
        Invoke-Restic @('check')

        $stage = Join-Path ([System.IO.Path]::GetTempPath()) ("mag-restore-test-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
        New-Item -ItemType Directory -Path $stage | Out-Null
        Write-Host "[verify] restoring latest biography snapshot to $stage"
        Invoke-Restic @('restore', 'latest', '--tag', 'biography', '--target', $stage)

        $chain = Get-ChildItem -Path $stage -Recurse -Filter 'verkle_chain.jsonl' | Select-Object -First 1
        if (-not $chain) { throw "verify FAIL: restored snapshot contains no verkle_chain.jsonl" }
        $restoredChain = $chain.FullName
        $restoredTip = Join-Path $chain.DirectoryName 'verkle_tip.json'
        $liveChain = Join-Path $Root 'memory\biography\verkle_chain.jsonl'
        $liveTip = Join-Path $Root 'memory\biography\verkle_tip.json'

        # diff-check 1: the restored chain and tip are byte-identical to the live ones.
        foreach ($pair in @(@('chain', $liveChain, $restoredChain), @('tip', $liveTip, $restoredTip))) {
            $name, $live, $restored = $pair
            if (-not (Test-Path $live))   { throw "verify FAIL: live $name missing: $live" }
            if (-not (Test-Path $restored)) { throw "verify FAIL: restored $name missing: $restored" }
            $hLive = (Get-FileHash -Algorithm SHA256 -LiteralPath $live).Hash
            $hRest = (Get-FileHash -Algorithm SHA256 -LiteralPath $restored).Hash
            if ($hLive -ne $hRest) {
                throw "verify FAIL: $name sha256 mismatch live($hLive) vs restored($hRest)"
            }
        }
        Write-Host '[verify] sha256 diff-check PASS (chain + tip byte-identical live vs restored)'

        # diff-check 2: the audit's law  run the REAL gate, _verify_chain_consistent, against the
        # RESTORED copy. Module globals CHAIN/TIP are read at call time inside verkle_knot, so
        # pointing them at the restored files runs the genuine append-gate on the restored chain.
        $gateCode = @"
import sys
from pathlib import Path
sys.path.insert(0, r'$Root')
import mag.verkle_knot as vk
vk.CHAIN = Path(r'$restoredChain')
vk.TIP = Path(r'$restoredTip')
ok, why = vk._verify_chain_consistent()
print(('[chain-gate PASS] ' if ok else '[chain-gate FAIL] ') + why)
sys.exit(0 if ok else 1)
"@
        & $VenvPy -c $gateCode
        if ($LASTEXITCODE -ne 0) {
            throw "verify FAIL: _verify_chain_consistent rejected the RESTORED chain copy"
        }
        Write-Host '[verify] restore-test PASS: chain gate green against the restored copy (not just backed up)'
    }
}
finally {
    if ($stage) {
        if ($KeepTemp) { Write-Host "[verify] staging kept for inspection: $stage" }
        else { Remove-Item -Recurse -Force -LiteralPath $stage -ErrorAction SilentlyContinue }
    }
    if ($hadRepoEnv) { $env:RESTIC_REPOSITORY = $oldRepoEnv } else { Remove-Item Env:\RESTIC_REPOSITORY -ErrorAction SilentlyContinue }
    if ($hadPassEnv) { $env:RESTIC_PASSWORD = $oldPassEnv } else { Remove-Item Env:\RESTIC_PASSWORD -ErrorAction SilentlyContinue }
}
