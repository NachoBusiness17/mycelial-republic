# Sweep: open-local-language-models via reddit - 2026-10-05

source-fetched: 2026-10-05
seat: sweep-open-local-language-models-reddit (workflow subagent, actor_3_3)
instrument: WebFetch + WebSearch only; every quote below came from a page fetched in this session.

## Doors scoreboard (RQ4 - closes the lens/doors.md OWED)

| Door | Recipe probed this session | Result |
|---|---|---|
| old.reddit.com JSON | `old.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` | BLOCKED: HTML "Welcome to Reddit" login-wall, no kind/data (matches lens/doors.md Door 3 finding) |
| www.reddit.com JSON | `www.reddit.com/r/LocalLLaMA/top.json?t=month&limit=50` | HTTP 403 Blocked (Retry-After: 0) |
| oauth.reddit.com (no bearer) | `oauth.reddit.com/r/LocalLLaMA/top?t=month&limit=50` | HTTP 403 Blocked (unauthenticated probe; requires real OAuth credentials, which this seat does not have) |
| web_reader tool on old.reddit | same URL via mcp webReader | login-wall HTML again ("Log in to use old Reddit") |
| pullpush.io mirror | `api.pullpush.io/reddit/search/submission/?subreddit=LocalLLaMA...` | HTTP 429 Too Many Requests |
| redlib.catsarch.com mirror | `/r/LocalLLaMA/top/?t=month` | HTTP 429 Too Many Requests |
| **safereddit.com mirror** | `safereddit.com/r/LocalLLaMA/top/?t=month` + `/comments/<id>/` | **WORKS.** Full monthly top listing (25 posts) and full threads readable; no auth, no key. This is the verified recipe. |

**Door verdict:** no recipe returned actual Reddit JSON today without credentials; oauth/www/old are all blocked unauthenticated and pullpush+one redlib 429'd. The verified working access recipe is the **safereddit.com mirror** (readable HTML, threads and scores intact). Closes `watch/inbox/frontier_olm_2026-10-05/lens/doors.md` OWED #1 with the caveat: mirror HTML, not JSON; a JSON-shaped answer still needs a real OAuth credential the estate does not currently hold. Subdirs probed through the mirror: r/LocalLLaMA, r/ollama, r/LocalLLM.

## Pass 1 broad sweep (30+ candidates considered, last 30 days)

From r/LocalLLaMA month top (safereddit mirror, 25 read): Jev architecture open-sourced (1wijo3e, 3.5k) [estate has memory/runs/jev_salon/ - overlap, skipped]; HF security.txt (1wdbvlt); fear-mongering/regulation meta (1wk979c); Anthropic GLM ad (1wth4iz); $9K RTX 5090 alternatives (1whf7ov); **Qwen 4 Announced at Apsara (1wmxfjs)**; iPhone second GPU (1wvz1ex); Qwen-Image-2.1 (1wlgrft); **DeepSeek V4-1 Flash is out (1wcbid7)**; **Ternary Bonsai 2 27B <6GB WebGPU (1wj6c4l)**; Jev dupe (1wihgum); OpenAI math accusations (1wapjaw); subsidised-compute meta (1wt5f4e); Alibaba medical AI (1wk9fag); Jev advertising meta (1wo6o0f); **Friends Don't Let Friends Use Ollama (1wa26pn)**; Mozilla: China open-weight 4 months behind (1wi32jg); frontier-model-self-torrent meta (1wkocvj); DeepSeek soft-retires V4 Pro (1wbfrut); AMD 256-core EPYC 16ch DDR5-12800 (1wtc4j9); golden-era meta (1wf3i1m); OpenAI training-data accusations (1wcmgbn).

From r/ollama month top (15 read): **400+ LLM agents on Qwen3-4B (1wt0tot)**; claude-cowork replica (1wboy1g); **Qwen 3.8 27B M4 Max benchmark (1wvxih5)**; stopped-using-smartest-models (1wjnkgm); Ollama-vs-runners explainer (1wiijww); NotebookLM alternative (1wms2s9); wtf-happened-to-ollama (1wa3zax); DwarfStar compression (1wx0jtb); 27B creative-writing open weights (1wlh7us); **hallucination detection 1.5B-120B (1wdasar)**; Mac Mini M4 server (1wq653p); DeepSeek v4.1 Flash praise (1wd8xc7); **unswallow: Qwen3 tool calls stuck in <think> (1wc6tka)**.

From r/LocalLLM month top (15 read): **Qwen4-27B just confirmed (1wmzky1, 2307pts)**; 1B driving assistant (1wp3vnh); uncensored models (1wffmri); 4x RTX PRO 6000 build (1w88rhz); **30 days of Qwen 3.8 27B (1whqwdq)**; Blackwell Pro 5k 48GB (1wpfxje); hemmingway-1 27B (1wlhh08); hardware acquisition (1wr8et1); **Gemma 5 - what to expect (1wuqsyy)**; GPT 5.6 vs Qwen 3.8 27B (1w8q5yd); huggingface_hub agent fingerprinting (1wehgvc); 40GB VRAM Qwen 27b home server dual 3080s (1wdramg); vram.wiki thread (1wf4y1qe).

From arXiv export API (`all:"local llm"`, totalResults 170, freshest 15): SoftGene (2610-02), Innocent Courier exfil (2026-10-01), multilingual privacy tagging (2026-09-29), two-confidence-gated local LLM judges (2026-09-27), LA-CPD (2026-09-27), **HESP alert-triage agents (2026-09-27)**, poisoning scaling exponents (2026-09-26), **Checkability Boundary (2026-09-25, 2609.31540)**, agent trace tampering (2026-09-24), SambaGraph (2026-09-22), Illusion of Local Privacy (2026-09-16), JustFit MLX serving (2026-09-15).

## Pass 2 deep reads (8 fetched end to end)

1. Ternary Bonsai 2 (r/LocalLLaMA 1wj6c4l, ~2026-09-18, 1.7k up / 344 comments)
2. Qwen 4 Announced (r/LocalLLaMA 1wmxfjs, ~2026-09-22, 2.1k / 568)
3. DeepSeek V4-1 Flash is out (r/LocalLLaMA 1wcbid7, ~2026-09-10, 1.7k / 297)
4. Friends Don't Let Friends Use Ollama (r/LocalLLaMA 1wa26pn, ~2026-09-08, 1.3k / 385)
5. Checkability Boundary (arXiv 2609.31540, 2026-09-25)
6. unswallow tool-calling thread (r/ollama 1wc6tka, ~2026-09-10)
7. 30 days of Qwen 3.8 27B (r/LocalLLM 1whqwdq, ~2026-09-16)
8. iPhone second GPU (r/LocalLLaMA 1wvz1ex, ~2026-10-03)

## Answers to the five research questions

**RQ1 (open-weight 7B-70B releases reshaping the ladder, at what VRAM).** The month's releases point one way: the 27B dense slot is the new ladder hinge. Qwen 4 keeps an exact 27B dense ("27b is the goat that keeps on giving", 122pts) targeted at 24-32GB VRAM; thread consensus: dual R9700 (32GB) runs 27B at Q8 with healthy context, a 12GB RTX 3060 fits IQ3_XS + Q4 KV at 96K context, Strix Halo decodes 43-50 t/s on Flash-Next. DeepSeek V4-1 Flash (552B backbone MoE, ~8B active prefill / 16B decode, native FP4 incl KV, ~196B of it n-gram "Engram" memory) needs ~310GB in 4-bit - it does not move the janitor tiers, it re-confirms "remote specialist scarce" for the big-MoE ceiling (ttkciar: "I couldn't host this on my 256GB Xeon server. I'd have to upgrade it to 384GB."). Ternary Bonsai 2 collapses the 27B class to <6GB (browser/WebGPU territory) - the janitor footprint can now carry a 27B, with the community's 98.2%-intelligence claim disputed in-thread (289pts comment: figure likely vs the 2-bit quant, not FP16).

**RQ2 (who beats the gemma:2b scut / gemma4 short-worker on tool-call shape at the same footprint).** Partially answered; a direct gemma-vs-Qwen tool-call bench was NOT found in anything I read - the closest primary evidence: (a) unswallow thread: Qwen3-class small models DO emit tool calls but engines (llama.cpp/vLLM/SGLang) can leave them swallowed inside `<think>`; recovery is mechanical, not model-bound; (b) 30-day Qwen 3.8 27B: "poisoned tool calls" loop-and-spam failure at >100k context, cured by harness loop-detection + deleting bad calls; one commenter ran "several million tokens with Qwen 3.8 27b at fp8 and no issues with tool calls"; (c) r/ollama pass-1: 400+ concurrent agents live on Qwen3-4B Q4_K_M at 4k context. WebSearch-only (weaker, unverified by page fetch): BFCL V4 board still names Qwen2.5-7B-Instruct the strongest small open function-caller. OWED for the estate: run our own kitchen A/B - gemma4 vs Qwen3.8-4B/8B vs Bonsai-2-27B on the janitor's actual tool JSON - no public thread does it for us.

**RQ3 (freshest arXiv: small local models as agent executors vs hosted API).** The proven door re-proved: totalResults 170 unchanged; the freshest results converge on "local-first with escalation": Touchstone/Checkability Boundary (2609.31540) runs seven 1-8B SLMs with cheap deterministic checks, hits 98.6%/93.8% on conflict detection/intent translation while escalating only 16%/17% to a frontier model - and fails on TeleQnA where no intrinsic check exists. HESP (2026-09-27) adds that an external controller managing what-to-probe/when-to-stop is what makes small local LLMs viable in triage. Side findings: local inference does not guarantee prompt confidentiality (Illusion of Local Privacy, 2026-09-16, includes a llama.cpp flaw) and most agent harnesses let agents delete their own traces (2026-09-24). Doctrine match: this is exactly the estate's janitor-first + deliberate-ask shape, now with peer-reviewed numbers.

**RQ4 (the access recipe).** Answered above: safereddit.com mirror is the only door that returned content; all three official JSON doors are blocked unauthenticated. Recorded for doors.md.

**RQ5 (mine/raw rows).** I ran `.\.venv\Scripts\python.exe watch\inbox\frontier_olm_2026-10-05\sweep\_mineraw_scan.py` (the RQ5 instrument already in today's sweep dir). It reads `mine\raw` as 5 subdirs (agent_bleeding_edge 15,759 files/1.41GB; agent_platform 75,279/3.95GB; mesh_comm 5,685/161MB; narrative_corpus 1,816/55MB; steal_protocol 4,494/152MB) and counts **56,613,549 rows - not 97,865** - and the samples are code-repo files (.gitignore/.dockerignore/.editorconfig), i.e. a code mirror, not a social-scrape row store. Staleness boundary measured: only 84 date-bearing lines, row-date range 2024-01-15..2026-06-18; oldest file mtime 2026-08-05T12:56Z; newest mtime is my own session's .mimosa hook-state (scan contamination, not estate content). Verdict: **mine/raw cannot answer any current best-local-model question** - it contains no model-eval rows, and nothing in it postdates the last 60 days of releases (Qwen4 ~09-22, V4-1 Flash ~09-10, Bonsai 2 ~09-18). The ask's 97,865 figure did not reproduce with this instrument; treat it as OWED-verify against whichever counter produced it.

## Ladder implications (feeds RIB_DRIVING_LADDER)

1. Janitor tier: keep gemma:2b scut, but the short-worker slot has two upgrade candidates at same-or-less footprint: Qwen3-4B-class (proven at 400-agent scale, with unswallow-style think-tag recovery in the harness) and Ternary Bonsai 2 27B (<6GB) IF the 98.2% claim survives our own kitchen check.
2. The 24GB "prosumer judgment" rung is real now: Qwen 3.8 27B UD-Q4_K_XL does 845 t/s mean prefill / 74 t/s mean decode on a 5070Ti+4070S, and 24GB Mac + spare iPhone prefills 29-44% faster. A local 27B undercuts paid-judgment dispatch for medium asks - route per the driving ladder, but the local 27B is now a legitimate SHERPA-cheap baseline before any $0.4+ ask.
3. Remote-specialist tier stays scarce by construction: 552B MoE needs ~310GB; nothing consumer-side closes that gap this month (AMD EPYC DDR5 thread is bandwidth-relevant but untested for us).
4. Harness laws to steal: escalation-only-when-uncheckable (arXiv), think-tag tool-call recovery, poisoned-call loop-breaker, delete-bad-tool-calls-from-context - all four map onto existing gate/lanes code.

## Overlap ledger (grep instrument: `grep -c` on catalog/catalog.jsonl + `grep -r -l` on memory/)

- DeepSeek-V4.1: catalog 14 hits; memory/behavioral/animals/deepseek_v4_1_flash.jsonl exists - HEAVY overlap, banked last, only the local-footprint comment deltas are new.
- Ternary Bonsai: catalog 1 hit; memory/runs/gapwave/splash_bonsai_livetranslate_verified_20260920.md (Bonsai 1) - partial; Bonsai 2 release itself new.
- Checkability: catalog 1 hit; memory/percolator/candidates.jsonl - paper already cataloged; escalation-rate framing is the delta.
- Jev architecture: catalog 0 but memory/runs/jev_salon/ exists - skipped as known.
- Qwen 4 / Qwen4-27B: catalog 0 (memory socratic_mesh mentions only) - new.
- unswallow, Friends-don't, Qwen 3.8 27B 30-day, iPhone-second-GPU (backburner/StayLameBro): catalog 0 - new.

## OWED / not run

- BFCL leaderboard page (gorilla.cs.berkeley.edu/leaderboard.html): fetch TIMED OUT at 60s - leaderboard claims above rest on WebSearch summaries only, not page-verified.
- oauth.reddit.com with a real bearer token: untested - no credentials in this seat.
- 97,865-row provenance for mine/raw: not found on disk; OWED.
- Gemma 5 thread (1wuqsyy) and Qwen3-4B 400-agent thread (1wt0tot): pass-1 only, not deep-read, not banked as items.
