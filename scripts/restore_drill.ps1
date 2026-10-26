# scripts/restore_drill.ps1  C2 continuity restore drill, LOCAL half (Q08, 2026-09-30).
#
# Cause (receipt): OFFSITE_BACKUP_PLAN_20260930 fix-table row 4 demands a TESTED restore, not
# just backups; mission Q08 (watch/inbox/frontier_asks/volley2/V2ASK2.md) asks for the drill
# runbook with restic restore commands, the verify call, the pytest gate and expected timing.
# Evidence it is fixed: this script RUNS the drill live on one machine  restic snapshot of the
# four backup sets -> restore into a TEMP tree (never the live tree) -> _verify_chain_consistent
# against the RESTORED copy -> pytest smoke (parity + water families) against the restored tree
# -> RESTORE-VERIFIED or the exact failure. Receipt: watch/inbox/last_mile_20260930/R11_RESTORE_DRILL.md.
#
# --local is the only automated mode. The FULL C2 drill (real offsite medium + a SECOND machine
# verifying at the published tip) is the M4 OPERATOR GATE: it needs hardware the seat does not
# own. Running without -Local prints the gate card and exits 3 (deliberate, not an error).
#
# TWIN-TREE design (lesson of the 2026-09-30 19:13 first run, which FAILED honestly):
#  - Run 1 failed because the frozen smoke family included tests/test_parity_gate_hook_pin.py,
#    which was STAGED BUT NOT COMMITTED at drill time (git ls-files reads the index; git archive
#    HEAD reads the commit). A restore can only return what is committed. Fix: the smoke family
#    is intersected with `git cat-file -e HEAD:<path>` and every exclusion is printed loudly.
#  - The live working tree is dirty and evolving under concurrent fleet seats (e.g. modified
#    tools/rule_parity_out/*.json changed a smoke test's live outcome between two runs 20 min
#    apart). A live-tree baseline is therefore nondeterministic. Fix: TWIN TREES  the baseline
#    tree and the restored tree get the IDENTICAL git-archive-HEAD code layer, and differ ONLY
#    in how the four data sets arrived: baseline = plain file copy of the live sets, restored =
#    restic snapshot->restore. Equal pytest outcomes on identical code isolate EXACTLY the
#    restic roundtrip; live-tree flakiness cannot leak in.
#  - Default code layer is the SMOKE SCOPE (~0.4 GB: mag tools tests configs scripts githooks
#    conftest.py pytest.ini watch/cage_bin  the paths these tests read, verified by grep
#    2026-09-30); the full tracked tree is 18.5 GB dominated by watch/dashboard/attic which the
#    smoke never reads. -FullTree archives all of HEAD for faithful-timing rehearsal.
#  - The chain gate imports the RESTORED tree's own mag.verkle_knot (tree first on sys.path)
#    and patches CHAIN/TIP to the restored files (both read at call time; verified against
#    source 2026-09-30)  the same gate that fences every live append, run on restored code
#    against restored data.
#  - NO live-vs-restored sha256 diff: the live chain grows ~150 rows/day from other seats and
#    any mid-drill autoseal append would make live bytes drift past the snapshot for a reason
#    that is not a restore defect. The restored-copy gate self-verifies internal consistency.
#  - The drill repo lives under %TEMP% (never inside the estate git tree, plan section 6
#    boundary) and its passphrase is a throwaway generated per run  this is NOT the real
#    offsite passphrase (passphrase law, plan section 6).
#
# Usage:
#   powershell -ExecutionPolicy Bypass -File scripts\restore_drill.ps1 -Local
#   powershell -ExecutionPolicy Bypass -File scripts\restore_drill.ps1 -Local -ResticPath C:\path\restic.exe
#   powershell -ExecutionPolicy Bypass -File scripts\restore_drill.ps1 -Local -FullTree -KeepWorkspace
[CmdletBinding()]
param(
    # The local half of the C2 drill: temp repo + temp twin trees on THIS machine.
    [Parameter()] [switch]$Local,
    # restic executable; default assumes restic on PATH (runbook step 1: winget install --id restic.restic).
    [Parameter()] [string]$ResticPath = 'restic',
    # Keep the drill workspace (repo + both trees) for inspection instead of deleting it.
    [Parameter()] [switch]$KeepWorkspace,
    # Archive ALL of git HEAD (18.5 GB) instead of the smoke scope (~0.4 GB).
    [Parameter()] [switch]$FullTree
)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $PSScriptRoot
$VenvPy = Join-Path $Root '.venv\Scripts\python.exe'

# ---------- M4 operator gate: -Local is the only automated mode ----------
if (-not $Local) {
    Write-Host @'
[M4 OPERATOR GATE] The FULL C2 drill is not automated here. It needs:
  1. a real offsite medium chosen + live (plan section 4: USB SSD / laptop-sftp / B2);
  2. a SECOND machine (the disk-loss survivor): python 3.11+, this repo's venv deps
     (scripts/ensure_venv.ps1), restic (winget install --id restic.restic), git;
  3. the offsite passphrase (passphrase law: stored off-machine BEFORE trusting green).
  Then on the second machine: scripts\backup_offsite.ps1 -Repository <offsite-url> -Verify
  (restore + sha256 diff + chain gate on the restored copy), then this drill's phases
  against that restore. The LOCAL half (this script, -Local) proves the mechanism.
Run: powershell -ExecutionPolicy Bypass -File scripts\restore_drill.ps1 -Local
'@
    exit 3
}

# ---------- preconditions ----------
if (-not (Test-Path $VenvPy)) {
    throw "-Local needs .venv\Scripts\python.exe. Repair: powershell -ExecutionPolicy Bypass -File scripts\ensure_venv.ps1"
}
& $ResticPath version *> $null
if ($LASTEXITCODE -ne 0) { throw "restic not runnable at '$ResticPath' (runbook step 1: winget install --id restic.restic, or pass -ResticPath)" }
$ResticVersion = (& $ResticPath version) -join ' '
$HeadSha = (& git -C $Root rev-parse HEAD).Trim()
Write-Host "[drill] restic: $ResticVersion"
Write-Host "[drill] git HEAD: $HeadSha"
Write-Host "[drill] python: $(& $VenvPy --version)"

# The four backup sets (plan section 3; same table scripts/backup_offsite.ps1 uses).
$Sets = @(
    @{ Tag = 'biography'; Path = 'memory/biography' },
    @{ Tag = 'seals';     Path = 'memory/seals' },
    @{ Tag = 'state';     Path = 'state' },
    @{ Tag = 'env';       Path = '.env' }
)
# The smoke families (parity + water). Frozen family list; each file must exist IN HEAD
# (git cat-file -e), because a restore can only return committed code (run-1 lesson).
$SmokeFamily = @(
    'tests/test_hunger_ledger_parity.py',
    'tests/test_parity_gate_hook_pin.py',
    'tests/test_rule_parity.py',
    'tests/test_k8s_water.py',
    'tests/test_water_computer.py',
    'tests/test_water_graph.py',
    'tests/test_water_graph_campaign.py',
    'tests/test_water_graph_starvation.py',
    'tests/test_water_swarm.py'
)
$SmokeTests = @()
foreach ($f in $SmokeFamily) {
    & git -C $Root cat-file -e "HEAD:$($f -replace '\\','/')" 2> $null
    if ($LASTEXITCODE -eq 0) { $SmokeTests += $f }
    else { Write-Host "[drill] SMOKE EXCLUSION: $f is not in HEAD $HeadSha  uncommitted code is unrestorable (commit it; run-1 lesson 2026-09-30)" -ForegroundColor Yellow }
}
if ($SmokeTests.Count -lt 4) { throw "smoke family collapsed to $($SmokeTests.Count) HEAD-tracked files; refusing to run a hollow smoke" }
# Smoke-scope git layer: everything these tests import/read. Derived empirically 2026-09-30:
# run 2 failed collection because tools/__init__.py imports root `config` and test_rule_parity
# imports `server.world`; both are tracked top-level code, now in scope. Excluded is only the
# 18 GB of watch/dashboard/attic bulk the smoke never reads.
$SmokeScope = @('mag', 'tools', 'tests', 'configs', 'config.py', 'server', 'scripts', 'githooks', 'watch/cage_bin', 'conftest.py', 'pytest.ini')

# ---------- helpers ----------
function Invoke-Restic {
    param([Parameter(Mandatory)][string[]]$ResticArgs)
    $out = & $ResticPath @ResticArgs 2>&1 | ForEach-Object { $_.ToString() }
    if ($LASTEXITCODE -ne 0) {
        throw "restic $($ResticArgs -join ' ') failed (exit $LASTEXITCODE): $($out -join ' ')"
    }
    return $out
}
function Get-TreeStats {
    param([Parameter(Mandatory)][string]$Path)
    if (Test-Path $Path -PathType Leaf) {
        $f = Get-Item -LiteralPath $Path
        return @{ Files = 1; Bytes = $f.Length }
    }
    $m = Get-ChildItem -LiteralPath $Path -Recurse -File -Force | Measure-Object -Property Length -Sum
    return @{ Files = $m.Count; Bytes = [long]($m.Sum) }
}
function Copy-LiveSet {
    # robocopy for dirs (fast, preserves structure), Copy-Item for the single .env file.
    # robocopy exit codes 0-7 are success; >=8 is failure.
    param([Parameter(Mandatory)][string]$RelPath, [Parameter(Mandatory)][string]$Target)
    $src = Join-Path $Root $RelPath
    if (Test-Path $src -PathType Leaf) { Copy-Item -LiteralPath $src -Destination (Join-Path $Target $RelPath); return }
    $dst = Join-Path $Target $RelPath
    New-Item -ItemType Directory -Path $dst -Force | Out-Null
    & robocopy $src $dst /E /NFL /NDL /NJH /NJS /NP /R:1 /W:1 *> $null
    if ($LASTEXITCODE -ge 8) { throw "robocopy $src -> $dst failed (exit $LASTEXITCODE)" }
}
function Invoke-PytestSmoke {
    param([Parameter(Mandatory)][string]$WorkDir)
    Push-Location $WorkDir
    try {
        # -p no:cacheprovider: no .pytest_cache churn in whichever tree we run against.
        $lines = & $VenvPy -m pytest @SmokeTests -q --tb=no -p no:cacheprovider 2>&1 | ForEach-Object { $_.ToString() }
        $exit = $LASTEXITCODE
    }
    finally { Pop-Location }
    $failed = @($lines | Where-Object { $_ -match '^(FAILED|ERROR)\s+(\S+)' } | ForEach-Object { $Matches[2] })
    $summary = ($lines | Where-Object { $_ -match '\d+ (failed|passed|error)' } | Select-Object -Last 1)
    $passed = 0; if ($summary -match '(\d+) passed') { $passed = [int]$Matches[1] }
    return @{ Exit = $exit; Failed = $failed; Passed = $passed; Summary = $summary; Lines = $lines }
}
$PhaseTimes = [System.Collections.Generic.List[object]]::new()
$sw = [System.Diagnostics.Stopwatch]::StartNew()
function Phase {
    param([Parameter(Mandatory)][string]$Name, [scriptblock]$Body)
    $sw.Restart()
    $r = & $Body
    $PhaseTimes.Add([pscustomobject]@{ Phase = $Name; Seconds = [math]::Round($sw.Elapsed.TotalSeconds, 1) })
    return $r
}

$hadRepoEnv = Test-Path Env:\RESTIC_REPOSITORY; $oldRepoEnv = $env:RESTIC_REPOSITORY
$hadPassEnv = Test-Path Env:\RESTIC_PASSWORD;  $oldPassEnv = $env:RESTIC_PASSWORD
$ws = $null
$drillFailed = $false
Push-Location $Root   # restic backup takes the set paths RELATIVE to the repo root
try {
    # Throwaway drill passphrase (NOT the offsite passphrase; dies with the workspace).
    $env:RESTIC_PASSWORD = ('drill-' + [guid]::NewGuid().ToString('N') + '-' + [guid]::NewGuid().ToString('N'))
    $ws = Join-Path ([System.IO.Path]::GetTempPath()) ("mag-restore-drill-" + (Get-Date -Format 'yyyyMMdd-HHmmss'))
    $repo = Join-Path $ws 'repo'
    $tree = Join-Path $ws 'tree'        # restored tree: HEAD code + restic-restored sets
    $btree = Join-Path $ws 'basetree'   # baseline twin: SAME HEAD code + plain-copied live sets
    New-Item -ItemType Directory -Path $repo, $tree, $btree | Out-Null
    $env:RESTIC_REPOSITORY = $repo
    Write-Host "[drill] workspace: $ws"

    # ---------- phase A: the shared code layer (identical bytes into BOTH twins) ----------
    Phase 'code-layer-archive-into-both-trees' {
        $zip = Join-Path $ws 'code-layer.zip'
        if ($FullTree) { & git -C $Root archive --format=zip -o $zip HEAD }
        else { & git -C $Root archive --format=zip -o $zip HEAD -- @SmokeScope }
        if ($LASTEXITCODE -ne 0) { throw "git archive failed (exit $LASTEXITCODE)" }
        Expand-Archive -LiteralPath $zip -DestinationPath $tree
        Expand-Archive -LiteralPath $zip -DestinationPath $btree
        Remove-Item -LiteralPath $zip
    } | Out-Null
    Write-Host "[phase A] git layer ($(if ($FullTree) {'full HEAD'} else {'smoke scope'})) extracted into BOTH twins"

    # ---------- phase B: baseline twin = live-copied four sets ----------
    foreach ($s in $Sets) { Copy-LiveSet -RelPath $s.Path -Target $btree }
    $baseline = Phase 'baseline-twin-pytest' { Invoke-PytestSmoke -WorkDir $btree }
    Write-Host ("[phase B] baseline twin: exit {0}, {1} passed, failed: {2}" -f $baseline.Exit, $baseline.Passed, ($baseline.Failed -join ', '))
    if ($baseline.Exit -notin @(0, 1)) {
        throw "baseline pytest internal error (exit $($baseline.Exit)): $($baseline.Lines | Select-Object -Last 5)"
    }

    # ---------- phase C: restic snapshot of the four sets ----------
    Phase 'restic-init' { Invoke-Restic @('init') } | Out-Null
    $setStats = @()
    foreach ($s in $Sets) {
        $livePath = Join-Path $Root $s.Path
        if (-not (Test-Path $livePath)) { throw "backup set missing on disk: $($s.Path) (plan section 3 table changed?)" }
        $t = Phase ("restic-backup-" + $s.Tag) { Invoke-Restic @('backup', '--tag', $s.Tag, $s.Path) }
        $snapId = ($t | Where-Object { $_ -match 'snapshot [0-9a-f]{8} saved' }) -join ''
        Write-Host "[phase C] backed up $($s.Path) (tag $($s.Tag)) $snapId"
        $st = Get-TreeStats -Path $livePath
        $setStats += [pscustomobject]@{ Tag = $s.Tag; Path = $s.Path; Files = $st.Files; Bytes = $st.Bytes }
    }

    # ---------- phase D: integrity check + restore the four sets INTO the restored twin ----------
    Phase 'restic-check' { Invoke-Restic @('check') } | Out-Null
    foreach ($s in $Sets) {
        Phase ("restic-restore-" + $s.Tag) { Invoke-Restic @('restore', 'latest', '--tag', $s.Tag, '--target', $tree) } | Out-Null
        Write-Host "[phase D] restored tag $($s.Tag) -> restored twin"
    }

    # ---------- phase E: the REAL chain gate, restored code against restored data ----------
    $restoredChain = Join-Path $tree 'memory\biography\verkle_chain.jsonl'
    $restoredTip = Join-Path $tree 'memory\biography\verkle_tip.json'
    if (-not (Test-Path $restoredChain)) { throw "verify FAIL: restored twin has no verkle_chain.jsonl at $restoredChain" }
    if (-not (Test-Path $restoredTip))   { throw "verify FAIL: restored twin has no verkle_tip.json at $restoredTip" }
    $gateCode = @"
import sys
from pathlib import Path
sys.path.insert(0, r'$tree')   # the RESTORED tree's own mag package, not the live one
import mag.verkle_knot as vk
vk.CHAIN = Path(r'${restoredChain}')
vk.TIP = Path(r'${restoredTip}')
ok, why = vk._verify_chain_consistent()
print('[chain-gate module]', vk.__file__)
print(('[chain-gate PASS] ' if ok else '[chain-gate FAIL] ') + why)
sys.exit(0 if ok else 1)
"@
    $gateOut = Phase 'chain-gate-restored-copy' { & $VenvPy -c $gateCode 2>&1 | ForEach-Object { $_.ToString() } }
    if ($LASTEXITCODE -ne 0) { throw "verify FAIL: _verify_chain_consistent rejected the RESTORED chain copy: $($gateOut -join ' ')" }
    Write-Host "[phase E] $(($gateOut | Where-Object { $_ -match 'chain-gate' }) -join ' | ')"

    # ---------- phase F: pytest smoke against the RESTORED twin ----------
    $restoredRun = Phase 'restored-tree-pytest' { Invoke-PytestSmoke -WorkDir $tree }
    Write-Host ("[phase F] restored twin: exit {0}, {1} passed, failed: {2}" -f $restoredRun.Exit, $restoredRun.Passed, ($restoredRun.Failed -join ', '))
    if ($restoredRun.Exit -notin @(0, 1)) {
        throw "restored pytest internal error (exit $($restoredRun.Exit)): $($restoredRun.Lines | Select-Object -Last 5)"
    }

    # ---------- comparison law: restored twin == baseline twin on identical HEAD code ----------
    $extraFail = @($restoredRun.Failed | Where-Object { $_ -notin $baseline.Failed })
    $missingFail = @($baseline.Failed | Where-Object { $_ -notin $restoredRun.Failed })
    if ($extraFail.Count -gt 0 -or $missingFail.Count -gt 0) {
        throw "smoke PARITY FAIL: restored twin diverged from baseline twin. extra failures restored-only: [$($extraFail -join ', ')]; baseline-only: [$($missingFail -join ', ')]"
    }
    if ($restoredRun.Passed -ne $baseline.Passed) {
        throw "smoke PARITY FAIL: passed count differs baseline($($baseline.Passed)) vs restored($($restoredRun.Passed))"
    }

    # ---------- sizes for the receipt ----------
    $repoStats = Get-TreeStats -Path $repo
    $treeStats = Get-TreeStats -Path $tree

    Write-Host ''
    Write-Host '================ DRILL RESULT ================'
    $PhaseTimes | Format-Table -AutoSize | Out-String | Write-Host
    $totalSetBytes = ($setStats | Measure-Object -Property Bytes -Sum).Sum
    Write-Host ("backup sets (live bytes in): {0:N0} B across {1} files" -f $totalSetBytes, ($setStats | Measure-Object -Property Files -Sum).Sum)
    $setStats | Format-Table -AutoSize | Out-String | Write-Host
    Write-Host ("drill restic repo on disk (zstd+dedup): {0:N0} B, {1} files" -f $repoStats.Bytes, $repoStats.Files)
    Write-Host ("restored twin on disk (git layer + 4 sets): {0:N0} B, {1} files" -f $treeStats.Bytes, $treeStats.Files)
    Write-Host ("baseline twin  : {0}" -f $baseline.Summary)
    Write-Host ("restored twin  : {0}  (identical outcome = smoke PARITY)" -f $restoredRun.Summary)
    Write-Host ("sum of phase times: {0:N1} s" -f (($PhaseTimes | Measure-Object -Property Seconds -Sum).Sum))
    Write-Host 'RESTORE-VERIFIED'
    exit 0
}
catch {
    $drillFailed = $true
    Write-Host "[FAIL] $($_.Exception.Message)" -ForegroundColor Red
    exit 1
}
finally {
    if ($env:RESTIC_PASSWORD) { Remove-Item Env:\RESTIC_PASSWORD -ErrorAction SilentlyContinue }
    if ($hadRepoEnv) { $env:RESTIC_REPOSITORY = $oldRepoEnv } else { Remove-Item Env:\RESTIC_REPOSITORY -ErrorAction SilentlyContinue }
    if ($hadPassEnv) { $env:RESTIC_PASSWORD = $oldPassEnv } else { Remove-Item Env:\RESTIC_PASSWORD -ErrorAction SilentlyContinue }
    if ($ws) {
        if ($KeepWorkspace) { Write-Host "[drill] workspace kept: $ws" }
        elseif ($drillFailed) { Write-Host "[drill] FAILED run: workspace kept for diagnosis: $ws" }
        else { Remove-Item -Recurse -Force -LiteralPath $ws -ErrorAction SilentlyContinue; Write-Host '[drill] workspace cleaned' }
    }
    Pop-Location
}
