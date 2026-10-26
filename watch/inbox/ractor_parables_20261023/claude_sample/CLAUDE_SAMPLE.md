# CLAUDE SAMPLE: 2026-10-23 ET (Claude lane only)
Method: same as batch 1. Each call got a fresh empty temp folder holding only PROMPT.txt, built from the batch-1 prompt (Ractor brief + subject brief + The Door) plus this line: "use no real device, seat, machine, or person names". Output is the parable, then ---KEY---, then the buried rules. Runner: cs_seat.py. Each seat ran its calls one at a time.

## Seats
| Seat / route | Account (from log) | Model per log | Result |
|---|---|---|---|
| bob agy.exe (C:\Users\etfag\AppData\Local\agy\bin) | nachobusinesscorp@gmail.com | label="Claude Opus 5.5 (Medium)" | 0/1. 12:30:01-12:30:20 ET, exit 3: `RESOURCE_EXHAUSTED (code 429): Individual quota reached. Please upgrade your subscription to increase your limits. Resets in 31h29m52s.` (error_id 04d816d1-bf61-4fbb-8a8d-0a5dccf182b9-1). Stopped using bob. |
| PC agy.exe (%LOCALAPPDATA%\antigravity\staging), --model claude-opus-5-5-medium | fostertron@gmail.com (a separate quota pool) | label="Claude Opus 5.5 (Medium)", 6/6 calls | 5 OK, 1 failed (content filter, not quota). No 429 seen. |
| PC Claude Code CLI 2.1.245 (claude -p --model opus, from hermes\node) | n/a | none (modelUsage empty, 0 tokens) | 0/4. 12:30:33-12:30:49 ET: `Not logged in · Please run /login`. Not logged in. I didn't attempt a login. |
| Claude Desktop app on PC (WindowsApps) | n/a | n/a | Not tried. It has no headless prompt route. |
| bob Claude Code | n/a | n/a | Not installed. |

## Outputs (PC agy Claude Opus 5.5 Medium)
| File | ET | Words |
|---|---|---|
| who_we_are__freud: "The House That Kept Flooding" (fills the batch-1 slot) | 12:30:33-12:31:18 | 797 |
| standing_wave_gate__hall: "The Hum at the Narrow Bridge" | 12:31:18-12:31:54 | 854 |
| the_congress__diogenes: "The Lantern at the Grain Gate" | 12:31:54-12:32:39 | 912 |
| water_governor__foucault: FAILED | 12:32:39-12:32:48 | - |
| parable_as_spec__jung: "The Heron in the Well" | ~12:3x | 879 |
| dirac_loops__mcluhan: "The Hitch-Walker of the Rope Loft" | ~12:3x | 841 |

Foucault x water_governor error, verbatim: `agent executor error: generating and executing: Your previous response was blocked by content safety filters\nOutput retries exhausted after 4 attempts` (exit 3, grpc code 2, retryable false). I didn't retry it. My first quota regex wrongly read routine `quota_manager.go` log lines as a quota error and stopped the seat. I fixed the regex and then ran Jung and McLuhan on the same seat.

## Compared with batch-1 Claude
- **Identity-in-record kept as disputed: yes.** In Freud's key, rule 8 says identity-in-record "stays under examination until it is proven". The physician writes "not yet known, return in spring". This matches the batch-1 Claude pattern (9/11 disputed).
- Freud carries base rules 1-7, except the two-stations rule, and drops the roster. That is the batch-1 Claude style. Its lens rule fits the PC Gemini Freud reading (repetition is a symptom): "what is only said gets lived again", plus "read a repeated failure, don't scold".
- **Hygiene:** none of the 5 parable bodies names a seat, device, or person (checked for Sancho/Bob/Pixel/T90/Hermes/Moto/foste/weights/Senate/ledger/hash/model/lane).
- **Lens fidelity:** Hall again ends on "the reading the house never hears is the one told by those who left". That makes outsider decoding go unheard in 4/4 Hall parables across batches. Diogenes adds the trust-only-the-record auditor.
- The same plain style holds (797-912 words, one-image scenes). The keys are more literal than batch 1's: McLuhan's key restates the numbers 33/21/20/8/6.
