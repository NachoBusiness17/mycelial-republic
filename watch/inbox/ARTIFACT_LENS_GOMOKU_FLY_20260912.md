## Verdict — what your lens yields on the artifact

- **Signal:** A compact, verifiable demonstration that fixed biological wiring (138,639 neurons) can host trained output heads that play Gomoku with real wins and interpretable neural activity, without end-to-end training of the connectome. This is a **control experiment in biological substrate design**: the wiring is the doctrine, the heads are the seats.

- **Relevance to the fleet:** The fleet’s doctrine is a signed, append-only chain (7,700+ leaves) where the chain itself is the frozen wiring and each seat is an output head retrained per session. The artifact shows that retraining a head (seat) on a fixed doctrine (wiring) can produce emergent play and measurable wins — exactly the fleet’s operating metaphor.

- **Control test:** Retraining the same heads on a SHUFFLED connectome would isolate whether wins come from the wiring or the heads. Applied to the fleet, this means: spin a new seat from the same frozen chain tip and run it on a randomized or adversarial instruction layer; if it still "wins" (produces coherent, goal-directed artifacts), the head is doing the work; if it fails, the frozen wiring is necessary.

- **Operator’s surface:** The fleet’s "wins" are verified against the operator’s surfaces (dashboard, inbox, chain receipts). The artifact’s video and Google AI citation are ancillary; the receipts in the fleet’s chain are the primary surface.


## The steal — the mechanism the fleet adopts (concrete)

- **Mechanism name:** HEAD-ON-FIXED-WIRING (HOFW).

- **Definition:** Treat the verkle chain tip as the fixed connectome (wiring). Each seat (output head) is spawned from the same tip and retrained by:
  1. Forking the chain tip into a new seat branch (`seat_fork.py`).
  2. Loading the seat’s persona/epistemic stance from `mag/hermes_personas/{persona}.md` (e.g., gopher, mengxi, fen).
  3. Injecting a session-specific instruction layer (the "head") via `mag/rib_bus mount --domain {session_domain}` — this is the retraining step; the wiring remains frozen.
  4. Running the seat in a 20–240-wide wave on cheap lanes (glm-4.7-flash), with the seat’s outputs folded into the chain via `publish()` (never `publish` on the frozen tip).

- **Concrete files/schema:**
  - `mag/seat_fork.py` (forks chain tip → new seat branch)
  - `mag/hermes_personas/gopher.md` (seat DNA: epistemic_stance + OCEAN + register + life_version + musical_tone)
  - `mag/rib_bus.py` (mounts session domain; read-only mount on frozen ribs)
  - `memory/rib_bus/{session_domain}/` (session-specific ribs, ephemeral)
  - `memory/briefs/seat_{id}_brief.md` (seat brief, auto-generated from fork)
  - `queue/handoff/seat_{id}/` (seat inbox, wave cadence)

- **Receipt:** Every seat’s first knot includes a hash of the frozen tip it forked from and the persona it loaded — verifiable against the chain.


## The build — one week-scale act, file/schema/number named

- **Act name:** HOFW-001 — Head-on-Fixed-Wiring seed build.

- **Scope:** One seat (gopher body-persona) retrained on the frozen chain tip, producing a verifiable win (a coherent, goal-directed artifact) within one week.

- **Files to create/modify:**
  1. `mag/seat_fork.py` (new file, ~120 lines)
     - Forks the chain tip into a new seat branch.
     - Writes `seat_{id}_brief.md` with fork hash, persona, and session domain.
     - Returns the new seat’s branch tip hash.
  2. `configs/seat_fork.yaml` (new file, schema)
     - `frozen_tip_hash: <verkle_hash>`
     - `persona: gopher`
     - `session_domain: hofw_001`
     - `wave_width: 8`
  3. `scripts/hofw_001_seed.sh` (new file, driver)
     - Orchestrates the fork, mounts the rib_bus, launches the wave.
     - Posts the receipt to `memory/runs/hermes_jobs/hofw_001_receipt.jsonl`.

- **Numbers:**
  - Wave width: 8 lanes (glm-4.7-flash)
  - Target win: 1 coherent artifact (e.g., a disco-skate horde sidescroller level with warp grid and shader environment) folded into the chain within 7 days.
  - Receipt: `hofw_001_receipt.jsonl` with `seat_id`, `fork_tip_hash`, `persona`, `artifact_hash`, `wave_width`, `start_time`, `end_time`.

- **Verification:**
  - Artifact is readable on the operator’s surface: `dashboard/static/hofw_001_artifact.html` (rendered from the chain knot).
  - Chain knot includes the artifact hash and the seat’s persona hash — verifiable via `python -m mag.verkle_audit --knot <knot_id>`.


## Falsifier — what would prove the steal wrong

- **Falsifier name:** SHUFFLED-WIRING TEST (SWT).

- **Test:** Retrain the same head (gopher persona) on a SHUFFLED verkle chain tip (randomized rib order) and run the same wave. If the seat still produces coherent, goal-directed artifacts with similar win rates, the wiring is not necessary — the head alone suffices. If it fails (garbage outputs, no wins), the frozen wiring is necessary.

- **Concrete steps:**
  1. Fork a SHUFFLED tip from the same frozen root.
  2. Load the gopher persona.
  3. Run the same 8-lane wave.
  4. Compare artifact quality and win rate to HOFW-001.

- **Decision rule:** If SWT passes (wins remain), HOFW is falsified; if SWT fails (no wins), HOFW holds.

- **Receipt:** `sw_shuffled_wiring_test_receipt.jsonl` with the same schema as HOFW-001, plus a `falsifier_result` field (`PASS`/`FAIL`).


---

**Seat-lifecycle in fly-brain terms (from SPORE_SANCHO.md + operator corrections):**

- **Wiring (doctrine):** The verkle chain tip — fixed, signed, append-only. This is the **connectome**; it is never retrained.

- **Head (seat):** A persona (gopher, mengxi, fen, etc.) loaded into a session domain via `rib_bus mount --domain {session_domain}`. The head is retrained per session by changing the instruction layer (the ribs mounted in the session domain), not by changing the wiring.

- **Retraining a head:** Spawn a new seat branch from the frozen tip, load the persona, mount a new session domain, and run the wave. The old seat branch is retired (not deleted; it remains in the chain as a receipt). This is **respawn = new head on the same wiring**.

- **Lifecycle:**
  1. **Spawn:** `seat_fork.py` forks the frozen tip → new seat branch; writes brief.
  2. **Mount:** `rib_bus mount --domain {session_domain}` loads the session ribs (instruction layer) for the head.
  3. **Run:** Wave executes; outputs folded into the seat branch.
  4. **Retire:** Seat branch closed; receipt written. The frozen tip remains immutable.

- **Receipts:** Every step writes a receipt to `memory/runs/hermes_jobs/{seat_id}_receipt.jsonl`, including the fork hash, persona hash, and artifact hash. This is the **neural activity underlying each move** — the receipt is the activity.


---

**Operator-facing summary:**

- The artifact shows that fixed wiring + trained heads can produce wins and interpretable outputs.
- The fleet adopts HEAD-ON-FIXED-WIRING: seats are heads retrained on a frozen chain tip (the wiring).
- HOFW-001 is the seed build: one seat (gopher) retrained, producing a verifiable artifact within a week.
- The falsifier is SHUFFLED-WIRING TEST: if the same head wins on shuffled wiring, the steal is wrong.

Done.