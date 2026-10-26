---
name: scout-census-and-schema-registry-20260927
description: 9/27 scout counting pin (crash census counts stanzas not
  substrings) + events key schema registry (30 writer keys, both gates armed) +
  late swarm findings
metadata:
  node_type: memory
  type: project
  originSessionId: sess_fd5ec147-a47d-41ee-91f4-afd899b524ca
---

Three significant landings from the late flash-lane burn:

**Crash census pin (B2-357)**: crash census counts stanzas (separated by `[iso] stage=` lines) instead of substring math; a chained exception's two Traceback headers count as ONE crash. Live log backward-compatible at real=52. The chains feature (chain-quote detection) has never fired on real production bytes — only synthetic fixtures exercise it.

**Events key schema registry (B2-342)**: 30 writer keys pinned with first-seen seq, owning writer, census count. Both gates armed: shared_surface validate = ERROR on never-seen key; fold = WARN per distinct unknown key. Two self-caught defects fixed pre-landing (Set.size vs .length loader bug, shared_surface.py file-too-long extracted instead of registered).

**Late swarm landings**: 12+ additional lanes landed across the queue — pointer rot checker (B2-491), resolver deadline bound (B2-489), G1 tripwire fired (first genuine fleet G1 FAIL = probe20_run.py), LAW-12 registered in law registry, seed-mcp server built and cold-join falsified 10/10.

**Why:** the burn shifted from "execute the queue" to "execute the queue AND file every latent defect each lane surfaces" — the self-feed multiplier turned 167 planned briefs into 422+ as each lane's receipt became the next lane's pointer.

**How to apply:** future burns should plan for the self-feed multiplier (~2.4x brief expansion) and budget lanes accordingly. The receipt-ghost and checkbox-desync diseases are structural at scale; one mechanism must own queue state above ~20 lanes.
