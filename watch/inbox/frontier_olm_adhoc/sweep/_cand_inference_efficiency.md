# inference-efficiency reddit sweep - candidate tracker (pass 1)

Door state 2026-10-11: old.reddit login-walled; www.reddit .json walled (curl+reader); DDG/Mojeek/pullpush/jina dead;
webReader www.reddit HTML = titles only + flaky interstitial; PER-THREAD .rss via curl WORKS (full post+comments Atom).
Wayback CDX 504. Discovery = WebSearch (quoted-title phrasing) + webReader listing titles + Bing-via-webReader.

| # | title (as surfaced) | sub | source of lead | canonical URL | date | status |
|---|---|---|---|---|---|---|
| 1 | Speculative decoding question, 665% speed increase | LocalLLaMA | WebSearch | .../comments/1sq7grd/speculative_decoding_question_665_speed_increase/ | 2026-04-19 | READ via RSS (outside 30d; background only) |
| 2 | The state of self-hosting LLMs in 2026 | LocalLLaMA | webReader top/month | 1x0i4sq DEAD (page not found) | Oct 1 2026 (listing) | resolve URL |
| 3 | GPU enhanced micro API containers for LLM | ollama | webReader top/month | 1x1jj5g (unverified) | recent | resolve |
| 4 | What is the most efficient model you've used with... | LocalLLM | webReader top/month | 1x2pp5u (unverified) | recent | resolve |
| 5 | [P] Local research agent idea | MachineLearning | webReader top/month | 1x2mk67 (unverified) | recent | resolve |
| 6 | Jev architecture thread | LocalLLaMA | webReader top/month | unknown | ~Oct | resolve |
| 7 | PewDiePie released a free LLM | LocalLLaMA | webReader top/month | unknown | ~Oct | resolve (low priority) |
| 8 | HF security.txt | LocalLLaMA | webReader top/month | unknown | ~Oct | low priority |
| 9 | I tested all llama.cpp's speculative decoding methods on Qwen 3.6 | LocalLLaMA | WebSearch related-blurb | unknown | ? | resolve - RQ1 priority |
| 10 | Speculative Decoding: My findings | LocalLLaMA | WebSearch | 1hmmmdg | 2025-01 | old, background |
