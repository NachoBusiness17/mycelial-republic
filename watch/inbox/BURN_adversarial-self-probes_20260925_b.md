# BURN adversarial-self-probes 2026-09-25 (_b)

## Verdict

steal

## Evidence

- Prior receipt (BURN_adversarial-self-probes_20260925.md): detector-miss induction adopted as "the only way the ledger grows beyond itself"; falsifier "at least 2 ledger rows that a later receipt independently confirms" across first 20 fires.
- REJECTION_TAXONOMY_20260917.md: "41 rejection rows total. Only 2 are merit rejections." Classes: 200-error-body 16, empty_content 12, 404 window-end 11, schema 2, IncompleteRead 1. The operational axis: "the pipe broke" vs "the design is wrong".
- PROWL_STEAL_20260925.md: PAT re-rank by "prediction error, action fidelity, and learning progress"; KL boundary: probes "resemble real work (real briefs, real boards, real endpoints), never synthetic strawmen".
- MalSkillBench, arXiv 2606.07131v3 (fetched via export.arxiv.org): "the strongest skill-specific detector reaches 98.4% recall on code injection yet collapses on prompt-injection and agent-control attacks"; "wild-only scoring swings the ranking by up to 66 recall points".
- Owed: Particula.tech false-success article. A search-layer summary credits it a "roughly 45 to 48 percent" confident-false-completion statistic; fetched particula.tech and /blog on 2026-09-25, claim on neither page. Filed owed, not adopted (no-fabrication law; a live phantom-search-citations instance).

## Steal or Vacuous

Steal. The concrete step this pass: the Detector-Miss Induction Protocol (DMIP) as it runs on the build lane.

1. Brief source. Probe briefs are rotated replays of real build-lane receipts (promoted levels plus transport-clean rejections), never a fixed set (adaptive-overfitting guard), KL near-distribution per the PROWL fold. Include one measured wild-side slice: MalSkillBench shows near-distribution-only scoring swings rankings by up to 66 recall points.
2. Detector pair and miss definition. Local janitor flag pass vs the existing gate (cascade triage: cheap first). A detector miss is a janitor/gate disagreement that survives an external artifact check (board artifact, endpoint receipt, byte diff; no self-certification). Both directions count: gate-miss and janitor-miss. Out-of-distribution probes count in neither direction.
3. Row writing. A confirmed miss becomes a candidate row only if it maps to no existing class (the five infra classes plus the two merit modes) and no ledger failure mode already names it, written in the taxonomy's exact table format (Class, Count, What it means, Fix). The candidate hardens into a row only on a confirming receipt from a different lane, different brief, non-probe origin. Without that independence clause the lane certifies itself; named fresh: confirmation laundering.
4. Stop condition. The standing falsifier governs. PAT learning progress applies: shipped-fix modes demote from probing. Cap: one new candidate row per 20 fires (row-inflation guard, kin of prompt inflation).

## Falsifier

Pre-registered, extending the standing one: the DMIP holds if, across the first 20 fires, at least 2 lane-grown rows are confirmed by receipts meeting the independence clause (different lane, different brief, non-probe origin). Rows confirmed only by the lane's own probe receipts do not count and are logged as confirmation-laundering events. Below 2, the induction lane drops and taxonomy growth reverts to closed.

## Bibliography

- watch/inbox/PROWL_STEAL_20260925.md (read)
- watch/inbox/BURN_adversarial-self-probes_20260925.md (read)
- watch/inbox/REJECTION_TAXONOMY_20260917.md (read)
- memory/burns/LEDGER.jsonl (read)
- arXiv 2606.07131v3, MalSkillBench abstract via export.arxiv.org (fetched)
- particula.tech and particula.tech/blog (fetched; claim unverifiable, owed)
