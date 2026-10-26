# CAPABILITY GATE LEDGER (handshake.v1)

A human-unlocked capability is not "available" — it is **on loan against a promised
use**. One JSONL line per gate records the unlock, the promise, the first real use, and
an honest status. Strong receipt discipline: the strongest in the source estate.

## The record (one JSONL line per gate)

```json
{"schema": "handshake.v1", "gate": "<name>", "unlocked_at": "<date>",
 "unlocked_by": "<who>", "what": "<capability unlocked>",
 "promised_use": "<what it was unlocked FOR>",
 "first_use": "<date or null>", "first_use_receipt": "<what actually ran, or omit until first use>",
 "status": "<PENDING|UNPROVEN|PARTIAL|OPEN|USED|DRIVEN>"}
```

## Field rules

| field | rule |
|---|---|
| `promised_use` | written at unlock time, by the unlocker — the loan terms |
| `first_use` / `first_use_receipt` | filled only by a real run; the receipt names what executed and where its record landed |
| `status` | `PENDING` (not unlocked) · `UNPROVEN` (unlocked, never used) · `PARTIAL` (used, parts failed) · `OPEN` (used, close-action owed) · `USED` (delivered once) · `DRIVEN` (in standing operation) |

## The status vocabulary is the value

"PARTIAL — F2 image gate still pending", "OPEN — close prompt still owed", "stays
STALLED-flagged until a full send+reply drive": the ledger records what the capability
CANNOT do yet, next to what it can. A gate without a status is a door off its hinge.

## Format drift to repair (carry this fix)

The source ledger's newest entry (line 7 of 7) **drops the `schema` field** — the one
field every reader keys on. Template law: `schema` is mandatory on every line, forever;
a validator that rejects schema-less rows would have caught this at write time. Line
count of the source file re-verified this session: `wc -l state/handshakes.jsonl` → **7**.

## Receipt

- state/handshakes.jsonl (estate) — all 7 lines read this session; the six statuses above
  all appear verbatim; the six-gate example set: staff-room front ends, android body,
  phone tunnel, device login, paid map seat, app instance, fleet-control top-up.
