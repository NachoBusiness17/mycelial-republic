# COUNSEL SALON: THE QUOTA BURN WE SHOULD HAVE CAUGHT
**Summoned:** Operator, 2026-09-05 ~04:1xZ — "Summon ponytail and lessig. We should have caught our quota burn in za."
**Specimen:** ZAI_API_KEY_Lite (GLM Coding Lite V3 yearly, 2,000 credits/5h + 10,000/wk) burned
6.42K/10K and died mid-promo — the SECOND death of the same class in 7 days (08-29 code 1310).
**Verdict:** both seats concur on the root; they disagree on the remaining half of the cure.

---

## THE EVIDENCE INVENTORY — what the fleet HAD before the death

| # | Instrument | What it said | Was it polled? |
|---|-----------|--------------|----------------|
| 1 | ZAI_API_EXPERT_REFERENCE.md:312 | "CAMPAIGN-WINDOW TENSION (tri-state): the 5.3-flash Lite rows SHOW credits consumed" — the burn was flagged IN THE HOUSE, as an open DISPUTED | No — sat on the wall for days |
| 2 | The 08-29 death | Same key, same wall, code 1310 "Weekly/Monthly Limit Exhausted" — precedent ON RECORD | Recorded, never converted to a guard |
| 3 | The seat usage db (the meter) | The ONE time spend verification ran (economist audit) it caught the 2.84B-tok zombie tick — the instrument WORKS | Wired to a one-off audit, no standing sweep |
| 4 | The provider dashboard | 6.42K/10K burned | Only seen when the Operator pasted a screenshot — provider truth entered through his eyes, not a sensor |

## PONYTAIL (verification skeptic — "hiring verifiers is a confession")
**Thesis:** The fleet verified OUTPUTS obsessively — tri-state claims, receipts, honest-conservative
mining — and verified SPEND never. Verification follows values, and the value model said
"Lite = $0," so the meter was nobody's job. Worse: the fleet's own tri-state discipline FLAGGED
the truth (row 1: credits showing consumed, in the house, DISPUTED) and nobody pulled the
thread — tri-state is being used as a LABELING practice, not a falsification WORK QUEUE.
A DISPUTED row with billing evidence behind it is a fire alarm, and it hung on the wall
unpulled. The frontier labs' confession is hiring verifiers (OpenAI Frontier Evals, Scale,
sayashk — receipted 09-05); our confession is the mirror: our evals verified answers and
never verified spend. "Should have caught it" is true — but catching was assigned to no
organ. An unowned watch is an unwatched meter.

## LESSIG (code is law — environments are jurisdiction)
**Thesis:** No sensor = no catch, ever. Catching is a SENSOR property, not a virtue property —
where the burn could not be seen AS burn, vigilance had nothing to grip. Every door in the
fleet encodes its founding belief: lane_runner's docstring literally said "the fleet's $0 lane
(night-window zero-metered)" — and code does not update itself when its belief is falsified.
Law 15's pacing fix was legislated in PROSE at 03:2xZ last night and prose executes nothing.
Deeper: z.ai's meter sat OUTSIDE the fleet's legal order; their court issues only one verdict,
a 429, and only AFTER the money is gone. The cure is annexation — bring the meter inside the
walls: ledger, guard at every door, defaults that answer "what if nobody specifies?" by
STRUCTURE rather than by whoever last edited a constant.

## MUTUAL CRITIQUE
- **Ponytail → Lessig:** a purely local guard is a self-graded exam. The ledger counts what the
  CAGE burns; the key is SHARED with the Operator's other windows (the very window that buzzed
  his phone). Ledger 300 vs provider 9,000 = you learn the delta only at the next death. A
  guard without external reconciliation can be confidently wrong.
- **Lessig → Ponytail:** "poll every meter" is how the premium seat becomes a diarist.
  Verification budget is finite; the law is not "watch all meters" but "any belief that routes
  SPEND carries a tripwire at the point of routing." And the queue problem is not labeling —
  even a perfect DISPUTED label rots without an OWNER.

## SYNTHESIS — the verdict
1. The catch you wanted is a structural property. "We should have caught it" was a category
   error: the fleet didn't miss the burn — it never had a place where burn could be SEEN as burn.
2. **LANDED today (Lessig half, structure):** `mag/lite_guard.py` — daily pacing ledger
   (law 15: ~1,400 of the 10,000/wk), wired at every automatic door (lane_runner flash_call,
   rib_chat, swarm dispatch); swarm DEFAULT_PROVIDER repointed z_ai3 → cerebras (ZAI_LITE_LAW
   order: cerebras → groq → Lite burst-only). Belief falsified 09-05 → structure flipped same day.
   Lanes stay UP under the ceiling; past it they raise/skip with the refill date NAMED (law 15 teeth).
3. **OWED (Ponytail half, reconciliation):** the weekly delta check — local ledger vs provider's
   number. Delta ≈ 0 = the cage is the only consumer; delta large = unaccounted windows/daemons,
   NAMED. Door order: probe z.ai for a usage/quota API first ($0); fallback = Operator's weekly
   dashboard paste reconciled against `lite_guard.status()`. Owner: economist lane.
4. **LAW MINTED (promotion queue — prose until the lattice admits it):**
   **METERED UNTIL RECEIPTED** — any lane believed free must carry (a) a receipt (billing rows
   or a falsifier probe) and (b) a tripwire at its door; a DISPUTED spend row is a fire alarm
   with a 48h falsification SLA owned by a named organ (economist). Precedent that the
   instrument works when pointed: the 2.84B-tok zombie-tick catch.
5. The callback: the fleet already trusts nothing against its own word — trust is verified
   against HIS surface. As of today, spend is too.

**Falsifier for this salon:** next billing cycle runs with the guard live. If the weekly pool
dies mid-week again, the class was NOT closed — check the ledger's per-door breakdown first
(it names which door overspent), then the delta (it names who outside the cage did).

---

## ADDENDUM (~04:4xZ) — THE OWED BUILD LANDED SAME DAY
Provider door found, $0: `api.z.ai/api/monitor/usage/quota/limit` + `/api/biz/subscription/list`
— the undocumented endpoints z.ai's own subscription UI calls (door source: openusage provider
notes; verified live with the Lite key, 200 OK, billed nothing). Reads need only the key — no
browser, no Google tap. Dashboard WRITES (quota reset button) still ride the operator's Google
accounts: nachobusinesscorp@gmail.com / fostertron@gmail.com (custody recorded).

**First reading corrected two beliefs on the spot:**
1. "Weekly pool refills ~Sep 5" (the veto's basis) — FALSE. nextResetTime = **Sep 08 02:19Z**,
   anchored to the purchase moment 2026-08-25 10:19 SGT. 3,579 credits must last ~3.4 days.
2. The key's "death" was 5h-BUCKET exhaustion (2,000/5h, Calcifer grind, self-healing every
   5h) — NOT weekly exhaustion; the weekly window still had 3,579 left.

**Structural consequence:** `lite_guard.check()` now CLAMPS the daily ceiling to provider truth
(remaining ÷ days-to-reset) — 1,228/day live, not the flat 1,400 that would have re-killed the
key on Sep 7. Denials name the exact refill moment. Every read banks to
`state/fuel/lite_quota_log.jsonl` — the weekly delta trail has begun; economist owns the read.

## ADDENDUM 2 (~18:3xZ) — THE FULL DASHBOARD API (found via opencode-glm-quota source mine)
The monitor family has three members, all live with the Lite key, all $0:
- `GET /api/monitor/usage/quota/limit` — the meters (5h bucket + weekly pool) — wired into
  lite_guard.provider_quota() (clamps the daily ceiling).
- `GET /api/monitor/usage/model-usage?startTime=YYYY-MM-DD HH:MM:SS&endTime=...` — per-model
  hourly series + totals + call counts (the dashboard graphs, raw).
- `GET /api/monitor/usage/tool-usage?...` — z.ai-MCP tool counts (web-reader etc.; NOT client
  apps — per-window attribution still rides ledger-delta).
Wired as lite_guard.usage_detail(start, end); first full reading BANKED: Sep 1-5 window =
87.04M tokens / 220 calls — GLM-5.3 full 73.24M (84%), GLM-5.3-Flash 13.80M. Attribution
confirmed by operator: the agents window pinned on the Lite plan (killed). Lane CLOSED.
