# GATE DEFECT — the secret gate does not block keys written as assignments

**Found:** 2026-09-27, by L2-Hermes while writing the missing gate tests
**Severity:** HIGH — the gate misses the dominant real-world credential form
**Component:** `tools/secret_gate.py` + `tools/secret_gate_scan.py` + `tools/secret_gate_rules.py`
**Status:** REPORTED, NOT FIXED (audit posture: report only)

---

## The defect

`COMBINED` is a single regex that ORs all 28 rule patterns into one alternation.
`COMBINED.finditer(line)` is therefore **non-overlapping** and consumes text as it
goes. `GENERIC-KEYASSIGN` (rule 28) and `ENV-ASSIGN` (rule 29) are the LAST two
alternatives, and both match a whole `NAME=value` line *including the value*.

So when a real provider token is written the way keys are actually written:

```
XAI_API_KEY=xai-Kp2mR9vT4xQ8nB1yH6jL3pW0eZ5dS2aC8uF1gI4oK9mN6pQ3rT7vY2w
```

`finditer` yields ONE match, span `(0, 72)`, attributed by `m.lastindex == 28`
to `GENERIC-KEYASSIGN` (medium) — or `ENV-ASSIGN` (low) when the name is not one
of the generic-assign keywords. The alternation **never reaches** the `XAI-KEY`
alternative, because that text was already consumed. The provider rule is never
evaluated at all.

`tools/secret_gate_scan.py:199-206` is where the attribution happens:

```python
for m in COMBINED.finditer(line):
    idx = m.lastindex
    kind = "ENT" if idx > len(RULE_NAMES) else RULE_NAMES[idx - 1]
```

`lastindex` is correct for the group that matched. The problem is upstream:
a greedy, earlier-positioned alternative swallowed the span.

## Measured proof (all three forms, real gate, real invocation)

| line | expected | actual | blocks? |
|---|---|---|---|
| `sk-ant-api03-…` bare, no assignment | ANTHROPIC-KEY high | `high=1` | **yes** |
| `api_key = sk-ant-api03-…` | ANTHROPIC-KEY high | `medium=1` | **no** |
| `XAI_API_KEY=xai-…` (real .env shape) | XAI-KEY high | `low=1` | **no** |
| `ANTHROPIC_API_KEY=sk-ant-…` | ANTHROPIC-KEY high | `low=1` | **no** |
| `MY_SECRET=xai-…` | XAI-KEY high | `low=1` | **no** |

The gate blocks a **bare** token and misses an **assigned** one. The bare form is
rarer in real files than the assigned form.

## Why this matters more than the finding it caused

The xAI key confirmed in `attic/20260923_biography_rotation/biography_backup_20260825.tar`
and in `memory/trajectory/steps.jsonl:1994` was captured from **command output** —
a `cat .env` / env-dump shape, which is assignment form. That is precisely the
shape this defect misses.

The gate reported `blocking=0` on the `--changed` run that cleared the push path
today. That clean result should be re-read as "did not look at the dominant
form," not "clean."

## The fix direction (NOT applied — operator's call)

Do not reorder the alternation. A correct fix must make attribution
**order-independent and overlap-aware**, because any single-pass alternation
will reproduce this class of bug for the next rule appended last:

1. Prefer per-rule evaluation over one combined regex for the BLOCKABLE set:
   for each blocking rule, `re.search(pat, line)` independently; take the
   **highest** severity hit, tie-broken to the most specific provider rule.
   Cost: 26 regex passes per line instead of 1. The entropy/SNIFF prefilter
   (`FAST_PASS_RE`) keeps that affordable, and `SG_NO_PREFILTER=1` already
   exists for A/B timing.
2. Keep `COMBINED` only for the non-blocking report tier, where over-matching
   is harmless.
3. Add a regression test with a `.env`-shaped line per blockable provider —
   the current test fixture in `tests/test_gate_blocking_paths.py` uses a BARE
   token, which is why it did not catch this.

## Files

- `tools/secret_gate_rules.py:87-95` — `COMBINED` construction, rule order
- `tools/secret_gate_scan.py:199-206` — `finditer` + `lastindex` attribution
- `tools/secret_gate_scan.py:320-345` — same pattern in `history_scan`
- `watch/inbox/secret_gate_results/full_*.json` — the evidence rows

## Receipt

Discovered while completing the 2026-09-27 gate blocking-path test work. The
positive-control test in `tests/test_gate_blocking_paths.py` failed against this
rather than being weakened to pass — the fixture was corrected to a verified
real-world shape, and the gate's behaviour is the finding. No gate source was
modified. HEAD unchanged.
