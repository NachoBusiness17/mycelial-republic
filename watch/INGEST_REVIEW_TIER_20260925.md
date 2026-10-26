# INGEST REVIEW TIER + SOURCE-TRUST SCORE - 2026-09-25

Seat: memsentry-tier (MICKEY-17 wave, OWED knockdown). Fold row: agent-memory-sota#0
(`corpus/steal/MASTER_MICKEY17_V2.md:70-73`): MemSentry pattern = persistent-memory write
triage as a deterministic gate that escalates trusted-source suspicions to human review
instead of silent exclusion. Task text, verbatim: "add a Review tier + source-trust score
to the estate's existing fail-closed ingest ... so trusted-source suspicions route to an
operator_inbox advisory tier."

## WHAT THE INGEST ORGAN IS

`mag/trust_gate.py` - the fail-closed ingest gate ("only NOVEL, DEDUPED, HIGH-TRUST data
writes to the chain"). Sits in front of the swarm tools; wired at `mag/swarm_tools.py:151-161`
(verkle_write refuses to write unless `verdict == "ACCEPT"`; gate unavailable = fail closed,
not written). Its v1 verdicts were binary: ACCEPT / QUARANTINE / REJECT. A trusted-source
suspicion (e.g. operator spam) was written to `memory/trust_gate/quarantine/` with zero
operator notification - exactly the silent exclusion the fold row names. Proof of the old
behavior still on disk: `memory/trust_gate/quarantine/q-02c08c2560a3d0672316.json`
(source=operator, flags=[low-entropy-repeat], no verdict field, no trust_score).

watch/inbox was grepped for the ingest organ first (fold-row law): no newer memory-ingest
organ is defined there; `mag/trust_gate.py` is the organ the fold row's action points at.

## THE PATCH (all in repo, read it, do not trust this memo)

`mag/trust_gate.py` (schema bumped trust_gate.v1 -> trust_gate.v2, only internal refs to the
schema string, checked by grep):
- NEW VERDICT REVIEW: suspicious content (poison flags) from a TRUSTED source
  (`_is_trusted_source`: SOURCE_TRUST >= TRUST_THRESHOLD, i.e. 0.6+) is held in quarantine
  AND routed to `operator_inbox.commit_guidance(advisory, source="trust_gate")` - the same
  inbox channel pro-library/ghost/press_digest use. Never auto-written; fail-closed kept.
  Route is best-effort (try/except): an inbox failure never un-holds the item.
- QUARANTINE now means: suspicious from an UNTRUSTED source (rep < 0.6 but overall trust
  score still clears 0.6, e.g. seed). No operator advisory.
- REJECT unchanged: duplicate / low-trust. Low-trust still silently excluded by design
  (untrusted sources do not earn operator attention; that is the MemSentry split).
- TRUST SCORE IN THE REGISTER: every ACCEPT stamps `trust_score` into the accepted-writes
  register `memory/trust_gate/seen.json`; every quarantine/review record carries
  `trust_score` + `verdict` (+ `review.routed` for REVIEW). `status()` reports `n_review`
  and the v2 contract.

`mag/trust_gate_audit_check.py` (self-test, rewritten):
- v1 self-test was destructive (wiped the live register + quarantine every run; it deleted
  the pre-existing 2026-09-13 register entry and quarantine record during this ask's first
  run - both were restored byte-for-byte from readings taken before the run).
- v2 self-test backs up and restores live register/quarantine/inbox; redirects the live
  operator inbox to a temp file so audits never file advisories into the real inbox.
- Covers: ACCEPT + trust_score in register, duplicate REJECT, low-trust REJECT,
  trusted spam -> REVIEW + advisory pending in inbox + record stamped, untrusted
  (seed) spam -> QUARANTINE + no advisory.

## CHECKS RUN (this ask, this machine)

1. Self-test (the ask's named check), exact command:
   `./.venv/Scripts/python.exe -m mag.trust_gate_audit_check` (cwd = repo root)
   -> `{"status": "all checks passed"}`. Re-run after the non-destructive rewrite: same
   output, and live register/quarantine verified intact afterwards
   (`seen.json` still holds the 2026-09-13 entry; quarantine still holds q-02c08c...).
2. End-to-end live-path probe, exact command:
   `./.venv/Scripts/python.exe _verify_review_tier_20260925.py` (scratch harness kept in
   repo root; it backs up live state and restores it after) -> all three lines OK:
   - LIVE REVIEW ROUTE OK: pending_n +1, advisory_id inbox-003238, source=trust_gate,
     trust_score 0.795
   - REGISTER TRUST_SCORE OK: {"ts": ..., "source": "operator", "domain": "verify",
     "trust_score": 0.925}
   - SWARM TOOLS GATE OK: verkle_write with trusted-source suspicion ->
     {"ok": false, "gated": "REVIEW"} - the write did not happen (fail-closed preserved).
3. CLI smoke: `./.venv/Scripts/python.exe -m mag.trust_gate gate "cli smoke probe with
   enough content bytes" --source operator` -> ACCEPT; and `-m mag.trust_gate status` ->
   schema trust_gate.v2, n_accepted 2, n_quarantined 1, n_review 0.
   Note: that CLI smoke ACCEPT added register entry `6470d0bcda2d7167b733` - an honest
   record of a real gate pass, left in place on purpose.
4. Live inbox residue check: no `source == "trust_gate"` notes remain in
   `memory/operator_inbox.json` (checked via python -c json load; empty list).

## NOT DONE / HONEST GAPS

- The 04:00 fold / memlance path is NOT rewired in this ask (that is fold row
  agent-memory-sota#3, a different seat's line: revoke memory-write tools from
  conversational seats). Only the gate organ itself changed.
- rib_bus doctrine alignment inside `trust()` is still the weak 0.5-default proxy it was;
  untouched by design (out of scope).
- Did not run the full repo pytest suite; the ask's check is the trust_gate self-test,
  which was run (see above). `tests/test_roadmap_gap_probe.py` touches only
  governor_autorun's trust_blocked flag, not trust_gate verdicts (verified by reading it).
