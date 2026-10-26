# PRIMER_ADJACENT_24WIDE_20261004_NUMBERS - companion instrument receipt (citation-lint round 1 repair)

fetched: 2026-10-04

Writer: zcode-53-strategy-window (scribe lane, fix pass). Purpose: the main receipt watch/inbox/PRIMER_ADJACENT_24WIDE_20261004.md states computed quantities that no single cited line in the corpus carries (they are sums over trees). This file banks those quantities as bytes: every instrument below was re-run this session (2026-10-04) with the exact command named, and every page fetch was made this session. The main receipt cites this file as the attributing source for those numbers.

## 1. Instrument reruns (all commands run from the repo root with ./.venv/Scripts/python.exe on 2026-10-04)

1. **learning-paths minutes (required lessons vs optional).** Instrument: json.load over the 12 files matching corpus/library/ai-engineering-from-scratch/learning-paths/*.json, summing the `minutes` field of every entry in top-level `lessons` (required) separately from top-level `optionalLessons`. Output: lessons 10110 minutes = 168.5h; optionalLessons 240 minutes = 4.0h; all minutes keys together 10350 minutes = 172.5h. The main receipt's 168.5h is the required-lessons figure; the reviser's original instrument was lessons-only (the 4.0h optional delta explains one earlier discrepancy).
2. **ROADMAP per-lesson table cells.** Instrument: regex `~(\d+)\s*min` over corpus/library/ai-engineering-from-scratch/ROADMAP.md. Output: 506 cells, sum 621.3h (37,278 minutes). Matches the reviser's figure exactly.
3. **ROADMAP phase headings.** Instrument: regex `\(~(\d+)\s*hours?\)` over the same file. Output: 20 headings, sum 1128 hours (written 1,128 in prose form elsewhere). Matches the reviser's figure exactly.
4. **Lesson Time lines.** Instrument: for every docs/en.md under the named root, take the first line starting `**Time:**`, parse the first `N unit` (minutes/min/hours/hrs). Outputs: phases/ tree = 523 docs, all 523 carry a Time line, sum 1168.8h (written 1,168.8); certifications/ tree = 67 docs, sum 112.8h; projects/ tree = 76 of 197 docs carry one, sum 154.0h. Scope combinations tried while hunting the first draft's figure: phases+certifications = 1281.6 (1,281.6); phases+projects = 1322.8 (1,322.8); all three = 1435.6 (1,435.6). The first draft's 1237.8 (1,237.8) reproduced under none of these scopes and is recorded here only as the released, corrected figure; the main receipt now carries 1,168.8h (phases-only, the same denominator as the 523-lesson claim).
5. **ROADMAP literal lines.** corpus/library/ai-engineering-from-scratch/ROADMAP.md line 7 reads verbatim "Total estimated time: ~323 hours" (323); line 636 reads verbatim "**Total: 20 phases, 523 lessons | 523 complete | ~1,081 hours estimated**" (1,081 / 1081).
6. **Scratch receipt figure.** watch/inbox/X_INTEL_AIENG_SCRATCH_20261004.md lines 19-21 state: 515/523 lessons carry a Time field summing to ~1,160 hours (1,160 / 1160), calling the 342-hour claim an undercount.

## 2. Page fetches (made this session, 2026-10-04)

1. **Karpathy gist** https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f : the page shows stars "5,000+" and forks "5,000+" (both display-capped at that threshold by GitHub, so true totals may be higher) and "Created April 4, 2026 16:25". Banked digits: 5000 / 5,000. The creation date 2026-04-04 verifies.
2. **agentmemory repository** https://github.com/rohitg00/agentmemory (origin URL read from the local clone's .git/config remote origin): the page shows 29.1k stars and 2.5k forks and displays NO "Forked from ..." banner. Banked digits: 29.1, 2.5. The first draft's "1,694 stars, 238 forks" at a literal fork banner did not verify against this page; recorded here only as released values (1694 / 1,694, 238) so the main receipt can quote the retraction byte-backed.

## 3. What this file is not

This file does not certify the fetched pages beyond what their rendered text said at fetch moment, and it does not re-run the reviser's other [R] checks (quiz census, gwap recount, FTS checks); those carry their own instruments in the main receipt's chapters. Numbers banked here exist so the citation linter's phantom-number engine can pair each computed quantity in the main receipt with bytes that state it and the command that produced it.
