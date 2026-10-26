# B2-492 provider-probe snapshot differ (2026-09-26)

## Verdict

LANDED. tools/provider_snapshot_differ.py reads the two newest snapshots in
memory/improve/provider_health/ (or an explicit pair) and prints one line per
lane-status transition: "FLIP <lane>: <old class> -> <new class>  (snapshots
<old day> -> <new day>)". The exact flips the cadence exists to catch are now
machine-visible, named on the tool's own docstring from the wave's bytes
(mistral 429-zero-quota to 403-wrong-default within one day; mistral 403 to
DORMANT after the B2-105 surgery, visible live in B2_106_cadence_live.json).
Falsifier proven on a fixture: two snapshots differing in exactly one lane
print exactly one FLIP line naming both classes. Real-state note: only ONE
snapshot exists on disk (memory/improve/provider_health/2026-09-26.json, the
B2-106 cadence's first run), so the differ exits 2 with "need two snapshots"
until the cadence's second run - the tool is ready one cadence day ahead of
the data.

## Evidence file:line quotes

- Snapshot shape (memory/improve/provider_health/2026-09-26.json, read this
  lane): {"day": ..., "ts": ..., "result": {"check", "ok", "statuses",
  "providers", "issues", "unverified", "degraded", "fenced"}} with 28
  statuses entries, class values like "REMOTE-UNVERIFIED" (first entry
  anthropic).
- Falsifier fixture (this lane, tmp pair written and diffed):
  {"mistral": "429-zero-quota", "groq": "ok", "deepseek": "ok"} vs
  {"mistral": "403-wrong-default", "groq": "ok", "deepseek": "ok"} ->
  exactly one line: "FLIP mistral: 429-zero-quota -> 403-wrong-default
  (snapshots 2026-09-25 -> 2026-09-26)". Identical pair -> "no lane-status
  transitions". Appearing/vanishing lanes transition to/from "(absent)".
- The motivating flips, watch/inbox/burn_wave_20260926/B2_106_cadence_live.json:9
  ("statuses" block) and the brief's own text naming mistral 429->403 and
  403->DORMANT (B2-105 surgery).
- Real invocation (this lane): rc 2, "need two snapshots under
  memory/improve/provider_health" - honest need-for-data, not a fabricated
  diff against one snapshot.

## Work done

1. Read the snapshot schema and the B2-106 cadence live output.
2. Wrote the differ (two-newest selection, explicit-pair override, statuses
   class extraction, sorted one-line-per-transition output, exit 2 on <2
   snapshots).
3. Proved the falsifier on the brief's own mistral case as a fixture (one
   flip -> exactly one line naming both classes); ran the no-flip and
   real-tree arms.
4. Filed this receipt; LEDGER row; QUEUE pointer (re-filed row after the
   20:57:55Z board truncation); INDEX registration.

## Falsifier

This tool is inverted if any of the following holds: (a) rerunning the
fixture pair yields zero or two lines for one flipped lane (the diff is
broken); (b) the differ reports "no transitions" on a pair where
B2_106_cadence_live.json records a known flip (class extraction misses the
statuses shape); (c) a snapshot whose statuses nest moved (schema change)
silently diffs as all-absent instead of erroring - then the loader needs a
schema guard, filed, not silent.

## Bibliography closed

memory/improve/provider_health/2026-09-26.json (bytes read, shape quoted);
watch/inbox/burn_wave_20260926/B2_106_cadence_live.json (statuses shape);
watch/inbox/burn_wave_20260926/B2_105_mistral_surgery_20260926.md (accepted
from the brief as the DORMANT flip's source). Fixture diff run locally; no
network calls.
