# B2-206 Workflow judge-seat independence, 2026-09-26

## Verdict

LANDED with an honest mechanism correction. The brief's fix ("give judge agents a subagent_model") is not expressible in the dwf facade: per the dynamic-workflows skill bytes, every subagent "runs on the session's model; there is no per-subagent tool profile or model choice" — the only model lever is the RUN-level subagent_model on CreateWorkflow/AmendWorkflow, which moves ALL subagents, not just judges. So independence is landed as a FIRING CONTRACT plus a gate marker, which is the strongest mechanism the harness actually has: (1) all three judge-seat workflows (the-gala, mickey17-v2, the-50) now carry a dated `judge-model: groq/compound-mini` stamp naming the cross-family model the operator must fire them with (groq vs the GLM/zai session family; id byte-grounded in this wave's own receipts B2_03/B2_35/B2_115/B2_132, not guessed); (2) tools/workflow_gate.py G3 gained the judge-independence marker (G6 soft-warn family): steering present + no judge-model stamp = soft WARN naming B2-60 D2, exit contract untouched (0/1/2 unchanged). Live gate behavior verified both directions: stamped the-gala shows G3 ok clean; unstamped tree-doctrine-dig shows "WARN G3-steering ... judge independence undeclared"; fail_g3 fixture stays hard-FAIL with no warn (marker fires only when steering passes). Scenario suite back to 7 of 7 green (fixtures single-purpose-stamped), gate tests 8 of 8 (one new pin added for the marker). The live cross-family fold falsifier is ARMED-OWED, not run: firing needs a fresh window and the operator's CreateWorkflow confirmation; the exact procedure is in Falsifier.

## Evidence file:line quotes

- Facade constraint (dynamic-workflows SKILL.md, persona section): "Every subagent has the same tools ... and runs on the session's model; there is no per-subagent tool profile or model choice. ... None of this can change after `agent()` — there is no per-task override."
- Stamps (post-edit): .zcode/workflows/the-gala.dwf.ts:28, mickey17-v2.dwf.ts:25, the-50.dwf.ts:20, each "// judge-model: groq/compound-mini (B2-206 firing contract: the dwf facade has no per-subagent model, so the FIRER must set subagent_model groq/compound-mini at CreateWorkflow/AmendWorkflow time; cross-family from the GLM/zai session family per B2-60 D2)".
- tools/workflow_gate.py (post-edit): G3_JUDGE_MODEL_RE = "(?i)\b(judge[-_ ]?model|subagent[_ ]?model)\s*:\s*[a-z0-9][a-z0-9._/-]+"; G3_SOFT_REASON names "B2-60 D2, context freshness is not weight independence"; run_checks arm "if cid == "G3-steering" and ok and not G3_JUDGE_MODEL_RE.search(text): row["soft"] = True ..." with the comment "the reviewer certifies steering, not weight independence".
- Live gate runs (this lane): the-gala "ok G3-steering" (stamped, no warn); tree-doctrine-dig "WARN G3-steering ... [judge independence undeclared: the fresh-reader seat runs same-session-model (B2-60 D2 ...)]"; pre-change baseline had zero warns on the same file.
- Scenario suite: 7 cards red immediately after the marker landed (every un-stamped fixture warned G3), 7 of 7 green after single-purpose fixtures were stamped ("SCENARIOS: 7 cards validated read-only (no registry row written)"); G3_steering.card.json validates with fail_g3 showing hard-FAIL and NO warn, pinning the fires-only-when-ok semantics.
- tests/test_workflow_gate.py: 8 passed (7 pre-existing, incl. the LAW-12 scenario round-trip whose inline fixture needed the stamp; 1 new test_g3_judge_independence_marker pinning warn-without-stamp, clean-with-stamp, no-marker-when-G3-fails, and the subagent_model spelling of the regex).
- Cross-family id provenance: groq/compound-mini appears across this wave's own landed bytes (watch/inbox/burn_wave_20260926/B2_03_endpoint_news_20260926.md:10, B2_35_groq_surgery_20260926.md:5,9,11, B2_115_probe_chain_freeze_20260926.md:9-16, B2_132_steering_fold_20260926.md:9, QUEUE.md:208,307).
- Ratchet after all edits: PASS, NEW=0.

## Work done

- Read B2_60 receipt D2/F2, the three workflow scripts' judge seats, the gate's G3/G6 rows and soft-warn machinery, the scenario card system, and the dynamic-workflows facade docs.
- Discovered and documented the mechanism correction: no per-subagent model exists in the facade; refitted the fix as firing contract (stamp) + gate marker instead of pretending a script-level subagent_model would work.
- Stamped the three judge-seat workflows; extended G3 with the marker; brought the scenario suite and gate tests back to green (7 fixture stamps + 1 inline test fixture stamp + 1 new pin test); kept every fixture single-purpose so each card isolates one gate.
- Ran the gate live on stamped and unstamped scripts, the full scenario suite, pytest, ratchet; em-dash 0 in all added lines.
- Filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- The brief's falsifier, ARMED with exact procedure: in a fresh window, fire the-gala twice via CreateWorkflow (operator-confirmed), once default (session model) and once with subagent_model groq/compound-mini, and diff the midnight-reader verdicts (B2_60 D2 F2). Until that run lands, same-model vs cross-family verdict deltas are UNPROVEN; this receipt claims the mechanism (contract + gate), never the measured independence effect.
- A future facade that gains per-subagent models makes the stamp approach obsolete: the gate marker should then check real per-agent model fields instead of a comment stamp (watch the skill bytes, not this receipt).
- A workflow stamped but fired WITHOUT subagent_model certifies nothing; the stamp is the contract, the firing is the compliance, and nothing in this lane can force the firer (named as the residual, not hidden).
- If G3_JUDGE_MODEL_RE's spelling set misses a future stamp style ("reviewer-model:"), the marker stays silent; the regex covers judge-model and subagent_model spellings only.

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_60_judge_independence_20260926.md (D2/F2); .zcode/workflows/the-gala.dwf.ts, mickey17-v2.dwf.ts, the-50.dwf.ts, tree-doctrine-dig.dwf.ts (judge seats, post-edit stamps); tools/workflow_gate.py (CHECKS G3, G6 soft pattern, new marker, run_checks); configs/workflow_gate_scenarios/*.card.json + fixtures (suite green 7 of 7); tests/test_workflow_gate.py (8 passed incl. new pin); dynamic-workflows SKILL.md facade bytes (persona/model section); groq/compound-mini provenance rows (B2_03/B2_35/B2_115/B2_132 receipts, QUEUE.md). No web sources. Em-dash count 0 in added lines and this receipt.
