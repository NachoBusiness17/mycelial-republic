# T1W3_N3_flock_netcode (anthropic/claude-opus-5.5, turn 1, channel: content)

<audit>

**Conditions:** This is a static read of the attached bytes only. Nothing was executed. Line numbers are UNVERIFIED, so each citation is anchored by file:function plus quoted bytes. The following are absent from evidence and marked UNVERIFIED: server.py, net_client.gd, game.gd, and tests/test_netcode_v0.py.

**(1) Desync: what diverges first**

TCP cannot lose or reorder, so the first divergence comes from stalls, not loss.

- **Unbounded fan-out.** rooms.py:broadcast does `peer["queue"].put_nowait(line)` with no QueueFull branch. A stalled reader accumulates ticks without limit.
- **Burst arrival collapses the timeline.** Arrival stamps come from the local clock (snapshot_buffer.gd:push `"t": t`), so a backlog lands with near-identical `t`.
- **Worst seam: the ring evicts events that were never crossed.** In push, `if _snaps.size() > CAPACITY: _snaps.pop_front()` runs with CAPACITY 32. Snapshots evicted before `crossed()` passes them lose their `events` permanently. No n-gap detector exists, since push accepts any `n > newest_n`. Exactly-once quietly becomes at-most-once.
- **Assumption:** crossed() is not called per push. This depends on net_client.gd and is UNVERIFIED.

**(2) What a hostile member can inject**

- **Room-spray.** The id space `^[a-z0-9][a-z0-9_-]{0,15}$` is 36 x 38^15, so effectively unbounded. Each new id triggers rooms.py:_create, which spawns:
  - one `MountainWorld`,
  - one log file,
  - an `Innkeeper` plus a memories file,
  - a pump via join_peer -> `ensure_pump()`.
- **Rooms are never reaped.** drop_peer only calls `stop_pump()`, and `self.rooms` never shrinks.
- **Routing amplification.** room_of_sid scans `for room in self.rooms.values()`, so every action server-wide costs O(rooms).
- **Capacity bypass.** The capacity law counts peers, not sids ("one connection may hold many sessions"), so one seat can mint unbounded sessions.
- **Bare-tick poison.** pump_once sends `self.broadcast(encode(payload))` unsealed. One forged on-path tick with a huge `n` makes push refuse every later real tick (`n <= ... return false`). The client freezes permanently.
- **Nonce gate:** UNVERIFIED, since no bytes were attached.

**(3) Deliverable: tests/test_event_ledger_parity.py (spec)**

1. Build `GameRoom("t", MountainWorld())` with `tick_interval=None`.
2. Seat a peer whose `asyncio.Queue` is never drained.
3. For t = 1..40, stage one `say`, then call `pump_once()`. Record each payload's events.
4. Drain the queue in one go into the Python mirror buffer, with every push stamped `t=0.0`.
5. Call `crossed(1e9, 0)` once.
6. Assert the multiset of delivered events equals the union of the 40 payloads' events.

<example kind="negative">Today: 8 ticks of events are evicted, so the assert fails.</example>

<example kind="positive">After the fix, the test passes. The fix is any one of:
- a bounded queue with drop-slow plus a resync,
- push refusing to evict uncrossed snapshots,
- a gap detector that requests a resync.</example>

<falsifier>If this test passes on today's tree, the eviction-loss claim is wrong. Likely causes would be that the mirror's CAPACITY differs from 32, or that crossed runs per push.</falsifier>

**Runner-up:** free-running clock parity. The harness feeds `sim_time = dec32(enc32(t * dt))` (flock_parity.py:run_teacher), while game.gd accumulates `sim_time += delta` (UNVERIFIED). This divergence is unmeasured.

</audit>
