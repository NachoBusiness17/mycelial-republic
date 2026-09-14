# SOURCE DIGEST — the z.ai Trajectory window vs the fleet's rib structures (Sep 5, 2026)

> **[AUDIT-TYPED 2026-09-08]** status: STAGED · claims: the Trajectory window's step anatomy (call hash, three-channel grouping, timing, verbatim reasoning) is real and adoptable as the canonical record shape, upgradable from the local db's 9,305 reasoning parts — SUPPORTED for the anatomy observation (75,023-byte sample pinned by sha256) / UNPROVEN for the re-joiner · falsifier: a db re-join failing to reconstruct input→tool→output→reasoning chains from message_id/session_id/sequence, or the vendor dropping the export door

Preserved sample: corpus/training_materials/zai_trajectory_window_sample_20260905.txt
(sha256 efd424dd6ff3caef43bbda2ec98e3ffa09b485754326075adc58a9abd858d517, 75,023 bytes).
It is the z.ai surface's Trajectory-window export of a REAL fleet conversation (the orchestrator
arc, 09-05). Operator order: "run a salon on how we can better incorporate the Trajectory window
within z.ai as a way to better understand our rib file structures and adapt for thinking we have
already harvested. This should change the way we interact with z.ai entirely. WE can draw this
data from every one of our previous interactions within the surface and learn how to extract the
same from every seat."

## The Trajectory window's observed anatomy (from the preserved sample)
One conversation renders as a sequence of STEPS. Each step shows:
- CHANNEL LABEL: "Input" / "Tool result" / "Output" (three-line header per step)
- TIMING BLOCK: "13.4s · 9/5/2026, 9:49:10 AM" + "Collapse" toggle (duration + timestamp + expand)
- TOOL NAME when a tool step: "Write", "Bash", "CronList"...
- CALL HASH: an opaque 24-hex id per step (e.g. 305501de0d7240dfab0e5d8f) — z.ai's handle for
  the exact call (their server-side correlation id)
- ROLE BLOCKS: "Assistant" → "Reasoning" → verbatim thinking text; "User" → message text;
  "System" → injected context (we can SEE the Mimosa hook injection rendered as a System block)
- TOOL RESULTS inline: file-created confirmations, command stdout, JSON payloads (CronList dump
  rendered whole)
- The model's Reasoning text is EXPOSED VERBATIM in the surface — the vendor chooses to show it.

## What we already harvest (the local door)
- ZCode db: ~/.zcode/cli/db/db.sqlite — session/message/part tables; part.data holds typed
  records: text / reasoning / tool (with state.input + status). We banked 9,305 reasoning parts
  / 17.3M chars from the Lite burn ("thought-bank", db part type=reasoning). Harvest script +
  arena-bench + claim-repair already exist.
- model_usage table: per-call tokens, timing, cache reads, finish_reason, error classes.
- What the local db LACKS that the trajectory window SHOWS: the step-hash correlation (z.ai's
  24-hex call id), the Input/Tool-result/Output three-channel grouping, and the surface's own
  envelope decisions (what the vendor renders vs keeps dark).

## Our rib structures (the things to align)
- memory/rib/ — RIB_LANE_WINDOW_BOOT (window-staff boot prompts + tier law), the frozen
  instruction envelope (FROZEN_RIB) — our own wrappers around prompts/thinking.
- The FROZEN_RIB lesson (receipted 08-27): the envelope consumes ~100 tokens before the answer
  — envelopes are REAL overhead and must be measured.
- Chain: memory/biography/verkle_chain.jsonl (7,243 knots, signed, OTS-sealed nightly) — our
  durability layer for exactly this kind of structured record.

## The known economics (why this matters now)
- The 300M weekend pool burned to zero; doctrine: the burn is training data — every trail is
  corpus. The thought-bank holds thinking BLOBS; the trajectory schema could upgrade them to
  INPUT/TOOL-RESULT/OUTPUT CHAINS = real supervised fine-tuning shape (what preceded the
  thinking, what the thinking produced, what the tools returned).
- 240:1 refeed tax measured on the free plan — envelope overhead is the enemy; a trajectory-
  aware envelope is a measured envelope.
- Multiple seats exist; the same part-stream schema runs under every seat — one extractor,
  every seat.

## The salon question
How does the fleet incorporate the z.ai Trajectory window so that (A) our rib file structures
adopt the trajectory schema (step hash, three-channel grouping, timing, envelope layers) as the
canonical record shape for harvested thinking; (B) the already-harvested 9,305-part thought-bank
is ADAPTED (upgraded from reasoning blobs to input→tool→output→reasoning chains — re-joinable
from our own db because we hold message_id/session_id/sequence); (C) an extractor draws the same
trajectory data from EVERY previous interaction on the z.ai surface (their export/rendering door)
and from EVERY seat's local db — one schema, all seats; (D) it changes how we interact with z.ai:
what we now know the vendor keeps, renders, and correlates — and what that means for how we
prompt, harvest, and structure every future call.

HARD RULE: answers land as code — the trajectory record schema (dataclass/JSON), the re-joiner
that upgrades the thought-bank, the extractor interface for surface + seats, with falsifiers.
Prose per artifact capped at 3 sentences.
