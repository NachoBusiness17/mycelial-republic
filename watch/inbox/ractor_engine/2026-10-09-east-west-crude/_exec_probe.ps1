$root = 'C:\Users\foste\.zcode\cli\exec'
$dirs = Get-ChildItem $root -Directory
$tot = 0.0; $cnt = 0
foreach ($d in $dirs) {
  $s = Get-ChildItem $d.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum
  $tot += $s.Sum; $cnt += $s.Count
}
'exec total GB: {0:N2}  files: {1}  session dirs: {2}' -f ($tot/1GB), $cnt, $dirs.Count
foreach ($pat in @('sess_dwf-dwfrun-ce3840bf*','sess_dwf-dwfrun-45632c53*')) {
  $sd = Get-ChildItem ($root + '\' + $pat) -Directory -ErrorAction SilentlyContinue
  $t = 0.0; $c = 0
  foreach ($d in $sd) {
    $s = Get-ChildItem $d.FullName -Recurse -File -ErrorAction SilentlyContinue | Measure-Object Length -Sum
    $t += $s.Sum; $c += $s.Count
  }
  '{0}  GB: {1:N2}  files: {2}  dirs: {3}' -f $pat, ($t/1GB), $c, @($sd).Count
}
