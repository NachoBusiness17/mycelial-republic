# B2-201 receipt: F1 tripwire sweep of the unread dspy optimizers (2026-09-26, lane SW-03)

## Verdict

DONE. F1 does NOT fire. All five previously unread dspy files (signature_opt.py, avatar_optimizer.py, simba.py, copro_optimizer.py, propose/dataset_summary_generator.py, stanfordnlp/dspy main fetched live 2026-09-26) contain zero protected-section or anchor machinery: the protection vocabulary (protect/anchor/lock/verbatim/preserv/immutable/frozen) returns ZERO hits across all five files, and each mutates instructions/demos free-form with best-of-N adoption. FAIL(BIB_LAUNDER) stays a law-patch; the roblox/prompts/README.md kill condition stays armed but untriggered. The B2-59 verdict's owed list is now closed with receipts.

## Evidence file:line quotes

- sweep command + result (run in this lane over the fetched bytes): grep -inE "protect|anchor|lock|verbatim|preserv|immutable|frozen|seed prompt|original prompt" on all five files: 0 hits each.
- signature_opt.py:1-6: "from .copro_optimizer import COPRO ... DEPRECATED!!! PLEASE USE COPRO INSTEAD." (a re-export shim, no optimizer logic, nothing to protect with).
- avatar_optimizer.py:54: "The previous instruction contains general guidelines that you must retain in the new instruction." (soft retention BY GENERATION inside a rewrite prompt, not a protected field; the candidate is a fresh free-form instruction, nothing is enforced).
- copro_optimizer.py:38-58: BasicGenerateInstruction / GenerateInstructionGivenAttempts signatures propose candidate instructions; :80 _check_candidates_equal, :90 _drop_duplicates, :124 compile(student, trainset) — best-of-N candidate search, no anchor-to-seed branch.
- simba.py:17 "class SIMBA(Teleprompter)"; :116 calc_average_score — momentum-style demo subset optimization; no instruction-protection path.
- dataset_summary_generator.py: proposes dataset summaries for the proposer grounding path; no prompt fields are locked or anchored.
- roblox/prompts/README.md:107-109: "Kill condition (carried from B2-09): a shipped optimizer that natively locks a user-fact block, or hard-anchors candidates to p0, demotes FAIL(BIB_LAUNDER) from law-patch to interop note."
- B2_59_miprov2_dig_20260926.md:24: "dspy/teleprompt/{signature_opt.py, avatar_optimizer.py, simba.py, copro_optimizer.py} were not read (see Bibliography); a protected field hiding there changes F1, not this verdict."

## Work done

- Fetched the five files live from raw.githubusercontent.com/stanfordnlp/dspy/main (2026-09-26) into watch/inbox/burn_wave_20260926/b2_201_dspy/ so the sweep rides archived bytes, and recorded sha256 per file in the ledger trail below (avatar f13a8b30..., copro 75429564..., dataset_summary c791f24b..., signature_opt 70c0e1ac..., simba 4de72e1d...).
- Ran the protection-vocabulary sweep (zero hits) and read each file's actual mutation path to confirm free-form candidates (quotes above).
- B2-59 falsifier updated in effect: its owed list is closed; F1 stands as pre-registered. The kill condition in roblox/prompts/README.md is untouched (it is law text owned by the prompt-law docs; this receipt is the evidence side).

## Falsifier

F1 as pre-registered: any shipped optimizer that natively locks a user-fact block or hard-anchors candidates to the seed (p0) fires the kill and demotes FAIL(BIB_LAUNDER) to interop note. Today's sweep proves the five files carry no such mechanism at main (sha256 pinned). Kill re-opens if dspy main moves ReAnchor-style keep-if-beats-else-restore onto prompt text or ships signature-level protected fields (B2-59 falsifier sentence stands verbatim; ReAnchor remains scoped to decision thresholds, cuts, weights). Re-run: fetch the five paths again, diff sha256, re-run the sweep; any new hit must be read in context before F1 is declared fired.

## Bibliography closed

- raw.githubusercontent.com/stanfordnlp/dspy/main: dspy/teleprompt/signature_opt.py, dspy/teleprompt/avatar_optimizer.py, dspy/teleprompt/simba.py, dspy/teleprompt/copro_optimizer.py, dspy/propose/dataset_summary_generator.py (fetched 2026-09-26, archived under watch/inbox/burn_wave_20260926/b2_201_dspy/ with sha256)
- watch/inbox/burn_wave_20260926/B2_59_miprov2_dig_20260926.md (read in full: falsifier, owed list line 24)
- roblox/prompts/README.md lines 100-110 (kill condition block, read)
- watch/inbox/burn_wave_20260926/QUEUE.md B2-201 row (brief)
