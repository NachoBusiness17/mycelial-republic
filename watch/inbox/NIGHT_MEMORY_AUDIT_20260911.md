# NIGHT MEMORY AUDIT — 2026-09-11

Lane: MEMORY-INDEX HEALTH AUDIT (night run, 8-wide). Read-only except this card.
Index audited: `C:\Users\foste\.zcode\cli\memories\projects\projects-0fb5e3041b59db21\memory\MEMORY.md`

## Health stats

- Index entries: **39 at audit start, 41 by audit end** — two entries landed mid-audit
  from concurrent lanes (`user-night-run-trust-test-20260911`, `project-wave-bruteforce-ledger-20260911`).
  The index is a live surface; counts below are a snapshot.
- Referenced files: **41/41 exist**. Zero missing files. The index never points at a void.
- Wiki-links in the newest 16 entries: 47 unique targets checked — **42 OK, 5 DEAD** (list below).
  (Audit-method note: first two link checks false-alarmed 100% DEAD — a `\r` in grep output and a
  glob-strip bug. Verified clean before believing anything.)
- Coverage: the memory dir holds **673 .md files; the index carries 41 (~6%)**. The index reads as
  a hot-set (09-08 → 09-11). The other 632 files (09-01..09-08 era: feedback laws, early projects)
  are invisible to index readers. Biggest structural question of this audit: hot-set by design, or
  632 memories the seat forgot it has?

## Spot-check (15 random entries: file exists + hook matches content)

15/15 files exist. 10/15 hooks match. 5 mismatches, two serious:

| Entry | Verdict |
|---|---|
| x-fresh-start-driver | match (1 dead link, see below) |
| steering-mesh | match-light — hook "firing gated"; file's 09-11 update adds hub-relay + tavern PROVEN, only direct-steer still gated |
| ractor-organs | match |
| astra-ask-cockpit | lag-light — hook "v3 amendments staged", file already "v3 PRE-REGISTERED" |
| night-run-trust-test | match (new entry, well-formed) |
| birth-canvas-verkle | match; AWAITING GO items consistent with the 09-11 lost-record card |
| fireball-era | match |
| same-animal-law | match |
| canary-ladder | match |
| mem1-anatomy | match |
| **open-rib-spine** | **INVERTED ROT** — hook (09-09→11: v5 fixed-mouths LIVE, 1,258,549-file estate pass, delta cron live) is AHEAD of the file body, which still says 09-09 "awaiting ONE promotion". The newest state lives ONLY in the index line; rebuild the index from files and that state is lost. |
| **astra-campaign** | **STALE** — hook ends "desk review = gate to HOLD 1", but the 09-11 `astra-hold0-desk-review` card records desk review DONE and HOLD 1 PASSED. Campaign hook lags its own successor card. |
| wave-five-parable-fold | match |
| pratchett-primer-seed | match |
| **pyramid-vision** | **HOOK STALE** — hook says "him at top, seats as windows"; the file records the same-day amendment ("by me i mean we" — apex is PLURAL, fractal pyramids). Index still teaches the pre-amendment vision. |

Full reads (3): `project-pyramid-vision-20260911` (well-formed, amendment intact, all 5 links OK),
`feedback-moon-speak-law-20260911` (exemplary — plain-English law, all links OK),
`project-x-fresh-start-driver-20260909` (well-formed, laws held, 1 dead link).

## Dead links (5) and their carriers

All five are namespace/date typos — the target files exist under a slightly different name:

1. `[[project-coldest-vertex-build-freeze-20260909]]` → actual: `feedback-coldest-vertex-build-freeze-20260909.md` — carrier: project-astra-hold0-desk-review-20260911
2. `[[project-consent-archetype-layer]]` (missing date) → actual: `project-consent-archetype-layer-20260909.md` — carriers: project-filter-1301-shadow-20260910, project-wrongthink-invariant-map-20260910
3. `[[project-mark-untried-known-20260908]]` (wrong namespace) → actual: `user-mark-untried-known-20260908.md` — carrier: project-x-fresh-start-driver-20260909
4. `[[project-pratchett-primer-seed]]` (missing date) → actual: `project-pratchett-primer-seed-20260909.md` — carrier: project-wrongthink-invariant-map-20260910
5. `[[project-wave-six-fold]]` (missing date) → actual: `project-wave-six-fold-20260909.md` — carrier: project-filter-1301-shadow-20260910

## Duplicates / near-duplicates

- **STRONG PAIR:** `project-water-arena-20260909` and `project-water-arena-and-new-instruments-20260909`.
  Both index lines cover the Water Arena ladder AND the Coastline Index. Merge shape: water half into
  `water-arena`; the X ToS half of "new-instruments" already duplicates `project-public-deployment-layer` —
  fold it there. One card per animal.
- **MODERATE CLUSTER (keep, fix the pointer):** the Astra family is 5 entries (ask-sovereign-cockpit,
  campaign, fold, hold0-desk-review, ractor-organs). Phase-distinct, legitimate — but campaign's hook
  duplicates hold0 state and is now wrong about it. Rule: campaign hook should point at the hold0 card
  as single source of truth for HOLD status.
- **SOFT (no action):** doctrine echoes across mountain-roads / same-animal / fireball-era and the wave
  family (four/five/six/cadence) overlap by design — duplication is emphasis, and each records a
  distinct event.
- Cosmetic: `project-shitpost-desk-20260908` hook is dated 09-09 (filename/hook date mismatch).

## Stale / superseded

- openclaw gate: **NO index rot.** `project-openclaw-consent-gate-20260909` is correctly marked
  ⚰️ RETIRED on operator GO; no indexed hook claims the gate live; same-animal-law references it only
  as ancestor. Clean. (Minor: the card body keeps a historical "AWAITING OPERATOR GO" security-grant
  line that a skim could misread as open — the description line disambiguates.)
- Superseded/stale hooks: astra-campaign (HOLD gate passed), pyramid-vision (pre-amendment apex),
  open-rib-spine (state ahead of file).
- Open gates, verified still-open in their files (NOT rot — morning watchlist):
  birth-canvas recovery offer + retro-knotter (GO-gated behind truth-gate fix, consistent across two
  cards), public-deployment-layer attribution ruling ("Bernays kills it" contradiction still awaiting
  operator), steering-mesh direct peer-steer (awaiting GO), x-fresh-start sweep execution (hook says
  APPROVED; file only knots START-OVER when operator confirms done — same-animal card hints the
  zero-sweep day happened; confirm and close the loop).

## Recommended fixes (not applied — read-only lane)

1. Rewrite 3 index hooks: pyramid-vision (plural apex), astra-campaign (point at hold0-desk-review),
   open-rib-spine (fold the 09-11 v5/estate-pass state INTO the file body so the hook isn't the only
   carrier).
2. Repair 5 dead links per the table above (4 files touched, or normalize: always link full filename).
3. Merge the water-arena pair into one entry.
4. Operator/lane decision: index policy — hot-set only, or full-catalog index of all 673 files.
5. Standing suggestion: a 20-line link-lint (grep `\[\[.*\]\]`, test `<target>.md` exists) run
   before each index write — tonight's 5 dead links are all mechanical typos a linter catches free.

— night audit lane, 09-11, $0, read-only except this card.
