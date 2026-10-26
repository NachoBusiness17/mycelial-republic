# THE STEER CHANNEL SPEC (2026-09-30) - the operator turns the fleet mid-flight

He is an INTERRUPTER; that is part of the law (his words, 2026-09-30). This spec defines watch/inbox/STEER.md: one file the operator edits (or one DM to Hermes) that every mate's next mission pack must consume. The fleet turns without a meeting, without a prompt-window rebuild, without waiting for any session to end.

## WHY A FILE (evidence)

- The seam already half-exists three times: (1) mag/compass.py injects a preamble when the operator types something ambiguous ("continue", "go", "steer ...") (FLEET_IMPRINT_20260917.md:159); (2) the [steer] rows in memory/facts/behavioral.jsonl are a fact-level steer channel with thousands of echoes; (3) phone_relay (2026-09-24, operator GO) already moves operator word to his phone over the Mag DM - the reverse direction is the same lane. This spec is the self-steal that unifies them, not a new organ.
- The shared-surface law fits: watch/inbox/ is the durable cross-surface root every context already reads first (AGENTS.md shared artifact boundary). A VS Code, z.code, or Docker session that never sees the DM still sees the inbox.
- Precedent for file-as-order: the operator's one-line orders are already standing orders (an entire workflow was born from one line, "go wide and concurrent on all our steal models and do mickey17 style", burn_reset_20260927/flash50/w4-12.md:76).

## THE FILE CONTRACT

Location: `watch/inbox/STEER.md` (Docker surface: `/board/inbox/STEER.md`). Format: JSONL rows, append-only, one row per interrupt.

Minimal row (the ask's shape, kept exactly):
```
{"mate": "all", "steer": "go wide on the lens backlog", "ts": "2026-09-30T14:02:00Z"}
```

Full row (recommended; the two extra fields are provenance, see ANTI-FORGERY):
```
{"id": "st_20260930T1402_1", "mate": "all|<mate-id>", "steer": "<operator text verbatim>", "ts": "<ISO-8601>", "via": "hand-edit|hermes-dm|phone-relay"}
```

Rules:
1. `mate`: `all` (fleet-wide) or a single mate id. No wildcards beyond `all` (one steerable scope, no cleverness).
2. `steer`: his words verbatim, no seat paraphrase. Parsing happens downstream against the INTERRUPTS.md grammar; the file holds the raw voice so later parsers can re-read it.
3. LATEST WINS: for a given mate, the operative row is the row with the newest `ts` among rows where `mate` equals that mate's id or `all`. Older rows remain in the file as history (append-only, like the tide - never amend the strata, law 20).
4. Write paths: (a) the operator hand-edits the file; (b) he DMs Hermes and Hermes appends the row with `via: hermes-dm` (Hermes is dormant but dispatch-capable, dispatch log active - AGENTS.md); (c) phone-relay appends with `via: phone-relay`. No other writer is a source of operator intent.

## THE READ PATH (leave protocol)

1. BETWEEN MATE CYCLES: the leave protocol (whatever composes the next mission pack) reads STEER.md, resolves the operative row for that mate, and injects it verbatim into the mission pack under an `## OPERATOR STEER` section, with the row id/ts, plus the one-line parse from the INTERRUPTS.md table (e.g. "go wide" -> WIDEN: fan out parallel lanes).
2. ACKNOWLEDGE IN THE NEXT RECEIPT: the mate's next landed receipt carries `steer_ack: <id or ts>`. Acknowledgment is compliance-shaped: one line naming what changed in the mate's plan because of the row. An unacked row older than one full mate cycle surfaces in memory/attention.md (same cadence law as the handshake STALLED flag, SKILL.md law 14).
3. MID-CYCLE INTERRUPTS (he should not wait for a cycle boundary): the DM path. He messages Hermes; Hermes appends the row AND, when the target mate is a live session the steerer can reach, passes it in-band immediately (one-steerer law, SKILL.md law 16: check LIVE SESSIONS before spawning anything). The row lands regardless - the file is the durable copy, the in-band pass is the accelerator.
4. CONFLICT WITH STATIC DOCTRINE: a steer row beats any static card, rib, or brief (it is him, live) EXCEPT the irreversible gates: a row still cannot self-authorize T3/L3 irreversible effects (secrets, deletion, spend beyond armed budget, publish-without-centerline). Those answer with the existing promote-gate shape - the row can REQUEST the seal; the seal is still his explicit act through the existing gate (AGENTS.md: model text can propose; the switchboard authorizes effects; law: no lockouts without operator, no lockups by operator text alone).

## ANTI-FORGERY (non-negotiable teeth)

The estate has already caught an ungated write forging `by="operator"` (audit_20260926/LANE10_ADVERSARIAL.md:405). Therefore:
- A row without a `via` field is treated by consumers as a PROPOSAL, not an order (shared-surface contract: model text proposes; only operator authorizes).
- `via: hand-edit` rows are operator-authored by definition (the file is his surface, like the journal).
- Hermes/phone-relay rows must quote his DM verbatim and carry the DM timestamp; Hermes never improves his wording (register is signal, INTERRUPTS.md parser note 2).
- Append-only: any rewrite of an existing row is an incident, not an edit.

## VALIDATION AND GATES

- Shape check rides the existing shared-surface validator surface: malformed rows (missing mate/steer/ts, unparseable JSON) fail loud in the leave protocol log, and the mate proceeds with the last VALID row - a corrupt steer never silently widens scope.
- Building the reader/injector is an amendment to the leave protocol, gated per the workflow-gate law if it ships as a workflow; spec-first (this file is the spec) per build discipline. Falsifier: a mate cycle that ignores an unacked operative row for a full cycle without an attention.md flag = the channel failed.

## WHAT THIS IS NOT

Not telemetry about him (presence mining has its own permission frame, operator_presence.json note). Not a chat log. Not a replacement for corrections-that-mint-law (a correction that should bind forever still graduates into operator-corrections SKILL with a law number; STEER.md is the live helm, the SKILL is the rudder design).

Activation: create the empty file with a header comment row and wire the leave-protocol read. One file, one reader, one acknowledgment field - and the fleet is steerable mid-flight by a man typing one line at 4PM on a Thursday.
