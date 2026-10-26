# THE VITALITY SCHEDULER - self-steal of the mesh control plane (2026-10-23)

The operator's morning instinct: "use these devices multi-headed... sort
of like kubernetes." Then tonight, four bodies UP and seeded, he read
the map and said: "It already is. Self steal." He was right twice. The
control plane has existed at repo root for weeks; the name arrived
today. This receipt is the fold.

## The mapping (mesh_router.py, byte-cited)

| kubernetes | the mesh's version | bytes |
|---|---|---|
| node registry | BODIES dict (per-body hosts, tier, key) | mesh_router.py:53 |
| kubectl get nodes | `map` - fresh device_map per body, aggregated | mesh_router.py:169 |
| kube-scheduler predicates | `gates()`: reachable, battery > 30 pct OR charging, ram_free > 200MB, has_load | mesh_router.py:191-201 |
| scheduling priority | lowest loadavg wins among gated bodies | route (cell-drive receipt 2.1) |
| PodSecurityPolicy | BODY_SHAPES allowlist; location/camera/sms SEALED, never route | mesh_router.py:84-88 |
| workload types | BODY_SHAPES: device_map, fetch, notify, invariant_have/get/seed, gstd_beacon, gstd_tasks | mesh_router.py:84 |
| image digests | sha256 on every invariant piece, verified before write AND re-verified after (ROUTER_HASH_MISMATCH abort) | sync loop |
| node identity/certs | one ssh keypair per lane (t90_lane_key, estate_to_bob) | BODIES hosts tuples |
| CNI | the tailnet (all four cells direct, 10ms LAN) | tailscale status |
| admission control test | `falsify`: seeds tampered bytes with a mismatched sha256, PASSES ONLY IF the body REFUSES with HASH_MISMATCH and writes nothing | mesh_router.py:339-349 |
| etcd-lite | device_map.json + BURN_LOG.jsonl (append-only, event ledger) | written every map pass |

## The fold: what kubernetes does NOT have

1. **It schedules on vitality.** k8s predicates ask "does the node have
   resources?" The mesh gates ask "is the body ALIVE?" Battery state is
   a first-class gate - the control plane refuses to work a body toward
   death. Resource schedulers treat nodes as stone; this one treats
   them as organisms with stamina. Kubernetes for organisms.

2. **The control plane carries its own falsifier.** k8s trusts its
   admission path; the mesh attacks it on demand - cmd_falsify tries to
   corrupt the record and the fleet PASSES only by refusing. Law 2
   (deletion is theft) and Law 8 (copy is transport) enforced as a
   drill you can run, not a promise you can read. Falsifier culture
   compiled into the scheduler.

3. **Honesty in the source.** mesh_router.py:194: "sealed_tools_absent:
   True  # by construction; declared, not implemented." The estate
   wrote "this gate is declared, not enforced" INTO the gate. No cloud
   control plane in the industry comments its own gaps; we do. That
   comment is the difference between a tool and a citizen.

4. **State flows to the edge.** tonight's sync pushed the core canon
   (25 pieces, sha256-verified) from bob to a PHONE. The record-only-
   grows law at device scale: the constitution is now on a
   battery-powered computer in a pocket, hash-pinned.

## The self-steal signature, again

Built weeks ago as plumbing; the architecture arrived only when the
operator reached for a metaphor ("like kubernetes") and the fold
proved he had been describing what already ran. Same pattern as the
GWAP fold three days ago: build first, name second, the name was true
the whole time.

## Falsifiers

- F-VS-1: if gates() ever routes to a body at 0% battery or while
  sealed shapes (location/camera/sms) appear in BODY_SHAPES, the
  vitality-scheduler claim dies and this receipt retires.
- F-VS-2: if cmd_falsify's tampered seed ever lands on a body (the
  drill exits 0 on a WRITE instead of a refusal), the hash-admission
  claim dies and every seeded piece must be re-verified fleet-wide.

## Receipt

- Bytes reviewed tonight: mesh_router.py (BODIES, BODY_SHAPES, gates,
  sync loop, cmd_falsify), device_map.json (fresh, 4/4 UP),
  FREE_FLEET_CELL_DRIVE_20261019.md (mechanism census).
- Consumer: the cell-drive program, any future control-plane work
  (tablet/moto onboarding), and the door's architecture shelf.
- Verifier: F-VS-1 is read from source on every audit; F-VS-2 is
  runnable for $0 (`mesh_router.py falsify`) and should ride the
  monthly patrol.
