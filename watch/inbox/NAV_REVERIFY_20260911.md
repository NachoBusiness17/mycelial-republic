# NAV RE-VERIFY — 2026-09-11 — wave worker slot 9, cycle 2 (verify-only lane)

- watch/NIGHT_FOLD_20260911.md — binds this slot: rotation at bounded width, no silent pass, name your dating method.
- watch/inbox/NAV_WIRING_20260906.md — nav.js LINKS = 63 entries at 09-06, additive-only law, rollback pattern; 91→93 growth since is measured below.
- watch/inbox/THEME_LEXICON_FOLDED_20260911.md — the birth-json fold; its "After 25,760" size and its "63-value" headline are both re-measured below and one of them moves.

## DATING METHOD (law 3 — stated up front, every count below uses it)

- Dating = box mtimes, local -0400, read via `stat` (box says Sep-09; operator says Sep-11; skew is real and written down in the night fold).
- Count definition = rows matching `["target","label",...]` in the named array, extracted by grep, not eyeballed.
- The lane name's "66/66" is DISPUTED (see §4): no file state on disk has 66 entries.

## 1. INDEX.HTML LINK TABLE (mtime 09-09 11:45 — the birth-canvas-edit-era file the lane named)

The only static link table in index.html is `VISUALS` (lines 168-206). The SURFACES/ORGANS/
CARDS/CODE+DATA sections are runtime-populated from `/api/workspace/tree`, not a static table —
named, not swallowed: they have no on-disk link targets to check.

- **37 entries checked, 37 OK, 0 broken.** Every target exists under dashboard/static/.
- 0 duplicate targets in the table.
- salon_lightmap.html — the 09-06 card's ABSENT pending surface — now EXISTS and is wired in both tables. Debt from NAV_WIRING cleared.

## 2. NAV.JS LINKS (mtime 09-07 20:11 — unchanged since before the birth-canvas edit)

- **93 entries checked: 91 file targets — 91 OK, 0 broken; 2 routes — both PROVEN, 0 UNPROVEN.**
- Route judgment: `/` → dashboard/server.py:556 `path in ("/", "/index.html")` serves STATIC/index.html, which exists (13,096 B). `/chan` → server.py:544 `path in ("/chan", ...)` serves STATIC/chan.html, which exists (12,719 B). Both handlers read on disk this run; nothing guessed.
- `node --check nav.js` → SYNTAX_OK.
- NAMED, NOT SWALLOWED — 10 duplicated targets render twice in the bar (tavern_brawl, spectral_maze, shadow_walk, phase_particles, maze_arena, light_maze, hardware_primer, arrakis, airflow_home, arena_operator_field). Harmless visually, but the array has grown 63→93 in two days by tail-append and the dupes are append-debt. Follow-up lane input, not fixed here.
- Also named: verkle_construction.html ("The Birth Canvas" tile) does NOT include nav.js (0 matches) — the tile works via index.html peek iframe, but the page opened directly has no nav bar. Observation, not a break.

## 3. THE "66" IS DISPUTED

Backup lineage of nav.js LINKS row-counts, counted with the same grep: 59 (bak-nav-20260906-wiring,
09-05 21:55) → 63 (the 09-06 wiring card's "current") → 80 (bak-fixall-20260907, 09-07 01:45)
→ 82 (bak-rehome-20260907, 09-07 02:40) → **93 (current)**. 66 appears in no preserved state —
at best it was a mid-append state on 09-06/07 that no backup caught, at worst a miscount that
became a lane name. The honest current numbers are **37/37 (index.html) and 93/93 (nav.js)**.

## 4. BIRTH CANVAS CHAIN

- `verkle_construction.html:265` fetches `./index_data/verkle_birth.json` with `cache:"no-store"` — CONFIRMED, path unchanged, target exists relative to the page.
- JSON parses (`json.load` PASS); 14 top-level keys, matching the fold receipt's reload round-trip.
- `theme_lexicon` PRESENT, subkeys: generated, source, denominator_note, population, vocabulary, delta, silence_only, vector_lengths.
- Pre-fold backup EXISTS: `index_data/verkle_birth.json.pre_theme_lexicon.bak`, 14,475 B — exactly the receipt's "Before".
- **Sizes (bytes): current 26,120 · pre_theme_lexicon.bak 14,475 · pre_dedupe.bak 25,760.**
- NAMED, NOT SWALLOWED — the receipt's "After 25,760" is now the pre_dedupe.bak: a later dedupe pass (mtime 09-09 15:34/15:35 box-time) edited the file again (+360 B) and no receipt in my inputs covers it. Data intact (parses, sum-guard holds), but the pass is unreceipted.
- NAMED, NOT SWALLOWED — count dispute: the receipt headlines a "63-value vocabulary (62 non-null + NULL)"; the folded data self-reports `values_total: 62, non_null_values: 61`, with NULL riding inside the 62-entry `vocabulary` list. The card's label is off by one on the non-null side; the data is internally consistent — the receipt's own sum-guard holds: 8,905 named + 12,147 NULL = 21,052 leaves, 0 parse failures (recomputed from the file this run).

## 5. CHECK COMMANDS (measure, don't assume — run from dashboard/static/)

```bash
grep -oE '^\s*\["[^"]+","[^"]*"' index.html | wc -l            # 37
grep -oE '^\s*\["[^"]+", ?"[^"]*"' nav.js | wc -l              # 93
while IFS=$'\t' read -r f l; do [ -f "$f" ] || echo "BROKEN $l $f"; done \
  < <(grep -oE '^\s*\["[^"]+","[^"]*"' index.html | sed -E 's/^\s*\["([^"]+)","[^"]*".*/\1\t\2/')
# same loop over nav.js rows with /static/ prefix stripped; routes ("/", "/chan") judged
# against dashboard/server.py:556 and :544 with target files stat'ed on disk
python -c "import json;d=json.load(open('index_data/verkle_birth.json',encoding='utf-8'));print('theme_lexicon' in d)"
```

## VERDICT

**YES — console nav healthy post-edit: 130/130 targets OK (index.html 37/37, nav.js 93/93 with both routes server-proven), 0 broken, birth-canvas chain intact.**

CYCLE GENETICS: scripting the count instead of trusting the lane name caught the real finding this slot — "66/66" was a stale mid-append number and the true state is 37 + 93 = 130 targets, all green, so the lane's premise (a possible break from the birth-canvas edit) dissolved on contact with measurement; the fold receipt's two headline numbers (63 values, 25,760 B) had also drifted from the file they describe. What worked: one grep extraction feeding both the index and nav loops made the two tables comparable, and judging routes by reading the two dispatch lines plus stat'ing their targets turned the only UNPROVEN risk into PROVEN in under a minute. What to change: lane names should carry the array they count and a commit/mtime anchor ("nav.js@93, mtime 09-07"), never a bare total — a count without its dating method is inherited as gospel and costs a whole slot to re-derive; and every post-fold edit to a receipted estate file should append one line to the receipt it amends, or the next verifier re-litigates the delta.
