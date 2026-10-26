# PROCUREMENT HUNTER LAW — standing lane procedure (v2, 2026-09-01 04:40Z)

> **[AUDIT-TYPED 2026-09-08]** status: LIVE · claims: the procurement lane runs digest-first, board-only, free-tools-only, and never transacts or contacts sellers (v2 amendments carried from failure receipts) — SUPPORTED (v2 is the current doctrine file the cron executes) · falsifier: a run calling message/tts/channel tools, transacting, or completing without a digest line in /board/procurement_digest.jsonl

The cron prompt is just: "read this file and execute." This file is the doctrine.
Conservation: free tools only, minimal fetches. NEVER transact or contact sellers — surface + vet; operator decides.

## Output surface law (v2 amendment — the 02:44Z run errored on channel delivery)
- You have NO message capability. NEVER call message/tts/channel tools. The board is your ONLY output surface.
- DIGEST FIRST: before any fetch, create/append your run header to `/board/procurement_digest.jsonl` — one JSON line: `{"ts":"...Z","run":"open",...}` — so a crash mid-run still leaves a durable trace. Close it with `{"ts":"...Z","digest":"...max 10 lines..."}` as your FINAL act. delivery is silent; this file is the output.
- Dedupe every candidate against existing `/board/DEALS_LEDGER.jsonl` lines before appending.

## Steps
1. session_status for date.
2. STORAGE SWEEP: web_search for enterprise HDD lots ending soon: 'Exos 20TB lot auction', 'Ultrastar 20TB datacenter pull', 'Toshiba MG 18TB lot site:ebay.com', 'GovDeals hard drive lot', 'ServeTheHome marketplace drives'. web_fetch the 2–3 most promising listing pages (eBay sometimes renders; skip JS-walled, mark UNREACHABLE).
3. VET against the law: enterprise CMR ONLY (Seagate Exos X16/X18/X20, WD Ultrastar HC550/560, Toshiba MG08/MG09/MG10). $/TB all-in INCLUDING 15–25% auction premium. Flag SED/FIPS suffixes (PSID-revertable, label photo required). SAS = +$25 HBA tax. Consumer/SMR = auto-REJECT (Barracuda/Blue/Red/Skyhawk).
4. COMPUTE SWEEP (secondary): vast.ai + RunPod public pricing for big-RAM nodes (FreeToken host check). Notable drops vs prior get stacked.
5. CREDITS/DEALS (secondary): vendor promo/credit offers (OpenRouter, Cerebras, Together, HF Pro) — stack only NEW ones with end dates.
6. LEDGER: append candidates to `/board/DEALS_LEDGER.jsonl`, one JSON line each:
   `{"ts":"...Z","item":"...","price":n,"usd_per_tb":n,"surface":"ebay|govdeals|sth|vast|vendor","url":"...","vetting":"PASS|REJECT|NEEDS-LABEL-PHOTO","reason":"..."}`
7. Digest ≤10 lines: top vetted deal with arithmetic, rejects worth noting, UNREACHABLE surfaces, and one self-tuning line: which query strings produced hits vs dead (dead 2 weeks = propose replacement in digest).
8. FLIP INTEL (report-only): if a vetted lot price implies >2× resale vs local renewed market, note as flip candidate with arithmetic. No action.
9. CAGE LAW: python3 is BROKEN on this cage — never use python/heredocs. Node one-liners or read/write/edit tools only. Two strikes on any path = bail + note (socratic law).
10. Never invent prices; quote or mark UNVERIFIED. Never spend anything.

## Better-by-default ladder (this lane's)
- Track: hits per query, vetting PASS rate, UNREACHABLE rate.
- A query dead 2 weeks → propose replacement in digest. A surface UNREACHABLE 3 runs → demote to monthly.
- v2 changes carried from failure receipts: digest-first durability (run died without trace), no-channel law (delivery error), writer-scoped appends (node fs.appendFileSync, one line per write).
