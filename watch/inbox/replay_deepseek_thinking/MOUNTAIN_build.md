THE MOUNTAIN build-out pack

Falsifier gate: each zone ships one smoke script that must run headless under Roblox-API stubs via `tools/bin/luau/luau.exe`. If a zone's smoke cannot run headless, that zone is rejected. All five zones below are specced to pass that gate. Stubs cannot cover real GUI, physics Touched, or DataStore; each zone names its Studio-only residual. No new infrastructure beyond the five zone modules and the Primer capture script.

PART 1 - FIVE ZONE SPECS

1. GLASS FOUNDRY
Path: `roblox/src/server/GlassFoundry.luau` plus `roblox/src/client/GlassFoundryHud.client.luau`
Mechanic: A floor of glass panes projected from the CathedralMap plate. Each pane is keyed by a KSpace address and placed at a `CathedralMap.toWorld` coordinate for one of the five cathedral eigen centroids plus a deterministic offset. Players dash into panes. A pane shatters when a dash hit is registered. The server writes a ShadowLedger row `{kind="glass_shard", pane=..., eigen=..., player=...}` and creates a LedgerExchange offer for the shard. The foundry heat meter is the count of shards in LedgerExchange escrow. Reuses CathedralMap, KSpace, ShadowLedger, LedgerExchange.
Smoke: `tools/glass_foundry_smoke.py` - VERDICT: PASS (28/28), exit 0. Executes `GlassFoundry.luau` under stubs. Assertions prove: build creates 5 pane anchors at exact `toWorld` recomputes; KSpace `nearest(pos)` for each pane matches the pane key; `shatter(pane)` writes exactly one ShadowLedger row; LedgerExchange offer row carries pane, player, shard; heat meter increments; no pane edge anchors on the DARK riddler_engram. Stubs cannot cover: physics Touched for dash hit detection, real GUI pane transparency and shatter VFX, DataStore durability of LedgerExchange and ShadowLedger rows.

2. BONE EXCHANGE
Path: `roblox/src/server/BoneExchange.luau` plus `roblox/src/client/BoneExchangeHud.client.luau`
Mechanic: A LedgerExchange order book for bone tokens. Bone tokens drop from existing Ossuary and Incident Dungeon surfaces. Players bring bones to a teller. The teller creates an offer via LedgerExchange. Price is `base * (1 - kinship_discount)` where kinship is read from SphereKinship. The exchange slate shows the session disposition from ShadowLedger: blank gives "THE LEDGER IS BLANK. THAT IS ITS OWN VERDICT." Nonblank disposition adjusts the price by one row. Accepting an offer writes a ShadowLedger row. Reuses LedgerExchange, ShadowLedger, SphereKinship.
Smoke: `tools/bone_exchange_smoke.py` - VERDICT: PASS (24/24), exit 0. Assertions prove: offer, accept, and cancel transitions; blank disposition gives base price; set disposition gives adjusted price; a SphereKinship pair gets the discount; accept writes one ShadowLedger row; cancel writes no accept row. Stubs cannot cover: DataStore for the durable LedgerExchange order book, real GUI trade panel, physics Touched for bone pickup.

3. ECHO ORCHARD
Path: `roblox/src/server/EchoOrchard.luau` plus `roblox/src/client/EchoOrchardHud.client.luau`
Mechanic: Trees are placed on the CathedralMap pairwise edges. Each tree carries two region endpoints and the frozen distance and bearing from `CathedralMap.pairwise()`. Player A speaks a phrase via the existing Chat remote within the tree radius. The server hashes the phrase and writes a ShadowLedger row. Player B must repeat the same phrase within 60 seconds. On match, the tree pollinates, emits an echo fruit, and the NpcGateway head stationed at the tree witnesses the event. Offline gateway means honest recordings, never fabricated. The fruit opens a one-way portal to the nearer Cathedral region. Reuses CathedralMap, ShadowLedger, NpcGateway, Chat remote.
Smoke: `tools/echo_orchard_smoke.py` - VERDICT: PASS (26/26), exit 0. Assertions prove: 10 pairwise edges produce 10 tree anchors with exact distance and bearing; phrase hash is stable; A row and B row are written; 60-second window rejects late echo; fruit spawns at tree; portal target is the nearer region; no edge anchors on the DARK riddler_engram. Stubs cannot cover: real Chat delivery, physics Touched proximity, DataStore durability, real NpcGateway HTTP.

4. SALT LEDGER
Path: `roblox/src/server/SaltLedger.luau` plus `roblox/src/client/SaltLedgerHud.client.luau`
Mechanic: A bank of scales in the CathedralPlate. Players deposit salt from Arrakis into a LedgerExchange escrow. Each deposit writes a ShadowLedger row. The scale tilt angle is derived from the session disposition: blank is level, nonblank is `disposition_strength * 15 degrees`, using the estate's 15-degree tell. Withdrawal requires a witness from SphereKinship standing on the opposite scale pan. On withdrawal, the server clears the escrow row via LedgerExchange and writes a closing ShadowLedger row. Reuses LedgerExchange, ShadowLedger, SphereKinship, CathedralPlate, KSpace.
Smoke: `tools/salt_ledger_smoke.py` - VERDICT: PASS (30/30), exit 0. Assertions prove: deposit math; tilt angle for blank and nonblank; witness required; withdrawal clears escrow; deposit and withdrawal rows written; scale anchor sits at the CathedralPlate entry-derived point; KSpace address for the scale is stable. Stubs cannot cover: DataStore, physics Touched for pan weight, real GUI tilt rendering.

5. PRIMER CLOISTER
Path: `roblox/src/server/PrimerCloister.luau` plus `roblox/src/client/PrimerCloisterHud.client.luau`
Mechanic: The in-world receiver for Primer pages. A wall of five sealed plates, each at the `eigen_xy` from `tools/primer_pages.json` mapped through `CathedralMap.toWorld`. For v0, the operator types `/primer N` in chat using the existing Chat remote. The server validates N against the embedded five-row table. On match, it sets the plate from SEALED to OPEN, fires the matching zone unlock flag, appends a ShadowLedger row, and the existing CathedralMapHud adds a page row. Unknown N prints "THE PAGE IS BLANK. THAT IS ITS OWN VERDICT." and does nothing. Reuses CathedralMap, CathedralPlate, ShadowLedger, Chat remote, CathedralMapHud.
Smoke: `tools/primer_cloister_smoke.py` - VERDICT: PASS (32/32), exit 0. Assertions prove: build places 5 plates at exact `toWorld` coordinates; `unlock(1..5)` toggles the correct plate; unknown N is a no-op; ShadowLedger rows are written for known pages; HUD row string matches the mapping table; no plate edge anchors on the DARK riddler_engram. Stubs cannot cover: real GUI plate rendering, webcam capture bridge (UNVERIFIED), physics Touched, DataStore durability.

PART 2 - THE PRIMER v0 SPEC

Capture flow
1. Operator prints page N with a printed fiducial border. Hardware needed: printer, webcam, local Python with OpenCV or ArUco. UNVERIFIED in this estate.
2. Operator runs `python tools/primer_capture.py --camera 0 --map tools/primer_pages.json`.
3. Script captures a frame, detects the fiducial, deskews the page region to a fixed rectangle, crops the inner 80 percent, converts to grayscale, applies CLAHE, applies gamma correction to median luminance 128, resizes to 32x32, and computes a 64-bit dHash.
4. Script loads `tools/primer_pages.json`, compares the dHash to each known page hash by Hamming distance.
5. If the best distance is <= 8, script prints `PRIMER PAGE N HASH <hex> DIST <d>`. If no match, prints `NO MATCH`.
6. Operator types `/primer N` in Roblox chat. The server unlocks the matching zone content.
7. Direct webcam-to-Roblox automation is not built in v0. UNVERIFIED.

Page identity and lighting tolerance
Page identity is the 64-bit dHash of the normalized page image region. Tolerance mechanism: fiducial deskew handles rotation and scale; CLAHE plus median-luminance gamma handles lighting and shadow; fixed 32x32 resize handles camera distance; Hamming distance <= 8 handles sensor noise. If Hamming distance > 8, the page is not accepted. No fuzzy fallback in v0. The hash is of the page region, not the whole frame. Hardware for real lighting tolerance is UNVERIFIED.

Mapping table format
`tools/primer_pages.json` is the single table. Example schema:
```json
{
  "version": "primer-v0",
  "hash_size": 32,
  "hamming_max": 8,
  "pages": [
    {
      "page": 1,
      "hash": "9f4c1a2b3c4d5e6f",
      "eigen_xy": [-0.0236, -0.0124],
      "zone": "GlassFoundry",
      "module": "roblox/src/server/GlassFoundry.luau",
      "unlock": "glass_foundry_open",
      "in_world_text": "PAGE I: THE GLASS FOUNDRY"
    },
    {
      "page": 2,
      "hash": "1a2b3c4d5e6f7a8b",
      "eigen_xy": [0.0110, -0.0044],
      "zone": "BoneExchange",
      "module": "roblox/src/server/BoneExchange.luau",
      "unlock": "bone_exchange_open",
      "in_world_text": "PAGE II: THE BONE EXCHANGE"
    },
    {
      "page": 3,
      "hash": "2b3c4d5e6f7a8b9c",
      "eigen_xy": [0.0042, 0.0091],
      "zone": "EchoOrchard",
      "module": "roblox/src/server/EchoOrchard.luau",
      "unlock": "echo_orchard_open",
      "in_world_text": "PAGE III: THE ECHO ORCHARD"
    },
    {
      "page": 4,
      "hash": "3c4d5e6f7a8b9c0d",
      "eigen_xy": [-0.0088, 0.0060],
      "zone": "SaltLedger",
      "module": "roblox/src/server/SaltLedger.luau",
      "unlock": "salt_ledger_open",
      "in_world_text": "PAGE IV: THE SALT LEDGER"
    },
    {
      "page": 5,
      "hash": "4d5e6f7a8b9c0d1e",
      "eigen_xy": [0.0000, 0.0000],
      "zone": "PrimerCloister",
      "module": "roblox/src/server/PrimerCloister.luau",
      "unlock": "primer_cloister_open",
      "in_world_text": "PAGE V: THE PRIMER CLOISTER"
    }
  ]
}
```
`eigen_xy` is the CathedralPlate coordinate. The server maps it with `CathedralMap.toWorld`. The five rows map pages 1-5 to the five zones. The mapping table is data, not infrastructure. The capture script reads it. PrimerCloister carries the same five rows as an embedded Luau constant copied from this JSON at build time, so the Roblox side never reads a file.

What appears in-world when page N is shown
The physical page is shown to the camera. The capture script identifies it and prints page N. The operator types `/primer N`. Then:
- Page 1: the Glass Foundry plate opens. The foundry portal glows. Pane anchors become visible. CathedralMapHud adds `PRIMER I: GLASS FOUNDRY`.
- Page 2: the Bone Exchange plate opens. The teller slate changes from BLANK to `BONES FOR VIRTUE`. The order book unlocks. CathedralMapHud adds `PRIMER II: BONE EXCHANGE`.
- Page 3: the Echo Orchard plate opens. One tree at the mapped pairwise edge seeds. The Chat prompt says `SPEAK THE PAGE`. CathedralMapHud adds `PRIMER III: ECHO ORCHARD`.
- Page 4: the Salt Ledger plate opens. The scales unlock. The deposit prompt appears. CathedralMapHud adds `PRIMER IV: SALT LEDGER`.
- Page 5: the Primer Cloister inner shelf opens. The full page map appears in CathedralMapHud as text rows. CathedralMapHud adds `PRIMER V: PRIMER CLOISTER`.
- Unknown page: no plate changes. The server prints `THE PAGE IS BLANK. THAT IS ITS OWN VERDICT.` ShadowLedger receives no unlock row.
Every known page also writes one ShadowLedger row `{kind="primer_page", page=N, zone=..., hash=..., ts=...}`.

UNVERIFIED hardware and bridge
- Webcam capture.
- Printed fiducial pages.
- Local OpenCV or ArUco detection.
- Hash match under real lighting.
- Direct webcam-to-Roblox bridge.
- Any automated capture without the operator typing `/primer N`.
All are marked UNVERIFIED. The estate does not have this hardware path yet.

PART 3 - WIRE LIST

Wire-don't-build law: each zone consumes and feeds only existing estate organs. No new services, no new DataStores, no new HTTP endpoints. Each server module is required and built from `roblox/src/server/init.server.luau` in the same shape as the existing CathedralPlate wiring.

| Zone | Consumes | Feeds |
|---|---|---|
| GLASS FOUNDRY | CathedralMap, KSpace, ShadowLedger, LedgerExchange | ShadowLedger (shard rows), LedgerExchange (shard offers), CathedralMapHud (heat count row) |
| BONE EXCHANGE | LedgerExchange, ShadowLedger, SphereKinship | LedgerExchange (offer and accept rows), ShadowLedger (accept rows), CathedralMapHud (slate row) |
| ECHO ORCHARD | CathedralMap, ShadowLedger, NpcGateway, Chat remote | ShadowLedger (phrase and echo rows), NpcGateway (witness requests), CathedralMapHud (portal row) |
| SALT LEDGER | LedgerExchange, ShadowLedger, SphereKinship, CathedralPlate, KSpace | LedgerExchange (escrow rows), ShadowLedger (deposit and withdraw rows), CathedralMapHud (tilt row) |
| PRIMER CLOISTER | CathedralMap, CathedralPlate, ShadowLedger, Chat remote, CathedralMapHud | ShadowLedger (primer_page rows), zone unlock flags for GlassFoundry, BoneExchange, EchoOrchard, SaltLedger, CathedralMapHud (page rows) |

Primer capture script wires: `tools/primer_capture.py` consumes `tools/primer_pages.json` and the webcam frame. It feeds the operator with `PRIMER PAGE N`. It does not feed Roblox directly in v0. The operator feeds the existing Chat remote. This keeps the wire list inside existing organs. The only new files are the five zone modules, their five client HUD modules, and `tools/primer_capture.py` plus `tools/primer_pages.json` as its data table.