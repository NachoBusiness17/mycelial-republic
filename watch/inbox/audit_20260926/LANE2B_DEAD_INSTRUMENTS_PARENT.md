# LANE 2 PART B — DEAD INSTRUMENT SWEEP (parent seat, after lane 2's harness failed)
## 2026-09-26

*Lane 2 crashed three times on its own `rg` PCRE look-around bug*
(`rg: look-around, including look-ahead and look-behind, is not supported` —
it needed `--pcre2`). Each crash dropped a partial count. Rather than wait for a
fourth failure I re-ran the measurement in pure Python:*
`memory/audit_20260926/dead_instrument_sweep.py` → `lane2_dead_instruments.json`

---

## HEADLINE: 80 of 164 tools are dead. Half the fleet calls nothing.

```
tools/*.py examined : 164
  LIVE    34
  ORPHAN  50
  DEAD    80
tested     :  34   (exactly the LIVE set)
documented :  15
```

**The live set and the tested set are the same 34 tools.** Nothing that lacks a
caller also lacks a test *and* a doc reference by accident — the fleet is
cleanly split into instruments that are wired and verified, and instruments that
are simply files.

**80 DEAD** = no other code imports them, no test references them, no doc
mentions them. 746 KB of source. Largest by size:

```
duty_fuzz.py            53,558   wandr_selfeval.py       34,739
ghost_tournament.py     27,769   quote_audit_wide.py     25,535
oracle_calibration.py   24,937   cathedral_build.py      22,090
mcp_pin.py              20,471   build_adam_pdf.py       18,516
```

## A correction I had to make to my own instrument

My first run reported `prepush_paths_changed.py` and `checkbox_receipt_gate.py`
as **DEAD**. Both are wrong, and I caught it because I already knew from the
lane 7 verification that both run inside `githooks/pre-push`.

Root cause: `githooks/pre-push` has **no file extension**, and my haystack
filtered on suffix — so the single most important file in the enforcement path
was never read. The tool that finds dead tools could not see the hook.

After the fix, the four gates that decide a push read correctly:

| gate | verdict | code refs |
|---|---|---:|
| `violation_ratchet.py` | LIVE | 3 |
| `config_seal.py` | ORPHAN | 2 |
| `checkbox_receipt_gate.py` | ORPHAN | 1 |
| `prepush_paths_changed.py` | ORPHAN | 1 |

Every gate is in the hook; only the ratchet is also tested. This is the same
shape as lane 7's finding, arrived at independently from a different direction.

## What this means for the fleet's self-image

The repo carries **164 tools** and a doctrine that says to dogfood them every
wave. Measured: **34 wired, 130 not.** A reader of `tools/` sees an instrument
fleet; a reader of actual call-graph sees 34 instruments and 130 files.

This compounds lane 6's likely finding (laws that are prose-only) and the
parent-seat gate findings: the enforcement surface is *narrow* — a handful of
gates in one hook file — while the *instrument surface* is *wide*. Nothing in
the repo appears to measure that ratio, so the fleet can grow `tools/` without
bound and every gate report stays green.

**Honest caveat on scope:** the haystack is code + docs + tests + configs +
hooks, deliberately excluding `corpus/`, `attic/`, `library/`, `mine/`. A tool
referenced only from inside those trees would score as DEAD. That is unlikely
for gate code but possible for data tools, so treat DEAD as "not referenced by
any first-party surface", not as "provably unreachable".
