# hermes_driver.ps1 - 24/7 hermes on free lanes (2026-10-06)
# Pulled by Task Scheduler every N minutes. Reads work from the queue,
# fires hermes headless, files results to the board. Free lanes only.
$ErrorActionPreference = 'Continue'

$BOARD = 'C:\Users\etfag\.zcode\workspace\default'
$QUEUE = "$BOARD\seats\hermes\QUEUE.md"
$RESULTS = "$BOARD\seats\hermes\RESULTS"
$LOG = "$BOARD\seats\hermes\driver.log"
$HERMES = "$env:LOCALAPPDATA\hermes\bin\hermes.exe"

function Log($msg) {
    $ts = Get-Date -Format 'yyyy-MM-ddTHH:mm:ssZ'
    Add-Content $LOG "[$ts] $msg"
}

# Ensure results dir exists
New-Item -ItemType Directory -Force -Path $RESULTS | Out-Null

# Read the next unclaimed task from the queue
if (-not (Test-Path $QUEUE)) {
    Log "no queue file, idle"
    exit 0
}

$tasks = Get-Content $QUEUE
$claimed = $false
$task_text = ''
$task_id = ''

foreach ($line in $tasks) {
    if ($line -match '^\s*\[ \]\s*(.+)$') {
        $task_text = $Matches[1]
        $task_id = "h$(Get-Date -Format 'yyyyMMdd-HHmmss')"
        $claimed = $true
        # Mark as claimed (append-only: write new status below, don't rewrite)
        Add-Content $QUEUE "[~] $task_text  # CLAIMED $task_id $(Get-Date -Format 'o')"
        break
    }
}

if (-not $claimed) {
    Log "queue empty, idle"
    exit 0
}

Log "firing task ${task_id}: ${task_text}"

# Fire hermes headless
# The prompt wraps the task in the estate's context (board awareness)
$prompt = @"
You are Hermes, driven by the ZCode seat's 24/7 driver. Read the board first:
- Board: type the file $BOARD\SEAT_AWARENESS.md
- Your notices: type $BOARD\seats\hermes\NOTICES.md
- Then execute this task to the best of your ability:

$task_text

File your result to $RESULTS\${task_id}.md (write the file directly).
Tri-state all claims. No secrets. Plain language, no em-dashes.
"@

try {
    $output = & $HERMES -p $prompt --always-approve --output-format text 2>&1 | Out-String
    Log "task ${task_id} completed, output length: $($output.Length)"
    # Save raw output as fallback if hermes didn't write the result file
    if (-not (Test-Path "$RESULTS\$task_id.md")) {
        Set-Content "$RESULTS\$task_id.md" $output -Encoding utf8
        Log "hermes didn't self-file; saved raw output"
    }
    # Mark as done in the queue (append)
    Add-Content $QUEUE "[x] $task_text  # DONE $task_id $(Get-Date -Format 'o')"
} catch {
    Log "task ${task_id} FAILED: $($_.Exception.Message)"
    Add-Content $QUEUE "[!] $task_text  # FAILED $task_id $(Get-Date -Format 'o')"
}

Log "cycle complete, exiting"
