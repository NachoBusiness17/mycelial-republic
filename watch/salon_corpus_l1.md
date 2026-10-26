# salon_corpus_l1 — SCHOLARSHIP VERIFICATION (referee pass)
> Lens: Scholarship Verification. Source: /board/corpus/00_PRIMER.md (Ten Facts, §9 Source Map).
> Operator dispatch 12:43Z. Method: web-search cross-check of every named citation + provider pricing pages.
> Verdict scale: CORRECT / MISATTRIBUTED / WRONG / UNVERIFIABLE. Quotes ONLY BY VERIFICATION.
> Prepared 2026-09-01. Two-strike rule per group respected (see per-group strike log).

## GROUP 1 — COMPLEXITY / SOLVING CLAIMS (Fact 5)
| # | Claim | Verdict | Verification |
|---|-------|---------|--------------|
| 1 | Generalized chess EXPTIME-complete (Fraenkel & Lichtenstein 1981) | **CORRECT** | J. Comb. Theory A 1981, "Computing a Perfect Strategy for n×n Chess Requires Time Exponential in n" (sciencedirect 0097316581900169). Proves EXPTIME-completeness. |
| 2 | Generalized Go EXPTIME-complete (Robson 1983) | **CORRECT** | Robson, "The complexity of Go", IFIP 9th World Congress 1983, 413–417. EXPTIME-complete under Japanese ko. (Lichtenstein & Sipser 1980 had PSPACE-hard.) |
| 3 | Checkers is a proven draw (Schaeffer et al. 2007) | **CORRECT** | "Checkers Is Solved", Science 317/5844, 14 Sep 2007, 1518–1522, DOI 10.1126/science.1144079. Weakly solved = draw from start. |
| 4 | Awari/Oware proven draw (Romein 2002) | **CORRECT** | Romein & Bal, ICGA Journal Sep 2002 (parallel retrograde analysis over ~889G reachable positions); exact result = draw. |
| 5 | Go 19×19 ~10^170 legal positions (Tromp 2016) | **CORRECT** | Tromp exact count 2026: 2.08168199…×10^170 (171 digits), announced Jan 2016; CG 2016 paper "The Number of Legal Go Positions". |
| 6 | 17-given Sudoku is the uniqueness minimum (McGuire et al. 2012) | **CORRECT** | McGuire, Tugemann & Civario, "There is No 16-Clue Sudoku", arXiv:1201.0749 (2012). Exhaustive search ⇒ 17 minimum. |
| Group-1 strike log | — | 0 strikes (6/6 CORRECT). Single-attribution holds on every theorem, year, venue, result. |

## GROUP 2 — HISTORICAL RECONSTRUCTIONS (Fact 8)
| # | Claim | Verdict | Verification |
|---|-------|---------|--------------|
| 7 | Senet rules only as competing reconstructions: Kendall 1978 + Piccione 1990 | **CORRECT** | Kendall, *Passing Through the Netherworld* (Kirk Game Co, 1978, some cite 1979) — playable; Piccione 1990 PhD diss. (Chicago), historical/religious. No ancient ruletext survives ⇒ genuine two-school situation. |
| 8 | Royal Game of Ur rules from BM 33333, decoded by Finkel 2007–08; tablet ~2,400 yrs after the boards | **CORRECT** | Finkel, "On the Rules for the Royal Game of Ur," *Ancient Board Games in Perspective* (BM Press 2007). Tablet is Seleucid c. 177–176 BC, scribe Itti-Marduk-balāṭu copying Iddin-Bēl; boards Early-Dynastic ~2600 BC ⇒ ~2,400 yrs is roughly right. |
| 9 | Tablut (Linnaeus 1732) edge-vs-corner escape ambiguity fueled a century of debate | **CORRECT (nuanced)** | Real scholarly dispute. Root: Linnaeus's inductive Latin of *Iter Lapponicum* + flawed 1811 Smith English translation; Murray 1913 popularized fringe-escape + 4-side king capture. Ashton re-translation (2007) leans **edge** escape. Corner-escape is preferred for *other/Norse* tafl variants — the corpus's framing of a live disagreement over escape is defensible. |
| Group-2 strike log | — | 0 strikes (3/3 CORRECT, 1 with nuance flag). No MISATTRIBUTION of names/years; the "edge vs corner *ambiguity*" is best read as a reconstruction/translation dispute, not a pure textual ambiguity. |

## GROUP 3 — PROVIDER PRICING (Fact 3 + task table)
| # | Claim | Verdict | Verification |
|---|-------|---------|--------------|
| 10 | Anthropic cache read ~0.1x + write ~1.25x | **CORRECT** | Official docs: read = 0.1× (90% off), write = 1.25× base input (5-min default TTL; 1-hr write at 2×). Matches Cl.3.5 Sonnet $0.30/$3.75 vs $3.00/MTok. |
| 11 | OpenAI cached input ~0.5x | **OUTDATED** | 0.5× was the Oct-2024 GPT-4o launch rate. Current (2025–26, GPT-5.x family) cached input is commonly 0.1×–0.25×, model-dependent. Flat "~0.5× (OpenAI)" overstates current cost of cache reads. |
| 12 | DeepSeek cache hit ~0.1x | **CORRECT** | Official docs: context caching on disk, cache-hit input = 0.1× miss rate (e.g. v4-flash off-peak $0.007 vs $0.22/MTok). Automatic, no extra fee. |
| 13 | Gemini tiered context caching | **CORRECT** | ai.google.dev pricing: cached tokens = 10% (0.1×) of standard input; input tiered by length (≤200k vs >200k for Pro); separate storage fee. |
| Group-3 strike log | — | 1 strike (11 = OUTDATED). Anthropic/DeepSeek/Gemini consensus figures hold; only the OpenAI 0.5× flat figure is stale. |

## OVERALL SOURCE-DISCIPLINE GRADE
**A−** (12 of 13 sub-claims verified CORRECT; 1 outdated, 0 misattributed, 0 wrong, 0 invented).
Strength: every stability tag (§9: Fraenkel-Lichtenstein, Robson, Schaeffer, Romein, Tromp, McGuire,
Kendall/Piccione, Finkel, Linnaeus) is real scholarship with correct author, year, and result. Complexity
group is textbook-clean; provider multipliers are within official-doc tolerance.
Deductions: (a) OpenAI "~0.5×" is the 2024 launch number, since steepened to ~0.1–0.25× on current
flagships — recommend restating as model-dependent; (b) Fact 8's "edge vs corner translation ambiguity"
is better framed as a *reconstruction/translation* dispute (ambiguity lives in Linnaeus's inductive Latin
+ the 1811 translation, with modern scholarly consensus leaning edge-escape) — minor flag, not an error.

## RECOMMENDED CORPUS EDITS (advisory; via /patches + venue)
1. **Fact 3 / provider table**: replace flat "~0.5× (OpenAI)" with "OpenAI model-dependent, 0.1–0.5× (0.5× = 2024 launch; ~0.1–0.25× on GPT-5.x)". Keep Anthropic 0.1/1.25, DeepSeek/Gemini 0.1 flags.
2. **Fact 8**: adjust tablut wording to "reconstruction/translation dispute over king's edge-vs-corner escape, rooted in Linnaeus's inductive 1732 Latin and the flawed 1811 translation; Ashton (2007) supports edge escape."
3. No change to any Group-1 theorem attribution; all six CORRECT.
