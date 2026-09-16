# X MINE — physical computing vein — 2026-09-16

Lane: X input search, physical-computing. Window: Sept 2026 (allow back to June 2026).
Method: WebSearch (site:x.com + plain) → fxtwitter.com/<user>/status/<id> for full text. Free APIs only.
Status: OPEN — findings appended below as discovered.

## Findings (appended per discovery)

### T1. @extropic — 2026-07-29
- Claim: Z1.5 (iteration over Z1, first production-scale TSU) to be fabbed at a US foundry; $75M non-binding CHIPS R&D LOI with Dept of Commerce; two X0 variants already taped out AND tested at two different fabs (fab-portability proof).
- Why it matters: **substrate + vocabulary** — TSU = "Thermodynamic Sampling Unit", samples from programmable probability distributions using CMOS thermal noise on mature nodes. The fab-portability claim (same design, two fabs, both tested) is the falsifiable detail worth tracking. Promise of "comprehensive technical update in coming days" — check for the follow-up post with real benchmarks.
- URL: https://x.com/extropic/status/2082459450166968328

### T2. @extropic / Z1T announcement (via @GillVerd amplification, ~2026)
- Claim: Z1T = first transformer-like model family for sparse probabilistic hardware; "up to 140x energy efficiency gains" on inference over GPUs; weights + training recipe open-sourced.
- Why it matters: **falsifier** — open weights make the 140x claim independently checkable (unlike most efficiency press releases). Third-party replication would be the strongest possible steal for the pack. Reddit thread r/AISEOInsider "Extropic AI Chip Claims 140x Energy Breakthrough" already flags inspectability.
- URL: https://extropic.ai/writing/z1t (canonical claim page; X amplification via https://x.com/GillVerd)

### T3. @DustinJuliano — thermodynamic computing benchmark proposal
- Claim: proposes a comprehensive open-source comparative benchmark for thermodynamic computing with baseline CPU and GPU comparisons.
- Why it matters: **falsifier** — exactly the eval-harness pattern our pack uses (bytes, not reports). If Juliano's harness exists, adopt rather than rebuild.
- URL: https://x.com/DustinJuliano (post ID not indexed; thread on profile)

### T4. @ronboger — skepticism on Extropic timelines
- Claim: Extropic ambition is "delusionally optimistic" like early SpaceX doubt; many experts doubted thermodynamic computing.
- Why it matters: **falsifier** — the skeptical pole. Useful for the pack's "claim vs measured" ledger: both poles of the discourse are now on record.
- URL: https://x.com/ronboger (all-posts page; post ID not indexed)

### T5. Normal Computing CN101 (context, non-X)
- Claim: world's first thermodynamic computing chip taped out (June 2025, ARIA UK-funded); up to 1000x energy-efficiency claim on matrix/sampling workloads; bring-up results shared; low-speed I/O test chip; arXiv 2608.00754 "A Digital Thermodynamic Computer for Generative AI"; CN product line releases planned 2026 and 2028.
- Why it matters: **substrate** — the competing pole to Extropic. The 2026 release window means third-party hands-on data may land this quarter. Bring-up post is on LinkedIn (activity-7407878852691025921).
- URL: https://www.normalcomputing.com/blog/normal-computing-announces-tape-out-of-worlds-first-thermodynamic-computing-chip

## A. Coherent Ising machines / annealers — 2026 results

### A1. @peterlmcmahon — 2026-04-21 (thread, post 9/9)
- Claim: McMahon lab (Cornell) + Ruomin Zhu + USRA + Princeton preprint on arXiv 2604.17109: "A fully parallel densely connected probabilistic Ising machine" — p-bit hardware, established as promising alternative to [quantum annealers per truncated card].
- Why it matters: **substrate + falsifier** — fully parallel + densely connected is the hard combo (most p-bit machines fake one or the other). Thread root likely has measured perf. Group also ships `mcmahon-lab/cim-optimizer` (open CIM simulator) — free baseline for any annealing claim we test.
- URL: https://x.com/peterlmcmahon/status/2046424810624831630 · paper: https://arxiv.org/abs/2604.17109

### A2. Toshiba "Edge of Chaos" simulated bifurcation — April 2026 (press + APS; X coverage sparse/not yet indexed)
- Claim: third-gen GSB algorithm harnesses edge-of-chaos dynamics; ~99% success / ~100x speedup claims on fully-connected 2,000-spin Ising problems; Goto et al., Phys Rev + arXiv 2508.17655.
- Why it matters: **vocabulary + falsifier** — "edge of chaos" is the exact regime word our mycelial pack uses for substrate dynamics; here it is quantitatively measured (time-to-solution on 2k spins). Classical quantum-inspired algorithm beating annealers = baseline every annealing claim must now clear.
- URL: https://www.global.toshiba/ww/technology/corporate/rdc/rd/topics/26/2604-01.html · https://arxiv.org/html/2508.17655v1

### A3. Reality-check literature (context)
- 2026 arXiv "A Reality Check on Quantum Optimisation" (2607.13325) treats Fujitsu Digital Annealer as the practical lower bound quantum must beat; CIM field: Nature Comms 2026 polarization-symmetry-breaking CIM (s41467-026-68794-6), 4,096-spin programmable optoelectronic IM (Light Sci Appl 2026), million-spin photonic IM roadmap (arXiv 2607.13446).
- Why it matters: **falsifier** — the field is converging on honest baselines (DA/GPU) before claiming quantum advantage; matches our "trust bytes" doctrine.
- URL: https://arxiv.org/html/2607.13325v1

<!-- APPEND BELOW THIS LINE -->

## 8 best steals (ranked)

(TBD)

## 3 things the timeline believes that our pack contradicts

(TBD)
