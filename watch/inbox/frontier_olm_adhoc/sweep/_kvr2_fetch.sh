#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
fetch() {
  out="$1"; url="$2"
  for i in 1 2 3; do
    curl -s --max-time 25 -A "$UA" -H "Accept: application/atom+xml" -o "$out" "$url"
    sz=$(stat -c %s "$out" 2>/dev/null || echo 0)
    if [ "$sz" -gt 2000 ]; then echo "OK $out $sz"; return 0; fi
    echo "retry $out (size $sz)"; sleep 12
  done
  echo "FAIL $out"
  return 1
}
fetch _kvr2_top_llama.xml "https://www.reddit.com/r/LocalLLaMA/top/.rss?t=month&limit=50"; sleep 10
fetch _kvr2_top_llm.xml "https://www.reddit.com/r/LocalLLM/top/.rss?t=month&limit=50"; sleep 10
fetch _kvr2_top_ollama.xml "https://www.reddit.com/r/ollama/top/.rss?t=month&limit=50"; sleep 10
fetch _kvr2_top_ml.xml "https://www.reddit.com/r/MachineLearning/top/.rss?t=month&limit=50"; sleep 10
fetch _kvr2_s1_evict.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=kv+cache+eviction&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s2_evict2.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=eviction+prefix&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s3_quant.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=cache+quantization+q8&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s4_quantref.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=quantization+quality+degradation&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s5_compact.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=context+compaction&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s6_hit.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=cache+hit+rate&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s7_prompt.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=prompt+caching+agents&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s8_llmkv.xml "https://www.reddit.com/r/LocalLLM/search/.rss?q=kv+cache&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s9_lost.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=model+forgets+context&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s10_tool.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=tool+calls+context+window&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s11_mlkv.xml "https://www.reddit.com/r/MachineLearning/search/.rss?q=kv+cache+compression&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s12_refusal.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=quantization+refusal&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s13_ollama.xml "https://www.reddit.com/r/ollama/search/.rss?q=context+kv&restrict_sr=on&sort=top&t=month"; sleep 10
fetch _kvr2_s14_rr.xml "https://www.reddit.com/r/LocalLLaMA/search/.rss?q=round+robin+cache&restrict_sr=on&sort=top&t=month"
echo DONE
