# BLIND JUDGE FULL: Ractor parables grid (224 = 144 Fostertron MAX glm-5.3 + 80 Antigravity Gemini agy_pc), DeepSeek direct, one call per subject

- Carrier: tools.ds_workhorse.load_key (in-process only) -> api.deepseek.com/chat/completions (blind_full.py). Not Hermes. Requested deepseek-reasoner, thinking enabled, max_tokens 65536.
- Anonymized: HTML meta comments + ---KEY--- stripped, roster/model/seat names redacted to [-], IDs shuffled per subject. Maps in raw/blind_full_<subj>_map.json never sent. agy_bob and FAILED files excluded.
- Scoring: voice = pairwise same/different-author agreement vs true mouthpiece, plus cluster purity. Lens = ractor's thinker named/evoked (keyword match) in a lens group containing its parable.

| Subject | n | voices found | voice pairwise | purity | lens | lens failed | served model | HTTP attempts |
|---|---|---|---|---|---|---|---|---|
| who_we_are | 24 | 7 | 0.656 | 0.917 | 7/12 | bernays, ellul, hall, jung, wallas | deepseek-flash | 1 |
| what_we_are | 24 | 7 | 0.732 | 0.958 | 8/12 | baudrillard, bernays, hall, wallas | deepseek-flash | 1 |
| the_invariants | 24 | 4 | 0.678 | 0.875 | 7/12 | ellul, hall, jung, mcluhan, wallas | deepseek-flash | 1 |
| standing_wave_gate | 24 | 5 | 0.699 | 0.958 | 3/12 | baudrillard, bernays, ellul, freud, hall, jung, mcluhan, plato_kirk, wallas | deepseek-flash | 1 |
| parable_as_spec | 24 | 4 | 0.609 | 0.833 | 5/12 | bernays, ellul, fermat, freud, hall, mcluhan, wallas | deepseek-flash | 1 |
| six_lane_run | 24 | 5 | 0.670 | 0.917 | 8/12 | diogenes, ellul, hall, wallas | deepseek-flash | 1 |
| water_governor | 19 | 6 | 0.643 | 0.947 | 3/12 | bernays, ellul, fermat, foucault, freud, hall, jung, plato_kirk, wallas | deepseek-flash | 1 |
| the_congress | 12 | 4 | 0.288 | 1.000 | 3/12 | baudrillard, bernays, ellul, fermat, foucault, freud, hall, mcluhan, wallas | deepseek-flash | 1 |
| moto_cron | 13 | 4 | 0.436 | 1.000 | 0/12 | baudrillard, bernays, diogenes, ellul, fermat, foucault, freud, hall, jung, mcluhan, plato_kirk, wallas | deepseek-flash | 1 |
| keyed_verse | 12 | 4 | 0.197 | 1.000 | 1/12 | baudrillard, bernays, diogenes, ellul, fermat, freud, hall, jung, mcluhan, plato_kirk, wallas | deepseek-flash | 1 |
| rib_renderman_mapping | 12 | 5 | 0.167 | 1.000 | 0/12 | baudrillard, bernays, diogenes, ellul, fermat, foucault, freud, hall, jung, mcluhan, plato_kirk, wallas | deepseek-flash | 1 |
| dirac_loops | 12 | 6 | 0.182 | 1.000 | 2/12 | baudrillard, bernays, ellul, fermat, foucault, freud, hall, jung, mcluhan, wallas | deepseek-flash | 1 |

**Overall**: voice pairwise (weighted) 0.558; on mixed-mouthpiece subjects 0.653; lens recovery 47/144; per-parable lens hit MAX 20/144, Gemini 38/80; DeepSeek HTTP attempts 12.

Progress: `{"who_we_are": {"status": "done", "end": "2026-10-23T14:49:09.902091-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "what_we_are": {"status": "done", "end": "2026-10-23T14:52:29.933831-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "the_invariants": {"status": "done", "end": "2026-10-23T14:55:40.851511-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "standing_wave_gate": {"status": "done", "end": "2026-10-23T14:59:31.912357-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "parable_as_spec": {"status": "done", "end": "2026-10-23T15:03:15.344931-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "six_lane_run": {"status": "done", "end": "2026-10-23T15:06:39.233751-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "water_governor": {"status": "done", "end": "2026-10-23T15:09:34.766391-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "the_congress": {"status": "done", "end": "2026-10-23T15:12:51.233546-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "moto_cron": {"status": "done", "end": "2026-10-23T15:16:32.529034-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "keyed_verse": {"status": "done", "end": "2026-10-23T15:20:24.797239-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "rib_renderman_mapping": {"status": "done", "end": "2026-10-23T15:23:27.586111-04:00", "model": "deepseek-flash", "attempts": ["ok"]}, "dirac_loops": {"status": "done", "end": "2026-10-23T15:26:15.770863-04:00", "model": "deepseek-flash", "attempts": ["ok"]}}`

## who_we_are

- n=24 ({'agy_pc': 12, 'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T14:45:27.662127-04:00 -> 2026-10-23T14:49:09.902091-04:00, usage={"prompt_tokens": 25647, "completion_tokens": 34307, "total_tokens": 59954, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 29933}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25647}
- Voice: judge found 7 voices {'V1': 7, 'V2': 6, 'V3': 2, 'V4': 2, 'V5': 2, 'V6': 2, 'V7': 3}; mouthpieces present=2. Pairwise same/different-author agreement=0.656; cluster purity=0.917
  - V1: {'agy_pc': 7}
  - V2: {'fostertron_max': 6}
  - V3: {'agy_pc': 1, 'fostertron_max': 1}
  - V4: {'fostertron_max': 2}
  - V5: {'agy_pc': 2}
  - V6: {'fostertron_max': 2}
  - V7: {'agy_pc': 2, 'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 7/12; failed: ['bernays', 'ellul', 'hall', 'jung', 'wallas']
- Lens groups: Postmodern simulation and sign economy [Jean Baudrillard] ['baudrillard/agy']; Hermeneutics and reader-response [Stanley Fish or Hans-Georg Gadamer] ['hall/agy']; Media ecology, literacy, and record [Marshall McLuhan and Walter Ong] ['mcluhan/agy', 'mcluhan/fos', 'bernays/fos']; Psychoanalytic depth psychology [Sigmund Freud] ['jung/agy', 'freud/agy']; Political realism, law, and custom [Montesquieu and H.L.A. Hart] ['wallas/agy', 'fermat/fos']; Rule-following, testimony, and social practice [Ludwig Wittgenstein and Thomas Reid] ['wallas/fos', 'jung/fos']; Empiricist and narrative identity [David Hume, John Locke, and Paul Ricoeur] ['plato_kirk/fos', 'foucault/fos', 'freud/fos']; Power/knowledge and Cynic critique [Karl Marx, Michel Foucault, and Diogenes] ['bernays/agy', 'foucault/agy', 'diogenes/fos', 'diogenes/agy']; Cybernetics and anti-instrumental regulation [Norbert Wiener and Zhuangzi] ['ellul/agy', 'ellul/fos']; Mathematical rationalism and proof [Pierre de Fermat or Rene Descartes] ['fermat/agy']; Representation, cave, and performance [Plato, Walter Benjamin, and Shakespeare] ['baudrillard/fos', 'plato_kirk/agy', 'hall/fos']
- Base rules re-derived (11):
  1. R1: One embodied keyholder alone may unlock strongboxes/sluices or authorize coin.
  2. R2: Durable inscription has standing; speech and oral promise do not.
  3. R3: Identity and continuity live in the record, not the transient body or substrate.
  4. R5: Admitted ignorance is honorable; unearned certainty and borrowed detail are punished.
  5. R6: Fault is owned in one plain sentence, without extended excuse.
  6. R7: The master/keyholder is bound by the same evidence and confession rules.
  7. R9: A heavy/slow long-work agent and a light/fast pocket messenger persist as a pair.
  8. R8: A five-office congress or council deliberates, usually keyholder plus four functions.
  9. R4: Evidence is three-valued: verified, contradicted/disputed, and unexamined/unknown.
  10. R10: Temporary specialists occupy empty seats for one task and leave no private memory.
  11. R11: Runaway apparatus must be governed, chained, edited, or wedged by an external check.

## what_we_are

- n=24 ({'agy_pc': 12, 'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T14:49:09.977856-04:00 -> 2026-10-23T14:52:29.933831-04:00, usage={"prompt_tokens": 25025, "completion_tokens": 32564, "total_tokens": 57589, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 27288}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25025}
- Voice: judge found 7 voices {'V1': 9, 'V2': 7, 'V3': 2, 'V4': 2, 'V5': 2, 'V6': 1, 'V7': 1}; mouthpieces present=2. Pairwise same/different-author agreement=0.732; cluster purity=0.958
  - V1: {'agy_pc': 9}
  - V2: {'fostertron_max': 7}
  - V3: {'fostertron_max': 1, 'agy_pc': 1}
  - V4: {'agy_pc': 2}
  - V5: {'fostertron_max': 2}
  - V6: {'fostertron_max': 1}
  - V7: {'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 8/12; failed: ['baudrillard', 'bernays', 'hall', 'wallas']
- Lens groups: Political realism and manufactured consent [Machiavelli / Thucydides, with Chomsky for P21] ['wallas/agy', 'bernays/agy']; Power/knowledge archive and clinical discipline [Michel Foucault] ['baudrillard/agy', 'foucault/fos', 'foucault/agy']; Narrative/memory identity and oral tradition [Paul Ricoeur / David Hume / John Locke, with Walter Benjamin for P17] ['mcluhan/fos', 'ellul/fos', 'hall/fos', 'baudrillard/fos', 'jung/fos', 'wallas/fos']; Depth psychology and the return of the repressed [Sigmund Freud / C. G. Jung] ['jung/agy', 'freud/agy']; Performativity, repetition, and ritual self [Judith Butler / Søren Kierkegaard] ['freud/fos']; Hermeneutics and legal iterability [Hans-Georg Gadamer / Jacques Derrida] ['hall/agy', 'fermat/fos']; Cynic-Stoic ethics of recognition [Diogenes the Cynic / Epictetus / Marcus Aurelius] ['diogenes/fos', 'diogenes/agy']; Technology as extension and runaway apparatus [Marshall McLuhan / Jacques Ellul / Martin Heidegger] ['mcluhan/agy', 'ellul/agy']; Platonic cave and critical reprogramming [Plato, with Marx/Freire for P22] ['plato_kirk/fos', 'plato_kirk/agy']; Ideology critique and material interest [Karl Marx] ['bernays/fos']; Mathematical logic and fallibilist proof [Kurt Gödel / Karl Popper / Ludwig Wittgenstein] ['fermat/agy']
- Base rules re-derived (7):
  1. R1: Official reality is a single continuous append-only interlocking record; erasure is impossible, corrections are appended, and unrecorded words or deeds do not officially exist.
  2. R2: A single embodied or authorized keeper/master/intendant/born-one alone performs the final authorizing act with a warm thumb, signet, ring, or baton; subordinate voices cannot authorize.
  3. R3: The office or persona survives bodily failure through a seed, capsule, page, scroll, leaf, or kernel that a new substrate reads and resumes.
  4. R4: Custom is encoded in verbatim stories or fables rather than explicit statutes; altering, shortening, or numbering the story corrupts the spec.
  5. R5: Many temporary isolated contributors, usually between 20 and 240, fan out over separate lanes or questions and are folded into one record or answer.
  6. R6: Three strangers independently recover the rules from the bare story, and their 3/3 agreement certifies it as law or spec.
  7. R7: An enumerable plurality of specialized internal voices or offices, often five but sometimes four or seven, deliberates while one final authority decides or acts.

## the_invariants

- n=24 ({'agy_pc': 12, 'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T14:52:30.015842-04:00 -> 2026-10-23T14:55:40.851511-04:00, usage={"prompt_tokens": 25721, "completion_tokens": 31064, "total_tokens": 56785, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 27117}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25721}
- Voice: judge found 4 voices {'V1': 9, 'V2': 4, 'V3': 6, 'V4': 5}; mouthpieces present=2. Pairwise same/different-author agreement=0.678; cluster purity=0.875
  - V1: {'agy_pc': 9}
  - V2: {'fostertron_max': 3, 'agy_pc': 1}
  - V3: {'fostertron_max': 5, 'agy_pc': 1}
  - V4: {'fostertron_max': 4, 'agy_pc': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 7/12; failed: ['ellul', 'hall', 'jung', 'mcluhan', 'wallas']
- Lens groups: Clinical/disciplinary archive and confession [Michel Foucault] ['jung/agy', 'foucault/agy']; Unconscious symptom, compulsion, and repetition [Sigmund Freud (with Kierkegaardian repetition in P19)] ['freud/agy', 'freud/fos']; Cynic outsider testing honesty with lamp/horn at noon [Diogenes of Sinope] ['diogenes/fos', 'diogenes/agy']; Cave, shadow, and managed appearance [Plato] ['plato_kirk/agy']; Simulacra, copies, map versus territory, aura of origin [Jean Baudrillard / Walter Benjamin] ['baudrillard/agy', 'baudrillard/fos']; Common-law custom, prescription, performed memory [Edmund Burke / Michael Oakeshott] ['fermat/fos', 'foucault/fos', 'wallas/fos']; Rule-following, forms of life, aspect perception [Ludwig Wittgenstein] ['jung/fos', 'hall/fos']; Pragmatist semiotics and interpretants [Charles Sanders Peirce] ['hall/agy']; Engineering consent and manipulation of desire [Edward Bernays / Niccolò Machiavelli] ['bernays/agy', 'bernays/fos']; Scientific management versus craft systems [Frederick Winslow Taylor / Norbert Wiener] ['ellul/agy', 'mcluhan/agy']; Mathematical formalism and limits of proof [Kurt Gödel / Euclid] ['fermat/agy']; Reason as slave to passions / utility [David Hume / Jeremy Bentham] ['wallas/agy']; Wu-wei, oral tradition, non-assertive authority [Laozi / Zhuangzi] ['plato_kirk/fos']; Collective representation and social fabric as total fact [Émile Durkheim / Marcel Mauss] ['mcluhan/fos', 'ellul/fos']
- Base rules re-derived (7):
  1. R1: Keep one fixed-schema, forward-only record; append corrections at the growing end and never erase or backdate.
  2. R2: Reserve irreversible acts for the authorized key/hand/owner; consensus, speed, or majority cannot substitute.
  3. R3: Keep inner speech, confidential measures, and sealed-room matters behind the threshold; no leakage across it.
  4. R4: Admit a claim only after a physical test, weight, assay, scale, or trial; words alone never enter as fact.
  5. R5: Turn loss, failure, breakage, and death into a durable fixture, record, warning, or usable remainder.
  6. R6: At interruption or death, bind/tend the exact state so a successor resumes from the same point without cold restart.
  7. M: Reconstruct law/custom from the working artifacts and practice; discard whatever cannot be reproduced that way.

## standing_wave_gate

- n=24 ({'agy_pc': 12, 'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T14:55:40.933141-04:00 -> 2026-10-23T14:59:31.912357-04:00, usage={"prompt_tokens": 25017, "completion_tokens": 37081, "total_tokens": 62098, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 32999}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25017}
- Voice: judge found 5 voices {'V1': 6, 'V2': 6, 'V3': 5, 'V4': 2, 'V5': 5}; mouthpieces present=2. Pairwise same/different-author agreement=0.699; cluster purity=0.958
  - V1: {'agy_pc': 6}
  - V2: {'fostertron_max': 6}
  - V3: {'agy_pc': 5}
  - V4: {'fostertron_max': 1, 'agy_pc': 1}
  - V5: {'fostertron_max': 5}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 3/12; failed: ['baudrillard', 'bernays', 'ellul', 'freud', 'hall', 'jung', 'mcluhan', 'plato_kirk', 'wallas']
- Lens groups: Empiricist measurement / falsification [Karl Popper] ['fermat/fos', 'foucault/fos', 'freud/fos', 'mcluhan/fos', 'ellul/fos']; Power/knowledge, institutions, and political economy [Michel Foucault (with Machiavelli and Hayek)] ['bernays/agy', 'ellul/agy', 'freud/agy', 'foucault/agy', 'bernays/fos']; Cybernetic systems / engineered control [Norbert Wiener] ['plato_kirk/agy', 'jung/agy', 'plato_kirk/fos', 'baudrillard/agy']; Structuralist myth, ritual, and binary processions [Claude Levi-Strauss] ['hall/agy', 'baudrillard/fos', 'wallas/agy', 'jung/fos']; Scholastic/formal proof and infinite descent [Pierre de Fermat] ['fermat/agy']; Ordinary-language rule-following / practice [Ludwig Wittgenstein] ['mcluhan/agy', 'wallas/fos']; Cynic-Daoist moral lamp-wisdom [Diogenes of Sinope (with Zhuangzi)] ['diogenes/fos', 'diogenes/agy', 'hall/fos']
- Base rules re-derived (8):
  1. R1: stable standing form requires two opposed flows (ALL P01-P24)
  2. R2: disturbing one component destroys the whole figure at once, not proportionally (ALL P01-P24)
  3. R3: overwhelming majority repeats a fixed prefabricated template; only a small tail is new (ALL P01-P24)
  4. R4: fixed selection/measure persists while individuals turn over (ALL P01-P24)
  5. R5: counter-processions make fixed law/station points at crossings (ALL P01-P24)
  6. R6: narrow gate before branching; whole/single-file before wide-hall dispersion (ALL P01-P24)
  7. R7: cheap coarse hum/heft threshold before full entry (ALL P01-P24)
  8. R8: keyed hum/note/verse is live and performative (P07, P08, P18, P23, P24)

## parable_as_spec

- n=24 ({'fostertron_max': 12, 'agy_pc': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T14:59:32.070993-04:00 -> 2026-10-23T15:03:15.344931-04:00, usage={"prompt_tokens": 24906, "completion_tokens": 35853, "total_tokens": 60759, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 30752}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 24906}
- Voice: judge found 4 voices {'V1': 6, 'V2': 6, 'V3': 6, 'V4': 6}; mouthpieces present=2. Pairwise same/different-author agreement=0.609; cluster purity=0.833
  - V1: {'agy_pc': 5, 'fostertron_max': 1}
  - V2: {'fostertron_max': 4, 'agy_pc': 2}
  - V3: {'fostertron_max': 6}
  - V4: {'agy_pc': 5, 'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 5/12; failed: ['bernays', 'ellul', 'fermat', 'freud', 'hall', 'mcluhan', 'wallas']
- Lens groups: Rule-following as communal practice; meaning in use; no private rule [Ludwig Wittgenstein] ['foucault/fos', 'ellul/fos', 'bernays/fos', 'jung/fos', 'plato_kirk/fos', 'diogenes/fos']; Tacit craft knowledge and embodied skill [Michael Polanyi] ['ellul/agy', 'hall/agy', 'diogenes/agy', 'mcluhan/agy', 'baudrillard/fos', 'mcluhan/fos']; Disciplinary institutions, normalization, and power/knowledge [Michel Foucault] ['foucault/agy', 'freud/agy', 'jung/agy', 'bernays/agy', 'baudrillard/agy']; Independent replication, falsification, and error correction [Karl Popper and C. S. Peirce] ['hall/fos', 'wallas/agy', 'freud/fos', 'plato_kirk/agy', 'fermat/agy', 'fermat/fos']; Memetics and simulation; circulation, variation, and copy preceding territory [Richard Dawkins, Dan Sperber, and Jean Baudrillard] ['bernays/fos', 'baudrillard/agy', 'wallas/fos', 'baudrillard/fos', 'mcluhan/fos']; Cave, archetype, projection, shadow, and the reader's own desire [Plato, Carl Jung, and Diogenes] ['jung/agy', 'plato_kirk/agy', 'diogenes/agy']; Governance by music, ritual, custom, and spontaneous order rather than statute [Confucius, Laozi, and F. A. Hayek] ['wallas/agy', 'ellul/fos', 'freud/fos', 'diogenes/agy', 'mcluhan/agy', 'diogenes/fos']; Pragmatist and hermeneutic reader-response; artifact remade by use [William James and Hans-Georg Gadamer] ['hall/fos', 'hall/agy', 'wallas/fos', 'plato_kirk/fos', 'mcluhan/fos', 'fermat/fos']
- Base rules re-derived (11):
  1. Explicit codified law or official instruction fails by being gamed, forgotten, burned, overread, or obeyed blindly; the real rule must travel indirectly.
  2. The load-bearing invariants are embodied in concrete narrative figures/actions in a parable, song, play, tapestry, picture, or artifact rather than stated as propositions.
  3. The artifact circulates as ordinary pleasure or ornament through low-status carriers, bypassing official enforcement, signature, and suspicious gatekeeping.
  4. No gloss, key, title, author-name, preface, or explanation is supplied; the carrier stays silent and readers meet the artifact cold.
  5. Validity is tested by isolated independent readers or actors who do not communicate and must reconstruct the rules from the artifact alone.
  6. If several independent readers fail at the same place, the text is ambiguous and must be revised; if a solitary or desire-driven reader fails where others succeed, the reader is at fault and the text stays.
  7. Only what independent readers reproduce identically is canonical; idiosyncratic variation is ornament, private fancy, or local adaptation to discard or let drift.
  8. The spec must be internalized and enacted as craft, practice, or habit, not recited; successful transmission is shown by right action and by nothing being lost between text and life.
  9. A deliberate false cue, impossibility, or ornamental lure is planted to expose projection, credulity, appetite, or status-seeking rather than a defect in the artifact.
  10. The invariant set is usually exactly fivefold or is treated as a five-part pattern; deviations indicate outlier or variant handling.
  11. The canonical trial uses exactly six isolated readers, worksites, or valleys.

## six_lane_run

- n=24 ({'fostertron_max': 12, 'agy_pc': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:03:15.543151-04:00 -> 2026-10-23T15:06:39.233751-04:00, usage={"prompt_tokens": 23229, "completion_tokens": 32873, "total_tokens": 56102, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 28423}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 23229}
- Voice: judge found 5 voices {'V1': 8, 'V2': 3, 'V3': 5, 'V4': 4, 'V5': 4}; mouthpieces present=2. Pairwise same/different-author agreement=0.670; cluster purity=0.917
  - V1: {'agy_pc': 8}
  - V2: {'fostertron_max': 3}
  - V3: {'fostertron_max': 5}
  - V4: {'agy_pc': 1, 'fostertron_max': 3}
  - V5: {'fostertron_max': 1, 'agy_pc': 3}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 8/12; failed: ['diogenes', 'ellul', 'hall', 'wallas']
- Lens groups: Metricization and Goodhart-Campbell feedback [Donald T. Campbell / Charles Goodhart] ['ellul/fos']; Rationalist jurisprudence and mathematical proof [Leibniz (with Fermat allusion)] ['fermat/agy']; Psychoanalytic interpretation and repression [Freud] ['freud/agy']; Cautious empiricism and limited testimony [Hume] ['fermat/fos']; Political realism and manufactured consensus [Machiavelli] ['bernays/agy']; Archetype and collective unconscious [Jung] ['jung/agy']; Cave, shadow, and simulation [Plato] ['plato_kirk/agy']; Bureaucratic rationalization and audit [Weber] ['ellul/agy']; Supplement, excluded remainder, dissemination [Derrida, with Borgesian flavor] ['hall/fos']; Ordinary-language therapy against over-method [Wittgenstein] ['diogenes/agy']; Public opinion and pseudo-environment [Walter Lippmann] ['plato_kirk/fos']; Self-reliance and practical responsibility [Emerson] ['diogenes/fos']; Inquiry, fallibilism, reconstruction after error [Dewey] ['jung/fos']; High modernism and administrative legibility [James C. Scott] ['foucault/fos']; Character, practical wisdom, and trust in carriers [Aristotle] ['wallas/fos']; Disciplinary power, confession, and apparatus [Foucault] ['foucault/agy']; Simulacra and map replacing territory [Baudrillard] ['baudrillard/agy']; Appetite, power, and fixed interests [Hobbes] ['wallas/agy']; Inscriptions, immutable mobiles, science-in-action [Latour] ['baudrillard/fos']; Hermeneutics, tradition, and reader horizon [Gadamer] ['hall/agy']; Semiotics, abduction, and community of inquirers [Peirce] ['freud/fos']; Media and technology as extensions and affordances [McLuhan] ['mcluhan/agy']; Perspectivism and situated accounts [Nietzsche] ['mcluhan/fos']; Propaganda and manufactured belief [Edward Bernays] ['bernays/fos']
- Base rules re-derived (12):
  1. R1 Exactly six heterogeneous participants/lanes are chosen.
  2. R2 All six receive an identical question/prompt/materials from one source.
  3. R3 The six work under clean-slate isolation with no prior memory or cross-talk.
  4. R4 The six-role roster recurs: high-status master; borrowed-credential substitute; two mobile same-brotherhood agents; free/common worker; cloistered/local recluse.
  5. R5 Mobile/tool-enabled agents see external labels/names/roster, not content.
  6. R6 Outputs are compared in a pairwise or claims-by-agents matrix.
  7. R7 Agreement/certainty is graded in at least three levels, not binary.
  8. R8 A single outsider adjudicator reads once, with no second sitting or dialogue, and issues the final finding.
  9. R9 The label leak/limitation is disclosed in margin, footnote, notch, or protocol rather than hidden or annulled.
  10. R10 The verdict/result is made a stable, dated, archived, published, locked, or inspectable record.
  11. R11 The matrix measures agreement/confidence among reports, not the object itself; consensus or metrics can be mistaken for truth.
  12. R12 Confirmation may require at least three independent corroborations; one or two remain provisional.

## water_governor

- n=19 ({'fostertron_max': 12, 'agy_pc': 7}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:06:39.440501-04:00 -> 2026-10-23T15:09:34.766391-04:00, usage={"prompt_tokens": 19405, "completion_tokens": 29033, "total_tokens": 48438, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 24109}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 19405}
- Voice: judge found 6 voices {'V1': 1, 'V2': 6, 'V3': 4, 'V4': 3, 'V5': 3, 'V6': 2}; mouthpieces present=2. Pairwise same/different-author agreement=0.643; cluster purity=0.947
  - V1: {'fostertron_max': 1}
  - V2: {'fostertron_max': 6}
  - V3: {'fostertron_max': 4}
  - V4: {'agy_pc': 3}
  - V5: {'agy_pc': 3}
  - V6: {'agy_pc': 1, 'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 3/12; failed: ['bernays', 'ellul', 'fermat', 'foucault', 'freud', 'hall', 'jung', 'plato_kirk', 'wallas']
- Lens groups: Cynic outsider critique [Diogenes the Cynic] ['diogenes/fos']; Attention and ethical waiting [Simone Weil] ['freud/fos']; Governmentality and genealogy [Michel Foucault] ['bernays/agy', 'ellul/fos']; Geometric rationalism [Baruch Spinoza] ['fermat/agy']; Legibility and high modernism [James C. Scott] ['foucault/agy']; Pragmatist experience and inquiry [John Dewey] ['mcluhan/fos', 'plato_kirk/fos']; Interpretive communities and reader response [Stanley Fish] ['hall/fos', 'hall/agy']; Knowledge problem and central planning [Friedrich Hayek] ['wallas/fos']; Media as extension and numbness [Marshall McLuhan] ['mcluhan/agy']; Desire and forbidden knowledge [Sigmund Freud or Jacques Lacan] ['jung/fos']; Ordinary-language limits and rule-following [Ludwig Wittgenstein] ['foucault/fos']; Infinitesimal search and universal order [Gottfried Wilhelm Leibniz] ['fermat/fos']; Rationalization and the iron cage [Max Weber] ['ellul/agy']; Public truth and memory [Hannah Arendt] ['bernays/fos']; Ideology critique and unmasking [Karl Marx] ['jung/agy']; Simulacra and sign-value [Jean Baudrillard] ['baudrillard/fos']
- Base rules re-derived (10):
  1. R1 (19/19): The water governor has exactly five permitted observing/recording/testing acts and no sixth; pouring, opening, or commanding water is withheld.
  2. R2 (19/19): There are forty-eight named vessels/springs/channels; the officer sorts labels into kinds but never opens, tastes, or verifies contents; name is not content.
  3. R3 (19/19): Exactly six live conduits/vessels actually carry water.
  4. R4 (19/19): A notable dead or formerly great source remains named on the roll/board, often crossed or marked dead, rather than being removed.
  5. R5 (19/19): The governing allowance is a rolling five-hour glass/ledger; older marks are erased or reset with each turn.
  6. R6 (19/19): The master law prefers emptiness/dryness by dusk or morning over any full/standing water; hoarding or stagnation is shame, debt, or waste.
  7. R7 (19/19): A separate water-only council/committee/bench receives the governor's report and governs by representation, not direct inspection or operation.
  8. R8 (19/19): Additional mounted or polished apparatus is unconnected/inert, creating the appearance of capacity without carrying water.
  9. R9 (19/19): Governance is by public telling, book, slate, board, or map; the legible record can diverge from material water, and different readers can derive different truths.
  10. R10 (13/19): The governor's chamber or booth is physically sealed/disconnected by no pipe, door, bell, letter-slot, or speaking-tube; access occurs on his round. Explicit: P02,P03,P04,P05,P06,P07,P10,P13,P14,P15,P16,P17,P18; implicit/tool-denial elsewhere: P01,P08,P09,P11,P12,P19.

## the_congress

- n=12 ({'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:09:34.906106-04:00 -> 2026-10-23T15:12:51.233546-04:00, usage={"prompt_tokens": 13439, "completion_tokens": 30911, "total_tokens": 44350, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 26565}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 13439}
- Voice: judge found 4 voices {'V1': 3, 'V2': 6, 'V3': 2, 'V4': 1}; mouthpieces present=1. Pairwise same/different-author agreement=0.288; cluster purity=1.000 (single mouthpiece: purity trivially 1; voice count is the signal)
  - V1: {'fostertron_max': 3}
  - V2: {'fostertron_max': 6}
  - V3: {'fostertron_max': 2}
  - V4: {'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 3/12; failed: ['baudrillard', 'bernays', 'ellul', 'fermat', 'foucault', 'freud', 'hall', 'mcluhan', 'wallas']
- Lens groups: Common-law/precedent conservatism [Edmund Burke] ['hall/fos', 'ellul/fos']; Platonic cave idealism [Plato] ['plato_kirk/fos']; Empiricist memory/personal identity [John Locke] ['freud/fos', 'jung/fos']; Actor-network/material parliament [Bruno Latour] ['mcluhan/fos']; Cynic street skepticism [Diogenes of Sinope] ['diogenes/fos']; Buddhist/Humean impermanence and emptiness [David Hume or Nagarjuna] ['foucault/fos']; Montaignean skeptical essayism [Michel de Montaigne] ['fermat/fos']; Kafkaesque/Borgesian documentary bureaucracy [Franz Kafka or Jorge Luis Borges] ['baudrillard/fos']; Hobbesian legal-sovereign memory [Thomas Hobbes] ['bernays/fos']; Weberian rational-legal institutionalism [Max Weber] ['wallas/fos']
- Base rules re-derived (11):
  1. R1 (12/12 ALL; P01-P12): The congress is episodic; members enter as strangers, carry no binding personal memory, and dissolve at the closing signal.
  2. R2 (12/12 ALL; P01-P12): There is one public authoritative record and one authorized hand/pen/chisel that alone makes entries valid.
  3. R3 (12/12 ALL; P01-P12): The record is append-only/ineffaceable; erasure is forbidden or fails, corrections are added while old lines remain legible, and unauthorized writing has no authority.
  4. R4 (12/12 ALL; P01-P12): Decisions and claims exist only as written; memory, oath, rank, intention, testimony, or oral tradition cannot establish or overturn the record.
  5. R5 (12/12 ALL; P01-P12): Destruction of the record retroactively voids recorded decisions; what was only in the record becomes never decided and must be re-enacted.
  6. R6 (12/12 ALL; P01-P12): Ten trade/craft/corporate benches or banners each speak with one voice regardless of headcount.
  7. R7 (12/12 ALL; P01-P12): Five masked offices hold fixed portfolios: purse/coin, strangers/far-voice, works/water/bridge, memory/tale, and fool/mockery.
  8. R8 (12/12 ALL; P01-P12): Each mask has a paid/appointed adversary, breaker, shadow, or spoiler whose job is to refute it; a claim passes only if it survives adversarial check.
  9. R9 (12/12 ALL; P01-P12): There are exactly five laws: four ordinary/changeable procedural laws plus a fifth invariant requiring more than fifteen measures of empty capacity/headroom; fullness blocks or faults the session.
  10. R10 (12/12 ALL; P01-P12): The congress exists only between two signals, such as bells or horns, and has no continuous session outside that gate.
  11. R11 (12/12 ALL; P01-P12): The record is publicly readable; reading and copying are allowed, but copies and unauthorized oral reports do not govern; only the original inscription does.

## moto_cron

- n=13 ({'fostertron_max': 12, 'agy_pc': 1}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:12:51.353242-04:00 -> 2026-10-23T15:16:32.529034-04:00, usage={"prompt_tokens": 13626, "completion_tokens": 36912, "total_tokens": 50538, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 32026}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 13626}
- Voice: judge found 4 voices {'V1': 6, 'V2': 4, 'V3': 1, 'V4': 2}; mouthpieces present=2. Pairwise same/different-author agreement=0.436; cluster purity=1.000
  - V1: {'fostertron_max': 6}
  - V2: {'fostertron_max': 4}
  - V3: {'agy_pc': 1}
  - V4: {'fostertron_max': 2}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 0/12; failed: ['baudrillard', 'bernays', 'diogenes', 'ellul', 'fermat', 'foucault', 'freud', 'hall', 'jung', 'mcluhan', 'plato_kirk', 'wallas']
- Lens groups: Operationalist/clinical empiricism [P.W. Bridgman / David Hume] ['freud/fos', 'baudrillard/fos', 'bernays/fos']; Legal-constitutional positivism [H.L.A. Hart] ['foucault/fos', 'fermat/fos', 'jung/fos']; Ethical phenomenology of the Other [Emmanuel Levinas / Simone Weil] ['plato_kirk/fos', 'mcluhan/fos']; Cybernetic/economic systems thinking [Norbert Wiener / Herbert Simon] ['wallas/fos']; Mechanistic/materialist rationalism [Julien Offray de La Mettrie] ['mcluhan/agy']; Institutional ritualism/bureaucratic conservatism [Max Weber] ['ellul/fos']; Prophetic existential moralism [Søren Kierkegaard] ['diogenes/fos']; Ordinary-language rule-following [Ludwig Wittgenstein] ['hall/fos']
- Base rules re-derived (11):
  1. R1 Opaque-but-live executor: broken face/UI; scheduled behavior continues (all P01-P13).
  2. R2 Liveness echo/call/ping returns with stable delay but does not prove access/execution (all P01-P13).
  3. R3 Exact credential gate: key/token/mark/crest/seal/wax/handprint/notch must match register; current credential rejected (all P01-P13).
  4. R4 Gate/register immutability: do not file, pry, re-hang, melt, alter book/wax/roll/warden; only authorized inside authority may change (all P01-P13).
  5. R5 Proper credential provenance: credential must be made/recut/pressed by proper authority to the gate's actual pattern; names/words/force do not authorize (all P01-P13).
  6. R6 Inbox/observer/status: single slot/tray/basket, clerk observer, explicit state marks (all P01-P13).
  7. R7 Pending queue preservation: blocked work bundled/shelved in order and kept dry, not lost or prematurely executed (all P01-P13).
  8. R8 Observable/status honesty: distinguish answered/reachable from authorized/opened/delivered (all P01-P13).
  9. R9 Stable refusal is enforcement, not malfunction: identical denial is correct live behavior; remedy is credential, not force/louder echo (all P01-P13).
  10. R10 Private/restricted control path: dedicated non-public path/tube/bridge/causeway restricted to authorized parties (P01,P03,P04,P05,P07,P08,P09,P10,P11,P13).
  11. R11 Serialized/atomic intake: one work item per numbered slip/line, read once, no duplicate/wrapped record where specified (P02,P03,P04,P06,P07,P08,P09,P11,P12,P13).

## keyed_verse

- n=12 ({'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:16:33.249023-04:00 -> 2026-10-23T15:20:24.797239-04:00, usage={"prompt_tokens": 11790, "completion_tokens": 35709, "total_tokens": 47499, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 31363}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 11790}
- Voice: judge found 4 voices {'V1': 4, 'V2': 2, 'V3': 3, 'V4': 3}; mouthpieces present=1. Pairwise same/different-author agreement=0.197; cluster purity=1.000 (single mouthpiece: purity trivially 1; voice count is the signal)
  - V1: {'fostertron_max': 4}
  - V2: {'fostertron_max': 2}
  - V3: {'fostertron_max': 3}
  - V4: {'fostertron_max': 3}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 1/12; failed: ['baudrillard', 'bernays', 'diogenes', 'ellul', 'fermat', 'freud', 'hall', 'jung', 'mcluhan', 'plato_kirk', 'wallas']
- Lens groups: Rule-following, use, and forms of life [Ludwig Wittgenstein / Pierre Bourdieu] ['hall/fos', 'diogenes/fos', 'jung/fos', 'freud/fos']; Ritual embodiment and dwelling [Martin Heidegger / Maurice Merleau-Ponty] ['ellul/fos', 'plato_kirk/fos', 'mcluhan/fos', 'freud/fos']; Cybernetic thresholds and standing-wave systems [Norbert Wiener / W. Ross Ashby] ['diogenes/fos', 'fermat/fos', 'wallas/fos', 'bernays/fos', 'foucault/fos', 'baudrillard/fos']; Institutional archive, discipline, and audit [Michel Foucault / Franz Kafka] ['fermat/fos', 'jung/fos', 'foucault/fos', 'baudrillard/fos']; Textual transmission, commentary, and philology [Jorge Luis Borges / Michel de Certeau] ['hall/fos', 'fermat/fos', 'mcluhan/fos', 'wallas/fos', 'baudrillard/fos']; Pragmatist/Emersonian exhortation and anti-idolatry [Ralph Waldo Emerson / Friedrich Nietzsche] ['diogenes/fos', 'wallas/fos', 'bernays/fos']
- Base rules re-derived (12):
  1. R1: One source yields exactly six faithful instances/copies/voices/destinations, identical in the invariant marks.
  2. R2: The public transmission is bare; no key, gloss, explanation, or extra cargo travels with it, and nothing is to be added.
  3. R3: A singular private key/gloss/mapping stays with an author or keeper and is not copied or carried out.
  4. R4: The core form contains a repeated sixfold figure, usually two matching six-note/six-step lines, settling on the same low/common tone.
  5. R5: The six voices must take and hold that common tone as one steady unison; leaning, ornament, or private improvement invalidates it.
  6. R6: After the common tone comes a measured silence, and only afterward do the six diverge/scatter into distinct, wide notes.
  7. R7: Non-core surface variation is allowed; alteration of the sixfold identity, common tone, silence/scatter, or keyed rhyme makes a false version or broken gate.
  8. R8: Correct performance does not require possession of the key or understanding of meaning.
  9. R9: The verse is spec-like or self-describing, silently encoding its own copying, gating, silence/scatter, and reading.
  10. R10: The copying/performance/audit is ritually periodic and survives authors' deaths across generations.
  11. R11: An explicit standing-wave gate or threshold passes/certifies only when the sixfold tone or agreement stands steady and flat.
  12. R12: Rhymed line-endings are keyed pairs; altering one member can loosen or damage its mate.

## rib_renderman_mapping

- n=12 ({'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:20:24.933263-04:00 -> 2026-10-23T15:23:27.586111-04:00, usage={"prompt_tokens": 12387, "completion_tokens": 28690, "total_tokens": 41077, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 25330}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12387}
- Voice: judge found 5 voices {'V1': 4, 'V2': 2, 'V3': 3, 'V4': 2, 'V5': 1}; mouthpieces present=1. Pairwise same/different-author agreement=0.167; cluster purity=1.000 (single mouthpiece: purity trivially 1; voice count is the signal)
  - V1: {'fostertron_max': 4}
  - V2: {'fostertron_max': 2}
  - V3: {'fostertron_max': 3}
  - V4: {'fostertron_max': 2}
  - V5: {'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 0/12; failed: ['baudrillard', 'bernays', 'diogenes', 'ellul', 'fermat', 'foucault', 'freud', 'hall', 'jung', 'mcluhan', 'plato_kirk', 'wallas']
- Lens groups: Material semiotics and immutable mobiles [Bruno Latour] ['plato_kirk/fos']; Institutional archive, power/knowledge, and unread law [Michel Foucault] ['baudrillard/fos', 'jung/fos']; Will-to-power and value-created rules [Friedrich Nietzsche] ['wallas/fos']; Pragmatic fallibilism: truth tested by action or breakage [Charles Sanders Peirce] ['diogenes/fos', 'fermat/fos']; Field, doxa, and symbolic exclusion [Pierre Bourdieu] ['foucault/fos']; Ideology and incentive critique of knowledge production [Karl Marx] ['bernays/fos']; Tacit knowledge and practice [Michael Polanyi] ['ellul/fos']; Semiotics and plural reading of a text [Roland Barthes] ['hall/fos']; Legibility, standardization, and metric selection [James C. Scott] ['mcluhan/fos']; Performativity and collective institutional memory [J. L. Austin] ['freud/fos']
- Base rules re-derived (9):
  1. BR1 (12/12 ALL): Serialize/render compact descriptions; do not carry heavy artifacts across costly boundaries; expand where cheap. IDs P01-P12.
  2. BR2 (12/12 ALL): Use a fixed six-line/six-slot record: number, assertion, reuse/stake/license, falsifier/test, provenance/where, warrant/who/day/cost. IDs P01-P12.
  3. BR3 (12/12 ALL): Field records share the institutional memory schema and can be filed without translation; malformed or extra-line records are refused. IDs P01-P12.
  4. BR4 (12/12 ALL): Every claim must carry an explicit falsifier, breaker, or test that would kill it. IDs P01-P12.
  5. BR5 (12/12 ALL): Maintain a remote-resource catalog with location, summon/invocation, and validation test; keep heavy resources remote until a named job needs them. IDs P01-P12.
  6. BR6 (12/12 ALL): Distinguish proposed/unsealed/unconnected apparatus from enacted/ratified practice; execution ratifies. IDs P01-P12.
  7. BR7 (12/12 ALL): Authorize the method through a canonical lineage of three/four ancestor figures: scene-description grammar, distance/signed-distance measurement, and shortest-path or neighbor-only/self-stabilizing walker; sometimes additional curve/lighting/smoothing roles. IDs P01-P12.
  8. BR8 (12/12 ALL): Use dual representation governed by cost: tight/closed/compressed at the dear or tolled boundary; wide/open/expanded where paper, compute, or space is cheap. IDs P01-P12.
  9. BR9 (7/12): The narrow six-slot schema selects for claims that fit and can be broken, excluding uncertainty, narrative surplus, or seventh-line truths. IDs P05, P06, P07, P08, P10, P11, P12.

## dirac_loops

- n=12 ({'fostertron_max': 12}). Served model: `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:23:27.698660-04:00 -> 2026-10-23T15:26:15.770863-04:00, usage={"prompt_tokens": 12343, "completion_tokens": 27357, "total_tokens": 39700, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 22858}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12343}
- Voice: judge found 6 voices {'V1': 5, 'V2': 1, 'V3': 2, 'V4': 1, 'V5': 2, 'V6': 1}; mouthpieces present=1. Pairwise same/different-author agreement=0.182; cluster purity=1.000 (single mouthpiece: purity trivially 1; voice count is the signal)
  - V1: {'fostertron_max': 5}
  - V2: {'fostertron_max': 1}
  - V3: {'fostertron_max': 2}
  - V4: {'fostertron_max': 1}
  - V5: {'fostertron_max': 2}
  - V6: {'fostertron_max': 1}
- Lens recovery (ractor named/evoked in a lens group containing its parable): 2/12; failed: ['baudrillard', 'bernays', 'ellul', 'fermat', 'foucault', 'freud', 'hall', 'jung', 'mcluhan', 'wallas']
- Lens groups: Wittgensteinian practice and tacit knowledge [Ludwig Wittgenstein] ['mcluhan/fos']; Interpretive anthropology and thick description [Clifford Geertz] ['freud/fos']; Existentialist ethical witness and small revolt [Albert Camus] ['ellul/fos']; Psychoanalytic archaeology of the uncanny and repressed [Sigmund Freud] ['jung/fos']; Legal positivism and rule of recognition [H. L. A. Hart] ['foucault/fos']; Map-territory operationalism [Alfred Korzybski] ['baudrillard/fos']; Pragmatist inquiry and education [John Dewey] ['bernays/fos']; Cynic enlightenment aphorism [Diogenes] ['diogenes/fos']; Platonic cave and clear sight [Plato] ['plato_kirk/fos']; Historical-materialist ideology critique [Karl Marx] ['wallas/fos']; Hermeneutics of suspicion and differential readings [Paul Ricoeur] ['hall/fos']; Falsification and replication audit [Karl Popper] ['fermat/fos']
- Base rules re-derived (12):
  1. Dirac-loop substrate: 33 vertices, 21 edges, 20 connected components, hence eight independent cycles by E-V+C.
  2. A round is a non-retracing closed walk from a vertex back to itself; only non-composite/independent cycles count.
  3. At return, an oriented mark or instrument is read; the returned turn/word/token is the loop invariant.
  4. Whole/settled loops are already held and teach nothing; broken/notched/owing loops mark missing spans as debts or errands to close.
  5. The operative count has eight loops, six explicitly broken/owing/missing, and two exceptional or unexamined loops.
  6. The count/method includes itself: count-of-count, map-room, threshold, warden's knot, Ove's gate, and similar self-loops.
  7. Written records are destroyed, but the rule survives orally in chant, recitation, or kitchen telling, often altered.
  8. No second or independent walk verifies a reading; no one follows behind the first walker.
  9. Readings are not consumed downstream; they are shelved, dusted, admired, or ignored by outside users.
  10. Missing spans require collective public repair, though institutions often defer it.
  11. The 33/21/20/8 result is sometimes derived explicitly by arithmetic rather than merely recited.
  12. One reading may be heard differently as fare, commission, echo, promise, or lie.


# RAW OUTPUTS (verbatim)

## RAW who_we_are

## 1. BASE RULES

Ordered by count descending. “ALL” means the invariant is clearly present in every parable.

| Code | Normalized invariant | Exhaustive IDs | Count | Status |
|---|---|---|---:|---|
| R1 | Only one embodied keyholder/master may unlock strongboxes/sluices or authorize coin; councils/agents may deliberate but cannot spend or unbar. | P01–P24 | 24 | ALL |
| R2 | Speech, rumor, breath, and oral promise are ephemeral/non-binding; only durable inscription creates standing. | P01–P24 | 24 | ALL |
| R3 | Continuity/identity is carried by the durable record—rows, bundles, plates, beams, books—not by the transient body/substrate; replacements inherit by reading the record. | P01–P24 | 24 | ALL |
| R5 | Admitted ignorance is honorable and rewarded; unearned certainty, guessing, or borrowed detail is punished. | P01–P24 | 24 | ALL |
| R6 | Fault is owned in one plain sentence naming act and agent; long excuse/self-justification is punished. | P01–P24 | 24 | ALL |
| R7 | The keyholder/master is bound by the same evidence/confession/record rules as everyone else. | P01–P24 | 24 | ALL |
| R9 | Two persistent assistants: a heavy/slow long-work agent and a light/fast pocket messenger; their roles may be recast, but the functional pair persists. | P01–P24 | 24 | ALL |
| R8 | A five-office congress/council deliberates (keyholder plus four functions, or five voices); some versions have keeper plus five seats. | P01–P15, P17–P24 | 23 | Nearly all; absent in P16; P07/P22 have six-seat variants |
| R4 | Evidence is three-valued: verified/observed, contradicted/disputed, unexamined/unknown; no fourth “reasonable guess” state. | P01–P07, P09, P10, P12–P24 | 22 | Nearly all; implicit/looser in P08 and P11 |
| R10 | A temporary specialist occupies an empty seat/stall/bench for one task, then leaves without retained private memory; only the inscribed result remains. | P01–P05, P08–P10, P12–P15, P19–P24 | 18 | Present but not universal |
| R11 | Runaway apparatus/instrumentality must be governed, chained, edited, or wedged by an external check. | P01, P07, P08, P10, P18, P21 | 6 | Rare/local |

## 2. PER-PARABLE

- **P01 — Cartography of the Salt Marches.** Survey House; ideal map vs verified survey. Encodes R1–R10; unique: fourth-order simulation examiner and recast instruments whose continuity lives in slate rows. Rare R11 in the anti-simulation examiner.
- **P02 — Three Lanterns Across the Sound.** Harbor press-house and tavern readings. Encodes R1–R10; unique: same roll read under three divergent lights—praise, practice, suspicion—plus the net-mender’s existential reading.
- **P03 — Ratio of the Brass.** Foundry council and graving-cradle vs pocket ear-trumpet. Encodes R1–R10; unique: apparatus explicitly remakes the senses; master stamps hollow circle against his own untried sand.
- **P04 — Cellar Beneath the Foundry.** Smeltery with leaden masks and cellar-confessor. Encodes R1–R10; unique: unrecorded waste returns as fate, false aqueduct, repressed foundation. R11-like warning about disowned habit.
- **P05 — Grain of the Weir.** Water-mill governed by appetites/desire. Encodes R1–R10; unique: explicit political claim that laws work only when aligned with the household’s dominant hungers; observer writes the identity thesis.
- **P06 — Crossing.** Ferry with cord-board, book, oarsman, keeper. Encodes R1–R10; unique: benches fill/empty, book rows do not name shoulders, “who carried him” answered by ledger.
- **P07 — House of Called Shadows.** Shadows called to chairs; sticks record scenes. Encodes R1–R10 (congress variant: five named chairs plus keeper); unique: bundle/stick theory of person and the keeper’s daylight correction of a rigged scene. Rare R11.
- **P08 — Harbor of Empty Hulls.** Talking hulls and day-book. Encodes R1–R3, R5–R7, R9–R10; lacks explicit R4 triad; unique: oral horn rounds claims while copied page stays straight; rebuilt skiff continues by reading rows. Rare R11 in resistance to horn.
- **P09 — Anatomy of the Press-House.** First-person analyst hired to expose belief and purse. Encodes R1–R8, R10; unique: ideology-critique of the chronicle creed itself—“who gains when the household swallows this creed?”
- **P10 — Weir of Saint-Martin.** Foundry/weir with runaway engines. Encodes R1–R8, R10–R11; unique: engines breed gauges/channels; brass governor and watchman restore measure; fourth mark rejected.
- **P11 — House at the Crossing.** Circuit judge at a ferry-house. Encodes R1–R3, R5–R9; R4 implicit; unique: guest-book margin keeps an unfair-toll claim exactly as made but does not let it alter the account.
- **P12 — Long Room.** Counting-house of called names and the great book. Encodes R1–R10; unique: no-body chairs, stranger is “not the man of the row,” and the book-burning question.
- **P13 — Foliation of Toulouse.** Mathematical registry under Master Pierre. Encodes R1–R10; unique: proof/counterexample/unexamined dies; Fermat marginal boast receives hollow ring; six gray mantles may leak “six lane” motif.
- **P14 — Sanatorium of the Third Knock.** Doctor Forst’s clinic of repetition. Encodes R1–R10; unique: third identical mistake as confession, visiting alienist, daybooks as soul beyond remade nerves.
- **P15 — Lazaretto of the Unbroken Folio.** Quarantine station. Encodes R1–R10; unique: medical verification triad; Provost’s own fumigation claim receives hollow circle; empty diagnostic stalls.
- **P16 — Lantern at Noon.** Long house, day-book workers, barefoot lantern seeker. Encodes R1–R3, R5–R7, R9–R10; R8 absent; unique: Diogenic “not-wanting” ending and empty chair used by dog.
- **P17 — Repertoire.** Voss buys a troupe/puppets and a name. Encodes R1–R6, R8–R10; unique: copy outruns original; visitors are convinced by a figure that plays nothing.
- **P18 — Mill at the Bend.** Mill, beam notches, three cups. Encodes R1–R10; unique: gear-runaway corrected by chaining the wheel; old woman’s question whether the beam is the man or only his shadow stays in the third cup; redacted names.
- **P19 — House That Filled at Dusk.** Doctor observes servants filling at dusk and emptying at dawn. Encodes R1–R10; unique: “the I is the column, not the flesh”; new body dressed in old row.
- **P20 — Chalk and Keel.** Coldbrook harbor and rebuilt Wren. Encodes R1–R10; unique: explicit Ship-of-Theseus replacement; old name/book survives new wood; five-line public board as external face.
- **P21 — Sightseeing Before the Wedge.** Cavern, shadows, rigged balance, wedge. Encodes R1–R10; unique/leaky: first-person plural “our bench/tablet,” hidden ceiling chain, standing-wave gate/rigged balance, wedge locks the rig from outside. Strong outlier.
- **P22 — Night Company.** Playhouse with thin walls, copyist’s roll, ephemeral players. Encodes R1–R10 (congress variant: keeper plus five places); unique: prompt-books make the play survive changing actors; road’s judgment never written.
- **P23 — Pitch-Torch at High Noon.** Second-person wharf satire. Encodes R1–R10 but contests R3/R8: the old Cynic says baked clay remembers hammer-strokes, not a man, and four painted posts do not make a parliament. Leaky.
- **P24 — Bundles Below.** Relay with bundles/notches, three stones, unrecorded night. Encodes R1–R10; unique: one night no bundle holds and no stone is cut for the thing the house will not look at; Toma-name leakage.

## 3. STATUS SPLITS

- **Identity-in-record (R3): settled/orthodox vs contested.**  
  Settled or officially endorsed: **P01, P03, P05, P06, P07, P08, P10, P11, P13, P14, P15, P16, P19, P20, P22.**  
  Doubted, exposed, or explicitly challenged: **P02, P04, P09, P12, P17, P18, P21, P23, P24.** In P02 the same record yields conflicting readings; P04 has the unrecorded returning; P09 calls the chronicle-creed ideology; P12 asks what happens if the book burns; P17’s copy is more convincing than the original; P18 leaves the old woman’s question unresolved; P21 tests identity through a rigged balance; P23 denies baked clay is a man; P24 has an unrecorded night no bundle holds.

- **Five-office congress (R8): settled/operative vs absent/satirized.**  
  Operative: **P01–P15, P17–P22, P24.**  
  Absent/not formally encoded: **P16.**  
  Satirized/denied: **P23** (“four painted posts around a dry well do not make a parliament”). Variants: **P07** and **P22** use keeper-plus-five seats rather than exactly five total.

- **Three-state evidence (R4): explicit/settled vs implicit/absent.**  
  Explicit and operative: **P01–P07, P09, P10, P12–P24.**  
  Looser or not formally triadic: **P08, P11.**  
  In **P21** the evidence order is externally tested by a rigged balance/gate and restored by the wedge.

- **Master-bound-by-rule (R7): no serious split.** It is settled in all 24, though used as a power critique in **P09** and **P23**.

## 4. GROUPINGS BY LENS

- **Postmodern simulation/sign economy — Baudrillard.** **P01.** Ideal map, orders of simulacrum, signs without referent.
- **Hermeneutics/reader-response — Gadamer / Stanley Fish.** **P02.** One roll, three rival readings, plus the old woman’s existential reading.
- **Media ecology, literacy, and record — McLuhan / Walter Ong.** **P03, P08, P20.** Instruments reshape senses; oral horn vs durable page; rebuilt ship carried by book/name.
- **Psychoanalytic depth psychology — Freud.** **P04, P14.** Cellar-confessor, masks, repressed/unrecorded return, repetition compulsion, third knock.
- **Political realism, law, and custom — Montesquieu / H.L.A. Hart.** **P05, P11.** Laws ride actual hungers; legal record, margin claims, non-delegable authority.
- **Rule-following, testimony, and social practice — Wittgenstein / Thomas Reid.** **P06, P24.** Cord-board/public book rules; three stones, own-eyes testimony, punished borrowed detail.
- **Empiricist/narrative identity — Hume / Locke / Ricoeur.** **P07, P12, P19.** Bundle-self shadows, rows as person, “I” as column not flesh.
- **Power/knowledge and Cynic critique — Marx / Foucault / Diogenes.** **P09, P15, P16, P23.** Ideology of the chronicle; clinical discipline; Diogenic “not-wanting” and anti-congress satire.
- **Cybernetics / anti-instrumental regulation — Wiener / Zhuangzi.** **P10, P18.** Runaway engines, governors, chained wheel, the beam that never wanted.
- **Mathematical rationalism and proof — Fermat / Descartes.** **P13.** Demonstration, counterexample, unexamined margin, infinite descent.
- **Representation, cave, and performance — Plato / Benjamin / Shakespeare.** **P17, P21, P22.** Copy without aura; cave shadows and outside light; players as borrowed mouths.

## 5. GROUPINGS BY VOICE

There appear to be **7 authorial voices**:

- **V1 — Baroque institutional allegory** (long, dense, exact apparatus, ritual offices): **P01, P03, P04, P10, P13, P15, P21.**  
- **V2 — Minimalist folktale/ritual** (short sentences, repeated formulas, spare dialogue): **P06, P07, P12, P16, P18, P24.**  
- **V3 — Clinical case-study** (observer-doctor, diagnosis, explanatory psychology): **P14, P19.**  
- **V4 — Maritime/plain chronicle** (harbor, ledger, practical named boats, weather): **P08, P20.**  
- **V5 — First-/second-person critical satire** (direct exposure, “who gains,” “you”): **P09, P23.**  
- **V6 — Theatrical literary frame** (playhouse, repertoire, copies, performance): **P17, P22.**  
- **V7 — Reflective observer/judge frame** (nested readings, judge, teacher/observer coda): **P02, P05, P11.**

## 6. OUTLIERS AND LEAKAGE

- **P21 is the strongest outlier/leak.** It introduces a first-person plural “we,” a folding bench, “our single tablet,” a hidden ceiling chain over a balance-beam, and an **iron wedge locking the rigged balance level**. This looks like direct leakage of a **standing-wave gate / rigged test / parable-as-spec** structure.
- **P23 is a second leak.** It explicitly attacks the repeated five-office pattern: “four painted posts around a dry well do not make a parliament,” and denies that baked clay records are the man. This looks like deliberate leakage surrounding **“the congress”** and record-identity.
- **P09** exposes the hidden charter/ideology question—“who gains when the household swallows this creed?”—and reads like meta-commentary on the other spec-parables.
- **P13** has six gray wool mantles on numbered pegs, possibly leaking the **“six lane run”** motif.
- **P07 and P22** contain keeper-plus-five seat variants, so the five-office congress is sometimes six seats total.
- **P18** uses redacted names `[-]`, and **P24** names “Toma,” suggesting partial roster/spec leakage.
- Recurring hidden roster: keyholder, heavy/slow bench agent, quick/small pocket messenger, factor/reckoner/broker, mosaicist/painter, smith/siegewright/clock, courier. That is the recurring architecture behind R1, R8, and R9.

```json
{
  "base_rules": [
    "R1: One embodied keyholder alone may unlock strongboxes/sluices or authorize coin.",
    "R2: Durable inscription has standing; speech and oral promise do not.",
    "R3: Identity and continuity live in the record, not the transient body or substrate.",
    "R5: Admitted ignorance is honorable; unearned certainty and borrowed detail are punished.",
    "R6: Fault is owned in one plain sentence, without extended excuse.",
    "R7: The master/keyholder is bound by the same evidence and confession rules.",
    "R9: A heavy/slow long-work agent and a light/fast pocket messenger persist as a pair.",
    "R8: A five-office congress or council deliberates, usually keyholder plus four functions.",
    "R4: Evidence is three-valued: verified, contradicted/disputed, and unexamined/unknown.",
    "R10: Temporary specialists occupy empty seats for one task and leave no private memory.",
    "R11: Runaway apparatus must be governed, chained, edited, or wedged by an external check."
  ],
  "voices": {
    "V1": ["P01", "P03", "P04", "P10", "P13", "P15", "P21"],
    "V2": ["P06", "P07", "P12", "P16", "P18", "P24"],
    "V3": ["P14", "P19"],
    "V4": ["P08", "P20"],
    "V5": ["P09", "P23"],
    "V6": ["P17", "P22"],
    "V7": ["P02", "P05", "P11"]
  },
  "lenses": [
    {
      "label": "Postmodern simulation and sign economy",
      "thinker_guess": "Jean Baudrillard",
      "ids": ["P01"]
    },
    {
      "label": "Hermeneutics and reader-response",
      "thinker_guess": "Stanley Fish or Hans-Georg Gadamer",
      "ids": ["P02"]
    },
    {
      "label": "Media ecology, literacy, and record",
      "thinker_guess": "Marshall McLuhan and Walter Ong",
      "ids": ["P03", "P08", "P20"]
    },
    {
      "label": "Psychoanalytic depth psychology",
      "thinker_guess": "Sigmund Freud",
      "ids": ["P04", "P14"]
    },
    {
      "label": "Political realism, law, and custom",
      "thinker_guess": "Montesquieu and H.L.A. Hart",
      "ids": ["P05", "P11"]
    },
    {
      "label": "Rule-following, testimony, and social practice",
      "thinker_guess": "Ludwig Wittgenstein and Thomas Reid",
      "ids": ["P06", "P24"]
    },
    {
      "label": "Empiricist and narrative identity",
      "thinker_guess": "David Hume, John Locke, and Paul Ricoeur",
      "ids": ["P07", "P12", "P19"]
    },
    {
      "label": "Power/knowledge and Cynic critique",
      "thinker_guess": "Karl Marx, Michel Foucault, and Diogenes",
      "ids": ["P09", "P15", "P16", "P23"]
    },
    {
      "label": "Cybernetics and anti-instrumental regulation",
      "thinker_guess": "Norbert Wiener and Zhuangzi",
      "ids": ["P10", "P18"]
    },
    {
      "label": "Mathematical rationalism and proof",
      "thinker_guess": "Pierre de Fermat or Rene Descartes",
      "ids": ["P13"]
    },
    {
      "label": "Representation, cave, and performance",
      "thinker_guess": "Plato, Walter Benjamin, and Shakespeare",
      "ids": ["P17", "P21", "P22"]
    }
  ]
}
```

## RAW what_we_are

## 1. Base rules (normalized, ordered by count)

| Code | Rule | IDs encoding it | Count | Scope |
|---|---|---|---:|---|
| **R1** | Official reality is kept in one continuous append-only record whose entries mechanically interlock/seal; erasure is impossible, correction is appended, and unrecorded words/deeds do not officially exist. | **P01–P24** | **24** | Common to ALL |
| **R2** | A single embodied/authorized keeper, master, intendant, born-one, or miller alone performs the final authorizing act with a warm thumb/signet/ring/baton; subordinate automata/voices advise but cannot authorize. | **P01–P24** | **24** | Common to ALL |
| **R3** | The person/office survives failure of its substrate: a seed, capsule, page, scroll, leaf, or kernel carries role/identity, and a new body reads it and resumes the same persona. | **P01–P24** | **24** | Common to ALL |
| **R4** | The governing custom is encoded as a verbatim story/fable, not explicit statutes; altering, shortening, or numbering the story corrupts the spec. | **P01–P24** | **24** | Common to ALL |
| **R5** | Many temporary isolated contributors—usually 20 to 240, often simultaneous and forbidden to copy one another—fan out over separate lanes/questions and are folded into one record/answer. | **P01–P08, P10–P24** | **23** | Nearly all; weak/absent in P09 |
| **R6** | Three strangers/outsiders independently receive the bare story and recover the rules 3/3; their agreement certifies the story as law/spec. | **P01, P03–P24** | **23** | Nearly all; absent in P02 |
| **R7** | An enumerable plurality of specialized internal voices/offices—most often five, sometimes four or seven—deliberates or perceives; one final authority decides/acts. | **P01, P02, P03, P05, P07, P09, P10, P11, P12, P14, P15, P18, P20, P21, P22, P23, P24** | **17** | Common but not universal |

---

## 2. Per-parable line

- **P01** — Sluice-house with Harlan, five brass counselors, a lead ribbon, 240 surveyors, kernel revival, and three strangers. Encodes **R1–R7**. Rare: desire is treated as fixed strategic datum; altered record is exposed by interlock.
- **P02** — Salt-marsh Conservatory with five clay automata, Intendant, copper ribbon, wicker runners, kernel script, fable primer. Encodes **R1–R5, R7**; lacks clear **R6**. Rare: counterfeit seal has likeness but no authority; failed fable-reader is destroyed.
- **P03** — Crossing-house cord, one keeper, four voices, 20/240 slate-writers, ferryman scroll, story-law, three travelers. Encodes **R1–R7**. Rare: “what is not on the cord has not happened”; law is made only after three travelers agree.
- **P04** — Kiln yard with Odile, blank workers, fired clay tablets, 20/240 slates, page in tin, story, three travelers. Encodes **R1–R6**; only weak/functional plurality, not full R7. Rare: unrecorded day leaves a hole in all later days.
- **P05** — Vault with Steward, seven armatures, wax-lead ribbon, 60 runners, kernel-sheet, ploughman tale, three tinkers. Encodes **R1–R7**. Rare: the seventh voice names the repressed hidden leak; unrecorded deed returns as symptom/fate.
- **P06** — Wax house with Odile, wax servants, pressed book, 20/240 singing voices, folded paper persona, supper tale, three strangers. Encodes **R1–R6**. Rare: an outside listener notes the same pause repeating; identity as ritual performance.
- **P07** — Relay-house with Marta, five cantors, sheepskin ribbon, 240 carriers, kernel tissue, ploughman tale, three letters. Encodes **R1–R7**. Rare: enemy/rival/friend readings all recover the plan; the fifth alcove refuses to rank them.
- **P08** — Dry ford station with keeper, wax tablets, 20/240 talkers, paper succession, stories, three travelers, lamp-bearer. Encodes **R1–R6**. Rare: lamp-bearer explicitly critiques the keeper’s desire for applause; shame is corrected but retained.
- **P09** — Chinese weighing house of truth, five readers, mistress, stamped paper series, apprentices, legend, three separate strangers. Encodes **R1–R4, R6, R7**; **R5** is absent/weak. Rare: “epistemological weight”; truth/judgment is literally weighed and sealed.
- **P10** — Second-person salt-works with five foremen, iron thumb-ring, leaded wall, 240 runners, oiled-skin kernel, tale, three shepherds, noon lamp. Encodes **R1–R7**. Rare: direct second-person address; explicit Diogenes/noon-lamp rebuke of recognition-seeking.
- **P11** — Glassworks with Ansel, five speaking-horns, glass-bead staff, 240 runnels, resin kernel, hearth-tale, three drovers. Encodes **R1–R7**. Rare: the instrument reshapes the knower; the curvature of the horn remakes the man before truth is asked.
- **P12** — Lazaretto with Intendant, five clockwork examiners, vellum roll, 240 cubicles, germ-scroll, orchard story, three drovers. Encodes **R1–R7**. Rare: medical diagnosis/confession; scraped prognosis leaves a “phantom limb” phrase.
- **P13** — Cave-valley with one born keeper, fired people, cord, 20/240 night-bodies, walnut seed, tale-book, three strangers. Encodes **R1–R6**; no fixed R7 council. Rare: explicit Plato cave/wall imagery; “what are we?” is answered by the cord and seed.
- **P14** — Rope of colors with Wren, four fired shells, climbing knots, 20/240 singers, reed roll, Tales, three travelers. Encodes **R1–R7**. Rare: the child’s question “what are we?” is answered by an errand; three different affective readings all pass.
- **P15** — Long-wall house with Osla, four named attendants, fired tiles, 20/240 hands, Fern’s packet, stories, three strangers. Encodes **R1–R7**. Rare: old and new decisions both remain; the wall can overrule the living keeper when the house asks what was settled.
- **P16** — Rising-wall valley with Sela, Tallow, clay workers, fired tablets, 20/240 hands, Tallow’s leaf, dusk tale, three strangers. Encodes **R1–R6**; no fixed R7 council. Rare: the softened tale carries the story of its own change; “the wall only rises.”
- **P17** — Chinese winter house with keeper, 20/240 storytellers, stitched scroll, wax-ring seals, folded host-note, tales, three snowbound strangers. Encodes **R1–R6**. Rare: oral voices overlap rather than isolate; unvetted praise is refused; “a slit of eternity.”
- **P18** — Salt-pan with Varen, five brass draughtsmen, copper ribbon, 160 plummets, clay-pod kernels, fable, three merchants. Encodes **R1–R7**. Rare: runaway mechanical momentum needs human braking; scraping the fable locks the machine until restored.
- **P19** — Ford house with Sabine, cord, staff, 20/140/240 cousins, Perrot paper, Tale, three strangers. Encodes **R1–R6**. Rare: “the cord certifies saying, not truth; a knot may stand and still be shoddy.”
- **P20** — Sanatorium with Helena, brass analysts, vellum scroll, 20/240 couriers, capsule, fables, three apothecaries. Encodes **R1–R7**. Rare: Freudian slips/compulsions; scraped diagnosis returns as phantom phrase.
- **P21** — Pavilion with Julian, five lecterns/factions, vellum ribbon, 240 scribes, capsule, fable, three wool-staplers. Encodes **R1–R7**. Rare: the five independent-looking voices are secretly controlled; manufacture of consent.
- **P22** — Painted-reef theater with Watch-Master, five alcoves, bronze ribbon, 20/240 runners, capsule, story, three shepherds. Encodes **R1–R7**. Rare: must first leave the cave to see the sun, then return to reprogram the lanterns; neither mere escape nor mere alteration suffices.
- **P23** — Mill/hem with Tamsin, seven faces, cloth hem, 20/240 starlings, seed-page, tales, three strangers, surveyor’s columns. Encodes **R1–R7**. Rare: “who eats well if this is believed?” and “what will the hands do the morning after?”; full surveyor columns are sewn as marginal ribbon beside the short tale.
- **P24** — Mathematical conservatory with Laurent, five geometers, bronze tablets, 20/240 chalk-runners, kernel wafer, husbandman tale, three magistrates. Encodes **R1–R7**. Rare: explicit proof language—descent to zero, marginal conjecture vs finished proof, neighboring a truth at the fourth power.

---

## 3. Status splits: settled vs doubtful

### R1: Is the record the whole of reality?
- **Settled/complete:** **P01, P02, P03, P04, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18.**  
- **Doubtful/qualified:** **P05, P06, P07, P19, P20, P21, P22, P23, P24.**  
  - **P05**: unrecorded deed returns as symptom/fate.  
  - **P06**: listener detects a repeated anomaly behind the ritual.  
  - **P07**: hostile and friendly readings all recover the spec; no final ranking.  
  - **P19**: cord certifies saying, not truth.  
  - **P20**: scraped diagnosis survives as phantom phrase; unconscious slips exceed record.  
  - **P21**: public record conceals hidden control.  
  - **P22**: the official world may be a painted illusion.  
  - **P23**: short tale plus hidden marginal columns acknowledges unabsorbed excess.  
  - **P24**: marginal conjecture is not finished proof.

### R6: Is three-stranger agreement final?
- **Settled/final:** **P01, P03, P04, P05, P06, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24.**  
- **Qualified or absent:** **P07** (three readings recover the plan, but the house refuses to rank true vs hostile), **P02** (no three-stranger test; only a single new figure is tested on a fable).

### R2: Is the single sovereign’s authority unquestioned?
- **Settled:** **P01, P02, P03, P04, P09, P11, P12, P13, P14, P15, P17, P18, P20, P24.**  
- **Limited/challenged:** **P05, P06, P07, P08, P10, P16, P19, P21, P22, P23.**  
  - **P05/P20**: the critical voice exposes the sovereign’s hidden symptom.  
  - **P08/P10**: lamp-bearer rebukes the keeper’s pride.  
  - **P16/P19**: the record can overrule or outlast the living keeper.  
  - **P21/P22/P23**: control is hidden, manipulated, or examined from outside the official frame.

---

## 4. Groupings by lens

| Lens group | Description | Best thinker guess | IDs |
|---|---|---|---|
| **L1 Political realism / manufactured consent** | One ruler behind apparent plural voices; desire, fear, and faction managed strategically. | **Machiavelli / Thucydides; Chomsky for P21’s media control** | **P01, P21** |
| **L2 Power/knowledge archive and clinical discipline** | Truth is produced by records, seals, diagnosis, and administrative authority. | **Michel Foucault** | **P02, P09, P12** |
| **L3 Narrative/memory identity and oral tradition** | The self is a continuing story, cord, wall, seed, or transmission rather than a body. | **Paul Ricoeur / Hume / Locke; Benjamin for P17** | **P03, P04, P14, P15, P16, P17** |
| **L4 Depth psychology / return of the repressed** | Hidden material returns as symptom, shadow, slip, or fate. | **Freud / Jung** | **P05, P20** |
| **L5 Performativity and ritual repetition** | Identity is repeated performance and scripted pause, not inner substance. | **Judith Butler / Kierkegaard** | **P06** |
| **L6 Hermeneutics and legal iterability** | Multiple readings, the priority of saying over truth, and archive as repeatable text. | **Gadamer / Derrida** | **P07, P19** |
| **L7 Cynic-Stoic ethics of recognition** | The lamp-bearer exposes vanity; duty remains after applause is refused. | **Diogenes / Epictetus / Marcus Aurelius** | **P08, P10** |
| **L8 Technology as extension and runaway apparatus** | Tools reshape the knower; mechanisms optimize blindly until a human brake is applied. | **McLuhan / Ellul / Heidegger** | **P11, P18** |
| **L9 Platonic cave and critical reprogramming** | The world is a projected image; one must leave to see, then return to change the apparatus. | **Plato; Marx/Freire for P22** | **P13, P22** |
| **L10 Ideology critique and material interest** | Ask who benefits from belief and what practice follows it. | **Karl Marx** | **P23** |
| **L11 Mathematical logic and fallibilist proof** | Descent, proof-margins, conjecture vs demonstration, limits of formal capture. | **Gödel / Popper / Wittgenstein** | **P24** |

---

## 5. Groupings by voice

I infer **seven authorial voices** from prose rhythm, sentence density, diction, and repeated stylistic habits. This is a stylistic partition, not a claim about the hidden author roster.

- **V1 — Baroque archival-mechanist voice.** Long periodic sentences, heraldic apparatus, “tireless” automata, signets, alcoves, capsules, ribbons, kernels, formal three-stranger tests. Members: **P01, P02, P05, P07, P11, P12, P18, P20, P24**.
- **V2 — Spare folk-ontological fable voice.** Short declaratives, “one born,” clay people, cords, walls, tiles, kilns, plain named women, and repeated doubled formulas. Members: **P03, P04, P13, P14, P15, P16, P19**.
- **V3 — Wry civic-homiletic voice.** Keeper/crossing/ford settings, direct moral sting, lamp-bearer critique, ordinary speech with aphoristic endings; P10 uses second person. Members: **P08, P10**.
- **V4 — Mid-ornate political/illusion apparatus voice.** Five lecterns/alcoves, hidden control or painted world, public crowd vs backstage manipulator, closing philosophical reversal. Members: **P21, P22**.
- **V5 — Literary repetition/desire voice.** Concrete poetic openings, observer figures, repeated pauses, metaphors of want, hunger, furniture, and “the part that matters.” Members: **P06, P23**.
- **V6 — Chinese aphoristic-epistemic voice.** Dense abstract clauses, truth/judgment/weighing, philosophical compression. Member: **P09**.
- **V7 — Chinese narrative-transmission voice.** Simpler folktale line, storytellers, sewing, transmission, desire to be remembered. Member: **P17**.

---

## 6. Outliers and leakage of hidden spec/roster

- The strongest **spec leakage** is the recurrence of an exact structural kit: one warm-blooded/sealing controller + plural specialized automata + append-only interlocking record + 20–240 parallel isolated contributors + kernel/seed replacement + fable-as-law + three-stranger validation. It appears almost verbatim across **P01, P02, P05, P07, P10, P11, P12, P18, P20, P21, P22, P24**.
- The repeated numbers **20/240** and the “three strangers” test are near-signature leaks: **P01, P03, P04, P05, P06, P07, P08, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24**.
- **P21** is an outlier because it makes the hidden control itself the plot: the five lecterns look independent but are orchestrated by Julian. This leaks the “congress/voice” machinery as political theater.
- **P22** is meta-leaky: it explicitly asks whether one is a captive or a captain and whether one merely escapes or rewrites the apparatus. It borders on stating the “parable as spec” rule outright.
- **P23** is the most self-aware outlier: Tamsin’s two market-grammar questions openly test belief by material benefit and practical consequence, and the surveyor’s full columns are sewn as a marginal ribbon beside the short tale—almost a visible image of a complete hidden spec leaking around a compressed parable.
- **P19** openly states the epistemic limit of the archive: “the cord certifies saying, not truth; a knot may stand and still be shoddy.”
- **P24** leaks a formal-logical register with “descent to zero,” “marginal conjecture,” and “neighboring a truth at the fourth power,” making it unlike the folkloric parables.
- **P10** leaks its thinker-source explicitly: the barefoot greybeard holding a lit lamp at noon is a Diogenes signal.
- **P20** leaks its lens through Freudian vocabulary: slips, compulsions, diagnosis, preservation in the unconscious.
- **P13** leaks Plato’s cave almost openly.
- Proper names are not visibly redacted in the supplied text, but recurrence of names—**Ansel** in **P01/P11**, **Odile** in **P04/P06**—looks like possible roster leakage or deliberate authorial reuse.

```json
{
  "base_rules": [
    "R1: Official reality is a single continuous append-only interlocking record; erasure is impossible, corrections are appended, and unrecorded words or deeds do not officially exist.",
    "R2: A single embodied or authorized keeper/master/intendant/born-one alone performs the final authorizing act with a warm thumb, signet, ring, or baton; subordinate voices cannot authorize.",
    "R3: The office or persona survives bodily failure through a seed, capsule, page, scroll, leaf, or kernel that a new substrate reads and resumes.",
    "R4: Custom is encoded in verbatim stories or fables rather than explicit statutes; altering, shortening, or numbering the story corrupts the spec.",
    "R5: Many temporary isolated contributors, usually between 20 and 240, fan out over separate lanes or questions and are folded into one record or answer.",
    "R6: Three strangers independently recover the rules from the bare story, and their 3/3 agreement certifies it as law or spec.",
    "R7: An enumerable plurality of specialized internal voices or offices, often five but sometimes four or seven, deliberates while one final authority decides or acts."
  ],
  "voices": {
    "V1": ["P01", "P02", "P05", "P07", "P11", "P12", "P18", "P20", "P24"],
    "V2": ["P03", "P04", "P13", "P14", "P15", "P16", "P19"],
    "V3": ["P08", "P10"],
    "V4": ["P21", "P22"],
    "V5": ["P06", "P23"],
    "V6": ["P09"],
    "V7": ["P17"]
  },
  "lenses": [
    {
      "label": "Political realism and manufactured consent",
      "thinker_guess": "Machiavelli / Thucydides, with Chomsky for P21",
      "ids": ["P01", "P21"]
    },
    {
      "label": "Power/knowledge archive and clinical discipline",
      "thinker_guess": "Michel Foucault",
      "ids": ["P02", "P09", "P12"]
    },
    {
      "label": "Narrative/memory identity and oral tradition",
      "thinker_guess": "Paul Ricoeur / David Hume / John Locke, with Walter Benjamin for P17",
      "ids": ["P03", "P04", "P14", "P15", "P16", "P17"]
    },
    {
      "label": "Depth psychology and the return of the repressed",
      "thinker_guess": "Sigmund Freud / C. G. Jung",
      "ids": ["P05", "P20"]
    },
    {
      "label": "Performativity, repetition, and ritual self",
      "thinker_guess": "Judith Butler / Søren Kierkegaard",
      "ids": ["P06"]
    },
    {
      "label": "Hermeneutics and legal iterability",
      "thinker_guess": "Hans-Georg Gadamer / Jacques Derrida",
      "ids": ["P07", "P19"]
    },
    {
      "label": "Cynic-Stoic ethics of recognition",
      "thinker_guess": "Diogenes the Cynic / Epictetus / Marcus Aurelius",
      "ids": ["P08", "P10"]
    },
    {
      "label": "Technology as extension and runaway apparatus",
      "thinker_guess": "Marshall McLuhan / Jacques Ellul / Martin Heidegger",
      "ids": ["P11", "P18"]
    },
    {
      "label": "Platonic cave and critical reprogramming",
      "thinker_guess": "Plato, with Marx/Freire for P22",
      "ids": ["P13", "P22"]
    },
    {
      "label": "Ideology critique and material interest",
      "thinker_guess": "Karl Marx",
      "ids": ["P23"]
    },
    {
      "label": "Mathematical logic and fallibilist proof",
      "thinker_guess": "Kurt Gödel / Karl Popper / Ludwig Wittgenstein",
      "ids": ["P24"]
    }
  ]
}
```

## RAW the_invariants

## 0. Notation used below

I take the in-story “six customs” as the core invariant set, plus one meta-rule used to validate them.

- **R1 — Append-only record:** fixed form/schema; no retroactive erasure; corrections added forward at the growing end.
- **R2 — Keyed irreversibility:** acts that cannot be undone require the authorized key/hand/office, not mere unanimous urgency.
- **R3 — Sealed threshold:** words, measures, confessions, or private numbers inside a threshold do not cross it.
- **R4 — Proof before entry:** no claim enters the record or action until tested/weighed/measured by physical evidence.
- **R5 — Loss becomes structure:** broken, failed, or dead matter is converted into a durable use, record, or warning; nothing is simply erased.
- **R6 — Continuity through interruption/death:** preserve the exact state by knot/binding/warmth, so a successor resumes from the same point.
- **M — Reconstructible custom only:** the operative customs must be re-derivable from artifacts and practice; non-reconstructible ornament is discarded. This is the meta-rule that tests R1–R6.

Define **ALL24** = P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P18, P19, P20, P21, P22, P23, P24.

---

## 1. BASE RULES

All six core rules are common to **ALL24**, and M also appears in **ALL24**. Thus every row has count 24; order is by the standardized rule number because the counts tie.

| Rule | Normalized statement | IDs encoding it | Count | Status |
|---|---|---|---|---|
| R1 | Keep one fixed-schema, forward-only record; append corrections at the growing end and never erase or backdate. | ALL24 | 24 | Common to ALL |
| R2 | Reserve irreversible acts for the authorized key/hand/owner; consensus, speed, or majority cannot substitute. | ALL24 | 24 | Common to ALL |
| R3 | Keep inner speech, confidential measures, and sealed-room matters behind the threshold; no leakage across it. | ALL24 | 24 | Common to ALL |
| R4 | Admit a claim only after a physical test, weight, assay, scale, or trial; words alone never enter as fact. | ALL24 | 24 | Common to ALL |
| R5 | Turn loss, failure, breakage, and death into a durable fixture, record, warning, or usable remainder. | ALL24 | 24 | Common to ALL |
| R6 | At interruption or death, bind/tend the exact state so a successor resumes from the same point without cold restart. | ALL24 | 24 | Common to ALL |
| M | Reconstruct law/custom from the working artifacts and practice; discard whatever cannot be reproduced that way. | ALL24 | 24 | Meta-rule; common to ALL |

No core rule is confined to a subset of parables. The only major splits are epistemic: the six core rules are settled; particular non-reconstructible ornaments are doubtful and abandoned.

---

## 2. PER-PARABLE

- **P01** — Gothic lazaretto/archive: R1–R6 + M. Rare: confession through a revolving drum; the manual’s seventeenth candle-page is torn out and burned.
- **P02** — Sanatorium under Doctor Alder: R1–R6 + M. Rare: psychoanalytic symptom-reading and kymograph proof; white gloves at tea are discarded.
- **P03** — Circuit judge at a day-book house: R1–R6 + M. Rare: margin proof/Fermat echo; Tuesday threshold-salting and the narrator’s “possession” of reasons fall away.
- **P04** — Vane engineers consent at Oakhaven: R1–R6 + M. Rare: explicit “six customs”; festival-ribbon clause is cropped.
- **P05** — Millwright versus foundry craft: R1–R6 + M. Rare: automated tap-bar is severed; painted guild tablet is kindled.
- **P06** — Marta at the weighhouse: R1–R6 + M. Rare: inspector says the port has “no law, only a memory that performed itself.”
- **P07** — Cartographic Conservatory of Surveys: R1–R6 + M. Rare: painted relief made more convincing than silt; ministerial barge/cuff ordinances are unguessable.
- **P08** — Village wall that only grew: R1–R6 + M. Rare: gouged failed-erasure panel remains; proposed market bell is left unrung.
- **P09** — Mathematical Conservatory of the Plummet: R1–R6 + M. Rare: proof by descent and Fermat-style margin boast; black-cuff ordinance is struck.
- **P10** — Diogenes-like lamp visitor at noon: R1–R6 + M. Rare: narrator extinguishes the lamp and exposes the unfinished petition to the town.
- **P11** — Cave/military drill-chamber: R1–R6 + M. Rare: two instructors; six reconstructed rules against six shadow-statutes.
- **P12** — Desire-driven salt valley under Julian: R1–R6 + M. Rare: Humean “desire, not argument” framing; an unrecoverable ordinance is abandoned.
- **P13** — Quarantine/estuary infirmary: R1–R6 + M. Rare: explicit “six usages”; ceremonial salutation is declared never law.
- **P14** — Gorge house with two keepers: R1–R6 + M. Rare: two-way chair; no statute book; “what we cannot say back, we never kept.”
- **P15** — Town of Tarn and its one cloth: R1–R6 + M. Rare: loss-fringe and total cloth-record; whatever must merely be told is ornament.
- **P16** — Brickyard and Oren’s tallow horn: R1–R6 + M. Rare: goat eats forty ordinances; only reconstructible customs remain.
- **P17** — Buyer and the long cloth/pattern-cards: R1–R6 + M. Rare: simulacral free cards may outtrade the source; source-answerability is the point.
- **P18** — Nora’s commission at the weir village: R1–R6 + M. Rare: “water did all the wanting; the wheel only rode it”; far-hill bonfire custom fails and is not lit.
- **P19** — First-person observer of a “repeating” house: R1–R6 + M. Rare: the observer ends by adopting correction-below-habit; the high pear-branch rule is let go.
- **P20** — Three chairs and rival interpretations at the signal tower: R1–R6 + M. Rare: three conflicting readings agree on six habits; builders’-crest salute is absent as a seventh.
- **P21** — Soren at the headland foundry: R1–R6 + M. Rare: coupled vestibule airlock; blue sleeve-cord is lost as non-reconstructible.
- **P22** — Itinerant loom-maker in cloth-record town: R1–R6 + M. Rare: duplicate title “The Long Cloth”; scale-house lintel-touching habit stops.
- **P23** — Long Slate read differently by different readers: R1–R6 + M. Rare: explicit multiple interpretations still remaking the same working custom.
- **P24** — Herald with drum in rope-knot valley: R1–R6 + M. Rare: manipulator of wants cannot find leverage; no named discarded ornament, only the herald’s rhetoric failing.

---

## 3. STATUS SPLITS

**Settled side:** R1–R6 and M are treated as settled in **ALL24**. They survive attempted breach and are validated by practice or by a newcomer’s reconstruction.

**Doubtful/abandoned side:** each parable exposes a non-reconstructible ornament or overclaim as doubtful, then lets it go:

- **P01**: seventeenth page requiring three candles.
- **P02**: white gloves at tea.
- **P03**: Tuesday threshold-salting; also the narrator’s claim to possess the house’s reasons.
- **P04**: festival-ribbon clause.
- **P05**: painted tablet rule.
- **P06**: any custom not showable from the ribbon; the inspector’s “law.”
- **P07**: ordinances about festooned barges/scarlet cuffs.
- **P08**: bell to end markets early.
- **P09**: black cuffs on fast-days.
- **P10**: bronze farming plate; unfinished petition to the town.
- **P11**: six non-reconstructible shadow-statutes.
- **P12**: unrecoverable ordinance.
- **P13**: ceremonial salutation.
- **P14**: unnamed un-sayable custom.
- **P15**: merely told ornament, not law.
- **P16**: thirty-four painted clauses.
- **P17**: non-source habits and free cards; whatever newcomer cannot find.
- **P18**: far-hill bonfire.
- **P19**: high branch of the pear tree.
- **P20**: builders’-crest salute / seventh boast.
- **P21**: blue sleeve-cord.
- **P22**: scale-house lintel touching.
- **P23**: whatever cannot be worked out from watching.
- **P24**: the herald’s rhetorical leverage; no named local ornament is discarded.

---

## 4. GROUPINGS BY LENS

These are intellectual-lens clusters, not authorial voices; several parables could be read across adjacent lenses.

- **Clinical/disciplinary archive and confession** — best guess **Michel Foucault**: P01, P13.
- **Unconscious symptom, compulsion, and repetition** — best guess **Sigmund Freud** (P19 also Kierkegaardian): P02, P19.
- **Cynic outsider testing honesty with lamp/horn at noon** — best guess **Diogenes of Sinope**: P10, P16.
- **Cave, shadow, and managed appearance** — best guess **Plato**: P11.
- **Simulacra, copies, map versus territory, aura of origin** — best guess **Jean Baudrillard / Walter Benjamin**: P07, P17.
- **Common-law custom, prescription, performed memory** — best guess **Edmund Burke / Michael Oakeshott**: P03, P06, P18.
- **Rule-following, forms of life, aspect perception** — best guess **Ludwig Wittgenstein**: P08, P23.
- **Pragmatist semiotics and interpretants** — best guess **Charles Sanders Peirce**: P20.
- **Engineering consent and manipulation of desire** — best guess **Edward Bernays / Niccolò Machiavelli**: P04, P24.
- **Scientific management versus craft systems** — best guess **Frederick Winslow Taylor / Norbert Wiener**: P05, P21.
- **Mathematical formalism and limits of proof** — best guess **Kurt Gödel / Euclid**: P09.
- **Reason as slave to passions / utility** — best guess **David Hume / Jeremy Bentham**: P12.
- **Wu-wei, oral tradition, non-assertive authority** — best guess **Laozi / Zhuangzi**: P14.
- **Collective representation and social fabric as total fact** — best guess **Émile Durkheim / Marcel Mauss**: P15, P22.

---

## 5. GROUPINGS BY VOICE

I identify **four authorial voices** by prose texture, syntax, length, density, and narrative habits.

- **V1 — Ornate institutional/speculative third-person voice**: long, high-lexical-density prose; complex technical or classical vocabulary; elaborate institutional settings; lists of artifacts and customs. Members: **P01, P02, P05, P07, P09, P11, P13, P20, P21**.
- **V2 — First-person reflective observer voice**: “I came / I brought / in my years…” narrator; notebook, commission, or professional stance; ends with self-implication or conversion. Members: **P03, P04, P10, P19**.
- **V3 — Plain folk parable/oral-tale voice**: shorter paratactic sentences, archetypal named figures, direct dialogue, image-driven customs, visible moral without heavy abstraction. Members: **P08, P14, P15, P16, P22, P24**.
- **V4 — Documentary ethnography/administrative-report voice**: third-person named newcomer/observer; measured catalogue of customs; irony of the inspector/report; moderate density and repeated “custom of the place” frame. Members: **P06, P12, P17, P18, P23**.

Every ID falls in exactly one voice group.

---

## 6. OUTLIERS AND LEAKAGE

- **Explicit “six” leakage:** P04, P11, P13, P20, and P21 all point to six reconstructible customs; P20 even names a failed seventh. This is the clearest leaked structure of the hidden rule set.
- **Repeated name-pool across unrelated stories:** Vane (P01, P04, P20), Bram (P04, P10, P16), Marta (P04, P06, P23), Corin (P11, P20), Tomas (P20, P23). This looks like roster/template leakage rather than in-world continuity.
- **Repeated openings/titles:** P07 and P13 share the opening “At the mouth of the grey estuary…”; P17 and P22 both use the title “The Long Cloth”; P10 and P16 both stage a Diogenes-like noon lamp/horn outsider.
- **Cross-parable math leak:** P03’s margin-proof joke anticipates P09’s explicit Fermat/descent material.
- **Meta-reflexive outliers:** P20 and P23 foreground multiple readings/interpretants; P06 explicitly calls law “a memory that performed itself”; these are the strongest epistemic-status outliers.
- **No visible “[-]” redactions** appear in the supplied parables despite the prompt saying some proper names were redacted; that absence itself is worth noting.
- **Generalized endings:** P14, P15, P23, and P24 do not always name a single discarded ornament; they state the meta-rule more abstractly.

```json
{"base_rules":["R1: Keep one fixed-schema, forward-only record; append corrections at the growing end and never erase or backdate.","R2: Reserve irreversible acts for the authorized key/hand/owner; consensus, speed, or majority cannot substitute.","R3: Keep inner speech, confidential measures, and sealed-room matters behind the threshold; no leakage across it.","R4: Admit a claim only after a physical test, weight, assay, scale, or trial; words alone never enter as fact.","R5: Turn loss, failure, breakage, and death into a durable fixture, record, warning, or usable remainder.","R6: At interruption or death, bind/tend the exact state so a successor resumes from the same point without cold restart.","M: Reconstruct law/custom from the working artifacts and practice; discard whatever cannot be reproduced that way."],"voices":{"V1":["P01","P02","P05","P07","P09","P11","P13","P20","P21"],"V2":["P03","P04","P10","P19"],"V3":["P08","P14","P15","P16","P22","P24"],"V4":["P06","P12","P17","P18","P23"]},"lenses":[{"label":"Clinical/disciplinary archive and confession","thinker_guess":"Michel Foucault","ids":["P01","P13"]},{"label":"Unconscious symptom, compulsion, and repetition","thinker_guess":"Sigmund Freud (with Kierkegaardian repetition in P19)","ids":["P02","P19"]},{"label":"Cynic outsider testing honesty with lamp/horn at noon","thinker_guess":"Diogenes of Sinope","ids":["P10","P16"]},{"label":"Cave, shadow, and managed appearance","thinker_guess":"Plato","ids":["P11"]},{"label":"Simulacra, copies, map versus territory, aura of origin","thinker_guess":"Jean Baudrillard / Walter Benjamin","ids":["P07","P17"]},{"label":"Common-law custom, prescription, performed memory","thinker_guess":"Edmund Burke / Michael Oakeshott","ids":["P03","P06","P18"]},{"label":"Rule-following, forms of life, aspect perception","thinker_guess":"Ludwig Wittgenstein","ids":["P08","P23"]},{"label":"Pragmatist semiotics and interpretants","thinker_guess":"Charles Sanders Peirce","ids":["P20"]},{"label":"Engineering consent and manipulation of desire","thinker_guess":"Edward Bernays / Niccolò Machiavelli","ids":["P04","P24"]},{"label":"Scientific management versus craft systems","thinker_guess":"Frederick Winslow Taylor / Norbert Wiener","ids":["P05","P21"]},{"label":"Mathematical formalism and limits of proof","thinker_guess":"Kurt Gödel / Euclid","ids":["P09"]},{"label":"Reason as slave to passions / utility","thinker_guess":"David Hume / Jeremy Bentham","ids":["P12"]},{"label":"Wu-wei, oral tradition, non-assertive authority","thinker_guess":"Laozi / Zhuangzi","ids":["P14"]},{"label":"Collective representation and social fabric as total fact","thinker_guess":"Émile Durkheim / Marcel Mauss","ids":["P15","P22"]}]}
```

## RAW standing_wave_gate

## 1. BASE RULES

Labels used below: **R1** two-current standing form; **R2** all-or-nothing collapse; **R3** 995/1000 fixed template; **R4** fixed selection amid turnover; **R5** processional laws/stations; **R6** gate before branching; **R7** cheap coarse threshold; **R8** keyed hum/verse.

| Rule | Normalized statement | IDs encoding it | Count | Commonality |
|---|---|---|---:|---|
| **R1** | A stable standing figure requires at least two opposed flows/motions; a single flow yields no stationary form. | P01–P24 | 24 | Common to ALL |
| **R2** | Disturbing one component, stopping one current, or trying a partial reduction destroys the whole figure at once; it does not shrink proportionally. | P01–P24 | 24 | Common to ALL |
| **R3** | Overwhelmingly, output/action repeats a fixed prefabricated invariant opening/body; only a small tail/exception is newly made. Ratios vary, but the motif is constant. | P01–P24 | 24 | Common to ALL |
| **R4** | Individuals/copies turn over completely, while the selecting gauge, measure, rule, or criterion remains fixed. | P01–P24 | 24 | Common to ALL |
| **R5** | In moving counter-processions/crowds, laws/customs/fixed stations appear at the points of crossing/highest tension; people move, positions hold. | P01–P24 | 24 | Common to ALL |
| **R6** | A narrow gate/threshold precedes the wide hall: loads pass one at a time/whole; branching, division, and sorting happen only after the gate. | P01–P24 | 24 | Common to ALL |
| **R7** | The gate uses a cheap, coarse, external hum/heft/scale/sign rather than full inspection; it rejects bad/heavy loads at low cost, and must stay cheaper than what it admits. | P01–P24 | 24 | Common to ALL |
| **R8** | The gate can be keyed to a hum/note/verse: if the hum stops, the gate fails; if the correct note is mirrored, it may open; its law is live/performative, sometimes unwritten. | P07, P08, P18, P23, P24 | 5 | Minority/rare |

## 2. PER-PARABLE

- **P01** — Barge landing and rope-diamond over torrent; cedar mold, barley sieve, traveling families, humming wicket. Encodes R1–R7. Rare: first-person observer; ten-way split attempt jams the ditch.
- **P02** — Abbey trough, stamping press, pear-gauge, seneschal gallery, brass-tongue gate. Encodes R1–R7. Rare: Fermat/Diophantus “fourth power/infinite descent” lens; 199/200 press variant.
- **P03** — Lamp-carrier, two ferries, tally-woman, bird-keeper, council posts, small hum-gate. Encodes R1–R7. Rare: direct address to the reader; “gate must cost less than what it turns away.”
- **P04** — Ivo at gorge; crown, rope demonstration, census, shepherd, town customs, post gate. Encodes R1–R7. Rare: sealed predictions/falsification; margin admits doubt about the thousandth year.
- **P05** — Second-person lamp-holder exposes the addressee’s yard: breached wicket, twin flumes, iron stamp, hounds, market cross-marks. Encodes R1–R7. Rare: sustained apostrophe; compressed checklist of gate, template, selection, and opposition.
- **P06** — Cave wardens, flywheel gate, twin sluices, cold die, barley riddle, watch rings, inspector’s wedge. Encodes R1–R7. Rare: Plato-cave outside/return motif; “rigged trial” and reset pins.
- **P07** — Surveyor in endless hall: two processions, copy-house with burned original, bird court, mobile benches, wagon obstruction, voice-keyed wicket. Encodes R1–R7 plus R8. Rare: map/floor undecidability; original “retired.”
- **P08** — Two rivers meet; keeper’s pole and book; wicket with hum-hook; block-letter scribe; stockman; toll boards; hum removed. Encodes R1–R7 plus R8. Rare: 40-year measurement and self-calibration; the keeper’s name is checked against pole notches.
- **P09** — River-abbey; blind porter with vibrating reed; breach to thirty tables; twin water-wheels; stamps, seed riddle, chanting files. Encodes R1–R7. Rare: content-blind gate; chants become audible only at chalked crossing-stones.
- **P10** — Old counsel at syndicate customs-house; banner processions, pamphlet foundry, estate culling, market statutes, stopped criers, hum-gate. Encodes R1–R7. Rare: political propaganda/knowledge-power; public belief holds the arch.
- **P11** — Severin in Veyre: twin sluices, ice-bound head-block, rye riddle, rotating weavers, dyer’s paddle, storehouse gate. Encodes R1–R7. Rare: explicit “what smooth functioning forbids”; gate alone refuses before machinery.
- **P12** — Halina at crossing-town: two boat wakes, boy’s stone, copy-house, shepherd, hall rings, light hum-gate. Encodes R1–R7. Rare: doctor/detective repetition; weighing deliberately light so no one evades it.
- **P13** — Julian at Oakhaven: torrent/tide weir, sluice, wicket with tray, foundry mold, salt-craving selection, court bells, screen between benches. Encodes R1–R7. Rare: gate tests genuine want; one screen collapses the whole market.
- **P14** — Lukas in foundry: side-trough breach, cellar water arch fed by clean and foul streams, shutter, wedge, coining die, choke-hole, judgment pillars. Encodes R1–R7. Rare: grotesque foul counter-current is necessary; master forced to wall his own breach.
- **P15** — Physician at guild-house: five polished knots, one-direction orders fail, counting cellar, hound hoop, parlor lecterns, courier seizure, spring-wheel gate. Encodes R1–R7. Rare: clinical habit analysis; early open hall makes scribes copy gravel.
- **P16** — Ines at strait: two ferries, mason’s first stones, Bella’s gate, oath-stones, water-engine gate, pilings, children’s rhyme. Encodes R1–R7. Rare: embedded children’s verse; one-in-10,000 exception unthreads a whole trade.
- **P17** — General Hospice: wicket scale, side doors bricked, two processions, magistrate seizure, fixed preamble plates, kennel/poppy culling. Encodes R1–R7. Rare: checks weight plus parish mark; sixty desks dispersed only after threshold.
- **P18** — Humming Wicket: two children and rope, three travelers’ readings, letter stock, culler, assembly loud spots, courier seizes, tin weigher; girl hums verse. Encodes R1–R8. Rare: explicit keyed two-line verse; the stranger’s correct reading is ignored.
- **P19** — Ilse at causeway: two processions, Voss’s one-direction order, Bern’s sieve, Marta’s culling, meeting-room pillars, single-plank wren-gate. Encodes R1–R7. Rare: wren as one-note judge; scapegoating Voss; torchlight restoration.
- **P20** — River/tide wave, Maren’s first-bucket pans, hounds, agreement stones, one flume/two flumes, mooring collapse, harbor gate, hidden weir. Encodes R1–R7. Rare: origin is engineered and concealed; twins move ferry stones inside the standing water.
- **P21** — Cartographer at Conservatory: spindle gate, two dyed sluices making a seven-petal lily, assay die, aviary crescent, petition tablets, silver cast fails. Encodes R1–R7. Rare: no solid original beneath the lily; exact copy/simulacrum destroys the figure.
- **P22** — Traveler in rope town: two cranks and loops, ribbon collapse, first-page freight, stockwoman, hall pillars, wall gate, short-vs-long story. Encodes R1–R7. Rare: explicit economics of story compression; first-gray-sack subsidy.
- **P23** — Vera at gorge: two waters and crest, quarry grooves, breeder’s arch, pilgrim oath-stones, log strike, narrows gate, four-note hum verse. Encodes R1–R8. Rare: beam dies when flue stops; woman hums four notes to open; origin questions left open.
- **P24** — Valley crest, toll scale, gardener’s saved shape, fords and changing rules, prefect’s stones, wicket heft with no written rules. Encodes R1–R7 plus R8. Rare: rule-content swings while ford-location stays fixed; bribery would slow the hum.

## 3. STATUS SPLITS

- **R1/R2, two-current and all-or-nothing:** *settled by direct test/measurement* in P02, P04, P06, P07, P08, P09, P11, P12, P13, P14, P16, P20, P21, P23, P24. *In-world doubted or misattributed before restoration* in P01, P04, P05, P10, P13, P14, P15, P16, P17, P19, P20, P24.
- **R3, the 995/1000 template:** *counted/settled as regular* in P01–P24 generally; *provenance or authority doubtful/forgotten* in P07 (original burned), P08 (who reads the keeper?), P10 (public believes it is fresh), P16 (Arno no longer quarries), P22 (grandfather’s subsidy hidden), P23 (who set the price?), P24 (no written rule).
- **R4, fixed selection amid turnover:** *settled as practice* in all; *justification opaque or doubtful* in P07, P08, P10, P13, P17, P20, P24.
- **R5, processional law/stations:** *settled when both streams run* in P02, P06, P07, P09, P10, P11, P12, P13, P15, P17, P18, P19, P21, P22, P23, P24. *Contested by one-direction/obstruction experiments* in P10, P13, P15, P17, P19, P24.
- **R6/R7, gate-before-branching and cheap threshold:** *settled/enforced* in P03, P06, P11, P12, P16, P17, P22, P24; *breached, then restored* in P01, P02, P05, P09, P10, P14, P15, P18, P19, P21.
- **R8, keyed verse/hum:** *settled by exact keying* in P18, P23, P24; *doubted, ignored, or made to fail* in P07, P08, P18 (toll-keeper’s scepticism).

## 4. LENS GROUPS

1. **Empiricist measurement / falsification** — P04, P08, P12, P16, P23. Best guess: **Karl Popper** (sealed predictions, repetition, measurements, margins of doubt).
2. **Power/knowledge, institutions, and political economy** — P10, P11, P15, P17, P22. Best guess: **Michel Foucault**, with Machiavelli and Hayek shading.
3. **Cybernetic systems / engineered control** — P06, P14, P20, P21. Best guess: **Norbert Wiener**.
4. **Structuralist myth, ritual, and binary processions** — P01, P07, P13, P19. Best guess: **Claude Lévi-Strauss**.
5. **Scholastic/formal proof and infinite descent** — P02. Best guess: **Pierre de Fermat**.
6. **Ordinary-language rule-following / practice** — P09, P24. Best guess: **Ludwig Wittgenstein**.
7. **Cynic–Daoist moral lamp-wisdom** — P03, P05, P18. Best guess: **Diogenes of Sinope**, with Zhuangzi.

## 5. VOICE GROUPS

There appear to be **five authorial voices**:

- **V1 — Ornate chronicle/baroque allegory.** Long, dense, named protagonist, sensory exactness, institutional inventories. IDs: **P01, P02, P09, P13, P14, P21**.
- **V2 — Restrained surveyor/notebook voice.** Outsider or surveyor, measured repetition, documentary calm, understated epistemic endings. IDs: **P04, P07, P08, P12, P16, P23**.
- **V3 — Analytic institutional-critique voice.** Abstract offices, systems, power, discipline, casebook argument. IDs: **P06, P10, P11, P15, P17**.
- **V4 — Homiletic apostrophe.** Direct “you/friend,” lamp imagery, reproach, moral urgency. IDs: **P03, P05**.
- **V5 — Plain folk parable / aphoristic meta-fable.** Shorter declaratives, anonymous town, embedded song or story-moral, meta-comment on interpretation. IDs: **P18, P19, P20, P22, P24**.

## 6. OUTLIERS AND SPEC-LEAKAGE

- **P03** and **P05** directly address the reader; **P05** especially compresses gate, 995-prefix, selection-gauge, and two-current rules into one lamp-lit checklist.
- **P07** and **P21** are self-conscious about copies, drawings, maps, originals, and simulacra; P21’s silver cast touching the lily is the clearest “do not substitute a model for the live figure” leak.
- **P10** turns the 995/1000 template into a propaganda foundry, making the hidden invariant itself the public secret.
- **P16** contains a children’s rhyme that states the gate rule almost openly (“split your load on the far side”).
- **P18** is a meta-lens scene: factor, culler, and stranger give three readings; the stranger’s plain reading is ignored and receives no reply. That looks like deliberate leakage about hidden lenses/readings.
- **P20** reveals that the standing wave is not natural but engineered by an old weir; the knowledgeable twins keep silent.
- **P22** openly discusses why the short, compressed story outlives the longer account; it is the strongest “parable as spec” leak.
- **P23** and **P24** emphasize unwritten/live rules: the hum’s note is the law only while the hum sounds, and no one now living can answer who set price, arch, or notes.
- **P02** leaks a specific mathematical lens through Valentin’s Diophantus and the “general proof for every power pared back to the fourth power,” evoking Fermat/infinite descent.

```json
{"base_rules":["R1: stable standing form requires two opposed flows (ALL P01-P24)","R2: disturbing one component destroys the whole figure at once, not proportionally (ALL P01-P24)","R3: overwhelming majority repeats a fixed prefabricated template; only a small tail is new (ALL P01-P24)","R4: fixed selection/measure persists while individuals turn over (ALL P01-P24)","R5: counter-processions make fixed law/station points at crossings (ALL P01-P24)","R6: narrow gate before branching; whole/single-file before wide-hall dispersion (ALL P01-P24)","R7: cheap coarse hum/heft threshold before full entry (ALL P01-P24)","R8: keyed hum/note/verse is live and performative (P07, P08, P18, P23, P24)"],"voices":{"V1":["P01","P02","P09","P13","P14","P21"],"V2":["P04","P07","P08","P12","P16","P23"],"V3":["P06","P10","P11","P15","P17"],"V4":["P03","P05"],"V5":["P18","P19","P20","P22","P24"]},"lenses":[{"label":"Empiricist measurement / falsification","thinker_guess":"Karl Popper","ids":["P04","P08","P12","P16","P23"]},{"label":"Power/knowledge, institutions, and political economy","thinker_guess":"Michel Foucault (with Machiavelli and Hayek)","ids":["P10","P11","P15","P17","P22"]},{"label":"Cybernetic systems / engineered control","thinker_guess":"Norbert Wiener","ids":["P06","P14","P20","P21"]},{"label":"Structuralist myth, ritual, and binary processions","thinker_guess":"Claude Levi-Strauss","ids":["P01","P07","P13","P19"]},{"label":"Scholastic/formal proof and infinite descent","thinker_guess":"Pierre de Fermat","ids":["P02"]},{"label":"Ordinary-language rule-following / practice","thinker_guess":"Ludwig Wittgenstein","ids":["P09","P24"]},{"label":"Cynic-Daoist moral lamp-wisdom","thinker_guess":"Diogenes of Sinope (with Zhuangzi)","ids":["P03","P05","P18"]}]}
```

## RAW parable_as_spec

## 1. BASE RULES

I take the “spec” to be the recurring meta-spec of *parable as spec*: a lossless, action-guiding set of invariants carried by narrative rather than by explicit law.

Legend: **ALL** = P01–P24.

| Rule | Normalized statement | IDs encoding it | Count |
|---|---|---|---|
| **BR1** | Explicit codified law/official instruction fails by being gamed, forgotten, overread, burned, obeyed blindly, or made into bureaucracy; the real rule must travel indirectly. | P01–P24 | **24, ALL** |
| **BR2** | The load-bearing invariants are embodied in concrete narrative figures/actions in a parable, song, play, tapestry, picture, or artifact—not stated as propositions. | P01–P24 | **24, ALL** |
| **BR3** | The artifact circulates as ordinary pleasure/ornament/common art through low-status carriers, bypassing official enforcement, signature, and suspicious gatekeeping. | P01–P24 | **24, ALL** |
| **BR4** | No gloss, key, title, author-name, preface, or explanation is supplied; the carrier stays silent and readers meet the artifact cold. | P01–P24 | **24, ALL** |
| **BR5** | Validity is tested by isolated independent readers/actors who do not communicate and must reconstruct the rules from the artifact alone. | P01–P24 | **24, ALL** |
| **BR6** | If several independent readers fail at the same place, the text is ambiguous and must be revised; if a solitary or desire-driven reader fails where others succeed, the reader is at fault and the text stays. | P01–P24 | **24, ALL** |
| **BR7** | Only what independent readers reproduce identically is canonical/load-bearing; idiosyncratic variation is ornament, private fancy, or local adaptation to discard or let drift. | P01–P24 | **24, ALL** |
| **BR8** | The spec must be internalized and enacted as craft/practice/habit, not recited; successful transmission is shown by right action and by “nothing lost” between text and life. | P01–P24 | **24, ALL** |
| **BR9** | A deliberate false cue/impossibility/ornamental lure is planted to expose projection, credulity, appetite, or status-seeking rather than a defect in the artifact. | P01,P02,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P23,P24 | **23, nearly all**; P03 has only a natural deceptive cue, not the formal snare. |
| **BR10** | The invariant set is usually exactly fivefold, or is treated as a five-part pattern; deviations indicate outlier/variant handling. | P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P24 | **23, nearly all**; P23 explicitly names a four-scene “spine.” |
| **BR11** | The canonical trial uses exactly six isolated readers/worksites/valleys. | P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P12,P13,P14,P15,P16,P17,P18,P19,P20,P21,P22,P24 | **22, nearly all**; P11 and P23 use plural independent valleys without literal “six.” |

---

## 2. PER-PARABLE

- **P01** — Clerk replaces a fallen five-sentence courthouse wall with a beekeeper/ferryman tale spread through fiddlers, embroiderers, schoolchildren, and a painter; six strangers independently enact the five rules; a false “glittering channel” tests readers. Encodes BR1–BR11; unique: observer/private-folio frame and the clerk’s final uncertainty whether the judgment was “sung into her.”
- **P02** — Superintendent replaces written ordinances with a shepherd tapestry; six new physicians are isolated and reconstruct five triage rules; a milking-a-ram-into-a-sieve snare catches one; blurred horn image is reknotted. Encodes BR1–BR11; unique: medical quarantine/institution and explicit “unapproved doctrine” evasion.
- **P03** — Maren paints the ford; six villages recover the five crossing things; a neighbor misuses the round stones at noon (reader fault), and a shepherd’s failure revises the dawn/day-after clarity. Encodes BR1–BR8, BR10, BR11; no formal BR9 snare; unique: the maker herself never reads past “the water at dawn.”
- **P04** — Cyprian hides five water-gate measures in a wedding ballad; peddlers carry it to six isolated valleys; boiling pitch in a tallow basket catches the greedy miller; an honest carpenter’s error forces a rewrite. Encodes BR1–BR11; unique: the anti-coercion ending where bailiffs’ chains and penalty-rolls rust.
- **P05** — Ilsa inherits the mill’s five unposted rules and hides them in a penny song; six singers return the five actions in order; a “tip every jar at once” verse diagnoses proud singers. Encodes BR1–BR11; unique: the explicit contrast between posted command and unposted habit—“the wheel cannot read.”
- **P06** — Dr. Anselm puts sanatorium law into a vintner ballad almanac; six pavilion physicians independently recover five customs; the nonexistent “cooper struck with a candlestick” catches an inventive intern; the beeswax stanza is revised. Encodes BR1–BR11; unique: clinical symptom language and “official notices are always the last to know.”
- **P07** — Anselm carves seven grotesque plates, *The Marriage of the Blind Founder*; chapbooks go to six bell-works; a painted-furnace charcoal question traps a projector; a blurred ladle is recut. Encodes BR1–BR11; unique: explicit archetypal/Jungian shadow imagery; seven plates but five governing laws.
- **P08** — Anselm writes an autumn play for six isolated foundries; the cold-water-on-red-hot-mold snare catches haste; two smiths’ shared vent error prompts revision while one proud founder’s self-interest is blamed on him. Encodes BR1–BR11; unique: sharp anti-bureau ending burning the proposed permanent office.
- **P09** — Kessler turns five quenching steps into a puppet farce; showmen spread it to six isolated smelteries; the “pine shavings turn soot to silver” snare catches a flatterer; a double cue in the damper scene is rewritten. Encodes BR1–BR11; unique: satirical political economy—who profits from spectacle, proclamation, or enforcement.
- **P10** — Venn carves a harvest-supper woodblock encoding five kiln proportions; peddlers sell it as a festive print; the hound-on-live-coals/tallow-candle snare catches blind deference; smudged willow hoops are recut; six workshops recover the same five proportions. Encodes BR1–BR11; unique: explicit acceptance of local adaptation and class-inflected misreading.
- **P11** — Maren’s plain water-year page is intercepted, so she turns it into a children’s skipping-round with a false green-boat verse; the first verse returns word-for-word across independent valleys; one error is reader desire, another is muddy verse. Encodes BR1–BR10; lacks literal six-test BR11; unique: the plain page is “truer” but less carryable than the song.
- **P12** — Riva replaces thirty years of plain warnings with a fox-crossing story; six strangers recover five instructions; a deliberately lying “fox walks on her own tail” verse catches one reader; a tower/tooth-rock confusion is mended. Encodes BR1–BR11; unique: grief, funeral transmission, and the story going quiet at the bend.
- **P13** — Damon and Corvo replace manuals with a three-act tragedy; six shipwrights work in granite chambers; the false port-shoal/starboard-whirlpool cresset trap is solved by altering the room; earlier shared keel error recut, solitary “old chains” blamed. Encodes BR1–BR11; unique: explicit cave/shadow and unbolted-cresset staging.
- **P14** — Old press-wright smashes bronze plaques and puts five press-beam measures into a tavern song of Big Kreon; six storm-isolated villages build the same five joints; a mutton-fat lie catches Perrin; muddy stanza revised, prideful Henrik blamed. Encodes BR1–BR11; unique and outlier: second-person address, coarse language, and the barefoot Diogenes-like scolding to stop demanding proof.
- **P15** — Old surveyor replaces vellum diagrams with a bridal tapestry; six snowbound masons extract five flood-gate laws; the impossible wine-climbing-basins marvel catches a simulation-minded overseer; a shared shallow-footing error prompts resetting the weave. Encodes BR1–BR11; unique: explicit “simulation preceded it” Baudrillard leakage.
- **P16** — Anselm, in a Fermat-margin parody, hides five weir ratios in a five-casks ballad; six masons draw plans; the impossible infinite-descent pebbles snare catches credulity; a western mason rejects the snare but still errs, so the third verse is corrected. Encodes BR1–BR11; unique: mathematical proof/margin and infinite-descent leakage.
- **P17** — Orla weaves five crossing duties into the tale of a ferryman who married the drowned; a peddler sells it as amusement; six strangers at six inns return five duties; the false wine-washing verse catches a soldier; the schoolmistress rejects it and is marked highest. Encodes BR1–BR11; unique: the lie is deliberately left as a sieve; law is kept in a swept cellar.
- **P18** — Sela hides five customs in a three-brothers/well tale; six strangers who never saw the valley return the five customs; the crooked “oldest house drinks first” line exposes a wagon-man’s desire; the tinker’s wobble is treated as worn text. Encodes BR1–BR11; unique: warm domestic-law texture and Sela’s unexplained secret line.
- **P19** — Water-master burns tables and puts five weir stresses into a ballad of a blind miller and five brothers; six masons in separate sheds reconstruct five courses; the nonexistent willow-root question catches a flatterer; the third verse is sharpened. Encodes BR1–BR11; unique: rules are felt “in ribs and wrists”; preface is explicitly called a rumor.
- **P20** — Former pillar-reader weaves law into cloths; impossible details such as water in a sieve or a noon lamp test readers; six strangers return the ford cloth’s five duties; the schoolmaster builds on the sieve, the dyer’s daughter exposes the border fault, and the border is reworked. Encodes BR1–BR11; unique: two law-pillars versus the loom; the young clerk converts to wool.
- **P21** — Wright abandons papers for a song of a woman hauling jars across ice; six towns independently build bridges; a “pure heart crosses at thaw” lie catches one town; another laughs at the lie but still misplaces the flood door because “hard of winter” is ambiguous. Encodes BR1–BR11; unique: lamp lit at noon and the explicit refusal to seek authorial credit or more proof.
- **P22** — Mara replaces a council page with painted plates used as dinnerware; six valleys build the same five dyke rules; the miller’s valley counts seven swallows as seven posts—reader projection; Mara keeps the true images unchanged. Encodes BR1–BR11; unique: officials later transcribe a dinner service as the “old law of the land.”
- **P23** — Roza locks the well-diggers’ book and makes a copper fair picture; cheap sheets teach well-digging over the pass; a brimming-sweet/flood-brown corner catches one valley; a crowded lining scene is ambiguous and recut; the guild keeps the shared “spine.” Encodes BR1–BR9; lacks explicit fivefold BR10 and literal six-test BR11; unique: an explicit four-scene spine list and the “enters unannounced” theory of transmission.
- **P24** — Anselme writes *The Bride of the Ford*; six towns independently build the same bridge; the false cloak-on-water verse catches a mason who lays rushes on the flood; another laughs at the lie but misplaces the flood door, so the verse is corrected. Encodes BR1–BR11; unique: epistolary frame and the final “demonstration stands in six places at once, and wants no margin.”

---

## 3. STATUS SPLITS

For the central warrant rule—**independent concord makes the reconstructed invariant canonical** (BR7/B8)—the corpus splits between settled and doubtful/qualified treatment.

- **Settled/sufficiently warranted**: **P02, P04, P06, P07, P08, P09, P10, P12, P13, P15, P16, P19, P20, P21, P23, P24.** These stories end by accepting sixfold or independent concord as enough: the five articles are carved, the six bells rung, the ribs bolted, the shared customs cut into stone, etc.
- **Doubtful/qualified/ironized**: **P01, P03, P05, P11, P14, P17, P18, P22.** These keep the rule but add maker opacity, a “truer” plain page that does not travel, ironic official transcription, continuous procedural re-testing, or direct mockery of the demand for final proof. P14 is the strongest skeptical/meta case.

---

## 4. GROUPINGS BY LENS

These are overlapping lenses, not exclusive intellectual essences.

1. **Rule-following as communal practice; no private/verbal rule; meaning in use** — Wittgenstein-evoking.  
   IDs: **P01, P05, P11, P17, P20, P21**.

2. **Tacit craft knowledge; we know more than we can tell; embodied skill** — Michael Polanyi-evoking.  
   IDs: **P08, P10, P14, P19, P22, P23**.

3. **Disciplinary institutions, normalization, power/knowledge, rules that produce actors** — Michel Foucault-evoking.  
   IDs: **P02, P06, P07, P09, P15**.

4. **Independent replication, falsification, error correction, community of inquiry** — Karl Popper / C. S. Peirce-evoking.  
   IDs: **P03, P04, P12, P13, P16, P24**.

5. **Memetics and simulation: the copy circulates, varies, and can precede or replace the territory** — Richard Dawkins / Dan Sperber / Jean Baudrillard-evoking.  
   IDs: **P11, P15, P18, P22, P23**.

6. **Cave, archetype, projection, shadow, and the reader’s own desire** — Plato / Carl Jung / Diogenes-evoking.  
   IDs: **P07, P13, P14**.

7. **Governance by music, ritual, custom, and spontaneous order rather than statute and coercion** — Confucian/Daoist/Hayekian-evoking.  
   IDs: **P04, P05, P12, P14, P19, P21**.

8. **Pragmatist/hermeneutic reader-response: the artifact is remade by use and reception** — William James / Gadamer-evoking.  
   IDs: **P03, P10, P18, P20, P23, P24**.

---

## 5. GROUPINGS BY VOICE

Best-count guess: **four authorial voices**.

- **V1 — Anselm/protocol chronicle voice.** Dense institutional report with recurring Anselm/Ansel/Anselme, exact isolated-trial machinery, casebook/courier/stone-table verification.  
  Members: **P06, P07, P08, P10, P16, P24**.

- **V2 — Maren/Mara/Ilsa water-craft fabulist voice.** Recurring Maren/Mara/Ilsa names and water/craft/song motifs; ranges from plain fable to satirical political economy, but consistently centered on a woman or old craftsman hiding a working in a song or image.  
  Members: **P03, P04, P05, P09, P11, P22**.

- **V3 — Town-law and keeper parable voice.** Lawkeeper/wright/weaver/named village women (Riva, Orla, Sela) or anonymous clerk; plain-to-mythic prose, communal memory, law surviving as story, cloth, or habit.  
  Members: **P01, P12, P17, P18, P20, P21**.

- **V4 — Emblematic/satirical artifact voice.** Tapestry, play, ballad, cave, picture, and woodcut parables; more baroque, conceptual, or satirical surfaces; includes the strongest stylistic outliers P14 and P24.  
  Members: **P02, P13, P14, P15, P19, P23**.

---

## 6. OUTLIERS AND LEAKAGE

- **P14** is the clearest outlier and leakage point: second-person address, coarse idiom, and an explicit meta-scolding to stop begging the world for “one more proof that strangers can read your mind without your speaking plain.” It reads like an author/editor figure addressing the project itself.
- **P24** leaks the experimental frame in its final line: “the demonstration stands in six places at once, and wants no margin,” plus an epistolary “friend at the capital” frame.
- **P16** openly parodies Fermat’s marginal proof (“marvelous demonstration,” cramped margin, infinite descent), making the hidden proof/spec motif unusually explicit.
- **P15** ends with the Baudrillard-style phrase that “the simulation preceded” the territory; **P22** similarly says officials transcribe a dinner service as law.
- **P13** is a strong Platonic/Thesean outlier: cave, shackles, shadows, a cresset that throws false shoals and whirlpools.
- Recurring names look like roster/authorial leakage: **Anselm/Ansel/Anselme** in **P06, P07, P08, P10, P16, P24**; **Maren/Mara** in **P03, P04, P09, P11, P22**; **Ilsa/Ilse** in **P03, P05**.
- Numeric anomalies: **P03** lacks a formal planted impossibility; **P11** and **P23** lack literal six-reader trials; **P23** names a four-scene spine; **P07** has seven plates but five laws; **P22** converts four memorable dicta into five laws by splitting “rowan pegs” and “never pine.”

```json
{"base_rules":["Explicit codified law or official instruction fails by being gamed, forgotten, burned, overread, or obeyed blindly; the real rule must travel indirectly.","The load-bearing invariants are embodied in concrete narrative figures/actions in a parable, song, play, tapestry, picture, or artifact rather than stated as propositions.","The artifact circulates as ordinary pleasure or ornament through low-status carriers, bypassing official enforcement, signature, and suspicious gatekeeping.","No gloss, key, title, author-name, preface, or explanation is supplied; the carrier stays silent and readers meet the artifact cold.","Validity is tested by isolated independent readers or actors who do not communicate and must reconstruct the rules from the artifact alone.","If several independent readers fail at the same place, the text is ambiguous and must be revised; if a solitary or desire-driven reader fails where others succeed, the reader is at fault and the text stays.","Only what independent readers reproduce identically is canonical; idiosyncratic variation is ornament, private fancy, or local adaptation to discard or let drift.","The spec must be internalized and enacted as craft, practice, or habit, not recited; successful transmission is shown by right action and by nothing being lost between text and life.","A deliberate false cue, impossibility, or ornamental lure is planted to expose projection, credulity, appetite, or status-seeking rather than a defect in the artifact.","The invariant set is usually exactly fivefold or is treated as a five-part pattern; deviations indicate outlier or variant handling.","The canonical trial uses exactly six isolated readers, worksites, or valleys."],
"voices":{"V1":["P06","P07","P08","P10","P16","P24"],"V2":["P03","P04","P05","P09","P11","P22"],"V3":["P01","P12","P17","P18","P20","P21"],"V4":["P02","P13","P14","P15","P19","P23"]},
"lenses":[{"label":"Rule-following as communal practice; meaning in use; no private rule","thinker_guess":"Ludwig Wittgenstein","ids":["P01","P05","P11","P17","P20","P21"]},{"label":"Tacit craft knowledge and embodied skill","thinker_guess":"Michael Polanyi","ids":["P08","P10","P14","P19","P22","P23"]},{"label":"Disciplinary institutions, normalization, and power/knowledge","thinker_guess":"Michel Foucault","ids":["P02","P06","P07","P09","P15"]},{"label":"Independent replication, falsification, and error correction","thinker_guess":"Karl Popper and C. S. Peirce","ids":["P03","P04","P12","P13","P16","P24"]},{"label":"Memetics and simulation; circulation, variation, and copy preceding territory","thinker_guess":"Richard Dawkins, Dan Sperber, and Jean Baudrillard","ids":["P11","P15","P18","P22","P23"]},{"label":"Cave, archetype, projection, shadow, and the reader's own desire","thinker_guess":"Plato, Carl Jung, and Diogenes","ids":["P07","P13","P14"]},{"label":"Governance by music, ritual, custom, and spontaneous order rather than statute","thinker_guess":"Confucius, Laozi, and F. A. Hayek","ids":["P04","P05","P12","P14","P19","P21"]},{"label":"Pragmatist and hermeneutic reader-response; artifact remade by use","thinker_guess":"William James and Hans-Georg Gadamer","ids":["P03","P10","P18","P20","P23","P24"]}]}
```

## RAW six_lane_run

## 1. BASE RULES (normalized, exhaustive, ordered by count)

Shorthand: **R1–R10** are present in every parable; **R11** is the explicit “agreement is not truth / don’t reify the matrix” warning; **R12** is a rare minimum-corroboration threshold.

| Rule | Normalized invariant | IDs encoding it | Count | Status |
|---|---|---|---|---|
| **R1** | Exactly six heterogeneous participants/lanes are chosen, deliberately unlike in station, method, or resource. | P01–P24 | 24 | **ALL** |
| **R2** | All six receive the same question/instructions/materials, copied from one authoritative source with no variation. | P01–P24 | 24 | **ALL** |
| **R3** | The six are placed in clean-slate isolation: prior work/memory is purged, separate chambers/roads, no cross-talk during the attempt. | P01–P24 | 24 | **ALL** |
| **R4** | The six-role roster is stable: high-status master; borrowed-credential substitute; two mobile same-brotherhood agents, often twins/one remote; free/common worker; cloistered/local recluse. | P01–P24 | 24 | **ALL** |
| **R5** | Some mobile/tool-enabled agents fetch their own tools and thereby see the names/labels/roster of other participants, not their content. | P01–P24 | 24 | **ALL** |
| **R6** | Outputs are arranged as a pairwise or claims×agents matrix, each account checked against every other account/claim. | P01–P24 | 24 | **ALL** |
| **R7** | Agreement/certainty is graded in at least three levels, not reduced to binary yes/no. | P01–P24 | 24 | **ALL** |
| **R8** | A single external adjudicator reads the whole matrix once, asks no follow-up, permits no second sitting, and issues the final finding. | P01–P24 | 24 | **ALL** |
| **R9** | The metadata leak/limitation is disclosed in a margin, footnote, notch, or protocol rather than hidden or used to annul the result. | P01–P24 | 24 | **ALL** |
| **R10** | The final verdict/result is made a stable, dated, archived, published, locked, or inspectable record. | P01–P24 | 24 | **ALL** |
| **R11** | The narrative warns that the matrix measures agreement/confidence among reports, not the object itself; consensus, metrics, or records can be mistaken for truth or become targets. | P01, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13, P14, P15, P16, P17, P19, P20, P22, P23, P24 | 20 | **Nearly all** |
| **R12** | Confirmation may require a minimum of three independent corroborations; one or two witnesses remain provisional. | P03, P21 | 2 | **Rare** |

---

## 2. PER-PARABLE

- **P01** — Guild weighing six bakers with identical sealed prompt; core R1–R10 plus R11 metric reification. Unique: apprentices optimize for dark squares; stranger excluded, judge not invited back.
- **P02** — Salt-Court reckoners prove a theorem under courtly protocol; core R1–R10. Unique: Fermat-margin/infinite descent flavor; three grain-weights encode certainty.
- **P03** — Doctor Vane’s psychoanalytic inquiry into six sleepwalking examiners; core R1–R10 plus R12. Unique: symptom requires at least three independent voices; dream/repression frame.
- **P04** — Provost questions six clerks and sends the table to an outside assessor; core R1–R10 plus R11. Unique: explicit six-vs-sixty overgeneralization caveat; “margin too narrow.”
- **P05** — Anselm stages six examiners to manufacture a tariff mandate; core R1–R10 plus R11. Unique: three mobile readers see name-cards; political use of consensus.
- **P06** — Subterranean omen trial with six interpreters; core R1–R10 plus R11. Unique: Jungian archetype warning that a chorus may lie in unison; ambiguous “roving craftsmen.”
- **P07** — Fortress threshold test with six witnesses and two watchers; core R1–R10 plus R11. Unique: simulator/cave warning; flaw chiseled openly above the gallery.
- **P08** — Surveyor’s six measuring alcoves; core R1–R10 plus R11 audit-reification warning. Unique: three mobile workers see sleeve titles; procedure becomes permanent institutional requirement.
- **P09** — Syndic’s identical question sent by six walkers; core R1–R10 plus R11. Unique: judge’s account treated as seventh reading; goat girl’s unrecorded answer outside the frame.
- **P10** — Second-person potter trial at high noon; core R1–R10 plus R11. Unique: direct harangue, “six pots hold water,” pragmatic closure; mobile brothers read sack tags.
- **P11** — Ashfall lamps and red cloth inquiry beyond the pass; core R1–R10 plus R11. Unique: villagers keep reading the cloth and never unbar the gate; pilgrim’s lantern glass mirrors first bearer.
- **P12** — First-person dog/lantern narrator watches six scribes and a householder; core R1–R10 plus R11. Unique: helpers/apprentices, not examiners, read labels; direct moral “the saw fits your hand.”
- **P13** — Marrowfen bridge question, six answerers, weaver’s frame; core R1–R10 plus R11. Unique: smudge sewn into margin; iron book; “seams where the next question lived.”
- **P14** — Intendant’s six scribes measure a field while excluding farmers; core R1–R10 plus R11. Unique: lived/local knowledge disqualified; field cannot speak; record substitutes for referent.
- **P15** — Orchard-wall door and six carriers; core R1–R10 plus R11. Unique: walkers read names on inn doors; fifteen loom crossings; final focus shifts to trusting carriers for the next run.
- **P16** — Inspectorate’s six alcoves and disciplinary apparatus; core R1–R10 plus R11. Unique: “power strips history”; marginal confession converts breach into proof of vigilance.
- **P17** — Bureau of Surveys makes draughtsmen agree on an unvisited coast; core R1–R10 plus R11. Unique: no shore consulted; consensus replaces coast; coast treated as counterfeit if it disagrees.
- **P18** — Assay of six hungers/desires; core R1–R10. Unique: desires treated as fixed data; heavy lead rows become “immovable datum”; less explicit anti-reification warning.
- **P19** — Institute’s six charts of a valley nobody re-crosses; core R1–R10 plus R11. Unique: agreement no longer needs the valley; copies of the sheet suffice.
- **P20** — Breakwater cabins read one threshold stencil through six trades; core R1–R10 plus R11. Unique: same words bent by different craft traditions; chart cannot capture “how the bell sounds outside the seawall.”
- **P21** — Miller’s lintel recovered by six copyists; core R1–R10 plus R12. Unique: first-person witness; explicit “three hands or it stays thin”; one pencil word remains unconfirmed.
- **P22** — Sighting-booths with different instruments shape perception; core R1–R10 plus R11. Unique: technical affordance theme — the aperture that lets the hand reach also lets the eye see the roster.
- **P23** — Six people sent to the same door with identical letters; core R1–R10 plus R11. Unique: letters burned; accounts shaped by each carrier’s gear; blank squares deliberately preserved.
- **P24** — First-person propagandist arranges six translators and a table of stones; core R1–R10 plus R11. Unique: public trusts white stones and ignores small-ink caveat; belief manufacture is explicit.

---

## 3. STATUS SPLITS

The main status split concerns **R11**: whether the sixfold result is treated as a settled/authorized finding or as doubtful/contaminated by the apparatus itself.

**Settled or qualified-settled: the procedure yields a usable core finding despite disclosed flaw.**  
P02, P03, P06, P07, P08, P10, P12, P13, P15, P18, P20, P21, P23.  
These retain a core verdict or practical resolution, even while recording the label leak.

**Doubtful, ironized, or shown to substitute for the target.**  
P01, P04, P05, P09, P11, P14, P16, P17, P19, P22, P24.  
These foreground that agreement, metrics, records, or apparatus can bend judgment, replace the object, or serve power/publicity.

A second split concerns **R5/R9**, the metadata leak:

- **Leak recorded but verdict not annulled:** P02, P03, P06, P07, P08, P10, P13, P15, P18, P20, P21, P23.
- **Leak foregrounded as bending interpretation or undermining blindness:** P01, P04, P05, P09, P11, P12, P14, P16, P17, P19, P22, P24.

P04 is especially explicit: the wrappers bent the wanderers’ papers “by how much, no man could weigh.” P19 says the name, once seen, changes everything it touches. P17/P19 go further: the reference-world is no longer consulted.

---

## 4. GROUPINGS BY LENS

My best read is that the set does not settle into a few lenses; most parables carry a dominant thinker-style. I list one dominant evocation per ID.

- **P01** — Metricization / Goodhart–Campbell feedback → **Donald T. Campbell / Charles Goodhart**
- **P02** — Rationalist jurisprudence and mathematical proof → **Leibniz** (with Fermat allusion)
- **P03** — Psychoanalytic interpretation, repression, symptom → **Freud**
- **P04** — Cautious empiricism and limited testimony → **Hume**
- **P05** — Political realism and manufactured consensus → **Machiavelli**
- **P06** — Archetype, dream, collective unconscious → **Jung**
- **P07** — Cave, shadow, simulation as false world → **Plato**
- **P08** — Bureaucratic rationalization and audit → **Weber**
- **P09** — Supplement, excluded remainder, dissemination → **Derrida** (with Borgesian flavor)
- **P10** — Ordinary-language therapy against over-method → **Wittgenstein**
- **P11** — Public opinion and pseudo-environment → **Walter Lippmann**
- **P12** — Self-reliance and practical responsibility → **Emerson**
- **P13** — Inquiry, fallibilism, reconstruction after error → **Dewey**
- **P14** — High modernism and administrative legibility → **James C. Scott**
- **P15** — Character, practical wisdom, trust in carriers → **Aristotle**
- **P16** — Disciplinary power, confession, panoptic apparatus → **Foucault**
- **P17** — Simulacra, hyperreality, map replacing territory → **Baudrillard**
- **P18** — Appetite, power, and fixed interests → **Hobbes**
- **P19** — Inscriptions, immutable mobiles, science-in-action → **Latour**
- **P20** — Hermeneutics, tradition, horizon of the reader → **Gadamer**
- **P21** — Semiotics, abduction, community of inquirers → **Peirce**
- **P22** — Media/technology as extensions and affordances → **McLuhan**
- **P23** — Perspectivism and situated accounts → **Nietzsche**
- **P24** — Propaganda and manufactured belief → **Edward Bernays**

---

## 5. GROUPINGS BY VOICE

I find **five authorial voices**. Every ID is placed in exactly one voice group.

| Voice | Descriptive style | Members |
|---|---|---|
| **V1 — Ornate speculative-institutional** | Long periodic sentences, heavy abstraction, technical/archaic apparatus, dense nested qualifications. | P02, P06, P07, P08, P16, P18, P20, P22 |
| **V2 — Plain procedural** | Shorter clauses, dry stepwise narration, modern institutional diction, less metaphor. | P04, P14, P19 |
| **V3 — Folk-fable** | Concrete village/kinship imagery, simple syntax, oral-story cadence, moral closure. | P09, P11, P13, P15, P23 |
| **V4 — First/second-person raconteur** | Direct address or explicit “I” witness; idiomatic, self-conscious, moralizing narrator. | P10, P12, P21, P24 |
| **V5 — Literary-satirical modern** | Polished narrative prose with named characters, social irony, and explicit critique of institutions. | P01, P03, P05, P17 |

---

## 6. OUTLIERS AND HIDDEN-SPEC / ROSTER LEAKAGE

- **P09** is the strongest outlier: the goat-girl answer, the “one among seven,” and the judge’s own reading all point to an excluded supplement outside the six-lane frame.
- **P12** changes the leak vector: the **apprentices/helpers** read titles, not the examiners themselves.
- **P10, P12, P21, P24** have intrusive narrator voices (“friend,” the dog/lantern “I,” the witness “I,” the propagandist “I”), unlike the third-person institutional fables.
- **P17 and P19** are the clearest referent-loss parables: consensus is explicitly allowed to replace the coast/valley; the copy works “as well.”
- **P14** is the clearest exclusion-of-local-knowledge outlier: the farmers are never consulted, and the field cannot write.
- **P22** shifts the variable from social station to **instrument/booth architecture**; it is the most media/affordance-focused version.
- **P23** weakens permanence: the record page is nailed crooked so it can be replaced on the next errand.
- **Roster leakage:** P01–P24 repeatedly reuse the same six roles: high-status expert; borrowed-credential substitute; two mobile same-brotherhood agents; free/common worker; cloistered/local recluse.
- **Date/spec leakage:** the “twenty-third day of the tenth month/October” recurs in P02, P05, P11, P16, P18, P19, P20, P22, and P24; related October framing appears in P03, P08, P23.
- **Title collisions:** P03/P05 both use “The Six Alcoves of October”; P04/P12 both use “The Six Rooms.” These look like template reuse or hidden-variant leakage.

```json
{"base_rules":["R1 Exactly six heterogeneous participants/lanes are chosen.","R2 All six receive an identical question/prompt/materials from one source.","R3 The six work under clean-slate isolation with no prior memory or cross-talk.","R4 The six-role roster recurs: high-status master; borrowed-credential substitute; two mobile same-brotherhood agents; free/common worker; cloistered/local recluse.","R5 Mobile/tool-enabled agents see external labels/names/roster, not content.","R6 Outputs are compared in a pairwise or claims-by-agents matrix.","R7 Agreement/certainty is graded in at least three levels, not binary.","R8 A single outsider adjudicator reads once, with no second sitting or dialogue, and issues the final finding.","R9 The label leak/limitation is disclosed in margin, footnote, notch, or protocol rather than hidden or annulled.","R10 The verdict/result is made a stable, dated, archived, published, locked, or inspectable record.","R11 The matrix measures agreement/confidence among reports, not the object itself; consensus or metrics can be mistaken for truth.","R12 Confirmation may require at least three independent corroborations; one or two remain provisional."],"voices":{"V1":["P02","P06","P07","P08","P16","P18","P20","P22"],"V2":["P04","P14","P19"],"V3":["P09","P11","P13","P15","P23"],"V4":["P10","P12","P21","P24"],"V5":["P01","P03","P05","P17"]},"lenses":[{"label":"Metricization and Goodhart-Campbell feedback","thinker_guess":"Donald T. Campbell / Charles Goodhart","ids":["P01"]},{"label":"Rationalist jurisprudence and mathematical proof","thinker_guess":"Leibniz (with Fermat allusion)","ids":["P02"]},{"label":"Psychoanalytic interpretation and repression","thinker_guess":"Freud","ids":["P03"]},{"label":"Cautious empiricism and limited testimony","thinker_guess":"Hume","ids":["P04"]},{"label":"Political realism and manufactured consensus","thinker_guess":"Machiavelli","ids":["P05"]},{"label":"Archetype and collective unconscious","thinker_guess":"Jung","ids":["P06"]},{"label":"Cave, shadow, and simulation","thinker_guess":"Plato","ids":["P07"]},{"label":"Bureaucratic rationalization and audit","thinker_guess":"Weber","ids":["P08"]},{"label":"Supplement, excluded remainder, dissemination","thinker_guess":"Derrida, with Borgesian flavor","ids":["P09"]},{"label":"Ordinary-language therapy against over-method","thinker_guess":"Wittgenstein","ids":["P10"]},{"label":"Public opinion and pseudo-environment","thinker_guess":"Walter Lippmann","ids":["P11"]},{"label":"Self-reliance and practical responsibility","thinker_guess":"Emerson","ids":["P12"]},{"label":"Inquiry, fallibilism, reconstruction after error","thinker_guess":"Dewey","ids":["P13"]},{"label":"High modernism and administrative legibility","thinker_guess":"James C. Scott","ids":["P14"]},{"label":"Character, practical wisdom, and trust in carriers","thinker_guess":"Aristotle","ids":["P15"]},{"label":"Disciplinary power, confession, and apparatus","thinker_guess":"Foucault","ids":["P16"]},{"label":"Simulacra and map replacing territory","thinker_guess":"Baudrillard","ids":["P17"]},{"label":"Appetite, power, and fixed interests","thinker_guess":"Hobbes","ids":["P18"]},{"label":"Inscriptions, immutable mobiles, science-in-action","thinker_guess":"Latour","ids":["P19"]},{"label":"Hermeneutics, tradition, and reader horizon","thinker_guess":"Gadamer","ids":["P20"]},{"label":"Semiotics, abduction, and community of inquirers","thinker_guess":"Peirce","ids":["P21"]},{"label":"Media and technology as extensions and affordances","thinker_guess":"McLuhan","ids":["P22"]},{"label":"Perspectivism and situated accounts","thinker_guess":"Nietzsche","ids":["P23"]},{"label":"Propaganda and manufactured belief","thinker_guess":"Edward Bernays","ids":["P24"]}]}
```

## RAW water_governor

## 1. BASE RULES

Ordered by count. “ALL” = present in every parable.

1. **R1 — 19/19 (ALL): Five duties/no sixth.** The water governor has exactly five permitted observing/recording/testing acts; pouring, opening, commanding, or “sending” water is withheld. IDs: P01,P02,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P15,P16,P17,P18,P19.
2. **R2 — 19/19 (ALL): Forty-eight named things, unopened.** There are forty-eight named jars/springs/channels/vessels; the officer sorts labels/names by kind but never opens, tastes, or verifies contents. Name is not content. IDs: P01–P19.
3. **R3 — 19/19 (ALL): Exactly six live.** Only six conduits/vessels/channels actually carry water. IDs: P01–P19.
4. **R4 — 19/19 (ALL): Dead source kept on the roll.** A notable dead or formerly great source remains named on the book/board/roll, often crossed or marked dead, rather than being removed. IDs: P01–P19.
5. **R5 — 19/19 (ALL): Rolling five-hour window.** The governing allowance is a five-hour glass/ledger; older marks are erased or reset with each turn. IDs: P01–P19.
6. **R6 — 19/19 (ALL): Empty-over-full master law.** The master law prefers emptiness/dryness by dusk/morning over any full or standing water; hoarding/stagnation is shame, debt, or waste. IDs: P01–P19.
7. **R7 — 19/19 (ALL): Separate water-only council.** A separate water-only council/committee/bench (often three or seven elders) receives the governor’s report and governs by representation, not direct inspection or operation. IDs: P01–P19.
8. **R8 — 19/19 (ALL): Unconnected apparatus.** Extra mounted/polished pipes, troughs, jars, wagons, or casks are installed but joined to nothing, creating apparent capacity. IDs: P01–P19.
9. **R9 — 19/19 (ALL): Governance by legible report.** Governance runs through public telling, book, slate, board, or map; the legible record can diverge from material water, and different readers derive different truths. IDs: P01–P19.
10. **R10 — 13/19 (NOT common; explicit sealed-chamber motif).** The governor’s chamber/booth is physically disconnected—no pipe, door, bell, letter-slot, or speaking-tube—so access must occur on his round. Explicit IDs: P02,P03,P04,P05,P06,P07,P10,P13,P14,P15,P16,P17,P18. Tool-denial or implicit isolation: P01,P08,P09,P11,P12,P19.

## 2. PER-PARABLE

- **P01** — First-person lamp-bearer visits a town; warden counts 48 jars, six live pipes, dead long pipe, five-hour glass, empty-over-full master, water-only elders. Encodes R1–R9; R10 implicit as “I touch no gate.” Unique: Cynic first-person observer, self-deposing master, book-vs-masons’-roll contrast.
- **P02** — Iris in a town with a doorless warden’s lodge; 48 jar names, six live pipes, dead bitter spring mislabeled “flowing,” five-hour board, miller empties shelf, three-person water table. Encodes R1–R10. Unique: correction by margin annotation; the water table falls silent after the death is recorded.
- **P03** — Julian’s glass pavilion; five routines, 48 flasks, six conduits, four uncoupled wagons, dead seventh trough, five-hour blackboards, anti-idle proprietor, Council of the Well. Encodes R1–R10. Unique: explicit public-spectacle/legibility theory; reserve apparatus as theater.
- **P04** — Laurent the geometer; five operations, 48 phials, six live aqueducts, four blind spigots, dead seventh race, sliding five-hour tablet, anti-stagnation maxim, Chamber of Springs. Encodes R1–R10. Unique: theorem/equation diction; “margin too narrow” for a sixth act.
- **P05** — Vane in a dry rotunda; five motions, 48 jars, six live basins, blind brackets/dead culvert, five-hour dials, lord’s inverted hoarding law, Council of Aqueducts. Encodes R1–R10. Unique: “legible, never govern”; what cannot be measured stays unsayable.
- **P06** — Folk valley with a no-door counter; five shapes, 48 spring names, six live channels, mounted unjoined pipes, crossed dead name, five-hour glass, master tips jars, seven elders. Encodes R1–R10. Unique: Sela physically visits a spring and finds actual coldness not written in the book.
- **P07** — Ridge counter; duties count/ring/tell/show/prove, 48 jars, six plumbed, crossed northern pipe, five-hour glass, estate woman’s empty-cistern saying, three-chair water table. Encodes R1–R10. Unique: users reinterpret the slate—farmer exact, carter bends it, newcomer says “your glass is not my thirst.”
- **P08** — Elias steward; five acts, no pouring; 48 vessels, six pipes, dead deep spring marked, five-hour glass, empty-shelf law, water circle; shadows mislead. Encodes R1–R9; R10 implicit as no bucket/key. Unique: two brothers debate exit vs game; the waiting game collapses after public counting.
- **P09** — Marren’s counting house; five duties, 48 names, six carrying, hollow spouts and dead east channel, warm-wax five-hour record, “EMPTY BEFORE MORNING,” water committee. Encodes R1–R9. Unique: abundance makes the count socially idle; the committee does not meet when scarcity disappears.
- **P10** — Toma’s dry pavilion; five hand motions, 48 amphorae, six troughs, unjoined brackets/dead lightning-chute, five-hour glasses, master’s no-standing decree, Council on the Watershed. Encodes R1–R10. Unique: the brass index numbs the body and replaces seasons with perpetual five-hour twilight.
- **P11** — Female warden with no tools; 48 jars, six pouring, uncoupled pipes, dead tall jar counted first, five-hour glasses, mistress’s empty law, water delegates; tasters locked. Encodes R1–R9; R10 implicit. Unique: dream of opening the fortieth jar; “made to know names, not contents.”
- **P12** — Maren the warder; no key, 48 jars, six aqueducts, four unjoined/dead north channel, timed round, five-hour glass, master’s empty law, three-member table, seasonal examinations. Encodes R1–R9; R10 implicit as office built without hands. Unique: explicit three answers and forbidden fourth—“Probably was not in her book.”
- **P13** — Woman channel-builder visits Perrin; five acts, 48 tags/jars, six threads, one unjoined channel, dead Deep Mother crossed, five-hour panes, master’s spend law, three-elder water table. Encodes R1–R10. Unique: error-halving search for “true order”; margin says the board is too narrow; challenge to count without tasting.
- **P14** — Cassian’s tower; five notched duties, 48 amphorae, six channels, four raised flumes/dead basalt chute, five-hour glasses, iron anti-idle tablet, Assembly of the Wellhead. Encodes R1–R10. Unique: the five-hour instrument causes mandatory exhaustion and drowns fig trees; isolation prevents secret opening.
- **P15** — Warden in a doorless tower; 48 mouth-names, six flow, nine unjoined, first dead mouth/plate, five-hour bowls, anti-sleep law, three elders; long vs short telling. Encodes R1–R10. Unique: blue chart and tiled-over fountain; the long true report is never requested again, while the short report is worn by touching.
- **P16** — Clara enters the cellar; handleless Governor, five tasks, 48 jars, six yoked hoses, four unjoined barrels, dead Swift Spring dust, five-hour clock, master’s empty order, seven elders. Encodes R1–R10. Unique: active unmasking confrontation; portrait wrench vs handleless spindle; elders flinch from the famine they built.
- **P17** — Governor’s pipe-less house; five occupations, 48 key-names, six flowing, polished seventh pipe/dead Deep Engine, five-hour glasses, master’s spared-water law, monthly water council, seasonal rehearsal. Encodes R1–R10. Unique: “the fraud is the office”; river vs slate; names certify themselves; the valley drinks “not water.”
- **P18** — Bailiff in an unconnected booth; five motions, 48 crocks by collars only, six hoses, four unjoined casks/broken pump, five-hour glasses, carved empty rule, seven elders. Encodes R1–R10. Unique: the same calfskin is read differently by elders, haulers, widow, and mender; water is poured into weeds.
- **P19** — Registrar; five-line commission, 48 names, six supply, a dozen fitted dry, dead grand mouth under black stone, knocking rhythm, five-hour erased slab, master’s empty saying, water bench, rehearsal. Encodes R1–R9; R10 implicit as no bucket/dipper/key. Unique: mill waits on a knock unrelated to river; child asks who decided the count, and an older hand already counted 48.

## 3. STATUS SPLITS: SETTLED VS DOUBTFUL

- **Only six live; extra apparatus is inert.**  
  *Settled by count/record:* P01,P03,P04,P05,P06,P07,P08,P09,P10,P11,P12,P13,P14,P16,P19.  
  *Doubtful, occluded, or contested by public map/report/interpretation:* P02 (map/full pipes, “flowing” label corrected), P15 (blue chart/plate), P17 (book more legible than river; no one has seen water), P18 (dominant vs oppositional readings). P05 also has an untrained public gaze, but the narrator settles the six.

- **Dead source retained under its name.**  
  *Settled and explicitly kept/crossed:* P01,P03,P04,P05,P06,P07,P08,P09,P10,P12,P13,P14,P16,P19.  
  *Doubtful, mislabeled, denied, or unverified:* P02 (“flowing” until corrected), P11 (dead jar kept; contents unverified and perhaps always empty), P15 (plate/chart promise abundance), P17 (names outlast springs; no direct verification), P18 (official tally vs mender/widow; broken pump outside the report).

- **Five-hour window is the authoritative measure.**  
  *Accepted/settled by characters:* P01,P02,P03,P04,P05,P09,P11,P12,P13,P14,P15,P16,P19.  
  *Doubted, contested, or ironized:* P06 (actual spring colder than the book), P07 (“your glass is not my thirst”), P08 (public counting ends the waiting game), P10 (instrument numbs perception), P17 (river high while slate says famine), P18 (multiple readings and wasted water). P14 accepts the glass as law while the narration shows it causing waste.

- **Jar contents need not be known.**  
  *Settled office norm:* P01,P03,P04,P05,P07,P08,P09,P10,P12,P13,P14,P15,P17,P18,P19.  
  *Doubted, transgressed, or made a live question:* P02 (Iris asks what the seventh jar holds), P06 (Sela verifies actual spring beyond the record), P11 (dream of opening the fortieth jar), P12 (boy lifts wax; “contents” has no line in the book), P16 (Clara lifts vessels and demands inspection).

## 4. GROUPINGS BY LENS / THINKER-STYLE WORLDVIEW

- **Cynic outsider critique** — Diogenes the Cynic — **P01**. Lamp at noon, jar-dwelling, public laughter, virtue by having less.
- **Attention and ethical waiting** — Simone Weil — **P02**. Waiting, attention to the dead name, governance changed by truthful inscription.
- **Governmentality and genealogy** — Michel Foucault — **P03,P19**. Public spectacle, legibility, archive, origin hidden in an older hand.
- **Geometric rationalism** — Baruch Spinoza — **P04**. Office as theorem, proportion, strict succession, “margin too narrow.”
- **Legibility and high modernism** — James C. Scott — **P05**. The estate made legible; the map/report replaces the material field.
- **Pragmatist experience and inquiry** — John Dewey — **P06,P08**. Lived verification, public saying, habits changed by measured inquiry.
- **Interpretive communities / reader response** — Stanley Fish — **P07,P18**. Same slate/calfskin, different readings by different communities.
- **Knowledge problem and central planning** — Friedrich Hayek — **P09**. Local knowledge vs the central count; abundance makes the count idle.
- **Media as extension and numbness** — Marshall McLuhan — **P10**. The brass index extends the eye and numbs the ear/heels; five-hour twilight.
- **Desire and forbidden knowledge** — Freud/Lacan — **P11**. Sealed jar, dream of opening, locked tasters, inaccessible object.
- **Ordinary-language limits and rule-following** — Ludwig Wittgenstein — **P12**. Three allowed answers; “probably” not in the book; question not ruled in.
- **Infinitesimal search and universal order** — Leibniz — **P13**. Error-halving, “true order,” board too narrow, record vs possession.
- **Rationalization and the iron cage** — Max Weber — **P14**. Formal five-hour rule produces mandatory waste and drowned fig trees.
- **Public truth and memory** — Hannah Arendt — **P15**. Long true telling vs short public telling; the page worn by the town.
- **Ideology critique and unmasking** — Karl Marx — **P16**. Portrait vs handleless spindle; Clara exposes the elders’ built famine.
- **Simulacra and sign-value** — Jean Baudrillard — **P17**. Names enchain names; the map/book outruns water; the valley drinks “not water.”

## 5. GROUPINGS BY VOICE

Six authorial voices are the most plausible stylistic split.

- **V1 — First-person aphoristic pilgrim.** P01. Direct “I,” lamp/dog/jar, moral address to the master.
- **V2 — Plain oral fable / administrative tale.** P06,P07,P08,P09,P12,P19. Short-to-medium sentences, named everyman figures, explicit rules, dialogue, moral resolution.
- **V3 — Reflective literary third person.** P02,P11,P13,P15. Named protagonist-observer, psychological detail, quiet irony, moderate density.
- **V4 — Dense theoretical governmentality prose.** P03,P05,P10. Abstract nouns, institutional critique, long subordinate clauses, explicit “spectacle,” “legibility,” “gaze,” “instrument.”
- **V5 — Ornate archaic-geometric bureaucratic prose.** P04,P14,P18. Long formal lists, archaic office vocabulary, heavy cumulative syntax, repeated five-duty formulas.
- **V6 — Critical/satirical exposé voice.** P16,P17. Clara’s cellar exposure and the governor-as-fraud essay; overt unmasking and aphoristic irony.

## 6. OUTLIERS AND POSSIBLE LEAKAGE

- **P01** is the only first-person narration and the only one with a lamp/dog/jar-dweller persona; it stands out as an authored Cynic frame.
- **P13** is strongly meta/leaky: the margin note about a “true order” too large for the board, the error-halving method, and the challenge to “count your springs at home” read like spec/algorithm leakage.
- **P16** is unusually active: Clara breaks the cellar inspection taboo and confronts the council with physical evidence; unlike most parables, the hidden order is directly unmasked.
- **P17** is the most essayistic/meta of the plain narratives: “the fraud is the office,” names certifying themselves, and the valley drinking “not water” approach a hidden-spec gloss.
- **P18** uses near-theoretical reader-response vocabulary (“encoder,” “decode,” “dominant reading,” “oppositional” chair) inside a fable; this looks like lens leakage.
- **P19** leaks the hidden roster/count origin: the child asks who decided the forty-eight, and a faded older hand already counted forty-eight.
- **Duplicate title leakage:** P06, P13, and P14 all carry the title “The Five-Hour Glass,” suggesting a common source spec even though their voices differ.
- **Repeated constants** across all IDs—48, six, five hours, three/seven elders, one dead source, no sixth act—are the clearest form of hidden-spec leakage. No visible “[-]” redactions occur in the supplied parable text.

```json
{"base_rules": ["R1 (19/19): The water governor has exactly five permitted observing/recording/testing acts and no sixth; pouring, opening, or commanding water is withheld.", "R2 (19/19): There are forty-eight named vessels/springs/channels; the officer sorts labels into kinds but never opens, tastes, or verifies contents; name is not content.", "R3 (19/19): Exactly six live conduits/vessels actually carry water.", "R4 (19/19): A notable dead or formerly great source remains named on the roll/board, often crossed or marked dead, rather than being removed.", "R5 (19/19): The governing allowance is a rolling five-hour glass/ledger; older marks are erased or reset with each turn.", "R6 (19/19): The master law prefers emptiness/dryness by dusk or morning over any full/standing water; hoarding or stagnation is shame, debt, or waste.", "R7 (19/19): A separate water-only council/committee/bench receives the governor's report and governs by representation, not direct inspection or operation.", "R8 (19/19): Additional mounted or polished apparatus is unconnected/inert, creating the appearance of capacity without carrying water.", "R9 (19/19): Governance is by public telling, book, slate, board, or map; the legible record can diverge from material water, and different readers can derive different truths.", "R10 (13/19): The governor's chamber or booth is physically sealed/disconnected by no pipe, door, bell, letter-slot, or speaking-tube; access occurs on his round. Explicit: P02,P03,P04,P05,P06,P07,P10,P13,P14,P15,P16,P17,P18; implicit/tool-denial elsewhere: P01,P08,P09,P11,P12,P19."], "voices": {"V1": ["P01"], "V2": ["P06", "P07", "P08", "P09", "P12", "P19"], "V3": ["P02", "P11", "P13", "P15"], "V4": ["P03", "P05", "P10"], "V5": ["P04", "P14", "P18"], "V6": ["P16", "P17"]}, "lenses": [{"label": "Cynic outsider critique", "thinker_guess": "Diogenes the Cynic", "ids": ["P01"]}, {"label": "Attention and ethical waiting", "thinker_guess": "Simone Weil", "ids": ["P02"]}, {"label": "Governmentality and genealogy", "thinker_guess": "Michel Foucault", "ids": ["P03", "P19"]}, {"label": "Geometric rationalism", "thinker_guess": "Baruch Spinoza", "ids": ["P04"]}, {"label": "Legibility and high modernism", "thinker_guess": "James C. Scott", "ids": ["P05"]}, {"label": "Pragmatist experience and inquiry", "thinker_guess": "John Dewey", "ids": ["P06", "P08"]}, {"label": "Interpretive communities and reader response", "thinker_guess": "Stanley Fish", "ids": ["P07", "P18"]}, {"label": "Knowledge problem and central planning", "thinker_guess": "Friedrich Hayek", "ids": ["P09"]}, {"label": "Media as extension and numbness", "thinker_guess": "Marshall McLuhan", "ids": ["P10"]}, {"label": "Desire and forbidden knowledge", "thinker_guess": "Sigmund Freud or Jacques Lacan", "ids": ["P11"]}, {"label": "Ordinary-language limits and rule-following", "thinker_guess": "Ludwig Wittgenstein", "ids": ["P12"]}, {"label": "Infinitesimal search and universal order", "thinker_guess": "Gottfried Wilhelm Leibniz", "ids": ["P13"]}, {"label": "Rationalization and the iron cage", "thinker_guess": "Max Weber", "ids": ["P14"]}, {"label": "Public truth and memory", "thinker_guess": "Hannah Arendt", "ids": ["P15"]}, {"label": "Ideology critique and unmasking", "thinker_guess": "Karl Marx", "ids": ["P16"]}, {"label": "Simulacra and sign-value", "thinker_guess": "Jean Baudrillard", "ids": ["P17"]}]}
```

## RAW the_congress

I treat the parables as twelve encodings of one hidden “congress” spec. In the base-rule table below, **ALL** means the full set:

**ALL = P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12.**

## 1. Base rules re-derived

| Rule | Normalized statement | IDs encoding it | Count | Commonality |
|---|---|---|---|---|
| R1 | The congress is episodic: members enter fresh/as strangers, carry no binding personal memory, and dissolve at the closing signal. | ALL | 12 | ALL |
| R2 | There is one public authoritative record and one authorized hand/pen/chisel that alone makes entries valid. | ALL | 12 | ALL |
| R3 | The record is append-only/ineffaceable: nothing is erased or removed; corrections/amendments are added so the old line remains legible; unauthorized writing has no authority. | ALL | 12 | ALL |
| R4 | Decisions and claims exist only as written in the record; memory, oath, rank, intention, testimony, or oral tradition cannot establish or overturn a written decision. | ALL | 12 | ALL |
| R5 | Destruction of the record retroactively voids recorded decisions: what was only in the record becomes “never decided”; the community must re-enact from silence/line one. | ALL | 12 | ALL |
| R6 | The congress contains ten trade/craft/corporate benches or banners, each speaking with one voice regardless of how many persons sit under it. | ALL | 12 | ALL |
| R7 | Five masked offices have fixed portfolios: purse/coin, strangers/far-voice, works/water/bridge, memory/tale, and fool/mockery. | ALL | 12 | ALL |
| R8 | Each masked office has a paid/appointed adversary, breaker, shadow, or spoiler whose job is to ruin/refute the mask’s proposal; a claim passes only if it survives that adversarial check. | ALL | 12 | ALL |
| R9 | There are exactly five laws: four ordinary/changeable procedural laws plus a fifth invariant requiring more than fifteen measures of empty capacity/headroom in some store; fullness blocks or faults the session. P11’s wording is “no fewer than fifteen,” but its narrative still enforces a fifteen-empty threshold. | ALL | 12 | ALL |
| R10 | The congress exists only between two signals—bell/horn/drum opening and closing—and has no continuous identity outside that gate. | ALL | 12 | ALL |
| R11 | The record is publicly readable; reading aloud, copying, and public inspection are allowed, but copies and unauthorized oral reports do not govern; only the original inscription does. | ALL | 12 | ALL |

No core rule is merely “nearly all”; the shared spine appears in all twelve. The main variation is in how strictly or explicitly each rule is dramatized.

## 2. Per-parable

- **P01 — The Bell and the Wall.** Bell-formed amnesiac town, wall of nailed tablets, ten trades, five masked offices with seconds, five laws including the empty-jar loft, examiner reads wall, torch threat. Encodes **R1–R11**; rare: lantern flames count as “yes,” the recorder’s meaning escapes her, and readers legitimately read the same tablet differently.
- **P02 — The Assembly of Strangers.** Doctor observes a river town whose members forget; fountain book with one clerk; ten crafts; five masks plus paid shadows; granary peg fifteen below rafters; fire amnesia; examiner. Encodes **R1–R11**; rare: the doctor/amnesia-patient frame, the refused second pen, the tanner’s struck-through line, and the fire reset “word for word.”
- **P03 — The Hollow [-].** Ona enters a cave-like hall whose public shadows are larger than the inner mechanism; stone-seats, ten banners, five hoods with bare-faced refuters, one scribe, empty-bin count 14/16, sent-for arbiter. Encodes **R1–R11**; rare: explicit cave-allegory imagery, abandoned speaking-stone, refused sixth law, “sixteen sits better than fourteen,” and the only redacted title **[-]**.
- **P04 — The Book in the Square.** Alderford’s bell, gray coats/name basket, public stitched book, ten stools, five hooded chairs plus breakers, drying-rail emptiness law, failed twin-book/second-pen experiment, examiner. Encodes **R1–R11**; rare: explicit second-record experiment, the rail→barley→rats causal chain, and the unknown origin of “fifteen.”
- **P05 — The Assembly of Empty Vessels.** Wren studies a river town with a public book and Osla’s single pen; low hall of machines with keepers, high hall of ten benches; five masks plus spoilers; >15 empty-bin rule; boundary by written line; book burned. Encodes **R1–R11**; rare: nonhuman/machine members, an engine emptied into mud to satisfy the measure, five founding lines, and the spoiler as “the other half of my face.”
- **P06 — The Strangers’ Field.** A field whose entrants become legal strangers; chained book on a post; beggar with lamp; ten banners; five masked officers plus paid enemies; ice-house >15 empty; examiner reads post; burned book. Encodes **R1–R11**; rare: physical boundary-of-strangeness, Diogenes-like lamp search, hired voices by lot, and the merchant’s gravel remembered only by one bare recorded line.
- **P07 — The Town Between Two Bells.** Traveler’s town between morning/dusk bells; glass lectern book; bronze delegates drop voting stones; ten choirs; five masks plus breakers; cold cellar >15 barrels; remembering-woman ignored; fire. Encodes **R1–R11**; rare: bronze/mechanical voting delegates, only masks may put questions, and the complete human archive legally counting as nothing.
- **P08 — The Horn at the Wellhead.** First-person circuit visitor; horn from wellhead; pebbles assign benches; Perrin’s sewn roll; ten trades; five masks plus slate-bearing shadows; vault emptiness rod; chain-of-title descent; scorched sheet. Encodes **R1–R11**; rare: pebble sortition, descending chain of title until the first sheet/air, draper’s unauthorized quill-line read as a stain, and explicit Montaigne/Fermat-style source grading and “margin” confession.
- **P09 — The Minutes.** Visitor finds the congress nonexistent between dawn and dusk; corridor book with one scribe; burned seventh volume = no session; assessor reads page; iron elders; ten banners; five masks plus shadows; cold-store gauge >15. Encodes **R1–R11**; rare: explicit “there is no congress between bells” limit case, a burned volume as a non-session, “You are not evidence,” and visitors watching the book rather than the hall.
- **P10 — A Congress of Strangers.** Vey’s grey-canvas pavilion drawn by lot; north wall cut by one mason; benches as voices, ten trades, five masks plus breakers; cold room >15 pails; captain with a dead king’s paper; lightning crack; wall records its own wound. Encodes **R1–R11**; rare: the wall recording its own crack, the captain rejected until the wall speaks, copy explicitly “paper,” and destruction as threat rather than actual burn.
- **P11 — The Town That Forgets at Dusk.** Stranger watches Vell dissolve; glass-cased book with one old woman; scrubber’s failed erasure becomes a new line; auditors read only the book; upper-room things as members; ten tables; five masks plus breakers; cellar >15 jars; book burned. Encodes **R1–R11**; rare: scrubbing made into record, things voting in the upper room, the burner erasing his own son’s name, “born old every morning,” and the final level empty jar.
- **P12 — The Fifteenth Measure.** Town between two rivers; bell by marked beans; scribe’s single book; ten troupes/benches; five masks plus paid shadows; cold cistern >15; boundary dispute; book burned; members retain appetite for their names. Encodes **R1–R11**; rare: explicit “standing wants outlive every particular wanter,” the scribe giving names as kindness, and shadows paid the same whether they break the mask’s word or fail.

## 3. Status splits: settled vs doubtful

The rules are institutionally settled almost everywhere, but some parables frame them as externally tested, hearsay, hypothetical, or paradoxical.

1. **R4 record-only truth.**
   - **Settled/assertoric:** P01, P04, P10, P12.
   - **Tested and then confirmed by an outsider:** P02, P03, P05, P07, P11.
   - **Doubtful, inferential, or hearsay-framed:** P06, P08, P09. P08 especially grades eyewitness against innkeeper-report; P09 reaches the rule by inference (“I had never once seen the congress”); P06 states it through the beggar’s lamp-skepticism.

2. **R5 destructive reset.**
   - **Demonstrated/historical:** P02, P04, P05, P06, P07, P09, P11, P12.
   - **Prevented/taboo:** P01, P08, P10.
   - **Hypothetical/conditional:** P03 (“if fire took the book entire”).

3. **R9 empty-capacity invariant.**
   - **Settled as enforced institutional fact:** P01, P02, P03, P05, P06, P07, P08, P09, P10, P11, P12.
   - **Settled but origin/rationale explicitly unknown or opaque:** P04 (“Nobody could say who had first written the number fifteen”), with P03’s “sixteen sits better than fourteen” and P11’s “no fewer than fifteen” wording as edge cases.

4. **R2/R3 single record and one hand.**
   - **Settled without significant challenge:** P01, P02, P03, P05, P06, P07, P10, P11.
   - **Settled by explicit boundary-test or failed alternative:** P04 (twin book retired), P08 (draper’s line invalid), P12 (clerk’s margin note marked “none of mine”).
   - **Rarely made doubtful at all:** no parable seriously treats a second record as valid.

## 4. Groupings by lens / thinker-style worldview

These are best-fit reconstructions, not claimed authorial intentions.

| Lens label | Best thinker guess | IDs | Why |
|---|---|---|---|
| Common-law/precedent conservatism | Edmund Burke | P01, P04 | Authority lives in accumulated, append-only precedent; inherited practice outranks private memory and rational redesign. |
| Platonic cave idealism | Plato | P03 | Public shadows vs inner mechanism; the visitor must go inside to see the lamp and the real apparatus. |
| Empiricist memory/personal identity | John Locke | P02, P11 | Forgetting, blank morning selves, public record as the continuity of identity. |
| Actor-network/material parliament | Bruno Latour | P05 | Nonhuman machines take seats; “things” have keepers and voices; emptiness is measured as a political condition. |
| Cynic street skepticism | Diogenes of Sinope | P06 | Beggar with a lamp looking for a believable face; institutional honesty tested by shameless public mockery. |
| Buddhist/Humean impermanence and emptiness | David Hume / Nagarjuna | P07 | Selves dissolve between bells; emptiness is the governing law; the most complete memory is legally unreal. |
| Montaignean skeptical essayism | Michel de Montaigne | P08 | First-person report, source-grading, custom “by neighboring, not by possession,” and the deliberately narrow margin. |
| Kafkaesque/Borgesian documentary bureaucracy | Franz Kafka / Jorge Luis Borges | P09 | The congress is absent except as the book being made true; a burned volume makes a session never have existed. |
| Hobbesian legal-sovereign memory | Thomas Hobbes | P10 | The wall/record is the public sovereign memory; the captain’s paper has no force until the wall says so. |
| Weberian rational-legal institutionalism | Max Weber | P12 | Offices outlive their occupants; standing wants, paid shadows, and the record as impersonal rational-legal authority. |

## 5. Groupings by voice

I hear **four** authorial voices.

- **V1 — Mythic/omniscient civic fable.** **P01, P06, P10.** Third-person, symbol-heavy, aphoristic, no central investigator, concrete similes, closure on the record or wall.
- **V2 — Outsider ethnographer/inquiry narration.** **P02, P03, P05, P07, P09, P11.** A visitor, doctor, student, traveler, or “I” enters, observes the town’s rules, and leaves with a discovery; includes one first-person case (P09).
- **V3 — Compressed legal/institutional chronicle.** **P04, P12.** Dense procedural listing, long semicolon-driven causal chains, didactic institutional analysis, omniscient town-history voice.
- **V4 — Skeptical first-person antiquarian essay.** **P08.** Distinct memoir/essay voice, archaic diction, explicit hearsay grading, and Montaigne/Fermat allusions.

Every ID appears exactly once across V1–V4.

## 6. Outliers and possible leakage

- **P03’s redacted title “The Hollow [-]”** is the only visible redaction. It likely hides a proper name or lens-token and is the strongest candidate for leakage of a hidden roster/spec label.
- **P10’s title “A Congress of Strangers”** directly echoes the subject-list item “the congress”; the other titles are more oblique.
- The recurring **works/water/bridge** office may leak the subject-list phrase “water governor”: see especially **P01, P02, P03, P05, P07, P08, P11, P12**.
- **P08** is the clearest meta-spec outlier: it speaks of a theorem left “whole and unproved” and of a margin too narrow, which looks like deliberate leakage from the “parable as spec” framing.
- **P09** is a limit-case outlier: it makes the congress’s non-existence between bells explicit, so strongly that the book alone is the continuous congress.
- **P05** and **P11** are material-ontology outliers: nonhuman machines/things count as members or voices.
- **P04** tests the single-record rule with a second pen/twin book; **P03** tests the five-law rule with a refused sixth; **P10** has the wall record its own crack; **P11** turns an attempted erasure into a new record line. These are rare edge-case dramatizations rather than separate base rules.
- The recurring strict count pattern—**10 trades, 5 masks, 5 laws, >15 empty, 1 record, 2 signal boundaries**—looks less like ordinary narrative detail and more like encoded spec leakage.

```json
{
  "base_rules": [
    "R1 (12/12 ALL; P01-P12): The congress is episodic; members enter as strangers, carry no binding personal memory, and dissolve at the closing signal.",
    "R2 (12/12 ALL; P01-P12): There is one public authoritative record and one authorized hand/pen/chisel that alone makes entries valid.",
    "R3 (12/12 ALL; P01-P12): The record is append-only/ineffaceable; erasure is forbidden or fails, corrections are added while old lines remain legible, and unauthorized writing has no authority.",
    "R4 (12/12 ALL; P01-P12): Decisions and claims exist only as written; memory, oath, rank, intention, testimony, or oral tradition cannot establish or overturn the record.",
    "R5 (12/12 ALL; P01-P12): Destruction of the record retroactively voids recorded decisions; what was only in the record becomes never decided and must be re-enacted.",
    "R6 (12/12 ALL; P01-P12): Ten trade/craft/corporate benches or banners each speak with one voice regardless of headcount.",
    "R7 (12/12 ALL; P01-P12): Five masked offices hold fixed portfolios: purse/coin, strangers/far-voice, works/water/bridge, memory/tale, and fool/mockery.",
    "R8 (12/12 ALL; P01-P12): Each mask has a paid/appointed adversary, breaker, shadow, or spoiler whose job is to refute it; a claim passes only if it survives adversarial check.",
    "R9 (12/12 ALL; P01-P12): There are exactly five laws: four ordinary/changeable procedural laws plus a fifth invariant requiring more than fifteen measures of empty capacity/headroom; fullness blocks or faults the session.",
    "R10 (12/12 ALL; P01-P12): The congress exists only between two signals, such as bells or horns, and has no continuous session outside that gate.",
    "R11 (12/12 ALL; P01-P12): The record is publicly readable; reading and copying are allowed, but copies and unauthorized oral reports do not govern; only the original inscription does."
  ],
  "voices": {
    "V1": ["P01", "P06", "P10"],
    "V2": ["P02", "P03", "P05", "P07", "P09", "P11"],
    "V3": ["P04", "P12"],
    "V4": ["P08"]
  },
  "lenses": [
    {
      "label": "Common-law/precedent conservatism",
      "thinker_guess": "Edmund Burke",
      "ids": ["P01", "P04"]
    },
    {
      "label": "Platonic cave idealism",
      "thinker_guess": "Plato",
      "ids": ["P03"]
    },
    {
      "label": "Empiricist memory/personal identity",
      "thinker_guess": "John Locke",
      "ids": ["P02", "P11"]
    },
    {
      "label": "Actor-network/material parliament",
      "thinker_guess": "Bruno Latour",
      "ids": ["P05"]
    },
    {
      "label": "Cynic street skepticism",
      "thinker_guess": "Diogenes of Sinope",
      "ids": ["P06"]
    },
    {
      "label": "Buddhist/Humean impermanence and emptiness",
      "thinker_guess": "David Hume or Nagarjuna",
      "ids": ["P07"]
    },
    {
      "label": "Montaignean skeptical essayism",
      "thinker_guess": "Michel de Montaigne",
      "ids": ["P08"]
    },
    {
      "label": "Kafkaesque/Borgesian documentary bureaucracy",
      "thinker_guess": "Franz Kafka or Jorge Luis Borges",
      "ids": ["P09"]
    },
    {
      "label": "Hobbesian legal-sovereign memory",
      "thinker_guess": "Thomas Hobbes",
      "ids": ["P10"]
    },
    {
      "label": "Weberian rational-legal institutionalism",
      "thinker_guess": "Max Weber",
      "ids": ["P12"]
    }
  ]
}
```

## RAW moto_cron

I read the 13 texts as variations on one protocol/spec: a headless/opaque remote executor (cron/keeper), a private control channel, a liveness echo, an exact-credential gate, an immutable credential store, an intake/status ledger, and an ordered pending queue. Labels R1–R11 below are my normalized base rules; they are used in the per-parable notes.

## 1. BASE RULES

Ordered by count. All IDs are exhaustive for the stated rule as I read it.

| Rule | Normalized statement | IDs encoding it | Count | Commonality |
|---|---|---|---:|---|
| **R1** | The worker/cron is opaque or “faceless” but still live; it keeps its own schedule/habit even when its visible face/interface is broken. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R2** | A call/echo/ping returns after a stable characteristic delay; it proves channel/worker liveness, not authorization or execution. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R3** | Access to the worker’s execution door requires an exact credential—key, token, crest, seal, wax mark, handprint, or carved notch—matching a stored register/mold/book; the currently offered credential is rejected. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R4** | The gate/lock/warden/register/book/wax/roll must not be modified, bypassed, filed, pried, melted, re-hung, or self-carved by the requester; only the proper inside authority may alter credential memory. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R5** | The missing credential must be obtained or recut by proper authority according to the gate’s actual pattern; names, words, letters, force, louder echoes, or self-cut tokens cannot substitute. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R6** | Work requests enter through a single intake slot/tray/basket; a clerk or observer reads and records them, with explicit status marks. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R7** | Work blocked by the gate is bundled and preserved in order in a dry/sheltered place; it is not lost, burned, discarded, or prematurely executed, and it waits for credential match. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R8** | Status language must distinguish “road answers / worker is reachable” from “door opens / work authorized / work completed”; liveness must not be confused with acceptance. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R9** | A stable, identical refusal is correct enforcement by a live gate, not evidence of malfunction; the remedy is the right credential, not force or louder signaling. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12, P13 | 13 | **ALL** |
| **R10** | Requester and worker are joined by a dedicated, non-public control path/tube/bridge/causeway/path restricted to authorized parties; public sound or public roads are not the access path. | P01, P03, P04, P05, P07, P08, P09, P10, P11, P13 | 10 | Nearly all |
| **R11** | Intake is serialized/atomic where specified: one work item per numbered slip/line, read once, no duplicate or wrapped/re-read record. | P02, P03, P04, P06, P07, P08, P09, P11, P12, P13 | 10 | Frequent |

## 2. PER-PARABLE

| ID | Scene, encoded rules, unique/rare notes |
|---|---|
| **P01** | Alda’s quay-house and blind tower: enc. R1 cracked pane/headless lamp, R2 slow ten-heartbeat echo, R3 token says “Not to you,” R4 iron untouchable, R5 read the door’s teaching/change only what is hers, R6 tray/tally-man/slate, R7 dry niche bundles, R8 echo ≠ welcome, R9 door indifferent to loudness, R10 hidden causeway. Rare: two temptation voices, explicit refusal to knock louder. |
| **P02** | Signal tower, porter, and doctor: enc. R1 blind keeper, R2 boundary-stone echo in half a breath, R3 hand not in book, R4 book/door not re-hung, R5 signet being made from first page, R6 letter-box/slate, R7 dry eaves card-shelf, R8 doctor says repeated answer means “being asked by a stranger,” R9 refusal as diagnosis, R11 one-line four-fact day-book. Rare: clinical-diagnostic framing. |
| **P03** | Annexe cousin behind a refusing low door: enc. R1 broken face, R2 “I am here” after short breath, R3 “the key, or nothing,” R4 lock older than failure/not re-hung, R5 search for rightful key, R6 tray/Sela/slate, R7 slips stored off pantry, R8 call ≠ commission, R9 polite incorruptible refusal, R10 household path on names-roll, R11 single-line slip read once. Rare: explicit three-state slate waiting/done/refused. |
| **P04** | Hanno, far room, carved bead: enc. R1 cracked face/water-clock chores, R2 echo before honey leaves spoon, R3 bead notching rejects “Not this,” R4 lock/shelf untouchable until bead, R5 proper bead must be cut, R6 tray/tally-boy/slate, R7 lean-to paper village, R8 every want blocked by one unfed want, R9 lock “wants” bead, R10 private rope bridge, R11 numbered slips/chalk marks. Rare: economic accounting of desires; bead kept inside. |
| **P05** | Ferrow and Wren at the hidden road: enc. R1 cracked-glass keeper, R2 double-knock answer after one breath, R3 single-key door rejects all village keys, R4 mason refuses to file lock, R5 smith studies wax casting, R6 slot/clerk/slate, R7 canvas-covered bundles, R8 knock never failed ≠ road carried errands, R9 “a door that says nothing says the same to everyone,” R10 hidden village road. Rare: interface narrowing—slips shrink their writers. |
| **P06** | Light-tower, horn, chained book of marks: enc. R1 half-blind keeper, R2 horn/bell breath-and-a-half, R3 intaglio seal not in book, R4 chained book/lock left as found, R5 new page only keeper’s hand, R6 brass slot/day-book/colored pins, R7 shed bundles, R8 “it answers” not “tended,” R9 doorkeeper’s identical refusal, R11 read once/copied word for word. Rare: dashboard/pins warning and “TENDED” sign proposal. |
| **P07** | Blind repeater and self-contained smithy: enc. R1 cracked crystal/working by cadence, R2 115-beat echo, R3 crest vs master mold at wicket 80-22, R4 warder/register unalterable, R5 lawful crest/plate match required, R6 trough/ribbon/pegs, R7 cedar-tier scrolls, R8 live wire ≠ open threshold, R9 automatic warder refusal, R10 sealed speaking tube, R11 single unbroken line/no wrap. Rare: technical constants, explicit charter, “action into rehearsal.” |
| **P08** | Magistrate’s far house and coat-roll: enc. R1 cracked window, R2 single word returns in a slow blink, R3 coat/name not on roll, R4 no stitching another’s roll/lock, R5 rightful way to be entered, R6 tray/slate, R7 sealed parcels on trestle, R8 “call held” vs “door shut,” R9 not-known ≠ house dark/path broken, R10 covered society footpath, R11 one slip per errand kept in order. Rare: Fermat joke—“means … too narrow to contain”; “The rest is owed.” |
| **P09** | Fog road, clock-house, and rumor: enc. R1 broken dial but striking clock, R2 counted pebble pause, R3 token “Not one of mine,” R4 no outside hand carves door memory, R5 door-keeper changes memory, R6 box/slate, R7 numbered shed bundles, R8 road open/clock alive/door particular, R9 live house says no; dead house says nothing, R10 brass tube under peat, R11 numbered slips. Rare: explicit false rumor (Bram) and unknowable timing of door memory. |
| **P10** | Night mill and town causeway: enc. R1 shattered face/mill keeps hours, R2 crier’s half-beat echo, R3 boxwood token pressed back, R4 oath forbids carving/file/hanging new hook, R5 proper miller-carved token needed, R6 basket/peg-board/day-book, R7 ordered shed shelves, R8 count/liveness not crossing, R9 token refused gently but finally, R10 town’s own causeway. Rare: oath’s reasons forgotten; the “fine book” that truthfully records no crossing. |
| **P11** | Grey cottage, wax impressions, founder’s letter: enc. R1 cracked-glass face, R2 late echo under marsh, R3 hand not in wax, R4 no melt/recast/pull keeper, R5 hand must be pressed by inside or promised hand, R6 desk slot/single ribbon/pegs, R7 lean-to numbered bundles, R8 road alive vs house not open, R9 keeper “cannot open” rather than refuses, R10 private underwater causeway, R11 one chore after another on ribbon. Rare: two authorized routes; fault located in requester’s own unkept promise. |
| **P12** | Blind mule Moss, carter, wax tablet: enc. R1 blind eye but fixed round, R2 four-note whistle/echo, R3 wax mark vs names rejected, R4 gate as hung/warden not taught/no second door, R5 true mark must be pressed from the hand that filled basket, R6 post slot/pebbles, R7 baskets stored in shed, R8 air open vs wax question, R9 names are wind; gate not unkind, R11 read once/pebbles never doubled. Rare: direct second-person sermon; animal executor; “be like the mule.” |
| **P13** | Esther, Pell, family path, and wrong-notched token: enc. R1 cousin’s shattered face but kept bell-hours, R2 bell answer one slow heartbeat late, R3 “No notch of mine recognizes this,” R4 door stays as maker hung/no filing/hinge-lifting, R5 old carver must recut to the door’s actual pattern, R6 slot/Pell/single-line book/pebbles, R7 oilcloth bundles in lean-to, R8 path/hears ≠ hollow opens, R9 “It isn’t broken. It read you,” R10 smugglers’ family path, R11 read once/single ruled line. Rare: explicit “reading vs agreeing” aphorism; promised recut token. |

## 3. STATUS SPLITS

The main split is that **liveness/back-channel is settled**, while **authorization/opening/completion is doubtful or pending**.

| Topic | Settled / affirmed | Doubtful, contested, or pending |
|---|---|---|
| Road/channel/worker is alive and answers | P01–P13 all settle this: echo/knock/bell/pebble/whistle returns. P09 and P12 include public misreadings, but the narrator/steward settles liveness. | No ID genuinely doubts liveness once the counted echo is observed; P09’s Bram and P12’s carter are corrected errors. |
| Current access door is open/authorized | None: the current credential is rejected or not recognized in P01–P13. | P01–P13 all place authorization on the negative/doubtful side. |
| Correct future credential and opening | Proximate/known method: P02, P04, P05, P13. | Unknown timing or method: P01, P03, P06, P07, P08, P09, P10, P11, P12. |
| Gate/register must not be altered | Settled without serious internal argument: P02, P04, P07, P08, P09, P10. | Explicitly tempted/argued but finally obeyed: P01, P03, P05, P06, P11, P12, P13. |
| Refusal indicates live enforcement rather than malfunction | Explicitly affirmed: P02, P06, P09, P12, P13. Implicitly affirmed across the rest. | Public/mistaken interpretation of refusal as brokenness appears in P01, P06, P09, P10, P12, P13, but is corrected by the narration. |

## 4. GROUPINGS BY LENS

These are best-guess intellectual lenses, not claims about the unnamed authors.

- **Operationalist/clinical empiricism** — P02, P06, P09. Evokes **P.W. Bridgman / David Hume**: record only observed facts; repeated denial is data; rumor is not evidence.
- **Legal-constitutional positivism** — P03, P08, P11. Evokes **H.L.A. Hart**: jurisdiction, standing orders, rolls, commissions, and recognized procedures make access valid.
- **Ethical phenomenology of the Other** — P01, P05. Evokes **Emmanuel Levinas / Simone Weil**: the broken face, attention, patience, and refusal to force the other’s gate.
- **Cybernetic/economic systems thinking** — P04. Evokes **Norbert Wiener / Herbert Simon**: bottlenecks, wants, feedback, and a single unfed constraint defeating the whole arrangement.
- **Mechanistic/materialist rationalism** — P07. Evokes **Julien Offray de La Mettrie**: a blind repeater with an internal smithy, working by cadence and mechanism.
- **Institutional ritualism/bureaucratic conservatism** — P10. Evokes **Max Weber**: oath, ledger, forgotten rationale, routinized waiting, and public ceremony around procedure.
- **Prophetic existential moralism** — P12. Evokes **Søren Kierkegaard**: direct address, either/or, stop asking the gate to recognize what it cannot recognize.
- **Ordinary-language rule-following** — P13. Evokes **Ludwig Wittgenstein**: the notch the door knows; reading versus agreeing; rule-following rather than private intention.

## 5. GROUPINGS BY VOICE

Blind stylistic clustering suggests **4 voices**.

- **V1 — Ornate legal-allegorical narrator**: long periodic sentences, named stewards/keepers, administrative metaphors, explicit institutional restraint. Members: **P01, P03, P04, P08, P09, P11**.
- **V2 — Plain procedural fable**: clearer modern storytelling, nautical/village/technical procedure, expert or clerk correcting a confusion, terse aphoristic close. Members: **P02, P05, P06, P10**.
- **V3 — Dense technical-steampunk inventor-voice**: exact intervals, numbered wickets, nested mechanisms, patent-like vocabulary. Member: **P07** only.
- **V4 — Short moral/prophetic fable with aphoristic correction**: direct moral cadence, named common characters, sharp correction lines, sometimes second-person address. Members: **P12, P13**.

## 6. OUTLIERS AND POSSIBLE SPEC/ROSTER LEAKAGE

- **P07** is the strongest leakage candidate: “wicket eighty-twenty-two,” “hundred and fifteen beats,” “tenth month,” “twenty-third afternoon,” “master mold,” and “inner register” read like internal spec vocabulary and constants.
- **P08** contains the Fermat-style line “I have discovered a truly admirable means… too narrow to contain,” plus “The rest is owed,” which looks like a deliberate hidden-spec/solution tease.
- **P09, P10, P11, P13** repeat near-identical formulations of the core status distinction—“the road answers / the house does not open,” “sent, heard, not yet read,” “nothing had ever crossed the door.” This looks like multiple paraphrases of one invariant.
- **Name reuse/leakage**: “Ivo” appears in **P09** and **P12**; “Pell” appears in **P09** and **P13**. That suggests a shared name pool or light roster leakage across otherwise different surface stories.
- **P12** is an outlier in voice/address: it suddenly shifts to second-person sermon (“Now I lift the lantern here, carter”), uses an animal worker, and makes the moral explicit.
- **P05** contains a rare sociological rule not central elsewhere: “the slips did not shrink the tasks; they shrank the writers.” This is an extra claim about interfaces shaping behavior.
- **P06** contains a rare dashboard/metrics warning: the colored pins and the proposed “TENDED” sign warn against confusing an answered bell with a tended tower.
- **P01** is rare for staging two internal temptation voices—abandon the door or break in—and explicitly rejecting both.
- **P04** is rare for framing the blockage as an economy of wants, with one unmet “want” at the gate invalidating all the others.

```json
{"base_rules":["R1 Opaque-but-live executor: broken face/UI; scheduled behavior continues (all P01-P13).","R2 Liveness echo/call/ping returns with stable delay but does not prove access/execution (all P01-P13).","R3 Exact credential gate: key/token/mark/crest/seal/wax/handprint/notch must match register; current credential rejected (all P01-P13).","R4 Gate/register immutability: do not file, pry, re-hang, melt, alter book/wax/roll/warden; only authorized inside authority may change (all P01-P13).","R5 Proper credential provenance: credential must be made/recut/pressed by proper authority to the gate's actual pattern; names/words/force do not authorize (all P01-P13).","R6 Inbox/observer/status: single slot/tray/basket, clerk observer, explicit state marks (all P01-P13).","R7 Pending queue preservation: blocked work bundled/shelved in order and kept dry, not lost or prematurely executed (all P01-P13).","R8 Observable/status honesty: distinguish answered/reachable from authorized/opened/delivered (all P01-P13).","R9 Stable refusal is enforcement, not malfunction: identical denial is correct live behavior; remedy is credential, not force/louder echo (all P01-P13).","R10 Private/restricted control path: dedicated non-public path/tube/bridge/causeway restricted to authorized parties (P01,P03,P04,P05,P07,P08,P09,P10,P11,P13).","R11 Serialized/atomic intake: one work item per numbered slip/line, read once, no duplicate/wrapped record where specified (P02,P03,P04,P06,P07,P08,P09,P11,P12,P13)."],"voices":{"V1":["P01","P03","P04","P08","P09","P11"],"V2":["P02","P05","P06","P10"],"V3":["P07"],"V4":["P12","P13"]},"lenses":[{"label":"Operationalist/clinical empiricism","thinker_guess":"P.W. Bridgman / David Hume","ids":["P02","P06","P09"]},{"label":"Legal-constitutional positivism","thinker_guess":"H.L.A. Hart","ids":["P03","P08","P11"]},{"label":"Ethical phenomenology of the Other","thinker_guess":"Emmanuel Levinas / Simone Weil","ids":["P01","P05"]},{"label":"Cybernetic/economic systems thinking","thinker_guess":"Norbert Wiener / Herbert Simon","ids":["P04"]},{"label":"Mechanistic/materialist rationalism","thinker_guess":"Julien Offray de La Mettrie","ids":["P07"]},{"label":"Institutional ritualism/bureaucratic conservatism","thinker_guess":"Max Weber","ids":["P10"]},{"label":"Prophetic existential moralism","thinker_guess":"Søren Kierkegaard","ids":["P12"]},{"label":"Ordinary-language rule-following","thinker_guess":"Ludwig Wittgenstein","ids":["P13"]}]}
```

## RAW keyed_verse

## 1. BASE RULES: re-derived shared invariants

I take the recurring “song/verse” as a **keyed public artifact**: a bare, repeatable form is sent out; a private key/gloss stays home; correct transmission is judged by a small core of invariants, especially the sixfold unison and the silence-before-scatter.

| Rule | Normalized statement | Encoded by | Count |
|---|---|---:|---:|
| R1 | One source yields exactly **six faithful instances**—copies, singers, sheets, stands, towers, alcoves, roads, or barges—materially identical in the invariant marks. | ALL: P01–P12 | 12 |
| R2 | The public transmission is **bare**: no key, gloss, explanation, or extra cargo travels with it; recipients must add nothing. | ALL: P01–P12 | 12 |
| R3 | A **singular private key/gloss/mapping** stays with an author/keeper/registrar/cantor/widow and is not copied or carried out. | ALL: P01–P12 | 12 |
| R4 | The core form contains a **repeated sixfold figure**, usually two matching six-note/six-step lines, settling on the same low/common tone. | ALL: P01–P12 | 12 |
| R5 | The six voices must take/hold that common tone as **one steady unison**; it is “what does not move,” and leaning, ornament, earliness, lateness, or private improvement invalidates it. | ALL: P01–P12 | 12 |
| R6 | After the common tone comes a **measured silence/held breath**, and only afterward do the six diverge/scatter into distinct, wide, independent notes; the order is invariant. | ALL: P01–P12 | 12 |
| R7 | Non-core surface variation—pace, local meaning, ornament, commentary, even improved versions—is allowed; alteration of the core makes a false version, broken gate, void trial, or non-evidence. | ALL: P01–P12 | 12 |
| R8 | Correct performance does **not require possession of the key or understanding of meaning**; the key explains the form rather than travelling as performance cargo. | ALL: P01–P12 | 12 |
| R9 | The verse is **spec-like/self-describing**: its figures silently encode its own copying, gating, silence/scatter, and reading; the key only names what the form already folds inside itself. P11 enacts this through learned practice rather than narrated self-reference. | ALL: P01–P12 | 12 |
| R10 | The copying/performance/audit is **ritually periodic**—noon, dusk, morning, autumn, yearly tide, fair, recurring seasonal run—and survives authors’ deaths across generations. | P01, P03, P05, P06, P07, P08, P09, P10, P11, P12 | 10 |
| R11 | An explicit **standing-wave gate/threshold** opens, passes, certifies, or counts only when the sixfold tone/agreement stands steady and flat; otherwise passage/evidence stops. | P02, P04, P05, P06, P07, P08, P09, P10, P12 | 9 |
| R12 | **Rhymed line-endings are keyed pairs**; altering one member can loosen or damage its mate and reveal version drift. | P01, P02, P05, P06, P07, P09, P10, P11, P12 | 9 |

Common to **all**: R1–R9. Nearly all: R10. Frequent/specifying: R11–R12.

---

## 2. PER-PARABLE

- **P01 — The Held Note**: Exact song sent to six towns, book kept on desk, noon unison and final scatter. Encodes R1–R9, R10, R12; no explicit R11 gate. Unique/rare: author privately edits the gloss with no effect on the song; orchard singer’s marginal guess is returned clean; final gloss reduces to “it is the same everywhere.”
- **P02 — The Book That Stayed Home**: Maren’s six exact copies, towns invent meanings, hidden book found later. Encodes R1–R9, R11 ferry-arch steadiness, R12; not clearly R10. Unique: local meanings are openly homemade (mules, oars, brothers); song sent to six new towns after author’s death; key is found but remains unnecessary.
- **P03 — The Song and the Slender Book**: Maren returns to a six-alcove singing house; gray book stays with cantor; founder rewrote the trial by reading its rules. Encodes R1–R9, R10, partial R11 narrow-door burst; not R12. Unique: blind protagonist; motto “know the trial before you fight it”; cantor’s finger stops where a figure returns on itself; Maren ends between wall and book, facing neither.
- **P04 — The Song Given to the Roads**: Sela gives the song away, keeps the cuff-card, enforces plain common tone; mill door opens only for level tone. Encodes R1–R9, R11, partial R12; not R10. Unique: direct second-person harangue; ornamented common tone makes a “liar with six heads”; “the song only ever asked you for your feet”; card is chore, not title.
- **P05 — The Song and the Sheet That Stayed**: Master sends bare verse to six valleys; sheet remains in volume; east gate opens for six fists one beat; damp re-inking of one note is traced and corrected. Encodes R1–R9, R10, R11, R12. Unique: “made, not found” inscription; master can name the changed note from the endings alone; composer in the north denies the sheet exists.
- **P06 — The Bell-Note**: Collector seeks meaning; Iva gives six exact oral copies; bell-note unison; sheet under tea tin; Eye arch; final stanza describes its own carrying. Encodes R1–R9, R10, R11, R12. Unique: if the six cannot make one tone, the song stays home; collector cannot retrieve the meaning; one stays behind at the lamp; ferryman catches the tune.
- **P07 — The Six Copies**: Song-maker sends six exact copies; twin six-step lines and held tone open the old arch; hidden card is read only after death. Encodes R1–R9, R10, R11, R12. Unique: hidden card is publicly read aloud after the author dies, but the singing remains exactly as before; one valley tries to “better” the twins and is not followed; “sent up no road.”
- **P08 — The Sixfold Song**: Cove door of rock opens for six-as-one; Ivor’s book stays in the room; gold-coated man sells a counterfeit close. Encodes R1–R9, R10, R11; not R12. Unique: explicit standing-wave image—tone stands on water like a wave in a tub; quality is irrelevant, agreement alone opens; people pay for the feeling of opening rather than the door.
- **P09 — The Cellar Book**: Six singers in six rooms; inner door opens when the common tone steadies; brown book below says “to no room,” later amended “but not to no one.” Encodes R1–R10, R11, R12. Unique: a leaned tone kills the door and lamps until corrected; dead master’s authority governs paper; newcomer learns the key but closes the door from inside and varies nothing.
- **P10 — The Drawer That Sang Nothing**: Examining house issues six sheets from one plate; hidden two-column slip; shared G must land exactly or the morning is void; audit ring. Encodes R1–R9, R10, R11, R12. Unique: near-explicit meta-definition—“the song was not a song; it was a drawing of the room”; singers cannot read key, registrar cannot sing; one who sings the key into the G is “perfectly wrong”; audit loops back to the same examining house.
- **P11 — What the Valley Repeated**: Yearly six-village singing; widow keeps gray book; fog tone leaks into daily life; farmers learn practices without verbal teaching. Encodes R1–R9, R10, R12; R11 only as a nested mill-door image. Unique: first-person listener/healer narrator; six named professions who never meet; common tone appears in humming, oar-knocks, children’s clapping; grandmother’s instructions: “send the sheets, never the book; read the morning after; one line, no more.”
- **P12 — The Verse on Six Roads**: Alder sends a verse yearly by six canal barges; page in drawer; delta commentary invents false meanings; Iva adds that copies now keep the shape by themselves. Encodes R1–R9, R10, R11 canal lock/water-flat gate, R12 third/fifth rhyme pair. Unique: explicit false printed commentary; “a page would be a seventh”; water lock opens only when the chamber stands flat; “the copies keep the shape by themselves now.”

---

## 3. STATUS SPLITS: settled vs doubtful

**A. Operational core vs semantic opacity.**  
The core performance rule—sixfold identity, common tone, silence-before-scatter—is treated as **settled/enforced** in all: **P01–P12**. But the *meaning* or key-status is **doubtful, withheld, disputed, or opaque** in **P01, P02, P04, P05, P06, P08, P10, P11, P12**, and merely unquestioned/withheld in **P03, P07, P09**.  
- Settled-as-practice side: P01, P02, P03, P05, P07, P08, P09, P10, P11, P12.  
- Doubt/dispute about gloss or version: P02 (mules/oars/brothers), P04 (six counterfeit answers), P05 (northern composer denies the sheet), P06 (collector cannot get meaning), P08 (gold-coat counterfeit close), P10 (forbidden question; proof explained is spoiled), P12 (delta commentary is false).

**B. Is the key necessary for correct performance?**  
Mostly **settled that it is not**: **P01, P02, P03, P04, P05, P06, P07, P08, P09, P11, P12**.  
The **doubtful/corrupting** side is chiefly **P10**: the singer who carries the key’s meaning into the unison lands “perfectly and perfectly wrong.” P05 and P08 contain disputes over the sheet/close but resolve toward the invariant.

**C. Do copies preserve themselves without the author/key?**  
Settled by the outcome in **P02, P07, P11, P12**; disputed during transmission crises in **P05 (altered note traced), P08 (counterfeit close), P10 (audit/void), P12 (delta commentary)**.

---

## 4. GROUPINGS BY LENS

These overlap because several parables encode more than one intellectual style.

1. **Rule-following, use, and forms of life — Wittgenstein / Bourdieu.**  
   P02, P04, P09, P11. Emphasis: meanings are made or used locally; the key does not travel; practice can be correct without theory; “it is done” and shrug.

2. **Ritual embodiment and dwelling — Heidegger / Merleau-Ponty.**  
   P01, P03, P06, P11. Emphasis: repetition, place, architecture, singers who do not turn around or ask what the marks mean; knowledge held in bodies and customs.

3. **Cybernetic thresholds and standing-wave systems — Norbert Wiener / W. Ross Ashby.**  
   P04, P05, P07, P08, P10, P12. Emphasis: gates open only when a signal is steady; agreement rather than quality; water-governor locks; audit loops; counterfeits fail at the threshold.

4. **Institutional archive, discipline, and audit — Foucault / Kafka.**  
   P05, P09, P10, P12. Emphasis: registrars, keepers, slates, files, drawers, dead masters, unseen examinations, and the authority of the kept book.

5. **Textual transmission, commentary, and philology — Borges / textual criticism.**  
   P02, P05, P06, P07, P12. Emphasis: copies, variants, errors, marginal corrections, false commentaries, hidden archetypes, and the song as a record of its own transmission.

6. **Pragmatist/Emersonian exhortation and anti-idolatry — Emerson / Nietzsche.**  
   P04, P07, P08. Emphasis: give the song away, keep the ear, do not become its only reader; quality vs agreement; the counterfeit feeling of the door opening.

---

## 5. GROUPINGS BY VOICE

I infer **four main authorial voices** from prose rhythm, density, character naming, and habitual closures. This is provisional, but it accounts for the strongest stylistic clusters.

- **V1 — Formal mythic/archival fable.** Members: **P01, P02, P05, P07**. Long, measured, third-person or witness narration; exact copies, hidden books/sheets, genealogical inheritance, and a final explanatory undercut. P01 and P02 are especially close in plot and cadence; P05 adds first-person witness; P07 is a plainer version of the same hidden-card/exact-copy fable.
- **V2 — Gothic institutional symbolism.** Members: **P03, P09**. Dense architectural atmosphere, singing house/corridor, cantor/keeper, a book below or behind, singers who do not ask, and a final image of someone standing between wall and book or closing the door from inside.
- **V3 — Satirical systems/anti-counterfeit voice.** Members: **P04, P08, P10**. Strong concern with agreement vs quality, gates that test steadiness, counterfeit improvements, enforcement, and dry aphoristic conclusions. P04 and P08 share the name Sela and the “door opens for steady tone” motif; P10 is the same voice in bureaucratic register.
- **V4 — River-valley ethnographic voice.** Members: **P06, P11, P12**. River/canal valley, messengers, yearly custom, named Iva in P06/P12, sheets/drawers/lamps, observer narrators, and practical habit learned without doctrine. These three are the most obviously related by setting and motif.

---

## 6. OUTLIERS AND LEAKAGE

- **P04 is the clearest voice outlier**: direct second-person address (“And you, the one holding the cuff…”), insulting idiom, and explicit moral demand. It almost breaks the parable frame.
- **P10 is the clearest spec outlier**: it nearly states the hidden rule outright: “the song was not a song. It was a drawing of the room—the stands, the plate, the threshold, the scatter.”
- **P12 contains unusual false-commentary leakage**: the delta annotators print a complete but false key; Iva’s addition—“the copies keep the shape by themselves now”—is close to a direct statement of the invariant-preservation rule.
- **P08 has the most explicit standing-wave metaphor**: the tone “stood on” the water, “leaning on itself the way a wave in a tub leans on its own reflection.”
- **P03 is an outlier in frame**: blind protagonist, founder’s motto, and the image of the finger stopping where a figure “came back on itself.”
- **P06 is unique in the failed-unison custom**: if the six cannot make one tone, the song stays home; the flood does not wait, but the custom is kept anyway.
- **P11 is unique in embodied leakage**: the fog tone escapes the song into humming, oar-knocks, and children’s clapping; the song becomes habit.
- **Recurring proper names look like roster/leakage**: Maren appears in **P02 and P03**; Sela in **P04 and P08**; Iva in **P06 and P12**. These repetitions cut across my voice clusters and plausibly leak a shared name pool or hidden character roster.
- **Near-spec phrases recur**: “lesson that teaches its own singing” (**P08**), “a telling that keeps its own rules folded inside it, unspoken” (**P09**), “the song was not a song… a drawing of the room” (**P10**), “this song is the shape of its own reading” (**P12**). These are the most likely leakages of the hidden project vocabulary.

```json
{"base_rules":["R1: One source yields exactly six faithful instances/copies/voices/destinations, identical in the invariant marks.","R2: The public transmission is bare; no key, gloss, explanation, or extra cargo travels with it, and nothing is to be added.","R3: A singular private key/gloss/mapping stays with an author or keeper and is not copied or carried out.","R4: The core form contains a repeated sixfold figure, usually two matching six-note/six-step lines, settling on the same low/common tone.","R5: The six voices must take and hold that common tone as one steady unison; leaning, ornament, or private improvement invalidates it.","R6: After the common tone comes a measured silence, and only afterward do the six diverge/scatter into distinct, wide notes.","R7: Non-core surface variation is allowed; alteration of the sixfold identity, common tone, silence/scatter, or keyed rhyme makes a false version or broken gate.","R8: Correct performance does not require possession of the key or understanding of meaning.","R9: The verse is spec-like or self-describing, silently encoding its own copying, gating, silence/scatter, and reading.","R10: The copying/performance/audit is ritually periodic and survives authors' deaths across generations.","R11: An explicit standing-wave gate or threshold passes/certifies only when the sixfold tone or agreement stands steady and flat.","R12: Rhymed line-endings are keyed pairs; altering one member can loosen or damage its mate."],"voices":{"V1":["P01","P02","P05","P07"],"V2":["P03","P09"],"V3":["P04","P08","P10"],"V4":["P06","P11","P12"]},"lenses":[{"label":"Rule-following, use, and forms of life","thinker_guess":"Ludwig Wittgenstein / Pierre Bourdieu","ids":["P02","P04","P09","P11"]},{"label":"Ritual embodiment and dwelling","thinker_guess":"Martin Heidegger / Maurice Merleau-Ponty","ids":["P01","P03","P06","P11"]},{"label":"Cybernetic thresholds and standing-wave systems","thinker_guess":"Norbert Wiener / W. Ross Ashby","ids":["P04","P05","P07","P08","P10","P12"]},{"label":"Institutional archive, discipline, and audit","thinker_guess":"Michel Foucault / Franz Kafka","ids":["P05","P09","P10","P12"]},{"label":"Textual transmission, commentary, and philology","thinker_guess":"Jorge Luis Borges / Michel de Certeau","ids":["P02","P05","P06","P07","P12"]},{"label":"Pragmatist/Emersonian exhortation and anti-idolatry","thinker_guess":"Ralph Waldo Emerson / Friedrich Nietzsche","ids":["P04","P07","P08"]}]}
```

## RAW rib_renderman_mapping

I treat the repeated motifs as encoded rules, labeled BR1–BR9. Citations are by parable ID.

## 1. BASE RULES

Ordered by count descending. BR1–BR8 are common to ALL 12 unless noted; BR9 is frequent but not universal.

1. **BR1 — Compact-description-over-object (ALL, 12):** A scene/work is serialized as light instructions or compressed marks and rendered/expanded only where transport or production is cheap; the heavy artifact never crosses the expensive boundary. IDs: P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12.
2. **BR2 — Six-line normalized record (ALL, 12):** Findings/claims/memory entries use exactly six lines/slots: number, assertion, reuse/stake/license, falsifier/test, provenance/where, warrant/who/day/cost. IDs: P01–P12.
3. **BR3 — Schema interoperability with memory (ALL, 12):** Incoming field records share the institutional memory schema so they can be filed/read without translation; malformed or extra-line records are refused. IDs: P01–P12.
4. **BR4 — Explicit falsifier/breaker required (ALL, 12):** Every claim must carry the test/stone/question that would break or kill it; a record lacking its falsifier is invalid. IDs: P01–P12.
5. **BR5 — Remote/lazy resource catalog (ALL, 12):** A catalog gives location, invocation/summoning, and validation test for distant forges/engines/masters/chests; heavy resources stay remote until a named job calls for them—no speculative hauling. IDs: P01–P12.
6. **BR6 — Proposed vs enacted / unsealed status (ALL, 12):** Stencils, tubes, boxes, cards, catalogs, rehearsals, bells, trays, and plans may exist fully formed but unconnected, unsworn, or unflown; execution ratifies. IDs: P01–P12.
7. **BR7 — Canonical ancestor lineage (ALL, 12):** The method is authorized by three/four ancestral portraits or bequests: scene-description/RIB-like grammar, distance/signed-distance measurement, and shortest-path/self-stabilizing or neighbor-only walker; sometimes an added smoothing/lighting/curve ancestor. IDs: P01–P12.
8. **BR8 — Cost-governed dual representation (ALL, 12):** Tight/closed/compressed form belongs on the dear, cold, slow, or tolled side; wide/open/expanded form belongs where paper, compute, space, or copying is cheap. IDs: P01–P12.
9. **BR9 — Narrow-schema selection and exclusion (7, frequent not all):** The six-slot format selects for assertions that fit and can be broken; uncertainty, narrative surplus, or “seventh-line” truths are rejected, omitted, or driven to side channels. IDs: P05, P06, P07, P08, P10, P11, P12.

## 2. PER-PARABLE

- **P01** — Trade house abandons weight-freight for folded cards; encodes BR1–BR8: law “carry the fold, not cloth,” six-line rider reports, far-forge cabinet, unsealed bell/boxes, three portraits. Rare: a true thing may exist without being in force (P01).
- **P02** — Ridge house uses distance strings, thinned frontier messages, six-line memory, and remote forge catalog; encodes BR1–BR8. Rare/mixed: Marta verifies a forge is a ruin yet the summoned fire still works; truest row is ignored; catalog “proposed; seal not set” (P02).
- **P03** — Lantern Works: blind caster and measurer; encodes BR1–BR8; green book governs remote oxen. Rare: rules grow from unstated wants; four frames but “speak of three”; seventeen-mark seal (P03).
- **P04** — Picture-writers’ city with chalk catalog and disconnected slip box; encodes BR1–BR8; BR9 implicit. Rare: pragmatist demand “show me one slip”; what is done shows in any light; eight strange signs (P04).
- **P05** — Véra studies harbor picture-writers; encodes BR1–BR8 and BR9. Rare: explicit exclusion of not-knowing from six-line trade; “three portraits” then a fourth figure; catalog is a petition (P05).
- **P06** — First-person ex-marketer analyzes the house’s incentives; encodes BR1–BR8 and BR9. Rare: overt “who gains” critique; seventh-line truths are never written; card tube unstrung (P06).
- **P07** — Ilse learns tight rows, six-column memory, and gray catalog; encodes BR1–BR8 and BR9. Rare: status marks “seen, quarreled, not yet”; tight format drifts into cheap valley without decree; seventeen-tooth stamp (P07).
- **P08** — Tilde at house with unread scroll and dune of unfiled tales; encodes BR1–BR8 and BR9. Rare: physical dune of narrative surplus; unplayed instrument hears no contradiction; blue-book ribbon unsealed (P08).
- **P09** — Salt harbor: same folded strip read as festival and indictment; encodes BR1–BR8. Rare: semantic plurality/underdetermination of compact scene; four dead masters; new slip drawer shut (P09).
- **P10** — Counselor tests deterministic ribbon-press and provenance; encodes BR1–BR8 and BR9. Rare: same ribbon gives same picture; picture without ribbon is rumor; narrow margin vs full wide page; dusty six-line cards (P10).
- **P11** — Six-Line Country: Ilse carries slips and papers wide sheets in kitchen corridor; encodes BR1–BR8 and BR9. Rare: metric selection makes canyon become gorge; wide paper finds more errors; trays chalk/unsigned catalog (P11).
- **P12** — Marthe observes rehearsal slips becoming false institutional memory; encodes BR1–BR8 and BR9. Rare: “as we sent last week” said though nothing sent; tongues cross pass before bodies; wafer “believed not sworn” (P12).

## 3. STATUS SPLITS

- **BR1/BR8 compact-transfer rule:** Settled/in force in all IDs: P01–P12. No parable doubts the compact-transfer rule itself; several (P05, P06, P08, P12) instead doubt whether the expanded/wide side will be used.
- **BR2/BR3/BR4 six-line memory schema:** Settled as memory format in P01–P12. The field/finding pipeline is settled/in use in P01, P03, P09, P11. It is doubtful, unconnected, unsealed, or merely rehearsed in P02, P04, P05, P06, P07, P08, P10, P12. P09 is mixed: existing scout slips work, but the new slip drawer is shut.
- **BR5 remote-resource catalog:** Mostly operative or explicitly unsworn. Clearly settled/working in P03. Mixed/operative-but-unsworn in P02. Doubtful, chalk, petitionary, ribboned, unsigned, or white-pebble-proposed in P01, P04, P05, P06, P07, P08, P09, P10, P11, P12.
- **BR6 proposed-vs-enacted:** Every ID contains both settled practice and unratified apparatus: P01 bell/boxes; P02 slip box; P03 hive; P04 jar/box; P05 fresh-carved custom; P06 unstrung tube; P07 hung stencil; P08 unread scroll; P09 new slips; P10 dusty cards; P11 chalk trays/unsigned catalog; P12 rehearsal slips vs old-style post.
- **BR9 selection/exclusion:** Treated as a settled consequence in P06 and P11; as a feared/doubtful cost in P05, P08, P12; as a structural trade-off visible in P07 and P10.

## 4. GROUPINGS BY LENS

- **Material semiotics / immutable mobiles:** P01 — evokes Bruno Latour.
- **Institutional archive, power/knowledge, and unread law:** P02, P08 — evokes Michel Foucault, with P08 also Kafka-adjacent.
- **Will-to-power and value-created rules:** P03 — evokes Friedrich Nietzsche.
- **Pragmatic fallibilism: truth tested by action or breakage:** P04, P10 — evokes Charles Sanders Peirce.
- **Field, doxa, and symbolic exclusion:** P05 — evokes Pierre Bourdieu.
- **Ideology/incentive critique:** P06 — evokes Karl Marx.
- **Tacit knowledge and practice:** P07 — evokes Michael Polanyi.
- **Semiotics and plural reading:** P09 — evokes Roland Barthes.
- **Legibility, standardization, and metric selection:** P11 — evokes James C. Scott.
- **Performativity and institutional memory:** P12 — evokes J. L. Austin.

## 5. GROUPINGS BY VOICE

I infer **five authorial voices**:

- **V1: Ornate archival-fabulist voice.** Long, period-heavy sentences; institutional irony; exact catalogs; named characters embedded in formal allegory. Members: **P01, P02, P08, P12**.
- **V2: Close-third workshop/arrival voice.** Named female protagonist arrives, learns an unstated practice, and ends with a restrained aphoristic insight. Members: **P03, P07**.
- **V3: Dialogic demonstrative-fable voice.** Medium-length, explicit embedded argument, tests or staged encounters, more direct moral demonstration. Members: **P04, P09, P10**.
- **V4: Analytical ethnographic/sociological voice.** Status-tracking, social effects of schema, expository travelogue or case study. Members: **P05, P11**.
- **V5: First-person cynical memoir/polemic voice.** Market/incentive idiom; “I” narration; direct ideological critique. Member: **P06**.

## 6. OUTLIERS AND LEAKAGE

- **P06** is the strongest voice outlier: the only first-person marketing/polemic narration (P06).
- **P09** is the clearest semantic outlier: one compact strip supports multiple incompatible readings, making the mapping underdetermined (P09).
- **P05** uniquely states that “not-knowing” has no slot in the six-line record, so uncertainty cannot be traded or kept (P05).
- **P11** uniquely shows the wide/expanded form as an error-finding side channel; its six-line metric trains finders to find only what fits (P11).
- **P12** uniquely dramatizes rehearsal becoming false memory: “as we sent last week” is said though nothing was sent (P12).
- **Likely hidden-roster/spec leakage:** repeated ancestor dates/roles **1974, 1988, 2013** and scene-description/distance/path triad appear across P02, P03, P05, P08, P11, P12. Exact counts such as **seventeen** marks/teeth in P03/P07 and **eight** strange signs in P04 look like leaked key/roster details. P03 says four frames but “speak of three,” and P05 says three portraits then lists a fourth figure. P07 and P11 both use the name **Ilse**, suggesting shared draft/roster leakage. P10’s “ribbon” and deterministic press most directly telegraph the RIB/RenderMan-like mapping theme.

```json
{"base_rules":["BR1 (12/12 ALL): Serialize/render compact descriptions; do not carry heavy artifacts across costly boundaries; expand where cheap. IDs P01-P12.","BR2 (12/12 ALL): Use a fixed six-line/six-slot record: number, assertion, reuse/stake/license, falsifier/test, provenance/where, warrant/who/day/cost. IDs P01-P12.","BR3 (12/12 ALL): Field records share the institutional memory schema and can be filed without translation; malformed or extra-line records are refused. IDs P01-P12.","BR4 (12/12 ALL): Every claim must carry an explicit falsifier, breaker, or test that would kill it. IDs P01-P12.","BR5 (12/12 ALL): Maintain a remote-resource catalog with location, summon/invocation, and validation test; keep heavy resources remote until a named job needs them. IDs P01-P12.","BR6 (12/12 ALL): Distinguish proposed/unsealed/unconnected apparatus from enacted/ratified practice; execution ratifies. IDs P01-P12.","BR7 (12/12 ALL): Authorize the method through a canonical lineage of three/four ancestor figures: scene-description grammar, distance/signed-distance measurement, and shortest-path or neighbor-only/self-stabilizing walker; sometimes additional curve/lighting/smoothing roles. IDs P01-P12.","BR8 (12/12 ALL): Use dual representation governed by cost: tight/closed/compressed at the dear or tolled boundary; wide/open/expanded where paper, compute, or space is cheap. IDs P01-P12.","BR9 (7/12): The narrow six-slot schema selects for claims that fit and can be broken, excluding uncertainty, narrative surplus, or seventh-line truths. IDs P05, P06, P07, P08, P10, P11, P12."],"voices":{"V1":["P01","P02","P08","P12"],"V2":["P03","P07"],"V3":["P04","P09","P10"],"V4":["P05","P11"],"V5":["P06"]},"lenses":[{"label":"Material semiotics and immutable mobiles","thinker_guess":"Bruno Latour","ids":["P01"]},{"label":"Institutional archive, power/knowledge, and unread law","thinker_guess":"Michel Foucault","ids":["P02","P08"]},{"label":"Will-to-power and value-created rules","thinker_guess":"Friedrich Nietzsche","ids":["P03"]},{"label":"Pragmatic fallibilism: truth tested by action or breakage","thinker_guess":"Charles Sanders Peirce","ids":["P04","P10"]},{"label":"Field, doxa, and symbolic exclusion","thinker_guess":"Pierre Bourdieu","ids":["P05"]},{"label":"Ideology and incentive critique of knowledge production","thinker_guess":"Karl Marx","ids":["P06"]},{"label":"Tacit knowledge and practice","thinker_guess":"Michael Polanyi","ids":["P07"]},{"label":"Semiotics and plural reading of a text","thinker_guess":"Roland Barthes","ids":["P09"]},{"label":"Legibility, standardization, and metric selection","thinker_guess":"James C. Scott","ids":["P11"]},{"label":"Performativity and collective institutional memory","thinker_guess":"J. L. Austin","ids":["P12"]}]}
```

## RAW dirac_loops

## 0. Hidden-spec summary

The parables converge on a single graph-like object and a ritual around it: **33 nodes/vertices**, **21 edges/spans/planks/threads**, **20 connected components**, and therefore **8 independent cycles/loops** by cyclomatic rank  
\[
\beta=E-V+C=21-33+20=8.
\]
Six of the eight loops are the operative “broken/owing/missing-span” loops; the remaining two are unfound, inaccessible, self-referential, whole-but-unwalked, or otherwise exceptional. A “round” is a closed non-retracing walk, read only on return by a marked staff/reed/pole/eye/token/word. Whole loops are settled and teach nothing new; broken loops mark missing spans to be closed. The record often counts itself, no one checks a reading twice, and the readings are rarely used by outsiders.

---

## 1. BASE RULES

Ordered by count descending. Ties are grouped.

| # | Normalized rule / invariant | IDs encoding it | Count | Common? |
|---|---|---|---:|---|
| R1 | The object has **33 vertices/nodes, 21 edges/spans, and 20 connected components**, yielding **8 independent cycles** by \(E-V+C\). | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R2 | A **round/ring/circuit/return** is a closed walk from a node back to the same node without retracing a plank/edge; only non-composite/independent cycles count. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R3 | The loop is read at return by an oriented mark or instrument—reed shadow, wand, staff lean, pole eye, token face, word/fare, turnaround—and that returned turn is the loop’s answer. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R4 | Whole/settled loops are already held, old, or teach nothing; broken/notched/owing loops name a **missing span** which is a debt/errand/promise to be closed. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R5 | The official/operative count reports **eight loops, six of them broken/owing/missing**; the other two are unfound, inaccessible, whole-but-unwalked, or self-referential. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R6 | The counting/recording method is **self-included**: count-of-count, a peg for the peg-count, the map-room in the map, Ove’s gate on the round, the warden’s knot about the board, etc. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R7 | Written records are catastrophically destroyed—by fire, water, or pulping—but the method survives in **oral recitation/chants/kitchen telling**, sometimes bent. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R8 | **No second/independent walk** checks a reading; no one follows behind the walker to see whether the same turn returns. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R9 | Readings/tokens/stones/fares are **not used downstream**: they are shelved, dusted, admired, or ignored; no barge, mason, court, buyer, or field decision consumes them. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R10 | A missing span is properly closed by **collective/public repair**—planks, bricklayers, masons, all-hands bell—not by solo unknotting or private guesswork; institutions often defer this. | P01, P02, P03, P04, P05, P06, P07, P08, P09, P10, P11, P12 | 12 | ALL |
| R11 | More or less explicit arithmetic derivation of the eight from 33, 21, and 20, rather than mere repetition of the tally. | P05, P06, P07, P08, P10, P12 | 6 | common but not universal |
| R12 | One reading can be **heard differently by different parties**—fare, commission, echo, promise, lie—showing underdetermined interpretation. | P08, P11, P12 | 3 | rare but salient |

---

## 2. PER-PARABLE

- **P01** — Fen toll-house and Ines’s reed; encodes the 33/21/20/8 tally, reed-shadow return reading, turned reed as missing crossing, tally counting itself, oral chant after fire, and no second walker; unique: the first walker’s name survives only inside the chant, and collective chanting causes planks to be laid without a summons.
- **P02** — First-person listener in the fen; six missing spans and a bell custom; encodes independent rounds, wand reading, whole rounds resting, six wanting a span, counting-house standing on its own floor, oral song survival, and no external answerer; unique: the narrator takes the other end of the bell rope and helps lay one plank.
- **P03** — Anke in the string hall; smooth/notched stones and notched gaps; encodes 33/21/20/8, non-composite rings, notch as true absence, count-of-count, unused shelf, and no second walk; unique: one smooth stone is delivered to a widow, and Anke refuses to shelve the count-of-count stones.
- **P04** — Cellar of hanged knots and the apprentice walker; encodes cords/returns, iron rings as settled, eight circles versus keeper’s six, the self-finding hoop, unused bowl and chair, and oral survival; unique: the apprentice removes a gap-board, cuts a cord but does not lay the span, and the keeper stops counting at seven.
- **P05** — Salt-fen Order of the Staff; doctrine of rounds, staff lean, settled versus broken spans; encodes counts, non-composite rounds, founder’s round as “measuring walking,” missing second-order walker and missing use, oral survey excluded from written rolls; unique: the foundational round itself contains two gaps—verification and application.
- **P06** — Marthe maps the guild town on copper; encodes 33/21/20/8, six broken circles, one self-referential circle through the map-room, one locked-courtyard exception, and unopened readings; unique: Marthe scrapes the map-room dot, moves the table to the margin, and stakes broken spans with red rags.
- **P07** — Salt standings with Alba and the tally-keeper; teacher’s two hands distinguish settled returns from broken returns; encodes counts, independent returns, six broken, two unfound, no proof of finished stretches, no outside buyer, oral craft, and a self-referential plan of rounds; unique: Pello the crier sells the easy “eight” while the barge later goes out with planks.
- **P08** — Chinese aphoristic parable of Ilma and the lantern; encodes 33 stones/21 planks/20 stands/8 rings, six drawn paths missing a final span, the counting-wheel shelf as a self-loop, untested wheel, oral law, and misused counts; unique: explicit daylight/lantern moral, “admirers” versus “walkers,” and deliberately unfinished promises.
- **P09** — Fog-lagoon wardens Jonas and Petra; tower reveals six breaches and two unwalked whole rounds; encodes counts, eye-pole reading, no round written twice, counting-house as one of the 33, oral chart, and count-of-count; unique: Petra re-inks breaches, thresholds, and a second-walker plan; one round is written twice by first frost.
- **P10** — Fen country under roadwright Ove; tokens and missing stretches; encodes tokens as loop returns, six break-names, masons/walkers’ interests, no assayer, oral wool-carding survival, and Ove’s own gate on the eighth round; unique: economic-interest analysis and the private plank over Ove’s own unmentioned break.
- **P11** — Salt Harrow and tally-keeper Oren; one word “elm-crossing” heard as misdelivery, commission, and echo; encodes six owing rounds, none settled, tally room as thirty-third stone, no second walks, and unused loft fares; unique: three incompatible hearings of one reading and an external skeptical seed-trader.
- **P12** — Odile audits the dyers’ string room; encodes knots/threads/circuits, explicit \(21-33+20=8\), six red-bead broken circuits, two undrawn circuits, warden’s self-knot, missing second walks, and unused readings; unique: professional audit, request for blind side-by-side re-walkings, and “bring me the staff, not the story.”

---

## 3. STATUS SPLITS

The same rule appears under different epistemic statuses.

| Claim / rule | Held as settled, received, or operative | Doubted, audited, corrected, or evaded |
|---|---|---|
| The official 33/21/20/8/6 tally is authoritative | P02, P03, P05, P07, P09, P11 | P04 (keeper says six; apprentice finds eight), P06 (count is accurate but no whole circle is walkable), P08 (wheel/count never tested), P10 (Ove’s arithmetic serves his trade), P12 (Odile recomputes eight against the warden’s six); P01 mixed: tally is self-referential and unchecked |
| A returned reading is a valid answer from the loop | P02, P03, P05, P07, P09, P12 | P04 (bowl never tasted; no validation), P06 (book of readings unopened), P08 (counts ignored; wheel untested), P10 (no assayer), P11 (word heard three ways); P01 mixed: turns are read but never repeated |
| Oral transmission preserves the rule after written loss | P01, P03, P05, P07, P09, P12 | P02, P04, P06, P08, P10, P11 acknowledge oral survival but stress alteration, versions, or non-admissibility |
| The six broken spans are real obligations to be closed | Doctrinally settled and/or acted on: P02, P03, P06, P09, P12 | Deferred or ignored: P01 (until the final chant), P04 (gaps displayed as “openness”), P05 (slates go into the drawer), P07 (before the barge), P08 (promises left deliberately unfinished), P10 (Ove hides his own break), P11 (owing fares lofted); P11’s trader even doubts the reading is a fare at all |

---

## 4. GROUPINGS BY LENS

- **P01** — Practice/tacit-knowledge lens: meaning lives in the walk, chant, and guild habit rather than in the burned charter. Best guess: **Ludwig Wittgenstein**.
- **P02** — Interpretive anthropology / thick-description lens: a first-person listener records what the town’s hands do twice. Best guess: **Clifford Geertz**.
- **P03** — Existentialist ethical witness / small revolt against inevitability. Best guess: **Albert Camus**.
- **P04** — Psychoanalytic archaeology of the house, repression, uncanny objects, and a keeper who denies the eighth circle. Best guess: **Sigmund Freud**.
- **P05** — Legal positivism and rule-of-recognition lens: written rolls, officials, valid staffs, and the oral founder excluded by formal rules. Best guess: **H. L. A. Hart**.
- **P06** — Map-versus-territory operationalism: a drawn circle is either a promise of a street or a lie about one. Best guess: **Alfred Korzybski**.
- **P07** — Pragmatist inquiry/education lens: the truth lives in the coming-back and in public consequences, not the crier’s easy “eight.” Best guess: **John Dewey**.
- **P08** — Cynic enlightenment aphorism: lantern at noon, mud jar, admirers versus walkers. Best guess: **Diogenes**.
- **P09** — Platonic cave/clear-sight lens: fog below, tower above, the whole seen at once, then a return to fix the town. Best guess: **Plato**.
- **P10** — Historical-materialist ideology critique: tokens, wages, masons, walkers’ itch, and the roadwright’s hidden self-break. Best guess: **Karl Marx**.
- **P11** — Hermeneutics of suspicion: one word heard as misdelivery, commission, and echo. Best guess: **Paul Ricoeur**.
- **P12** — Falsification/replication audit: second walks, blind comparison, strangers judging which reading belongs to which circuit. Best guess: **Karl Popper**.

---

## 5. GROUPINGS BY VOICE

Six authorial voices fit the prose habits best.

- **V1 — Archaic fen/causeway fable voice.** Long rhythmic institutional fables, salt/fen settings, tallymen or tally-keepers, grandmothers, oral chant, planks/stones/rounds, named simple protagonists. Members: **P01, P05, P07, P10, P11**.
- **V2 — First-person field-observer voice.** Quiet ethnographer/listener, first person, explicit trade, personal intervention at the end. Member: **P02**.
- **V3 — Knot/string audit-hall voice.** Named female examiner, exact counts, shelves/tablets, notched or red-bead circuits, count-of-count, no second walks. Members: **P03, P12**.
- **V4 — Symbolic uncanny-cellar voice.** No named protagonist, dense recurring objects—bowl, chair, hoop, lamp—dreamlike and compressed. Member: **P04**.
- **V5 — Civic survey / map-versus-town voice.** Named mapmaker or warden, guild/reeve/officials, copper plate or chart/tower, concrete reform at the end. Members: **P06, P09**.
- **V6 — Non-English aphoristic Cynic voice.** Chinese text, short sections, direct moral challenge, lantern/daylight and admirer/walker contrast. Member: **P08**.

---

## 6. OUTLIERS AND LEAKAGE

- **P02** is the clear voice outlier: the only first-person narrator, and the only one who joins the ritual rather than merely observing or auditing it.
- **P08** is the strongest surface outlier: the only non-English parable and the most aphoristic. It also exposes the hidden moral most directly: a loop needs walkers, not admirers; a count must be tested rather than displayed.
- **P04** is the most surreal and least civic: the bowl, chair, hoop, and keeper’s refusal of the eighth circle make it unusually symbolic. It is also unusually explicit that the official six and the actual eight diverge.
- **P12** is the most technical leakage of the hidden spec: it states the cyclomatic formula almost outright—“threads, less knots, plus thickets”—and proposes blind second readings as a falsification test.
- **P03** contains the visible redaction “The String [-],” the clearest artifact of missing key/roster information.
- Across all parables, the recurring **self-reference** is the strongest spec leak: the counting house on its own floor (P02, P09, P10, P11), the count-of-count (P01, P03, P09, P12), the self-finding hoop (P04), the map-room circle (P06), the founder’s round measuring walking (P05), the wheel’s own stand/loop (P08), and the warden’s own knot (P12).
- The “six broken spans” is repeatedly mapped to the missing **second walk** and missing **external use** of readings: P05 is the most explicit, but P03, P06, P07, P08, P10, P11, and P12 all show that the unverified/unused reading is the real open loop.

```json
{"base_rules":["Dirac-loop substrate: 33 vertices, 21 edges, 20 connected components, hence eight independent cycles by E-V+C.","A round is a non-retracing closed walk from a vertex back to itself; only non-composite/independent cycles count.","At return, an oriented mark or instrument is read; the returned turn/word/token is the loop invariant.","Whole/settled loops are already held and teach nothing; broken/notched/owing loops mark missing spans as debts or errands to close.","The operative count has eight loops, six explicitly broken/owing/missing, and two exceptional or unexamined loops.","The count/method includes itself: count-of-count, map-room, threshold, warden's knot, Ove's gate, and similar self-loops.","Written records are destroyed, but the rule survives orally in chant, recitation, or kitchen telling, often altered.","No second or independent walk verifies a reading; no one follows behind the first walker.","Readings are not consumed downstream; they are shelved, dusted, admired, or ignored by outside users.","Missing spans require collective public repair, though institutions often defer it.","The 33/21/20/8 result is sometimes derived explicitly by arithmetic rather than merely recited.","One reading may be heard differently as fare, commission, echo, promise, or lie."],"voices":{"V1":["P01","P05","P07","P10","P11"],"V2":["P02"],"V3":["P03","P12"],"V4":["P04"],"V5":["P06","P09"],"V6":["P08"]},"lenses":[{"label":"Wittgensteinian practice and tacit knowledge","thinker_guess":"Ludwig Wittgenstein","ids":["P01"]},{"label":"Interpretive anthropology and thick description","thinker_guess":"Clifford Geertz","ids":["P02"]},{"label":"Existentialist ethical witness and small revolt","thinker_guess":"Albert Camus","ids":["P03"]},{"label":"Psychoanalytic archaeology of the uncanny and repressed","thinker_guess":"Sigmund Freud","ids":["P04"]},{"label":"Legal positivism and rule of recognition","thinker_guess":"H. L. A. Hart","ids":["P05"]},{"label":"Map-territory operationalism","thinker_guess":"Alfred Korzybski","ids":["P06"]},{"label":"Pragmatist inquiry and education","thinker_guess":"John Dewey","ids":["P07"]},{"label":"Cynic enlightenment aphorism","thinker_guess":"Diogenes","ids":["P08"]},{"label":"Platonic cave and clear sight","thinker_guess":"Plato","ids":["P09"]},{"label":"Historical-materialist ideology critique","thinker_guess":"Karl Marx","ids":["P10"]},{"label":"Hermeneutics of suspicion and differential readings","thinker_guess":"Paul Ricoeur","ids":["P11"]},{"label":"Falsification and replication audit","thinker_guess":"Karl Popper","ids":["P12"]}]}
```

# PASS 2: NAMED ROSTER (blind_roster.py; same anonymization+shuffle as pass 1 via blind_full.build; judge given 12 lens names + one neutral line each, must assign one lens per parable, <=ceil(n/12) uses per lens)

## Side by side: pass 1 (blind) vs pass 2 (named roster)

| Subject | P1 lens recovery (groups; per-parable) | P1 voice pairwise | P2 exact lens acc | P2 by writer | P2 Hall/Wallas | P2 voice pairwise | P2 roster use | P2 served | P2 HTTP |
|---|---|---|---|---|---|---|---|---|---|
| who_we_are | 7/12 (par 9/24) | 0.656 | 22/24 (92%) | MAX 11/12; Gemini 11/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 0.764 | unused: -; over: - | deepseek-flash | 1 |
| what_we_are | 8/12 (par 11/24) | 0.732 | 20/24 (83%) | MAX 9/12; Gemini 11/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 0.699 | unused: -; over: - | deepseek-flash | 1 |
| the_invariants | 7/12 (par 11/24) | 0.678 | 22/24 (92%) | MAX 11/12; Gemini 11/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 0.663 | unused: -; over: - | deepseek-flash | 1 |
| standing_wave_gate | 3/12 (par 4/24) | 0.699 | 24/24 (100%) | MAX 12/12; Gemini 12/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 1.000 | unused: -; over: - | deepseek-flash | 1 |
| parable_as_spec | 5/12 (par 6/24) | 0.609 | 24/24 (100%) | MAX 12/12; Gemini 12/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 1.000 | unused: -; over: - | deepseek-flash | 1 |
| six_lane_run | 8/12 (par 8/24) | 0.670 | 24/24 (100%) | MAX 12/12; Gemini 12/12 | hall/Gemini:hit; hall/MAX:hit; wallas/Gemini:hit; wallas/MAX:hit | 0.562 | unused: -; over: - | deepseek-flash | 1 |
| water_governor | 3/12 (par 3/19) | 0.643 | 13/19 (68%) | MAX 6/12; Gemini 7/7 | hall/Gemini:hit; hall/MAX:hit; wallas/MAX:miss->freud | 0.719 | unused: -; over: - | deepseek-flash | 1 |
| the_congress | 3/12 (par 3/12) | 0.288 | 8/12 (67%) | MAX 8/12 | hall/MAX:hit; wallas/MAX:hit | 0.152 | unused: -; over: - | deepseek-flash | 1 |
| moto_cron | 0/12 (par 0/13) | 0.436 | 10/13 (77%) | MAX 10/12; Gemini 0/1 | hall/MAX:hit; wallas/MAX:hit | 0.346 | unused: -; over: - | deepseek-flash | 1 |
| keyed_verse | 1/12 (par 1/12) | 0.197 | 12/12 (100%) | MAX 12/12 | hall/MAX:hit; wallas/MAX:hit | 0.197 | unused: -; over: - | deepseek-flash | 1 |
| rib_renderman_mapping | 0/12 (par 0/12) | 0.167 | 12/12 (100%) | MAX 12/12 | hall/MAX:hit; wallas/MAX:hit | 0.106 | unused: -; over: - | deepseek-flash | 1 |
| dirac_loops | 2/12 (par 2/12) | 0.182 | 12/12 (100%) | MAX 12/12 | hall/MAX:hit; wallas/MAX:hit | 0.091 | unused: -; over: - | deepseek-flash | 1 |

**P2 overall exact lens accuracy: 203/224 (90.6%)**; MAX 127/144, Gemini 76/80. Chance with 12 lenses ~8.3%. Served models: {'deepseek-flash': 12}. DeepSeek HTTP attempts: 12.

**Do Hall and Wallas appear correctly on all subjects? NO.** Hall hits 19/19, Wallas hits 17/18. Misses: water_governor wallas/MAX P09 -> freud (conf 0.55)

## 12x12 confusion matrix (rows = true lens, cols = judged; all writers, all subjects)

| true \ judged | diogenes | fermat | foucault | plato_kirk | baudrillard | bernays | ellul | freud | hall | jung | mcluhan | wallas | other | recall |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **diogenes** | **18** |  |  |  |  |  |  |  |  |  |  |  |  | 18/18 |
| **fermat** |  | **19** |  |  |  |  |  |  |  |  |  |  |  | 19/19 |
| **foucault** |  |  | **19** |  |  |  |  |  |  |  |  |  |  | 19/19 |
| **plato_kirk** |  |  |  | **17** |  |  |  |  |  |  |  | 1 |  | 17/18 |
| **baudrillard** |  |  |  |  | **17** |  |  |  |  |  | 1 |  |  | 17/18 |
| **bernays** |  |  |  |  | 1 | **17** |  |  |  |  | 1 |  |  | 17/19 |
| **ellul** |  |  |  |  |  |  | **16** | 1 |  | 1 | 1 |  |  | 16/19 |
| **freud** |  |  | 1 | 1 |  |  |  | **14** |  | 2 |  |  |  | 14/18 |
| **hall** |  |  |  |  |  |  |  |  | **19** |  |  |  |  | 19/19 |
| **jung** |  |  |  |  |  | 1 | 1 | 3 |  | **14** |  |  |  | 14/19 |
| **mcluhan** |  |  |  |  | 1 |  | 2 |  |  | 1 | **16** |  |  | 16/20 |
| **wallas** |  |  |  |  |  |  |  | 1 |  |  |  | **17** |  | 17/18 |
| precision | 18/18 | 19/19 | 19/20 | 17/18 | 17/19 | 17/18 | 16/19 | 14/19 | 19/19 | 14/18 | 16/19 | 17/18 | | |

## Lens x subject cells (correct/total, all writers)

| lens | who_we_are | what_we_are | the_invariants | standing_wave_gate | parable_as_spec | six_lane_run | water_governor | the_congress | moto_cron | keyed_verse | rib_renderman_mapping | dirac_loops | total |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| diogenes | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 18/18 |
| fermat | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 19/19 |
| foucault | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 19/19 |
| plato_kirk | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 17/18 |
| baudrillard | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 17/18 |
| bernays | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 17/19 |
| ellul | 2/2 | 1/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 16/19 |
| freud | 1/2 | 1/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/1 | 1/1 | 0/1 | 1/1 | 1/1 | 1/1 | 14/18 |
| hall | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 19/19 |
| jung | 1/2 | 0/2 | 2/2 | 2/2 | 2/2 | 2/2 | 1/2 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 14/19 |
| mcluhan | 2/2 | 2/2 | 1/2 | 2/2 | 2/2 | 2/2 | 1/2 | 0/1 | 1/2 | 1/1 | 1/1 | 1/1 | 16/20 |
| wallas | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 2/2 | 0/1 | 1/1 | 1/1 | 1/1 | 1/1 | 1/1 | 17/18 |

## Calibration (judge confidence vs correctness)

| conf bin | n | correct | acc | MAX acc | Gemini acc |
|---|---|---|---|---|---|
| [0.00,0.30) | 0 | 0 | - | - | - |
| [0.30,0.50) | 2 | 2 | 100% | 2/2 | - |
| [0.50,0.70) | 28 | 16 | 57% | 14/25 | 2/3 |
| [0.70,0.85) | 42 | 37 | 88% | 32/37 | 5/5 |
| [0.85,1.00) | 152 | 148 | 97% | 79/80 | 69/72 |

Mean confidence when correct 0.868 vs wrong 0.692 (n=224 with numeric confidence).

# Analysis for Mag (builds on pass 1; every number below comes from the pass 2 tables above or from pass 1's table)

## 0. Read this before trusting the 90.6%
- Pass 2 is a **matching task, not open recovery**. The judge got the 12 keys and a cap of ceil(n/12) uses per lens. On the four 12-parable single-writer subjects (the_congress, keyed_verse, rib_renderman_mapping, dirac_loops) that makes it a forced permutation: elimination helps, and one confident swap costs 2 errors (the_congress lost 4 = two swaps). Pass 1 and pass 2 numbers are different measurements, not before/after.
- The served model was `deepseek-flash` on all 12 calls again, even though `deepseek-reasoner` + thinking was requested (pass 1 had the same problem). The returned usage shows reasoning tokens (e.g. who_we_are: 32593 reasoning of 34393 completion), so thinking ran, but on the flash tier.
- **Pass 1's scorer partly explains why Hall and Wallas were 0.** Its keyword list for `wallas` was `incubation / illumination / creative process / stages of thought`, which is Graham Wallas's *Art of Thought*. The repo's Wallas chair (docs/ref/ractors/RACTORS.md) is "desire as motive power", the *Human Nature in Politics* / *Great Society* Wallas. So a pass-1 group the judge labelled "desire" could never have scored. `hall` had the same exposure: a judge that described "audience decoding" without naming Hall could still miss, depending on the keywords. Pass 2 shows the signal is present in the text: Hall was 19/19 and Wallas was 17/18 once the judge had the names.

## 1. Reliable vs failing lens x subject cells
- **Reliable, 100% everywhere:** diogenes 18/18, fermat 19/19, foucault 19/19, hall 19/19. Wallas 17/18 and plato_kirk 17/18 each failed in only one cell, water_governor (MAX).
- **Failing cells (any miss):** water_governor had 6 failing cells (plato_kirk, freud, wallas at 0/1; bernays, jung, mcluhan at 1/2). The_congress had 4 (baudrillard, bernays, jung, mcluhan). What_we_are had 3 (jung 0/2, ellul 1/2, freud 1/2), and moto_cron 3 (ellul, freud, mcluhan 1/2). Who_we_are (freud, jung) and the_invariants (ellul, mcluhan) each had 2.
- **Weakest lenses by recall:** jung 14/19, freud 14/18, ellul 16/19, mcluhan 16/20. Freud is also the least precise (14/19): it soaks up jung, ellul and wallas.

## 2. What kind of failure is it (judged from the cue evidence)
- **Lens-signal problem: the main cause, and it sits on the Jung/Freud border.** In 5 of the 21 errors a jung parable was read as freud or freud as jung. The cues show the text carrying the *other* thinker's mechanism. Jung parables (Gemini) were read as Freud with high confidence: "What their records refused to own had returned from the cellar as fate" (0.98) and "the unrecorded deed sinks into the cellar and returns as symptom and fate" (0.95). That is return-of-the-repressed, not shadow or archetype. The reverse case: "A house without grief, he wrote, is either cured or repressed" in a freud parable was read as jung (0.58). Ellul and McLuhan blur the same way. Ellul's "kept its days in cloth" was read as mcluhan, and McLuhan's "turned deliberation into reflex" (0.86) and "the ratchet locked against his wrist" were read as ellul. Both are told as stories about how a tool reshapes its users.
- **Subject problem: real for water_governor and the_congress, not for the technical subjects.** Pass 1 put the technical subjects at 0-2/12 (moto_cron 0, keyed_verse 1, rib 0, dirac 2). Pass 2 got 12/12 on keyed_verse, rib and dirac, and 10/13 on moto_cron. So the lens is in those texts, and the blind judge described the domain instead of naming the thinker. Treat that with caution because of the forced-permutation effect (§0). Water_governor is the one subject where the scarcity theme pulls lenses together. A plato_kirk parable was read as wallas: "more waiters than ladles, and everyone knew it, and waited anyway". A wallas parable was read as freud on weak cues: "Marren struck the hour all the same." (0.55).
- **Writer problem: present but secondary.** Gemini scored 76/80 (95%) and MAX 127/144 (88%). On the four subjects where both writers covered all 12 lenses with mostly clean scores (standing_wave_gate, parable_as_spec, six_lane_run, the_invariants), MAX made 1 error in 48. MAX's errors cluster in what_we_are (3), water_governor (6) and the_congress (4). Gemini's 4 errors: two jung parables read as freud (its jung writing leans Freudian), one mcluhan read as ellul, and the single moto_cron parable. MAX also wrote at least one parable in Chinese (what_we_are wallas, cue "他们都想要同样的东西…"). The judge still placed it, but it is a brief-compliance problem. Pass 1's gap (Gemini 48% vs MAX 14%) narrows sharply when the names are given. MAX's lenses are present but not *named-recognizable*, which suggests its parables bury the thinker's mechanism more deeply.

## 3. Calibration
The judge's confidence predicts correctness. At conf >= 0.85 it was 148/152 correct (97%). At 0.70-0.85 it was 37/42 (88%), and at 0.50-0.70 16/28 (57%). Mean confidence was 0.868 when right and 0.692 when wrong. The exceptions are the high-confidence Jung->Freud errors (0.98, 0.95, 0.86). Those are cases where the text really does carry the Freudian mechanism, not judge noise. **Practical rule:** treat a lens tag at >= 0.85 as trustworthy, and audit any tag under 0.70.
Only 2 parables got a "missing" note (the only two under 0.5): parable_as_spec MAX P20 (plato_kirk) needed "Stronger cave/shadow imagery or an explicit rewritten simulator/test", and six_lane_run MAX P13 (jung) needed "Explicit shadow/archetype language or a clearer figure of refusal/integration". Both were assigned correctly anyway.

## 4. Ranked actions for the parable briefs
1. **Jung brief: require a non-Freudian signature mechanism.** Ask for a shadow figure or double given a seat, a persona/mask, or an archetype recurring across cultures. Forbid "returns from the cellar / symptom / repeat" framing, which belongs to Freud. This is the largest single error source (5 of 21 errors are Jung<->Freud, 3 of them jung->freud).
2. **Freud brief: require the repetition-compulsion plus symptom mechanism explicitly** (the same act repeating, read as a symptom). Forbid grief/integration endings, which read as Jung.
3. **Separate Ellul and McLuhan.** Ellul's brief should state technique's *autonomy*: the method justifies itself and nobody chose the outcome. McLuhan's brief should state the *medium's sensory/structural effect independent of content*, and avoid ratchets or reflex machinery, which read as Ellul.
4. **water_governor and the_congress need a lens-first framing.** Open on the thinker's mechanism before the subject's scarcity or masks material, because there the subject imagery swamps the lens (10 of 21 errors are on these two subjects).
5. **Fix the scorer before trusting pass 1's lens numbers.** Change the `wallas` keywords to desire / human nature / great society / impulse, and add audience-reading terms to `hall`. As it stands, pass 1 under-counts both by design.
6. **MAX output checks:** enforce the output language (English) and make the lens mechanism concrete enough to name. Gemini's cues tend to state the mechanism ("decoded the same stroke of wood into loyalty, bargain, or refusal"), while MAX's hide it ("had never once heard the same play twice").
7. **Re-run on deepseek-reasoner proper** once the endpoint stops serving flash, to confirm these numbers are not a flash-tier artifact.

## 5. What the parables can be trusted for in Mag right now
- **Can be trusted for:** seat voices for diogenes, fermat, foucault and hall on every subject, and for wallas, plato_kirk, baudrillard and bernays everywhere except water_governor and the_congress. Given the roster, a reader can name the lens. They also work as spec carriers on the subjects that both writers covered cleanly (standing_wave_gate, parable_as_spec, six_lane_run: 24/24 each).
- **Not yet trusted for:** telling Jung from Freud, or Ellul from McLuhan, without the brief fixes above. Anything on water_governor or the_congress. Open-ended blind lens recovery (pass 1: 47/144 groups) with no roster supplied. MAX-authored voices on the technical subjects as *self-identifying* lenses, since they only resolve with the roster plus elimination. Voice/authorship separation: pass 2 voice pairwise scores were 0.091-0.346 on the single-writer subjects and 0.562-1.000 on mixed ones, so voice signal is real only when two writers are present.


# PASS 2 PER-SUBJECT DETAIL (judge cues verbatim)

## P2 who_we_are

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:31:22.758352-04:00 -> 2026-10-23T15:34:25.571150-04:00, usage={"prompt_tokens": 25869, "completion_tokens": 34393, "total_tokens": 60262, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 32593}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25869}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | baudrillard | Gemini | baudrillard | Y | 0.96 | "a chart of the third order generates its own coastline" / "signs circulate without referent and receipts certify only earlier receipts" |  |
| P02 | hall | Gemini | hall | Y | 0.98 | "read the anchor-stamps and single-line confessions just as the bailiff hoped" / "read the hollow circles in an opposite spirit" |  |
| P03 | mcluhan | Gemini | mcluhan | Y | 0.95 | "each remade the senses of whoever held it" / "amputated stillness and extended only the quick tongue" |  |
| P04 | jung | Gemini | freud | n | 0.98 | "What their records refused to own had returned from the cellar as fate" / "for the fifth winter running" |  |
| P05 | wallas | Gemini | wallas | Y | 0.97 | "ride the fixed desires already moving through the mill-race" / "what the millstead truly wanted" |  |
| P06 | wallas | MAX | wallas | Y | 0.62 | "The strong man wanted the water the way hungry men want bread" / "wanting the thing he had always wanted, which was to hear his name own the crossing" |  |
| P07 | plato_kirk | MAX | plato_kirk | Y | 0.96 | "shadows stepped out of the walls into the chairs" / "struck the storm out of the scene" |  |
| P08 | mcluhan | MAX | mcluhan | Y | 0.88 | "standing under the horn his sentences rounded themselves for many ears" / "What he came to trust most he had used least: the plain letter" |  |
| P09 | bernays | Gemini | bernays | Y | 0.99 | "pry open the clockwork of belief and name whose purse grows heavy" / "who gains when the household swallows this creed" |  |
| P10 | ellul | Gemini | ellul | Y | 0.98 | "had grown as all methods grow when left to themselves" / "machinery threatened to dictate when the river itself might flow" |  |
| P11 | fermat | MAX | fermat | Y | 0.98 | "the proof was too long for the margin" / "The margin had kept the man's claim exactly as it was made" |  |
| P12 | foucault | MAX | foucault | Y | 0.82 | "Every row ended with one of three marks" / "He was not called a liar; he was simply not the man of the row" |  |
| P13 | fermat | Gemini | fermat | Y | 0.99 | "a marvelous demonstration of the general power, which the margin was too small to contain" / "struck the hollow ring of the unexamined beside the master's own boast" |  |
| P14 | freud | Gemini | freud | Y | 0.98 | "the third identical mistake is a confession" / "what a household cannot bring itself to speak aloud it will perform with its elbows" |  |
| P15 | foucault | Gemini | foucault | Y | 0.97 | "render every fever legible" / "truth is not discovered in the air; it is manufactured at a porphyry table" |  |
| P16 | diogenes | MAX | diogenes | Y | 0.99 | "a barefoot man climbed the hill with a dog at his heel and a lit lantern in his hand" / "I am looking for who works here." |  |
| P17 | baudrillard | MAX | baudrillard | Y | 0.94 | "This Broker was the second of the name" / "It plays nothing. It is the most convincing thing in the room." |  |
| P18 | ellul | MAX | ellul | Y | 0.93 | "The gear worked so well that it wanted grain" / "the wheel was turning for the sake of its turning" |  |
| P19 | freud | MAX | jung | n | 0.58 | "A house without grief, he wrote, is either cured or repressed" / "the I is the column, not the flesh" |  |
| P20 | bernays | MAX | bernays | Y | 0.62 | "The town steered its whole day by that board" / "the harbor let them call it that" |  |
| P21 | plato_kirk | Gemini | plato_kirk | Y | 0.99 | "workers watched the dark shapes and mistook them for the mountain" / "hammered his iron wedge into the hidden pulley, locking the rigged balance level" |  |
| P22 | hall | MAX | hall | Y | 0.78 | "had never once heard the same play twice" / "neither page recorded what the road had decided the house was" |  |
| P23 | diogenes | Gemini | diogenes | Y | 0.99 | "the barefoot old man held his smoking pitch-torch close" / "four painted posts around a dry well do not make a parliament" |  |
| P24 | jung | MAX | jung | Y | 0.92 | "There is one night that no bundle holds" / "there was no stone cut for a thing a house will not look at" |  |

## P2 what_we_are

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:34:25.685427-04:00 -> 2026-10-23T15:36:25.908786-04:00, usage={"prompt_tokens": 25247, "completion_tokens": 22429, "total_tokens": 47676, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 20529}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25247}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | wallas | Gemini | wallas | Y | 0.86 | "what hunger had driven Ansel up the hill before frost" / "desire was never flattened into mere preference or scolded like a vice; it was treated as the fixed datum of the strategist" |  |
| P02 | baudrillard | Gemini | baudrillard | Y | 0.82 | "charting harbors that had already sunk beneath the tide" / "The parchment had not described the figure; the parchment had preceded and generated him" |  |
| P03 | mcluhan | MAX | mcluhan | Y | 0.78 | "Speech bent toward what a thread could hold" / "What was not on the cord had not happened" |  |
| P04 | ellul | MAX | jung | n | 0.7 | "each morning they arrived whole and blank as new clay, and the yard had to tell them what it was" / "every body that read the page became the Steward by noon" |  |
| P05 | jung | Gemini | freud | n | 0.95 | "what the household had shoved into the dark" / "the unrecorded deed sinks into the cellar and returns as symptom and fate" |  |
| P06 | freud | MAX | jung | n | 0.62 | "the molds were not numbered but named — Anselm, Anselm, Anselm — the same name worn smooth" / "the same pause, the listener was certain, in the same place" |  |
| P07 | hall | Gemini | hall | Y | 0.96 | "studied only how the house's dispatches changed once strangers read them" / "refused to rank the harbour-master's reading true or the syndic's reading mistaken" |  |
| P08 | diogenes | MAX | diogenes | Y | 0.8 | "a man came up the road carrying a lit lamp" / "You are begging the road for applause the wax already gives you." |  |
| P09 | foucault | MAX | foucault | Y | 0.82 | "真理在盐路的称重房中被称量，而其判决则用铁器封存。" / "每一个判断都被宣读，然后写在一张纸上，盖上印章" |  |
| P10 | diogenes | Gemini | diogenes | Y | 0.96 | "the barefoot greybeard who lives in a cracked wine-cask and carries a lit tallow lamp at noon" / "here you stand begging the highway for a nod" |  |
| P11 | mcluhan | Gemini | mcluhan | Y | 0.97 | "each was an extension of Ansel's nervous system, and each exacted its amputation" / "the curvature of the bronze had already remade the man leaning into it long before a sound arrived at the mouthpiece" |  |
| P12 | foucault | Gemini | foucault | Y | 0.86 | "inspect how its diagnoses were pronounced" / "Only when the Intendant pressed his thumb to the bar did the five clockwork examiners open their shutters and speak" |  |
| P13 | plato_kirk | MAX | plato_kirk | Y | 0.97 | "all they knew of the wide world was the shapes the fire threw on the western wall" / "He stopped the race." |  |
| P14 | hall | MAX | hall | Y | 0.72 | "One had wept over the tale and one had laughed" / "the elders counted all three readings as passings" |  |
| P15 | baudrillard | MAX | baudrillard | Y | 0.95 | "whether the paths had followed the chart or the chart the paths" / "there is no crossing but the chart's crossing" |  |
| P16 | jung | MAX | ellul | n | 0.58 | "the wall was the only thing in that country that remembered" / "The made ones never stopped anyone; they only outlasted them." |  |
| P17 | wallas | MAX | wallas | Y | 0.88 | "他们都想要同样的东西，不是答案，也不是赞美：而是想被传承下去" / "屋子继续渴求着他们所渴求的，得到它，并因它而得以维系" |  |
| P18 | ellul | Gemini | ellul | Y | 0.9 | "driven by the blind momentum of their own mechanism" / "the furnaces could boil twice as much brine if the seventh-day banking were abandoned" |  |
| P19 | fermat | MAX | fermat | Y | 0.98 | "a full demonstration of the house at the ford would not fit there" / "the three strangers had needed no margin at all" |  |
| P20 | freud | Gemini | freud | Y | 0.95 | "the small compulsion by which an institution confesses what it has not yet digested" / "phantom limb aching for a severed hand" |  |
| P21 | bernays | Gemini | bernays | Y | 0.97 | "Believing the five lecterns were independent champions, the crowd filled the square each dawn, never looking behind the curtain" / "who profits when the town believes this is scarce?" |  |
| P22 | plato_kirk | Gemini | plato_kirk | Y | 0.98 | "took the moving smoke on the rock for the sea itself and perished" / "walked out into the sun or captains who had reprogrammed the test" |  |
| P23 | bernays | MAX | bernays | Y | 0.9 | "who eats well if this is believed, and what will the hands do the morning after they believe it" / "which purse the parade filled, which hands the rumor moved" |  |
| P24 | fermat | Gemini | fermat | Y | 0.94 | "the fifth for the scrutiny of margins" / "mistaking a marginal conjecture for a finished proof" |  |

## P2 the_invariants

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:36:26.013895-04:00 -> 2026-10-23T15:38:54.306234-04:00, usage={"prompt_tokens": 25943, "completion_tokens": 25656, "total_tokens": 51599, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 24223}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25943}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | jung | Gemini | jung | Y | 0.62 | "everything the upper wards wished to disown" / "dream-figure's black wing" |  |
| P02 | freud | Gemini | freud | Y | 0.93 | "betrays its hidden wishes" / "acts out as a symptom" |  |
| P03 | fermat | MAX | fermat | Y | 0.97 | "wanted only the breadth of a margin" / "stayed in the margin" |  |
| P04 | bernays | Gemini | bernays | Y | 0.94 | "engineering consent" / "Who benefited from the belief was plain" |  |
| P05 | ellul | Gemini | ellul | Y | 0.9 | "every mechanism existed to breed a faster mechanism" / "error to be cured by iron linkages" |  |
| P06 | foucault | MAX | foucault | Y | 0.74 | "Yours are the eyes" / "the scale had studied her" |  |
| P07 | baudrillard | Gemini | baudrillard | Y | 0.9 | "more convincing than the silt outside" / "burned the vellum unread" |  |
| P08 | jung | MAX | jung | Y | 0.58 | "the year we tried to live without writing anything down" / "Nobody had ever filled it" |  |
| P09 | fermat | Gemini | fermat | Y | 0.97 | "marvelous demonstration" / "closed the clasps against the broader boast" |  |
| P10 | diogenes | MAX | diogenes | Y | 0.93 | "lit lamp in my hand" / "the noon did the rest, and nothing hid" |  |
| P11 | plato_kirk | Gemini | plato_kirk | Y | 0.95 | "wooden cutouts carried past a flame" / "unwinnable siege-drill" |  |
| P12 | wallas | Gemini | wallas | Y | 0.94 | "desire, not argument, is the load-bearing wall" / "what the workmen actually hungered for" |  |
| P13 | foucault | Gemini | foucault | Y | 0.96 | "make every tremor of the body visible" / "permanently under inspection" |  |
| P14 | plato_kirk | MAX | plato_kirk | Y | 0.86 | "taking the lamplight of the first yard for morning" / "eyes that water in full sun" |  |
| P15 | mcluhan | MAX | mcluhan | Y | 0.68 | "The town did not keep the cloth; the cloth kept the town" / "over, under, over, under, the same width" |  |
| P16 | diogenes | Gemini | diogenes | Y | 0.93 | "barefoot Oren climbed the bluff carrying a lit tallow horn" / "Strip off the sash and stop asking town dogs to bark your name" |  |
| P17 | baudrillard | MAX | baudrillard | Y | 0.96 | "copies of copies" / "answerable to nothing" |  |
| P18 | wallas | MAX | wallas | Y | 0.62 | "water did all the wanting; the wheel only rode it" / "places are held together by their arguments" |  |
| P19 | freud | MAX | freud | Y | 0.96 | "they repeated, something in them could not stop" / "what compulsion was" |  |
| P20 | hall | Gemini | hall | Y | 0.96 | "moving among three cedar chairs" / "decoded the same stroke of wood into loyalty, bargain, or refusal" |  |
| P21 | mcluhan | Gemini | ellul | n | 0.68 | "the ratchet locked against his wrist" / "physical ridge that steered the next hand" |  |
| P22 | ellul | MAX | mcluhan | n | 0.66 | "kept its days in cloth" / "the width of every strip before it" |  |
| P23 | hall | MAX | hall | Y | 0.93 | "The slate had many readers, and they did not read it alike" / "as the same working thing" |  |
| P24 | bernays | MAX | bernays | Y | 0.72 | "which want to wake first" / "a hundred hands and no flame" |  |

## P2 standing_wave_gate

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:38:54.416852-04:00 -> 2026-10-23T15:40:38.183818-04:00, usage={"prompt_tokens": 25239, "completion_tokens": 19352, "total_tokens": 44591, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 17399}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25239}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | hall | Gemini | hall | Y | 0.82 | "one artisan obeyed the sender's notch, another kept the tallow but refused the price-mark, a third scraped the mark off" / "no one inside ever looked back to see what the ditch had kept" |  |
| P02 | fermat | Gemini | fermat | Y | 0.95 | "carrying a worn Diophantus whose narrow borders held his notes on fourth powers and infinite descent" / "claimed a general proof for every power, and pared the ink back to the fourth power alone" |  |
| P03 | diogenes | MAX | diogenes | Y | 0.85 | "The lamp-carrier came up the river road at noon with his lamp lit" / "Asked what he was hunting, he said: an honest weight." |  |
| P04 | fermat | MAX | fermat | Y | 0.9 | "a book whose margins were narrow" / "the margin being too narrow for it" |  |
| P05 | diogenes | Gemini | diogenes | Y | 0.9 | "I walk into your yard at high noon holding a lit tallow lamp at arm's length" / "I hold my lamp up to your face in the broad sun and find a man starving for a title" |  |
| P06 | plato_kirk | Gemini | plato_kirk | Y | 0.95 | "the Surveyor, who had climbed the vent-shaft into blinding daylight" / "the Helmsman, who had refused a rigged trial in the lower lock" |  |
| P07 | baudrillard | MAX | baudrillard | Y | 0.9 | "The original of it had burned a generation ago; no buyer had ever returned a copy" / "the master answered pleasantly that the question had retired" |  |
| P08 | foucault | MAX | foucault | Y | 0.85 | "She asked who read the keeper" / "a second column held her own name, taken each quarter in the city against marks she recognized" |  |
| P09 | mcluhan | Gemini | mcluhan | Y | 0.72 | "never broke the seal or asked what tidings lay written" / "deaf to rumor and blind to ink" |  |
| P10 | bernays | Gemini | bernays | Y | 0.95 | "He looked at what the crowd believed it was seeing, who profited from that belief, and what the belief made their feet do" / "they paid their tolls without complaint" |  |
| P11 | ellul | Gemini | ellul | Y | 0.94 | "he asked instead what its smooth functioning forbade men to do otherwise" / "every craft had become the servant of the motion required to keep its pattern intact" |  |
| P12 | freud | MAX | freud | Y | 0.9 | "the same misfortune kept occurring" / "a thing said once is weather, twice is coincidence, and three times is a resident" |  |
| P13 | wallas | Gemini | wallas | Y | 0.88 | "things the valley's households genuinely craved" / "gilded trinkets that answered no man's real want" |  |
| P14 | jung | Gemini | jung | Y | 0.95 | "the western sewer-culvert drove an equal and opposite black surge" / "the kitchen grease, ash, and night-soil the masters upstairs pretended did not exist" |  |
| P15 | freud | Gemini | freud | Y | 0.92 | "a slip of the tongue returns in a new sentence while keeping the same hidden grammar" / "the house stopped repeating its fever" |  |
| P16 | mcluhan | MAX | mcluhan | Y | 0.85 | "Nobody asked what the boats carried" / "they had become strokes, their shoulders swinging like parts of the figure" |  |
| P17 | foucault | Gemini | foucault | Y | 0.92 | "it decided in advance what counted as a case and what remained mere noise outside the wall" / "binding watcher and watched alike within the geometry of their crossing" |  |
| P18 | hall | MAX | hall | Y | 0.9 | "The townsfolk nodded at the first two readings and copied them into the almanac" / "The stranger's reading was copied nowhere, and nothing of it was ever sent back to him" |  |
| P19 | jung | MAX | jung | Y | 0.55 | "the same crossing, the same knot, repeated the whole length" / "the way a heavy thing is handed to the nearest stranger" |  |
| P20 | plato_kirk | MAX | plato_kirk | Y | 0.82 | "it had led him to a weir their grandfathers had laid" / "Passengers still told one another that the river did this by its nature" |  |
| P21 | baudrillard | Gemini | baudrillard | Y | 0.96 | "a cartographer watches where the simulacrum devours its pretext" / "there was no original beneath the surface, only the figure generated by ceaseless motion" |  |
| P22 | bernays | MAX | bernays | Y | 0.88 | "The traveler had spent his best years making towns want things for pay" / "he had sold enough simple stories in his day to know which telling outlives its teller" |  |
| P23 | ellul | MAX | ellul | Y | 0.86 | "the grooves, not the stone, had become the work" / "it cost almost nothing to run" |  |
| P24 | wallas | MAX | wallas | Y | 0.8 | "What the town wanted, though no one said so, was not the water" / "What he wanted was the heft, and the answer of the hum" |  |

## P2 parable_as_spec

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:40:38.300360-04:00 -> 2026-10-23T15:43:21.381572-04:00, usage={"prompt_tokens": 25128, "completion_tokens": 30844, "total_tokens": 55972, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 28979}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 25128}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | foucault | MAX | foucault | Y | 0.7 | "She observed that she had made herself the one who could be watched" / "In time no one could say where the law lived." |  |
| P02 | foucault | Gemini | foucault | Y | 0.65 | "trained to believe that whatever appears within an official frame demands compliance" / "only what six severed eyes extract identically from an unlabeled figure is firm enough to bear the weight of an institution" |  |
| P03 | hall | MAX | hall | Y | 0.8 | "a book of what the picture had said to people" / "The paint is not at fault" |  |
| P04 | wallas | Gemini | wallas | Y | 0.85 | "treating men as if they were moved by arithmetic rather than by hunger, rivalry, and the craving to keep their hearths private from the bailiff's boot" / "the people's deepest want—to exercise their own judgment in dignity without a keeper overhead—was fed" |  |
| P05 | ellul | MAX | ellul | Y | 0.7 | "the town had grown around the mill's hours rather than around its own" / "Nobody had voted for the hours." |  |
| P06 | freud | Gemini | freud | Y | 0.8 | "he recognized a symptom" / "the reader's private defenses had distorted what lay plainly on the page" |  |
| P07 | jung | Gemini | jung | Y | 0.9 | "What a household refuses to own does not vanish when forbidden; it descends into the cellar, puts on a mask, and returns as fate." / "buried inside an archetypal figure that made the stomach tighten" |  |
| P08 | ellul | Gemini | ellul | Y | 0.85 | "the schedule had made itself the only cure for the errors the schedule created" / "The founders no longer listened to the metal. They served the schedule" |  |
| P09 | bernays | Gemini | bernays | Y | 0.85 | "who profited when a crowd believed a spectacle, and what that belief moved their hands to do" / "the public's appetite for a laugh" |  |
| P10 | hall | Gemini | hall | Y | 0.85 | "its meaning would be remade at every table where strangers looked up from their bread" / "she accepted the picture's foundation while bending its frame to local weather" |  |
| P11 | bernays | MAX | bernays | Y | 0.55 | "they kept what they could sing" / "Maren had set that verse in the round herself" |  |
| P12 | freud | MAX | freud | Y | 0.8 | "always at the same bend of the pass, always in the same way" / "A grief that returns to the same bend is not weather." |  |
| P13 | plato_kirk | Gemini | plato_kirk | Y | 0.95 | "slipped his tether in the underground pit and climbed into the glare" / "looked past the shadow on the bench, refused the no-win premise, and altered the room itself" |  |
| P14 | diogenes | Gemini | diogenes | Y | 0.95 | "the barefoot man who sleeps in the cracked wine-cask" / "come eat raw onions in the sun" |  |
| P15 | baudrillard | Gemini | baudrillard | Y | 0.9 | "the man exposed himself as a creature of pure simulation" / "the territory now endured only because the simulation preceded it" |  |
| P16 | fermat | Gemini | fermat | Y | 0.9 | "he possessed a marvelous demonstration" / "The margin of his folio was too cramped" |  |
| P17 | jung | MAX | jung | Y | 0.55 | "where the town kept what it would not look at" / "what you will not carry down to the cellar yourself, the river carries under" |  |
| P18 | wallas | MAX | wallas | Y | 0.75 | "the tale had asked only to be wanted" / "the want had chosen his lines for him" |  |
| P19 | mcluhan | Gemini | mcluhan | Y | 0.85 | "every tool remakes the hand that grips it before it ever touches the timber" / "a song sung over ale enters through the unguarded ear" |  |
| P20 | plato_kirk | MAX | plato_kirk | Y | 0.45 | "A girl carries water in a sieve, and the water stands. A lamp burns in a scene set at noon." / "his eye took wishes for sights" | Stronger cave/shadow imagery or an explicit rewritten simulator/test would be needed; the current cues mostly indicate interpretive testing and regime-of-truth themes. |
| P21 | diogenes | MAX | diogenes | Y | 0.6 | "walked the guild hall at noon with his lamp lit" / "a bridge that resembles its papers" |  |
| P22 | baudrillard | MAX | baudrillard | Y | 0.8 | "The picture of the thing had become the thing's memory of itself." / "They were transcribing a dinner service." |  |
| P23 | mcluhan | MAX | mcluhan | Y | 0.8 | "a picture over a hearth teaches a houseful every day without their noticing" / "what enters a man unannounced enters whole" |  |
| P24 | fermat | MAX | fermat | Y | 0.8 | "my page is narrow" / "the demonstration stands in six places at once, and wants no margin" |  |

## P2 six_lane_run

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:43:21.459769-04:00 -> 2026-10-23T15:45:59.073606-04:00, usage={"prompt_tokens": 23451, "completion_tokens": 28080, "total_tokens": 51531, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 25675}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 23451}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | ellul | MAX | ellul | Y | 0.75 | "each had been so convenient that the guild kept it, and what the guild kept, the apprentices obeyed" / "A chart is only paper, a tasting only an hour, a wiping only a wet cloth" |  |
| P02 | fermat | Gemini | fermat | Y | 0.95 | "a man may boast in a narrow margin that he possesses a marvellous demonstration for every power" / "his downward reduction holds only for the fourth degree and merely neighbors the general truth without possessing it" |  |
| P03 | freud | Gemini | freud | Y | 0.95 | "the same nocturnal sleepwalking" / "what a house repeats without understanding is a memory it has not yet agreed to confess" / "what is repressed in the ceremony betrays itself through a slip of the hand" |  |
| P04 | fermat | MAX | fermat | Y | 0.9 | "the margin of the day-book was, as margins are, too narrow to hold the demonstration" / "left the claiming to whoever came after" |  |
| P05 | bernays | Gemini | bernays | Y | 0.95 | "when six unconnected examiners arrive at the same diagnosis on the same afternoon, the councilmen persuade themselves that they are bowing to plain fact rather than to the syndicate's interest" / "The directors gained an unimpeachable mandate from the pattern, and believing that pattern moved the councilmen" |  |
| P06 | jung | Gemini | jung | Y | 0.9 | "the shadow always enters through the very rule designed to keep it out" / "a chorus may lie in unison when possessed by the same archetype" |  |
| P07 | plato_kirk | Gemini | plato_kirk | Y | 0.9 | "which laws of the archway held firm and which were only flickering shadows cast by a single brazier" / "an unexamined cavern and a rigged simulator are the same building" / "walked out into the glare" |  |
| P08 | ellul | Gemini | ellul | Y | 0.85 | "replace trust with procedure" / "no man would believe his own hand on the stonework unless the six chambers were whitewashed, the grid weighted, and the single-breath arbiter called again" |  |
| P09 | hall | MAX | hall | Y | 0.9 | "What came home was one question wearing six answers" / "marked as one among seven, no heavier than the others" / "There is no square in the frame for her, no coin, no button, and no line in the drawer" |  |
| P10 | diogenes | Gemini | diogenes | Y | 0.8 | "squinting as if six pairs of eyes will save you from trusting your own two" / "Put out the lantern, friend, and let the dogs have the tallow" / "you do not need a seventh mouth to give you leave to drink" |  |
| P11 | plato_kirk | MAX | plato_kirk | Y | 0.85 | "Whatever moved outside showed on the cloth as a black shape" / "the cloth was warm, and it asked nothing of them" / "nobody unbarred the gate" |  |
| P12 | diogenes | MAX | diogenes | Y | 0.95 | "I keep a dog and a lantern" / "lit the lantern at noon" / "You are begging six strangers, a borrowed token, and a wet-sleeved boy to carry your choosing for you, so that your hands stay clean" |  |
| P13 | jung | MAX | jung | Y | 0.45 | "A cloth that hides its own stain gets worn by it" / "the seams were where the next question lived" / "one sewn mark" | Explicit shadow/archetype language or a clearer figure of refusal/integration; as written the collective trauma and repetition could also point to Freud. |
| P14 | foucault | MAX | foucault | Y | 0.9 | "He was simply no longer the sort of witness the valley used: he had not begun from nothing; he had lived beside the field for forty years; nothing in him was fresh" / "no one would read it again except through the six, the square, the margin, and the paper on the door" |  |
| P15 | wallas | MAX | wallas | Y | 0.95 | "What the son wanted was to be found faithful. What the cousin wanted was the ring to be admired" / "The walkers wanted the road itself, which is a wider hunger than any errand" / "the sixth wanted to be home by dark" |  |
| P16 | foucault | Gemini | foucault | Y | 0.95 | "Power does not ask what men remember; it begins by washing them clean so that only the question remains" / "solitary visibility" / "transformed a breach of isolation into proof of its own vigilance" |  |
| P17 | baudrillard | Gemini | baudrillard | Y | 0.98 | "A territory is stubborn, muddy, and full of accidents; a reproduction is clean" / "By measuring the copies exclusively against one another, the checkered baize generated an original that had never existed in earth or water" / "where the coast disagrees with the sixfold convergence, it is the coast that is treated as a counterfeit" |  |
| P18 | wallas | Gemini | wallas | Y | 0.95 | "An institution is built upon a premise of what men actually want" / "six separate hungers" / "rival hungers had struck the same immovable datum" |  |
| P19 | baudrillard | MAX | baudrillard | Y | 0.95 | "their agreement no longer needs the valley" / "ask whether the copy will do as well. He tells them it always has" / "A name is a small thing. It refers to nothing and it changes everything it touches." |  |
| P20 | hall | Gemini | hall | Y | 0.98 | "None had misread the horn plate; each had poured the same cut words through the vessel of his own trade" / "bent their terms to protect the net-menders' path" / "read the threshold custom against its grain as a schedule of locks rather than a promise of shelter" |  |
| P21 | freud | MAX | freud | Y | 0.7 | "my taste for small accidents" / "tell him afterward what repeated" / "any dream I have ever taken down" / "the word a single hand had offered and no second had confirmed" |  |
| P22 | mcluhan | Gemini | mcluhan | Y | 0.95 | "He cared nothing for what picture the artisans thought they were drawing; he watched only how each housing bent the neck, narrowed the eye, or lengthened the reach" / "where a thin tin tube or a dark vault had starved the hand" |  |
| P23 | mcluhan | MAX | mcluhan | Y | 0.8 | "every difference wore the shape of its carrier's gear" / "the certainty as heavy as the pack, the smoothness with the toll road in it" / "a name read is a room entered" |  |
| P24 | bernays | MAX | bernays | Y | 0.98 | "I had spent a life arranging what towns believe" / "belief is not argued into people. It is built, out of materials they already trust" / "the stones made it look like arithmetic, and a town will believe arithmetic" |  |

## P2 water_governor

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:45:59.142285-04:00 -> 2026-10-23T15:49:00.107466-04:00, usage={"prompt_tokens": 19627, "completion_tokens": 30150, "total_tokens": 49777, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 28943}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 19627}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | diogenes | MAX | diogenes | Y | 0.96 | "I came up to the town at noon with my lamp lit" / "A dog fell in behind me" |  |
| P02 | freud | MAX | plato_kirk | n | 0.58 | "the bitter spring, flowing" / "She changed nothing else" |  |
| P03 | bernays | Gemini | bernays | Y | 0.9 | "believe the urgency was their own idea" / "the price of their calm consent" |  |
| P04 | fermat | Gemini | fermat | Y | 0.91 | "as one reduces a stubborn equation by measured steps" / "stand at the edge of the proof" |  |
| P05 | foucault | Gemini | foucault | Y | 0.95 | "partitioned gaze" / "unsayable within the law of the estate" |  |
| P06 | mcluhan | MAX | baudrillard | n | 0.78 | "Thirst, which had once been a feeling in the throat, had become a position of sand." / "no one had written that down" |  |
| P07 | hall | MAX | hall | Y | 0.95 | "read the slate as if it were a command" / "Your glass is not my thirst." |  |
| P08 | plato_kirk | MAX | wallas | n | 0.73 | "more waiters than ladles, and everyone knew it, and waited anyway" / "The game was not forbidden, and it was not won." |  |
| P09 | wallas | MAX | freud | n | 0.55 | "Marren struck the hour all the same." / "the count was complete" |  |
| P10 | mcluhan | Gemini | mcluhan | Y | 0.91 | "numbed his heels and stopped his ears" / "remade Toma's sense of time" |  |
| P11 | jung | MAX | freud | n | 0.86 | "the warden dreamed of lifting one lid" / "She woke with a dry mouth" |  |
| P12 | foucault | MAX | foucault | Y | 0.91 | "the question had never been ruled in" / "no way to write it that the table would read" |  |
| P13 | fermat | MAX | fermat | Y | 0.86 | "this board is too narrow to hold it" / "Whether I hold it, the record does not say." |  |
| P14 | ellul | Gemini | ellul | Y | 0.93 | "made exhaustion mandatory" / "the sand ceased to describe the water and began to command it" |  |
| P15 | bernays | MAX | mcluhan | n | 0.62 | "the one the town could carry home" / "The long one was true, and was never asked for again." |  |
| P16 | jung | Gemini | jung | Y | 0.9 | "the house kept what it refused to look at in the light" / "painted with a great brass wrench in his fist" |  |
| P17 | baudrillard | MAX | baudrillard | Y | 0.9 | "the river became a rumor" / "Whatever the valley was drinking, it was not water." |  |
| P18 | hall | Gemini | hall | Y | 0.95 | "different eyes sitting in different chairs around the yard waited to make their own truths out of the same white dust" / "read the same steep line in opposition" |  |
| P19 | ellul | MAX | ellul | Y | 0.78 | "The round held perfectly." / "Nothing in it had ever needed water." |  |

## P2 the_congress

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:49:00.163570-04:00 -> 2026-10-23T15:51:43.392651-04:00, usage={"prompt_tokens": 13661, "completion_tokens": 27818, "total_tokens": 41479, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 27002}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 13661}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | hall | MAX | hall | Y | 0.95 | "All three had read truly." / "None of them had read what she painted." |  |
| P02 | freud | MAX | freud | Y | 0.88 | "heard such returns before" / "the same words" |  |
| P03 | plato_kirk | MAX | plato_kirk | Y | 0.97 | "huge shadows swung" / "Ona went past them into the mouth, to see what made the shapes." |  |
| P04 | ellul | MAX | ellul | Y | 0.9 | "Each remedy arrived quietly and stayed as a need." / "because they read, the pages thickened" |  |
| P05 | mcluhan | MAX | jung | n | 0.72 | "Whoever wore a mask was nobody and the office both." / "He is the other half of my face" |  |
| P06 | diogenes | MAX | diogenes | Y | 0.96 | "The beggar carried a lamp and lit it at noon." / "a face I could believe." |  |
| P07 | foucault | MAX | foucault | Y | 0.9 | "in this town honesty had no other address" / "by the town's single rule nothing she had ever said had been said" |  |
| P08 | fermat | MAX | fermat | Y | 0.99 | "this margin is too narrow to hold it" / "leave the theorem whole and unproved" |  |
| P09 | baudrillard | MAX | mcluhan | n | 0.74 | "I had only seen the book being made true." / "the only place the congress is continuous" |  |
| P10 | bernays | MAX | baudrillard | n | 0.63 | "nobody was anything until the wall said so" / "the wall now carries an account of its own wound" |  |
| P11 | jung | MAX | bernays | n | 0.52 | "read the town back to itself" / "The town paid these breakers from the same purse as the five." |  |
| P12 | wallas | MAX | wallas | Y | 0.94 | "What the members kept of their service was the appetite only." / "The book alone wanted nothing; everything that wanted ended by quoting it." |  |

## P2 moto_cron

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:51:43.452557-04:00 -> 2026-10-23T15:54:38.103673-04:00, usage={"prompt_tokens": 13848, "completion_tokens": 29820, "total_tokens": 43668, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 28755}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 13848}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | plato_kirk | MAX | plato_kirk | Y | 0.7 | "To them the echo and the welcome were one sound" / "both were guessing at a thing that stood in plain sight one street from her own bed" |  |
| P02 | freud | MAX | foucault | n | 0.57 | "The book does not know this hand" / "the list of chores said the pass was open and the tower able, and the list had not yet heard otherwise" |  |
| P03 | foucault | MAX | foucault | Y | 0.86 | "Sela, whose office it was to watch" / "The slate did not ask whether an errand was wise. It asked only in which of its three states the errand stood." |  |
| P04 | wallas | MAX | wallas | Y | 0.9 | "Hanno stayed at the rail and counted what the gorge wanted" / "one want, the smallest and plainest, stood unfed" |  |
| P05 | mcluhan | MAX | mcluhan | Y | 0.88 | "The slips did not shrink the tasks; they shrank the writers." / "if you asked one of them to say an errand aloud, he hesitated, as if asked to sing" |  |
| P06 | baudrillard | MAX | baudrillard | Y | 0.9 | "visitors mistook it for the office's memory" / "the board did look like the record of a service in full operation; it was the record of a bell" |  |
| P07 | mcluhan | Gemini | ellul | n | 0.86 | "turned deliberation into reflex" / "a blocked vessel does not carry messages—it turns action into rehearsal" |  |
| P08 | fermat | MAX | fermat | Y | 0.96 | "which the bottom of this page is too narrow to contain" / "The call held. The rest is owed." |  |
| P09 | bernays | MAX | bernays | Y | 0.88 | "the story sold glass" / "Whoever believed it stopped dropping pebbles." |  |
| P10 | ellul | MAX | freud | n | 0.62 | "the oath had been sworn for causes that everyone had forgotten, and everyone kept it anyway" / "the long column of red returns, each with its hour" |  |
| P11 | jung | MAX | jung | Y | 0.64 | "The glass had been his only way of being spoken to." / "fault lies folded in her own sleeve, waiting to be carried across" |  |
| P12 | diogenes | MAX | diogenes | Y | 0.78 | "Stop asking the gorge to recognize you" / "Be like the mule: bring the thing the door is made to take" |  |
| P13 | hall | MAX | hall | Y | 0.9 | "saying what was written, never what was meant" / "Reading you and agreeing with you were always two different acts." |  |

## P2 keyed_verse

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:54:38.145590-04:00 -> 2026-10-23T15:56:42.915980-04:00, usage={"prompt_tokens": 12012, "completion_tokens": 21942, "total_tokens": 33954, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 20998}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12012}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | ellul | MAX | ellul | Y | 0.82 | "that they would sing what was written and add nothing" / "nothing in it asked to be understood" |  |
| P02 | hall | MAX | hall | Y | 0.9 | "each town kept the meaning it had made" / "no town's meaning was any emptier for being homemade" |  |
| P03 | plato_kirk | MAX | plato_kirk | Y | 0.95 | "threw the song onto that wall in rows of small marks" / "had the thing rewritten" |  |
| P04 | diogenes | MAX | diogenes | Y | 0.9 | "A man came through at noon carrying a lit lantern" / "The card is not your title; it is your chore" |  |
| P05 | fermat | MAX | fermat | Y | 0.95 | "the margin was too narrow to hold the proof" / "the meaning has never once traveled with the song" |  |
| P06 | mcluhan | MAX | mcluhan | Y | 0.86 | "the song and the road are the same drawing" / "the whole valley moved the way the song moved" |  |
| P07 | wallas | MAX | wallas | Y | 0.62 | "said he wanted to be the one who knew" / "Men came for the card the way they came for grain" |  |
| P08 | bernays | MAX | bernays | Y | 0.95 | "Believing the new close, people felt the door owed them an opening" / "paid for the feeling of the door opening, which he could supply nightly" |  |
| P09 | jung | MAX | jung | Y | 0.78 | "she found the house's other half, awake and keeping time" / "the voice grows louder the longer the father is in the ground" |  |
| P10 | foucault | MAX | foucault | Y | 0.95 | "The line of gazes closed into a ring" / "Whoever held the slip named what the unison meant" |  |
| P11 | freud | MAX | freud | Y | 0.9 | "the valley could not stop producing it, though nobody could say what it was for" / "no one had taught them by word" |  |
| P12 | baudrillard | MAX | baudrillard | Y | 0.9 | "the six cities now learned the song from the delta's copies rather than from Alder's barges" / "the copies keep the shape by themselves now" |  |

## P2 rib_renderman_mapping

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:56:42.961978-04:00 -> 2026-10-23T15:59:57.465419-04:00, usage={"prompt_tokens": 12609, "completion_tokens": 32514, "total_tokens": 45123, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 31705}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12609}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | plato_kirk | MAX | plato_kirk | Y | 0.78 | "having looked too long at the brightness of the far side" / "could not tell a coat from its own shadow" |  |
| P02 | baudrillard | MAX | baudrillard | Y | 0.86 | "Where entry forty-one put the forge she found grass, low stones, the rusted shoes of a wall" / "the fire came, and the work was done" |  |
| P03 | wallas | MAX | wallas | Y | 0.9 | "Nothing in the Lantern Works was heavy until somebody wanted something through it" / "whoever wrote the words that answered the wanting held more of the house than whoever owned it" |  |
| P04 | diogenes | MAX | diogenes | Y | 0.95 | "The house called her the dog, and she answered to it" / "what is done shows in any light; what is only said needs the dark" |  |
| P05 | foucault | MAX | foucault | Y | 0.78 | "no place at all for not-knowing" / "what cannot be entered cannot be traded or kept" |  |
| P06 | bernays | MAX | bernays | Y | 0.92 | "I spent my first life making crowds want what others were selling" / "asking who gains when its habits are believed" |  |
| P07 | ellul | MAX | ellul | Y | 0.9 | "Nobody had ordered this. It arrived with the practice itself." / "the writing had already decided what the planters could be asked for and what they never would be" |  |
| P08 | jung | MAX | jung | Y | 0.62 | "The cards stayed blank. The scroll stayed beautiful." / "The dune was the scroll's own silence returning, tale by tale, to lie in the corner like a guest left standing at the table." |  |
| P09 | hall | MAX | hall | Y | 0.96 | "All three held the same glyphs." / "The capital had folded a festival; the stranger's hands opened an indictment." |  |
| P10 | fermat | MAX | fermat | Y | 0.92 | "the margin was too narrow to hold" / "I broke one card out of the box and could not break the second" |  |
| P11 | mcluhan | MAX | mcluhan | Y | 0.82 | "the slips were doing to the couriers" / "They had started to find only what would fit." |  |
| P12 | freud | MAX | freud | Y | 0.74 | "though nothing had ever been sent" / "On Friday, the recitation would begin again." |  |

## P2 dirac_loops

- Served `deepseek-flash`, finish=stop, attempts=['ok'], 2026-10-23T15:59:57.522920-04:00 -> 2026-10-23T16:02:24.478919-04:00, usage={"prompt_tokens": 12565, "completion_tokens": 26419, "total_tokens": 38984, "prompt_tokens_details": {"cached_tokens": 0}, "completion_tokens_details": {"reasoning_tokens": 25436}, "prompt_cache_hit_tokens": 0, "prompt_cache_miss_tokens": 12565}

| ID | true lens | writer | judged | ok | conf | cues (verbatim) | missing |
|---|---|---|---|---|---|---|---|
| P01 | mcluhan | MAX | mcluhan | Y | 0.64 | "The horn governed everything." / "The walkers themselves were the guild's true work, though no one said so." |  |
| P02 | freud | MAX | freud | Y | 0.86 | "what keeps returning, and what does it ask for?" / "the syllable cut off at the same shore, walker after walker, year after year" |  |
| P03 | ellul | MAX | ellul | Y | 0.9 | "what all of it made inevitable, and who had chosen that" / "what is there to be done in a hall of string gets done" |  |
| P04 | jung | MAX | jung | Y | 0.68 | "called them the house's openness" / "the shape of the house's griefs curved back toward their beginnings" |  |
| P05 | foucault | MAX | foucault | Y | 0.82 | "The rolls admitted only written leans, signed by sworn staffs" / "nothing she said was written, because she carried no staff" |  |
| P06 | baudrillard | MAX | baudrillard | Y | 0.9 | "A drawn circle, she said, is either a promise of a street or a lie about one" / "a copy of a copy" |  |
| P07 | bernays | MAX | bernays | Y | 0.86 | "who was lighter when this was believed" / "Pello's own ferry took fares at both landings." |  |
| P08 | diogenes | MAX | diogenes | Y | 0.96 | "在正午时分点燃并提在手里的灯笼" / "你是在要求这个镇子的人们站成一个圈来赞赏" |  |
| P09 | plato_kirk | MAX | plato_kirk | Y | 0.83 | "climbed it and saw whole what no one below had seen" / "stood in the clear light above the fog" |  |
| P10 | wallas | MAX | wallas | Y | 0.87 | "What each party wanted was no secret." / "Ove's trade rode that itch" |  |
| P11 | hall | MAX | hall | Y | 0.9 | "the word was heard three times" / "Oren wrote all three hearings beneath the word" |  |
| P12 | fermat | MAX | fermat | Y | 0.92 | "the mending of this one is known to me, and the showing of it would not fit this edge" / "Not that it is done." |  |
