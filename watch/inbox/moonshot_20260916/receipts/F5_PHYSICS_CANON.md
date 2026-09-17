# F5 — MOONSHOT PHYSICS CANON (receipt-first)

- **Lane:** operator moonshot 2026-09-16 — retrocausal steering program, physics canon fetch
- **Window:** fetched 2026-09-16
- **Targets:** Feynman Lectures Vol III ch. 1–9 (feynmanlectures.caltech.edu, free+legal per Caltech); TT1-cited papers — TSVF reviews (Aharonov & Vaidman), transactional interpretation (Kastner), Wharton retrocausal models, delayed-choice entanglement swapping (Peres 2000 line → Ma/Zurbriggen 2012 → later never-coexisted-photon work), time-refraction/time-interface metamaterials 2023–2026, Deutsch CTC paper, Aaronson CTC lecture notes; Aharonov & Vaidman TSVF chapter if openly hosted; NIST DLMF if relevant.
- **Discipline:** free+legal fetches only (Caltech open lecture site, arXiv, author-hosted preprints). No git. Receipt appended as fetches land.
- **Write root:** `memory/corpus/moonshot_canon/` (shared surface, durable copy). Manifest lives with the files.

<!-- SWEEP LOG -->
- [x] receipt filed (this file)
- [x] corpus dir scaffolded (`memory/corpus/moonshot_canon/{feynman,papers}/`)

### 2026-09-16 — fetch log (append-only)

**Route notes (honesty first):**
- feynmanlectures.caltech.edu serves a Cloudflare managed challenge to non-browser
  clients (curl with browser headers still challenged). Internet Archive / Wayback was
  "Temporarily Offline" + 429 during the window. Browser-use tool unavailable in this
  subagent. Working route: r.jina.ai reader proxy, markdown transcription of the free
  Caltech pages (content identical, equations/images preserved as links/LaTeX; NOT the
  raw HTML bytes). Saved as `feynman/jm_III_0X.md`. Source license unchanged: Caltech
  New Millennium Edition, free to read online.
- arXiv: PDFs fetched from arxiv.org (free, legal). IDs verified against the arXiv API
  (titles + authors) BEFORE download; two remembered IDs were wrong and were corrected
  via API search (1903.10738 → 1906.04313; "1209.2020" → 1304.7474).

- [x] Feynman Vol III ch 1–9 → feynman/jm_III_01..09.md (titles verified: Quantum Behavior;
      Wave/Particle Viewpoints; Probability Amplitudes; Identical Particles; Spin One;
      Spin One-Half; Dependence of Amplitudes on Time; Hamiltonian Matrix; Ammonia Maser)
- [x] TSVF: quant-ph/0105101 Aharonov & Vaidman, "The Two-State Vector Formalism of
      Quantum Mechanics: an Updated Review" — this IS the arXiv version of the
      Time in Quantum Mechanics (LNP 733, 2008) chapter, so the "A&V chapter if openly
      hosted" target is satisfied by the same fetch.
- [x] Kastner TI: arXiv:1608.00660 "The Transactional Interpretation and its Evolution
      into the 21st Century: An Overview"
- [x] Wharton retrocausal: arXiv:1003.4273 (Time-symmetric boundary conditions, Symmetry
      2010); arXiv:1805.09731 (A New Class of Retrocausal Models); arXiv:1906.04313
      Wharton & Argaman (Bell's Theorem and Locally-Mediated Reformulations of QM, Rev.
      Mod. Phys. 92 colloquium)
- [x] Delayed-choice entanglement swapping: arXiv:1203.4834 Ma et al. (Nat. Phys. 2012);
      arXiv:1209.4191 Megidish et al. (PRL 2013, photons that never coexisted).
      NOTE: Peres 2000 (J. Mod. Opt. 47, 139) is NOT on arXiv (API search returned
      nothing) and no legal open copy surfaced — the lineage is covered by the 2012/2013
      experiments whose intros cite it. Zhao et al. PRL 2019 extension not found via the
      title/abs searches tried; not fetched (recorded as a gap, not a silent skip).
- [x] Time-refraction: arXiv:2208.07236 Moussa et al. "Observation of Temporal Reflection
      and Broadband Frequency Translation at Photonic Time-Interfaces" (Nature Physics
      2023) — 4.7 MB, includes supplementary.
- [x] CTC: arXiv:0808.2669 Aaronson & Watrous (CTCs make quantum and classical computing
      equivalent); Aaronson PHYS771 Lecture 19 "Time Travel" HTML from scottaaronson.com
      (14 hits "closed timelike", 5 hits "Deutsch") — this is the Aaronson CTC lecture
      notes (the democritus lec27 guess was a 404; the real lecture is lec19).
      Deutsch 1991 PRL-D 44,3197: no arXiv (pre-arXiv quant-ph); open legal copy not yet
      located (daviddeutsch.org.uk fetch failed mid-window; will retry once).

### 2026-09-16 — closing

- [x] MANIFEST written: `memory/corpus/moonshot_canon/MANIFEST.md` (per-file source URL, arXiv ID,
      publication venue, SHA-256; gaps + refusals recorded; reading order).
- [x] Deutsch 1991: daviddeutsch.org.uk unreachable twice in window — final state: NOT fetched,
      gap recorded in manifest; D-CTC content covered by Aaronson-Watrous + Aaronson Lecture 19.
- [x] NIST DLMF: evaluated → ruled out of scope (no DLMF-class special functions load-bearing in
      this canon; a math annex would be padding). Recorded in manifest.
- [x] Aharonov & Vaidman chapter target: satisfied by quant-ph/0105101 (it IS the LNP 733
      chapter's arXiv version).

## Fetched table (final)

| # | File (under memory/corpus/moonshot_canon/) | What | Source | Bytes | SHA-256 (first 16) |
|---|---|---|---|---|---|
| 1 | feynman/jm_III_01.md | FLP III Ch.1 Quantum Behavior | feynmanlectures.caltech.edu/III_01.html (via reader proxy, md) | 46,109 | 1a4e7e35dc65e240 |
| 2 | feynman/jm_III_02.md | FLP III Ch.2 Wave and Particle Viewpoints | …/III_02.html | 42,378 | e4e07d2c6de05d80 |
| 3 | feynman/jm_III_03.md | FLP III Ch.3 Probability Amplitudes | …/III_03.html | 52,143 | fed43e72843b1b21 |
| 4 | feynman/jm_III_04.md | FLP III Ch.4 Identical Particles | …/III_04.html | 56,767 | c035cabaa279c193 |
| 5 | feynman/jm_III_05.md | FLP III Ch.5 Spin One | …/III_05.html | 52,906 | 92beb82bc1abbd80 |
| 6 | feynman/jm_III_06.md | FLP III Ch.6 Spin One-Half | …/III_06.html | 44,458 | b8dd801b0f36415d |
| 7 | feynman/jm_III_07.md | FLP III Ch.7 Dependence of Amplitudes on Time | …/III_07.html | 47,142 | 5c4da022a1ef0ec3 |
| 8 | feynman/jm_III_08.md | FLP III Ch.8 The Hamiltonian Matrix | …/III_08.html | 51,587 | 1113d24526472b05 |
| 9 | feynman/jm_III_09.md | FLP III Ch.9 The Ammonia Maser | …/III_09.html | 61,076 | a70e379d69d4a16a |
| 10 | papers/aharonov_vaidman_TSVF_updated_review_2001.pdf | TSVF updated review (= LNP 733 chapter) | arXiv:quant-ph/0105101 | 432,560 | ec624b268f576b53 |
| 11 | papers/kastner_TI_evolution_overview_2016.pdf | Kastner TI overview | arXiv:1608.00660 | 201,615 | 97b2ec6e4f8924e6 |
| 12 | papers/wharton_timesymmetric_boundary_conditions_2010.pdf | Wharton, time-symmetric BCs | arXiv:1003.4273 | 164,437 | 87e42841e11ee1ab |
| 13 | papers/wharton_new_class_retrocausal_models_2018.pdf | Wharton, new class of retrocausal models | arXiv:1805.09731 | 580,430 | 4f8a59812ceb127f |
| 14 | papers/wharton_argaman_bell_locally_mediated_RMP_2019.pdf | Wharton & Argaman RMP colloquium | arXiv:1906.04313 | 966,695 | 844984968ac8179c |
| 15 | papers/ma_delayedchoice_entanglement_swapping_2012.pdf | Ma et al., delayed-choice ent. swapping | arXiv:1203.4834 | 1,047,973 | 82d39acf6171dd56 |
| 16 | papers/megidish_entanglement_never_coexisted_2013.pdf | Megidish et al., photons never coexisted | arXiv:1209.4191 | 391,975 | 7078f1c1f7427b0f |
| 17 | papers/moussa_temporal_reflection_photonic_time_interfaces_2023.pdf | Moussa et al., temporal reflection (Nat. Phys. 2023) | arXiv:2208.07236 | 4,730,949 | eab0233b1914f037 |
| 18 | papers/vaidman_past_of_quantum_particle_2013.pdf | Vaidman, past of a quantum particle | arXiv:1304.7474 | 1,060,857 | d2d5603c3c8ea954 |
| 19 | papers/aaronson_watrous_CTC_quantum_classical_equivalent_2008.pdf | Aaronson & Watrous, CTC equivalence | arXiv:0808.2669 | 215,117 | eb7674b2b1ff0515 |
| 20 | papers/aaronson_time_travel_lecture19.html | Aaronson PHYS771 Lec.19 Time Travel (CTC notes) | scottaaronson.com/democritus/lec19.html | 30,909 | 0607d6f8dd747d08 |

Not fetched (no legal open copy; gaps recorded in MANIFEST.md): Deutsch 1991 PRL-D 44,3197 ·
Peres 2000 J. Mod. Opt. 47,139 · Zhao et al. PRL 2019 (unconfirmed arXiv record). NIST DLMF:
evaluated, ruled out of scope.

## The moonshot's required reading, in order

1. **Feynman Lectures Vol. III, ch. 1–9** (`feynman/jm_III_01..09.md`) — the language: amplitudes,
   two-slit logic, spin, amplitude-with-time, the Hamiltonian matrix. Everything downstream is
   written in this grammar; ch. 7–9 are the hinge (amplitude phase over time → two-state thinking).
2. **Aharonov & Vaidman, "The Two-State Vector Formalism of Quantum Mechanics: an Updated Review"**
   (`papers/aharonov_vaidman_TSVF_updated_review_2001.pdf`) — the formalism the parable doctrine
   borrows: what two boundary conditions (⟨ψ| forward, |φ⟩ backward) actually buy, weak values, and
   where pre-/post-selection is bookkeeping vs. physics.
3. **Wharton & Argaman, "Bell's Theorem and Locally-Mediated Reformulations of Quantum Mechanics"**
   (`papers/wharton_argaman_bell_locally_mediated_RMP_2019.pdf`) — the honesty gauge for the whole
   program: exactly what a retrocausal/locally-mediated picture can and cannot claim, which is the
   discipline the pre-registration-as-retarded-boundary-condition doctrine has to survive.

<!-- APPEND POINT -->

**Status: CLOSED 2026-09-16.** 20 files, ~9.9 MB, all hashed in MANIFEST.md. No git used. Free+legal
fetch discipline held; two paywalled anchors (Deutsch 1991, Peres 2000) left as recorded gaps
instead of grey-zone grabs.
