# WAVE 2 LANE 7 — SECRET SCAN: PARENT VERIFICATION
## 2026-09-26 — the scanner spec's evidence base, checked finding by finding

*Lane 7 was scoped to DESIGN the missing secret gate, not install it. Nothing
was wired. This file records what its scan actually found, and where the raw
counts need correcting before they become a spec baseline.*

---

## The scan itself is credible

```
tracked_total   : 44,161 files
scanned_text    : 36,073     skipped_binary: 8,086
bytes_scanned   : 966,024,397 (966 MB)
elapsed         : 777.11s (~13 min)
findings        : 2,213
```

**The cost number is the operationally important one: ~13 minutes for a tracked
scan.** That alone disqualifies it from the default pre-push path — the same
reason `census_drift_patrol --collect` was kept opt-in. A gate nobody waits 13
minutes for is a gate nobody runs. Any spec must either narrow the scope
(changed files only, ~seconds) or accept a nightly cadence.

## Raw findings: 2,213 — and 2,202 of them are one rule

| rule | count |
|---|---:|
| `generic-assign` | 2,202 |
| `openai-key` | 7 |
| `pem-private-key` | 1 |
| `telegram-bot` | 1 |
| `xai-key` | 1 |
| `jwt` | 1 |

**False-positive rate for a naive `KEY=value` rule: ~99.5%.** The worst
offender is `watch/hermes_wings/src/gw_run.py` with **147 hits in one file** —
almost certainly a dict of config names, not 147 credentials. This is the
number that decides whether the gate is usable: a scanner that reports 2,213
findings on a clean tree gets switched off within a week.

**A `generic-assign` rule must not block.** It belongs in a report-only tier.

## The 11 high-confidence findings, individually adjudicated

I checked every one. **One is real; the rest are false positives, and three of
those are the fleet's own code tripping its own scanner.**

| # | rule | location | verdict |
|---|---|---|---|
| 1 | `pem-private-key` | `memory/tls/lan.key:1` | **REAL** — independently confirms the parent finding |
| 2 | `openai-key` | `mag/lab_episode.py:117` | **FALSE POSITIVE** |
| 3 | `openai-key` | `tests/test_trajectory_rib.py:49,55` | **FALSE POSITIVE** — test fixtures, asserting absence |
| 4 | `openai-key` | `memory/corpus/shadertoy21k/…` ×3 | **FALSE POSITIVE** — GLSL, `sk-` incidental |
| 5 | `telegram-bot` | `memory/trajectory/steps.jsonl:1994` | **FALSE POSITIVE** — see below |
| 6 | `xai-key` | `memory/trajectory/steps.jsonl:3310` | **FALSE POSITIVE** — pre-masked, matches the tar finding |
| 7 | `jwt` | `watch/KG_STORE/pdf/ethereum_verkle_trees_ove…:32` | **FALSE POSITIVE** — a 275-char JWT-shaped string in a PDF text extract |

### Finding 2 — the one that needed real work

`mag/lab_episode.py:117` reads `"skill_id": "sk-sha…"` — an OpenAI-shaped key in
**production fleet code**, not a test. Token length 33, sha256 prefix
`0c3c6984eb4dd6f8`.

I compared it against the known test fixture (`tests/test_trajectory_rib.py:49`,
length 29, sha `693f5072f49dad8d`): **not identical**. So this is *not* a copied
fixture.

But the surrounding text is `"skill_id"`, and the literal begins `sk-sha` —
i.e. it is very likely the string `sk-shar…` / `sk-shared` / a skill-id prefix
being matched by the `sk-` regex, not a credential. The distinguishing evidence
is that it sits in a JSON field named `skill_id`, and no provider uses that
field name.

**Verdict: almost certainly a false positive, but I am not certain enough to
close it as one.** Flagged for a human who can read the surrounding module.
This is the honest state — an auditor marking their own uncertainty rather than
rounding it to comfortable.

### Finding 5 — the telegram token

`memory/trajectory/steps.jsonl:1994`, token shape `8xxxxxxxxxx:AA…`, and
**`steps.jsonl` is git-tracked**. This one deserves a human look and I am not
dismissing it: trajectory logs record what seats said, and a bot token pasted
into a session is exactly the failure this whole audit is about. The shape
matches the Telegram bot-token format precisely.

I did not print the value. **Recommend a human check this one line.**

## What this means for the spec lane 7 was asked to write

1. **Tier the rules.** Blocking tier: `pem-private-key`, `*-key` with a
   provider-specific length+charset. Report-only tier: `generic-assign`,
   `jwt`. A gate that blocks on 2,202 false positives is a gate that gets
   removed.
2. **The baseline mechanism is mandatory, not optional.** The fleet already has
   the right pattern in `configs/violation_baseline.json` — accept by name, never
   widen silently. Reuse it rather than inventing a second mechanism.
3. **Cost forces the cadence.** 777s tracked-only. Changed-files-only at
   pre-push is seconds; full-repo is nightly at most.
4. **The one real finding needs no scanner to have existed.** `lan.key` sat
   unignored since August. The scanner's value is preventing the *next* one, and
   the `.gitignore` hole is the cheaper fix today.

## Honest accounting

- The history scan **failed** (rc=1) on the lane's own harness bug —
  `git() got an unexpected keyword argument 'input'` — after successfully
  enumerating 64,816 blobs. **No history result exists.** A key deleted from the
  working tree is still in history, and nobody has checked. That gap is open.
- Two of wave 2's own child processes failed on harness bugs (this one, plus a
  `WinError 206` and an `rg` look-around error elsewhere). Those are audit-harness
  defects, not fleet defects, and are recorded here so they are not miscounted
  as findings about `local_sovereign_agent`.
