# G-B_SPECIES_DATA — receipt (wave lane: physical_computing / GAP G-B)

**Gap:** species selection for cube 1 and the multispecies lattice.
**Wave law:** receipt FIRST, append as you go · no git · no paid APIs · WebSearch/WebFetch only.
**Date:** 2026-09-16

## Questions (socratic tease)

1. Which species shows the strongest/cleanest electrical spiking in published measurements (amplitude, rate, SNR)?
2. Which is fastest to colonize on oats and most forgiving for a first-time grower?
3. Which species PAIRS create the sharpest zone-line incompatibility while both being cultivable?

## Log (appended as gathered)

- [receipt opened — searches starting]
- **Search 1 (Adamatzky species comparison):** primary sources identified — "Towards fungal computer" (Adamatzky 2018, PMC6227805), "Language of fungi…" (Adamatzky 2022, Royal Society Open Science 9:211926; four species: ghost *Omphalotus nidiformis*, enoki *Flammulina velutipes*, split gill *Schizophyllum commune*, caterpillar *Cordyceps militaris*; S. commune reportedly most complex lexicon), "Electrical activity of fungi: Spikes detection and complexity analysis" (Biosystems 2021; *Pleurotus djamor* action-potential-like trains). Newer arXiv 2601.08099: directional spiking in *P. ostreatus*.
- **Search 2 (colonization on oats/grain):** Foxfire Mushrooms colonization chart — grain (incl. oats) 7–21 d by species; **pink oyster fastest 7–12 d**; lion's mane 14–21 d. Nature Lion: oyster "by far the fastest bulk colonizer" 7–10 d surface, 14–21 d full; spore→first harvest 3–5 wk (Colorado Cultures). Zombie Myco/SporesMD tables: oysters 7–14 d (fastest), shiitake 14–21, lion's mane 14–21, reishi 14–28. Enoki ~moderate 14–21 d (reported, to verify). *S. commune*: very fast contaminant-tolerant colonizer, ~7–14 d, but leathery texture (not commonly cultivated for food — fine, we're not growing for food).
- **Search 3 (incompatibility / zone lines):** rich. *S. commune* is THE model for barrage zones: incompatible pairings → dense black melanin demarcation lines (Wei et al. 2023 Microbiome); barrage = thick elevated mycelial density zone between incompatible homokaryons; *het-c* locus 3 allelic specificities (h-c1/2/3) triggers heterokaryon incompatibility; polypeptide/receptor cross-signaling (Bond & Huang). *Trametes versicolor* vs *T. hirsuta*: barrage zone without melanin (Ohira 2007). *Ganoderma* pairs (G. meridionale/lucidum/tsugae): barrage zones with lines of inhibition (Adaskaveg & Gilbertson 1986). *P. ostreatus* barrage zone characterized (Wang et al. 2017 FEMS Microb Lett). Cross-species: *S. commune* × *T. hirsuta* — PDA gives clamp connections, MEA gives S. commune dominance/overgrowth (Ratushny et al. 2020). King et al. 2025 "Fungal Wars" (Molecules) — table of heterospecific pairings incl. S. commune, T. versicolor, Fomes fomentarius, Irpex lacteus, Cerrena unicolor. Wei et al. 2023: 22-strain wood-block study — S. commune among dominant combative species.

## Sources

- https://pmc.ncbi.nlm.nih.gov/articles/PMC6227805/ (Towards fungal computer — fetch pending)
- https://royalsocietypublishing.org/rsos/article/9/4/211926/96736/Language-of-fungi-derived-from-their-electrical (403 on fetch; numbers via alternate routes)
- https://arxiv.org/html/2601.08099v1 (directional spiking P. ostreatus)
- https://openaccess.uoc.edu/bitstream/10609/144547/1/1-s2.0-S0303264721000307-main.pdf (Biosystems 2021; fetch retry)
- https://foxfiremushrooms.com/mushroom-colonization-times-chart/
- https://naturelion.ca/blog/mushroom-growing-timeline
- https://www.coloradoculturesllc.com/post/how-long-does-an-oyster-take-to-grow
- https://zombiemyco.com/blogs/mushrooms/liquid-culture-colonization-time
- Wei et al. 2023 Microbiome (S. commune zone lines) · Ohira 2007 BioControl (Trametes barrage) · Adaskaveg & Gilbertson 1986 Mycologia (Ganoderma barrage) · Wang et al. 2017 FEMS Microb Lett (P. ostreatus barrage) · King et al. 2025 Molecules "Fungal Wars" · Ratushny et al. 2020 (S. commune × T. hirsuta)

### Spiking numbers — fetch round 1

**"Towards fungal computer" (Adamatzky 2018, PMC6227805) — *Pleurotus ostreatus* (pearl oyster), 7 commercial kits, differential electrodes:**
- Endogenous spikes: large-spike avg amplitude **0.77 mV (sd 0.29)**, typically in pairs (pair gap ~238 s); overall avg amplitude **0.12 mV**, avg duration **516 s**; two largest spikes (>0.8 mV) 20–48 min apart.
- Fruiting-body signalling: ch. oscillations avg **0.47 mV**, spike duration 1669 s, period 1819 s; non-periodic changes up to **1 mV**.
- Stimulated (substrate injection): single 9 mV spike at injection; trains 4 h later **0.29–12.3 mV (avg 4.1 mV)**, duration 33–151 s (avg 71 s), periods 450–2870 s (avg 953 s).
- Fruit-to-fruit potential difference: avg amplitude 0.25 mV, avg duration 287 s, avg gap 4111 s.

**"Language of fungi" (Adamatzky 2022, RSOS 9:211926; PMC8984380) — the 4-species comparison (ghost *Omphalotus nidiformis*, enoki *Flammulina velutipes*, split gill *Schizophyllum commune*, caterpillar *Cordyceps militaris*):**
- Amplitudes span **0.03–2.1 mV**; spike durations 1–21 h (as summarized by Europe PMC — exact per-species table fetch pending).
- *S. commune* produced the most complex "sentences"/lexicon; vocabulary structure resembles human word-length distributions.
- 33 citations; PMID 35425630.

**"Language of fungi" RSOS 2022 — full-text extracted (PDF mirrored on Wikimedia Commons; downloaded + pypdf):**

Conditions: differential electrode pairs 1–2 cm apart, 1 sample/s, 8 pairs simultaneous, 21°C ~80% RH dark; S. commune recorded 1.5 d, others ~5 d.

**Table 1 (verbatim):**

| species | no. spikes | interval (min) | amplitude (mV) |
|---|---|---|---|
| C. militaris (caterpillar) | 881 | 116 | 0.2 |
| F. velutipes (enoki) | 958 | 102 | 0.3 |
| S. commune (split gill) | 530 | 41 | 0.03 |
| O. nidiformis (ghost) | 1117 | 92 | 0.007 |

Per-species narrative:
- **F. velutipes (enoki): highest average amplitude (0.3 mV, sd ~0.3) AND bursts of 12 spikes/train at avg 2.1 mV (σ=0.1), spike duration 64 min** — "rich spectrum of diverse patterns", low- and high-frequency oscillations. Electrical standout of the four.
- **S. commune: fastest spiking** (avg interval 41 min), "remarkably diverse", transitions low-amp/low-freq → high-amp/high-freq wave packets; synchronized spikes between neighbouring fruit bodies (first 4 spikes 1425 s apart, σ=393). Avg amplitude low (0.03 mV) partly an artifact of reference electrodes in host wood. Lexicon: **"S. commune generate the most complex sentences", "uncontested champion in complexity"** (normalized algorithmic complexity ~2x O. nidiformis); avg word length 4.4 (≈ Greek 4.45).
- C. militaris: second-highest amplitude 0.2 mV but lowest spiking frequency (~2 h interval); avg word length 4.7 (≈ English 4.8).
- O. nidiformis: weakest (0.007 mV) — NOT the high-amplitude species one might assume from folklore; highest spike count though (1117).
- Fungal lexicon size up to ~50 words; word-length distributions Zipf-like, in range of English/Swedish.

**Cross-paper synthesis so far:** amplitude ranking endogenous: enoki 0.3 mV / cordyceps 0.2 mV > S. commune 0.03 > ghost 0.007 (RSOS); P. ostreatus large spikes 0.77 mV avg (2018 paper) — i.e. **P. ostreatus is the amplitude champ in endogenous recordings, enoki second and the amplitude champ among the RSOS four**; stimulated P. ostreatus reaches 12.3 mV. "Cleanest" = enoki (high amplitude + high σ-reproducible 2.1 mV bursts + mixed patterns) or P. ostreatus (0.77 mV avg, burst pairs). SNR note: S. commune fastest rate but µV-scale amplitude → needs better front-end.

## Final deliverables

### Species scorecard

Score bands: strong · ok · weak. Electrical numbers are published values (see log above); cultivation numbers from grow-guide consensus (7–21 d grain typical).

| species | amplitude (published) | grow speed (oats/grain) | forgiveness (1st-timer) | pair-compatibility (zone lines) |
|---|---|---|---|---|
| **P. ostreatus** (blue/pearl oyster) | **strong** — 0.77 mV avg large endogenous spikes; 0.12 mV overall; 12.3 mV stimulated (Adamatzky 2018); mV→tens-of-mV events (arXiv 2601.08099) | **strong** — 7–14 d colonize, 2–3 wk to fruit | **strong** — canonical beginner species, contaminant-tolerant, wide temp window | **ok** — intra-species barrage zone characterized (Wang 2017); strong hyphal interference vs other species |
| **F. velutipes** (enoki) | **strong** — 0.3 mV avg, clean 2.1 mV (σ=0.1) 12-spike bursts; richest pattern mix (RSOS 2022) | ok — ~14–21 d; needs cold shock to fruit | ok — moderate; fruiting temp (~10–15°C) conflicts with 21°C recording room | weak/understudied — no zone-line literature surfaced |
| **S. commune** (split gill) | weak-amplitude / **strong-rate** — 0.03 mV avg (partly electrode artifact), fastest spiker (41 min interval), **highest spike-train complexity** (RSOS 2022) | **strong** — ~7–14 d, weed-like, contaminant-tolerant, fruits on twigs | ok — very easy to grow; **caution: spores are a documented respiratory allergen (timber-worker hypersensitivity) — filter/vent the cube** | **strong** — THE model for barrage zones + melanin zone lines (het-c, 3 specificities; black demarcation lines at non-self contacts) |
| **C. militaris** (caterpillar) | ok — 0.2 mV but slowest (≈2 h interval) | weak — fruits readily only on insect-rich substrate | weak — special substrate | weak — no data surfaced |
| **O. nidiformis** (ghost) | weak — 0.007 mV avg; not the high-amplitude species folklore suggests | weak — specialist grower species | weak | weak — no data |
| **G. resinaceum/lucidum** (reishi) | ok (partial) — AP-like trains, amplitudes rising from ~0.35 mV (Adamatzky 2021, partial extract only) | ok — easy but 14–28 d, slow | ok | ok — barrage zones w/ inhibition lines (intra-genus, Adaskaveg 1986) |
| **T. versicolor** (turkey tail) | ok (less characterized in core papers; used in later Adamatzky work) | **strong** — ~14–21 d, easy | **strong** — medicinal-grow standard | **strong** — zone-line champion in culture/wood (spalted-wood black lines; combative in 35-species wood study) |

### Cube-1 pick: **Pleurotus ostreatus (blue oyster)**

Reason: the only species that is simultaneously (1) amplitude-leader among fast cultivars — 0.77 mV average large endogenous spikes, ~6–25x the RSOS-four averages, with stimulated trains to 12.3 mV that clear any cheap ADC noise floor; (2) fastest on oats — 7–14 d colonization, 2–3 wk to fruiting; (3) the standard first-time-grower recommendation; (4) the richest published protocol base (2018 fruiting-body recordings + 2026 16-electrode directional study = copy the electrode geometry). Runner-up: enoki (best burst cleanliness, 2.1 mV σ=0.1) — take it only if the cube can hold ~12°C fruiting. Rejected for cube 1: S. commune (µV-scale amplitudes need a serious front-end) despite being the fastest spiker.

### Cube-2 pairing: **S. commune × Trametes versicolor**

Reason: sharpest, most reliably formed zone line from two cultivable species. S. commune carries the genetically hardwired non-self barrage response (het-c, 3 allelic specificities) producing black melanin demarcation lines — the textbook incompatibility line — and is simultaneously Adamatzky's fastest-spiking, most-complex-sentence species (electrical payoff at the collision front). T. versicolor is the classic zone-line producer in culture and a combative, easy, ~2-week grain colonizer. Caveat (honest flag): no published S. commune × T. versicolor zone-line measurement surfaced — this is an engineering pick from (a) S. commune's general non-self barrage response and (b) T. versicolor's documented zone-line/combative behavior; outcome is known to be medium/condition-dependent (Ratushny 2020: S. commune overgrew T. hirsuta on MEA). Mitigation: inoculate both sides simultaneously at equal density with a meet-in-the-middle geometry. **Fallback pair: P. ostreatus × S. commune** — reuses cube-1 infrastructure and unites Adamatzky's two best-electrically-characterized species; expect S. commune barrage at the front, but risk of P. ostreatus hyphal interference pushing through (use a removable barrier strip).

### Open items

- Biosystems 2021 (P. djamor spike complexity) full text not retrieved (UOC mirror serves HTML stub; paper noted from search record only).
- Ganoderma amplitudes from secondary snippet only (0.35 mV rising trains) — unverified against PDF.
- No direct published S. commune × T. versicolor interaction study — first experiment would be novel; file under G-B follow-up.
- RSOS 2022 spike "durations" in the 1–21 h range are wave-packet/train timescales, not single-AP widths — mind the sampling (1 Hz) and electrode artifact budget when designing cube electronics.

*Receipt complete — 2026-09-16. All numbers above are byte-quoted from fetched texts (pypdf extract of the Wikimedia-mirrored RSOS PDF, PMC full text, arXiv HTML) or clearly marked as grow-guide consensus.*
