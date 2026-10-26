# Congestion costs time and calm — operator record 2026-08-30

**Who:** Nacho (operator). **Presented, not interpreted.**

## The lesson

Congestion costs more than money. It costs time and calm.

Cheap tokens on a 1-concurrency pipe are not cheap. Waiting, 429s, `NO_REPLY`, `next=none`, and the fear of touching the mill are the bill.

## Receipts this window

- OpenClaw `zai/glm-4.7-flash` 429, failover `next=none` (OUTBOX `ext-a214146281`)
- Salon thread `moonshot`: NVIDIA `quota exhausted` both turns; Groq/DeepSeek posted
- Usage tail: Groq 215 calls / 47 ok — congestion, not price
- DeepSeek mill ~3169 calls almost all ok — the door that was actually open

## Law

Launch N only if N doors are open. Fan-out on a locked lane is 50 people in one doorway.

Dollar cache-hit is not the metric. Calm-to-FILE is. If the operator is afraid to use it, the mill already overcharged.

## Falsifier

A 50-way salon that returns on open lanes, no wait-spin, and a knot or patch FILEd without a second try.
