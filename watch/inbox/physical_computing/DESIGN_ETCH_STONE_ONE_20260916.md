# DESIGN — Etch Stone One: the 16-node Ising Covenant Plate

**Filed:** 2026-09-16 · **Tier:** $0 design / Tier-$small to produce · **Pack:** `PHYSICAL_COMPUTING_PACK_20260916.md` §3 Tier-$0 "Etch inventory"
**Receipt:** `receipts/C16_ETCH_INVENTORY.md` · **Status:** SPEC — physical output pending falsifier §4.4

---

## 0. Candidate decision (pick one, kill the others honestly)

| Candidate | Verdict | Why |
|---|---|---|
| **Laser-etched Ising coupling lattice (16-node signed plate)** | **PICKED** | Ties to the fleet's own canon (Ising machines brief, pack §2 row 3, the plaque-lie doctrine); verifiable end-to-end with zero sim fudge (16 spins = 65,536 states = brute-force enumerable); achievable with a 2 W diode on anodized aluminum; doubles as the etch-pipeline calibration + damage-detection protocol every later etch rides. |
| Etched waveguide test | **KILLED** | Optical waveguides need femtosecond-pulse lasers inside glass (filtered refractive-index modification). A 2 W CW diode cannot write a guiding structure. At our tier this is decoration wearing a physics costume — the plaque-lie. |
| Spore-print ledger plate | **DEFERRED, not killed** | The instrumented cube it would log (pack §3 Tier-$small) does not exist. Etching a ledger before any logs exist inverts the dependency — a ledger plate with nothing to ledger is a plaque. Revives the day the first cube ships. |

Doctrine binding: `watch/inbox/LIVING_CIPHER_20260914.md` — the Isfahan lock "was all gears …
every dial counts"; a living cipher "is legal exactly where it is lossless." **Every etched
mark on this plate is a dial.** If the readback does not reproduce the couplings losslessly,
the plate is decoration, and the receipt must say so.

## 1. What the artifact IS

A **100 × 100 × 3 mm black-anodized 6061 aluminum plate** carrying:

1. A **16-node signed Ising coupling lattice** — 16 nodes in a 4×4 grid, couplings drawn as
   ferromagnetic (solid) or antiferromagnetic (dashed) edges.
2. The **etched ground state** — a 4×4 spin panel showing the provable minimum-energy state
   of that exact coupling instance.
3. An **integrity block** — the first 16 hex chars of `sha256` of the canonical coupling
   JSON, etched as text.
4. A **resolution wedge** — line ladder 0.10 / 0.15 / 0.20 / 0.30 / 0.50 mm — the permanent
   calibration record of the machine that cut it.

```
+------------------------------------+
|  STONE ONE          3f9a1c...e2b7  |  <- title + sha256[0:16]
|                                    |
|   o----o    o  o----o              |
|   |    :    :  |    :   J lattice  |
|   o----o    o  o----o   4x4, 10mm |
|   :  solid = J=+1      pitch       |
|   o    o--: o    o      dashed =   |
|   :    :    :  :       J=-1        |
|   o----o    o--o                   |
|                                    |
|  [s][ ][s][ ]   WEDGE: .1 .15 .2   |
|  [ ][s][ ][s]          .3  .5      |  <- ground-state
|  [s][ ][ ][s]   2026-09-16        |     panel + wedge
|  [ ][s][s][ ]                      |
+------------------------------------+
   100mm x 100mm, black anodized Al
```

## 2. The coupling instance (canonical, reproducible by anyone)

```python
import numpy as np, json, hashlib
rng = np.random.default_rng(20260916)          # date-seeded, public
J = np.zeros((16, 16), dtype=int)
edges = [(i, j) for i in range(16) for j in range(i+1, 16)]   # 120 candidate edges
picked = rng.choice(len(edges), size=36, replace=False)        # 30% density
signs  = rng.choice([-1, 1], size=36)
for k, idx in enumerate(picked):
    i, j = edges[idx]; J[i, j] = J[j, i] = signs[k]
canon = {"n": 16, "edges": [[i, j, int(J[i, j])] for i in range(16)
         for j in range(i+1, 16) if J[i, j] != 0]}
h = hashlib.sha256(json.dumps(canon, sort_keys=True).encode()).hexdigest()
```

- **Nodes:** 16 spins, index 0–15 etched as single hex digits (0…F) beside each node.
- **Nodes 0–15 map row-major to the 4×4 grid**, 10 mm pitch, 20 mm margin.
- **Ground state:** found by **exhaustive enumeration of all 2^16 = 65,536 states** —
  no annealer, no seed ambiguity, provably minimal. If the minimum is degenerate, the
  canonical panel is the lexicographically smallest minimizer, stated in the JSON.
- The generator + enumerator + readback checker land as **one script** filed next to this
  spec before first etch (pre-registration: the etched panel is committed before the plate
  is cut, hash into the receipt).

## 3. Etch parameters (machine: Opt Lasers PLH3D-2W on Prusa-class FDM)

Material note: black anodized aluminum is the classic 2 W diode job — the diode ablates
the anodization layer, leaving bright metal marks. No marking compound needed for this
plate. Bare-metal marking (the "passives/metals" goal) needs LaserBond 100-class compound
(~$30/can) and is a later burn test, honestly out of scope for Stone One.

**Job 0 — burn matrix (before any artifact etch, ~30 min):** 5×5 ladder, power
40/60/80/100 % × speed 500/1000/1500/2500/4000 mm/min on a scrap anodized coupon.
Select params where 0.15 mm dashes are unbroken and 0.10 mm fills don't close.

**Job 1 — Stone One etch (starting guesses, QUOTED ranges from Opt Lasers 2 W anodized
docs, to be frozen by Job 0 — UNVERIFIED until run):**

| Param | Value |
|---|---|
| Lines/edges (vectors) | 100 % power, 1000 mm/min, 1 pass |
| Dashed edges (J=−1) | same, 1.0 mm dash / 0.6 mm gap |
| Node dots + spin fill | 0.08 mm line interval, 1500 mm/min |
| Text (title, hash, date) | 0.20 mm stroke font, 4 mm cap height |
| Nominal line width | 0.20 mm design; wedge records actual |
| Total est. etch time | 25–45 min |

## 4. What computation/verification it embodies

- **A physical commitment to a hard instance.** The plate carries a specific signed
  coupling matrix whose minimum anyone can verify by brute force — the plate is a puzzle
  whose published solution is physically etched beside it, Isfahan-style: every dial counts.
- **Lossless readback test (the anti-plaque gate).** Flatbed-scan or macro-photo the plate
  → threshold → extract nodes/edges/dashes → reconstruct J′ → `sha256(J′)` must equal the
  etched hash. Pixels-to-matrix is the fleet's "trust bytes" law pointed at atoms.
- **Damage detection for free.** If abrasion flips one coupling in J′, the exhaustive
  minimum of J′ generally **differs** from the etched ground-state panel — the plate audits
  its own integrity, forever, with no instrument beyond a camera and the script.
- **Pipeline calibration.** The wedge records what this machine can actually hold at each
  line width — the parameter sheet every later etch (cube sensor labels, PCB silk, the
  spore ledger plate when it revives) inherits.

**DAD honesty (falsifier §4.5):** this plate is an *information* artifact, not a dynamic
computer — encode/decode overhead is trivial and it computes nothing after manufacture.
It satisfies §4.4 (a physical artifact within tier budget) and builds the etch pipeline;
the §4.5 dynamic slot stays reserved for the ~$15 two-bucket XOR vs the MUD hydraulic sim.
Saying so is the pack working.

## 5. Test protocol (pre-registered)

1. File `stone_one_j.json` + `stone_one_check.py` next to this spec; record `h` in the
   production receipt **before** cutting.
2. Job 0 burn matrix → freeze parameters into the receipt.
3. Etch Stone One.
4. Verify within 24 h: scan at ≥600 dpi → checker reconstructs J′ → hash equal → exhaustive
   ground state of J′ equals etched panel → PASS line filed with the scan image hash.
5. Any FAIL is filed with the coupon, not silently retried — the wedge is data, not shame.

## 6. Cost to produce (honest, three doors)

| Door | Contents | Cost |
|---|---|---|
| **A — June-tweet path (canon, pack Tier-$small)** | used Prusa MK3S $250–400 (eBay street 2026, median ~$300; MK4S release has pushed MK3 prices down) + Opt Lasers PLH3D-2W kit €239.95 ≈ $260 (MYBOTSHOP.DE; MK3-mount — pair with an MK3, not MK4) + shipping ~$40–135 + anodized plate 100×100×3 ~$8 + scrap coupon $0 (offcut) | **~$610–700** |
| **B — standalone 10 W-class diode engraver** (xTool/Sculpfun/Ortur class) | better metal marking, but buys no FDM — fails the June-tweet "bootstrap replicator" argument (printer first, laser as conversion) | ~$300–400 |
| **C — borrowed access** (library makerspace / friend's laser, plate only) | keeps Tier-$small unspent; still produces the artifact | **~$10–40** |

Door A is the canon path and the recommendation (FDM chassis + conversion is exactly the
tweet's bootstrap thesis; the printer then also serves battle-bot parts and cube fittings).
Door C is the $0-law fastest route to the artifact itself. No purchase is authorized by
this spec — Tier-$small needs the operator word per pack law.

**Budget to produce Stone One: $10 (door C, plate only) — $700 (door A, full canon path).**

## 7. Sources (QUOTED+URL'd where possible; UNVERIFIED flagged)

- Opt Lasers PLH3D-2W "Original Prusa Laserupgrade" — €239.95, MYBOTSHOP.DE (QUOTED listing; MK3-generation mount)
- No official Prusa MK4 laser kit exists; Prusa's own conversion kits are printer upgrades (MK3S→MK4S $249–499, prusa3d.com) (QUOTED)
- Infinity Flow S1 MK4/MK4S laser mount adapter, $7.99 (QUOTED listing; laser not included)
- Used Prusa MK3/MK3S street: $200–400 eBay 2026, community fair-price $250–300 (QUOTED, live listings + r/prusa3d consensus)
- 2 W diode + marking compound for bare stainless/ceramic: LaserBond 100 class, ~$30 (QUOTED range; not yet priced live — UNVERIFIED until quote-gather)
- Anodized 6061 blank 100×100×3 mm: ~$5–10 typical (UNVERIFIED — confirm at order)
