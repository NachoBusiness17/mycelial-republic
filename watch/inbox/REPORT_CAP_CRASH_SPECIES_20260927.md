# REPORT-CAP CRASH SPECIES + SALVAGE BOUND — 2026-09-27

**Species (named, twice-confirmed):** a workflow script that reports rich findings inline dies mid-run when one item exceeds the report() 32KB cap. The game-dig veins lost two full runs to it the same hour: roguelike dwfrun-038cd25b died at a 33,974-byte deep-dive item (32 findings banked first) and co-op dwfrun-ef372bc6 died at 40,898 bytes (37 findings banked first). The work was never lost (reported items and lane files survived; the amended runs imported everything finished as cache), but the run-level deliverables (wheel spec artifact, final return) died with the run.

**Fix (landed all five veins):** a `shrink()` producer-side bound on every report site: numbers 1200, retention_hook 600, abuse_vector 1200, evidence 4000 chars, sources 8, owed 400. The reported item is a bounded copy for the salvage channel; the FULL finding still returns from the ask and feeds the synthesizers and the wheel spec unchanged. Ask text untouched, so cache replay holds across the amendment.

**Amended runs (all live at write time):** roguelike dwfrun-ba80ec38 (64.4M), co-op dwfrun-77a25387 (67.7M), creature-farming dwfrun-1011ea86 (54.9M), horror dwfrun-0873f855 (39.7M), liveops dwfrun-5005fbf4 (46.6M).

**Law (standing, for every future vein script and any fan-out workflow):** bound the salvage channel at the producer. A finding worth more than the cap goes to the artifact; the report carries its bounded shadow. The saved workflow copies in .zcode/workflows/ (game-dig-*) all carry the fix since the promotion sweep saved the final amended forms.

**Salvage digest (what the crashed runs had already banked, richest finds):** Hades duo-boon complete K8 graph (28 boons, 8 gods, every pair); Hades heat-menu cherry-pick with the lowest-incomplete-rung payout patch to port; Hades Wretched Broker infinite-mint (+5 keys/cycle into Titan Blood); Balatro Naneinf copy-stack engine terminating the game's own math at Ante 39; Stardew race-window duplication + even-split treasury flip; DRG resupply-pod team-kill + pooled Morkite trust; DST wealth-targeted Deerclops as a proxy-raid warhead needing faction-scope checks.
