# Cathedral combine — groq lane (openai/gpt-oss-120b)

*5ms, free/metered lane, CLARITAS-neutral system prompt*

**RIB_CATHEDRAL_WORLD_V1 – Combined World Specification**  

**1. Core Topology & Module Connections**  
All seven mag_game_module.v1 instances are stitched together on the persistent floor v0 (the “Atrium Hub”). Each module’s exit points have been re‑mapped to create a single directed graph that the player traverses linearly, while still allowing optional back‑tracking for side‑quests.

| From (module/room)                     | Exit label → | To (module/room)                               | Connection purpose |
|----------------------------------------|--------------|-----------------------------------------------|--------------------|
| `water_computer.gallery` (OUT tank)    | **flow** →   | `fractal_maze.field_entry` (scale‑1 field)    | Supplies the “gravity‑as‑computation” fluid that powers the maze’s bending field. |
| `fractal_maze.field_exit` (scale‑2)    | **gate** →   | `dnd_classic_stub.keep_entrance` (door)       | Opens the 14‑room keep once the player has aligned the field’s fractal vector. |
| `dnd_classic_stub.keep_exit` (tower)   | **stair** →  | `audit_dungeon.atrium` (north)                | The keep’s tower collapses into the Atrium, exposing the audit vault. |
| `audit_dungeon.dashboard_gallery` (north) | **arch** →   | `doctrine_library.lens_gate` (garage_gate)   | The ten‑lens gate opens only after the player has collected all audit “lenses” (see §3). |
| `doctrine_library.lens_gate` (garage_gate) | **portal** → | `riddler_optics.garage` (entry)               | Optics garage becomes accessible; lenses are physically placed here. |
| `riddler_optics.garage_exit` (exit)    | **bridge** → | `riddler_engram.session_hall` (door)          | Crossing the optics field triggers the engram session. |
| `riddler_engram.session_exit` (end)    | **gate** →   | `adventure_2d6_stub.river_ford` (gallery)     | The final engram unlocks the “gallery” exit that loops into the water‑computer’s gallery (see invariant in `adventure_2d6_stub`). |
| `adventure_2d6_stub.crossroads` (north) | **path** →   | `blob-double.level_1` (entry)                 | The 2d6 adventure’s “hill shrine” leads to the first Blob level. |
| `blob-double.level_3` (exit)           | **return** → | `water_computer.gallery` (IN tank)            | Completing all three Blob levels pushes the final duplicate‑push token back into the water‑computer, closing the resource loop. |

All other exits (south/east/west) remain internal to their modules for exploration but do not affect the main through‑line.

**2. Player Path (Canonical Play‑through)**  

1. **Water Computer – “The Reservoir”**  
   - Start in `water_computer.gallery`. Fill the OUT tank by solving the *fill sequence* (3‑step gravity‑computation puzzle). The tank’s fluid level becomes the **Computation Token** (CT).  

2. **Fractal Maze – “Bending Field”**  
   - Enter `fractal_maze.field_entry`. Use the CT to power the field; the player must align the fractal vector (scale‑1 → scale‑2) by rotating three concentric rings. Success opens `field_exit`.  

3. **D&D Classic Keep – “The Four‑Story Keep”**  
   - Walk through `keep_entrance` → 14 rooms, each containing a “code‑riddle” that yields a **Lens Fragment** when solved. The final tower room drops the **Key of Audit** (opens Atrium north door).  

4. **Audit Dungeon – “The Repo Atrium”**  
   - Navigate the Atrium, Mag Halls, Memory Warrens, Dashboard Gallery, Canon Docks, Doctrine Library, Deploy Graveyard, Inbox Lighthouse, Mine Shaft, and Git Vault.  
   - Collect **Ten Lens Fragments** hidden in the Dashboard Gallery (each ghost page contains a fragment).  
   - Resolve the “audit walk” by stamping 30 000 files; each stamp increments a global **Audit Counter** (AC). When AC reaches 30 000, the `lens_gate` unlocks.  

5. **Doctrine Library – “The Lying Number”**  
   - Deposit the ten Lens Fragments at the `lens_gate`. The gate opens to the Optics Garage.  

6. **Riddler Optics – “Ten‑Lens Optic Path”**  
   - Guide a light ray through ten lenses in a fixed order (mirrors, prisms, filters). The ray’s final exit yields the **Engram Token** (ET).  

7. **Riddler Engram – “Session Hall”**  
   - Use ET to start a ten‑seat session. Each seat represents a “phase” of the engram; completing all phases unlocks the `session_exit`.  

8. **Adventure 2d6 Stub – “Dusty Crossroads”**  
   - Enter via the gallery door; solve the crossroads riddle (answer: *shadow*). Follow the north path to the Hill Shrine, then east to the Market Ruin (defeat stray dog), west to River Ford (trigger invariant).  

9. **Blob‑Double – Levels 1‑3**  
   - Each level is a push‑duplicate puzzle (no slides). Success pushes a **Duplicate Token** (DT) forward. Level 3’s exit returns DT to the water computer.  

10. **Water Computer – “Final Convergence”**  
    - The returned DT merges with the original CT, forming the **Unified Computation Core** (UCC). The UCC automatically triggers the world‑reset event: all modules’ “exit refused” invariants are satisfied, and the cathedral’s doors open to the “Exit Hall” (a simple win screen).  

**3. Shared Resource Loop (The Computation Cycle)**  

- **CT (Computation Token)** – generated in Water Computer by the fill‑gravity puzzle.  
- **CT → Fractal Maze** – powers the field; each successful scale crossing consumes 1 CT unit and returns 0.5 CT (energy loss).  
- **CT → Blob‑Double** – each level consumes 1 DT; upon completion DT is returned to the Water Computer, converting into 0.8 CT.  
- **CT + AC (Audit Counter)** – when AC reaches 30 000, a “Law of Conservation” invariant grants a bonus +5 CT to the player.  
- **CT + ET (Engram Token)** – the Engram session consumes 2 CT to finalize the session, producing the ET.  
- **ET → Optics** – the ray’s traversal consumes ET, returning a **Lens Charge** (LC) that fuels the Doctrine Library gate.  
- **LC → Doctrine Library** – ten LC unlock the lens gate, allowing the player to deposit Lens Fragments.  

The loop closes when the final DT from Blob‑Double is merged back into the original CT, producing the **UCC**. The UCC is the single shared resource that validates all “exit‑refused‑until‑condition” invariants across modules, guaranteeing a coherent end‑state.

**4. Water Computer’s Global Computation**  

The Water Computer implements **Gravity‑as‑Computation (G‑C)**: each unit of water in the OUT tank represents a binary digit (0 = empty, 1 = filled). The fill sequence (three chambers, each with a valve) encodes a 3‑bit number **N** (0‑7).  

- **N** is interpreted as a *rule‑index* for the world’s procedural narrative.  
- **Rule‑0**: “All doors open after 3 minutes.”  
- **Rule 1**: “Every Lens Fragment spawns a minor enemy.”  
- **Rule 2**: “Audit stamps double AC gain.”  
- **Rule 3**: “Optics ray splits, creating a duplicate token.”  
- **Rule 4**: “Blob‑Double levels require an extra push.”  
- **Rule 5**: “Riddler Engram phases shuffle order.”  
- **Rule 6**: “2d6 adventure’s riddle answer changes to *echo*.”  
- **Rule 7**: “Final UCC grants a permanent +1 to all dice rolls.”  

When the player first fills the tank, **N** is recorded in the world state. All subsequent module mechanics reference this rule set, ensuring the seven modules behave as a single, rule‑coherent cathedral. The final UCC overrides **N** with Rule 7, rewarding the player with a permanent meta‑bonus.

**5. Victory Condition**  

- All ten