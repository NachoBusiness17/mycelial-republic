# ERRATA for the 48h synthesis chapter (append-only)

ERRATA 001, written 2026-10-01 by lane fill-191m-errata of the fillball-1001 ball
(archive: watch/inbox/gala_20260925/fillball-1001/lanes/fill-191m-errata.json).
This file is APPEND-ONLY: later errata append below, never rewrite above, never
edit a landed errata silently. House laws: ascii only, no em or en dashes, every
claim carries the check that stands on it.

## ERRATA 001: the 191.8M-token mine headline is a phantom; STRUCK

What stood: STORY.md:240 (section 5, "The mine's two deaths and amendments")
read "... 5 steal cards with falsifiable probes, 191.8M tokens spent, and the
two percolator code reads verified in-session ...", citing
watch/inbox/frontier_olm_20260928/DIGEST.md, "executive summary and register
table", as the named source.

Why struck, on the bytes:

1. The named source carries no such number. `grep -c "191"
   watch/inbox/frontier_olm_20260928/DIGEST.md` returns 0 with exit 1 (run this
   session, 2026-10-01; first found by the measure lane same window,
   measure.md:81, then re-confirmed by audit lane a08-48h-synth and gap
   register rank 4). The DIGEST's 13 "token" mentions are paper-content
   numbers (88k working sets, 1,506.5 vs 4,010 medians, a 262,144-token
   context, a char-vs-token budget note), none is an aggregate spend total.
2. No REGISTRY row binds it. memory/workflows/REGISTRY.jsonl carries seven
   frontier-olm-mine rows (lines 31 to 35 and 38 for the 09-29 window, line 40
   the 09-30 saved-workflow registration); every row holds ts, digest, script,
   verdict PASS and the seven gate checks, and NO row carries a token total.
3. The run journal binds nothing either. The a08 audit named the journal
   (.zcode/workflow-runs/dwfrun-c41194a8-e725-4bd7-8ee8-5f46206f8fde.mjs,
   31,822 bytes, re-measured this session): it is the compiled workflow
   payload; its one "token" hit is prompt-law text; zero "191.8", zero token
   accounting fields.
4. Provenance of 191.8M is unboundable from any estate surface: no receipt,
   ledger, usage journal or register row in the estate carries a total it
   could be a rounding of. Per the gap register's own recommendation (fill 4:
   "bind to workflow REGISTRY rows or cut the number"), the REGISTRY rows
   cannot bind it, so it is CUT, not re-bound.

What replaced it (STORY.md:240, edited in place 2026-10-01 so every existing
pointer to line 240 lands on the strike, no other line moved): the phantom
clause is replaced by a bracketed ERRATA marker naming this file and the
REGISTRY-row truth (six PASS rows, no token accounting). What the sentence
still claims is unchanged and byte-checks against the same DIGEST: 32 of 32
sweep returns ok, 21 confirmed finds, 3 unconfirmed held, 5 steal cards, and
the two percolator code reads verified in-session (DIGEST.md:18 and 27, 41).

Second live carrier struck the same sitting: .agents/skills/frontier-mine/
SKILL.md:50 (the Lineage section) carried "2026-09-29: 191.8M tokens, 32/32
miners, 21/24 confirmed, 5 organ-mapped" as fact. The 191.8M there is struck
with a bracketed pointer to this errata; the sibling counts stay (32/32
sweeps, 21/24 confirmed, 5 cards all byte-check in the DIGEST and RECEIPT).
The skill card is tracked and read before every daily mine fire, so leaving
it live would have re-propagated the phantom daily.

Carrier census, estate-wide, this sitting (grep "191\.8" over the tracked
tree via git grep, plus a bounded text sweep over watch/ memory/ queue/
state/ docs/ tools/ mag/ scripts/ tests/; raw output at
watch/inbox/gala_20260925/fillball-1001/lanes/fill-191m-errata.check.txt):

- Live carriers of the number as fact: exactly two, both struck above
  (STORY.md:240, SKILL.md:50).
- Record carriers left untouched on purpose (they quote or flag the phantom;
  they are the audit trail, not the disease): watch/inbox/48h_synth/measure.md
  :81-82,192 (the original UNVERIFIED flag); watch/inbox/gala_20260925/
  48h-synthesis_RECEIPT.md:48,60,91,103 (receipt of the flag);
  watch/inbox/gap_analysis_20261001/GAP_REGISTER.md:56,77,101,104 (rank 4 and
  fill spec); memory/runs/mickey17_v2/runs/gap-analysis-of-the-estate-s-09--15/
  lanes/a08-48h-synth.json + a08-48h-synth.checks.json + a15-rollup.json +
  a15-rollup.checks.json (the audit lanes); watch/inbox/gala_20260925/
  48h-synthesis/lanes/measure.json + measure.check.txt (measure lane bank);
  watch/inbox/MICKEY17_V2_RUN_SPEC_ADDENDUM.md:63,132 (byte-checked quote
  table); watch/inbox/ractor50/selfsteal.md:240 (describes the flag);
  corpus/steal/MASTER_MICKEY17_V2.md:82 (master ledger row); watch/inbox/
  ractor_engine/2026-10-01-dogfood-gaps/*.md (19 hits: the ractor lenses
  scoring the gap as LIVE, which this errata now cures); tools/citation_lint.py
  (11 hits: the sibling fillball lane's founding fixture, embedded bytes by
  design so this strike cannot break its suite, its own comment at :542
  anticipates it); watch/inbox/gala_20260925/fillball-1001/lanes/
  fill-citation-lint.json (that lane's JSON); this file and the receipt.
- Non-carriers (unrelated 191.8 substrings, no action): corpus PDF link-rect
  coordinates (191.843, 191.856), a tracked stray HTML file's CSS values,
  heartbeat unix timestamps ending 191.88 (memory/mail/t*/heartbeat.jsonl),
  flight_recorder latency_ms 4191.8, an orchestrator task duration_s 191.8,
  trajectory steps.jsonl command logs (41 hits: audit lanes' own grep
  commands recorded in the step log).

Falsifier for this errata: any future surface asserting an aggregate token
total for the 09-29 frontier-olm-mine run must cite a receipt that carries
the number (a usage ledger row, a run journal field, a REGISTRY row), or it
inherits this phantom. As of this sitting no such surface exists.

 debt honored: GAP_REGISTER rank 4 / fill spec 4 (a08-r2), the fillball-1001
 ask "fill-191m-errata". Byte evidence for every check above is in
 watch/inbox/gala_20260925/fillball-1001/lanes/fill-191m-errata.check.txt.
