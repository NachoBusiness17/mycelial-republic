# S5 — Journal / venue map: fungal electrophysiology → computing → bio-hybrid

- **Wave:** wave_20260916 · **Seat:** S5 (venues half of "steal existing research and journals around this")
- **Operator mission:** map WHERE the field lives and where a rigorous hobbyist-grade result ($31 instrumented cube, pre-registered stage-2) could land.
- **Method:** receipt-first, appended as research progressed. WebSearch/WebFetch only (free). No paid APIs, no git.
- **Status:** IN PROGRESS — sections appended below as completed.

## §0. Sections plan
1. Journals (scope / OA model / bar / 1 recent fungal-computing example each)
2. Conferences & workshops (ALife, ECAL, UCNC/UCC, bio-hybrid & necrobotics venues)
3. Preprint norms (arXiv q-bio vs bioRxiv)
4. Practical venue ladder for the $31 cube stage-2 result (3 concrete steps + requirements)

*(appended below)*

## §1. Journals — where fungal electrophysiology / computing actually publishes

**Census method:** Europe PMC API query `"fungal computing"` (25 results, free) + C17's verified DOI set + targeted WebSearch (survived 2× gen-1-style 429 rate limits). Journals ranked by fit-to-our-stage-2-result.

### Confirmed fungal-computing venues

| Journal | Scope (one line) | OA model | Typical bar | Fungal example (verified) |
|---|---|---|---|---|
| **Biosystems** (Elsevier) | Information processing, computation and cognition in biological systems — the field's home journal | Hybrid: publish FREE non-OA; ~high APC only if you want gold OA | Moderate; specialist audience; EIC is **Andrew Adamatzky** (field founder — fit is guaranteed, conflicts possible, do not cite yourself his retracted paper) | Boolean gates in fungal colony (10.1016/j.biosystems.2020.104138); "Fungal electronics" review (10.1016/j.biosystems.2021.104588); **Fungal biohybrid substrates…** 262:105739 (Feb 2026) [all V in C17] |
| **Scientific Reports** (Springer Nature) | All natural sciences; multi-disciplinary | Full OA, APC ≈ $2,490–2,690 (2026; waivers only for low-income countries — a US independent researcher pays) | **Soundness-only peer review** (novelty/impact explicitly not judged) — the honest-home for a rigorous null result | Telhan et al., mycelium chips for physical RC, s41598-026-55550-5 (2026, PMC13500807); Responsive fungal insoles (10.1038/s41598-023-31594-9) [V] |
| **PLOS ONE** | All of science | Full OA, APC ≈ $2,140 (2026 approx.; fee-assistance programs exist) | Soundness-only review; negatives publishable | LaRocco et al., shiitake memristors, e0328965 (2025, PMC12513579) [V] — preprint 10.1101/2025.07.11.664296 → published same data |
| **Interface Focus** (Royal Society) | Theme-issue driven cross-disciplinary biology/physical sciences | Gold OA | Higher than the above (Royal Society quality bar, invited theme issues + open submissions) | Adamatzky, "Towards fungal computer" 8(6):20180029 (2018, PMC6227805) [V] |
| **Natural Computing** (Springer) | Computing paradigms from nature, incl. bio-physical computing | Hybrid (free non-OA) | Moderate; theory-friendly but took a growth-modeling RC paper | Tompris et al., "Mycelium as a computational medium…", 10.1007/s11047-025-10040-x (2025) [V via C17+search] |
| **Journal of Biological Physics** (Springer) | Biological physics incl. complex/experimental systems | Hybrid; **no free gold-OA guarantee** — searches did NOT confirm S2O; subscription route = free | Moderate; biophysics framing required | Adamatzky posted "Fungi anaesthesia" as arXiv:2106.09007 with JBP as intended venue (preprint→journal pipeline is the norm here) |
| **Frontiers in Fungal Biology** | Mycology incl. fungal physiology/biophysics | Full OA, APC ≈ $3,000+ class | Frontiers review style; mycology audience — electrophysiology is in-scope only when framed as fungal physiology | *(verification pending — see below)* |
| **Biosensors & Bioelectronics** (Elsevier) | Bio-sensing DEVICES — engineering-first | Hybrid, high OA fee | High (IF ~10, device must work well) | No fungal-computing canon found — wrong venue unless the cube becomes a published biosensor |
| **MDPI Biosensors** (distinct journal!) | Biosensing incl. reviews | Full OA (MDPI APC ~2,600 CHF class) | Moderate-low reputation discount (MDPI) | Grasso, "Fungal Frontiers in (Bio)sensing," 10.3390/bios16020131 (2026) — explicit fungal electrophysiology coverage [V] |

**Tier-adjacent instrument venues (for the RIG, not the biology):** HardwareX (Elsevier, OA — open-hardware papers) and Journal of Open Hardware (diamond OA, minimal/no APC). The $31 stage-0 rig itself is a legitimate separate artifact there.

**NOT confirmed as fungal-computing venues:** IEEE Trans. NanoBioscience (hybrid; $2,800 OA fee for 2026, free traditional route; scope = nano/micro-scale bioengineering; **zero fungal-RC papers surfaced** — only plausible for the instrumentation side). Topics in Cognitive Science took a fungal-cognition piece (Colombo 2025, 10.1111/tops.70024) — philosophy-adjacent, not rig-level.

**Retraction hazard carried forward from C17:** "Fungal sensing skin" (Fungal Biology and Biotechnology, 2021) retracted (note 10.1186/s40694-021-00114-7) — never cite as support; Fungal Biol Biotechnol itself remains a viable OA venue (BMC).

*(§2 conferences appended below)*

## §2. Conferences & workshops — which take rig-level (not theory-level) work

| Venue | Format/proceedings | Rig-level accepted? | Fungal/bio-hybrid fit |
|---|---|---|---|
| **ALife (Int. Conf. on Artificial Life)** — ALIFE 2025: Kyoto, 6–10 Oct 2025 | MIT Press proceedings (vol 37, "Ciphers of Life", direct.mit.edu/isal) | **Yes** — full/short papers, posters, special sessions, workshops, art track | ALIFE 2025 ran a **"Distributed Ciphers" special session explicitly bridging fungi, swarms, plants + ALife/AI** (nichele.eu/ALIFE-DistributedCiphers); unconventional-computing-with-materials papers are in the volume |
| **ECAL** (European ALife) | Same series — ECAL and ALife merged into the single annual ALife conference series years ago; treat as one venue | Yes (same) | Same community; Adamatzky-adjacent work is routine |
| **UCNC** (Unconventional Computation and Natural Computation) — 22nd: Nice, 1–5 Sep 2025; 23rd: **Trieste, 22–26 Jun 2026** | Springer **LNCS 16364** (2025) | **Yes — CfP explicitly solicits both theoretical AND experimental contributions** (molecular, cellular, amorphous, nature-inspired) | Experimental Physarum/fungal computing from the Adamatzky orbit appears here regularly. Timing note: UCNC 2026 deadline (~Jan–Feb 2026) already passed for a Nov-2026 stage-2 finish — target UCNC 2027 |
| **Living Machines** (Int. Conf. on Biomimetic and Biohybrid Systems) — 14th: Sheffield, 15–18 Jul 2025 | Springer proceedings (Biomimetic and Biohybrid Systems series) + **Nature "Living Machines" companion collection** | **Yes** — this is THE rig-level bio-hybrid venue (robots + living tissue; hardware demos normal) | Best conference fit for a living-substrate sensing/computing rig with honest baselines |
| **ICRA "Unconventional Robots" workshop series** — 2nd: ICRA 2025 Atlanta (19 May 2025); **3rd: ICRA 2026 Vienna, 5 Jun 2026** | Non-archival workshop | **Yes** — workshops take late-breaking rigs | Closest robotics home for necrobotics-adjacent substrate work (necrobotics canon: Yap & Preston, Advanced Science — dead-spider grippers; no dedicated necrobotics workshop exists) |
| **Unconventional Robotics Symposium 2026** — TU Delft, 14–15 Sep 2026 | Free symposium | Yes | Soft bodies / embodied intelligence / unconventional actuation — cheap to attend, good for feedback, not archival |

**Verdict:** ALife and Living Machines are the two rig-level conference homes; UCNC takes experiments but skews theory; ICRA Unconventional-Robots workshops are the fast non-archival option. Deadlines land ~Feb–May each year — after a Nov-2026 stage-2, the realistic first conference shot is spring-2027 deadlines for ALife/Living Machines/UCNC 2027, which means the preprint (§3) does the work in the meantime.

## §3. Preprint norms in this space

**Both arXiv and bioRxiv are used; the split is by flavor, and the field's most important recent papers all preprinted:**

- **bioRxiv** (free to post, no endorsement needed, immediate DOI) — the bio-flavored default:
  - Telhan et al. mycelium-chip RC: bioRxiv 2025.08.20.671348 → Scientific Reports (the closest prior art, C17).
  - LaRocco et al. shiitake memristors: bioRxiv 10.1101/2025.07.11.664296 → PLOS ONE (preprint and journal versions both indexed).
  - Bhattacharyya, "Digital Twins for Fungal Computing" (2026, bioRxiv, DOI 10.64898/2026.03.27.714860 per Europe PMC).
- **arXiv** — computing-flavored papers (Adamatzky posts constantly; e.g. "Fungi anaesthesia" arXiv:2106.09007, posted with Journal of Biological Physics as the intended journal). Categories in play: q-bio.TO/q-bio.NC, cs.NE, nlin.AO.
- **Practical constraint:** arXiv **q-bio requires an endorsement** for a first-time submitter (an existing q-bio author must vouch) — an independent researcher may have to route via bioRxiv or ask the small field (Adamatzky lab, Ecovative/Telhan) for an endorsement. bioRxiv has no gate.
- **Data preprints:** this repo already mints Zenodo DOIs (`wave_20260916/receipts/B9_ZENODO_DOIS*`); raw-trail + Zenodo DOI is exactly the norm LaRocco/Telhan set (Telhan's analysis code is public on GitHub — github.com/otelhan/NeuromorphicMyceliumChip, MIT).

**Field-specific reviews to position against (both open):** Buffi et al. 2025, "Electrical signaling in fungi: past and present challenges," FEMS Microbiology Reviews (10.1093/femsre/fuaf009, PMC11995700) — the methods-critique anchor; Grasso 2026, "Fungal Frontiers in (Bio)sensing," Biosensors 16:131.

*(§4 practical ladder appended below)*

## §4. The honest venue ladder for cube01 stage-2 (positive OR negative result)

What the C17 plan ALREADY does (so the ladder only names the DELTA): pre-registration hashed into the trail before data closes; hash-chained append-only raw rows with declared gaps; TWO baselines (shuffled labels + dead-substrate control through identical electronics); n=100 balanced/seeded, Bonferroni α=0.025; Telhan-comparable MC methodology; pre-registered kill criteria with the "physical altar" retreat. The plan's evidence machinery is already at-or-above what many published papers in this field carried — the ladder is mostly packaging, independence, and money.

### STEP 1 — Receipt + public data/code deposit (Zenodo DOI) — same day the stage closes
- **Artifact:** one Zenodo deposit (or two: dataset + software) containing the raw CSV chunks, the admission-view trail export, the registered analysis script (hash visible in the deposit), and a data dictionary/methods README. Mint DOIs. Mirror the receipt + DOI into `watch/inbox/physical_computing/`.
- **Requirements beyond the plan:** (1) code must run from a clean clone on a stranger's machine — `mag.cube01_replay` + analysis need a synthetic-data self-test so a referee/reader can verify the pipeline end-to-end; (2) the methods prose must reach journal grade (electrode geometry, sampling, stimulus schedule, inclusion/exclusion of contaminated restarts — all already decided in the plan, just written out); (3) one outside re-hasher of the raw bytes (fleet mechanical witness + one human seat — A2 two-eyes); (4) `$0` — Zenodo is free.
- **This tier alone satisfies the fleet's receipt doctrine and is the irreducible floor:** a clean NEGATIVE stage-2 with this package is a publishable-quality falsification of the reservoir wording even if nothing below ever happens.

### STEP 2 — Preprint (bioRxiv; arXiv only if an endorsement is obtainable) — weeks after
- **Venue choice:** bioRxiv default (free, no endorsement gate, field precedent: Telhan 2025, LaRocco 2025). arXiv q-bio.TO/q-bio.NC requires a first-timer endorsement — the field is small enough to ask (Adamatzky lab / Ecovative line) but bioRxiv first is fine and norm-consistent.
- **Requirements beyond the plan:** (1) a structured manuscript (Abstract / Intro positioning against Telhan-SciRep-2026, LaRocco-PLOS-2025, Buffi-FEMS-Rev-2025 methods critique, Adamatzky-Biosystems-2026 gap; Methods / Results / Limitations); (2) an **independent statistical re-run**: a second seat re-executes the registered analysis from the deposited raw bytes and signs a one-line statement — cheap insurance, because this is exactly what referees and the A2 CORROBORATED gate both demand anyway; (3) link the registration artifact (hash + timestamp + Zenodo DOI) from the paper so the pre-registration is verifiable, not asserted; (4) limitation section written honestly: hobby-grade electronics ($25 ADC class, not a DAQ), no environmental chamber, single cube, independent-researcher affiliation; (5) figures to journal standard (vector, readable grayscale); (6) state the negative result plainly if it is negative — a pre-registered K2 death is a result, not a failure to file.
- **Cost:** $0.

### STEP 3 — Journal (and conference, in parallel) — only after Step 2
- **If POSITIVE (stage-2 pass) or informative stage-1 MC numbers:**
  1. **Scientific Reports** — soundness-only review (novelty not judged), took Telhan, full OA; the honest first target. Barrier: APC ≈ $2.5–2.7k (Nature waivers are low-income-country based; a US independent pays). Requires operator word on money.
  2. **Biosystems** (free to publish, non-OA) — the field's home journal, Adamatzky's editorial seat, our Feb-2026 gap paper lives there; zero-cost route if the APC is refused.
  3. **Natural Computing** or **Journal of Biological Physics** (both Springer hybrid, free non-OA routes) as further no-APC fallbacks.
- **If NEGATIVE (stage-2 kill / K2):** **PLOS ONE** is the designed home — soundness-only review, negatives explicitly publishable, LaRocco precedent, APC ≈ $2.1k; free fallback = keep it at Steps 1–2 and submit the null to Biosystems (which has published critical/protocol work) — never bury the null in a drawer; the pre-registration makes the null MORE credible than an unregistered positive from a worse rig.
- **Rig-as-artifact branch (any outcome):** **HardwareX** or **Journal of Open Hardware** — the $31 open-hardware instrument is a separate citable paper; JOH is near-zero cost.
- **Conference, spring-2027 deadlines (stage-2 finishes Nov 2026; 2026 deadlines already passed):** **Living Machines 2027** (best rig-level bio-hybrid fit, Springer proceedings) and **ALife 2027** (MIT Press; fungi had a dedicated special session at ALIFE 2025) — both take exactly "rigorous rig-level result with honest baselines"; **UCNC 2027** (LNCS) as the unconventional-computing alternative.
- **Requirements beyond the plan at this tier:** (1) referee-grade statistics will be asked for anyway — effect sizes with CIs and the power story; the registration already carries Bonferroni and binomial logic, so this is exposition, not new work; (2) raw data + code as DOI supplements (done at Step 1); (3) **independent repetition is the one honest gap no tier up to here closes** — a soundness-only journal will not force it, but the field's own history (Telhan's 4x chip-to-chip MC spread, the 2021 Fungal-Biol-Biotechnol retraction) means a single-cube claim must be worded as "cube v1" evidence with the replication invitation explicit — that is already how the plan words it, keep it that way; (4) cover letter positions the result against the Adamatzky 2026 Biosystems roadmap gap (our ladder = a concrete instance of their named open problem); (5) the APC decision (~$2–3k) is an operator-word item with genuine $0 alternatives — this is the only tier where money, not evidence, is the binding constraint.

**Do NOT aim at:** IEEE Trans. NanoBioscience (zero fungal-computing canon found; device-engineering bar), Elsevier Biosensors & Bioelectronics (IF~10 device bar), MDPI Biosensors (reputation discount — fallback only), Topics in Cognitive Science (philosophy venue).

## FINAL REPORT

**Deliverable:** venue map (this receipt) — 9 journals triaged with scope/OA/bar/example, 6 conference/workshop venues with rig-level verdicts and deadline reality, preprint norms (bioRxiv = free default, arXiv needs endorsement), and a 3-step venue ladder for cube01.

**Headline findings:**
1. **The field's real journal homes are Biosystems (Adamatzky-edited, free non-OA), Scientific Reports and PLOS ONE (soundness-only, took the two closest prior-art papers — Telhan 2026 and LaRocco 2025), with Interface Focus as the canon origin.** The mission's guess list was right on all of these except IEEE TNB (no fungal canon found — drop it).
2. **Rig-level conferences exist and took fungi:** ALife (MIT Press; fungi special session 2025), Living Machines (Springer, best fit), UCNC (LNCS, explicitly experimental-welcoming). All 2026 deadlines precede our Nov-2026 stage-2 — spring 2027 is the realistic window, preprint carries the interval.
3. **Preprint norm is double-tracked:** bioRxiv (free, no gate — Telhan, LaRocco both went preprint→journal in 2025) for bio-flavored, arXiv (Adamatzky's constant habit) for computing-flavored; q-bio endorsement is the only gate an independent researcher hits.
4. **The ladder's only non-evidence constraint is money at tier 3:** Steps 1–2 are $0 (Zenodo + bioRxiv); tier 3 has genuine $0 routes (Biosystems, Natural Computing, JBP) so the APC (~$2–3k) is a choice, not a wall.
5. **Independent repetition is the standing hole in every tier** — no venue up to PLOS/SciRep will force it, but the field's retraction history and Telhan's 4x inter-chip spread make "cube v1, replication invited" the only honest wording; the plan already words it that way. Keep it.

**Method notes:** Europe PMC API census (free) + 4 WebSearch rounds (survived 429 rate limits; C17's predicted killer recurred and was outlasted) + C17 verified-DOI base. Unverified numbers flagged: PLOS ONE APC ≈ $2.1k and Sci Rep ≈ $2.5–2.7k are approximate 2026 figures; Frontiers APC "~$3k class" approximate; JBP S2O status NOT confirmed (searched, not found — treat as hybrid, free subscription route).

**Status:** COMPLETE — receipt ends with the venue ladder as 3 concrete steps with requirements (§4). Operator decisions surfaced: none required now; APC word needed only at step 3.
