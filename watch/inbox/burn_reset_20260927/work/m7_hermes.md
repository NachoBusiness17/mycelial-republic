# WORK m7

lane: hermes (headless one-shot)
ts: 2026-10-07T19:23:25.200830+00:00
ask: Quantify the ALLOW_RE × ENT counter-leak blast radius in the secret gate scanner. Read tools/secret_gate_scan.py lines 270-276 and the ALLOW_RE definition, then scan a sample of 5-10 real repos (the operator's desktop corpus under C:/Users/foste/Documents/projects/local_sovereign_agent/ plus any accessible open-source repos) to count: (a) tokens matching ALLOW_RE that also exceed ENTROPY_MIN, (b) 

---

All data collected. Here is the blast-radius report.

---

(1) FINDING

Lines 270-276 of tools/secret_gate_scan.py implement a counter-leak:

```
270| if kind == "ENT":
271|     if len(tok) >= ENT_LEN_MIN:
272|         h = shannon(tok)
273|         if h >= ENTROPY_MIN:
274|             ent_counts["total"] += 1      # counted
275|             if ALLOW_RE.search(tok):       # then suppressed
276|                 continue                   # never stored
```

The ALLOW_RE pattern (secret_gate_rules.py:70-76) matches 15 clause types:
your_api_key / your_token / angle_bracket <...> / dollar_brace ${...} /
x_repeat / dot_repeat / star_repeat / REDACTED / MASKED / PLACEHOLDER /
EXAMPLE* / DUMMY / FAKE / abcd1234 / 1234567890 / 0123456789abcdef

Tokens matching ALLOW_RE AND entropy >= 4.3 AND length >= 25 increment ent_counts["total"] but are never added to findings. The total is inflated relative to the stored count.

(2) STEALABLE IDEA

Move the ALLOW_RE check BEFORE the ent_counts["total"] increment on line 274. Check ALLOW_RE first, count only non-allowlisted tokens in the total, then only store if entropy passes. This makes the counter truthful instead of counting then discarding. The fix is a 3-line reorder, no new imports.

(3) TESTABLE HYPOTHESIS

If ALLOW_RE is moved before the counter increment, the reported entropy_total across any repo scan drops by exactly the ALLOW_RE x ENT count, and stored findings stay unchanged (those tokens were never stored). Prediction: after the fix, entropy_total = entropy_total - ALLOW_RE_x_ENT for every repo.

(4) EVIDENCE

Live probe of 10 repos, 1803 files, via tools/blast_radius_probe.py:

Repo | ALLOW hits | high-entropy leaks
---|---|---
local_sovereign_agent | 9111 | 2949
ai-job-search | 327 | 122
azerothcore-wow | 2820 | 505
field-strike-the-chord | 268 | 54
mag-sovereign-kit | 305 | 77
mycelial-republic | 18 | 5
audit_prep | 1 | 0
env-secrets-checker | 0 | 0
embassy-aos | 0 | 0

TOTAL: 12850 ALLOW hits, 3712 high-entropy leaks = 28.9% blast radius

By clause (high-entropy only): other=3598, angle_bracket=112, EXAMPLE=2

6 of 10 repos affected (60%)

Fleet scan history: memory/runs/ contains 20260727T203059Z-gate-test-8b22ae and 20260727T214717Z-seat-gate-verify-5be332 — both are compose feature-gate runs, not secret_gate scans. No prior secret_gate scan results exist to compare inflated counts against. OWED: whether any repos in the fleet scan history have inflated totals — no secret_gate scan history found to verify.

Sources: tools/secret_gate_scan.py:270-276, tools/secret_gate_rules.py:70-76, tools/blast_radius_probe.py output (live), memory/runs/ directory listing.
