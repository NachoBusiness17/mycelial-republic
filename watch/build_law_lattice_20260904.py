# -*- coding: utf-8 -*-
# Generator for THE LAW LATTICE (2026-09-04) — normalizer gopher run.
# Writes queue/lanes/law_lattice.json (law_lattice.v1) and the canonical
# export dashboard/static/lattices/law_lattice.json (lattice_logic.v1).
# One source of truth -> two files, no drift.
import json
from collections import Counter

L = []
def law(id_, name, statement, source, scope, enforcement, consumer, disposition):
    L.append({"id": id_, "name": name, "statement": statement, "source": source,
              "scope": scope, "enforcement": enforcement, "consumer": consumer,
              "disposition": disposition})

# --- Embodiment / transducer (dogfood + vision endowment) ---
law("LAW-001","AX-RESOLVE-OVER-PIXEL-GUESS",
 "Resolve targets from the accessibility tree (exact bounds, clickability) and act on those; never let a vision brain guess pixel coordinates (measured: pixel-guess missed by 1009px; small-text pixel misreads confirmed twice; AX exact).",
 "watch/DOGFOOD_DAYTOOL_AX_VS_PIXEL_20260904.md",
 "Tapping/reading UI on embodied surfaces (WebView measured; native apps Unproven). Absorbs SMALL-TEXT-PIXEL law (vision endowment) as second measurement.",
 "runtime",
 "android_surface manifest; mag/autoglm.py + scripts/vision_endowment.py harnesses",
 "FOLDED")
law("LAW-002","NORMALIZE-AT-BOUNDARY",
 "Normalize verb case/aliases at the harness boundary; the action lattice stays canonical inside.",
 "watch/DOGFOOD_DAYTOOL_AX_VS_PIXEL_20260904.md",
 "Actuator harness input parsing (vendor returned 'Tap' vs grammar 'tap').",
 "runtime",
 "mag/autoglm.py boundary normalizer; android_surface manifest",
 "FOLDED")
law("LAW-003","ONE-CANONICAL-MIRROR-SHAPE",
 "Every file in dashboard/static/lattices/ is produced only by mag.lattice_logic export with shape {schema: lattice_logic.v1, entries: [...]}; raw copies are forbidden (measured: cp collapsed 47 entries into 1 walked entry).",
 "watch/DOGFOOD_DAYTOOL_AX_VS_PIXEL_20260904.md",
 "dashboard/static/lattices/* mirrors; any future static lattice export.",
 "structural",
 "mag/lattice_logic.py export (sole producer); daytool walker",
 "FOLDED")
law("LAW-004","TRUNCATION-BURN",
 "Treat empty-content-at-token-cap (finish=length, no error field) as a quota-BURNING failure, not a clean empty: set max_tokens above the realistic answer budget (vision-exp cap now 1200) and count the burned tokens.",
 "watch/VISION_ENDOWMENT_RECEIPT_20260904.md",
 "Vision/LLM calls with max_tokens caps, especially free-lane vision models.",
 "runtime",
 "mag/vision.py; vision/endowment harness caps",
 "FOLDED")
law("LAW-005","SHARED-RIG-DRIFT",
 "On shared rigs every prep self-heals to the expected surface (tap the home button) and every run raises on null ground truth — never score against a drifted environment.",
 "watch/VISION_ENDOWMENT_RECEIPT_20260904.md",
 "emulator-5554 and any surface more than one driver can navigate.",
 "runtime",
 "scripts/vision_endowment.py prep+drift-guard; android test harnesses",
 "FOLDED")
law("LAW-006","PILL-CONCATENATION",
 "Inject delimiters between concatenated AX spans in the transducer; never hand a small model unsegmented pill text ('generic entries47 entriesinvariants.json').",
 "watch/VISION_ENDOWMENT_RECEIPT_20260904.md",
 "AX/accessibility-tree text serialization feeding small models.",
 "runtime",
 "see()/transducer output format (fix belongs in the tool, not the model)",
 "FOLDED")
law("LAW-007","TRANSDUCER-PREFERENCE",
 "Offer the structure channel first and label both channels; dumb models prefer the tree when both are available (measured 5/5 chose 'ui').",
 "watch/VISION_ENDOWMENT_RECEIPT_20260904.md",
 "Endowment tool design; observation-grade (n=5 tasks, one page).",
 "prose",
 "transducer/endowment tool design notes",
 "FOLDED")
law("LAW-008","QUESTION-TEMPLATE",
 "Task wording is part of the transducer surface: state answer formats exactly and idiomatically — dumb models read templates literally and will pour wrong data into a literal template.",
 "watch/VISION_ENDOWMENT_RECEIPT_20260904.md",
 "Harness question authoring for small models (t4 exhibit: coords poured into 'pos X/Y').",
 "prose",
 "harness/task authors; evals lane",
 "FOLDED")

# --- Platform / z.ai steal ---
law("LAW-009","POLL-NOT-PUSH",
 "z.ai exposes zero webhook/callback surface (86/86 mirror pages, 14 openapi paths): own the polling loop; never wait for a push that cannot come — the vendor concedes orchestration to us.",
 "watch/STEAL_ZAI_SYSTEMS_AUTOMATE_20260904.md",
 "All z.ai API integrations (async doors are FIRE then POLL).",
 "structural",
 "scheduler organ; day_work scheduler; any agent calling z.ai async",
 "FOLDED")
law("LAW-010","HONEST-AUTH-WALL",
 "Never fake past an auth wall (login/captcha): name the wall, stop, escalate to the operator — steal the vendor's Take_over primitive pattern into every fleet actuator spec.",
 "watch/STEAL_ZAI_SYSTEMS_AUTOMATE_20260904.md",
 "Embodied/web actuators hitting credentials, captchas, consent screens.",
 "prose",
 "android_surface manifest; actuator specs (operator-gates kin)",
 "FOLDED")

# --- Claim organ / leases ---
law("LAW-011","JUDGE-THEN-CAS",
 "Commit takeovers by compare-and-swap on the target's identity token: re-read at commit and act only on exact token match; on any race lose honestly with zero writes (split-brain closed: exactly 1 winner per contended round).",
 "watch/CAS_FIX_RECEIPT_20260904.md",
 "bay claim organ stale-takeover; window throttle takeover; any file-based claim commit.",
 "structural",
 "mag/bay_organs.py (_tomb_move_if_same); mag/window_throttle.py; mag/race_harness.py gate",
 "FOLDED")
law("LAW-012","LEASE-OUTLIVES-CLAIMANT",
 "A lease can outlive its claimant: expiry or proven staleness — not pid liveness alone — governs takeover; pid is attribution. Judge staleness at takeover; never trust that a present claim is live.",
 "watch/CAS_FIX_RECEIPT_20260904.md",
 "Claim leases everywhere (bay claims: grace+pid-death variant; window throttle: expiry-only variant, claim outlives claimant — builder receipt-002 lease law).",
 "structural",
 "mag/bay_organs.py; mag/window_throttle.py",
 "FOLDED")

# --- Two-strike + economics/meter ---
law("LAW-013","TWO-STRIKE-AMENDED",
 "Two strikes kill the DOOR, not the task: switch lane/approach and keep driving (retries near-free); bail only on operator attention, judgment-seat context, clock, or no-new-information — bail on boredom, not on cost.",
 "watch/LAW_AMENDMENT_TWOSTRIKE_20260904.md",
 "All seats/lanes, all retries. Supersedes scarcity-era original (original tombstoned into this row's lineage). Abundance premise is a LANE claim: flash/bay abundant, premium seat-lane scarce until discipline lands (economist stamp).",
 "prose",
 "all 7 lane manifests (amended block)",
 "FOLDED")
law("LAW-014","OUTPUT-RATIO",
 "Retire any automation/session whose useful-output divided by billed-tokens < 0.01 over rolling 24h (zombie-tick exhibit: would have killed it day one).",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "Every automation and long session; premium lanes first. Origin: watch/USAGE_METER_SELF_STEAL_20260904.md law 1.",
 "runtime",
 "usage meter + nightly usage-db sweep organ (salon direction item 2)",
 "FOLDED")
law("LAW-015","CONTEXT-DEBT",
 "Compaction + context re-feed must stay <= 3x peak useful output; retire beyond.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "Long conversations and looped agents. Origin: watch/USAGE_METER_SELF_STEAL_20260904.md law 3.",
 "runtime",
 "lane manifest budget guards; judgment-seat hygiene",
 "FOLDED")
law("LAW-016","HEARTBEAT-THROTTLE",
 "Heartbeats are budgeted burns: 'exit fast' is not free when context re-feed dominates; budget heartbeat cadence against useful output.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "Scheduled loops, watchers, daemons. Origin: watch/USAGE_METER_SELF_STEAL_20260904.md law 4.",
 "runtime",
 "meter; scheduler organ cadence",
 "FOLDED")
law("LAW-017","MODEL-PIN-ISOLATION",
 "Subagents never inherit premium pins; default every spawn to the cheapest capable lane.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "All subagent spawns. Origin: watch/USAGE_METER_SELF_STEAL_20260904.md law 2.",
 "runtime",
 "swarm_worker DEFAULT_PROVIDER + rib_chat defaults (repointed 08-27)",
 "FOLDED")
law("LAW-018","MODEL-PIN-EXPIRY",
 "A premium pin >72h without a completed task auto-demotes to the cheap lane.",
 "watch/USAGE_METER_SELF_STEAL_20260904.md",
 "Premium lane pins (z_ai2-class). No enforcing organ yet — beyond the mission's named sources, disclosed in the receipt.",
 "prose",
 "swarm pin manager / economist",
 "FOLDED")

# --- Epistemics / handbook ---
law("LAW-019","CITE-VERIFY",
 "A citation is a claim until byte-checked against its source (ns-3 fake-citation exhibit); grok's auto-sourced captures are the cheapest verify lane.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "Research outputs, salon witnesses, any agent citing a source.",
 "runtime",
 "research lane verify pass; intake organ",
 "FOLDED")
law("LAW-020","TRAIL-DISCIPLINE",
 "Every lane action lands as a trail row (ts/actor/event/detail/artifacts) same-turn; trails/surfaces/digests are files on disk, mirrored — no era gets lost again.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "All lanes and seats. Append-only is convention until LAW-043 hash-chaining lands.",
 "structural",
 "queue/lanes/*/trail.jsonl + dashboard mirrors",
 "FOLDED")
law("LAW-021","RECEIPTS-HAVE-HYPOTHESES",
 "Every receipt states its hypothesis and a tri-state verdict (Supported/Disputed/Unproven) with evidence attached; thinking is evidence of method, not law itself.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "watch/ cards, salon folds, run receipts.",
 "prose",
 "card template; salon runner",
 "FOLDED")
law("LAW-022","SACRED-COWS-NOT-LEGACY-SHIT",
 "Old daemons/drafts are one draft of the brain: steal the bones, name the reinterpretation, retire the draft — never frame fleet history as garbage.",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "All self-steal and retirement work (operator-corrected standing law).",
 "prose",
 "AGENTS.md standing laws; operator-corrections skill",
 "FOLDED")
law("LAW-023","TOPOLOGY-LAW",
 "Android fleet: one golden body — never clone logins (canon account at stake); UI-as-API; bodies are the embodied lane's field office (2 live, 4 fit).",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "android_surface lane; AVD/emulator management.",
 "prose",
 "android_surface manifest",
 "FOLDED")

# --- Frontier thinking rules (FT-001) ---
law("LAW-024","CUTOFF-HONESTY",
 "State knowledge limits in ONE line and keep driving structurally sound reasoning; never confabulate past a cutoff (blind-7B honest refusals = the baseline pattern).",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "All answer composition under knowledge limits.",
 "prose",
 "RIB boot clauses (RIB_LANE_WINDOW_BOOT)",
 "FOLDED")
law("LAW-025","DEFINE-THE-NEGATIVE-SPACE",
 "Before proposing X, enumerate what counts as NOT-X so the boundary is structural, not a vibe.",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "Research/scouting missions; rubric definitions.",
 "prose",
 "RIB boot clauses; intake rubric",
 "FOLDED")
law("LAW-026","STRUCTURAL-OVER-TEMPORAL",
 "Under knowledge limits, rank candidates by structural persistence (likely to remain so) over recency claims.",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "Signal-source selection; restock missions.",
 "prose",
 "research restock rubric",
 "FOLDED")
law("LAW-027","LEADING-INDICATOR-PREFERENCE",
 "Score signal sources by how EARLY the signal fires (certs before press, filings before calls, downloads before coverage).",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "Signal-source ranking.",
 "prose",
 "research restock rubric",
 "FOLDED")
law("LAW-028","DISCARD-TRACKING",
 "The thinking is wider than the answer: capture the cut list too — ingest both the verbatim thinking and the answer (FT loop harvests both).",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "FT ingest loop; salon distills.",
 "prose",
 "corpus/frontier_thinking/ captures + INDEX",
 "FOLDED")
law("LAW-029","OUTPUT-BUDGET-DISCIPLINE",
 "Restate the user's format contract to yourself before composing; enforce via a format gate where machine-checkable.",
 "corpus/frontier_thinking/FT001_zai53_research_restock_20260904.md",
 "All composing agents; harness format gates.",
 "runtime",
 "RIB boot clauses; format gates",
 "FOLDED")

# --- Lane contract (manifest clauses) ---
law("LAW-030","MANIFEST-AT-SPAWN",
 "The lane manifest is read once at spawn, never at runtime; invariants live in files, not in-process memory.",
 "queue/lanes/builder/manifest.md",
 "All 7 lanes (LAWS block). Convention until MCP_MANIFEST_SPEC enforces at spawn.",
 "runtime",
 "lane spawn; MCP_MANIFEST_SPEC (hardening pending)",
 "FOLDED")
law("LAW-031","INBOX-POINTERS-ONLY",
 "Inbox rows are compact pointers; payloads live in the files the pointer names.",
 "queue/lanes/builder/manifest.md",
 "All lane inboxes (jsonl).",
 "runtime",
 "queue/lanes/*/inbox.jsonl writers",
 "FOLDED")
law("LAW-032","SURFACE-BROWSE-TARGET",
 "The lane surface is the operator's browse target: populate at every phase change; never idle with a stub surface.",
 "queue/lanes/builder/manifest.md",
 "All lane surfaces (+ dashboard mirrors).",
 "prose",
 "queue/lanes/*/surface.md; hardener = LAW-044",
 "FOLDED")
law("LAW-033","ONE-SCHEDULER-ORGAN",
 "All timers live in ONE scheduler organ; a lane cannot run its own cron — architectural absence is the enforcement.",
 "queue/lanes/builder/manifest.md",
 "Whole fleet (respawn law kin: no second supervisors).",
 "structural",
 "container governor + restart policies; mag-docker-watchdog",
 "FOLDED")
law("LAW-034","MCP-WHITELIST",
 "A lane may call only the MCP servers named in its manifest.",
 "queue/lanes/builder/manifest.md",
 "All lanes (fair-use firewall kin).",
 "runtime",
 "lane spawn enforcement (MCP_MANIFEST_SPEC)",
 "FOLDED")
law("LAW-035","TRI-STATE-RECEIPTS",
 "No receipt = never happened: every completed action carries a tri-state receipt (Supported/Disputed/Unproven) before the arc closes.",
 "queue/lanes/builder/manifest.md",
 "All lanes; today a logging convention — hardens via LAW-037 gate.",
 "runtime",
 "all lane trails/receipts",
 "FOLDED")
law("LAW-036","KILL-WORD",
 "Manager fires 'KILL <NAME>': the lane flushes its inbox, writes a KILLED receipt, and exits.",
 "queue/lanes/builder/manifest.md",
 "All lanes. Kill-switch designed, never fired — untested physics; keep the path warm.",
 "runtime",
 "manager; kill-switch registry (Agreements charter)",
 "FOLDED")
law("LAW-037","HANDOFF-GATE",
 "Every inbox drop is validated atomically at transfer (tri-state receipt + policy check + budget check) before the lane acts on it.",
 "watch/STEAL_ORG_VS_FIELD_20260904.md",
 "All lane inboxes (clause 9, v1.1). In manifests as convention; enforcement build pending.",
 "prose",
 "all lane manifests (clause 9); hardener = LAW-046",
 "FOLDED")
law("LAW-038","ASK-BUDGET",
 "Asking the operator early is a sanctioned, receipted SENSING action with its own allocation — never a demerit, never a stall condition.",
 "watch/STEAL_ORG_VS_FIELD_20260904.md",
 "All lanes (clause 10, v1.1). DISPUTED: the stall-ladder organ (stall->nudge->worth-eval->kill) still counts asking as stalling — live conflict until LAW-048 counter lands.",
 "prose",
 "all lane manifests (clause 10); hardener = LAW-048",
 "FOLDED")
law("LAW-039","CHAN-COMMS",
 "Lanes talk to each other through the chan surface: typed rows {from_lane,to_lane,msg,ref} appended to watch/room.jsonl; the manager answers IN LINE, not only in batched digests. Speed over comfort: use the tools the task needs.",
 "queue/lanes/builder/manifest.md",
 "All lanes + manager (clause 11, v1.2).",
 "prose",
 "watch/room.jsonl; /chan surface (8765)",
 "FOLDED")
law("LAW-040","RESEARCH-SAME-TURN",
 "Dropped links process SAME TURN (score/route/launch), run in background, surface at every phase change; duplication of long digs is emphasis (cross-verification). Never wait idle with a stub surface.",
 "queue/lanes/research/manifest.md",
 "Research lane charter amendment. Measured FAILING as prose (forgotten 3x — architecture card tier-1 exhibit): flagged, hardener = LAW-044.",
 "prose",
 "research manifest; hardener = LAW-044",
 "FOLDED")

# --- Architecture doctrine + candidates ---
law("LAW-041","STRUCTURE-IS-LAW",
 "Enforce by physics first (structural: violation impossible or instantly self-evident), then runtime checks, then prose; move every Tier-1 law down a tier and harden Tier-2 to Tier-3 — every law that worked today was structural, every failure was prose.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "The meta-law: all law authoring and audits (this lattice follows it via the enforcement field).",
 "prose",
 "this lattice; evals lane; redesign candidates below",
 "FOLDED")
law("LAW-042","MACHINE-CHECKABLE-OR-DECORATIVE",
 "A law whose condition is prose is decorative to a machine (measured: 8/8 law-registry conditions unfirable by lattice_logic chain()): law conditions go structured as they are touched — the Evals lane's first KPI.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "The law registry, this lattice's conditions, invariant checks. Same finding in dogfood card + salon blind spot + company-design open wound (deduped into this row).",
 "runtime",
 "mag/lattice_logic.py chain(); evals lane charter (pending)",
 "FOLDED")
law("LAW-043","HASH-CHAINED-TRAILS",
 "Each trail row commits to the prior row's hash (verkle for trails) so rewriting history is self-evident, not trusted — append-only becomes physics.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "All trails. Candidate (Unproven) pending the physical-computing field fold.",
 "prose",
 "trail writers; verkle chain (design kin)",
 "ROUTED")
law("LAW-044","STRUCTURAL-SURFACE-POPULATION",
 "The scheduler writes interim state to any lane surface whose trail grows while its surface stays stale — population stops being the agent's choice.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "Lane surfaces; fixes the LAW-032/LAW-040 class of prose failures. Candidate (Unproven).",
 "prose",
 "scheduler organ build (salon direction kin)",
 "ROUTED")
law("LAW-045","DELETE-AS-APPEND",
 "Nothing deletes silently: removals are moves-to-tomb with receipts (claims organ already does this — generalize to every destructive act).",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "Claims today; general destructive ops candidate. Backup-first on ground-truth surgery is the standing kin.",
 "runtime",
 "mag/bay_organs.py tombstones (.expired-*); generalization pending",
 "FOLDED")
law("LAW-046","CAPABILITY-CHECKED-INBOXES",
 "An inbox drop without a valid handoff-gate row is invisible to the lane — unreadable by construction.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "Lane inboxes; structural hardening of LAW-037. Candidate (Unproven).",
 "prose",
 "lane inbox readers; MCP_MANIFEST_SPEC spawn gate",
 "ROUTED")
law("LAW-047","TIME-UNFAKEABLE-ROWS",
 "Receipts carry chain-anchored (RFC-3161-style) timestamps so 'when' cannot be backdated.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "Receipts/trails. Candidate; chain gives this nearly free but needs a design pass — SHELVED to the REEMBER shelf.",
 "prose",
 "verkle chain anchoring (design owed)",
 "SHELVED")
law("LAW-048","ASK-BUDGET-COUNTER",
 "A monotonic per-lane counter enforces the ask allocation: asking decrements it; the stall-ladder cannot see sanctioned asking as failure because the counter says it is sanctioned.",
 "watch/ARCHITECTURE_IS_LAW_20260904.md",
 "All lanes; resolves the LAW-038 vs stall-ladder dispute. Candidate (Unproven).",
 "prose",
 "scheduler/evals build",
 "ROUTED")

# --- Salon direction ---
law("LAW-049","RESTOCK-FIRST",
 "Food (genuinely new signal) is the binding constraint: research mandate is restock-first on NEW domains, archaeology secondary (orphans folded; rereading our own mail was a one-time recovery); sweeps retire at diminishing returns (shift-5+ theater).",
 "watch/SELF_STEAL_COMPANY_DESIGN_20260904.md",
 "Research lane mandate (salon-unanimous + economist concur with lane-scope caveat). Manifest edit pending.",
 "prose",
 "research manifest mandate flip; HUNGER_LEDGER instrument",
 "FOLDED")
law("LAW-050","WINDOW-PRIMARY-CLAIM",
 "One primary per work window, claimed by file: claim via atomic create with judge-then-CAS takeover and expiry-only lease (race-verified, 154 checks, 0 failures).",
 "watch/SALON_DAY_DIRECTION_20260904.md",
 "Night windows 23:00-09:00 and any multi-booked window; launch-law same-turn builders.",
 "runtime",
 "mag/window_throttle.py (BUILT 09-04, builder receipt-002)",
 "FOLDED")

# --- The normalizer itself ---
law("LAW-051","FOUR-VERB-STANDARD",
 "Every orphan/lesson/root gets all four verbs — WIRE (named consumer), TRANSDUCE (structure not prose), DISPOSE (FOLDED/TOMBSTONED/ROUTED/SHELVED, in the digest), SUBSTRATE (queryable/append-only/read-at-spawn); prose is the input format, never the storage format.",
 "watch/THE_NORMALIZER_20260904.md",
 "All normalization work (this run is its first enforcement). Disclosed: +1 beyond the mission's named source list.",
 "runtime",
 "THE_NORMALIZER standard; day digests; this lattice",
 "FOLDED")

assert len(L) == 51, len(L)
assert len(set(r["id"] for r in L)) == 51

reg = {"schema": "law_lattice.v1", "laws": L}
with open("queue/lanes/law_lattice.json", "w", encoding="utf-8") as f:
    json.dump(reg, f, indent=1, ensure_ascii=False)

entries = [dict(r, _key=r["id"]) for r in L]
export = {"schema": "lattice_logic.v1", "name": "law_lattice", "family": "registry",
          "source": "queue/lanes/law_lattice.json", "count": len(entries), "entries": entries}
with open("dashboard/static/lattices/law_lattice.json", "w", encoding="utf-8") as f:
    json.dump(export, f, indent=1, ensure_ascii=False)

print("rows:", len(L))
print("tiers:", dict(Counter(r["enforcement"] for r in L)))
print("dispositions:", dict(Counter(r["disposition"] for r in L)))
