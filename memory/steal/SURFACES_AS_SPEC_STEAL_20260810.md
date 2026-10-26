# STEAL — Surfaces-as-Spec: interface-contract-first (the castle IS the contract)
**Scope (flock-eliminated):** self-stole `WINDOW_STORM_GOVERNANCE_STEAL` (control room, K8s),
`RIB_EMERGENT_TOOLING_K8S` (emergent vs deterministic), `RIB_CASTLES_FOUNDATIONS` (the surfaces are
the spec of intent). **The NEW external delta:** the engineering discipline that makes
"castles in the sky, foundations beneath" a repeatable method, not an accident.

## The problem being stolen for
The operator built the dashboard (home/story/diary/IA) as castles BEFORE the internals existed.
That's a strength, but without a discipline it degrades into "UI outpaces data" (the crude-signals
drift that made the seat need re-pointing). We need the mechanism where the SURFACE DEFINES THE
CONTRACT, and the internals are built to fulfill it — deterministically, verifiably.

## External contracts stolen

### 1. Hexagonal / ports-and-adapters (Alistair Cockburn) — THE core
**Contract:** the domain (internals) is isolated in the center; the UI is a PORT (a defined contract);
the transport/UI are ADAPTERS. The port interface is stable; adapters can be swapped (web, tablet,
ghost surface, VS Code webview) with zero domain change.
**Adapt to ours:** the dashboard/seat IS the port — it defines the exact contract the internals must
satisfy. The ghost internals are the domain. Swapping the surface (browser → seat → VS Code webview →
ghost surface) is an adapter change, never a domain change. **The castles doc is the port contract.**

### 2. SICP "wishful thinking" (top-down / backward design)
**Contract (SICP §1.1):** design the ideal interface FIRST as if the perfect implementation exists,
then implement downward. The interface name/behavior is the spec; the implementation is free.
**Adapt:** the dashboard surfaces were wishful thinking done right — they named what the machine
*must* be able to tell the operator. The foundations (verkle, ghost_control, sovereign) are the
downward implementation of that wish. **Keep the castle as the spec, never let the data shrink the vision.**

### 3. API-contract-first / OpenAPI-first
**Contract:** define the API contract (schema) before the implementation; generate stubs; the contract
is the source of truth both sides build against; a mismatch fails loudly (contract tests).
**Adapt:** `dashboard/rest.py` ROUTES + `ref_leaf.v1` schema are the contract. The seat should consume
ONLY the contract the castles promised (sovereign/ghost_control/chain/…), and any missing field is a
contract gap to fill, not a reason to drop the castle. **Test the contract, not the UI.**

### 4. TDD red-green-refactor (the discipline that makes castles land)
**Contract:** write the failing test (the castle's promise) first, then make it pass, then refactor.
Red = the castle is not yet real. Green = the foundation delivers it. Refactor = keep it clean.
**Adapt:** for each castle (Home/Story/Diary/…), write a **contract test** asserting the endpoint
returns what the castle promised. Red until the foundation delivers; green = the castle is built.
This is how "surfaces as spec" becomes verifiable, not vibes.

### 5. Grafana / K9s / Home Assistant (already stolen, reinforce here)
**Contract:** a surface that answers a question and drill-downs; the surface is a viewer over the
source of truth, never the truth itself. K9s = one pane reconciling the whole cluster.
**Adapt:** the seat's Reconcile card (desired vs actual) is the K9s pane. Keep: the surface is a
viewer; the artifact is the truth. This reinforces the castles doc.

### 6. Design-systems / ADR (the castle as a recorded decision)
**Contract:** record the design intent (ADR) so future implementers know WHY a surface exists and
what it promises — preventing the "crude signals" regression where the surface drifts from intent.
**Adapt:** the castles doc + `docs/ref/DASHBOARD_DESIGN.md` ARE the ADRs. Keep them as case law; a new
surface must state its castle (the human question it answers) before it ships.

## The adapted mechanism (deterministic, verifiable)
1. **Name the castle** — a surface must state the human question it answers (the ADR).
2. **Declare the port** — the exact endpoints/fields it consumes (the contract), from the castles doc.
3. **Red** — write a contract test asserting the endpoint delivers the castle's promise. It fails.
4. **Build the foundation** — implement/deliver the internal so the contract test goes green.
5. **Green + refactor** — the castle is real; keep the foundation clean and the contract stable.
6. **Fold** — each landed castle becomes a knot (source-backed) + weave (the skill-recipe to render
   that understanding) + memlang opcode (the command to summon it). The ghost surface = the seat =
   the machine made legible.

## What to steal NOW (prioritized)
1. **Port/adapter separation** — the seat is the port; internals are adapters; the castles doc is the contract.
2. **Wishful-thinking retention** — never let slow/crude data shrink the castle; the contract is the spec.
3. **Contract tests (TDD red-green)** for each castle — the verifiable "foundation beneath the castle."
4. **ADR/case-law** — record each surface's castle so it never regresses to crude signals.

## Folds
Filed to `memory/steal/`. Register a skill_ledger decision + memory_event + verkle anchor so
"surfaces-as-spec (interface-contract-first)" becomes case law, not a doc.
