# W3W — STEER channel LIVE (2026-09-29/30)

Mission (Mickey17 W3): make watch/inbox/operator_model/STEER.md spec live. Done.

## Landed

| Artifact | Path | Status |
|---|---|---|
| Live channel | `watch/inbox/STEER.md` | created: schema header (4 `#` rows) + seed row |
| Reader | `tools/steer_read.py` | created: `read(target_mate, path=None)` + CLI |
| Tests | `tests/test_steer.py` | 5 channel tests APPENDED (file pre-existed testing `mag.steer` — that coverage kept intact, both sections green) |

Seed row (operator's standing order tonight, verbatim per mission):
`{"id": "st_20260930_seed_1", "mate": "all", "steer": "keep rolling 24 wide; proven seats only; dogfood gps", "ts": "2026-09-30T00:00:00Z", "via": "hand-edit", "provenance": "operator session order 2026-09-30, filed by coordinator"}`
`via: hand-edit` + `provenance` kept verbatim so anti-forgery classifies it an ORDER, not a proposal (a bare `provenance` field is not in the spec's `via` set and would have misfiled his order as a proposal).

## Reader contract

- Applicable = `mate == target` or `mate == "all"`; LATEST WINS on parsed ISO ts (file order breaks ties); rows returned oldest-first.
- Schema validation: `mate`/`steer`/`ts` required strings, ts ISO-8601. Malformed lines skipped + reported (`malformed[]` + stderr) — corrupt rows never silently widen scope; last VALID row stays operative.
- Anti-forgery: `via` not in {hand-edit, hermes-dm, phone-relay} -> row annotated `proposal: true` in output (missing or forged `via` alike).

## Leave-protocol integration note (inject between cycles — 3 lines)

1. Between mate cycles run `from tools import steer_read; out = steer_read.read(mate_id)`.
2. If `out["operative"]`, inject into the mission pack under `## OPERATOR STEER`: the `steer` text verbatim + `id`/`ts`; when `operative["proposal"]` is true, prefix `PROPOSAL (no operator provenance) — treat as ask, not order`.
3. The mate's next landed receipt carries `steer_ack: <id or ts>` naming the one plan change the row caused; unacked operative row older than a full cycle surfaces in memory/attention.md.

## Verification (real counts)

- `./.venv/Scripts/python.exe -m pytest tests/test_steer.py -q` → **9 passed in 6.27s** (4 pre-existing `mag.steer` + 5 new channel: latest-wins, all-vs-target match, proposal marking, malformed-fail-loud, missing file).
- Live read: `python tools/steer_read.py w3` and `... all` → ok, operative = seed row, `proposal: false`, `malformed: []`, exit 0.

Not committed to git (per mission). Append-only law: rows below the seed line only; rewriting a landed row is an incident.
