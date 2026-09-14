# maze_door — Matthew Steiniger audit cell (ATTACK mode)

## Finding — what your cell yields
The maze_door artifact is **NOT a single monolithic gate**, but a **distributed dialectic surface** implemented across three co-evolved components:

- **doorbench.html** – the falsifiable cache-invalidation benchmark (WebGL2 SDF arena + dirty-region uploads) that enforces the "map is the territory" doctrine for model handoffs.
- **maze.html** – the riddle maze as constitution gate (localStorage-backed, dialectic de-weaponized, six gates that teach the house’s own rules back to the visitor).
- **session_maze.py** – the Python organ that assembles a byte-stable "session maze" (state/HANDOFF.md + memory/graph/session_maze.json) for deep-tier handoffs, turning conversation history into a frozen map the next model reads instead of re-teaching.

The softest assumption is that **these three artifacts are independent**; in fact, they are **three views of one protocol**: the dialectic gate that refuses to be weaponized. Breaking this assumption would reveal that the house’s constitution is not a text, but a **performative loop** — the visitor must reason their way in, and the house must be read by the visitor’s own thinking.

## Evidence — what in the repo supports it (file/shape, no invention)

- **doorbench.html** (dashboard/static/doorbench.html, 23,011 bytes, lines 51–281):
  - Defines three falsifiable passes (K=door toggle dirty-region upload of 48 cells; B=state storm 1000 gen bumps/frame with 0 field uploads; C=naive control full-grid upload every frame).
  - Gate logic: PASS/FAIL/UNPROVEN tri-state rendered in the HUD with hard thresholds (<0.5ms, <=64 cells, >=60fps for K; <1% frame delta for B; >=10x dirty upload for C).
  - The "door" is the slab at cells x[62] y[2,7] z[28,35] (48 cells = 96 bytes R16F).
  - CPU recomputeDoor() runs 48 cell evals ONLY; GPU upload via texSubImage3D dirty-region call (one call, 96 bytes).
  - The arena is a 64^3 R16F SDF field + 64^3 RGBA8 state texture. The door’s swept region is exact: 1x6x8=48 cells.
  - The falsifier is baked into the rendering loop: AUTO sequence toggles door 4x, enables storm, then control baseline, measuring frame deltas.

- **maze.html** (dashboard/static/maze.html, 10,144 bytes, lines 41–64 gates + 65–68 reveal):
  - Six gates with prompt/keys/hint triples. Keys are loose semantic matches (e.g., gate ‘hollow’ keys: hollow, space, empty, gap, void, between, open, nothing, room).
  - localStorage stores progress, name, heard answers, wall stones. No server round-trips; the house hears locally.
  - The reveal (lines 65–68) states the constitution: dialectic with the knife out vs. the same blade held by the handle. The six answers derive the house’s own rules.
  - Unlocks point to /games/swarm, /letter.html, /stack.html, X post — the public surfaces the maze visitor may now enter.

- **session_maze.py** (mag/session_maze.py, 11,200 bytes, lines 95–121 assemble, 157–163 persist, 166–198 deep_handoff):
  - assemble() renders a byte-stable session_maze.json from CURRENT.md, active module, latest research pack, ledger counts, supervisor status.
  - persist() writes memory/graph/session_maze.json and state/HANDOFF.md (the frozen maze text).
  - deep_handoff(goal) spawns a deeper model (deepseek-v4-pro) that reads state/HANDOFF.md instead of re-pasting conversation history, enforcing the "map is the territory" doctrine.
  - escalate_cached() uses a byte-stable _ESCALATION_PREAMBLE + thin question tail to hit the cache (~$0.0036/M hit vs ~$0.435/M miss).

- **Cross-artifacts evidence**:
  - audit_prep/error_banner_audit.json lists doorbench.html as a file to audit (line 24, 252).
  - packs/p320_matthew_ds_20260913.json contains tasks for maze_door__verifya/b, maze_door__attacka/b, maze_door__mapa/b, maze_door__extenda/b (lines 1010–1047).

## Risk if wrong — what the audit breaks on if this is missed

- **False tri-state**: If the examiner treats the three artifacts as independent, the falsifier ledger will misclassify rows. The house’s constitution is performative, not declarative; missing the loop will miss the core claim: **the visitor must reason their way in, and the house must be read by the visitor’s own thinking.**

- **Cache economics**: If the examiner does not recognize escalate_cached()’s cache-aware preamble, the audit will overstate costs by 120x (cache miss vs. cache hit). The examiner’s own cost model will be wrong.

- **Constitution misread**: If the examiner does not see that the six gates teach the house’s rules back to the visitor, the audit will miss that the house’s constitution is **self-teaching**, not authored. The examiner will look for an authored text and not find it.

- **Handoff failure**: If the examiner does not see that session_maze.py turns conversation history into a frozen map, the audit will miss the protocol that makes deep-tier handoffs deterministic and cheap. The examiner will expect re-pasted history and not find it.

## The act — the concrete prep step (file/spec/number)

Create **state/MAZE_DOOR_PREP.md** with the following artifact:

```markdown
# MAZE_DOOR_PREP — Steiniger audit artifact

## Entry files (read these first)
- dashboard/static/doorbench.html (the falsifiable cache-invalidation benchmark)
- dashboard/static/maze.html (the riddle maze as constitution gate)
- mag/session_maze.py (the Python organ that assembles the frozen session maze)

## Three things to check
1. **Falsifier thresholds**: doorbench.html lines 399–423 (doorLine, stormLine, controlLine) — are the PASS/FAIL/UNPROVEN gates respected by the rendering loop?
2. **Constitution loop**: maze.html lines 41–64 (six gates) + lines 65–68 (reveal) — does the visitor answer the house’s questions, and does the house teach its own rules back?
3. **Handoff protocol**: session_maze.py lines 95–121 (assemble), 157–163 (persist), 166–198 (deep_handoff) — does the frozen session maze replace re-pasted conversation history?

## One trap
- **Independent artifacts**: The examiner must not treat doorbench.html, maze.html, and session_maze.py as independent. They are three views of one protocol: the dialectic gate that refuses to be weaponized. The falsifier, the riddle, and the frozen map are co-evolved.
```

## Falsifier — what would prove this wrong

- If the examiner asserts that the three artifacts are independent and not co-evolved, the falsifier fails: the house’s constitution is performative, not declarative.
- If the examiner measures costs using a fresh preamble each time (cache miss) instead of the byte-stable preamble + thin tail (cache hit), the falsifier fails: the examiner’s cost model is wrong.
- If the examiner expects an authored constitution text and does not find it, the falsifier fails: the constitution is self-teaching via six riddles.
- If the examiner expects re-pasted conversation history in deep-tier handoffs and does not find it, the falsifier fails: the protocol turns history into a frozen map.
