# EXTERNAL STEAL — the Desk/DEP/AOS corpus (two-way, 2026-09-17)

*Source: four documents + growth log + S-001 audit from the sibling sovereign-kit lineage
("Desk — Dual-Venue Trading Control Plane", "Possible Worlds Not Panic" Amendment 0
monograph, "Tool Lifecycle for Agentic Systems Vol 5", "Session Zero Growth Log", "MAG
Socratic Control-Surface Audit S-001", Keystone skill). Operator order: steal both ways,
no sacred cows, keep core structures, x3 iterations touching everything.*

## WHAT THEY EXECUTE BETTER (steal — no sacred cows)

1. **The typed control surface** (S-001 A1/A2/A6/A7/A10). Our receipts and gates are
   CONVENTIONS; theirs are proposed TYPES: EvidenceRef, Claim, Decision, Capability,
   ActionRequest, ActionReceipt, StateMutationReceipt. Their finding A10 confirms OUR
   defect: mag/registry.py does read-modify-write with no locking — lost updates are
   possible tonight. **ADOPT: S-001 Phase 0-1 — build CONTROL_SURFACE_AUDIT (observe-only
   inspector) then wrap write_file with typed ActionRequest→Capability→ActionReceipt.**
   This is also the Elder pass-2 meter: typed receipts are the instrument the audit demanded.
2. **UNCERTAIN as a load-bearing state + evidence classes** (Amendment 0). Four classes
   (NON_AUTHORITATIVE / EVENTUALLY_CONSISTENT / AUTHORITATIVE_POSITIVE / NEGATIVE) govern
   whether the possible-world set may shrink; exit from UNCERTAIN is never "silence means
   absence." Our effect semantics have UNKNOWN but no evidence ladder. **ADOPT: the
   evidence-class table verbatim into the effect broker contract (HOLD-3 crosswalk).**
3. **Conformance report, not trophy run** (Amendment 0 §adversary): "if it passes we have
   proven" is STRUCK; the artifact is version hashes, seeds, explored states, coverage,
   minimized counterexamples, explicit assumptions. **ADOPT: gate receipts carry this
   shape (our BFS gate already produces seeds+states — add coverage + assumptions lines).**
4. **Tool lifecycle + tombstone** (Vol 5): six stages (proposed/alpha/beta/stable/
   deprecated/retired), per-tool manifests (owner, last_reviewed, successor, contract),
   review cadence, retirement log never deleted. Our tools have no stages and no
   tombstones. **ADOPT: manifests for the drive/librarian/gate trio first.**
5. **Role-conditioned rendering**: one renderer, role configs as data, no per-role forks;
   "if a role needs different facts that is a different query." **ADOPT for the dashboard
   surfaces (operator vs stranger vs seat views of the same ledger).**
6. **Keystone's exemplar-driven development**: modules derive from hardened exemplars;
   dedup/vetting before status. Already our ruins_go→new-games pattern — NAME it as law.

## WHAT WE EXECUTE BETTER (keep — the core structures)

- **Free-lane economics at fleet scale** (26 lanes, stealth rotation, law-15 pacing,
  U8-measured concurrency) — their corpus prices compute; ours operates it at $0.
- **The evolution loop with an EXACT gate** — BFS solvability beats rubric-judged
  promotion; 9-for-9 on the decoration tier.
- **The games estate itself** — 8 shipped games with harnesses; their corpus has specs.
- **Hash-chained verification in production** (grounding_wave, verkle) — their S-001
  audit notes our cryptographic primitives EXIST and are merely un-joined to action
  receipts (their A11). The join is the steal, not a rebuild.
- **The Librarian/imprint cold-load** — no analogue in their corpus.

## THE MERGE LAW (core structures kept, boundaries typed)

Their §VIII names us: "Desk is a hostile laboratory for a more general side-effect
protocol." Ours is the general protocol; theirs stress-tested it in the domain where a
wrong story is priced in minutes. The lineage they fixed — INTENT → COMMITMENT → ATTEMPT
→ MANIFESTATION → CONSEQUENCE → OBSERVATION → BELIEF → possible-world set → UNCERTAINTY
BUDGET → RECONCILIATION — is our grounding_wave with the gaps filled.

## BUILD ORDER ADOPTED (S-001 dogfood sequence, fleet-adapted)

- Phase 0: CONTROL_SURFACE_AUDIT inspector (observe-only, no blocking).
- Phase 1: wrap write_file with typed ActionRequest→Capability→ActionReceipt
  (pre/post hashes captured).
- Phase 2: critic/gates read receipts (a write is not an outcome).
- Phase 3: registry mutations → StateMutationReceipt with version+hash (kills A10).
- Phase 4: join receipt roots to the verkle chain.
- Phases 5-7: skill beads as candidates; shell/python surface; dashboard mutators.

*This receipt is the Elder pass-2 meter list. Pass 2 re-audits WITH these instruments.*
