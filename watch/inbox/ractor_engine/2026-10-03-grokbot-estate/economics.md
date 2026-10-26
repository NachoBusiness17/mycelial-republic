# economics.md - ractor lens: economics (2026-10-03 grokbot-estate run)

Lens: economics (EV-per-cost pricer; jacket: burning without a banked usage
line). No paid calls made. Verdicts: TRUE / FALSE / THEATER / UNVERIFIED.

## Findings

E1. Unblocking cost. Direction TRUE, dollars UNVERIFIED. 375 janitor spawns
in about 7 days (about 54/day) are free today only because they crash at
import. autonomous_task_loop polls every 60 s (mag/ghost.py:1314), one quest
per cycle (:1470-1472), dedup only 60 minutes per signature
(mag/ghost.py:1296, 1299-1311). After the health fix each spawn becomes a
metered deepseek-v4-flash call (configs/cost_rates.yaml:9-15) with a 300 s
timeout. No usage rows exist to price a run, so per-run cost is OWED.

E2. kpi.jsonl growth. TRUE. 753,736,154 B at 10/02 07:36 ET
(2026-10-02-dogfood-48h/SYNTHESIS.md:67-69) to 790,310,798 B at 10/03
18:39 ET: about +36.6 MB in about 35 h; the rotation move (that synthesis's
move 3) is still unpaid.

E3. Backup disk. TRUE. 18 chain backups today = 129,621,240 B; every future
logon adds one (operations O7).

E4. Stealth driver dead routes. TRUE. 59 of 216 ticks today burned on two
dead free routes; probe20 and rumor topics produce nothing on 216/216. Cost
is wall time and log bytes, not dollars.

Tally (this lens): TRUE 3, UNVERIFIED 1 (E1 dollars).

No em-dash bytes. Filed by the economics lens.
