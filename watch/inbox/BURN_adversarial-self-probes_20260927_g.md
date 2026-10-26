# BURN adversarial-self-probes pass g, 2026-09-27

## Verdict

steal

## Evidence

Baseline, pre-edit, this pass: "POOL 329 FIRED 158 FRAC% 48.0 CHECKS 292 WARNS 19 ZERO 171"; official draw "PATROL: 12 rows, 9 mechanical checks, 0 warns". 17 bare-eligible rows found; pass f's dominant blind token githooks/pre-push is carried by 10 of them (pass f: "10 of 19 rows use githooks/").

Build (Edit tool only): BARE_PATH_RE = (githooks|scripts|tests|tools|configs|mag|docs)/[\w.-]+; binds only dotless-tail tokens; PATH_RE-bound tokens never re-fire; a bare path fires a check only when the constructed path exists on disk.

After: "POOL 329 FIRED 158 FRAC% 48.0 CHECKS 300 WARNS 19"; draw identical (9 checks, 0 warns, same 12 rows). Eight rows gained a bare-path-exists check, all on githooks/pre-push: B2-215, B2-249, B2-260, B2-328, B2-164, b2-316, B2-451, B2-272. The 17 remaining bare tokens (dir paths like configs/workflow_gate_scenarios, absent mag/ module refs like mag/cost_truth, tools/__init__, tests/selftests) resolved to no file: the existence gate refused every one, so warns could not inflate.

HEAD-vs-edit diff, same pool: "POOL 329 OLDCHECKS 292 NEWCHECKS 300 OLDWARNS 19 NEWWARNS 19 SLUGS-WITH-WARN-DIFF 0". B2-384 keeps all 3 warns; the silencing that killed pass f is structurally blocked because bare paths never join the arity-sensitive path list. Honest limit: fired fraction did not move because all 8 bare-bound rows already fired via other tokens (pass f: "the blind things are the tokens, not whole rows"); the gain is 8 previously-unbindable existence claims now mechanically verified.

## Steal or Vacuous

The fleet adopts: (1) the known-dirs prefix matcher as the landed, gap-shaped fix for the exact gap pass f named, binding extensionless tokens that extension-scoped grammar structurally cannot reach; (2) heuristic isolation as code, not advice: any new claim class must be additive-only, existence-gated, and never join the arity-sensitive path list, so warn silencing is impossible by construction; (3) the fresh pre-registration pass f demanded is discharged by measurement, not re-litigation. PROWL note: the near-distribution cheat was re-running the extension grammar; the receipt-named gap got the gap-shaped fix instead.

## Falsifier

Armed and passed this pass: revert if any pre-existing warn is silenced (HEAD-vs-edit per-slug warn diff must be zero; measured 0) or any warn inflates from guessed paths (existence gate; measured 0 new warns). Pass c's standing falsifier stays armed: two consecutive weeks of zero claim-artifact mismatches and zero acted warnings means the patrol is vacuous overhead. Pass f's bars (10 of 19 blind rows, 58% fired) were consumed executing the extension grammar; this pass reports the same metrics for continuity (0 rows crossed zero-to-firing, 48.0% held) without claiming them.

## Bibliography

- tools/ledger_spot_patrol.py (read whole; edited; git HEAD source for the old-grammar diff)
- watch/inbox/BURN_adversarial-self-probes_20260927_f.md (named gap, revert history, kill criterion)
- memory/burns/LEDGER.jsonl (329 LANDED rows, read-only)
- memory/burns/SPOT_PATROL.jsonl (the two --rows 12 appends)
- Web search thin: "extensionless path matching claim extraction log verification 2026" returned no on-point work (deeplink hijacking, an arXiv LLM case study, CVE-2026-59314, PII tools release notes); consistent with passes e and f.
