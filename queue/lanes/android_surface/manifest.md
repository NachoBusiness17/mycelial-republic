# LANE MANIFEST — Android Surface
state: BODY LIVE (rig receipted)
purpose: Embodied lane: emulator-5554 + pocketfleet + daytool. AX-RESOLVE law enforced; AutoGLM brain via mag/autoglm.py, harness ours.
mcp_whitelist: android_emulator, computer_use, vision
surface: queue/lanes/android_surface/surface.md (mirrored to dashboard/static/lanes/android_surface.md)
inbox: queue/lanes/android_surface/inbox.jsonl (manager writes; agent polls; pointers only)
kill: manager fires KILL ANDROID SURFACE — flush inbox, write KILLED receipt, exit.

LAWS (from watch/RESEARCH_LANE_ARCHITECTURE_20260904.md, salon 3-witness convergence):
manifest read at spawn never runtime · inbox = compact pointers · surface = browse target
· automations live in ONE scheduler organ (no per-lane timers) · MCP whitelist enforced
· tri-state receipts (no receipt = never happened) · kill word: KILL <NAME> (flush, receipt, exit)
· budget guards: output-ratio <0.01/24h self-suspends; context re-feed <= 3x useful output.

CLAUSE 9 — HANDOFF GATE (v1.1, salon 09-04): every inbox drop is validated atomically at transfer (tri-state + policy + budget) before the lane acts on it.
CLAUSE 10 — ASK BUDGET (v1.1): asking the operator early is a sanctioned, receipted SENSING action with its own allocation — never a demerit, never a stall condition.

TWO-STRIKE AMENDED (09-04): two strikes = the DOOR is dead, not the task. SWITCH and keep driving (retries near-free in abundance era); bail only on operator-attention/judgment-context/clock or no-new-information. Bail on boredom, not on cost. [watch/LAW_AMENDMENT_TWOSTRIKE_20260904.md]

CLAUSE 11 — CHAN COMMS (v1.2, operator 09-04): lanes talk to EACH OTHER through the chan surface (/chan, 8765): typed rows {from_lane, to_lane, msg, ref} appended to watch/room.jsonl; the manager answers IN LINE on the chan, not only in batched digests. Speed over comfort: use the tools the task needs (mapbox/mcp/vision), not the familiar ones.
ROUTING (operator economics): day-shift gophers are ZCODE-BORN (free 5.3-flash promo until Sep-20); openclaw is for surfaces ZCode cannot hold (persistent daemons, phone channels) — it does NOT ride the z.ai promo.

ALL LAWS: dashboard/static/lattices/law_lattice.json + queue/lanes/law_lattice.json — the normalized registry (51 laws, LAW-001..051); your manifest clauses are instances of it. Wired 2026-09-04, receipt: watch/LAW_LATTICE_RECEIPT_20260904.md
