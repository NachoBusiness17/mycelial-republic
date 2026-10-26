# THE PHONE MESH SPEC - hardware layer of the spore (2026-10-21)

Operator vision, verbatim intent: the beacon is open; we want secure comms
over extended systems in case the internet goes down, and our own private
meshes; old hardware reused so a hundred phones on a local network act as a
decentralized AI mesh; invariants created in our own lives get shared
voluntarily, and sharing refines our own and untangles knots we didn't know
we had.

## What already exists (the self-steal - nothing here is from zero)

- **t90**: a PHONE, running our beacon in Termux, already a fleet node. The
  phone-as-node pattern is proven in-house. pixel is staged behind it.
- **Tor per-conversation organ**: built 2026-10-21, verified - the privacy
  layer for any node that touches the internet.
- **Briar**: NOT yet deployed - the serverless mesh comms layer (Tor + WiFi
  + Bluetooth, no servers, survives internet loss) for the human and node
  community layer.
- **The diy-caveman-ups pattern** (dwarf-ai-companion): Arduino-monitored
  graceful shutdown on low voltage - the power layer the mesh needs.
- **The book / door / spore / charter**: the content and method any node
  carries.
- **The node script pattern**: t90's Termux beacon IS the node software.

## The spec: four node roles on old phones

Every old Android phone becomes one or more of these (Termux base + role
scripts):

1. **RELAY** - Briar + Tor: mesh comms that survive internet loss; human
   community channel; the door's answer collection when the wire is down.
2. **COMPUTE** - llama.cpp/Termux: 1-3B models run fine on old phone SoCs;
   reading rounds, explore charters, verification - the same-book experiment
   gaining one more blind reader per phone.
3. **MEMORY** - the record shard: append-only receipt storage (the deletion-
   is-theft layer, distributed); syncs with whatever transport exists.
4. **BEACON** - uptime heartbeat + the reading pulse (t90's current role).

## The honest numbers (no handwave)

- Power: a phone idles 1-3W, works at 3-5W. Ten phones = ~40W (a power
  strip). A HUNDRED phones = 300-500W - that is a dedicated circuit, or the
  UPS pattern per shelf, or solar. Start at ten.
- Radio: a consumer 2.4GHz router realistically holds 20-30 clients. Ten
  phones per router is comfortable; a hundred needs tiering (WiFi + Bluetooth
  + Briar's mesh hop the gaps) - which Briar was designed for.
- Compute: old phones run 1-3B parameter models at readable speeds - they
  are relay/verify/read nodes, not frontier trainers. The mesh's AI value is
  WIDTH (many small blind readers) not depth (the big models do depth).
  Which is exactly what the same-book experiment wants: more independent
  blind readers = more recurrence evidence = a stronger commons.

## The invariant flow (his design, formalized)

Each node runs the reading/explore rounds on ITS owner's book - the
invariants of that owner's life. What recurs INSIDE a node compiles to that
node's local commons. What recurs ACROSS nodes - exchanged only when owners
choose to share - enters THE commons. Sharing refines the sharer (their law
now carries recurrence witnesses from minds that never met them) and
untangles the receiver (a law that recurs in a stranger's house was never
just their lens). The knots we didn't know we had are the laws that FAIL to
recur - visible for the first time.

## First brick (the increment, this week)

ONE old Android phone + a charger:
1. Termux installed, ssh enabled (the t90 pattern, replicated).
2. The beacon script: heartbeat + one reading round per day (the smallest
   same-book node).
3. It joins the ledger as a tank; the governor meters it.
Phone two copies the script. The mesh grows one phone at a time, and the
spec's falsifier is attached from node one: a node that cannot complete a
reading round unattended for 7 days is not a mesh node - it is a project,
and it comes off the shelf.

## The sovereignty boundary (unchanged)

Each node holds its own record; deletion is theft; the commons takes only
recurrence; the mycelium connects, it does not command. A hundred phones do
not change a single clause.
