# BURN adversarial-self-probes pass f, 2026-09-27

## Verdict

vacuous

## Evidence

Baseline reproduced exactly: 329 LANDED rows; 158 fire at least 1 check (48.0%); the 12-row day draw sums 9 checks ([0,0,1,2,1,1,1,0,0,2,0,1]).

Precision fix on the blind class: the 19 rows with a .ps1/.log/githooks token are not all silent. 18 of 19 already fire via other covered tokens; only B2-314-census-patrol-liveness-tripwire fired 0. The blind things are the tokens, not whole rows.

Extension built as authorized (Edit tool): PATH_RE gains psm1|ps1|log|cmd|sh|rbxlx|lua; KNOWN_DIRS gains logs/ and githooks/ (evidence: B2-246's real paths are scripts/census_patrol_daily.ps1 and logs/census_patrol.log; 10 of 19 rows use githooks/; none use .agents/).

Measured against pass e's thresholds, the extension misses both arms: fired fraction 159/329 = 48.3% (bar: 58%); blind rows gaining a fired check 7 of 19 strict delta (B2-246, B2-357, B2-372, B2-104, B2-469, B2-465, B2-314), 8 counting B2-384's extension-bound find, which nets negative (bar: 10). Live patrol --rows 12: 9 checks before, 9 after, same draw, 5 of 12 rows still zero.

Warn diff (extended module vs git HEAD source, same pool): 19 warns old, 16 new. The extension added zero false warns (all 14 new binds resolve ok on real files) but SILENCED 3 existing warns on B2-384-real-chains-census: added paths broke the single-path sha256/bytes heuristics.

Root cause of the miss: the dominant blind tokens are extensionless (githooks/pre-push, 10 of 19 rows) or dir-prefix-bare (supervisor_autorun.out.log, seat_crashes.log, mag.cmd, B2_164_gate_block_probe.sh). Extension-scoped grammar structurally cannot bind either class. Pass e's build sketch included root-file resolution; it was outside this pass's authorized scope.

## Steal or Vacuous

The grammar reverts; the measurements are the steal. Fleet canon: (1) the spot patrol's pre-registered falsifier executed on schedule, so the PROWL loop has a working abort path, green-by-vacancy is now caught by arithmetic, not by vibe; (2) the true coverage gap is extensionless and bare tokens, so any next build must target extensionless-path binding plus root-file resolution as a fresh pre-registration, not a re-litigation of this one; (3) new law for extractor edits: diff warns, not just checks, because widening the path set silently disables single-path heuristics (B2-384 lost 3 warns to a grammar that looked additive).

## Falsifier

Executed this pass: pass e pre-registered "Revert if (a) fewer than 10 of the 19 blind-class rows gain at least 1 fired check, or (b) the pool-wide fired fraction stays under 58% (baseline 48.0%)." Measured 7 of 19 and 48.3%; grammar reverted same pass; post-revert behavior re-verified identical to baseline (158 fired, 48.0%, 19 warns, draw sums 9). Standing falsifier for the patrol itself (pass c, two weeks of zero mismatches and zero acted warnings means vacuous overhead) stays armed.

## Bibliography

- watch/inbox/BURN_adversarial-self-probes_20260927_e.md (armed thresholds)
- watch/inbox/BURN_adversarial-self-probes_20260927_d.md (via pass e)
- tools/ledger_spot_patrol.py (landed, extended, reverted; git HEAD for the old-grammar diff)
- memory/burns/LEDGER.jsonl (329 LANDED rows, read-only)
- memory/burns/SPOT_PATROL.jsonl (the --rows 12 append)
- Web search thin: "regex coverage extension claim extraction 2026" returned no on-point work (rfp.wiki JMeter extractors, a ResearchGate simplification paper, Debian s-nail man page); consistent with pass e's thin result.
