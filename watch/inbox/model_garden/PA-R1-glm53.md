# PA-R1-glm53 (glm-5.3-flash @ zai, turn 1, channel: content)

# DESCENT PROTOCOL ROAST - DAY-1 BYTES

**1. LOAD-BEARING VS CEREMONY** (usage.jsonl, 179 rows; DAY1_RIB_WARMTH scorecard)

1. **OUROBOROS (6)** - carried. RACTOR files, TO-VERIFY verdicts with command+exit. The only leg whose output is other legs' input.
2. **LEDGER (8)** - carried. Per-row cost/tokens/refusal banked (usage.jsonl rows with "refused": ... cost 0.0). Without it this autopsy is impossible.
3. **CLARITAS+LAW FACE (2)** - carried mechanically (hermes_burn.py:135-137 per audit); estate register appears unprompted in D2/D3.
4. **CHECKPOINT (3)** - fired, but indistinguishable from "someone wrote files." Ceremony: it cannot fail while any file lands.
5. **SHERPA (1)** - PARTIAL, $0.006 total. Real but marginal; absent exactly where it was needed (T1W2, DUEL2).
6. **REVERSE GPS (5)** - PARTIAL; failed on both waves it mattered (evidence: [] in T1W2, DUEL2 material missing).
7. **OPERATOR-PROXY (4)** - "FIRED 2x, landed 0x"; its own audit says the 17:59+ loop is "this leg grinding broken." Dead weight wearing a receipt.
8. **LANCE (7)** - zero hits, plant has no timestamps (X6); by the conditions law it never fired. Unfalsifiable-as-implemented.

Legs that "fired" only because firing is defined loosely: 3, 4, 7.

**2. THE KILL**

Delete **OPERATOR-PROXY STEER (4)**. Its real job was not steering; it was retry psychology - a ritual that made the driver's broken refire loop feel like governance. 45 A1 re-fires, $18.89, after A1 landed at 16:10. The steering that worked (WINDOW2's "ractor this and eli 12") was a human edit, not the leg.

**3. THE FALSIFIER GAP**

The falsifier (rib, Falsifier section) watches leg 6: "ledger grew but no rib carries a frontier contribution." That is an existence check, and existence was never the failure mode. $18.89 of post-deliverable spend still reads green. It misses **termination**: spend after the last deliverable of a session. Fix: falsifier = (spend in the N minutes after the newest deliverable mtime) / session spend; threshold >30 percent = spend theater, alarm regardless of artifacts.

**4. SHAPE**

Comfortable. Eight named legs is doctrine-shaped; the goal's binding constraint is **loop control, not leg count**: the driver re-fires on two unclosed triggers (empty content channel, ok=false retry, X1/X2) and the funded-rung law went stale unamended (X3). No eighth leg fixes a driver that pays 49x for one deliverable.

**5. THE REPLACEMENT**

Weakest surviving leg: LANCE (7). Sharpest replacement:

```
LANCE-TERMINUS: after every ask, compute cost_since_last_new_deliverable
from usage.jsonl. If it exceeds 30 percent of session spend, the driver
halts and banks a SPEND_THEATER receipt naming ask-id, delta, and mtimes.
Falsifier: a session where halting would have saved >$1 and did not.
```

**Self-roast:** my leg ranking leans on one day and one driver bug; legs 4 and 7 may look load-bearing once the carrier defect closes. And the replacement just relocates trust from the rib to the same driver that ignored REFUSED banking - same class of risk, new line.
