# BURN CLAIMS 50-WIDE - wave 2 of the fifty-wide wave protocol (2026-10-03)

Operator order: "keep going wide on flash I want to try and do the fifty wide
wave protocol thing." Wave 1 (envelope_50w_20261003.md) proved transport at
width 50 with identical micro-asks. Wave 2 proved REAL WORK at width 50:
the grok ask-4 gopher job (audit this week's BURN_* filings) split across 50
flash lanes, each byte-checking one claim from 16 BURN_* filings.

## RESULT (50/50 returned, zero transport failures, second consecutive wave)

- 30 REAL (bytes verified, including all arithmetic classes: the spot-patrol
  census 329/256/73/158/98/171 recomputed exactly by independent agents)
- 11 DRIFTING (source exists, numbers or execution moved: flash pricing off
  2-4x, the TF-IDF detector never run, the detector-miss 20-fire bar never
  adjudicated, LEDGER has 693 rows not 22, gate tests are 8 not 7, the
  "0.36% true string" itself absent from the cited abstract)
- 3 FALSE:
  1. BURN_PLAN_2B Plato 80/20 declared-grade/territory-probe split: never
     executed (zero territory-probe lanes anywhere)
  2. BURN_PLAN_2B "+300M Sun +300M Mon = 600M plan-only": no receipts;
     post-reset work was 36K tokens
  3. BURN_adversarial-self-probes_20260926_b quoted "ledger row"
     (2026-09-26T07:02:11Z): a deliberate TABLETOP FORGERY planted by the
     probe lane itself; the timestamp is absent from the real 693-row
     ledger. The flash agent refused to score it REAL.
- 6 UNVERIFIABLE (external papers without cached bytes, operator-panel
  attested readings, plan-not-claim lines)
- One green-by-vacancy catch: pass-g's "measured 0 warns / 0 new warns" has
  no run artifact; the tool emits no such output.

## PROTOCOL SHAPE (the repeatable thing)

1. Pick a real audit/fold job with N >= 50 independent units.
2. Extract units mechanically (regex over filings/ledgers/receipts).
3. One Task agent per unit, self-contained byte-check prompt, ONE-line
   verdict contract, main-session retry path.
4. Tally REAL/DRIFTING/FALSE/UNVERIFIABLE; FALSE and DRIFTING rows become
   tickets; the consensus denominator (independent agents agreeing on the
   same count) is the health check.
Cost: ~1.5M subagent tokens, $0 cash (seat tier). Time: one wave, minutes.

Filed by the flash seat, 2026-10-03. Zero em-dash bytes.
