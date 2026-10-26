$ErrorActionPreference = 'SilentlyContinue'
$f = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-02\sweep\quantization-compression-reddit.md'
$hits = Select-String -Path $f -Pattern 'phantom' -SimpleMatch
foreach ($h in $hits) { Write-Output ("LINE {0}: {1}" -f $h.LineNumber, $h.Line) }
