# TOPIC INDEX BUILD — the unlock, delivered (2026-09-06)

**Card:** G5-1 from `watch/RESEARCH_ARCHAEOLOGY_20260905.md` — the corpus is
organized by TIME+SEAT, never TOPIC. This organ is the fix: `what do we know
about X` is now one grep / one section read.

## What was built
- `mag/topic_index.py` (v4) — CLI: `python -m mag.topic_index build [--dir watch]`
  (also `query <term>`). Streams every `*.md` under watch/ **recursively**
  (top level + inbox/ + scout/ + hermes_wings/ + all), skips files >2MB and
  hidden dirs, excludes its own two outputs so rebuilds stay deterministic.
  Extracts per card: title (first heading), rubric score (max of all
  `\d{1,2}/25` hits), date (first `20YYMMDD` in filename), tri-state/disposition
  flags (DISPUTED/UNPROVEN/WINDOWED/BUILD NOW/OWED/FOLDED), topic tags.
- `watch/topic_index.json` — machine mirror (per-card path/title/date/score/
  states/topics, `generated_at`).
- `watch/TOPIC_INDEX_20260905.md` — human mirror: summary table, then one
  section per topic (newest first, count + median score), plus a **no-topic**
  bucket so nothing vanishes.

## Counts (build 2026-09-06T02:04Z)
**1040 cards indexed** (skipped >2MB: 0) · 23 topics · **166 no-topic**.

| topic | cards | median |
|---|---|---|
| corpus-canon | 380 | 16 |
| auth-lite | 336 | 17 |
| dnd-game | 307 | 19 |
| salon | 301 | 19 |
| economics | 283 | 19 |
| intake | 276 | 17 |
| docker-fleet | 230 | 21 |
| verkle-chain | 184 | 19 |
| self-steal | 165 | 22 |
| x-harvest | 152 | 21 |
| refguard-refeed | 124 | 19 |
| vision | 116 | 18.5 |
| mcp | 94 | 16 |
| trajectory | 93 | 20 |
| concurrency | 73 | 21 |
| shadow-fields | 60 | 15.5 |
| android | 42 | 22 |
| max-distill | 33 | 19 |
| astra | 26 | 21 |
| grounding | 26 | 22 |
| beacon | 20 | 22 |
| overseer | 14 | 21.5 |
| gstd | 7 | 18.5 |
| (no topic) | 166 | - |

Multi-label: cards can sit in several topics, so topic mass > card count.
**Biggest topic: corpus-canon (380)** — also the lowest-median big bucket (16),
which matches the archaeology's "ghost era is unexcavated" read.

## Determinism
Proven: two consecutive builds over a stable corpus produce **identical json
except `generated_at`** (verified by programmatic diff — zero changed/extra
cards). During the 8-wide probe window the corpus is live: consecutive runs
may pick up newly-landed cards (observed 1036 -> 1040 while sibling workers
wrote), which is corpus drift, not indexer nondeterminism.

## How to rerun
```
cd ROOT
python -m mag.topic_index build            # rebuild json + md
python -m mag.topic_index query autoglm    # ask "what do we know about X"
```
Read-only on cards; outputs are the only files written. To widen buckets, edit
`TOPIC_BUCKETS` in `mag/topic_index.py` (name + keyword list, word-boundary
matched on path+title+first 6KB) and rebuild.

## Provenance
Supersedes the v3 TF-IDF draft (kept intact at `mag/topic_index_v3_tf_draft.py`;
its mirrors `watch/TOPIC_INDEX.md` + `dashboard/static/topic_index.json` left
in place untouched). Bones stolen, reinterpretation named: named keyword
buckets instead of free-form TF terms; recursive stream instead of top-level
glob; deterministic output.
