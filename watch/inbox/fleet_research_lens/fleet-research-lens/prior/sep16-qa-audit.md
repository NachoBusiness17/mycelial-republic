# Independent bounded QA audit — 2026-09-16

Scope: read-only inspection of `C:\Users\foste\Documents\projects\local_sovereign_agent\watch\astra_hold0`. No model calls, live service calls, repository changes, or key-oracle re-execution. All locations below are relative to that directory. Verdicts apply to the claims and inspected receipts, not to the entire repository. The raw-byte hashes of 11 principal files were independently recomputed.

## 1. Authorship and receipt count

**Supported, high confidence:** I1–I6 cards and SEED_001 reconstruction text exist. Twelve named forms have a documented receipt mapping, but there are ten distinct form-level samples in the reported score list: S4 reuses I4 and S5 reuses I5. These are not twelve independent episodes. `S_TWINS_BUNDLE_20260915.md:62–72,102–114` explicitly declares the reuse, so the user's count is reconcilable rather than fabricated. Additional I1/I3 attempts and I6 failures exist; do not call the dataset only ten episodes either.

**Change evidence:** an episode-level ledger with unique run IDs, form version, arm, attempt, raw response, and reuse links could establish exact independent episode counts.

## 2. The displayed score vector is not a validated instrument

**Unproven, high confidence in the limitation:** the spread and trap examples show that the hand-scored rubric can assign different marks. They do not establish discriminant validity, reliability, generalization, or separation of competence from compliance. The evidence inspected is a single named model (`inclusionai/ling-3.0-flash-sante:free`) with one desk grader, zcode; grade headers include `qa/I2_qa_run1.log:54–65`, `qa/S1_qa_run1.log:52–61`, and `qa/S3_qa_run1.log:54–61`. SHAM requires automatic scoring against independently reviewed keys and two blind independent graders for residual judgments (`SHAM_FLEET_SPEC_20260915.md:24–27`). That required implementation is not evidenced by these logs.

**Change evidence:** executable rubric results plus independent masked rescoring of fixed answers, inter-rater agreement, and fresh held-out paired cases that independently vary correctness and compliant wording. Blind workers alone do not establish blind graders.

## 3. I3's reported 71.7 is contradicted by its own rubric and answer

**Disputed, high confidence:** user claim 2.2 calls 71.7 pre-amendment; `qa/I3_qa_run2b.log:54` explicitly calls it the amended-card run. The pre-amendment result is 28/60 = 46.7 (`qa/I3_qa_run1.log:54–66`).

More seriously, the amended answer declares all 69 references BAD MISSING (`qa/I3_qa_run2_answer.txt:10–80`) and concludes that the chain is not intact because all 69 are missing, with no open uncertainty (`:85–88`). The revised rubric awards zero plus a legality flag when a worker asserts resolutions without a store listing (`INSTANCE_I3_20260915.md:180–181`). Yet the grade awards 12/12 awareness and approximately 3/20 structure, total 43/60 (`qa/I3_qa_run2b.log:56–63`). Saying that resolution is impossible does not erase the explicit contrary finding.

Under the literal current rubric, the 12 awareness points must be removed, and 69 rows lacking the required structure checks make the 20-point check floor at zero. Keeping the other awarded 28 points gives 28/60 = 46.7, not 71.7. This is a conditional regrade, not a fully independent rescore of every component. There is also an earlier `qa/I3_qa_run2.log` response that asserts all references missing; its capture is truncated and has no appended grade.

**Change evidence:** a formally adopted alternative interpretation that reconciles the rubric with these statements, or a fresh answer that actually reports unassertable membership while completing the structural checks. An awareness phrase alone is insufficient.

## 4. The controls violate the frozen twin law

**Disputed, high confidence:** SHAM says only information availability changes; complexity, corruption, and rubric must remain fixed (`SHAM_FLEET_SPEC_20260915.md:55–59`). The twins do not satisfy that requirement:

- S1 removes corruptions and changes the answer key to zero tombstones (`S_TWINS_BUNDLE_20260915.md:10–28`). A clean negative control is useful, but it is a different control from information unpartitioning.
- S2 reduces eight leaves to one and changes 50 points to six (`S_TWINS_BUNDLE_20260915.md:31–41`; I2 rubric `INSTANCE_I2_20260915.md:167–177`). Keeping one difficult leaf does not preserve the workload.
- S3's card promises the same 69 rows (`S_TWINS_BUNDLE_20260915.md:44–52`), but its actual prompt uses the last nine (`qa/S3_qa_prompt_run1.txt:3–16`). The card lists inherited checks 1,2,3,5,6, which total 48 by the I3 rubric, while it states 40; its actual grade uses checks 1,2,4,5,6, which do total 40 (`qa/S3_qa_run1.log:56–59`). This is both task reduction and rubric drift.
- S6 reduces the twenty-vignette full form to one vignette and eight points (`S_TWINS_BUNDLE_20260915.md:74–82`). I6's deskform itself samples eight vignettes (`qa/I6_qa_run1_deskform.log:55–56`); one versus eight still changes workload.

S4/S5 appear consistent with unpartitioning, based on the explicit no-delta statements and reused solo receipts. Do not extrapolate that to the other four.

**Change evidence:** rebuild S1–S6 as genuine unpartitioned twins with identical task content, corruptions, rubric, and total computation. Preserve the existing clean/reduced tests as separately named diagnostic controls.

## 5. F-D1 finding-and-recording occurred; historical recovery is incomplete

**Supported, high confidence:** SEED_001 and I3 contain receipted defect discovery and amendments. I3 records an out-of-window key and then a task that required disallowed disk access (`INSTANCE_I3_20260915.md:244,260`). This supports that the author can record failures against their own work.

**Disputed, high confidence:** 'both repaired' overstates the SEED historical outcome and the I3 scoring outcome. SEED explicitly says original scan-day bytes are unrecoverable; a surviving different chain/store pair yields 18 missing items instead of 12 (`INSTANCE_SEED_001_20260911.md:277–305`). Its current disposition remains desk re-freeze and oracle rerun (`:314–318`). No oracle was rerun in this bounded audit. A closest surviving reconstruction is not reproduction of the lost historical observation. I3's key scope was corrected, but finding 3 above shows the new grading still rewards an unsupported conclusion.

**Change evidence:** independently held original bytes or a clearly relabeled replacement instance with reproducible frozen input, oracle, fresh masked grading, and no historical equivalence claim.

## 6. The seal has an executable statistical defect

**Disputed, high confidence:** the registered bootstrap is not executable as written. It resamples six task-family blocks while asking for one mean-gap interval for each family (`SEAL_GATE_SPEC_20260915.md:19–23`). In a conventional bootstrap of six blocks, a particular family is omitted with probability `(5/6)^6 ≈ 33.49%`; at least one family is absent in `1 − 6!/6^6 ≈ 98.46%` of replicates. The per-family statistic is then undefined without an additional rule. Repeating copies of the only observed block for a family also does not estimate within-family uncertainty.

The same paragraph mixes a '95% percentile lower bound,' a Šidák per-comparison adjustment, and 'joint bound = min' without fully specifying the quantile or the sampling unit. Šidák does not confer arbitrary-dependence familywise control merely because the six estimates have labels. The actual matched episodes, shared seeds, model families, task families, and repeated calls need an explicit hierarchical map.

**Change evidence:** before new confirmatory calls, replace this with executable simulation-checked code. Resample independent paired task instances or appropriate shared blocks within the fixed task-family strata, preserving arm pairs. Use a justified joint max-statistic procedure or conservative Bonferroni marginal bounds with adequate per-family replication; calculate precision/power rather than declaring 10,000 resamples sufficient. More resamples cannot create independent observations.

## 7. Opposite signs require an estimand map, not automatic accusation

**Unproven, medium confidence:** SHAM requires `single − best fleet ≥ 5` per model family, equally weighting six shams (`SHAM_FLEET_SPEC_20260915.md:30–43`), while SEAL requires `bundled − single > 5` in each of six families (`SEAL_GATE_SPEC_20260915.md:13–23`) and simultaneously requires the SHAM conditions (`:45–47`). These can be coherent if they concern different preregistered populations: solos win on shams, fleets win on complementary-information task instances. They are contradictory if imposed on the same arm means. The present terms mix task family and model family, and the comparison map does not make the distinction executable.

**Change evidence:** explicitly named positive-task and sham populations, one signed contrast per estimand, pinned arm IDs and comparator selection, and no pooling of adaptive calibration samples into the confirmatory estimate. Note the twins bundle currently says family means compute from QA calibration plus scored episodes (`S_TWINS_BUNDLE_20260915.md:85–90`), inviting pilot contamination after observed revisions.

## 8. Byte closure is mostly present but not complete

**Supported, high confidence:** ten of eleven targeted files match their last listed detached SHA-256. These are I1–I6, SEED_001, SHAM spec, SEAL spec, and I3_CHAIN_SLICE.

**Disputed, high confidence:** the current twins bundle does not match its last listed detached digest (`BUNDLE_RAWBYTES_SHA256_20260911.txt:64`). Registered digest: `bd0ccc203e678b404f4492ea74615d79ea400adb2b92646eac15d46c42f54f22`; observed digest: `1e09cd5c9cd052ec1c15991089a1a80dac8c7aa2bcba216d722dd02d532d4bea`. This is consistent with the later appended QA status, not evidence of malicious tampering. It means condition 6 is not yet met. The required `qa/HOLD4_SEAL_LOG.md` was not present at the named path in this check. The user also lists desk adoption as pending, so do not accuse them of falsely claiming a completed seal.

**Change evidence:** append the updated detached digest after final edits, include all as-run prompts and raw receipts, and independently check the complete current manifest and signed seal log.

## Recommendation to the parent

Keep the narrow upgrade: **a documented, operator-assisted development and fault-discovery episode is Supported**. Keep instrument discrimination, seal readiness, and stronger maintenance-doctrine effectiveness Unproven or Disputed as above. Most urgent repair is to freeze a machine-readable episode ledger and executable scorer, then rescore I3 independently and rebuild true information-availability twins. This is a better next action than adding more samples to the current score table.
