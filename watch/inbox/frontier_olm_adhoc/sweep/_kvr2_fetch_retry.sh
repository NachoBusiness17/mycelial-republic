#!/bin/bash
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/131.0 Safari/537.36"
fetch() {
  out="$1"; id="$2"
  for i in 1 2 3 4; do
    curl -s --max-time 30 -A "$UA" -H "Accept: application/atom+xml" -o "$out" "https://www.reddit.com/comments/$id/.rss?limit=100"
    sz=$(stat -c %s "$out" 2>/dev/null || echo 0)
    if [ "$sz" -gt 3000 ]; then echo "OK $out $sz"; return 0; fi
    echo "retry $out (size $sz)"; sleep 15
  done
  echo "FAIL $out"
}
fetch _kvr2_thread_1wnedrc.xml 1wnedrc; sleep 14
fetch _kvr2_thread_1wyf63m.xml 1wyf63m; sleep 14
fetch _kvr2_thread_1whf345.xml 1whf345; sleep 14
fetch _kvr2_thread_1wjhk0r.xml 1wjhk0r
echo DONE
