# DIRAC_GAPS_READ.md — six open loops read into next-window actions (2026-09-27)

Lane: read+verdict only. Fresh bytes: `python -m mag.dirac_loop scan` at 2026-09-27T22:17Z → beta1=8, 6 loops, closed_solved=0, open_gaps=6. `rank --scope knowledge` → beta1=0 (knowledge graph still a tree, 2566v/816e/1750c). Matches the a3efe226d census (33v/21e/20c, beta1=8).

## How the graph makes an edge (and why loops are structurally "open")

`operational_graph()` in `mag/organ_map.py` (L650-672) is the ONLY edge source for the operational scope: a hand-written `transitions` tuple, emitted iff both endpoint organ ids sit in `REGISTRY`. Each edge carries `"verified": False, "evidence_required": "receipt:a->b"`. Nothing runtime-detected; no new edge appears from code landings unless a tuple row (or REGISTRY row) is added.

Closing mechanics (read from `mag/dirac_loop.py` L185-202): `scan()` marks a loop closed iff its invariant — sha256 of `"dirac_loop:" + sorted-unique member labels joined by "|"` — appears in `_known_invariants(scope)`, which hashes labels of nodes whose `kind` is `knot`/`case_law`/`doctrine`. Operational-scope nodes are all `kind: "organ"`, so on the default scope `known` is ALWAYS empty: **the scan can never report "closed" today regardless of landings.** A loop flips only if (a) a same-scope knot/case_law/doctrine row is banked whose label equals the loop's sorted-joined label string (then `scan --scope all` sees it), or (b) a small build teaches `dirac_loop` to honor the declared edges' `evidence_required` transition receipts. Every verdict below is against that law. Adding an edge never closes a loop — each non-tree edge IS a loop's generator.

## Per-loop readings

**Loop 1 — context_pack -> swarm_surface (`pressure_offload`), invariant d678489d…** The detour (pack→admission→dirac→self_audit→worker→surface) says: today, when the context pack is under pressure, its overflow reaches the swarm only by being audited and downstream-queued — there is no direct offload. The direct contract is `mag/context_pack.py` calling `mag/swarm_surface.route_novel` when admission pressure trips. Grep: zero `swarm_surface`/`route_novel` references in `mag/context_pack.py`. The declared edge exists; the call and its receipt do not. **NEEDS-BUILD** (pressure-offload call + `receipt:context_pack->swarm_surface`).

**Loop 2 — context_checkpoint -> context_pack (`restore`), invariant 7d51fda7…** The detour (checkpoint→worker→self_audit→dirac→admission→pack) says: restored state re-enters a fresh pack only via the worker/audit round trip. The direct contract is checkpoint restore feeding `build_context_pack`. Evidence: `mag/context_checkpoint.py` has `restore_pointer` (L183, L452) and `mag/agent_cli.py` wires checkpoints, but `mag/context_pack.py` has zero `checkpoint` references — restore and pack never meet directly. **NEEDS-BUILD** (restore-into-pack receipt).

**Loop 3 — verkle_knot -> manifest (`commit`), invariant 4ea628f1…** The detour (verkle→pack→admission→dirac→manifest) says: the chain reaches the manifest only through the map/observe path. But this contract is REAL in live code: `mag/manifest.py` `anchor()` commits the manifest hash via `verkle_knot.append_verkle_knot` (L116-141) and `verify()` is chain-verified (L144-160). Tonight's landing (commit 7b8617d78, suite burn-down): the 11:20Z broken chain repaired under lock, post-append self-heal guard in verkle_knot, standing `tools/chain_repair.py` verb. The edge is already declared in the transitions tuple — **no organ_map row needed.** Only the banking act remains: walk the holonomy once (anchor + verify = committed) and bank the loop invariant as a knot row (or land the receipt-honoring build). **CLOSABLE-NOW.**

**Loops 4 + 5 — context_admission <-> openclaw (`runtime_policy` / `runtime_receipt`), shared invariant 1992f396…** Mirror pair; `loop_invariant` is order-independent, so BOTH carry the identical hash — one artifact closes two loops. The detour (admission→dirac→self_audit→worker→effect_broker→switchboard→openclaw, and back) is actually the estate's real authority chain: admission never touches the runtime directly; policy flows only through switchboard authorization and broker execution. The gap is the handshake: nothing writes admission-derived policy into the OpenClaw runtime config (`~/.openclaw/openclaw.json`, `deploy/openclaw/openclaw.container.json`) and nothing writes a runtime receipt back. Grep: zero `openclaw` references in `mag/context_admission.py` and `mag/switchboard.py`. **NEEDS-BUILD** (policy handshake + `receipt:openclaw->context_admission`); note the direct edges short-circuiting the authority chain may be the WRONG closure — closing via receipt-of-the-chain (bank the holonomy) respects the "only the switchboard/broker authorizes effects" law.

**Loop 6 — water_computer -> manifest (`proof`), invariant d7d32581…** The detour (water→pack→admission→dirac→manifest) says the water computer's proof reaches the chain only as map noise. The water family landed tonight (`mag/water_graph.py`, commit f1bceeb3a — "water is a wire now", family 14/14), but grep shows zero `manifest`/`verkle` references in `mag/water_computer.py` and `mag/water_swarm.py`: the declared `proof` edge has no call behind it. The anchor mechanism it needs already exists (shared with loop 3: `manifest.anchor()`), so this is a one-wire build + receipt, not a new organ. **NEEDS-BUILD (thin).**

## Verdict table

| Loop | Edge | Verdict | Closing action |
|---|---|---|---|
| 3 | verkle_knot->manifest (commit) | CLOSABLE-NOW | anchor+verify receipt; bank invariant as knot row; no organ_map row needed |
| 1 | context_pack->swarm_surface (pressure_offload) | NEEDS-BUILD | offload call + transition receipt |
| 2 | context_checkpoint->context_pack (restore) | NEEDS-BUILD | restore-into-pack receipt |
| 4+5 | context_admission<->openclaw (one invariant) | NEEDS-BUILD | policy handshake; or bank-the-chain holonomy (authority-law-safe) |
| 6 | water_computer->manifest (proof) | NEEDS-BUILD (thin) | water proof -> manifest.anchor() wire + receipt |

Queued: `queue/todo.md` "## Dirac open loops" (2026-09-27).
