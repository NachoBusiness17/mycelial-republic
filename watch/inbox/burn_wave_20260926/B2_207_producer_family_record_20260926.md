# B2-207 Constitutional filter producer record

## Verdict

LANDED. producer_model is now threaded end to end: CritiqueResult carries producer_model and same_family_refused (fields + to_dict), filter_response accepts producer_model and on a critic/producer family match refuses the same-family critique, falling back to local heuristics with the marker set, and the ghost.py call site passes the actual producer variable (was: hardcoded critic model="deepseek" with the producer a variable and no producer record anywhere). Live probe: producer deepseek-chat vs critic deepseek returns same_family_refused=True, model_used=local_heuristics, and still catches the rank-language violation via local heuristics; family keys (qwen2.5-coder:7b -> qwen2, gemma:2b -> gemma) differ from deepseek so normal routing is unchanged. Suites: 49 passed across the constitution/critique/ghost selections. Falsifier D3 F3 (30 days of producer logs with zero same-family events closes it) is now COMPUTABLE: every critique record names producer_model and the refusal flag.

## Evidence file:line quotes

- mag/ghost.py:1970 (pre-fix): `cr = filter_response(output, tier="T2", model="deepseek")` inside the dashboard-talk route whose producer is the variable `model = body.get("model", "qwen2.5-coder:7b")` (:1926); critique_info recorded only model_used.
- mag/constitutional_critique.py:56-73 CritiqueResult (post-fix): new fields `producer_model: str = ""` and `same_family_refused: bool = False` with the B2-207 cause comment naming D3 F3 and the 30-day falsifier; to_dict adds "producer_model" and "same_family_refused".
- mag/constitutional_critique.py filter_response (post-fix): docstring "on a critic/producer family match the same-family critique is refused and the call falls back to local heuristics with same_family_refused=True (judge-independence D3 F3: a model must not audit its own family's output)"; _model_family key = first alphanumeric segment of the lowercased id, deliberately over-refusing mixed families.
- mag/ghost.py call site (post-fix): `filter_response(output, tier="T2", model="deepseek", producer_model=model)` and critique_info carries producer_model + same_family_refused.
- Live probe (this lane): same-family arm same_family_refused=True / model_used local_heuristics / violations 1 (rank language caught by local heuristics); family census printed qwen2, deepseek, gemma; to_dict round-trip verified.

## Work done

1. Read the three pointer sites (ghost.py:1970 route, ghost.py:1125 producer variable, constitutional_critique.py CritiqueResult) and the full critique flow.
2. Threaded producer_model + same_family_refused through CritiqueResult (fields, to_dict) and filter_response (kwarg, family-refusal branch to the dry-run local-heuristics path).
3. Wired the ghost.py producer variable into the call and its audit record.
4. Ran the live probe (same-family refusal + family census + to_dict round-trip) and the constitution/critique/ghost test selections: 49 passed, 0 failed.
5. Filed this receipt, LEDGER row, QUEUE row.

## Falsifier

D3 F3 (B2_60_judge_independence_20260926.md): "30 days of producer logs with zero same-family events closes it." Now computable: every CritiqueResult.to_dict() and the ghost critique_info carry producer_model and same_family_refused, so a 30-day census (count of same_family_refused==True per producer family) decides it. The landing does NOT pre-close the falsifier: zero events have been observed for zero days at filing time; the concern closes only when the 30-day census runs clean. Inversion: any critique of a same-family output without the refusal marker (e.g., producer deepseek-chat through the deepseek critic landing same_family_refused=False) inverts this receipt.

## Bibliography closed

- mag/ghost.py (call site + producer variable, wired)
- mag/constitutional_critique.py (CritiqueResult, filter_response, _model_family, added)
- mag/constitutional_critique.py _local_heuristics (the fallback path, exercised live)
- watch/inbox/burn_wave_20260926/B2_60_judge_independence_20260926.md (D3 F3 falsifier owner, named in the brief)
- Test selections -k "constitution or critique or ghost": 49 passed
- Owed: the 30-day census itself (dated from this landing's first logged producer record).
