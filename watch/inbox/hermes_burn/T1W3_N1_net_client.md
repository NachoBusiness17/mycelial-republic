# T1W3_N1_net_client (anthropic/claude-opus-5.5, turn 1, channel: content)

## Stranger Audit: W1 transport and netcode v0

**Instrument and conditions:** These findings come from reading the attached bytes. No Godot was executed. Line numbers for `snapshot_buffer.gd` are hand-counted. Other locations are cited by quoted bytes, with line numbers UNVERIFIED.

### (1) Hostile peer in 3 moves

| Attacker | What they get | Bytes |
|---|---|---|
| **Sniffer** | The password and sid in cleartext. Whether a sniffed sid can be replayed depends on server-side sid binding, which is UNVERIFIED because `server/` is not attached. | `_send({"op": "hello", "user": user, "pass": password})` (scripts/net_client.gd) |
| **Spoofed MOUNTAIN_SERVER** | The connection is retargeted silently, and the client sends its credentials to the new endpoint unprompted. Malformed input such as `"h:x"` or IPv6 parses to port 0. | `port = int(parts[1])` (scripts/net_client.gd) |
| **Hostile server** | It can send a huge tick number, after which every later tick is refused, freezing the render permanently. It can also forge `winner:true` or `BAD_AUTH`. | `n <= int(_snaps[...]["n"])` (snapshot_buffer.gd:53); `float(nodes[name])` unguarded (network/net_client.gd) |

The rubber-band law is a counter, not a gate. `rubber_band_frames += 1` runs, and then `ticked.emit(..., nodes, ...)` emits the frame anyway. Whether NaN values slip past every comparison is UNVERIFIED.

### (2) Load and race, ranked

1. **REAL, HIGH: eviction before scan.**
   - `super._process` drains every available byte into the ring in one frame, all stamped with the same `_clock`.
   - Any burst larger than 32 triggers `_snaps.pop_front()` (snapshot_buffer.gd:63) before `_render_tick` runs.
   - `crossed()` iterates only `for s in _snaps:` (snapshot_buffer.gd:121), so the evicted events and winner are lost silently.
   - The test oracle itself admits the assumption: "capacity 32 vs ~6 ticks of 100ms lag: never" (test_netcode_v0.py). That holds only at steady cadence.
2. **LATENT, MEDIUM: rewind freeze.** This is unreachable today because the transport has no reconnect ("no reconnect", scripts/net_client.gd header). A server restart therefore surfaces as `_down`, not as a rewind. It becomes real the day v1 adds reconnect, and it is already real as the hostile-server pin above.
3. **DEFENDED, LOW: zero-span bursts.** `frac := 0.0 if span <= 0.0` (snapshot_buffer.gd:95) prevents a NaN. The cost is visual only: a snap instead of a glide.

### (3) The one test

```python
def test_burst_after_stall_loses_nothing():
    nc = InterpClient()
    nc.feed_tick({"n": 1, "nodes": {"a": 0}, "events": [], "winner": False}, 0.0)
    nc.feed_tick({"n": 2, "nodes": {"a": 0}, "events": [], "winner": False}, 0.8)
    nc.render(0.9)                       # cursor reaches n=2
    for n in range(3, 43):               # 40 ticks drained in ONE stalled frame
        nc.feed_tick({"n": n, "nodes": {"a": n}, "events": [f"e{n}"],
                      "winner": n == 3}, 30.0)
    nc.render(30.0)
    nc.render(30.2)                      # resume
    assert nc.events_delivered == 40     # today: 32 (e3..e10 evicted)
    assert nc.winner_fired == 1          # today: 0
```

**Negative example:** `test_live_300_ticks_interpolation_no_rubberband` passes today because it feeds exactly one tick per stamp and never bursts.

**Falsifier of this deliverable:** If this test passes on today's tree, finding (2.1) is wrong.

**Conditions on the test:**
- It runs on the Python mirror, not on the `.gd` file.
- The winner assertion assumes the server's winner flag is non-sticky, which is UNVERIFIED. The events assertion is unconditional.

**Fix direction:** Make `push` return the snapshot it evicts, and have the client move that snapshot's events and winner into a pending queue that `crossed()` flushes.
