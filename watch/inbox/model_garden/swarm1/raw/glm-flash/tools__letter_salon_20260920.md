# swarm1-glm-flash-tools__letter_salon_20260920 (glm-5.3-flash @ zai, turn 1, channel: content)

DEFECT 1: DNS-resolve check in _validated_api_url is TOCTOU: urlopen re-resolves api.deepseek.com so the private-range block can be bypassed by rebinding | EVIDENCE: tools/letter_salon_20260920.py:44-49 vs 98 | FIX: pin the validated IP (connect by IP with SNI/Host header, or resolve again post-connect and verify peer IP matches the checked set).
DEFECT 2: retry loop re-sends the paid request on non-transient failures: JSONDecodeError from a 200 body hits the generic except and retries, double-billing the call | EVIDENCE: tools/letter_salon_20260920.py:107-111 | FIX: parse JSON outside the retry guard or retry only on URLError/timeout/429, return immediately on decode failure.
DEFECT 3: missing LETTER file crashes main with an uncaught traceback at letter_text after OUTDIR.mkdir, leaving an empty receipts dir and no manifest | EVIDENCE: tools/letter_salon_20260920.py:117-118, 53 | FIX: check LETTER.exists() before mkdir and exit with a one-line error if absent.
DEAD-CODE: terminal "429 x2" return is unreachable: every path through the (0, 1) loop returns inside the loop | EVIDENCE: tools/letter_salon_20260920.py:112
ONE-SITTING FIX: hoist a fail-fast preflight (LETTER exists, at least one chair rib exists, deepseek key present) before any spend, so a misconfigured run costs zero API calls | EVIDENCE: tools/letter_salon_20260920.py:116-127

Falsifier: run with watch/inbox/OPERATOR_JOURNAL_20260920.md absent; current code exits 1 with traceback and an empty OUTDIR; the patched preflight exits 1 with a message and creates nothing.
