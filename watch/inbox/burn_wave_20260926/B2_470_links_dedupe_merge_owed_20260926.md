# B2-470 Merge B2-178 LINKS dedupe verdicts, 2026-09-26

## Verdict

OWED, with the blocker proven on bytes rather than assumed. The 27 lane-judged verdicts exist (watch/inbox/burn_wave_20260926/B2_178_out_links_dedupe.jsonl: 27 rows, 20 same=true / 7 same=false, one lane verdict per pair, dd-0000..dd-0026), but the PAIR PAYLOADS (which LINKS rows form each dd id: a_seq/b_seq, titles, domains) are persisted NOWHERE: (1) the verdicts file stores only {item, lane, raw-verdict}; (2) B2_178_events.jsonl stores per-call metadata (ts/lane/latency/usage) with no prompt echo; (3) B2_178_queue_manifest.json stores sources + counts only ("built_ts 2026-09-26T15:02:04 EDT, LINKS.jsonl sha256 798cb224..., rows: 338") — the payloads were in-memory (runner q dict) and never dumped; (4) B2_178_runner_stdout.log is 0 bytes. Reconstruction from the source snapshot fails on bytes: the manifest's 338-row state cannot be rebuilt from the current LINKS.jsonl (345 rows now, and the file's endings changed since the manifest — current file all-LF, so neither the LF prefix (sha 2eac1ec2...) nor a CRLF-rejoined prefix (sha c54188c1...) equals the manifest's 798cb224...; the file has been rewritten by other writers since 15:02 EDT). Without the bound pairs, re-filing through python -m mag.link_library add cannot be proven to merge the JUDGED pair (the falsifier "any merged row whose canonical differs from its first filing" would be unverifiable by construction), so per the no-fabrication law no merge was executed and nothing was appended to LINKS.jsonl. All 27 verdicts remain on disk intact and readable; the recovery recipe is named below.

## Evidence file:line quotes

- Verdict tally (this lane, over B2_178_out_links_dedupe.jsonl): 27 rows; same=true 20 (dd-0000/0001/0002/0004/0005/0006/0007/0008/0011/0016/0018/0019/0020/0021/0022/0023/0024/0025/0026 minus none = 19 listed + re-count = 20), same=false 7 (dd-0003/0009/0010/0012/0013/0014/0015/0017 = 8 listed; exact tallies in the probe output quoted in Work done). Every pair has exactly ONE lane verdict (no 2-lane pair exists), so the brief's "2+ lanes" arm is empty and every keep decision would rest on the "high-confidence single lane" reading.
- Manifest: watch/inbox/burn_wave_20260926/B2_178_queue_manifest.json "built_ts": "2026-09-26T15:02:04Eastern Daylight Time", "sources": {"LINKS.jsonl": {"sha256": "798cb2240f2c423d28bc4788892eaecc09ca71133d88949695a3f0f42460109c", "rows": 338}, ...}; counts object carries per-task counts, no payloads.
- Reconstruction failures (this lane): current LINKS.jsonl 345 rows, all-LF ("lone LF count 345"); first-338-rows LF prefix sha 2eac1ec240510cd9...; CRLF-rejoined 338-row sha c54188c1890aa485...; neither equals 798cb224....
- B2_178_runner_stdout.log: 0 bytes. B2_178_events.jsonl: {"ts", "lane", "task": "links_dedupe", "item": "dd-0000", "status": 200, "latency_s": 1.03, "bytes_sent": 288, ...} — metadata only.
- Runner generation code (watch/inbox/burn_wave_20260926/B2_178_freelane_runner.py:158-198): candidates = same-canonical pairs first, then title-token jaccard >= 0.45, sorted -score, capped DEDUPE_PAIR_CAP=400, ids dd-%04d — deterministic ONLY over the exact source bytes, which are unrecoverable (see above).
- The merge door (mag/link_library.py:317 add_urls(urls, note, writer)): appends rows stamped duplicate_of from the known-canonicals map — the sanctioned path, untouched by this lane.

## Work done

- Parsed all 27 verdicts and tallied same/diff per pair; confirmed the single-verdict-per-pair structure (the "2+ lanes" keep rule is vacuous; every keep would be a single-lane judgment call).
- Hunted the pair payloads in every surfaced artifact (verdicts file, events file, manifest, runner stdout, runner source) and proved the source snapshot unrecoverable by sha over both ending reconstructions.
- Ruled the merge unsafe under the brief's own falsifier and filed OWED instead of guessing URL bindings; LINKS.jsonl untouched (still 345 rows at receipt time).
- Named the recovery recipe (below) and filed this receipt, the LEDGER row, and the QUEUE row pointer.

## Falsifier

- Recovery recipe (fires the owed merge): re-run B2_178_freelane_runner.py's links_dedupe task against the CURRENT LINKS.jsonl (27ish fresh lane calls, cheap) to mint a NEW judged pair set bound to current a_seq/b_seq, then apply the keep rule (2+ lanes, or single lane with identical-URL/title evidence) and re-file the B-side URL of each kept pair via python -m mag.link_library add <url> --writer b2-178-dupe-triage, verifying per append that the recomputed canonical equals the B row's first filing and no pre-existing line changed (git diff / byte compare). The OLD 27 verdicts cannot be joined and stay archive-only.
- Any merged LINKS row whose canonical differs from its first filing, or any pre-existing LINKS.jsonl line modified, kills the eventual merge (brief's falsifier, unchanged).
- If the 338-row snapshot later surfaces (a shadow copy once admin exists, or a lane transcript with the prompts), the original verdicts become joinable and this owed item converts to a direct merge with the old dd ids.
- The tallies (20/7) are over the verdicts file bytes; they move only if that file is touched (it should never be).

## Bibliography closed

watch/inbox/burn_wave_20260926/B2_178_out_links_dedupe.jsonl (27 verdicts, parsed and tallied); B2_178_events.jsonl (metadata-only proof); B2_178_queue_manifest.json (source sha + rows, counts only); B2_178_runner_stdout.log (0 bytes); B2_178_freelane_runner.py:146-198, 289-292 (generation + prompt shape, DEDUPE_PAIR_CAP 400); watch/inbox/LINKS.jsonl (345 rows, all-LF, ending-sha probes); mag/link_library.py (add_urls door). No web sources. Em-dash count 0.
