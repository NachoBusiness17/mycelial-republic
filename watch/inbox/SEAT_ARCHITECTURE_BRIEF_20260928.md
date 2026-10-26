# SEAT ARCHITECTURE DECISION BRIEF — ZCode window vs Hermes + PC/Phone — 2026-09-28

Operator: "these are all shovels problems, find people who fixed this, check
the ZCode best practices; does the ZCode window still make sense vs Hermes?
We used the window because it was the free flash model but that's over.
Figure out the best way to work from PC and phone."

## Part 1 — the shovels, and who already fixed them

Every shovel we hand-fixed this week has a solved prior art, most of it in
the ZCode harness's own source (corpus/steal/ZCODE_OPERATING_PLAYBOOK_
20260925.md, 15/15 fact-checked against engine source):

| Our hand-fix | The solved prior art (steal source) |
|---|---|
| Headless spawn law (windows popping) | ZCode's own Bash tool channel: managed execution never pops consoles. The pops came from OUR test files doing raw subprocess. Steal: route all spawned execution through mag.headless / managed channels; never raw subprocess in tests. |
| Suite-vs-live-daemon races | ZCode test discipline + our own MAG_GAPS_LOG conftest precedent: ephemeral per-worker state dirs via env redirect. Serialization groups were the band-aid; env-redirect is the cure. Next window. |
| Prompt-cache measurement | Playbook law 1: the amend-cache is keyed on byte-identical ask text (FNV-1a). Our stealth driver's stable mining preamble now mirrors it; cached_tokens is the measurement. |
| Reasoning-model empty content | Provider-convention steal (tonight): reasoning_content field + finish_reason=length + 4x retry rail. |
| Hook contracts | Playbook laws 10-13: exit-2-or-deny only, model guidance via additionalContext, yolo bypass law. Already codified — keep citing it. |

Law: before hand-rolling any future shovel, check the playbook + ZCode
source first. The harness is open source (zai-org/ZCode); its answers are
citable by path.

## Part 2 — ZCode window vs Hermes: BOTH, with different jobs

Byte finding that reframes the question: **Hermes's default model is
already Ling-3.0-flash-sante:free via Nous** (config.yaml 2026-09-28) —
the free flash did not end; it moved. Hermes is alive (3 processes),
gateway green, Discord channel (NT-ACv2) wired, steering + warm boot
integrated with the estate.

The window's real advantage was never only the free model — it is the TOOL
HARNESS: subagent fan-out, hooks, the workflow gate, the record
integration, the seats-are-disposable architecture. That value is
model-independent.

**Ruling (proposed):**
- **Hermes = the standing 24/7 ambient seat.** Free Ling via Nous,
  headless, Discord-connected, already running. Owns: monitoring, mesh
  comms, phone-visible status, steering intake, the AFK cadence.
- **ZCode window = the deep-work bench**, opened on demand: reset-day
  fullsends, heavy coding, subagent waves (the envelope law's home), gate
  and surgery work. Not the standing interface — the standing interface
  must cost $0 and survive a model change, and only Hermes does.
- The estate already runs without either window open (boot lane + stealth
  driver + 13 tasks) — tonight proved it. The windows are tools the estate
  uses, not the place the estate lives.

## Part 3 — PC + phone, best work

Laws on record: plain-text status only (phone cannot render cards),
boot-lane at logon, TG bot deleted (stays deleted), Discord gateway green.

- **Phone = Discord, through Hermes.** Status, GO/STOP words, steering:
  all as plain text in NT-ACv2, which the phone renders natively. The
  mechanism exists end to end (Discord -> Hermes gateway -> hermes_steering
  -> the estate's steer intake). Proposal: Hermes posts ONE daily plain-text
  digest (drill verdict, fossil check, dirac scan, driver heartbeat count)
  to the channel — phone-readable by construction.
- **PC = the organs run themselves** (boot lane + stealth driver + tasks).
  A ZCode window opens for fullsends and heavy work; a Hermes desktop
  session holds the ambient conversation.
- **Netlify dashboard**: stays pending — once the Discord digest flows it
  is optional, not load-bearing.

## Decisions needed from the operator (one line each)

1. Ratify the split: Hermes ambient / ZCode on-demand. (Say "ratified".)
2. Discord daily digest GO? (Hermes posts it; no new bot.)
3. Desk chrome: restore or formally retire (open since this morning).
