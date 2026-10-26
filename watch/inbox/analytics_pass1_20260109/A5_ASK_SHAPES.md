# A5 Ask Shapes vs Landings (analytics pass 1, lane A5)

Window 2026-09-25 to 2026-10-08. Data: memory/zknot session cards (16 interactive sessions, 383 visible prompt first-lines; the 6 biggest sessions truncate to latest 30 per card, denominators are visible-sample, not total) joined to 566 git commits and commit-message text.

Method note (the confound): the estate commits around the clock (~40/day autonomous), so a naive "commits within 24h" join is non-empty for every prompt and proves nothing. The discriminating instrument is the estate's own convention: commits that QUOTE the operator's words in the subject ("operator order:", "operator ask:", his phrase verbatim). Only named-echo commits count as conversion below. Instrument: git log --pretty subject grep + zknot timestamps.

## Shape table (visible sample, approximate counts)

| Shape | Seen | Named-echo commits | Typical latency | Landing surface |
|---|---|---|---|---|
| order-with-constraint | ~120 | ~16 | 5 to 90 min | mechanism code + receipt |
| vision-statement (quotable, under ~10 words) | ~30 | ~8 | 2 to 8 min | LAW / SPEC / doctrine commit |
| URL-drop, github/product | ~10 | ~5 | 5 to 56 min | commit (DROP / LINK-DROP / steal) |
| URL-drop, x.com bare | ~34 | 0 | hours | frontier sweep receipts only, never a commit subject |
| one-word GO with pending referent | ~10 | ~7 | 9 to 41 min | fires the queued thing |
| one-word GO bare (next / continue / go) | ~25 | 0 | n/a | throughput signal to running lanes |
| question, status-type | ~35 | 1 (disk distress) | 9 min (that one) | conversation |
| question, analogy-anchored | ~15 | ~4 | 27 to 48 min | doctrine or new mine |

## Conversion findings by shape

- Orders with a machine-checkable constraint are the workhorse. "the fold step on the workflows were running into eachother... make it so they dont hold eachother up" 10-05 20:33 -> 55cdaaa4f 10-05 21:14 FOLD GATE FLEET-WIDE, 41 min, constraint quoted verbatim. Same pattern: headed-windows cure (86 min), GSTD draft v1 (57 min), mesh roster (5 min: "i have a tablet an old phone..." 10-07 19:13 -> 193bd303b 19:18), smith chart (2h21m).
- Vision statements are the fastest convertors in the repo. "remember duplication is emphasis" 10-02 11:46 -> fb829aa49 11:48 LAW, 2 min. "its thiving ecosystem of memory palaces..." 10-07 12:40 -> e02fef752 12:43 COGNITOPOLIS v0 SPEC, 3 min. "we should have model gates" doctrine x3 09-30 17:30-17:32 -> f0768f3be 17:38, 8 min. Aphorisms are treated as legislation; orders are treated as work.
- The TLD predicts the landing surface. GitHub or product URLs convert to commits (gstdcoin/ai drop 10-05 14:52 -> fb0760853 14:57 DROP, 5 min; superhivemarket 10-07 12:29 -> d7ab3e227 12:35 LINK-DROP, 6 min; no-ai-slop 10-07 21:45 -> ee3756f0d 22:41 steal, 56 min). Bare x.com drops (10-08 morning cluster of 8, 10-05 a8c2ebd2 night cluster of 7) produced zero commit echoes, only frontier_olm sweep receipts hours later.
- Hybrid URL + one-line verdict is the single most reliable ask: the URL supplies material, the verdict supplies the order. "https://github.com/petergyang/no-ai-slop Love it brother... lets tighten up yes?" -> steal landed and banked as a skill.
- Bare GO words do nothing by themselves. "next", "continue", "go", "gogo" (~25 visible) produced zero named echoes; the GOs that converted carried a pending referent ("go referee" 09-26 00:19 -> d34fa3887 00:36, 17 min; HISTORY PURGED under "operator GO"; CLEANUP P1-P3 under operator GO 10-08). GO is a trigger, not an ask.
- Status questions stay conversations ("How's our nous spend going", "What's our token throughput", "How do we 10x..." - zero echoes). Analogy-anchored questions convert because the analogy is a template to clone: "can we just mine her and vault mother like we do with hermes" 10-07 12:26 -> e925a8d1a 13:14 PERSON MINE LIVE, 48 min; "we're outta cash... write out a research summary" -> 316cc26bb CONVERGENCE DOCTRINE banked (operator question), 27 min.

## Strange findings (datum + join + confidence + falsifier)

1. STRANGE: five words outrank five paragraphs. Datum: the shortest quotable vision prompts convert to LAW commits in 2 to 8 min; explicit orders take 40 to 90 min and land as code. Join: prompt timestamp vs commit timestamp vs verbatim quote in subject (fb829aa49, e02fef752, f0768f3be). Confidence: high (3 clean cases, quotes verbatim). Falsifier: find an order-with-constraint that landed as a LAW commit inside 10 min, or an aphorism that took over an hour.
2. STRANGE: his X feed and his GitHub feed are different organs. Datum: ~34 bare x.com URL drops -> 0 named-echo commits (receipts only); ~10 github/product URLs -> 5 commit landings at 5 to 56 min. Join: URL host in prompt first-line vs commit subjects naming the repo. Confidence: medium-high (denominator is the visible 383, truncation on big sessions). Falsifier: find an x.com-only drop whose tweet content is named in a commit subject within 24h.
3. STRANGE: distress converts, curiosity does not. Datum: "the c drive is nearly full whats going on waht is the plan" 10-08 16:34 -> relief commit 0b9980351 16:43, 9 min, while same-day status questions produced none all window. Join: prompt urgency markers vs commit latency. Confidence: medium (1 clean positive; the 16:44/17:02 angrier follow-ups rode the same lane). Falsifier: a calm status question that produced a named-echo commit.
4. STRANGE: GO can kill the operator's own idea. Datum: "do it add it to the list" 10-07 20:15 -> fd09a9fce 20:18 pull queued -> 9b72d287c 21:00 GPS-EMBED TRIAL VERDICT: KILLED BY ITS OWN FALSIFIER. The GO shape executes pre-registered falsifiers, not just intent. Confidence: high (commit chain is explicit). Falsifier: find a killed-idea verdict that did NOT trace to an operator GO.
5. STRANGE: the complaint shape produces zero commits and one apology. Datum: "you told me no. why?" 10-05 03:49 (and the 10-05 03:50 follow-up) - no commit echo; every other shape in the window lands something. Join: card prompt list vs commit subjects that hour. Confidence: medium (absence evidence). Falsifier: a grievance prompt that produced a named-echo commit.

## Honest limits

- The latest-30 truncation on the six biggest cards (bb9913b3 286 prompts, c6ad00b4 167, 6334e346 91, 6eb89c85 112, fce37d85 55, fd5ec147 55) means ~600 prompt lines are unclassified; ratios above describe the visible 383.
- Named-echo is a conservative conversion bar: prompts may have driven commits that did not quote them (autonomous lanes blur attribution by design, zknot hides child sessions).
- Latencies use zknot prompt times (ET) vs git author times (ET); both local, clock skew unlikely.

Written 2026-10-08, lane A5, read-only sources: memory/zknot/*.md + git log since 2026-09-25.
