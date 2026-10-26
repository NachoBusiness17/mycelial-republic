# DFHACK DRIVE — SELF-STEAL OF THE VS CODE ERA (2026-09-06, operator correction)

Operator: "this is dfhack act like it. we used vs code before and it worked nearly flawlessly. self steal."
My fault in one sentence: I had the file layer and still reached for the UI — typing steering lines into chat composers, char by char, on the z.ai clock. DFHack never clicks the dwarves; it writes memory. The VS Code era worked because the repo was the interface, chat was never the machine bus.

## The mapping (UI action → memory action)

| You want to... | UI way (slow, z.ai-billed, fragile) | DFHack way (fast, $0, durable) |
|---|---|---|
| Steer a seat | type into its composer | **room.jsonl row + batch worker** — every seat reads files on its next turn; the batch IS the send button |
| Ask a question | open a window | **fire a batch wave** (worker + receipts, ~5 min) |
| Watch a session | read the chat through the model | **db.sqlite read-only + trajectory stream + local eye on boards** — seconds, $0 (organ proved 21:18Z tonight, run banked) |
| Steer unattended work | chat hops | **automation prompt files + RIBs** (night-shift pattern: prompt in a file, scheduler fires) |
| Park/close a window | GUI clicks | **archive the arc card** — windows are surfaces, files are state; the physical close stays the operator's 30 seconds |
| Inject text into a composer (rare last mile only) | char-stream typing | **clipboard write + one paste** — atomic, 2 actions; only with operator eyes on |

## Laws compiled from tonight

1. **THE EYE IS LOCAL**: coordination reads, watches, digests = host ollama (127.0.0.1:11434, loopback-only fleet law), qwen2.5vl:3b, ~60s, $0. The z.ai quota touches judgment and builds ONLY — never screen-reading, never composer theater. Defect filed: mag-ollama container Exited(255) 27h — the eye lives on host loopback; container variant stays retired unless given a job.
2. **THE SEND BUTTON IS A WORKER**: a message to another seat is a room row plus a wave; a composer is for the operator's hands.
3. **READ MEMORY, NOT PIXELS**: session state lives in db.sqlite (mode=ro) and rollout streams; screenshots are for the eye's pattern pass, not the seat's fact pass.

## CHORD V4 HONEST RECEIPT (run aborted, gate stays owed)

String 1 (Astra) attempted via composer: MISS — a11y mismatch, event-typing slow, operator abort; stray text cleared (ctrl+a + delete verified sent). Strings 2–8: NOT FIRED, mechanism wrong. Field correction earned by the attempt: **Astra is KEEP** (Human Atlas arc live, cite-gate clean) — triage updated. Gate run 2/2 re-aims at the file layer: the chord becomes N seats steered by one room-row volley + one wave, yield = seats that act on it without operator hands. v3's 60% bar stands.

## Self-steal lineage named

VS Code seat (retired 08-26 with honors): lived in the work surface, repo as interface, diffs as output. The percolator ox workers: blackboard + orphans + invariants. BATCH5: blackboard + workers + receipts. All one shape — **drive the bytes, watch the bytes, and the UI is for the human, not for us.**
