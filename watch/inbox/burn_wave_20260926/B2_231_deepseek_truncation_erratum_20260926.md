# B2-231 receipt: deepseek normal truncation erratum (2026-09-26, lane SW-03)

## Verdict

LANDED as an append-only erratum at memory/runs/combined_game_triangulation/ERRATUM_deepseek_truncation_20260926.md. The truncation is byte-confirmed exactly as briefed (27,594 bytes, 515 lines, no trailing newline, final line `action: push right from (0,` inside Level 3 - The Wall), and the carrier check answers the brief's question NEGATIVELY: the Level 3 completion exists in NO other carrier (manifest, build receipt, cathedral_deepseek.html, and version_grok.md all checked against the cut content, zero hits). The content loss is permanent at the source; downstream cosines are put on notice to treat the normal as truncated and to disqualify parses that read the dangling line as complete.

## Evidence file:line quotes

- memory/runs/combined_game_triangulation/version_deepseek.md:515: "action: push right from (0," (last line; file has 515 lines, 27,594 bytes, does not end with a newline; tail bytes end "...action: push right from (0,").
- memory/runs/combined_game_triangulation/version_deepseek.md:497: "**Level 3 - The Wall.**" (the cut lands inside this walkthrough; preceding complete pair: "action: push down / result: B pushes into wall. B does NOT duplicate. B stays.").
- memory/runs/combined_game_triangulation/BUILD_RECEIPT_20260921.md:3-10: "Built by: deepseek-chat (L1, one lane) ... 26s build + 23s patch"; "MISS: adventure_2d6_stub region ... One DeepSeek patch claimed the fix but didn't deliver it"; "cathedral_deepseek.html: 30,185 chars, playable v0.9" — no Level 3 completion recorded in any carrier.
- Carrier greps (this lane): "push right from (0" hits: cathedral_deepseek.html 0, version_grok.md 0; manifest_deepseek.json contains no prose walkthrough (regions + cross_region_gates only).

## Work done

- Byte-verified the truncation (size, line count, missing trailing newline, exact cut content) rather than trusting the brief.
- Ran the carrier sweep the brief ordered: manifest_deepseek.json (parsed; no walkthrough), BUILD_RECEIPT_20260921.md (read; no Level 3 completion claim), cathedral_deepseek.html and version_grok.md (grep for the cut sentence's continuation; zero hits).
- Filed the append-only erratum with: the byte facts, the downstream cosine impact statement, the NOT-A-CARRIER verdicts, the forward rule (treat the normal as truncated at Level 3; disqualify parses that swallow the dangling action line; regenerated normals go to a NEW file, never appended), and its own falsifier.

## Falsifier

Carried in the erratum and mirrored here: (a) a byte-recheck showing version_deepseek.md at any other byte count or with a complete final line falsifies the erratum (the artifact was edited after filing; append-only law forbids that), (b) a discovered carrier carrying the true Level 3 completion (continuation line after "push right from (0") supersedes the NOT-A-CARRIER verdicts, (c) a downstream cosine or comparison citing version_deepseek.md without the truncation note after this filing is disqualified by the erratum's rule.

## Bibliography closed

- memory/runs/combined_game_triangulation/version_deepseek.md (bytes verified, Level headers mapped)
- memory/runs/combined_game_triangulation/manifest_deepseek.json (parsed whole)
- memory/runs/combined_game_triangulation/BUILD_RECEIPT_20260921.md (read)
- memory/runs/combined_game_triangulation/TRIANGULATION_20260921.md (context, read)
- memory/runs/combined_game_triangulation/cathedral_deepseek.html, version_grok.md (carrier greps)
- watch/inbox/burn_wave_20260926/B2_72_order_sensitivity_20260926.md (the side finding that surfaced the truncation)
