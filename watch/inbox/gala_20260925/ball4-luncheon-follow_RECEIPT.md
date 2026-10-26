# GALA RUN RECEIPT: ball4-luncheon-follow

- Date: 2026-09-29
- Receipt: `watch/inbox/gala_20260925/ball4-luncheon-follow_RECEIPT.md`
- Ball root: `watch/inbox/gala_20260925/ball4-luncheon-follow/` (lanes verified on disk this session: all four lane JSONs plus their `.check.txt` receipts present in `lanes/`)
- Source of record: script-written sections (authoritative) + script metadata (danced array, fold, review, filing). No number below was invented; every number is copied from those sections or that metadata.
- **GATE PASS**

## Header

- Slug: `ball4-luncheon-follow`
- lanes_json_count: **4** (expected 4)
- by_division: `{"B": 4}`

## Scoreboard

| Instrument | Value |
|---|---|
| lanes_parsed_ok | **2/4** |
| byte_checks_cited | **5** |
| mined_rows | **3** |
| decisions_changed | **4** |
| ballroom (danced/refired/buried) | **3/0/1** |
| by_division | `{"B": 4}` |
| gate | **PASS** |

Ballroom notes (script sections):

- **stuck:** `follow-capital-policy.json` (no ok, rows=0, checks=0 - the empty-on-refire buried shape)
- **banked:** `follow-compute.json` (ok absent/false, evidence-banked: 3 checks, 0 rows)

Danced list (script metadata, 4 entries, all `ok:true`):

| Lane | Division | ok | rows |
|---|---|---|---|
| follow-defense-enterprise | B | true | 3 |
| follow-models | B | true | 0 |
| follow-capital-policy | B | true | 0 |
| follow-compute | B | true | 1 |

Shape note (fold scoreboard, script): the ballroom counter reads JSON shape fields (ok/rows/checks arrays); capital-policy and compute carry status strings and rows outside those fields, so their on-disk receipts are the tiebreaker and both receipts PASS. lanes_parsed_ok 2/4 = the two lanes carrying `ok:true` (defense-enterprise.json:4, models.json:4); the other two carry status instead (capital-policy.json:3 done, compute.json:3 complete). This is why the counter reads 3 danced while the danced metadata array names 4 lanes.

## Decision ledger

**PARADE: false** (fold verdict: `parade=false`). Not a parade: 4 decisions changed, every one listed.

1. `follow-capital-policy.json`: **Closes: which policy channel binds the sovereignty program.** Answer: NOT domestic regulation (deregulated by design this window: Sacks no-restrictions, Johnson voluntary guardrails, Wiles/Bessent slimmed-down EO, Ferguson anti-pacing-cartel, Kratsios anti-global-governance); the bound is the Commerce/BIS export-control licensing channel, on three named receipts (the 2026-06-12 Is-Informed Letter precedent making model access licensable and open-weight release an export under that theory, the 2026-09-21 AI Exports Program deadline that passed silently in-window, the standing Cairncross pre-release 30-day review machinery); swing variable the AI-czar appointment (Bessent vs Kupor float). Receipt: `watch/inbox/ball4/capital-policy.md`; check receipt PASS/EXIT 0 (`follow-capital-policy.check.txt`).
2. `follow-compute.json`: **hardware buy-window changed:** the attic HARDWARE_RADAR_20260901 used-24GB price quotes (~$1,100-1,300 RTX 3090) are now stale inputs under the memory supercycle (Micron HBM4 sold out CY2026, Rubin HBM4e / MI455X HBM4 demand) - any VRAM-ladder purchase must re-quote street prices first; model-pinning refresh loops need shortening (Grok 4.7 mid-cycle). Banked as decision inputs in `watch/inbox/ball4/compute.md`; no decision executed by this lane.
3. `follow-defense-enterprise.json`: **luncheon watchlist register decisions changed in place:** lunch-sean-cairncross org corrected from the WRONG "WH Deputy Chief of Staff" guess to White House National Cyber Director (ONCD); lunch-richard-walters resolved from "unverified org"/search to White House Deputy Chief of Staff for Legislative, Political and Public Affairs/gov; lunch-bill-mcdermott handle graded search to confirmed on live fxtwitter match; signals baseline created with explicit in-window vs out-of-window honesty flags.
4. `follow-models.json`: **no decision executed by this read-only lane; it arms one:** run the next distill/quantize cycle against the current frontier (Sonnet 5.5 / GPT-5.6-class) BEFORE Gemini 4 lands, while the parity window OpenAI's training pause opened is still open.

Top laws carried out of the fold (script fold metadata, sources as cited there):

- **deployment-in-the-loop beats model-sale (Palantir pattern)** - Palantir's defense-AI wins (Maven into Japan MoD, Ukraine defense stack) come from sitting inside the customer's workflow, not from selling models; the estate's own receipts-not-labels law confirmed at nation scale, with a named falsifier (dies if September coverage proves roadmap-driven with no Maven-in-Japan or Ukraine stack). Source: follow-defense-enterprise.json:7-15.
- **provenance-graphing is a warfare-domain frame (Exiger pattern)** - Exiger's CEO publicly framed supply-chain risk AI as a warfare domain (WashingtonExec interview 2026-09-22), the estate's corpus registry discipline (hashes, bounded pointers, receipts) read at nation scale; an external corroborator the next corpus-provenance law write-up can cite directly. Source: follow-defense-enterprise.json:16-24.
- **orbital compute is the compute-sovereignty endgame (NASA/Isaacman pattern)** - the NASA administrator publicly backs Earth-orbit AI data centers (Isaacman note 2026-09-20, The Hill 2026-08-26), a state nod that moves off-planet compute onto the compute-watch surface alongside the VRAM-ladder and memory-supercycle decisions. Source: follow-defense-enterprise.json:25-33.

## Refired

- **0** (none). Metadata `refired` array is empty.

## Buried

- **1**: `follow-capital-policy.json` - stuck (no ok, rows=0, checks=0 - the empty-on-refire buried shape).
- Fold keeps the work: its own lane JSON says status done with 14/14 targets covered and its check receipt is PASS/EXIT 0 on disk; the gate still counts its changed decision in decisions_changed:4, so the ledger keeps it (fold scoreboard, script).

## Review verdict

**REVISE** (review instrument, this run). Findings as returned by the reviewer:

- **Quotes byte-match (3/3):** the three follow-defense-enterprise.json row quotes are exact substrings of their cited sources (the estate_angle fields of the lunch-alex-karp, lunch-brandon-rahbar-daniels and lunch-jared-isaacman rows in `watch/inbox/luncheon_watchlist_20260929_signals.jsonl`; Python substring check, all True, run in the review session). The models lane's "Wikipedia byte-verified" claim is byte-backed in `lanes/fetch_wiki_claude.html` (Claude Opus 5.5 -> 2026|09|22, Claude Sonnet 5.5 -> 2026|09|28). Capital-policy's Mayer Brown/Lawfare quotes have no on-disk source artifact to check against (no fetch saved; the reviewer did not fetch), so those were not spot-checkable.
- **Check backing exists but one does not reproduce:** all four claimed checks have `.check.txt` files on disk. The reviewer reran all four instruments: capital-policy exit 0 (OVERALL: PASS), follow_compute_check.py exit 0, finish_check.py (models) exit 0 - but check_finish.py (defense-enterprise) now exits 1 with 3 FAILs because it hardcodes "signals has 8 rows" against the now-36-line shared register. Its `.check.txt` was a true snapshot of its own run moment (shows "signals rows: 8"), but the lane JSON's exit-0 claim does not hold on final disk state.
- **Decision ledgers are honest (no strikes):** capital-policy's decision_ledger needles (Is-Informed, 2026-06-12, 2026-09-21, open-weight, export-control, AI-czar) all verified by the reviewer's rerun of its check script; defense-enterprise's register edits (Cairncross org -> ONCD, Walters resolved, McDermott @BillRMcDermott confirmed) still PASS on rerun; compute.md on disk carries the banked HARDWARE_RADAR re-quote/model-pinning inputs; models and compute both explicitly say "no decision executed" - honest negatives, nothing names a phantom.
- **B-division finish lines: met per-lane but broken at register level.** Per-writer counts are exact (capital-policy 14, models 9, defense-enterprise 8, compute 5) and all four receipts exist (capital-policy.md 11,203B, compute.md 7,647B, models.md 5,670B, defense-enterprise.md 5,857B). But the shared register has 36 rows for 35 unique targets: lunch-sean-cairncross appears twice (line 8 by gala-ball4-follow-defense-enterprise, line 31 by gala-ball4-follow-capital-policy, both org=National Cyber Director), unflagged in any lane JSON or receipt - and this duplicate is exactly what trips the defense lane's own "one row per target, no dupes" FAIL on rerun. Fix before banking: dedupe or annotate the second Cairncross row and re-scope (writer-filter) the defense instrument so its exit code matches final state.
- **No lane claims another's work:** capital-policy attributes the Cairncross org fact to the "sibling lane row", compute's register_note and models' ask_correction explicitly assign foreign rows/grades to other lanes, and the register writer tags (8+9+14+5) match each lane's self-claim.
- **Fold cross-check gap:** the gala-level FOLD_SECTIONS.txt covers w1/w2/w3 only - no fold sections for ball4-luncheon-follow exist on disk to cross-check (fold_gate.sh not run; not part of the ask), so fold-side numbers for this run could not be verified against anything.

## Filing verdict

**DONE.** Filed 4 GALA LINKS rows into `memory/corpus/LINKS.jsonl` and one BALL4 CLOSE STATE entry into `memories/session/next-window-handoff.md`.

- LINKS ledger: dedupe scan first (json parse of every line): 201 existing rows, 0 prior ball4-luncheon-follow srcs, so 4 candidates -> 4 appended; post-append whole-ledger re-parse OK, ledger 201 -> 205, 4 slug rows with 4 unique srcs, ids `GALA-ball4-luncheon-follow-<lane>`, kind gala, slug `ball4-luncheon-follow`, src `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/<id>.json`, division-B author/lane fields mirroring the prior ball3 gala row schema. Titles per the rule (top law, else changed decision): defense-enterprise "deployment-in-the-loop beats model-sale (Palantir pattern)" (lane JSON rows[0].law); compute "sensed-never-done (luncheon follow)" (from the ask's top law; lane JSON carries it via decision_changed/estate_synthesis, noted in the row); models and capital-policy have top:null, so titles are their armed decision and changed decision respectively. No em-dash in any filed text (asserted in the writer script).
- STATE entry: one "- BALL4 CLOSE 2026-09-29 23:20Z" entry with danced count 4 (basis: lane JSON ok/status flags - ok:true, ok:true finished 22:00Z, done, complete), decisions changed (2 executed: in-place watchlist register corrections and the Commerce/BIS-over-Congress/FTC sovereignty re-ranking; 1 banked unexecuted: compute buy-window re-quote inputs; 1 armed unexecuted: models parity-window distill cycle), B-division finish 4/4 with per-lane check status including the defense-enterprise fold repair (check re-scoped to writer filter, rerun receipt exit 0: `lanes/follow-defense-enterprise.check.rerun20260929.txt`) and the capital-policy unverified-on-disk fetch boundary, graves filed 0, and the 4-row LINKS ledger 201 -> 205. Pre-append guard confirmed no prior ball4-luncheon-follow entry existed; post-append count of "BALL4 CLOSE" = 1.
- Grounding checks run by the filing step: (1) shared-register recount of `watch/inbox/luncheon_watchlist_20260929_signals.jsonl` by writer = 36 rows (defense-enterprise 8, models 9, capital-policy 14, compute 5), byte-matching every lane JSON's claim; (2) all four receipts confirmed on disk (`watch/inbox/ball4/defense-enterprise.md` 5,857B, `models.md` 5,670B, `capital-policy.md` 11,203B, `compute.md` 7,647B); (3) graves = 0, verified by filesystem scan (no GALA_GRAVE_* under any watch/inbox/ball4 path, no ball4/graves dir, no fold_gate output at the ball root, which holds only `lanes/`).
- Not done (stated as such): the filing step did not re-run the lanes' own check instruments; their exit-0 claims are cited from lane JSONs and their on-disk check receipts (`lanes/follow-defense-enterprise.check.rerun20260929.txt`, `lanes/follow-models.check.txt`, `lanes/follow-capital-policy.check.txt`, `lanes/follow-compute.check.txt`). The ask was a filing ask, not a re-verification ask. See the review verdict above for the reviewer's independent reruns (defense-enterprise's original instrument does not reproduce on final disk state).
