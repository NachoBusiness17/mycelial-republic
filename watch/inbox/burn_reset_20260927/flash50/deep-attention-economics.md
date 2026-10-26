# DEEP: Attention Economics for the Mag Estate

Item: deep-attention-economics · banked 2026-09-28 · all paths relative to repo root.
Method: every number below was read or run in this session (files cited path:line; shell
outputs quoted where they are the evidence). Literature is named where it carries the
argument; the estate's own lineage is cited before any outside paper.

## 1. The measured state: the estate is IN attention bankruptcy on its primary surface

Ran this session (PowerShell-free, via rg/wc/ls):

1. `wc -c memory/attention.md` -> **40,436 bytes at 15:51 today**. Q-005's receipt
   (`watch/inbox/burn_reset_20260927/queue/Q-005.md:50`) records the same file at
   **1,330 bytes after the 12:40 triage** (down from 40,443). Regrowth from 1,330 to
   the full 40k cap in ~3h11m, ~30x, is the refill rate of the dominant writer.
2. `rg -c "### Session record ready"` -> **120 pings**, every one the same biography
   class; `rg -c "patrol fired|doctor fired|check fired|probe-alarm"` -> **0 alert-class
   blocks** in the file.
3. `tail -3 logs/census_patrol.log` -> `[2026-09-27 08:30:02] TASK-DOCTOR: 1 unhealthy
   task(s) named, alert appended` / `END exit=0`. A REAL patrol alert was appended to
   attention.md yesterday morning. It no longer exists in the file: evicted within the
   day by biography pings.
4. `rg -c "Triage 2026-09-28" memory/attention.md` -> **no match: today's triage block
   itself was already amputated** by the writer's 40,000-char cap. The bankruptcy
   consumed the record of the bankruptcy.
5. `head -c 600 memory/attention.md` -> exactly the newest biography ping. This is what
   the leanest consumer sees, because `mag/context_pack.py:620` clips the file to 600
   chars head-first (`mag/lanes.py:293` clips to 3,000; `mag/token_economy.py:50`
   budgets it at 15k).
6. `ls memory/attention_feedback.jsonl` -> **does not exist**. The feedback ledger of the
   attention ranker has never received a single event.
7. `wc -l watch/inbox/phone_relay_log.jsonl` -> 138 lifetime rows;
   `wc -l memory/pile/state_summaries.jsonl` -> 144 rows.

Definition (operational, not metaphor): **attention bankruptcy is the state in which the
marginal value of reading a surface falls below the cost of reading it, so the operator
rationally stops reading; every future alert on that surface then has zero value
regardless of its true urgency.** Items 1-4 are the estate crossing that line and
recrossing it three hours after a human spent a session digging out. Item 3 is the cost:
a genuine "unhealthy scheduled task" signal was produced by a working instrument and
destroyed by a lower-value writer before it could act.

## 2. What reaches the operator today: five channels, three different physics

Grounded inventory of every writer and consumer I read:

| Channel | Writers | Pricing today | Consumer |
|---|---|---|---|
| `memory/attention.md` standing board | `mag/biography.py:509-526` (prepend + 40k truncate), `mag/act.py:87-94`, `mag/tangent.py:286-294`, `mag/improve.py:527-536` (EXACTLY ONE [priority] line on provider alarms), `scripts/secret_scan_weekly.py:55-57`, `scripts/census_patrol_daily.ps1:79,109,150,170` and `scripts/fts_index_daily.ps1:145` (append on failure) | none: FIFO by recency, eviction by byte cap | `mag/context_pack.py:620` (600 chars), `mag/lanes.py:293` (3,000), `mag/chronicle.py:16-44` (latest 10) |
| Ranked attention API | `mag/attention_ranker.py` `build_ranked_attention` | 8-factor linear score, P0-P4 bands, hard rules immune to feedback | `dashboard/rest.py:862-871`, `dashboard/static/app.js:746-758` (P0/P1/P2 as "Needs attention", rest hidden), feedback buttons `app.js:764-767` |
| Phone (Discord DM) | `mag/phone_relay.py` | **hard budget `MAX_ASKS_PER_HOUR = 12`** (`phone_relay.py:54`), fail-closed timeout=DENY, exact-token decisions (`:37-53`), append-only log | the operator's phone |
| Scheduled patrol stack (08:00 / 08:30 / 09:00) | MagImproveDaily, MagCensusPatrolDaily (census deep check + meter patrol + fleet task doctor + fossil check, `census_patrol_daily.ps1:57-188`, worst-code-wins exit `:190-192`), MagFtsIndexDaily | batch; alert only on failure; appends documented "best-effort, loss-prone under concurrent writers" (`fts_index_daily.ps1:134-146`) | `logs/census_patrol.log` + attention.md block |
| The pile | `mag/state_snapshot.py:36` (`memory/pile/state_summaries.jsonl`, dedup by state_hash) | batch, zero interrupt | `tools/pile_classify.py:12` drains overnight with the local worker model |

The five channels already implement three physically different delivery models:
push-board (attention.md), priced-feed (ranker), interrupt-with-budget (phone). What is
missing is not a channel. It is **exchange**: the channels do not share a currency, so a
writer chooses a channel by convenience (biography.py chose the board) rather than by
price.

## 3. The failure mechanics, read from code (why bankruptcy recurs in hours)

Three concrete mechanisms, each citable:

(a) **Recency-FIFO consumption with unlimited low-value supply.** biography.py prepends
one ping per session-record first-write and truncates the tail at 40k
(`biography.py:525-526`). Consumers clip head-first. So consumption order is strictly
newest-first and eviction is strictly oldest-first. With ~120 pings per 3.2h (measured),
an alert appended at 08:30 has a visible window measured in minutes at the 600-char clip
and a survival window of ~3h at the full cap. The alert-class writers append at the TAIL
(`Add-Content`), i.e. they enter the queue at the position that evicts FIRST. The
census patrol's alert does not merely get buried; the truncate amputates it.

(b) **Lost-update race between classes.** biography.py does read-modify-write of the
whole file (`prev = att.read_text(...)` then `att.write_text(note + prev[:40000], ...)`,
`biography.py:525-526`) while the patrol scripts append with `Add-Content` between the
read and the write. The append is silently destroyed. The estate knows this and
documents it rather than fixing it: `fts_index_daily.ps1:136-146` calls attention.md "a
hot multi-writer file" whose appends are "best-effort, loss-prone under concurrent
writers". Notably Q-005's own collapse script DID use compare-and-swap
(`Q-005.md:46-49,63-64`), so the fix pattern already exists in the estate; the
highest-frequency writer simply does not use it. This is not alert fatigue, it is
**byte-level destruction of alert-class information by a noise-class writer**.

(c) **A priced feed with a dead price signal.** `mag/attention_ranker.py` is genuinely
good economics: score = 3*actionability + 2.5*impact + 2*urgency + 1.5*centrality +
1.2*novelty + uncertainty - 1.5*redundancy - wallpaper_cost (`attention_ranker.py:89-93`);
feedback may pin/mute/demote ordinary items but **cannot demote hard-band rules**
(`:231-243`, policy string at `:250`); it even prices the all-clear NEGATIVELY
(repo:ready gets `redundancy=.5, wallpaper_cost=.4`, `:137-144`), which is exactly
Herbert Simon's point that attention is conserved, so confirmation-of-good still costs.
Burst caps `failed[:3]` / `active[:4]` (`:166`, `:177`) prevent one class from owning the
feed. But the feedback ledger `memory/attention_feedback.jsonl` has never existed, so the
weights have never learned anything. The ranker is a static priority encoder wearing the
clothes of a market.

## 4. What the literature says, and where the estate already agrees

- **Herbert Simon (1971, "Designing Organizations for an Information-Rich World"):** a
  wealth of information creates a poverty of attention; the scarce factor is attention,
  so the design problem is allocation, not transmission. The estate's biography writer is
  a transmission solution (the record IS delivered, byte-verified, per Q-005) bolted onto
  an allocation surface (attention.md). Q-005's verdict, "the pings are delivered
  notifications, not open asks" (`Q-005.md:18-19`), is the diagnosis: delivery is fine,
  allocation is broken.
- **Signal detection theory (Green & Swets 1966):** a decision criterion flooded with
  false alarms shifts the operator's beta upward; the cost lands as misses. The 09-27
  TASK-DOCTOR alert evicted unread is the miss. The estate has its own version of this:
  AGENTS.md's census-carrier tripwire paragraph ("the retired 1,341 headline rode 12
  days stale ... no gate noticed") is the miss-shaped memory of exactly this dynamic on
  a different carrier.
- **Google SRE book (Beyer et al. 2016), alerting chapters:** page on symptoms, make
  every page actionable, use multiwindow multi-burn-rate alerting, and treat "too many
  pages" as an SLO violation of the human. The phone relay is the estate's pager and it
  already has the right shape: budget (12/h), fail-closed deny, log. attention.md is
  being used as a pager by biography.py while being shaped like a ticket queue.
- **Estate lineage:** `mag/decl_attention.py:1-52` folds Declarative Attention
  (arXiv:2609.02737) and SparDA (arXiv:2606.04511) into the doctrine that attention is
  "who pays the read, not what is read", with misses COUNTED, never silent. The operator
  surface violates its own estate doctrine: attention.md misses are silent. Prior
  receipts already hold the vocabulary: ASTRA_FOLD5_20260909.md ("the attention economy
  as the strangers' wage"), memory/working/deepseek_share_2fk77d79vdhzepjzqe.md:1032
  ("Every policy consumes an attention budget").

## 5. The design: currency, prices, a central bank, and bankruptcy law

Everything below is buildable from instruments the estate already has. No new surface is
required; the point is exchange between the surfaces that exist.

**(1) One currency: the attention token.** Define 1 token = one operator read of one
600-char block (the existing clip unit, `context_pack.py:620`). Budgets become counts of
tokens per surface per day: phone = 12/hour (already law, `phone_relay.py:54`), dashboard
needs-intervention list = the ranker's `limit` (already capped, `attention_ranker.py:252`),
standing board = K blocks/day, with K calibrated from observed reads, not asserted.
`mag/token_economy.py` already does exactly this accounting for model tokens
(chars/4, caps per file, `token_economy.py:42-55`); attention tokens deserve the same
ledger. Without a measured budget, "too many alerts" is unfalsifiable; with one, it is a
number that trips.

**(2) Prices by class, not by ping.** Q-005 cost a human session to triage 127 identical
pings; a class price costs one config row. Every writer declares (or inherits) a class
with a price vector feeding the ranker's existing formula: biography session-pings score
actionability ~0 (delivered notifications, durable trail in `biography/latest.md` and the
`_upsert_index_row` index `biography.py:485-500`), so they price P4 and P4 does not enter
the board at all; it goes to the pile (`state_snapshot.py`), which already has dedup and
an overnight local-model drainer (`tools/pile_classify.py`). Patrol alerts inherit
P1/hard-band, phone asks P0-only. Single-mouth law already exists and should be honored:
`improve.py:527-532` writes EXACTLY ONE line per alarm precisely because "two alarm
mouths is the fan-out disease"; every new writer should be refused a second mouth.

**(3) Exchange rules that stop the destruction.** Two mechanical laws, both one-line
auditable: (i) ALERTS PREPEND, NOISE APPENDS (alerts enter at the head where consumers
actually read; noise enters at the tail where the cap eats), and (ii) no writer may
read-modify-write the whole file; appenders append, prependers take the Q-005
compare-and-swap pattern. This closes mechanism (b) at its root instead of documenting
the loss, per the build-discipline law that a found design defect gets aligned, not
guarded (`AGENTS.md` build discipline).

**(4) The central bank: mechanical bankruptcy detection.** Bankruptcy must be detected
by a checker, never by human suffering. Rides the existing 08:30 patrol (it already
self-catches and is fail-open, `census_patrol_daily.ps1:113-120,155-157`): one new step
computes, per 24h window, (alpha) dominant-class byte share, (beta) alert-class survival
(attached block still present 24h later), (gamma) lost-update count (append succeeded,
block absent later, same as fts_index_daily.ps1:134-146 already worries). Fire when
alpha > 80% AND (beta < 1 or gamma > 0). Graduated response per estate law (WARN-ONLY
first, flip-to-enforce is an operator call, the census bullet's own grammar): WARN for a
day, then auto-demote the dominant writer's class one band, then after a week demote the
writer to the pile outright. The Q-005 collapse script is the precedent that a mechanical
actor may rewrite this file when verification gates the write.

**(5) The digest must speak even when green.** The 08:00/08:30/09:00 stack currently
emits on failure only, so "no news" is confounded with "surface is dark" (the census law
itself names darkness as a failure mode: "No START stamp for today: the surface is
dark", `census_patrol_daily.ps1:28-30`). SRE's multiwindow insight adapted: alert on
sustained burn, but ALWAYS emit the window. A one-line green digest each morning
("08:30: census ok N/M, meters ok, doctor ok x/y Mag* tasks, fossil ok, fts ok") costs
~15 tokens/day and converts silence from ambiguous to evidence. This is the cheapest
large win in the whole design: it makes the digest a trust-building instrument instead
of a fire alarm, which is what keeps the operator reading at all.

**(6) Mint the price signal.** The feedback loop exists end to end in code (buttons
`app.js:764-767`, endpoint `rest.py:869-871`, ledger `attention_ranker.py:16,63-79`,
application `:231-243`) and has recorded zero events ever. Two options, either is
legitimate: (a) the operator actually clicks, and prices become revealed preference;
(b) if clicks never happen, that is itself the finding, and prices should be derived from
behavior instead (did an inbox commit or a "Talk" follow the item within a session,
`operator_inbox.py:115` commit_guidance is already an implicit signal). An economy with
no price formation is a priority list; the difference matters because prices are what
let NEW classes of writer be admitted without a human re-tuning weights.

**(7) Bankruptcy insurance on the last channel.** The phone is the channel of last
resort; its budget (12/h) and fail-closed deny are correct and should be constitutionally
protected: only hard-band P0 may ask the phone, ever. A noise writer that reaches the
phone is the one failure this design cannot absorb, because an interrupt budget that
breaks is spent from sleep.

## 6. Priority order if only one thing ships

1. Stop biography pings on attention.md (their durable index already exists; P4 to the
   pile). This alone ends the 3-hour refill cycle. Cost: one condition change at
   `biography.py:510`.
2. Green one-liner from the 08:30 patrol (item 5 above).
3. Compare-and-swap for prependers / append-only for everyone (closes the lost-update).
4. Then the ledger and class prices; the ranker is ready for them today.

## 7. Falsifiers and what I did not do

- I did not start the dashboard or call `/api/v1/attention-ranked` live; the handler
  exists (`rest.py:862-871, 5241-5242`) and the frontend consumes it (`app.js:746-758`),
  but the check "ranker returns a healthy feed on live :8765" was NOT run. Reported as
  not run.
- The 3.2h refill estimate is one sample (12:40 triage to 15:51 measurement, same day);
  the true daily refill rate varies with fleet activity. The claim "recurs in hours" is
  supported; a precise lambda is not established.
- Which unhealthy task the 09-27 doctor named is in `logs/census_patrol.log` upstream of
  the three lines I tailed; I did not autopsy it (out of scope for this item).
- Literature citations (Simon 1971; Green & Swets 1966; Beyer et al. 2016) are cited
  from knowledge, not fetched this session; estate citations are all byte-read here.
- No em-dashes were used, per house law; no subprocess was spawned.
