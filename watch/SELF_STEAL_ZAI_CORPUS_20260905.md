# SELF-STEAL: THE Z.AI CORPUS — 2026-09-05 (worker: corpus, $0, local-only)

Task: inventory everything BANKED from z.ai rides so future burns can't corrupt or
duplicate it — and answer whether we hold Ponytail's canon. All counts measured by
direct parse, not memory.

## 1. Inventory table (measured 2026-09-05 ~21:20 local)

| Corpus | Path | Parts/rows | Parseable | Size | Time strata | Verdict |
|---|---|---|---|---|---|---|
| Thought bank (main) | `memory/thinking/app_reasoning.jsonl` | 9,305 parts | 9,305/9,305 = **100%** | 22.2MB file; reasoning `chars` sum = **17,300,511** (17.3M — matches memory) | 2026-08-25T12:38Z → 2026-09-05T03:37Z | SUPPORTED, matches the 9,305 / 17.3M claim exactly |
| Thought bank (new lane) | `memory/thinking/glm-5.3-flash.jsonl` | 5 rows | 5/5 = **100%** | 9.4KB | 2026-09-05T02:05Z → 2026-09-05T23:01Z | SUPPORTED (new, live) |
| ASTRA corpus | `memory/runs/astra_world/ASTRA_CORPUS_20260905.md` (+dispatch_001.log 227KB, goals_mined.json, 2 prompts, seat_exec_01.log) | 1 main doc (198,730 B) | markdown (not row-parseable; n/a) | ~450KB total | 2026-09-05 (dated) | SUPPORTED |
| X canon (grok harvest, roots) | `corpus/canon/x_canon_2026_fx/` — 130 `fx_*.json` + 1 stray at `corpus/canon/` top level = **131 files** | 131 tweets, ALL author `NachoQuixotic` | 130/130 folder = **100%** | 0.54MB | 2026-08-14 → 2026-09-02 (+1 stray 09-05) | SUPPORTED |
| X canon — reply layer | same folder: `replying_to` non-null = **17 rows**; roots (null) = 113 (+1 stray self-reply) | — | — | — | — | **UNPROVEN** for the "215 reply bodies" claim (below) |
| Founding curriculum | `corpus/canon/founding_curriculum/` — 12 `curriculum_*.json` + `MANIFEST.json` (per-file sha256, source: api.fxtwitter.com door #1) | 12 posts | 12/12 = **100%** | small | 2023-11-23 → 2025-08-07 | SUPPORTED |
| Session digest | `watch/session_digest.jsonl` | 15,365 rows | 15,365/15,365 = **100%** | 5.0MB | 2026-07-20T11:59Z → 2026-09-05T22:51Z | SUPPORTED |
| Summarized sessions | `watch/summarized_sessions.json` | 3 top-level entries | valid JSON | 0.05MB | — | SUPPORTED (thin) |

Memory cross-check: "9,305 parts / 17.3M chars" — **exact match** (17,300,511).
"6/6 roots complete" — the canon analysis card (`watch/CANON_SELF_STEAL_20260904.md`)
walks 6 numbered posts (its tables number 1–6); roots are present. "215 reply bodies" —
claimed only at `watch/X_HARVEST_DOCTRINE_20260905.md:54` ("Canon folder pass 2 (215
replies via grok multi-door, all trees complete)"); the folder holds **17** reply rows
and no other reply-body store was found under corpus/. **Verdict: UNPROVEN — either the
pass-2 output was never landed in the repo, or it landed somewhere not named.**

## 2. PONYTAIL

**Verdict: SUPPORTED — we hold Ponytail's canon.** 2,369 hits across 340 files
(watch/, state/, memory/, research/). Ponytail is not an X personality — **zero**
mentions in the X canon tweets. It is the GitHub methodology repo
`DietrichGebert/ponytail` (npm `@dietrichgebert/ponytail`), "the lazy senior dev."

Held:
- **Full source tree**: `memory/improve/sources/ponytail-2026-08-03/` — README (+es/ko),
  benchmarks + dated results (2026-06-12 → 06-22), skills (ponytail/gain/debt/audit/
  review/help), hooks, ponytail-mcp server, tests, examples, 20-agent platform configs.
- **Fleet adaptation receipts**: `watch/PONYTAIL_LADDER_STATS_20260901.md` (ponytail.mjs
  ladder: 5 fires / 0 misses, promotion gate measured), `watch/sea/board_receipts/
  19_ERA3_PONTAIL_BASE.md`, `memory/improve/evals/ponytail-audit-self-2026-08-03.md`.

Two identifying lines (per protocol, max 2):
- `memory/improve/sources/ponytail-2026-08-03/README.md` — "He says nothing. He writes
  one line. It works."
- `watch/PONYTAIL_LADDER_STATS_20260901.md` — "Ladder promotion gate (per ponytail.mjs):
  R1 hit-rate >= 3 fires/24h twice running, and a rule hitting 0 fires in 72h gets a
  prune note. **NOT YET REACHED**"

## 3. So we don't fuck shit up — the 3 corruption/duplication vectors

| # | Risk | Structural prevention in place | Missing |
|---|---|---|---|
| R1 | **Schema drift inside one bank dir.** `app_reasoning.jsonl` (thought_bank_app: part_id/text/chars/sha16) and `glm-5.3-flash.jsonl` (thought_bank.py: model/lane/reasoning/answer) are TWO schemas in ONE directory; both writers are append-only and silent-fail by design. A future caller re-banking with the wrong helper mixes schemas or double-banks the same turn — nothing rejects it. | The choke-point doctrine is written into the code head ("THE single choke point", one-line `bank_response` for any caller) + the prose census flags unbanked callers; dedup keys exist (`sha16`, `prompt_sha16`). | Keys are stored but **not enforced unique**; no schema-version field; no row-count/size sentinel file to detect a burn that rewrote or re-appended history. |
| R2 | **Misfiled writes outside the canon folder.** Live proof found this pass: `corpus/canon/fx_2096341325960417585.json` (Sep 5 self-reply) sits at `corpus/canon/` top level, NOT inside `x_canon_2026_fx/`. Any future glob-based consumer of "the canon folder" misses it; any re-harvest re-fetches it → duplicate. | `founding_curriculum/` has a `MANIFEST.json` with per-file sha256 + source door recorded — the model pattern exists. | **No MANIFEST for `x_canon_2026_fx/`**; the 215-reply pass-2 output is claimed in `watch/X_HARVEST_DOCTRINE_20260905.md:54` but not locatable under corpus/ — unlocated pass-2 output is the same trap one level up. |
| R3 | **Re-harvest overwrite via a time-decaying source.** The fx door returns LIVE engagement counts (likes/views drift hourly); filenames are bare tweet ids, so a re-run silently OVERWRITES files with different numbers, and engagement-at-read time (used as evidence in CANON_SELF_STEAL) is destroyed. | Id-in-filename makes same-id writes collide (accidental idempotence) and the doctrine card already treats the canon as cite-verified pass-1 record. | No per-file sha256 + no harvest lock/"already banked" gate on the fx folder; no snapshot of engagement-at-harvest timestamp inside each record's provenance. |

**One-line law for the next burn:** nothing touches `memory/thinking/` or `corpus/canon/`
except through the existing choke points, and no harvest runs without first writing its
MANIFEST (sha256 per file) — the curriculum folder already shows the pattern; the fx
folder is the one missing it.

*Worker corpus, 2026-09-05. All numbers direct-parsed; tri-state per row. $0, local files only.*
