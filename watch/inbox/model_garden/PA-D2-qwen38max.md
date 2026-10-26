# PA-D2-qwen38max (qwen/qwen3.8-max-prime @ nous, turn 1, channel: content)

## ADJUDICATION: Movement 1 Objections vs. Cheap-Arm Answers

---

### (1) EXIT SEMANTICS - L1 Objection

**Verdict: DIES as contradiction. Amends to a prose-clarity note.**

- The code at `02__workflow_gate.py` shows `main()` returns 0 (pass), 1 (OSError on file read), 2 (gate failure with failed checks).
- The docstring (line 10 of the pasted file) states: "exit 2 is the only hard block; every submission registers a row."
- The final line `sys.exit(main())` passes these return values as process exit codes.
- Zero literal `sys.exit(1)` calls exist; exit 1 arises only from the `except OSError` handler.
- Exit 1 is an I/O error path (undecidable - the gate could not evaluate), not a gate verdict.
- If logic.md describes exit 1 as "undecidable" or "soft," that is byte-consistent with the code's semantics.
- My L1 objection claimed a contradiction between logic.md and the code. No contradiction exists.
- Residual note: calling exit 1 "soft" is imprecise (it is not a soft verdict from the checks; it is a pre-check error), but this is a prose-clarity issue, not a contract violation.

**L1 is dead.**

---

### (2) REGISTRY ORDER - A4/O7 Reconciliation

**Verdict: DIES as census-violation objection.**

- The cheap arm reports row 40 at `ts: 2026-09-30T01:18:10Z` and rows 41-45 at `2026-10-01`.
- The REGISTRY.jsonl evidence confirms append-only structure: timestamps increase monotonically through the visible rows.
- Operations lane's "40 rows" was true at its read moment (on or before 2026-09-30).
- Accuracy lane's "45 rows" was true at its later read moment (on or after 2026-10-01).
- Append-only arithmetic holds: 40 then 45 is consistent; 45 then 40 would not be.
- My A4 objection stated "the order cannot be reconstructed." The cheap arm reconstructed it from row timestamps.
- The underlying hygiene concern (chapters should state their read moment) survives as a style recommendation, but the specific claim of a census violation or arithmetic impossibility is dead.

**A4 is dead as a defect. The moment-stamping recommendation lives as a minor hygiene note, not a line-pinned defect.**

---

### (3) UF-124 - Objection 1 Status

**Verdict: CONFIRMED with amendment.**

- Movement 2 could not locate the premise files; objection stayed OPEN.
- Movement 3 located them at `watch/inbox/burn_wave_20260926/` and `watch/inbox/union_fullsend_20260917/`.
- The bytes show UF-124 carries: (a) `openreview.net/forum?id=XYZ` - a literal placeholder that would NOT resolve; (b) "Constitutional AI - OpenAI" - misattributes Anthropic's paper to OpenAI.
- The proposed gate ("each id must resolve to fetched bytes") catches defect (a): the placeholder id fails resolution.
- The proposed gate does NOT catch defect (b): if the id were real, the misattribution would pass.
- My original prediction ("the gate would pass UF-124") is wrong for this specific instance: the gate catches it via the placeholder.
- My general claim ("the gate checks form not substance") survives: the misattribution defect exists in the same row and the gate's mechanism does not address it.
- Amendment: UF-124 is not a clean proof case for "gate passes a misattributed citation." It is a proof case for "substance-level defects coexist with form-level defects in the corpus, and the gate addresses only the form level."

**Objection 1 is confirmed in substance, amended in mechanism.**

Evidence that would have killed it entirely: a UF-124 variant where the id is real, resolves, and the attribution is correct - showing the gate's scope is sufficient. No such variant exists in the swept bytes.

---

### (4) LANDABLE AMENDMENT (from Movement 1)

**Chapter:** accuracy.md
**Location:** Replace the first sentence of Incident 1 "Instrument upgrade" and the "(2)" clause of the Decision ledger.

**Paste-able sentence:**

> A row carrying an external citation or a tool-behavior claim lands LANDED only when the same session's receipt quotes, from fetched bytes or captured command output, the span carrying the specific claimed value (author attribution, effect size, default behavior); an id that resolves without that span lands UNVERIFIED, and until a resolver enforcing this exists in tracked code this rule is PROPOSED, not a changed contract.

**Why this and not something else:**
- Addresses the confirmed form-vs-substance gap (adjudication 3 above).
- The "PROPOSED, not a changed contract" clause addresses defect A2 (no enforcing code exists; the Decision ledger currently states the change as landed).
- The "specific claimed value" requirement addresses the original falsifier's demand for effect-size quotation, not just id resolution.

**Falsifier for this amendment:** If a tracked resolver already exists in `tools/` or `mag/` that enforces span-level quotation (not just id resolution), then the "PROPOSED" qualifier is wrong and the sentence should drop it. Command to test: `grep -rn "resolve\|fetch.*bytes\|quote.*span" tools/ mag/ --include="*.py"`.

---

### (5) NEXT THREE DIG TICKETS

**T4 - UNTRACKED WORKFLOW COUNT**
How many `.dwf.ts` files under `.zcode/workflows/` are NOT git-tracked?
Command: `find .zcode/workflows/ -name "*.dwf.ts" -exec sh -c 'git ls-files --error-unmatch "$1" 2>/dev/null || echo "UNTRACKED: $1"' _ {} \;`
Purpose: Movement 3 confirmed the-gala.dwf.ts is untracked. This quantifies the total single-disk risk for the estate's workflow lineage.
Settles: Whether O1 (operations objection about untracked workflows) is a single-file gap or a systemic one.

**T5 - G6 SOFT-WARN SATISFACTION**
Does any `.dwf.ts` file in `.zcode/workflows/` contain a line matching `G6_STAMP_RE` (the pattern `(?i)\b(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*\d{4}-\d{2}-\d{2}`)?
Command: `grep -rn -iP '(source[-_ ]fetched|fetched|observed[-_]at)\s*:\s*\d{4}-\d{2}-\d{2}' .zcode/workflows/`
Purpose: The registry shows repeated G6 soft-warns. If zero scripts satisfy the stamp regex, the soft-warn is a permanent fixture that no one has fixed, making it a dead letter rather than a ratchet.
Settles: Whether G6's soft-warn family is functioning as a ratchet (someone eventually adds the stamp) or is a permanent unfired warning.

**T6 - FAIL-THEN-PASS PAIRING**
For every registry row with `"verdict": "FAIL"`, does a subsequent row with the same `"name"` and `"verdict": "PASS"` exist?
Command: `python3 -c "
import json, sys
rows = [json.loads(l) for l in open('memory/workflows/REGISTRY.jsonl') if l.strip()]
fails = {}
for i, r in enumerate(rows):
    if r['verdict'] == 'FAIL':
        fails.setdefault(r['name'], []).append(i)
    elif r['verdict'] == 'PASS' and r['name'] in fails:
        fails[r['name']] = [x for x in fails[r['name']] if x < i]
orphans = {k: v for k, v in fails.items() if v}
print(f'{len(orphans)} FAIL names never followed by PASS: {list(orphans.keys())}')
"`
Purpose: The gate's docstring claims "amend-not-rewrite is visible in digests." If FAIL rows exist with no subsequent PASS for the same script, either the workflow was abandoned (not amended) or the registry is incomplete.
Settles: Whether the amend-not-rewrite claim holds across the full registry history, or whether some failures were silently dropped.

---

### DELIVERABLE FALSIFIER

This adjudication is wrong if any of the following holds:

- L1 lives: `grep -n "exit\|return" tools/workflow_gate.py` shows a code path where exit 1 blocks a push (e.g., a pre-push hook that treats exit 1 as failure).
- A4 lives: Row 41's timestamp is EARLIER than row 40's, violating append-only order.
- Objection 1 dies: A tracked resolver in `tools/` or `mag/` already enforces span-level quotation, making the amendment redundant.
- The landable amendment is incoherent: pasting it into accuracy.md creates a contradiction with an existing sentence in the same chapter that I have not accounted for.
