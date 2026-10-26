---
name: npc-seat-architecture-20260917
description: NPC = SEAT architecture filed 2026-09-17 — every NPC is a Kabuki model seat, one ractor many faces, mesh-distributed over the 26-lane pool; steals = DCC System/Pratchett narrativium/WoW character work; build order behind gates; falsifiers bind
metadata:
  node_type: memory
  type: project
  originSessionId: sess_199e4b14-3a8b-46e9-ba5e-57c166fc2967
---

Operator order 2026-09-17 night (with his Don Quixote 2.0 rendered piece — "WAKE UP NPC" as
the spec): "steal Dungeon Crawler Carl and Terry Pratchett full research and game systems,
steal how WoW does their character work, and I want to make ours AI based — every NPC is
basically a different Kabuki model you're talking to; one ractor, many faces, within the mesh
network of our wave protocol at scale. Self steal distribution of compute."

**THE ARCHITECTURE (watch/inbox/NPC_RACTOR_ARCHITECTURE_20260917.md):** every NPC is a
SEAT. The ractor engine (Laplacian belief graph, OCEAN constants, threshold verdicts) is the
shared substrate; each face = a Kabuki seat (configs/kabuki_cast.json + dissection personas —
machinery exists: mag/cage_intake.py, kabuki_salon.py) with its own personality prompt, lane
routing, and memory edge; compute distributes across the 26-lane providers.yaml pool under
U8's measured concurrency; face→lane by class (DM face = strongest free lane, mob faces =
fast small lanes, Elder face reads only).

**THE THREE STEALS:** DCC = the System as narrator-AI with personality/agenda (our ractor is
the DM seat), NPCs-were-people = our bones ghosts/grudges already, sponsors = mud boons,
followers-as-resource = relay presence. Pratchett = narrativium is load-bearing (our parable
register IS it), Death SPEAKS IN CAPS = the inscription register, Small Gods = attention
powers lanes, L-space = corpus through the Librarian. WoW = class→face template, spec→OCEAN
weights, talents→persisted learned traits (fs_lore pattern), gear→boon/bestowal, leveling→
ramp law + evolution-loop ledger.

**BUILD ORDER (each behind its gate):** (1) face registry — extend kabuki_cast schema with
{face, class, spec-weights, lane, grudge, tale}; mud's first 3 NPCs (innkeeper, vault warden,
bones guide) answer through chat_provider with face prompts. (2) traits into step() — the
Elder's #1, NPC faces inherit trait effects. (3) the DM face — one ractor-backed narrator
seat: DCC's System + Pratchett's Death + WoW's quest-giver, one seat with faces. (4) belief =
attention — relay presence + X followers feed named-NPC belief meters gating lane routing.

**FALSIFIERS:** player can't tell faces apart in 3 exchanges → collapse to one narrator; NPC
persistence fails a reload + relay restart → ledger decorative; DM face cost >2× mob face →
mesh routing wrong.

Research deep dives queued: UF-116 (DCC systems: narrator voice, sponsors, floors, crowd
economics) + UF-117 (WoW server-side character architecture: tables, spells packet, quest
text, eluna per-NPC personalities). Related: [[ractor-engine-spec-complete]],
[[mud-superhot-adam-access]], [[union-fullsend-day-20260917]].
