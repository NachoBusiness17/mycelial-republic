$t = Get-Content 'watch\inbox\frontier_olm_2026-10-02\steal\evals-self-improvement via x.md' -Raw
Write-Output ("chars: " + $t.Length)
Write-Output ("em-dash count: " + ([regex]::Matches($t, [char]0x2014)).Count)
Write-Output ("en-dash count: " + ([regex]::Matches($t, [char]0x2013)).Count)
