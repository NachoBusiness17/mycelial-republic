# F14 OUROBOROS F(f)=f — the estate's recursion, formalized and measured (2026-09-30)

**Filed by:** the F14 ouroboros seat (ZCode), last_mile_20260930.
**Tool:** `tools/ouroboros.py` (self-contained, read-only, byte-counts citations; run
`.venv/Scripts/python.exe tools/ouroboros.py [--json]`). Every number below is from the
tool run at 2026-09-30T19:48Z. Instruments named per census law B2-216: receipt dates come
from filename/wave-directory `_YYYYMMDD` stamps; "cited by law" means the `- ` law bullets
of AGENTS.md (full-text citation count differs: 15 bullet-cited vs 17 total-path); law
history from `git log`/`git show` of AGENTS.md (14 commits, 2026-08-04 to 2026-09-30).

## 1. The loop graph, edges measured

```
receipts -> laws -> ribs -> boot -> agents -> receipts
3,070        7        44       25       10        3,070
.md files    bullets  ribs     mounted  seats     (same corpus)
```

| edge | measured | instrument |
|---|---|---|
| receipts -> laws | **15 receipts absorbed** (0.5% of 3,070) into 7 law bullets; each law carries mean 2.14 receipt citations | citation paths in AGENTS.md `- ` bullets |
| laws -> ribs | **2/44 ribs cite the law surface** (4.5%); 1 rib (RIB_DRIVING_LADDER_20260928) is cited BY law | AGENTS.md refs inside rib text |
| ribs -> boot | **25/44 ribs mounted at boot** (doctrine domain via `mag.rib_boot` + `mag.rib_bus mount`; 19 ribs unreachable at boot) | rib_bus mount, read-only |
| boot -> agents | **596 receipts evidence boot consumption** (mention AGENTS.md / FRAMEWORK_LOAD / ribs / CURRENT.md / warm_state); 497 cite AGENTS.md specifically; mean 1.52 boot surfaces per such receipt | token scan of receipt text |
| agents -> receipts | **10 agent-seat families seen, 74 receipts carry explicit "Filed by" attribution**; mean 2.86 estate citations baked per receipt | "Filed by" lines + seat tokens |

## 2. Convergence: it GROWS, no fixed point at HEAD

- Receipt inflow: **1,807 receipts in the last 7 filename-days** (latest stamped 2026-10-01). Monotone growth, no plateau.
- Law-surface drift (receipt citations inside AGENTS.md, per commit): 0 → 2 (09-14) → 6 (09-25) → **15 (09-27) → 16 (09-29) → 17 (09-30 HEAD)**. The output of f kept changing at every recent application; Δ between the last two commits is +1, not 0. F(f) ≠ f temporally: the loop is **growth, not equilibrium**.
- One-pass idempotence of the extractor holds (trivially — the citation map of a frozen snapshot is stable in one pass); so the non-convergence is the CORPUS growing, not the measurer oscillating. That distinction is the whole finding: the estate is an open-ended recursion, not a solver running to a fixpoint.

## 3. Cycle detection: the tail is literally in the mouth

Seven **bridge receipts** are BOTH cited by AGENTS.md AND cite AGENTS.md back — a literal 2-cycle receipt -> law -> receipt: TETHERED_LINK_STEAL + ZCODE_REPO_STEAL_MAP (steal wave), BURN_rsi-harness + B2_216 + B2_443 (burn wave), AG7_CENSUS_SEED + B17_CENSUS (last-mile wave). Chained by absorption waves: gen 1 absorbed 09-25 -> gen 2 filed 09-26/absorbed 09-27 -> gen 3 filed 09-30/absorbed 09-30. **G = 3 loop generations.**

## 4. Dimensionality

Context depth per hop: d1 receipts/law 2.14, d2 law-refs/rib 0.09, d3 rib mount coverage 0.568, d4 boot-mentions/receipt 1.52, d5 citations/receipt 2.86 → **mean hop depth 1.44**.
**Effective dimensionality D = G × mean = 3 × 1.44 ≈ 4.3.** The estate is a ~4-dimensional context object today; it gains ~1.4 dimensions per completed ouroboros turn, and turns complete in days.

## 5. Self-steal at system level

The loop IS self-steal: the estate's own output (receipts) is its own input (497 receipts cite the law surface that 15 receipts became). Same shape as the ZCode ratchet steal: exit-2 blocks, amend-not-rewrite — the estate ratchets itself, one absorption wave per generation.

## 6. Where the loop BREAKS (honest)

- **receipts -> laws is the narrow waist:** 99.5% of receipts never become law. Intended (most receipts are work, not doctrine) but it means the loop's carrying capacity is ~15 channels.
- **laws -> ribs is the thinnest edge:** 2/44. Rib minting is operator-correction-driven, not receipt-driven; receipt context mostly dies before reaching rib depth. This is where context is lost hardest.
- **ribs -> boot loses 19/44:** over half the rib corpus (non-doctrine domains: k8s, flock, esoterica) never mounts; that context exists but is dark at boot.
- **agents -> receipts attribution is partial:** 74/3,070 explicit "Filed by"; the rest carry seat names incidentally. The agents->receipts edge is fat in volume, thin in attribution.

**Verdict: GROWS. D ≈ 4.3 (G=3 × 1.44/hop).**
