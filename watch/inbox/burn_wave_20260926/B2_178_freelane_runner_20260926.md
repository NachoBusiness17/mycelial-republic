# B2-178 receipt: free-lane tandem burn runner, 2026-09-26

## Verdict

LANDED AND RUNNING. `watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py`
(sha256 7a3b45712dba0636...) is a self-sufficient loop driver burning estate
work through the 8 alive free lanes measured by B2-04 (groq gpt-oss-120b,
openrouter key1+key2 stealth/space-bunny-alpha, nous-hermes stealth,
together DeepSeek-V4-Flash-0731, cohere command-r-plus-08-2024, zai Pro+Lite
glm-4.7-flash). It launched at 15:05 EDT with a 57,375-item real-estate queue
and runs to the 23:30 local deadline, where it files close totals
(FREELANE_BURN_CLOSE_20260926.md) plus its own LEDGER.jsonl row without a
sitter. Smoke run (150 s, 12 items, SMOKE-suffixed artifacts only) proved
every lane alive and all four estate tasks producing parses before the real
launch. Privacy law held by construction: caption text, filenames, and file
contents never leave the machine; only LINKS titles/domains (public) travel.

## Evidence

- Smoke close (FREELANE_BURN_CLOSE_20260926_SMOKE.md): 13 calls, 13x200,
  6,736 usage-reported tokens across 8 lanes; counters match the per-call
  usage blocks in B2_178_events_SMOKE.jsonl line for line.
- Live liveness check at 15:07 EDT (B2_178_counters.json): groq 15 calls,
  openrouter-k1/k2 31+31 (15.5 RPM each, inside the 20 RPM operator shape),
  nous 12, together 11, cohere 12, zai-pro 1, zai-lite 4; 117 calls, zero
  non-200, 32,289 usage-reported tokens. Openrouter pace 15.5 RPM measured
  from B2_178_events.jsonl timestamps, under the 20 RPM brief shape.
- Queue manifest (B2_178_queue_manifest.json): links_title_norm 210 (titled
  rows of watch/inbox/LINKS.jsonl, sha256 b95a-verified source CAPTION
  ledger inside), links_dedupe 27 candidate pairs (same-canonical plus
  title-token jaccard >= 0.45; B2-06 already flushed the silent dupes, so 27
  is the honest residual), caption_enrich 2,726 (every CAPTION_LEDGER
  row), corpus_class 54,412 files (non-.git corpus walk), total 57,375.
- First real launch crashed in ntpath.relpath on a corpus reparse point
  resolving to the NUL device namespace ("path is on mount \\. nul"); the
  walk now guards every path call and counted exactly skipped_device_paths 1,
  so the crash cause is a measured estate fact, not a guess (fix comment in
  the runner names this receipt wave).
- Rate shapes honored in code: groq interval 8 s (1K RPM ceiling never
  approached) plus hard TPD guard 185,000 tokens (under the 200K TPD brief
  shape) that disables the lane with a named reason; openrouter 3.5 s
  spacing on both keys; zai lanes space 10 s and on 429 body "1305" wait
  15 s and retry up to 3 attempts (B2-04 re-measured lore); 429/5xx requeue
  once, 401/402/403/404/410 disable the lane.

## Work done

1. Read B2_04_provider_health_20260926.md, B2_04_probe.py/_probe2.py and
   results JSON; took the 8 alive lanes, model ids, and the 1305 discipline
   from measured bytes, not from configs folklore.
2. Surveyed the estate inputs: LINKS.jsonl (338 rows, fields url/canonical/
   title/seq), CAPTION_LEDGER_20260926.jsonl (2,726 rows, B2-12), corpus/
   walk (54,412 non-.git files, 18 top-level subdirs).
3. Built the runner (stdlib only, one thread per lane): four estate tasks
   with privacy-scrubbed prompts (links_title_norm: public titles only;
   links_dedupe: title/domain pairs; caption_enrich: kind/ext/status/size
   bucket/caption-length bucket/has-url only, caption text never in the
   prompt by construction; corpus_class: subdir + extension + size bucket
   only, filenames never sent). Per-lane counters: requests, per-status,
   bytes_sent, bytes_recv, usage-reported prompt/completion/total tokens
   (the falsifier), latency, no_usage. Every call appends a line to
   B2_178_events.jsonl; outputs land per task in B2_178_out_*.jsonl.
4. Hourly receipts: FREELANE_BURN_H<H>.md written at each hour bucket
   (H15 landed at launch; H16..H23 follow) with window delta counters, queue
   state, and trimmed real output samples; close totals + LEDGER row fire
   automatically at 23:30 (row only when not --smoke).
5. Smoke run --smoke (150 s): verified 8/8 lanes 200, all four tasks parsing,
   hourly writer, close writer, empty-content retry on zai-pro (reasoning
   token sink, retried once then landed with note). Smoke artifacts carry
   the _SMOKE suffix so the real falsifier files stay clean.
6. Launched the real run to 23:30 via .venv/Scripts/python.exe (background,
   stdout log B2_178_runner_stdout.log); verified liveness from
   B2_178_counters.json, not from intent.

## Falsifier

This verdict dies if: (a) per-lane token counters in
B2_178_counters.json / FREELANE_BURN_CLOSE_20260926.md disagree with the
sum of usage blocks in B2_178_events.jsonl (recompute by jq-style sum over
usage.total_tokens per lane); (b) any outbound prompt string in the events
or code contains caption text, a corpus filename, or file contents (the
prompt builders in B2_178_freelane_runner.py take metadata fields only;
check prompt_for()); (c) the close file claims work for a lane whose
counters show 0 calls; (d) the hourly receipts show fabricated numbers (all
fields are printed directly from state.snapshot(), read the code path);
(e) openrouter counters exceed the 20 RPM shape over any hour (events
timestamps give the real rate); (f) groq tokens_total exceeds 200,000 (the
185K guard must fire first, leaving a named disabled reason).

## Bibliography closed

- watch/inbox/burn_wave_20260926/B2_04_provider_health_20260926.md,
  B2_04_probe.py, B2_04_probe2.py, B2_04_probe_results.json,
  B2_04_probe_results2.json (lane roster, model ids, measured shapes)
- watch/inbox/LINKS.jsonl (338 rows), watch/inbox/CAPTION_LEDGER_20260926.jsonl
  (2,726 rows, B2-12), corpus/ walk (54,412 files)
- watch/inbox/burn_wave_20260926/B2_06_link_dupes_20260926.md (dedupe
  conventions, explains the 27-pair residual)
- watch/inbox/burn_wave_20260926/QUEUE.md header law block (self-feed,
  claim, restore-guard laws); memory/burns/LEDGER.jsonl (row schema)
- This wave: B2_178_freelane_runner.py, B2_178_queue_manifest.json,
  B2_178_counters.json, B2_178_status.json, B2_178_events.jsonl,
  B2_178_out_{links_titles,links_dedupe,caption_enrich,corpus_class}.jsonl,
  FREELANE_BURN_H15.md (and later hourly buckets),
  FREELANE_BURN_CLOSE_20260926.md (auto at 23:30), B2_178_runner_stdout.log,
  _SMOKE-suffixed smoke artifacts. No external sources.
