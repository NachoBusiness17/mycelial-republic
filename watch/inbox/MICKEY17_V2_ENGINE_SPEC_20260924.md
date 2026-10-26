# MICKEY-17 v2 — FRONTIER-BURN ENGINE SPEC

> **SUPERSEDED 2026-09-25** by `MICKEY17_V2_ENGINE_SPEC_v2.1_20260925.md` (amendments A1–A12 applied; see that file's changelog). Preserved unmodified as the v2 record — its lane-archive paths are relative and stale by A1; the archive of record now lives at `memory/runs/mickey17_v2/lanes/`.

Formalized 2026-09-25 from the first dogfood run. Inputs of record: the 50 lane backups at `mickey17_v2/lanes/*.json` (their note fields carry the observed failure modes), the master fold `mickey17_v2/MASTER_MICKEY17_V2_20260924.md`, and the estate's original Mickey 17 receipts at `memory/runs/mickey17/` (folded 2026-09-20). Every count in this spec was recounted by script from the lane files during formalization: 50 lane files, 246 rows, estate_status split 96 confirms-ours / 61 owed / 48 we-have-better / 41 new; 246/246 rows carry non-empty `quote`, `source`, `steal`, and `estate_status` (leverage: 118 high / 121 medium / 7 low).

---

## 1. PURPOSE

MICKEY-17 v2 is the estate's frontier-burn engine: for one topic, it fans out a fixed width of cheap parallel lanes across the live frontier (papers, vendor engineering blogs, OSS repos, operator forums), drags every claim home as a register row bound to a verbatim quote and a URL, rules honestly on contradictions instead of averaging them, folds the register into one master document whose numbers are recounted by script rather than trusted from any agent's self-report, then files itself back into the estate so the next run starts from a spec instead of a memory. It is named for the v1 run of 2026-09-20 (`memory/runs/mickey17/`), which pointed the same shape inward: a `digestion` agent in refill batches produced 72 register slices (`digest_canon/inbox/mem/rp/watch_*` files — the brief's "~74" rounds this; 72 digest files + 1 master index are on disk) covering 2,493 estate files, folded by script ("Recounted by script from 72 register files", `MASTER_INDEX_20260920.md:3`). v2 runs the identical register-and-recount discipline outward at the moving frontier. The first dogfood (2026-09-24/25) burned 50 lanes in roughly 65 minutes of wall clock and returned 246 verified rows.

## 2. INTERFACE

One invocation takes three arguments:

```json
{
  "topic": "one-line statement of what this burn is stealing for",
  "targets": [
    { "id": "short-lane-name", "what": "the source or source-family to mine", "start": "https://absolute/start/url" }
  ],
  "width": 50
}
```

- **`topic`** — one line, the burn's objective. It prefixes every lane prompt.
- **`targets[]`** — one target per lane. `id` names the lane and becomes the backup filename `<id>.json`. `what` describes the primary source or family (a paper, a vendor blog, a repo, a forum month-window). `start` is the absolute start URL; it is optional — a lane may start from search when no single URL exists (observed: `kv-agents-week` and `verifier-scaling` targets carry no start URL and begin from arXiv listings/search), but `what` is mandatory.
- **`width`** — number of lanes to fan out. Default 50. Constraints come from the width ladder (LAWS, Law 7); lanes = targets 1:1, so `width` must equal `len(targets)` or the extra side is truncated to the other.

**On-disk mapping (observed this run).** Each target lands as `mickey17_v2/lanes/<id>.json`. A lane file is either a single object with a `rows` array or a bare JSON array of row objects (both shapes occur; the fold's counting script must accept both). One row is:

```json
{ "lane": "...", "source": "https://...", "claim": "...", "quote": "verbatim from source",
  "estate_status": "confirms-ours | owed | we-have-better | new", "steal": "concrete action + landing spot", "leverage": "high | medium | low" }
```

Lane-level note fields (`fetched`/`fetch_method`/`verified_via`, `caveats`, `rubric_gaps`, `negative_results`, `negative_result_check`, `unverified`, `premise_check`, `grep_evidence`/`estate_greps_run`) are where fetch provenance, rubric gaps, and failure modes live. A dead lane (source does not exist) is a valid lane file consisting of exactly one negative-result row.

## 3. PHASE MACHINE

Five phases, strictly ordered. Phases 1–2 fan out; phases 3–5 are single-seat.

1. **SWEEP.** Fan out `width` lanes, one subagent per target, each on the cheapest flash-tier model (COST DOCTRINE). The lane reads its primary sources and mines register rows. During the sweep a lane only reads the world and writes exactly one file — its own backup at `lanes/<id>.json`. No lane touches another lane's file or any shared state.
2. **PER-ROW CONFIRMATION.** Every row must survive: the quote byte-checked against the fetched source, the URL recorded and live, the estate grep run over at least two directories, and — for high-leverage rows that will carry the fold — an explicit verifier pass. Verifier verdicts are `verified` or `unconfirmed` with the reason; unconfirmed rows are itemized in the fold and used only as negative results (this run: 8 unconfirmed, fold §5, none used as support anywhere).
3. **FOLD.** One seat reads all lane JSONs with a counting script (never by eyeball), recounts the scoreboard, and writes the master fold: scoreboard by estate_status, top steals ranked by leverage, a DISPUTED tier of contradiction pairs each with a conditional ruling, negative results named plainly, and a go list of actions sized one-seat-one-sitting. Provenance check this run: an independent script recount returned 246 rows split 41/61/96/48, matching the fold exactly.
4. **SPEC.** One seat formalizes or updates this engine document from the run's own evidence — the dogfood step. Every run files its own spec; the engine is a product of every run, not a frozen preamble.
5. **FILE-INTO-ESTATE.** Fold and spec land in the estate through the three ports (Section 8): the reusable workflow, the task-wall chore family, and the corpus/steal entry. A run that does not file itself did not happen.

## 4. THE RUBRIC

Six checks every lane ran. A lane that cannot pass one records why in a note field instead of faking it — a recorded gap is rubric-compliant; a silent one is not. Verified this run across all 246 rows: quote, source, steal, and estate_status present and non-empty in every row.

1. **Primary source fetched.** The lane records how and when it fetched (`fetched`/`fetch_method`/`verified_via`). Summaries from fetch tools are cross-checked against raw bytes where possible (observed: `github-trending-agents` cross-checked a WebFetch summary against `curl -sL` raw HTML, 709,988 bytes, all 22 repos and star counts matched).
2. **Verbatim quote bound.** Every row's `quote` is copied byte-for-byte from the fetched source. A paraphrase is not a quote; a quote with silently dropped words is a failed row (both were caught this run — Section 7). If a claim cannot be bound to a verbatim quote, the row does not exist.
3. **URL recorded.** Every row carries its source URL in `source`, even when the source is an estate-internal file (then the absolute estate path is the URL).
4. **Estate grep ≥ 2 dirs.** The lane greps at least two of the estate's three steppable directories — `corpus/steal`, `memory/research_polished`, `watch/inbox` — and records the greps in `grep_evidence`/`estate_greps_run`. A zero-hit grep is a recorded finding (this run produced several), never a reason to skip the check.
5. **Concrete steal action.** Every row's `steal` names an action a single seat can take in one sitting and a landing spot — a file, ideally file:line. "Worth exploring" is not a steal.
6. **Negative results first-class.** Dead sources, walls, empty greps, premise drift, and verifier unconfirmations are filed as rows or note fields with their evidence trail. A lane whose source turns out not to exist files that non-existence as its row — this run's `skywork-guide` is exactly that: one row, the API's verbatim `{"code":100101,"message":"Data not exist",...}`, and the enumeration evidence.

## 5. LAWS

Seven laws. Each is checkable; a run that breaks one says so in its fold.

1. **CITATION-BINDING.** No quote, no row. A claim without a verbatim quote from a fetched primary source is not a register row, no matter how plausible. This is the engine's answer to the field's measured quote-fidelity failure — LLMs verbatim-quote correctly only ~47% of the time (BITF self-test, fold steal #3) — so the engine makes the quote the unit of storage and lets the check be mechanical.
2. **NEGATIVE-FIRST-CLASS.** A dead source is a result. Phantom citations, paywalls/SSO walls, unreachable hosts, empty greps, and unconfirmed claims are filed with evidence and survive into the fold's negative-results section. Nothing is silently dropped and nothing is substituted without being labeled as a substitute.
3. **CONTRADICTION-TIER.** Never average, rule with conditions. When two sources conflict, both go to the DISPUTED tier with a ruling that states the conditions under which each side holds — or names the claim that is actually false. This run folded six pairs this way (fold §4), e.g. Anthropic's 80% token-variance vs Brown's <10% multi-agent credit: both hold, they answer different questions (spend governs variance; base model governs the win). A merged "both are kind of right" sentence is a fold defect.
4. **ABSOLUTE-PATHS.** All prompts carry absolute paths. Every lane prompt, estate citation, and file reference is absolute (`C:/...` or full URL) and estate citations land as path:line so the next seat can click and check. Relative paths in prompts are how clones end up reading the wrong tree.
5. **FOLD-BY-SCRIPT.** Counts recounted from files, never from agent self-reports. The fold seat runs a counting script over the lane JSONs; a lane's own "I found N rows" is a claim to be checked, not a number to store. Both v1 ("Recounted by script from 72 register files") and v2 (this run's 246-row recount matching the fold) hold this line.
6. **WRITES-SERIAL.** Reads fan out, folds that write are single-seat. Sweep lanes read the web in parallel and each write exactly one file of their own. Any write to shared state — the master fold, this spec, estate files — happens in one seat, after all lanes have landed. This is the estate's own published law (arXiv 2603.05344v3: read-only tools parallel, write tools sequential; Cognition's independent reversal, fold steal #4) applied to the engine that stole it.
7. **WIDTH-LADDER.** 14 = day minimum, 50 = standard burn, night window = more. A day shift runs at least 14 lanes; the standard burn is 50; an unattended night window takes more. Width buys elapsed time, not per-lane quality — this run landed 50 lanes in ~65 minutes of wall clock (lane file mtimes 06:18–07:23) because lanes are independent; v1's 72 slices in refill batches are the same shape at different width.

## 6. COST DOCTRINE

Cheap flash lanes for lanes; verification spend only on high-leverage rows. Every sweep lane runs on the cheapest flash-tier model that can fetch and extract — v1 ran its fold driver on glm-4.7-flash, and the current fold re-ranks lanes toward deepseek-flash at $0.003/1M off-peak cache-hit (fold steal #13). Judgment at the row level is cheap because the rubric makes it mechanical. The expensive model appears only where a row's failure would contaminate the fold: byte-checking quotes for high-leverage rows, verifier passes on the rows that will become top steals, and the disputed-pair rulings. Medium/low rows ride on lane-internal checks and are marked as such. Big burns are scheduled off-peak (DeepSeek's windows: avoid 01:00–04:00 and 06:00–10:00 UTC Mon–Fri) — the night window of the width ladder is also the cheap window.

## 7. FAILURE MODES OBSERVED THIS RUN

Named from the lane note fields and fold §5, each with its instance. The engine's standing answer to every one of them is the same: the lane files the failure in a note field and substitutes nothing.

1. **Phantom sources.** `skywork-guide`: the cited guide does not exist — the site's own API returns `Data not exist`, and enumeration of 710 blog + 75 guide posts plus 3,000 Wayback URLs found no match. `nous-latest`: `psyche.nousresearch.com` ENOTFOUND, repo 404, zero homepage matches.
2. **Premise drift between ask and fetch.** `apex-agents`: the ask's premise (Fable 5.1 at 68.6% Pass@1, release-date leader) was true at release but the live board now ranks Opus 5.5 Max 73.5%; the 71.9% circulating in search snippets was a per-job score, not the headline. Numbers move while the burn runs.
3. **URL and owner rot.** `contradiction-synthesis`: `arxiv.org/html/2403.08319v3` 404'd (v1 fetched). `wide-deep-search-agents`: SearchOS was not at `github.com/antgroup/SearchOS` (404) — real owner `antins-labs`; `perplexityai/wandr`'s README clone URL still says `ppl-ai` after the org rename.
4. **Walled sources.** `nous-latest`: Vercel Security Checkpoint on Portal pricing after 2 attempts (webReader + curl with browser UA). `meta-fair-agents`: Meta Spark SSO-walled. `x-frontier-today`: X search 404/login. `orchestrator-war-stories`: Factory.ai unreachable after 5 attempts. `swarm-economics`: Arize/Artificial Analysis 403s + rate limits — those pages were explicitly NOT cited as verified rows.
5. **Barren start URLs.** `contradiction-synthesis`: the start URL fetched fine but carried no on-topic papers (titles only, no abstracts); rows came from search-located primaries instead. `hn-agents-month`: the agent-evals threads this month had 0 or <10 comments — nothing to mine, recorded in `rubric_gaps`.
6. **Fabricated names and rumors.** `contradiction-synthesis`: "ContraGen" has 0 occurrences in its cited source — the real paper is LegalWiz — and the alleged quote silently dropped "and potentially risky". `state-artifact-formats`: "The Crovia Seal" IETF draft verified nonexistent. `openai-agents-latest`: "OpenAI shutting down Agent Builder/Evals Nov 30" traced to a 2022-template content-farm site with no such article.
7. **Quote drift.** `citation-binding-tools`: BITF's self-test on its own README produced 47% verbatim verification — paraphrase passing as quote is the field's default state, which is why Law 1 exists. `langgraph-patterns`: the row said writes are cleared "on retry exhaustion"; the source clears them before the retry decision.
8. **Unit errors in sources.** `perplexity-lab`: fast-preset $6.209 vs $611.00 is a 1000x renderer error in the source (real: $0.006209 vs $0.6110 per request); the ~98.98% ratio survives, the dollar figures do not.
9. **Verifier unconfirmations on high rows.** 8 itemized in fold §5 — e.g. `apex-agents` Pass@4/Pass^4 have 0 occurrences on the leaderboard page; `persistent-coding-agents`' "in five months" and "Search Infrastructure team" appear nowhere in the Photon post; `openai-agents-latest`' claimed publish date is contradicted by Wayback; `supersonic-x`'s "Jev does not resolve" is simply false.
10. **Empty estate greps.** `agentic-researcher`: the estate doctrine "laws-as-ribs / structural tool grant" named in context returns 0 textual hits in the three greppable dirs. `verifier-scaling` files an explicit NEGATIVE/empty row. A 0-hit grep narrows the map; it is a finding, not a gap in the lane.

## 8. PORTS

How a run's output becomes standing estate infrastructure — three ports, all exercised by this formalization.

1. **Reusable workflow.** The engine saves as one workflow definition taking `{topic, targets, width}`. The script: phase 1 spawns `width` subagents (flash-tier model) each writing `lanes/<id>.json`; phase 2 a verifier pass over high-leverage rows; phase 3 one fold subagent whose first act is the counting script over all lane files; phase 4 this spec-writer; phase 5 the file-in step. Re-firing is passing a new `topic` and target list — nothing inside the engine is topic-specific, and the lane-backup schema (Section 2) is the stable contract between runs.
2. **Task-wall chore family.** The recurring wall rows the engine generates: a daily 14-wide burn at the day minimum; the standard 50-wide weekly burn, scheduled off-peak into the night window; and, after every fold, its go list converted one-to-one into wall chores sized one seat, one sitting (this fold's: migrate Sonar-wired lanes before the 2026-09-27 sunset; file the W4 FAILED verdict; run the 47%-style verbatim audit; strip write tools at fan-out; schedule DeepSeek burns off-peak). The chore row format is `burn(<topic>, width=N) -> fold -> chores[]`.
3. **Corpus/steal entry.** The engine registers itself in `corpus/steal` beside the existing steal map (`ZCODE_REPO_STEAL_MAP_20260924.md`): one entry naming `MICKEY17_V2_ENGINE_SPEC.md` as the standing frontier-burn organ, with the interface, the lane-backup row schema, the seven laws, and the width ladder — so any future seat can fire a burn without re-deriving any of it. The entry points at the current fold (`MASTER_MICKEY17_V2_20260924.md`) as the newest instance and at v1 (`memory/runs/mickey17/`) as the inward-facing ancestor.

---

*Provenance: this spec was written from the 50 lane JSONs (read plus a scripted recount of 246 rows and their field coverage), the master fold, and the v1 receipts (MASTER_INDEX_20260920.md header and register, digest files). All failure-mode instances cite their lane or fold section. Nothing in Section 7 is invented; each item was read in a lane note field or fold §5 this session.*
