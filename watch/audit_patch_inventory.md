# Patch inventory + intent-vs-artifact audit — 2026-08-31

Scope: `/patches` (proposed, unapplied) and `/patches/applied`. Read-only on `/mag` (existence tests + bounded grep only).

## Totals

| Bucket | Count |
|---|---|
| Proposed, unapplied | 1 |
| Applied | 10 |
| — of which self_steal_* | 4 |

## Proposed (unapplied) patches

| Patch | Target | Target exists | Intent | Risk |
|---|---|---|---|---|
| sancho_lattice_row.json | memory/lattice/nodes.jsonl (under `/mag`, i.e. `/mag/memory/lattice/nodes.jsonl`) | yes | Append a `lattice_node.v1` seat row for "Sancho" (tier judgment, GLM-5.3 Max plan, role grounding) after the c0015_url_15 dig node. | **Medium** — see collision note. |

## Applied patches — self_steal_* (4)

| Patch | Target | Target exists | Intent | Risk |
|---|---|---|_applied already — risk is historical_ |
| self_steal_effect_broker.json | mag/effect_broker.py | yes | Unified effect execution layer: enforces authority + granted capabilities + policy validation; full receipt state machine (ENQUEUED→…→RECEIPT_COMMITTED). | applied |
| self_steal_harness.json | mag/harness.py | yes | Integration harness wiring switchboard + effect_broker + policy_engine into one control loop (leases, queues, receipts, operator confirmation). | applied |
| self_steal_policy_engine.json | mag/policy_engine.py | yes | Policy-as-data engine (memory/policy.json): 5 gates — authority, capability grant, TTL, budget, revocation — before AUTHORIZED. | applied |
| self_steal_switchboard_v2.json | mag/switchboard_v2.py | yes | BBS control plane with policy enforcement on every grant(), operator confirmation gate (DEFERRED→inbox), TTL/budget, receipt chain. | applied |

## Collision check (proposed patches vs existing files)

Target file ends with the patch's exact `search` string (search string present 1× in target, grep -c verified). But:

- **`sancho_lattice_row.json` — HARD COLLISION.** The search string embeds `\r\n` (0x0d0a); the target file has **zero CR bytes** (grep -c $'\r' → 0). An exact-string search would not match; apply would fail or no-op. Search/replace must strip the embedded `\r` (match the file's bare-LF tail) before apply.
- Applied self_steal_* patches are whole-file writes (path + content), not search/replace — no search-string collision risk by construction.

## Recommended apply order (1 proposed patch only)

1. **sancho_lattice_row.json** — single blocking dependency: **fix the `\r\n` vs LF mismatch in the `search` string** (de-CRLF it to match the target's actual line ending) before `python -m mag.openclaw_patches apply`. There is no other pending patch to order against; the 4 self_steal targets are already applied and present.

## Verification commands used (reproducible)

- `ls -la /patches /patches/applied`
- `test -f` per target; `grep -c -F 'dig:c0015_url_15' /mag/memory/lattice/nodes.jsonl` → 1
- `grep -c $'\r' /mag/memory/lattice/nodes.jsonl` → 0 (search string contains `\r\n`)
