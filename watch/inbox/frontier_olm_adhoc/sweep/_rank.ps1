param([string]$Pattern, [int]$Top = 45)
$rows = @()
foreach ($f in (Get-Item $Pattern)) {
    $j = Get-Content $f.FullName -Raw | ConvertFrom-Json
    if ($j.data) { $rows += $j.data }
}
# dedupe by id
$rows = $rows | Sort-Object id -Unique
$rows | Sort-Object score -Descending | Select-Object -First $Top | ForEach-Object {
    $d = [DateTimeOffset]::FromUnixTimeSeconds([long]$_.created_utc).ToString('yyyy-MM-dd')
    '{0,5} | {1,4}c | {2} | {3} | https://reddit.com{4}' -f $_.score, $_.num_comments, $d, $_.title, $_.permalink
}
