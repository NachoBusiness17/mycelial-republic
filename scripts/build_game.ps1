# scripts/build_game.ps1 - BUILD PIPELINE v1 (B5 + R6, last_mile 2026-09-30)
#
# Exports The Mountain headless to build/mountain-windows/ and zips it to
# build/mountain-<gitshort>.zip. Verifies the artifact by a fresh unzip
# (exe + pck + manifest present, non-trivial sizes).
#
# ARTIFACT IDENTITY (R6, Q09): after export the exe is STAMPED with an
# appended trailer [JSON payload][MAGSTMP1][u32 LE payload length]. The
# payload pins the source git sha + the pck sha256. The game's BootIntegrity
# autoload reads the stamp at boot, hashes the pck beside the exe, prints
# "ARTIFACT_ID git=<sha> pck=ok" to stderr, and exits 1 on a mismatch
# (swapped pck). A mountain-manifest.json sidecar (exe sha after stamping,
# pck sha, git sha, build time) ships in the zip for offline verification.
#
# SOURCE: default builds the estate twin (roblox_to_godot/). -FromTheMountain
# builds the public tree instead (the-mountain repo's game/ dir, default
# <repo root>\..\the-mountain, override with -MountainRepo) and stamps that
# repo's HEAD sha - the shape a stranger can rebuild from.
#
# Godot binary resolution order: -GodotBin param > $env:GODOT_BIN >
# tools/godot/Godot_v4.3-stable_win64_console.exe > tools/godot/Godot_v4.3-stable_win64.exe.
#
# Export templates: if %APPDATA%\Godot\export_templates\<version>\ is missing
# the platform template, downloads the official .tpz for the binary's version
# from GitHub releases and unpacks templates/ into the version dir.
# -SkipTemplates skips that attempt (offline run).
#
# Exit codes: 0 = artifact verified (stamped, manifest written, boot smoke
# exit 0); 2 = blocker banked (message says the fix).

param(
    [string]$GodotBin = "",
    [switch]$SkipTemplates,
    [switch]$FromTheMountain,
    [string]$MountainRepo = ""
)

$ErrorActionPreference = "Stop"
$Repo = Split-Path -Parent $PSScriptRoot
$Project = Join-Path $Repo "roblox_to_godot"
$BuildRoot = Join-Path $Repo "build"
$OutDir = Join-Path $BuildRoot "mountain-windows"
$ExeName = "TheMountain.exe"
$StampMagic = "MAGSTMP1"

function Fail([string]$Blocker, [string]$Fix) {
    Write-Output "BLOCKER: $Blocker"
    Write-Output "FIX: $Fix"
    exit 2
}

# --- 0. source tree (estate twin default; -FromTheMountain = public tree) ----
$SourceRepo = $Repo
$SourceLabel = "estate-twin"
if ($FromTheMountain) {
    if (-not $MountainRepo) { $MountainRepo = Join-Path (Split-Path -Parent $Repo) "the-mountain" }
    if (-not (Test-Path (Join-Path $MountainRepo ".git"))) {
        Fail "the-mountain repo not found at $MountainRepo" "clone NachoBusiness17/the-mountain there or pass -MountainRepo <path>"
    }
    $Project = Join-Path $MountainRepo "game"
    if (-not (Test-Path (Join-Path $Project "project.godot"))) {
        Fail "no game/project.godot under $MountainRepo" "sync the estate twin into the-mountain/game first (AC11 idiom)"
    }
    $SourceRepo = $MountainRepo
    $SourceLabel = "the-mountain"
    Write-Output "[0] source: the-mountain public tree ($MountainRepo @ HEAD)"
} else {
    Write-Output "[0] source: estate twin ($Project)"
}

# --- 1. locate the Godot binary ---------------------------------------------
if (-not $GodotBin) { $GodotBin = $env:GODOT_BIN }
if (-not $GodotBin) {
    $cand = @(
        (Join-Path $Repo "tools\godot\Godot_v4.3-stable_win64_console.exe"),
        (Join-Path $Repo "tools\godot\Godot_v4.3-stable_win64.exe")
    ) | Where-Object { Test-Path $_ } | Select-Object -First 1
    if ($cand) { $GodotBin = $cand }
}
if (-not $GodotBin -or -not (Test-Path $GodotBin)) {
    $g = Get-Command godot -ErrorAction SilentlyContinue
    if ($g) { $GodotBin = $g.Source }
}
if (-not $GodotBin -or -not (Test-Path $GodotBin)) {
    Fail "no Godot binary found (param, GODOT_BIN, tools/godot/, PATH all empty)" `
         "place Godot 4.3 win64 at tools/godot/ or set -GodotBin"
}
Write-Output "[1] godot: $GodotBin"

# --- 2. export templates (bootstrap if missing) ------------------------------
$Version = (& $GodotBin --version 2>$null | Select-Object -First 1).Trim()
Write-Output "[2] godot version: $Version"
$TemplatesRoot = Join-Path $env:APPDATA "Godot\export_templates"
# Template dir is the short version (4.3.stable), NOT the full --version string
# (4.3.stable.official.77dcf97d8); verified against the export error that names
# the expected path (B5 2026-09-30).
$parts = $Version.Split(".")
$TplVersion = ($parts[0..2] -join ".")
$TemplatesDir = Join-Path $TemplatesRoot $TplVersion
$NeedTpl = Join-Path $TemplatesDir "windows_release_x86_64.exe"
if (-not (Test-Path $NeedTpl)) {
    if ($SkipTemplates) {
        Fail "export template missing ($NeedTpl) and -SkipTemplates set" `
             "re-run without -SkipTemplates to auto-download"
    }
    Write-Output "[2] templates missing, downloading (about 1 GB, one time)"
    $rel = "$($parts[0]).$($parts[1])-$($parts[2])"
    $tpzName = "Godot_v$($parts[0]).$($parts[1])-$($parts[2])_export_templates.tpz"
    $url = "https://github.com/godotengine/godot/releases/download/$rel/$tpzName"
    $tpz = Join-Path $env:TEMP $tpzName
    $tmpExtract = Join-Path $env:TEMP "godot_tpl_$PID"
    try {
        & curl.exe -L --fail --retry 3 --silent --show-error -o $tpz $url
        if ($LASTEXITCODE -ne 0 -or -not (Test-Path $tpz) -or (Get-Item $tpz).Length -lt 100MB) {
            throw "download failed (curl exit $LASTEXITCODE, url $url)"
        }
        Add-Type -AssemblyName System.IO.Compression.FileSystem
        if (Test-Path $tmpExtract) { Remove-Item -Recurse -Force $tmpExtract }
        [System.IO.Compression.ZipFile]::ExtractToDirectory($tpz, $tmpExtract)
        $inner = Join-Path $tmpExtract "templates"
        if (-not (Test-Path $inner)) { throw "tpz has no templates/ dir inside" }
        if (-not (Test-Path $TemplatesDir)) { New-Item -ItemType Directory -Force -Path $TemplatesDir | Out-Null }
        Copy-Item (Join-Path $inner "*") $TemplatesDir -Recurse -Force
        Write-Output "[2] templates installed to $TemplatesDir"
    } catch {
        Fail "export template download failed: $($_.Exception.Message)" `
             "manual fix: curl -L -o `"$tpzName`" $url ; unzip ; move templates\* into '$TemplatesDir'"
    } finally {
        if (Test-Path $tmpExtract) { Remove-Item -Recurse -Force $tmpExtract -ErrorAction SilentlyContinue }
        if (Test-Path $tpz) { Remove-Item -Force $tpz -ErrorAction SilentlyContinue }
    }
} else {
    Write-Output "[2] templates present: $TemplatesDir"
}

# --- 3. export_presets.cfg (create if absent) --------------------------------
$PresetPath = Join-Path $Project "export_presets.cfg"
if (-not (Test-Path $PresetPath)) {
    Write-Output "[3] writing minimal export_presets.cfg (Windows Desktop, pck separate)"
    @'
[preset.0]

name="Windows Desktop"
platform="Windows Desktop"
runnable=true
advanced_options=false
dedicated_server=false
custom_features=""
export_filter="all_resources"
include_filter=""
exclude_filter=""
export_path=""
encryption_include_filters=""
encryption_exclude_filters=""
encrypt_pck=false
encrypt_directory=false

[preset.0.options]

custom_template/debug=""
custom_template/release=""
debug/export_console_wrapper=1
binary_format/embed_pck=false
texture_format/s3tc_bptc=true
texture_format/etc2_astc=false
binary_format/architecture="x86_64"
codesign/enable=false
application/modify_resources=false
application/icon=""
application/console_wrapper_icon=""
application/icon_interpolation=4
application/file_version=""
application/product_version=""
application/company_name=""
application/product_name=""
application/file_description=""
application/copyright=""
application/trademarks=""
application/export_angle=0
application/export_angle_64=false
ssh_remote_deploy/enabled=false
'@ | Set-Content -Encoding ASCII $PresetPath
} else {
    Write-Output "[3] export_presets.cfg exists, leaving untouched"
}

# --- 4. headless export -------------------------------------------------------
if (Test-Path $OutDir) { Remove-Item -Recurse -Force $OutDir }
New-Item -ItemType Directory -Force -Path $OutDir | Out-Null
$ExePath = Join-Path $OutDir $ExeName
$PckPath = [System.IO.Path]::ChangeExtension($ExePath, ".pck")
$log = Join-Path $BuildRoot "export_log.txt"
Write-Output "[4] exporting: $ExePath"
$env:GODOT_NO_ATTACH_CONSOLE = "1"
# Godot writes its real diagnostics to stderr; with $ErrorActionPreference=Stop
# PowerShell turns each stderr line into a terminating NativeCommandError that
# kills the script before the artifact check runs. Drop to Continue for the call.
$ErrorActionPreference = "Continue"
& $GodotBin --headless --path $Project --export-release "Windows Desktop" $ExePath 2>&1 |
    Tee-Object -FilePath $log
$godotExit = $LASTEXITCODE
$ErrorActionPreference = "Stop"
if (-not (Test-Path $ExePath)) {
    Fail "export produced no exe (godot exit $godotExit, see $log)" "open $Project in the editor and fix the errors the log names"
}

# --- 5. verify + stamp + manifest + zip ---------------------------------------
$exeSize = (Get-Item $ExePath).Length
$pckOk = (Test-Path $PckPath)
$pckSize = 0
if ($pckOk) { $pckSize = (Get-Item $PckPath).Length }
if ($exeSize -lt 30MB) { Fail "exe too small: $exeSize bytes" "inspect $log; a stripped export means a broken template" }
# pck sanity floor is 10 KB, not 100 KB: The Mountain is pure GDScript with
# hand-drawn _draw rendering and zero art assets, so its compiled-script pack
# is ~95 KB. The exe floor (30 MB, the template runtime) is the real gate.
if (-not $pckOk -or $pckSize -lt 10KB) { Fail "pck missing or trivial (pck=$pckOk size=$pckSize)" "check binary_format/embed_pck=false in export_presets.cfg and rerun" }

# --- 5b. artifact identity: sha stamp the exe (R6) ---------------------------
# Trailer layout (must mirror core/boot_integrity.gd byte for byte):
#   [ exe ][ JSON payload ][ ASCII "MAGSTMP1" ][ u32 little-endian len(payload) ]
# The length is the FINAL 4 bytes so the boot code (and the stranger's
# python one-liner) can find the stamp from EOF without a scan.
$GitSha = (git -C $SourceRepo rev-parse HEAD 2>$null).Trim()
if (-not $GitSha) {
    Fail "cannot stamp: git rev-parse HEAD empty in $SourceRepo" "run from a git checkout (the stamp is the artifact's ID - no sha, no build)"
}
$gitShort = $GitSha.Substring(0, [Math]::Min(9, $GitSha.Length))
$ProjectRel = Split-Path -Leaf $Project
$dirtyRows = @(git -C $SourceRepo status --porcelain -- $ProjectRel 2>$null)
$dirty = if ($dirtyRows.Count -gt 0) { $dirtyRows.Count } else { 0 }
$pckSha = (Get-FileHash -Algorithm SHA256 -Path $PckPath).Hash.ToLower()
$builtUtc = [DateTime]::UtcNow.ToString("yyyy-MM-ddTHH:mm:ssZ")

# refuse a double stamp: a re-appended trailer would sit behind the payload
# and the boot code would read the INNER one as corrupt "GDPC-adjacent" bytes
$fs = [System.IO.File]::Open($ExePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Read)
$null = $fs.Seek(-12, [System.IO.SeekOrigin]::End)
$tail = New-Object byte[] 12
$null = $fs.Read($tail, 0, 12)
$fs.Close()
if ([System.Text.Encoding]::ASCII.GetString($tail, 0, 8) -eq $StampMagic) {
    Fail "exe already stamped (trailer magic present)" "the script wipes $OutDir at step 4; this canary means stamping logic ran twice on one exe"
}

$stamp = [ordered]@{
    v = 1
    git = $GitSha
    pck_sha256 = $pckSha
    built = $builtUtc
    source = $SourceLabel
}
if ($dirty -gt 0) { $stamp["dirty_files"] = $dirty }
$payloadJson = $stamp | ConvertTo-Json -Compress
$payloadBytes = [System.Text.Encoding]::UTF8.GetBytes($payloadJson)
if ($payloadBytes.Length -gt 4096) { Fail "stamp payload too big ($($payloadBytes.Length) B)" "shrink the stamp fields; boot code caps payloads at 4096" }
$magicBytes = [System.Text.Encoding]::ASCII.GetBytes($StampMagic)
$lenBytes = [BitConverter]::GetBytes([UInt32]$payloadBytes.Length)
if (-not [BitConverter]::IsLittleEndian) { [Array]::Reverse($lenBytes) }  # FileAccess.get_32 in GDScript is always LE
$fs = [System.IO.File]::Open($ExePath, [System.IO.FileMode]::Open, [System.IO.FileAccess]::Write)
$null = $fs.Seek(0, [System.IO.SeekOrigin]::End)
$fs.Write($payloadBytes, 0, $payloadBytes.Length)
$fs.Write($magicBytes, 0, $magicBytes.Length)
$fs.Write($lenBytes, 0, $lenBytes.Length)
$fs.Close()
$exeShaStamped = (Get-FileHash -Algorithm SHA256 -Path $ExePath).Hash.ToLower()
$stampedSize = (Get-Item $ExePath).Length
Write-Output "[5b] stamped exe: git=$gitShort pck_sha256=$($pckSha.Substring(0,12))... (+$($stampedSize - $exeSize) B trailer, source=$SourceLabel, dirty=$dirty)"

# --- 5c. manifest sidecar (ships in the zip; offline verification) -----------
$ManifestPath = Join-Path $OutDir "mountain-manifest.json"
@{
    stamp_version = 1
    source = $SourceLabel
    source_git = $GitSha
    source_dirty_files = $dirty
    built_utc = $builtUtc
    exe = $ExeName
    exe_sha256 = $exeShaStamped
    pck = "TheMountain.pck"
    pck_sha256 = $pckSha
    boot_check = "TheMountain.exe --headless --quit-after 2  (expect 'ARTIFACT_ID ... pck=ok', exit 0)"
} | ConvertTo-Json | Set-Content -Encoding ASCII $ManifestPath
Write-Output "[5c] manifest: $ManifestPath"

# --- 5d. boot smoke: run the stamped exe, identity must print + exit 0 -------
$smokeLog = Join-Path $BuildRoot "boot_smoke.txt"
$ErrorActionPreference = "Continue"
$bootOut = & $ExePath --headless --quit-after 2 2>&1 | Tee-Object -FilePath $smokeLog
$bootExit = $LASTEXITCODE
$ErrorActionPreference = "Stop"
$bootText = ($bootOut | Out-String)
if ($bootExit -ne 0) {
    Fail "stamped exe boot smoke exit $bootExit (see $smokeLog)" "the game refused its own fresh artifact - read the ARTIFACT_ID line in the log"
}
$ids = @($bootOut | Where-Object { "$_" -match '^ARTIFACT_ID' })
if ($ids.Count -eq 0) {
    Write-Output "[5d] boot smoke: exit 0 but no ARTIFACT_ID captured (GUI subsystem swallowed stderr); exit code stands as the signal"
} elseif (-not ($ids -join ' ' -match 'pck=ok')) {
    Fail "boot smoke ARTIFACT_ID line present but not pck=ok: $($ids -join ' | ')" "stamp/pck mismatch on a fresh build - do not ship; read $smokeLog"
} else {
    Write-Output "[5d] boot smoke: $($ids[0])"
}

# --- 5e. zip + fresh unzip ----------------------------------------------------
$ZipPath = Join-Path $BuildRoot "mountain-$gitShort$(if ($FromTheMountain) {'-mt'}).zip"
if (Test-Path $ZipPath) { Remove-Item -Force $ZipPath }
Compress-Archive -Path (Join-Path $OutDir "*") -DestinationPath $ZipPath
$zipSize = (Get-Item $ZipPath).Length

# fresh unzip check
$verifyDir = Join-Path $env:TEMP "mountain_verify_$PID"
if (Test-Path $verifyDir) { Remove-Item -Recurse -Force $verifyDir }
Expand-Archive -Path $ZipPath -DestinationPath $verifyDir
$vExe = Test-Path (Join-Path $verifyDir $ExeName)
$vPck = Test-Path (Join-Path $verifyDir ($ExeName -replace '\.exe$', '.pck'))
$vMan = Test-Path (Join-Path $verifyDir "mountain-manifest.json")
Remove-Item -Recurse -Force $verifyDir -ErrorAction SilentlyContinue
if (-not ($vExe -and $vPck -and $vMan)) { Fail "fresh unzip missing exe/pck/manifest (exe=$vExe pck=$vPck manifest=$vMan)" "rerun the script; if it persists inspect $ZipPath by hand" }

Write-Output ""
Write-Output "PASS: build verified + stamped"
Write-Output "  exe     : $ExePath ($([math]::Round($stampedSize/1MB,1)) MB, sha256 $exeShaStamped)"
Write-Output "  pck     : $PckPath ($([math]::Round($pckSize/1KB,1)) KB, sha256 $pckSha)"
Write-Output "  zip     : $ZipPath ($([math]::Round($zipSize/1MB,1)) MB)"
Write-Output "  identity: git $gitShort ($SourceLabel) built $builtUtc dirty_files=$dirty"
Write-Output "  manifest: $ManifestPath"
Write-Output ""
Write-Output "STRANGER'S CHECK (no Godot needed), from the unzipped folder:"
Write-Output "  python -c `"import json,hashlib;f=open('$ExeName','rb');import sys;f.seek(-4,2);L=int.from_bytes(f.read(4),'little');f.seek(-12,2);m=f.read(8);f.seek(-12-L,2);s=json.loads(f.read(L));p=hashlib.sha256(open('TheMountain.pck','rb').read()).hexdigest();print('MOUNTAIN',('OK' if m==b'MAGSTMP1' and p==s['pck_sha256'] else 'FAIL'),s['source'],s['git'])`""
Write-Output "  or run it: .\$ExeName --headless --quit-after 2   (expect ARTIFACT_ID ... pck=ok, exit 0)"
exit 0
