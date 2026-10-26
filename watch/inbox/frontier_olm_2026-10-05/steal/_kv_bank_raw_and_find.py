# REV 2 scratch: bank the raw fxtwitter JSON + the ask's find JSON (R4), measure text chars (R5).
import json
import urllib.request
from pathlib import Path

RAW = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/watch/inbox/frontier_olm_2026-10-05/sweep/_raw")
req = urllib.request.Request("https://api.fxtwitter.com/theo/status/2100762304862384257", headers={"User-Agent": "curl/8"})
body = urllib.request.urlopen(req, timeout=25).read()
(RAW / "fx_theo_2100762304862384257.json").write_bytes(body)
d = json.loads(body)
tw = d["tweet"]
text = tw["text"]
print("banked bytes:", len(body), "| author:", tw.get("author", {}).get("screen_name"), "| created:", tw.get("created_at"))
print("measured text chars (this fetch, from banked file):", len(text))
print("60% fragment present:", "cache write costs go over 60%" in text)
print("delete-2 fragment present:", "you have to rewrite" in text)

find = {
    "title": "Theo: compaction is not a filter; cache writes dominate agent spend",
    "url": "https://x.com/theo/status/2100762304862384257",
    "date": "2026-09-18",
    "quote": "Cache writes are the biggest cost by far for agents. I often see cache write costs go over 60% of my total LLM spend in my personal use of Claude Code and Codex.",
    "why": "Quantifies why the estate's frozen-prefix law is the paid-turn cost lever: every mid-history edit forces a cache rewrite of everything after the edit point, so per-tool-call trimming is self-defeating; direct feed for the descent protocol's prompt-shape leg.",
    "overlap": "grep 'cache writes are more expensive' vs catalog:0, memory (md minus agent_sessions): none; new. Related but distinct: watch/inbox/burn_reset_20260927/flash50/w3-research-cachemech.md:151-169 holds the frozen-prefix mechanism itself.",
    "confidence": 0.97,
    "area": "kv-cache-context-engineering via x",
    "source": "x.com via fxtwitter JSON door (curl, code 200 on all resolves), discovered through Latent Space AINews editions (RSS feed https://www.latent.space/feed?sectionId=327741) plus live provider docs (platform.claude.com, developers.openai.com)",
    "banked_by": "REV 2: banked verbatim from the round-2 ask find array (the confidence 0.97 carrier)",
}
p = RAW / "find_theo_2100762304862384257.json"
p.write_text(json.dumps(find, ensure_ascii=True, indent=2), encoding="utf-8")
print("find JSON banked:", p.name, "| confidence field:", find["confidence"])
