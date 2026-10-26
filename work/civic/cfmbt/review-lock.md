# REVIEW LOCK — CFMBT v5 · 2026-09-22

**Spec:** CFMBT-v5-SPEC (AOS inbound, filed `watch/inbox/inbound/AOS_CFMBT_V5_SPEC_20260922.md`)
**Spec seal (sha256, first 24):** `925fd4f294381d54009fc6137`
**Build tree:** `work/civic/cfmbt/` — Lead/Build: ZCode seat (GLM-5.3-Flash)

## Implement echo (per spec §11)

```
spec: CFMBT-v5-SPEC
inputs touched: local/bind.json (absent — page ships placeholders + not-proven)
wrote: app/index.html, app/styles.css, app/app.js, data/case.json, data/sources.json,
       data/schema.json, forms/self-disclosure.md, legal/privacy-posture.md,
       conversation/beats.md, README.md, review-lock.md
stopped because: done-when lock met
unknown: none
```

## Done-when lock (spec §0) — PASS

1. **One page, three questions, ten minutes.** PASS — `app/index.html`, four
   sections in order: Decision file (Q1+Q2), Conflict check (Q3), Fund-level
   sunlight, Method statement. Render-verified in a real browser (screenshot
   receipt, 2026-09-22).
2. **Never lists natural-person beneficial owners.** PASS — no such field
   exists in `data/schema.json`; the refusal is printed in section 3 of the page.
3. **Every number and document link carries a source and a score.** PASS —
   chips on all fields; `data/sources.json` pre-scores the 11 framework
   sources (we-have-a-record · Evidence); case fields default `not-proven`.
4. **Only the 7 local tokens.** PASS — `{{COUNTY}} {{PROJECT}} {{SERIES}}
   {{YEAR}} {{DEBT_SERVICE_Y1}} {{ISSUE_SIZE}} {{PROJECT_COST}}` verified
   present; the additional `{{field.path}}` placeholders are public
   `case.json` keys (null in the public copy), not host-bound local tokens —
   reviewed and accepted on that reading.
5. **No secrets, no PII, no host folder map, no git, no public bind.** PASS —
   tree contains none; `local/bind.json` does not exist yet (operator binds it
   at run time).

## Reviewer notes

- Render check: `index.html` served, chips render, drawer present, 4 sections.
- Print CSS ships (sections page-break clean, chrome hidden).
- The lane's own two timed-out checks are Mickey-17 tombstoned for re-seed and
  are NOT part of this lock's basis.
- Human final call: `local/bind.json` and any send remain the operator's hand.

**Verdict: Review lock — PASS.**
