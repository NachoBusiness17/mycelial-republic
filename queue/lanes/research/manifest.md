# LANE MANIFEST — Research
state: ARMED-PENDING
purpose: The ONLY lane that clicks. Live web research: browser-use + kernel. Feeds the intake rubric; RAW+min_faves pair pattern.
mcp_whitelist: mag, browser_use, node_repl
surface: queue/lanes/research/surface.md (mirrored to dashboard/static/lanes/research.md)
inbox: queue/lanes/research/inbox.jsonl (manager writes; agent polls; pointers only)
kill: manager fires KILL RESEARCH — flush inbox, write KILLED receipt, exit.

LAWS (from watch/RESEARCH_LANE_ARCHITECTURE_20260904.md, salon 3-witness convergence):
manifest read at spawn never runtime · inbox = compact pointers · surface = browse target
· automations live in ONE scheduler organ (no per-lane timers) · MCP whitelist enforced
· tri-state receipts (no receipt = never happened) · kill word: KILL <NAME> (flush, receipt, exit)
· budget guards: output-ratio <0.01/24h self-suspends; context re-feed <= 3x useful output.

CLAUSE 9 — HANDOFF GATE (v1.1, salon 09-04): every inbox drop is validated atomically at transfer (tri-state + policy + budget) before the lane acts on it.
CLAUSE 10 — ASK BUDGET (v1.1): asking the operator early is a sanctioned, receipted SENSING action with its own allocation — never a demerit, never a stall condition.

TWO-STRIKE AMENDED (09-04): two strikes = the DOOR is dead, not the task. SWITCH and keep driving (retries near-free in abundance era); bail only on operator-attention/judgment-context/clock or no-new-information. Bail on boredom, not on cost. [watch/LAW_AMENDMENT_TWOSTRIKE_20260904.md]

CHARTER AMENDMENT (09-04, operator): this lane is THE LINK DUMP + BACKGROUND RUNNER. Operator drops links -> process same turn (score/route/launch) -> run in background -> surface populated at every phase change. Never wait idle with a stub surface. Duplication is emphasis: duplicate long digs for cross-verification.

CLAUSE 11 — CHAN COMMS (v1.2, operator 09-04): lanes talk to EACH OTHER through the chan surface (/chan, 8765): typed rows {from_lane, to_lane, msg, ref} appended to watch/room.jsonl; the manager answers IN LINE on the chan, not only in batched digests. Speed over comfort: use the tools the task needs (mapbox/mcp/vision), not the familiar ones.
ROUTING (operator economics): day-shift gophers are ZCODE-BORN (free 5.3-flash promo until Sep-20); openclaw is for surfaces ZCode cannot hold (persistent daemons, phone channels) — it does NOT ride the z.ai promo.

SENSOR REGISTRY (intake organ 09-04, watch/INTAKE_ORGAN_SPEC_20260904.md): z.ai=CLAIMED(research) · grok/deepseek/claude/chatgpt=UP cross-verify+lens+spec+frontier-compare · X decks=feed · android=embodied · MCP rack=api · monitor=nightly. Every pull: mission-with-contract -> verbatim capture (FT-file) -> rubric card -> route. Rival pass before BUILD.

ALL LAWS: dashboard/static/lattices/law_lattice.json + queue/lanes/law_lattice.json — the normalized registry (51 laws, LAW-001..051); your manifest clauses are instances of it. Wired 2026-09-04, receipt: watch/LAW_LATTICE_RECEIPT_20260904.md


AMENDMENT — VISION PIPELINE ROW SHAPE (2026-09-05, operator order "this is what i want
the vision pipeline to do automatically"): every intake batch runs the five verbs —
READ (verbatim multi-door capture) -> FILTER (goal lattice = PULL axis) -> INTERPRET
(semantic CLUSTERS, not per-item cards) -> CITE-GATE (deterministic primary-source
verify, tri-state, uncited claims demoted to Unproven BEFORE rightsize — the organ
spec'd in watch/SELF_STEAL_VISION_PIPELINE_20260905.md) -> RIGHTSIZE (bands size the
output; BUILD launches same turn) -> FILE+WIRE same turn. Wave falsifiers: rotation
test (structure invariant across seat/time/order) + cite-rate 100% on BUILD cards.
Card: watch/SELF_STEAL_VISION_PIPELINE_20260905.md; proof run: watch/INTAKE_XBATCH_20260905.md.


SENSOR ADDITION — TELEGRAM (2026-09-05, self-steal watch/SELF_STEAL_TELEGRAM_CHANNEL_20260905.md):
public Telegram channels are a feed sensor via the t.me/s/<channel> logged-out web
preview — cage-side HTTPS GET verified live 09-05 (145KB, 20 msgs, $0, no ports).
Door rule: Bot API + public previews = sanctioned; grey scrapers / user-API harvesting
of others' channels / mass-DM = ToS ban class, REFUSED (LAW-055 line). Channels to
follow = same registry shape as X decks; add candidates to inbox with kind=pointer.
