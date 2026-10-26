# B2-195 receipt: express-mode quota lane block (2026-09-26, lane SW-03)

## Verdict

OWED-DORMANT, condition unmet. The brief fires "if the aiplatform enable lands"; the latest probe bytes (B2_63_vertex_probe_results.json, both auth shapes) still answer 403 PERMISSION_DENIED "Agent Platform API has not been used in project 1055073037365 before or it is disabled". No enable has landed, no 200 exists anywhere in the tree, so there is no measured quota to write and no first-200 timestamp to anchor. Writing the docs-table 10-requests-per-minute number into providers.yaml now would file an unmeasured docs quote as if it were the brief's "measured express quotas". The block's contract is registered here so the enabling lane owes exactly two writes.

## Evidence file:line quotes

- watch/inbox/burn_wave_20260926/B2_63_vertex_probe_results.json (latest bytes, header_auth and query_param_auth blocks): "status": 403, "error_status": "PERMISSION_DENIED", "error_message": "Agent Platform API has not been used in project 1055073037365 before or it is disabled. Enable it by visiting https://console.developers.google.com/apis/api/aiplatform.googleapis.com/overview?project=1055073037365 then retry."
- watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md: "run watch/inbox/burn_wave_20260926/B2_63_vertex_probe.py (expect 200)" and "express docs cap Gemini models at 10 requests per minute".
- configs/providers.yaml gemini block (402-440): "dormant: true   # 2026-09-26 B2-61: generation 401-dead; operator GO flips this + re-adds to routing" plus the B2-63 verdict comment ending "auth shape proven, API enablement owed".
- QUEUE.md B2-195 row (the conditional clause): "if the aiplatform enable lands, write the measured express quotas into providers.yaml gemini quota ... and record the first-200 timestamp as the observable clock anchor".

## Work done

- Checked the firing condition against the latest probe bytes and the providers.yaml gemini block: unmet (403 both auth shapes, dormant:true, no 200 anywhere).
- Registered the landing contract so the enabling lane cannot half-do it: on the first 200 from B2_63_vertex_probe.py, that lane must (a) write a quota block into the gemini provider carrying the MEASURED request rate it observed plus the docs-table 10 req/min cap as a cited ceiling, (b) record the first-200 timestamp (from the probe results file) as the express free-window clock anchor, explicitly marked "window start inferred from first observed 200, docs start date unknown", and (c) cite this receipt + B2-63 in the quota comment. The 90-day window start remains unknown-from-here per the brief; it is never to be backdated.

## Falsifier

Kill conditions: (a) a quota block appearing in providers.yaml gemini whose numbers are not backed by a recorded probe run (docs numbers dressed as measured), (b) a first-200 anchor timestamp that predates the earliest 200-bearing probe results file, (c) this receipt left standing while the probe file shows 200 (the condition would have fired and the block was owed, not dormant). Re-check trigger: any rerun of B2_63_vertex_probe.py.

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_63_vertex_probe_results.json (read, latest bytes)
- watch/inbox/burn_wave_20260926/B2_63_gemini_auth_20260926.md (read, verdict + enable path)
- watch/inbox/burn_wave_20260926/B2_63_vertex_probe.py (existence + expect-200 contract)
- configs/providers.yaml gemini block lines 402-440 (read, dormant state)
- docs.cloud.google.com express-mode overview (named by brief; the 10 req/min cap is quoted via the B2-63 receipt's own fetch, not re-fetched here: the condition to measure is unmet, so no quota numbers are being filed from it)
