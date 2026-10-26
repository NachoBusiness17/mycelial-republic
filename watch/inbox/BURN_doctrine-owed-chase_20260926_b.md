# BURN receipt: doctrine-owed-chase (2026-09-26, pass b)

## Verdict

steal

## Evidence

1. Sefaria API: Kol_HaTor.4 returns {"error": "Kol HaTor ends at Chapter 3."}. Sweep: Sefaria chs 1 to 3 (81,079 chars) plus Wikisource chs 1 to 7, 9 pages (223,166 chars): 304,245 chars, nikud stripped. Zero hits for מצות גילוי הקץ, יש מצוה לגלות הקץ, גילוי הקץ, מצווה לגלות, or any מצוה...גלות...הקץ span. Sefaria corpus-wide search "מצות גילוי הקץ": 0 hits. Closest real text, Kol HaTor 3.1 (Sefaria he): "נשלח מן השמים לגלות רמזי התורה בהתקרב עקבתא דמשיחא דרך קץ המגולה". Ch.4 (Wikisource "קול התור ד"): "רמיזין קדישין על מועדי הפקידות וקץ המגולה בדור אחרון"; six occurrences of קץ המגולה, no mitzvah-of-revealing form. The working idiom is קץ המגולה; the bigram גילוי הקץ never occurs in either edition.

2. arXiv API: arXiv:2606.26479v1, "Adaptive Evaluation of Out-of-Band Defenses Against Prompt Injection in LLM Agents", published 2026-06-25, Narisetty et al. Abstract byte-matches the prior snippet: "Recent work (2024 to 2026) has converged on a strategy for defending tool-using LLM agents against indirect prompt injection". Load-bearing: "we warn that every one of them is validated only on static benchmarks (a fixed set of injection attempts)"; adaptive defense-aware attacks "broke twelve of them at over 90% success"; "Progent cut mean attack success roughly sixfold (25.8% to 4.2%), and a hand-crafted adaptive attack did not raise it (2.6%)"; "a stronger optimized (white-box GCG) attack remains open".

3. OpenAI news RSS (1,230 items, full feed): Sep 17 2026 carries exactly two items, "How Cooley is accelerating IPO work with ChatGPT" and "Introducing Astra for Law". Neither is guidance. Honest substitute: "Our framework for reporting model misalignment", on-page date "September 16, 2026": "We are sharing a new framework for tracking, investigating, and disclosing instances of model misalignment at OpenAI, along with six reports"; "our disclosures have been ad hoc and less frequent than ideal".

## Steal or Vacuous

Steal. (b) fully resolved: arXiv:2606.26479; the prompt-uplift-lane OWED line closes and the drafted BIB_LAUNDER patch gains its adjacent prior art at ID strength, with the paper's own static-benchmark warning attached. (a) closed as a decisive negative: the literal wording is absent from both full online Hebrew editions and corpus-wide on Sefaria; fleet doctrine must stop citing "Kol HaTor ch.4" for it; still owed: a printed-edition scan (hebrewbooks) or the Gaon-source behind the secondary claim; the quotable cognate is the קץ המגולה wording above. (c) substituted, not resolved: the Sep 17 guidance item does not exist in OpenAI's primary feed; the Sep 16 misalignment-reporting framework is the dated stand-in for the middle-path citation; the literal item stays owed.

## Falsifier

none proposed

## Bibliography

- watch/inbox/BURN_doctrine-owed-chase_20260926.md; BURN_prompt-uplift-lane_20260925_d.md; BURN_middle-path-doctrine_20260926.md
- sefaria.org/api/texts/Kol_HaTor.1, .2, .3 (?language=he), .4 (error response); Sefaria search-wrapper "מצות גילוי הקץ"
- he.wikisource.org קול התור index + pages א, ב_א, ב_ב, ג, ד, ה_א, ה_ב, ו, ז
- export.arxiv.org/api/query (title phrase; all:"out-of-band" AND all:"prompt injection"); arXiv:2606.26479v1 abstract
- openai.com/news/rss.xml (full feed); openai.com/index/model-misalignment-reporting-framework (fetched)
- WebSearch x2 (Hebrew phrase; OpenAI Sep 17): no direct hit; 429s on the Hebrew query
