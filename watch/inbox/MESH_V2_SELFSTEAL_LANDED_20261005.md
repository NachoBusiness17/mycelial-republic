# MESH V2 SELF-STEAL LANDED - the salon verdict is now running code (2026-10-05)

**Trigger:** operator order "do it self steal" on AGENT_MESH_TRIANGULATION_STEAL_20261005.md section 3.
**What landed:** architecture v2 as a working package + the freshness law wired into both existing MCP doors + pack v2 amendments. All tests green, ratchet PASS, live dogfood run.

## 1. The package: mag/mesh/ (schema mesh.*.v1)

| File | Lines | Owns |
|---|---|---|
| feeds.py | 145 | per-writer Ed25519 signed feeds (SSB shape), merged DERIVED room view (room is never a write surface), per-feed chain (chain proves WHAT, sig proves WHO), rate law (30 rows/min, honest refusal) |
| knot.py | 100 | merkle knots over all feed tips + blobs + refusal/decision logs; knot-before-rows and knot-at-every-commit laws; verify names unsealed leaves instead of hiding them |
| broker.py | 155 | put_blob content store (blobs are the single truth, index DERIVED), propose (never commits), adjudicate = provenance checker (source_hashes must resolve; supersedes targets must be COMMITTED, not merely referenced), refusal log with reasons, knot cut on every accept |
| door.py | 129 | MCP door: exactly search / get_by_hash / propose_write + verify_chain + tail_room; freshness header on every response; recall floor NAMED in every search; 200KB read bound (fat reads are a competence negative); gps_mcp-pattern stdlib JSON-RPC stdio loop |

Tests: tests/test_mesh_v2.py, 11 tests - every salon verdict as an executable law (two-writer merge, the sed -i forgery caught by signature, knot coverage + unsealed naming, chain tamper, provenance refusal, supersedes-at-tip, rate burst, freshness + recall floor, door round-trip incl. a real stdio subprocess session). One real bug the tests caught: _known_row originally substring-grepped raw text so a proposal's own supersedes field matched itself; now only committed things (blobs + landed effect hashes) count as targets.

## 2. The freshness law wired into the existing doors

- tools/query_broker.py: ask() responses now carry freshness {corpus_tip_hash, last_growth_ts, frozen} computed over the catalog pair. 10/10 tests still green.
- tools/gps_mcp/server.py: _ok() attaches the same header (over ledger db + receipts) to every tool response. 41/41 tests green.
- The mesh door carries it natively. Three doors now declare their corpus state; a caller can always tell live from frozen.

## 3. Live dogfood (memory/runs/mesh_v2/)

Knot cut on the EMPTY root first (the law), first signed feed row ("mesh v2 online"), the triangulation steal receipt banked as library blob #1 via a real propose -> adjudicate(accept) -> knot cycle. verify_chain: tip a6acf3b270657a56c7064a0bfa6defbdc8fa030f82ed580c85a8e128024513ed, 0 unsealed leaves; search finds the receipt; freshness unfrozen.

## 4. Pack v2 (memory/research_packs/20261005_agent_mesh_salon/PACK.md)

PART 3.5 added: revised build order (knot first, feeds, 3-tool door, provenance broker, contention test, replicate last), cut list (four channels -> room+wants; derived index; replication demoted), five cheap adds (signature column, refusal log, embedding-model-ID, LABELS.jsonl, README-per-room), three promoted laws (freshness header, rate law, witness law: N seats from M families = max M witnesses). The pack now teaches v2 and cites mag/mesh as the worked instance.

## 5. What is NOT claimed

- The mesh is local-first: writer keys live beside feeds; remote-peer key publication is out-of-band (SSB/Nostr shape) and unbuilt.
- Search is substring over the derived index (FTS5/embeddings are a later cache upgrade); the recall floor says so in every response.
- No replication fired yet (the fold says replicate when a second reader exists; the contention test is the next gate before any of that).
