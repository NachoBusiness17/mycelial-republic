# FREELANE BURN H16 (B2-178, 2026-09-26T16:00:11Eastern Daylight Time)

Hour bucket H16: window counters cover this hour bucket only (delta since the previous hourly snapshot).

## Per-lane counters (window | falsifier: usage-reported tokens)

| lane | calls | 200 | err | bytes_sent | bytes_recv | tok_prompt | tok_completion | tok_total | state |
|---|---|---|---|---|---|---|---|---|---|
| groq | 435 | 435 | 0 | 192,906 | 419,557 | 66,869 | 37,284 | 104,153 | running |
| openrouter-k1 | 775 | 775 | 0 | 325,415 | 2,428,003 | 181,041 | 205,278 | 386,319 | running |
| openrouter-k2 | 769 | 769 | 0 | 323,354 | 2,444,677 | 179,885 | 208,184 | 388,069 | running |
| nous-hermes | 344 | 344 | 0 | 144,340 | 871,386 | 80,406 | 69,687 | 150,093 | running |
| together | 345 | 345 | 0 | 148,610 | 378,060 | 31,200 | 64,340 | 95,540 | running |
| cohere | 337 | 337 | 0 | 141,377 | 197,321 | 29,537 | 8,164 | 37,701 | running |
| zai-pro | 50 | 21 | 29 | 20,653 | 87,842 | 1,828 | 19,885 | 21,713 | running |
| zai-lite | 102 | 84 | 18 | 42,244 | 327,824 | 7,313 | 75,228 | 82,541 | running |

## Queue state

- links_title_norm: 210 done this window, 0 remaining (manifest 210)
- links_dedupe: 27 done this window, 0 remaining (manifest 27)
- caption_enrich: 1,189 done this window, 1,534 remaining (manifest 2,726)
- corpus_class: 1,344 done this window, 53,063 remaining (manifest 54,412)

## Output samples (last per task, trimmed)

- links_title_norm: {"item": "lt-0195", "lane": "openrouter-k2", "raw": "{\"site\":\"\",\"work\":\"Azure Architecture Center: Circuit Breaker Pattern\",\"type\":\"article\"}"}
- links_title_norm: {"item": "lt-0175", "lane": "openrouter-k2", "raw": "{\"site\":\"klymentiev.com\",\"work\":\"Cerebras free tier now requires a card\",\"type\":\"post\"}"}
- links_title_norm: {"item": "lt-0147", "lane": "cohere", "raw": "{\"site\": \"x.com\", \"work\": \"LukaPiskorec: structure is more than the sum of its parts; workflow unlock\", \"type\": \"post\"}"}
- links_dedupe: {"item": "dd-0026", "lane": "openrouter-k2", "raw": "{\"same\":true,\"reason\":\"Same BenchLM leaderboard, with B reconfirming the 104-model listing.\"}"}
- links_dedupe: {"item": "dd-0024", "lane": "cohere", "raw": "{\n  \"same\": true,\n  \"reason\": \"Identical content, minor differences in formatting.\"\n}"}
- links_dedupe: {"item": "dd-0012", "lane": "openrouter-k1", "raw": "{\"same\":false,\"reason\":\"No repository path or identifying information is provided for B.\"}"}
- caption_enrich: {"item": "ce-1435", "lane": "together", "raw": "{\"class\": \"video-clip\", \"archive_worthy\": true, \"reason\": \"Video file with caption and URL\"}"}
- caption_enrich: {"item": "ce-1437", "lane": "openrouter-k2", "raw": "{\"class\":\"photo-scene\",\"archive_worthy\":true,\"reason\":\"Photo media with stored bytes and linked source\"}"}
- caption_enrich: {"item": "ce-1439", "lane": "openrouter-k1", "raw": "{\"class\":\"photo-scene\",\"archive_worthy\":false,\"reason\":\"Standalone JPEG photo with small payload and capped context\"}"}
- corpus_class: {"item": "cc-01434", "lane": "groq", "raw": "{\"class\":\"code\",\"keep\":true,\"reason\":\"C++ source file in code directory\"}"}
- corpus_class: {"item": "cc-01437", "lane": "openrouter-k1", "raw": "{\"class\":\"config\",\"keep\":true,\"reason\":\"Protocol Buffer schema definition\"}"}
- corpus_class: {"item": "cc-01436", "lane": "nous-hermes", "raw": "{\"class\":\"code\",\"keep\":true,\"reason\":\"Protobuf interface definition is source code.\"}"}

Privacy: caption rows and corpus files send structure metadata only; caption text, filenames and file contents never leave this machine.
