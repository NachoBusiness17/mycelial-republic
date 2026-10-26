# THE ASK: BUILD INSTRUCTIONS - WITNESS + CONTINUITY + ARTIFACT (Q07+Q08+Q09)

Context in V2CTX.md one directory up. Three questions from the 52-question
inventory:

- Q07: the verkle chain is writer-only tamper-evident (618 evidence_lost
  rows, 2821 unaudited amendments; a disk-holder regenerates consistency).
  We have staged a gist-based tip witness (unfired, awaiting operator GO)
  and Crosby-Wallach / RFC 6962 in the bibliography. Ask: the witness
  architecture that turns our chain into externally-verifiable receipts -
  gist sufficiency vs transparency-log vs countersigning; the amendment
  second-key design; the gossip/verification recipe a stranger runs to
  check our receipts against the published tip.

- Q08: continuity is one disk deep; the C2 restore drill (offsite backup ->
  second machine -> chain verify at the published tip) has no receipt.
  Ask: the drill's exact runbook (restic restore commands, the verify call,
  the pytest gate, expected timing on a 679MB set) and what the second
  machine needs installed before the drill.

- Q09: the build artifact is unverifiable (built from the estate twin, not
  the public tree; the sha is not printed at boot; the .pck sits beside the
  exe and can be swapped). Ask: the reproducible-build design for a Godot
  4.3 export - embedding the source commit at boot, pck-integrity check,
  butler/wharf channel choice, and the one command a stranger runs to
  verify the artifact against the public repo.

Deliver: buildable specs + falsifiers per spec. Tag [public]/[inference].
1200-2500 words.
