# QUOTA LEDGER v0 — the window currency made visible (2026-09-30)

The lensing this fixes: dollars are metered to the cent (cost_rollup, IMP5: $135.71
lifetime) while the BINDING currency — the provider 5-hour window quota on
account:zai-individual-coding-plan — was invisible. Today it cost **6 wall
moments / 24 coded lane deaths** while the day's spend field reads **$0.18**.
The estate optimizes what it meters; this meters the window.

## Instrument

- Tool: `tools/quota_ledger.py` (ledger: fires, windows, walls, verdict) +
  `tools/quota_ledger_report.py` (receipt grep + rendering; split for the
  400-line ratchet cap, census_patrol_selftest pattern B2-248). Stdlib only.
- Tests: `tests/test_quota_ledger.py` — 10 passed (2026-09-30).
- Rerun live: `.venv/Scripts/python.exe tools/quota_ledger.py [--day
  YYYY-MM-DD] [--json]`. Exit 0 GREEN/AMBER day shape, 1 RED, 2 cannot verify.
  Violation ratchet: zero flags on both modules (checked --changed).
- Inputs (byte truth first): subagent records `~/.zcode/cli/agents/sess_*/
  agent_*/metadata.json` (createdAt = fire ts, lane = description,
  usage.totalTokens where recorded) + `output.txt` death payloads
  (`[1302]`/`[1308]`, reset time, provider request id); `DROP_LEDGER.jsonl`
  wave context (date-granular); watch/inbox receipts grepped as secondary
  evidence only.

## Live run @ 2026-09-30T21:07Z (final)

- Fires on the day: **321** (completed 288 / failed 28 / running 5); wall
  moments **6** (24 deaths coded 1302/1308)
- Current trailing-5h window: **75 fires**, 5 running, 0 walls in the last
  hour → current shape **GREEN**
- Peak rolling-5h window: **138 fires** at 12:28Z; peak in-flight width
  **26 lanes** at 00:38Z
- Tokens (ROUGH): 662,545,165 recorded on 288 fires + 33 unrecorded × mean
  2,300,504 ≈ **738,461,797** total (cache-inclusive, fire-time attributed)
- **Day-shape verdict: RED** (26-wide burst + a 1308 window kill; current
  dispatch signal GREEN)

### Wall log (byte truth: failed-agent death payloads, UTC)

| wall moment | code(s) | lanes dead | window ended |
|---|---|---|---|
| 00:20:57 | 1302 | 4 (W3 skill_fired, W3 ledger registry, W2 mountain clone-proofing, W3 realign) | anchor unknown (no reset payload) |
| 02:21:03 | 1302 | 1 (W3l grok sessions parser) | anchor unknown |
| 09:17:13 | 1302 | 2 (Z1 production weld, Z8 mountain push) | anchor unknown |
| 12:07–12:13 | 1302+1308 | 14 (AH1-4, AH6-10, AH13-14, AH16-17, AH19) | **window 15:54→20:54 provider clock** (reset payload byte) |
| 17:37:03 | 1302 | 2 (LM8 handshake, IMP4 query tool) | anchor unknown |
| 18:13:04 | 1302 | 1 (LM2 DFHack reveal) | anchor unknown |

The 12:13Z moment is the 20-wide AH fire into the 5-hour wall (receipt:
`watch/inbox/last_mile_20260930/AH_REFIRE_QUEUE.md`, "13 lanes dead + AH10
died earlier on 1302" — bytes confirm 13×1308 + 1×1302 at 12:07). Four more
IMP lanes died 17:30Z on bare "Model request failed." (no code — wall-suspect,
NOT counted). Receipts corroborate: MICKEY17_WAVE_LEDGER_20260929.md lanes
1-5, DAY_SYNTHESIS_20260929.md ("~19-20 wide in one burst → 1302 killed 4 in
~6 minutes; staggered 12+12 → 24/24 landed, zero 1302s").

### HOLD recommendation (measured envelopes, receipts-cited)

- **GREEN**: 8-12 sustained (AFTERPARTY_CLOSE_20260926 B2-476; today's
  staggered steal waves: 24/24 landed zero 1302s at 12+12).
- **First 1302s**: ~15-wide (envelope-probe 9/25). **RED**: 19-20 at once.
- **HOLD rule v0**: no new waves when trailing-5h fires >= 16 OR any
  1302/1308 death in the last hour (post-burst decay law); stagger 6-8;
  never 19-at-once.

## Honesty (v0 limits, named)

- Token totals are ROUGH: usage bytes exist only for completed subagents —
  the lanes that died ON the wall carry none (exactly the blind spot);
  cache-inclusive; fire-time attributed; main-session turns invisible.
- The exact instrument is provider-side: per-response usage fields plus the
  account usage snapshot inside every 1302/1308 payload (request ids
  embedded, e.g. `[202609302013252ffd3407af7d46b2]`) would reconcile exact
  per-window usage. The estate cannot read that meter from inside the car.
- Provider clock offset (UTC+8) inferred from 14 byte-consistent request-id
  stamps on 2026-09-30; wall UTC times come from harness completedAt bytes,
  not the inference.
- The 5 1302-only walls carry no reset payload, so which provider window
  they ended is unknowable harness-side (logged anchor-unknown, never
  guessed).

Landed: `tools/quota_ledger.py`, `tools/quota_ledger_report.py`,
`tests/test_quota_ledger.py`, this receipt.
