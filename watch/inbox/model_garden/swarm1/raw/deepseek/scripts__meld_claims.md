# swarm1-deepseek-scripts__meld_claims (deepseek-chat @ deepseek, turn 1, channel: content)

DEFECT 1: Cache file read/written with no schema check, so a non-list JSON (dict, null) crashes `claim_sets_match` on non-iterable or silently yields zero matches. | EVIDENCE: scripts/meld_claims.py:108-115 | FIX: after load, `if not isinstance(claims, list): claims = extract_claims(body, key)` and validate each element is str.
DEFECT 2: Per-file exception only guards `extract_claims`; `json.loads` on a corrupt cache and `cfile.write_text` are outside the try, so one bad file aborts the whole sweep. | EVIDENCE: scripts/meld_claims.py:106-115 | FIX: wrap load+extract+write in one try/except that logs `WARN` and `continue`s.
DEFECT 3: Convergence denominator uses `min(len(ca), len(cb))`, so an answer with 1 claim against one with 8 scores 1.00 on a single incidental token-overlap match, inflating the headline mean. | EVIDENCE: scripts/meld_claims.py:128-131 | FIX: use `max(len(ca), len(cb))` or Jaccard over the union, and print the denominator basis.
DEAD-CODE: `urljoin` imported but never referenced; the file builds no relative URLs. | EVIDENCE: scripts/meld_claims.py:19
ONE-SITTING FIX: Move cache read, extraction, and write inside a single try/except with `continue`, validating the loaded value is a list of strings. | EVIDENCE: scripts/meld_claims.py:106-115

Falsifier for my own deliverable: if `out_dir` caches are always produced by this same script (so always `list[str]`), DEFECT 1 and the ONE-SITTING FIX are non-load-bearing; check by grepping the claims dir for hand-edited or foreign-written JSON.
