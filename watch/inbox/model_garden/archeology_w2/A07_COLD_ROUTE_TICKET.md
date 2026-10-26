# A-07: COLD_ROUTE_TICKET (archeology.wave2 lane receipt + amend)

Schema: archeology.wave2.receipt.v1 · lane A-07 · night lane 2026-10-02 ~05:0xZ
Cost: $0 (bytes only). Deliverable per memory/plans/ARCHEOLOGY_20.md row A-07:
two-regime steering policy as amend to model_garden specs, wiring
chord_pipeline stage 4 to the policy the trial just proved.

## The evidence chain tonight (all byte-cited)

1. The policy exists: watch/inbox/model_garden/COLD_VERTEX_LAYER.md "THE
   POLICY" section: two-regime steering, exploit hot vertices AND deliberately
   sample cold ones; the second regime is the Heart of Gold; dead as policy if
   cold never beats hot across a fair trial.
2. The trial ran and PAID: watch/inbox/model_garden/COLD_HOT_RESULT.md sec 5:
   VERDICT COLD-PAYS (composite 297 vs 279; raw-cluster axis a statistical
   tie inside named confounds). Cold bought law-class yield 5 vs 3 and
   cross-surface connections 3 vs 2, 6 new clusters on the estate's unreviewed
   spine, $0.0829 metered. Hot still paid on fifth-review files, so the policy
   is two-regime, not cold-only.
3. The router exists but predates the verdict: mag/chord_pipeline.py
   route_work() (stage 4) splits SHADOW (coldest) vs FRONTIER (standing-wave)
   per the 2026-08-12 operator order, with selection helpers NOT wired to the
   proven instruments.
4. The cold-ranker exists: mag/ghost_summon.py coldest_vertices() (line 182):
   low degree first, then oldest first; report_coldest (line 201) folds it
   into summon reports.

## THE AMEND (ticket, not code tonight)

route_work() selection adopts the trial's paid shape verbatim:

- SHADOW arm: keep ghost_summon.coldest_vertices() as the base ranker but
  apply the trial's two corrections: (a) sharedness-size cap (the 2056-line
  orchestrator produced 0 REAL clusters; cap by line count, prefer
  mid-network spine like registry/chain_query), (b) a divergence quota:
  2 of 10 slots from CROSS_RACTOR_MATRIX unsettled pairs, priced per the
  trial's finding 6 (policy_engine's intent-questions paid 0 REAL; v1
  switchboard paid the richest cluster - divergence slots buy variance, not
  certainty).
- FRONTIER arm: unchanged (GPS-gradient, the hot list), per verdict line
  "hot kept paying on fifth-review files."
- The quota ratio (8 coldest + 2 divergence of a 10-slot shadow budget)
  becomes a named constant citing COLD_HOT_RESULT.md sec 5, so the next
  trial's numbers can amend it without re-deriving the mix.

## Success falsifier (carried from the spec, unchanged)

If a repeat trial at the amended routing shows cold never beating hot on the
composite across a fair repeat, the Heart of Gold dies as policy and ROUTE
reverts to GPS-only. The trial instrument (tools/code_swarm.py arms,
coldhot_select.py census) is already standing.

Filed by night lane, 2026-10-02Z. $0. No em-dash bytes. Implementation: one
sitting in mag/chord_pipeline.py route_work() + a route-shape test.
