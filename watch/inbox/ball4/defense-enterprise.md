# BALL4 lane receipt: follow-defense-enterprise (division B)

Date: 2026-09-29. Writer: gala-ball4-follow-defense-enterprise.
Ask: mine defense-infra + enterprise + security + space layers of the luncheon watchlist (last 14 days), resolve the 2 search-grade names, append one signals row per target, update resolved rows in place.

## Register work

- Signals register CREATED: `watch/inbox/luncheon_watchlist_20260929_signals.jsonl`, 8 rows (one per target), each with in_window / out_of_window_nearest split, a date_honesty_note, an estate_angle, and a handle_check field.
- Watchlist `watch/inbox/luncheon_watchlist_20260929.jsonl` edited IN PLACE, 3 rows (register is the single surface, no duplication):
  - `lunch-richard-walters` line 22: RESOLVED. Org: White House (EOP), Deputy Chief of Staff for Legislative, Political and Public Affairs (Axios + Politico, 2026-05-01; ex-RNC chief of staff, ex-Trump-Vance Inaugural Committee ED). Lane search to gov, handle empty with gov grade (no verified personal X handle found). Was "unverified org" / handle_grade "search".
  - `lunch-sean-cairncross` line 34: RESOLVED and CORRECTED. Org: White House, National Cyber Director (ONCD), nominated 2025-02, confirmed 2025-08. The seat-drop row's "WH Deputy Chief of Staff" guess was WRONG; corrected with source. Leading WH interagency AI policy coordination (Politico 2026-05-16); "secure AI without new rules" posture (CyberScoop, 2026-08); SCTE TechExpo26 Atlanta 2026-09-30.
  - `lunch-bill-mcdermott` line 32 (one-row scope extension beyond the 2 named, evidence in hand): handle "search:BillMcDermott" to "@BillRMcDermott", grade search to "confirmed", live-verified via api.fxtwitter.com/BillRMcDermott (bio: "now leading @ServiceNow"). New grade value "confirmed" = live fxtwitter account match; documented here and in the signals row.

## Signals mined (window 2026-09-15/2026-09-29, honesty about dates)

- **Karp (Palantir CEO)**: in-window window-plausible: urges US gov to nationalize leading AI labs; first key investor in Ukraine's new defense-tech company (Fedorov announcement); Japan MoD reportedly considering Maven Smart System. Date-pinned but out-of-window: Chabad Neilah appearance 2026-09-21. Three items are recency-filter-search-placed without pinned article dates; flagged in the row, not passed off as verified.
- **Sankar (Palantir CTO)**: NEGATIVE in-window result, first-class. Role current as of 2026-09-01 profile data. Nearest dated item 2026-05-21 (AI job-displacement fears exaggerated). @ShyamSankar live on fxtwitter, tweet bodies not retrievable.
- **Daniels (Exiger CEO)**: strongest lane hit. Date-pinned IN-WINDOW: WashingtonExec interview 2026-09-22, "Supply chain is a new domain of warfare". Fox Business (AI vs tariff evasion) and Bloomberg (geopolitical supply-chain volatility) items window-plausible, dates unpinned. fxtwitter "@Exiger" resolves to an unrelated squat account ("Graham", 0 tweets): company X handle NOT live-confirmable via fxtwitter, org attribution rests on web sources.
- **McDermott (ServiceNow)**: no date-pinned in-window item. Nearest dated: Goldman Sachs conference 2026-09-10, 5 days before the window opens (reported as nearest-dated, never as in-window). "Only AI control tower that drives workflow, action and business outcomes" positioning continues (undated).
- **Arora (PANW)**: no date-pinned in-window item; one-month recency-filtered search returned EMPTY. Nearest: Q4 FY2026 earnings call 2026-09-08; 2026-09-01 reports of Okta and Datadog talks before the ~$25B CyberArk deal (closed ~2026-02-11/12). @nikesharora live-confirmed ("Palo Alto Networks" bio), matches declared grade.
- **Isaacman (NASA Administrator)**: in-window: agency-wide "Lengthy Note" dated 2026-09-20 (NASA Watch); Kennedy Space Center presser on the new Boeing Starliner crew-flight deal (date unpinned); Space Academy Ohio "good shot" (date unpinned). The headline space-compute item is OUT-of-window and so marked: The Hill 2026-08-26, Isaacman backs moving AI data centers to Earth orbit (direct fetch 403'd, date from webReader metadata). Race context 2026: SpaceX 1M-satellite filing, Google Project Suncatcher (TPUs in orbit), Orbital 2027 first launch, Aetherflux $275M pivot; Brookings feasibility-gap governance warning.

## Estate angles (written into every signals row)

- Defense AI deployment shapes: Palantir wins by sitting inside the customer's workflow (Maven into Japan MoD, Ukraine stack), not by selling models: the receipts-not-labels deployment pattern. Daniels proves provenance-graphing is a warfare domain: the estate's corpus registry discipline pointed at suppliers. McDermott's control tower is the enterprise mirror of the estate's single-surface laws: whoever owns the workflow layer where agents act wins. Arora's platformization says the identity/credential surface is the next consolidated control point: the estate's seats and keys.
- Space-compute angle: orbital compute is the long-horizon compute-sovereignty play (unlimited solar, radiative cooling, no siting politics); an Isaacman-backed NASA endorsement (2026-08-26, The Hill) is the state nod legitimizing the lane. Estate posture: watch who owns off-planet compute the way we watch who owns the meter.

## Checks

Byte-checked finish line run at close; raw output: `watch/inbox/gala_20260925/ball4-luncheon-follow/lanes/follow-defense-enterprise.check.txt`.

## Gaps (stated, not papered)

- Karp's nationalize-AI-labs, Ukraine-investment, and Japan-Maven items carry no pinned article dates (recency-filter placement only). Arora and McDermott have no in-window dated items at all. fxtwitter returned profiles only, never tweet bodies, so no tweet text is quoted anywhere in the register. The Hill fetch 403'd; its date comes from the webReader metadata line. All of this is flagged in the rows themselves.
