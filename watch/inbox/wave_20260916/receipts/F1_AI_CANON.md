# F1 — AI/RL TEXTBOOK CANON FETCH (receipt-first)

- **Lane:** F1 · wave_20260916 · target: `memory/corpus/ai_canon/`
- **Law:** free + legal only (author/publisher-hosted) · verify legality before fetch · PDF magic bytes checked · manifest.jsonl `{url,file,sha256,title,bytes}` · **no git** · receipt appended as I go.

## Log

- 2026-09-16 receipt opened BEFORE first fetch (law honored).
- Targets verified for legality:
  - Sutton & Barto RL 2nd ed — incompleteideas.net (author-hosted free PDF) — probing.
  - Jurafsky & Martin SLP3 ed3book_aug26.pdf — Stanford-hosted (author), free draft — CONFIRMED 200 OK, 26,506,144 bytes, application/pdf.
  - Goodfellow/Bengio/Courville Deep Learning — deeplearningbook.org free HTML (publisher-sanctioned site), chapter set — CONFIRMED chapter list scraped.
  - Norvig PAIP — checking norvig.com for author-hosted PDF.
- TT1 moonshot receipt status: `watch/inbox/moonshot_20260916/receipts/TT1_RETROCAUSAL_PHYSICS.md` EXISTS but is an unfilled skeleton (no arXiv set extracted). Canonical arXiv anchors for the named topics (two-state vector formalism, transactional interpretation, time refraction) will be search-verified and fetched; the full extracted set is QUEUED for post-TT1 backfill.

## Fetched (running)

| # | title | file | bytes | magic | legality |
|---|---|---|---|---|---|
| 1 | Sutton & Barto, *Reinforcement Learning: An Introduction*, 2nd ed (2020 printing) | sutton_barto_reinforcement_learning_2nd.pdf | 73,129,769 | %PDF- | author-hosted free PDF (incompleteideas.net). NOTE: host's HTTPS cert chain fails Windows schannel (untrusted root) → fetched over plain HTTP; integrity pinned by sha256 in manifest.jsonl. |
| 2 | Jurafsky & Martin, *Speech and Language Processing*, 3rd ed draft (ed3book_aug26, Aug 2026 release) | jurafsky_martin_slp3rd_draft.pdf | 26,506,144 | %PDF- | author-hosted free draft PDF (web.stanford.edu/~jurafsky/slp3/), free for personal/educational use per book site. |

- Norvig PAIP verdict: norvig.com hosts only the PAIP **code** page (norvig.com/paip.html); no author-hosted full-book PDF found → **skipped** per "if still hosted" clause. Not pirated; queue stands.

## Deep Learning chapter set (fetched 2026-09-16)

24 official HTML chapters + front matter PDF from deeplearningbook.org (publisher-sanctioned free HTML renderings, pdf2htmlEX), 73,330,700 bytes of chapter HTML + 1,000,627 bytes front matter. All saved under `memory/corpus/ai_canon/chapters/dlb_*.html`. Chapter list: TOC, notation, acknowledgements, bib, intro, linear_algebra, prob, numerical, ml, mlp, regularization, optimization, convnets, rnn, guidelines, applications, linear_factors, autoencoders, representation, graphical_models, monte_carlo, partition, inference, generative_models (all 20 chapters + apparatus — complete set).

## TT1 moonshot anchors (arXiv, free)

TT1 receipt (`moonshot_20260916/receipts/TT1_RETROCAUSAL_PHYSICS.md`) exists but is an UNFILLED skeleton — no extracted arXiv set. Per mission, canonical anchors for the three named topics were search-verified and fetched:

| topic | paper | file | bytes |
|---|---|---|---|
| two-state vector | Aharonov & Vaidman, "The Two-State Vector Formalism of Quantum Mechanics: an Updated Review", arXiv:quant-ph/0105101 | arxiv_tsvf_aharonov_vaidman_0105101.pdf | 432,560 |
| transactional | Kastner, "The Transactional Interpretation and its Evolution into the 21st Century", arXiv:1608.00660 | arxiv_transactional_kastner_1608.00660.pdf | 201,615 |
| time-refraction | Moussa et al., "Observation of Temporal Reflections and Broadband Frequency Translations at Photonic Time-Interfaces", arXiv:2208.07236 (Nat. Phys. 19, 863, 2023) | arxiv_time_refraction_moussa_2208.07236.pdf | 4,730,949 |

**QUEUED for post-TT1 backfill:** full extracted arXiv set once TT1 fills the receipt (delayed-choice family, CTC computation, weak values per TT1 §2/§4/§5).

## Delight hunt — fetched

| title | file | bytes | legality |
|---|---|---|---|
| David MacKay, *Information Theory, Inference, and Learning Algorithms* (640 pp, Cambridge) | mackay_information_theory_inference_learning_algorithms.pdf | 11,675,219 | author's Cambridge site (inference.org.uk/itprnn), explicitly free PDF. **THE find: DVW-grade foundational text off-target.** |
| Richard Bartle, *Designing Virtual Worlds* | bartle_designing_virtual_worlds.pdf | 5,205,807 | author's own site (mud.co.uk), free PDF. The named bar itself — canon'd. |

Delight candidates NOT landed: *The Elements of Statistical Learning* (Hastie/Tibshirani/Friedman, free full PDF historically at hastie.su.domains/ElemStatLearn/) — official print12 link currently 404s (link rot); re-hunt later. Norvig PAIP: not author-hosted → skip stands.

## Final tally (manifest.jsonl, sha256-pinned)

| # | title | file | bytes | sha256 (16) |
|---|---|---|---|---|
| 1 | Sutton & Barto, RL: An Introduction, 2nd ed | sutton_barto_reinforcement_learning_2nd.pdf | 73,129,769 | 2dd0d71d9ee883fb |
| 2 | Jurafsky & Martin, SLP 3rd ed draft (Aug 2026) | jurafsky_martin_slp3rd_draft.pdf | 26,506,144 | 88d0362c3bcb62a0 |
| 3 | Deep Learning book (Goodfellow et al) — 24 HTML chapters | chapters/dlb_*.html (24 files) | 73,330,700 | per-file in manifest |
| 4 | Deep Learning — Front Matter PDF | chapters/dlb_front_matter.pdf | 1,000,627 | 1f6f329f952557e7 |
| 5 | Aharonov & Vaidman TSVF review | arxiv_tsvf_aharonov_vaidman_0105101.pdf | 432,560 | ec624b268f576b53 |
| 6 | Kastner Transactional Interpretation review | arxiv_transactional_kastner_1608.00660.pdf | 201,615 | 97b2ec6e4f8924e6 |
| 7 | Moussa et al time-refraction observation | arxiv_time_refraction_moussa_2208.07236.pdf | 4,730,949 | eab0233b1914f037 |
| 8 | MacKay, Information Theory, Inference, and Learning Algorithms | mackay_information_theory_inference_learning_algorithms.pdf | 11,675,219 | 868adc5f0ef66303 |
| 9 | Bartle, Designing Virtual Worlds | bartle_designing_virtual_worlds.pdf | 5,205,807 | 1f1581ddb94a2566 |

- **Entries:** 32 manifest lines (9 canonical units; DL chapters itemized individually) · **TOTAL: 196,213,390 bytes = 196.21 MB**
- **All PDF magic bytes verified `%PDF-`** (7 root PDFs + front matter). HTML chapters verified as official pdf2htmlEX renderings (DOCTYPE + generator header).
- **Delight verdict:** YES — caliber sense: MacKay's *Information Theory, Inference, and Learning Algorithms* is a free, author-hosted foundational text of Designing-Virtual-Worlds grade that was NOT on the target list (now canon'd), and Bartle's DVW itself was secured free from the author. Size sense: no fetched text beats Sutton & Barto's 69.7 MB; the only known legal free full-book fetch that could (ESL II, ~70+ MB) has a 404'd official link — queued for re-hunt.
- Legality: every fetch is author- or publisher-hosted free content. No paywalled/pirated sources, no git writes.

*Sources (search-verified IDs): [TSVF arXiv:quant-ph/0105101](https://arxiv.org/abs/quant-ph/0105101) · [Kastner arXiv:1608.00660](https://arxiv.org/abs/1608.00660) · [Moussa arXiv:2208.07236](https://arxiv.org/abs/2208.07236) · [SLP3](https://web.stanford.edu/~jurafsky/slp3/) · [Sutton & Barto](http://incompleteideas.net/book/the-book-2nd.html) · [deeplearningbook.org](https://www.deeplearningbook.org/) · [MacKay book](https://www.inference.org.uk/itprnn/book.pdf) · [Bartle DVW](https://mud.co.uk/richard/DesigningVirtualWorlds.pdf)*

<!-- RECEIPT SEALED 2026-09-16 · F1 · no git -->
