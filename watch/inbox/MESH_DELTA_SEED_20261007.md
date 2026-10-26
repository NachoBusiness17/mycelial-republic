# THE MESH DELTA SEED: memory as a standing wave, torrent-semantics

- Operator orders fused 2026-10-07: "mirror our shit across everything so
  they can work on the same copy in tandem with local versions, dogfooding
  our network, mcp serving/torrenting the added/removed items in memory";
  "a smarter way to switchboard this across all our machines so we're not
  bogging one down - we're seeing 100 different disk greps and none of our
  processes locally are working together"; plus the thinking-budget question.
- Landed: tools/mesh_delta.py (seed + client + MCP) in the house gps_mcp
  JSON-RPC dialect. Commit: this receipt's sibling.

## The water-computer answer (the switchboard)

The disease tonight was measured, not vibes: four concurrent AI runs each
greping the same tree independently, 16 pythons, sibling olm-mine at 181M
tokens, the hung-cycle zoo the longrunner patrol caught. A hundred disk
greps is a hundred eyes each re-reading the same library. The water spec
says: index ONCE, serve MANY. Three surfaces make that real:

1. mesh_delta (this build): the MEMORY standing wave. Snapshot index with
   sha256 per file (content-addressed chunks), snapshot history (12 kept),
   and three doors:
     GET /picture                 - the most updated picture + verkle cursor
     GET /delta?since=<iso>       - added/changed/removed, each with sha256
     GET /chunk?path=&sha=        - verify-then-serve, 8MB cap, traversal-proof
   Client: `python -m tools.mesh_delta pull --peer http://<tailnet-ip>:8767
   [--apply] [--prune]` - sha-verifies every byte against the advertised
   hash before writing; removals never touch the live tree without --prune.
   MCP mode: `python -m tools.mesh_delta mcp` speaks the gps_mcp dialect
   (tools: picture, delta, fetch) for MCP clients on this machine.
2. FTS (exists): corpus text. 3. GPS ledger (exists): task_shape routing.
4. water_swarm/flock organs (exist): machine-load routing.
The switchboard law: no seat greps what an index can answer; scans are
pulled from a seeder, not re-walked per process.

## The tandem-with-local-versions cure

The R5 stash-sweep disease exists because seats share ONE working tree.
The mesh shape kills it: each machine keeps its LOCAL copy and pulls deltas
(added/changed/removed, hash-verified) from the desktop seeder. Bob's leg:
run ON bob `python -m tools.mesh_delta scan` then `pull --peer
http://<desktop-tailnet-ip>:8767 --apply` (start the seed with --bind
<tailscale-ip>); Pixel stage 2 = the same pull from Termux. Why the network
"was not transferring": nothing scheduled the transfer - git pushes were
manual, the SMB estate share is auth-walled and nothing read it on a clock.
The seeder makes the transfer a door, not a chore.

## Thinking budget (the operator's flash question, answered from the laws)

Yes: GLM-5.3-Flash levels low/high/max (default max per the model table) are
reasoning-effort rungs - max allows a larger thinking budget. "Appropriate
per task" is already law, not taste: RIB_MODEL_GATES POST-DATUM - thinking-on
rides ONLY at depth=design, 32K+ max_tokens, substance-gated; everywhere
else explicit-off (omission is a MEASURED ON state on deepseek-v4-flash).
Budget-exhaustion law: thinking-on needs sized budgets (16K starved 2/10).
The enhancement via our methods: token cues (2610.06851) steer reasoning at
decode time for free; the FAMILY_TABLE + inference_budget carry the per-task
levels; the quantizer pack now propagates these laws to every flash seat
(d01 lane proved seat inhalation tonight). Task-shape keyed thinking levels
+ cue columns = the per-task thinking spec, riding the GPS coordinates.

## v0 proof + owed

- First bootstrap scan ran 15+ min (memory/ is enormous: knots churn per
  janitor fire) - itself the water lesson; scan() now incremental
  (size+mtime fast path, sha only on change). Bootstrap lands in the
  background; round-trip proof (scan -> serve -> pull --dry -> chunk fetch
  sha-verified) completes on its landing, receipt appended below.
- Owed: seed on the tailnet IP + bob's first pull (ON bob), dashboard door
  link, and the per-machine pull tasks (the clock side of the standing wave).

## PROOF ROUND TRIP (2026-10-07T01:40Z, appended on landing)

- Bootstrap index: 561,386 files / 7.6GB in memory/ (the knot churn is the
  mass); incremental scans now diff on size+mtime.
- Round trip on 127.0.0.1:8767: picture door answered (files/bytes/ts);
  delta?since= correct 0/0/0 against a fresh snapshot; chunk fetch of
  memory/zknot/LATEST.md sha-verified True; TAMPER CHECK: a bad-sha chunk
  request refused 403; client `pull --peer` joined its local cursor to the
  peer picture in dry mode (0/0/0, as the snapshot is current).
- Mimosa L2 SSRF cure landed: _guarded_fetch (scheme fence, userinfo refusal,
  explicit allowlist - loopback + tailnet CGNAT 100.64/10 + RFC1918; public,
  link-local cloud metadata, multicast refused), DNS resolved and pinned to
  the validated IP (rebinding defense), redirects refused, bounded reads.
  The tripwires (tests/test_mesh_delta_guard.py, 5 green) caught two
  Python 3.11 ipaddress traps before they shipped: is_private now counts
  link-local metadata as private (metadata would have passed the naive
  check) and reads CGNAT as not-private (the tailnet would have been
  refused).
- Owed noted: chain_tip_index reads null (verkle_tip.json key shape differs
  from rib_boot's chain block - wire the real cursor key); production seeding
  rides the burners cage per the longrunners law; bob's first pull ON bob.
