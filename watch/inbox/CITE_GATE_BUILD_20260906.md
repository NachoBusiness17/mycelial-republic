# CITE-GATE BUILD — the vision pipeline's missing organ, landed (2026-09-06)

**Worker:** citegate (concurrency probe group 2, width 8, operator GO). **$0** — local
files only, no network, no daemons. **Organ:** `mag/cite_gate.py`.

## Design

CLI: `python -m mag.cite_gate check <card.md> [--json] [--strict]`.

Deterministic extraction of a card's citations, in order (later scans masked so no
double-count): (1) http(s) URLs, (2) repo-anchored evidence pointers — known top-level
dir (`state|watch|memory|mag|corpus|docs|configs|queue|handoff|docker|salon|example|
tests|tools|.agents|.claude|.zcode`) + >=1 segment, trailing slash = directory pointer,
(3) `--strict` only: bare filenames with no anchor → class NONE (audit mode; in default
mode a bare name in prose is a mention, not a load-bearing citation — this call is what
lets a genuinely fully-cited card reach 1.0).

Classification (tri-state stamped per citation):
- **LOCAL-VERIFIED** — path exists under ROOT and is non-empty (empty file/dir = missing)
- **LOCAL-MISSING** — path given, absent on host → claim demoted to Unproven
- **URL-UNVERIFIED** — http(s) citation; no network in this build → deterministic UNPROVEN
- **NONE** — citation-shaped token with no resolvable anchor (strict mode)

Per-card verdict: `cite_rate = LOCAL-VERIFIED / total_citations`, `complete` flag at 1.0.
State row (latest + capped 50-row history, `worker`, `ts`, `card`, `card_sha256`,
counts, per-citation detail) → `state/cite_gate_latest.json`. The URL fetch door is a
clearly-marked stub, `cite_gate.fetch_url()`, raising NotImplementedError.

## Rotation test (falsifier leg — PASSES)

| leg | card | citations | result | expected |
|---|---|---|---|---|
| A fully-cited | `watch/CAS_FIX_RECEIPT_20260904.md` | 7 paths | **cite_rate 1.0**, 7/7 LOCAL-VERIFIED, complete=True | 1.0 PASS |
| B link-only | `watch/INTAKE_GLORIOUS_LINE_20260903.md` | 5 URLs | **cite_rate 0.0**, 5/5 URL-UNVERIFIED (all UNPROVEN) | 0.0 PASS |
| C broken-path | TEMP copy `state/tmp_citegate_rotationC_20260906.md` (canonical vision-pipeline card + appended `watch/CITE_GATE_MISSING_EVIDENCE_PROBE_20260906.md`; original untouched) | 5 | **cite_rate 0.8**, probe row = LOCAL-MISSING, complete=False | LOCAL-MISSING PASS |

Outcomes rotate 1.0 → 0.0 → 0.8 as required; originals never edited (their sha256 rows
sit in the state history). Full receipt rows: `state/cite_gate_latest.json` (history).

## Integration row (before RIGHTSIZE)

```
INTERPRET → CITE-GATE → RIGHTSIZE
   check card → any LOCAL-MISSING / URL-UNVERIFIED / NONE citation DEMOTES its
   claim to Unproven BEFORE bands are sized; complete=True (cite_rate 1.0) is the
   gate BUILD-band output must clear (cite-rate 100% falsifier). Code-owned, $0.
```

## What the fetch door needs when approved

`fetch_url(url)` (stubbed, raises NotImplementedError today) needs: operator GO for
network egress; GET + body cache under `state/cite_gate_cache/`; claim-match extract
(arXiv id / DOI / repo+sha / release page); reclassify URL-UNVERIFIED → URL-VERIFIED
with a content sha256 receipt; then cite-rate becomes a true primary-source gate and
card B-style links stop auto-dragging the rate. CAGE-side per MCP topology law
(senses live in the cage), not host.

## Known limits (named, not hidden)

- Line-wrapped citations resolve to their line-local prefix (e.g. the Fomenko PDF path
  wraps in the canonical card, so the gate verifies `corpus/training_materials/` as a
  directory, not the cage-only PDF file itself — the PDF is absent on host by design;
  corpus is CAGE-ONLY).
- Trailing punctuation is stripped deterministically; Windows normpath quirks (trailing
  dots) are neutralized by the same strip, so verdicts are cross-platform stable.
- Bare-filename prose mentions are deliberately NOT citations in default mode (`--strict`
  audits them as NONE).

Card: watch/SELF_STEAL_VISION_PIPELINE_20260905.md · Build order item 1 of 3
(rotation harness = item 2, trigger unification = item 3).
