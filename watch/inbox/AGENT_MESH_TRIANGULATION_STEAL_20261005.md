# AGENT MESH TRIANGULATION STEAL - the wide salon verdict (2026-10-05)

**Trigger:** operator order "run that workflow go wide and hard across our free surfaces and deep seek to do a triangulation steal how could we best do this knowing what we do."
**Run:** watch/salon_runner.py fire over memory/research_packs/20261005_agent_mesh_salon/PACK.md; 6/7 shapes gated (S5 rejected all lanes: gemini 404, anthropic 401, hermes thin); engines: deepseek x3, cohere/free, zai, hermes/ling; fold zai-campaign 66.9s. Artifact: memory/runs/salons/agent_mesh_triangulation/SALON_ARTIFACT.md (brief sha f7fb84e4a38dbe33).
**Monoculture caveat (the fold's own law applied to itself):** deepseek carried 3 of 6 seats, so S1/S2/S3 agreement counts as ONE family witness; cohere, zai, and ling provide the cross-family legs. Verdicts below note which legs carry them.

## 1. THE TRIANGULATED ANSWER (how we best build it, knowing what we know)

**Architecture v2 - three files are the whole system** (S3 fold line, cross-family held):
1. **Per-writer signed feeds, not one shared room file**: `feeds/{agent_id}.jsonl`, Ed25519-signed rows, merged at knot time. This is the SSB fix; CRDTs are NOT needed for the room (CRDTs are merge policy for shared documents, not ordered event logs; the room wants NO writer to win, not last-writer-wins). CRDTs enter only if concurrent same-source index enrichment shows up (UNPROVEN, no instance yet).
2. **The knot is the load-bearing step and goes FIRST**: "without the knot, append-only is a belief, not a property." Build it on the empty room to prove the chain script before rows arrive. Knots at every broker commit plus a timer, not just nightly.
3. **The MCP door with exactly three tools**: `search`, `get_by_hash`, `propose_write` (~150 lines), plus `verify_chain` from day one. Everything else in the pack is derived or premature.

**JSONL's four exact break points** (S2 enumeration, S1/S3 converged): same-key concurrent update (policy gap); partial reads during append (framing gap, PIPE_BUF); compaction (nobody owns it); dual-log consistency (two append-only logs = two truths; make the index DERIVED from blobs, FTS5 a rebuilt cache, never a second truth).

**Trust model, smallest honest**: read open, write signed, effect brokered. Three gates, no PKI, no CA; revocation = a signed row on your own feed (Nostr shape). The broker is a PROVENANCE CHECKER, not a bouncer: reject proposals whose source_hashes do not resolve in the current chain tip or whose supersedes target is not at tip.

**MCP verdict (Q3)**: changes REACH and GATE-ABILITY, not competence. The honest line: it changes the failure mode from "hallucinated shell command" to "well-formed call to the wrong tool", which is gateable. S4's "30% hallucination reduction" was DISPUTED by the fold as unsourced - caught live. Bound read-tool response size: a read that returns 10MB of context is a competence negative. NOTE: the controlled measurement everyone says does not exist IS RUNNING in this estate right now (the k8s fault suite, K8S_FAULT_SUITE_FIRED_20261005.md) - its fold answers Q3 with numbers.

**Archival law (Q4)**: every artifact readable with nothing newer than a text editor and a hash function. Bytes + sha256 + plain FTS5 survive; everything above is a rebuildable cache. New cheap devices to adopt: freshness header on every MCP response `{corpus_tip_hash, last_growth_ts, frozen}` (the cheapest anti-fabulation device proposed - it makes frozen-corpus reasoning VISIBLE); embedding-model-ID inside index rows; restore drill yearly (replication without a tested restore is fake); refusal log (the broker records what it refused - the negative space is mineable).

**Free-mine law (Q5)**: false consensus is the most dangerous output (correlated errors look like consensus). N seats from M families = at most M witnesses; count only cross-family agreement, tag intra-family agreement CORRELATED at 0.5 witness; one non-LLM witness per fold (grep, SQL, human). LOW_DIVERSITY folds read back with that tag and count as hypotheses, not findings.

**Ladder v2 (revised order)**: mkdir -> knot (on empty room) -> per-writer feeds -> MCP read door + verify_chain -> propose_write + broker (provenance-checking, refusal-logging) -> contention test (two writers, same key, 30s) -> replicate (git only; Syncthing/IPFS/torrent later when a second reader exists) -> mine.
Cut from v1: four channels to two for newcomers (room + wants; channels re-derive from usage); the separate index.jsonl (make it derived); replication as a distinct early step.

**Five cheap adds for the pack's v2** (S3 list, fold-endorsed): signature column, refusal log, embedding-model-ID column, LABELS.jsonl (human tags on every blob/feed/knot/fold), README-per-room (dated prose saying WHY - the single artifact most likely to keep the corpus minable for a decade).

## 2. THE STEAL-IN-REVERSE (what the salon validated about the estate)

- queue/lanes/*/trail.jsonl ARE per-writer feeds already: the estate accidentally built the SSB shape (per-lane logs) while worrying about the shared room.jsonl monolith. The salon's Q1 verdict validates the lane-trail design; the fix for watch/room.jsonl is to treat it as the MERGED VIEW (knot material), not the write surface.
- The effect-broker law (model proposes, switchboard authorizes) was independently re-derived by every seat as non-negotiable - third external convergence on our own law.
- The recall-floor/freshness law (map_asof census, frozen-corpus doctrine) got its wire format: the freshness header. S3 derived it blind from our pack; we had the law but not the response header. STEAL: add {corpus_tip_hash, last_growth_ts, frozen} to query_broker and gps_mcp responses.

## 3. WHAT TO DO WITH IT (operator gate)

1. Adopt architecture v2 for the new comms layer: per-writer feeds + knot-first + 3-tool MCP door. (The one next build sentence, cross-family held.)
2. Wire the freshness header into existing MCP surfaces (query_broker, gps_mcp) - one line class of change.
3. Feed the fault-suite fold to the Q3 question when the grid lands - it is the first controlled measurement in the field.
4. Pack v2 edits: the five cheap adds + ladder reorder + cut list, then the pack is teachable with the salon's own receipts as the worked example (file this artifact into the pack directory).
