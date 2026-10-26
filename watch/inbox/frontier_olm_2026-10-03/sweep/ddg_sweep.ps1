$ErrorActionPreference = 'Continue'
$ProgressPreference = 'SilentlyContinue'
$work = 'C:\Users\foste\Documents\projects\local_sovereign_agent\watch\inbox\frontier_olm_2026-10-03\sweep'
$ua = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'

function Decode-DDG([string]$href) {
  if ($href -match 'uddg=([^&]+)') {
    return [uri]::UnescapeDataString($Matches[1])
  }
  return $href
}

$queries = @(
  'site:reddit.com/r/LocalLLaMA "KV cache"',
  'site:reddit.com/r/LocalLLaMA prefix caching vLLM',
  'site:reddit.com lost in the middle long context degradation',
  'site:reddit.com prompt compression LLMLingua cost',
  'site:reddit.com KV cache eviction agentic tools',
  'site:reddit.com/r/LocalLLaMA KIVI quantized KV cache',
  'site:reddit.com/r/LocalLLM ollama context window memory',
  'site:reddit.com/r/MachineLearning context rot long context',
  'site:reddit.com llama.cpp cache-type-k q8_0 KV quantization',
  'site:reddit.com "KV cache" reuse across sessions agent'
)

foreach ($q in $queries) {
  $url = 'https://html.duckduckgo.com/html/?q=' + [uri]::EscapeDataString($q)
  try {
    $resp = Invoke-WebRequest -Uri $url -UserAgent $ua -TimeoutSec 30
    $html = $resp.Content
    $rx = [regex]'(?s)<a[^>]*class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>'
    $snipRx = [regex]'(?s)class="result__snippet"[^>]*>(.*?)</a>'
    $ms = $rx.Matches($html)
    $snips = $snipRx.Matches($html)
    Write-Output ("=== Q: {0} : HTTP {1} : {2} results ===" -f $q, $resp.StatusCode, $ms.Count)
    for ($i = 0; $i -lt [Math]::Min(8, $ms.Count); $i++) {
      $t = $ms[$i].Groups[2].Value -replace '<[^>]+>','' -replace '&amp;','&'
      $u = Decode-DDG $ms[$i].Groups[1].Value
      $s = ''
      if ($i -lt $snips.Count) { $s = $snips[$i].Groups[1].Value -replace '<[^>]+>','' -replace '&amp;','&' -replace '&#x27;',"'" }
      if ($s.Length -gt 200) { $s = $s.Substring(0,200) }
      Write-Output ("[{0}] {1} :: {2} :: {3}" -f ($i+1), $t.Trim(), $u, $s.Trim())
    }
  } catch {
    Write-Output ("=== Q: {0} : FAILED : {1} ===" -f $q, $_.Exception.Message)
  }
  Start-Sleep -Seconds 3
}

# RSS doors for the four subreddits
foreach ($sub in @('LocalLLaMA','MachineLearning','LocalLLM','ollama')) {
  try {
    $r = Invoke-WebRequest -Uri ("https://old.reddit.com/r/" + $sub + "/top/.rss?t=month") -UserAgent $ua -TimeoutSec 30
    $file = Join-Path $work ("rss_" + $sub + ".xml")
    [IO.File]::WriteAllBytes($file, $r.RawContentStream.ToArray())
    $titles = [regex]::Matches($r.Content, '<entry>.*?</entry>', 'Singleline').Count
    Write-Output ("=== RSS {0} : HTTP {1} : {2} entries ===" -f $sub, $r.StatusCode, $titles)
  } catch {
    Write-Output ("=== RSS {0} : FAILED : {1} ===" -f $sub, $_.Exception.Message)
  }
  Start-Sleep -Seconds 2
}
