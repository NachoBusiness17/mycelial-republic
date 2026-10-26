# r-attractor-portfolio: chaos-theory attractor concepts applied to engineering portfolio management

Research item, banked 2026-09-28. Question: do formal treatments exist of chaos-theory attractor
concepts (bounded unpredictability, attractor shapes as policy) applied to engineering portfolio
management? Every bibliographic claim below was verified through web search during this session
(method and query list at the end); full texts were not fetched, and anything resting on
snippet-level evidence is flagged in the OWED ledger.

## Bottom line

**No established, formal (mathematical) treatment of attractor concepts specifically for
engineering project / R&D portfolio management was found.** Direct searches for "project
portfolio" + "strange attractor" / chaos + engineering management surface exactly one
project-portfolio-proximate conceptual paper (Geraldi 2008, below) plus adjacent literatures.
The strongest formal analogues live in four neighboring fields:

1. **Nonlinear dynamics itself** defines bounded unpredictability precisely (attractor +
   Lyapunov exponent + predictability horizon: Lorenz 1963, Wolf et al 1985).
2. **Strategy / organization theory** imported the concepts formally via NK fitness landscapes,
   where "basin of attraction" is a rigorous object (Levinthal 1997, Rivkin 2000).
3. **Resilience science** is the one tradition that already treats *attractor shapes as explicit
   policy objects* (Holling 1973; Walker et al 2004: manage the stability landscape).
4. **Financial portfolio management** has the only chaos-based *portfolio selection* methodology
   found (Spelta et al 2022; Peters 1991/1994), but for investment portfolios, not projects.

Geraldi 2008 is the closest single hit inside multi-project management, and it is a conceptual
model, not a formal one. The phrase-level idea "attractor shapes as policy" (choose the topology
of the attractor as the governing instrument) does not appear in any source found; the nearest
existing thing is resilience-based governance of basins of attraction (Walker et al 2004) and
Levy's managerial reading of strange attractors (1994).

## Layer 1: the formal math (what "bounded unpredictability" means exactly)

- **Lorenz, E.N. (1963). "Deterministic Nonperiodic Flow." *Journal of the Atmospheric Sciences*
  20(2): 130-141.** Verified (full-text PDF at cdanfort.w3.uvm.edu, Semantic Scholar, PhilPapers,
  NASA ADS; 33,000+ citations). Establishes deterministic, bounded, aperiodic solutions: the
  trajectory stays in a finite region of phase space (bounded) yet never repeats and diverges
  from nearby starts. This is the canonical formalization of bounded unpredictability: finite
  envelope, unbounded horizon of detail.
- **Wolf, A., Swift, J.B., Swinney, H.L., Vastano, J.A. (1985). "Determining Lyapunov exponents
  from a time series." *Physica D* 16(3): 285-317.** Verified (ScienceDirect, NASA ADS, UT Austin
  chaos group, free PDF at hal.science; 14,000+ citations). First practical algorithms to
  estimate non-negative Lyapunov exponents from experimental time series. Search output quotes
  the paper: Lyapunov exponents "measure the exponential divergence of initially near trajectories"
  and "are characteristic dimensions of the attractor." The largest exponent sets the
  **predictability horizon**: forecast life scales like (1/lambda1) * ln(C/delta) with C the
  tolerance and delta the initial error (formula as given in search output, attributed to lecture
  notes citing this paper). For a portfolio interpretation: bounded unpredictability is not a
  modeling failure, it is an estimated quantity lambda1 with an explicit horizon.

## Layer 2: formal treatments in strategy and organization theory (NK landscapes, basins)

The genuinely formal import of "attractor" into management did not come through chaos theory
directly; it came through Kauffman's NK model, where basins of attraction are well-defined
objects on a fitness landscape.

- **Levinthal, D.A. (1997). "Adaptation on Rugged Landscapes." *Management Science* 43(7):
  934-950.** Verified (INFORMS DOI 10.1287/mnsc.43.7.934; 3,600+ citations). Introduced the NK
  model into organization theory: with high interdependence K, local search and long jumps both
  fail; organizations get trapped near local peaks. A portfolio of initiatives searching a rugged
  landscape is the direct formal reading.
- **Rivkin, J.W. (2000). "Imitation of Complex Strategies." *Management Science* 46(6): 824-844.**
  Verified (HBS faculty publication list). Complex (high-K) strategies sit in "small stable highs":
  hard to imitate, hard to find. Portfolio implication: complexity itself is a moat, and the
  basin, not the peak, is what search dynamics see.
- **Basin-of-attraction language in strategy search** appears throughout the follow-on literature
  (Siggelkow & Rivkin 2006 on search after "locating a promising basin of attraction"; Dosi et al
  2015/2017 on organizations settling into basins determined by cognitive frames). Verified only
  at snippet level this session: OWED-3.
- **Levy, D. (1994). "Chaos Theory and Strategy: Theory, Application, and Managerial
  Implications." *Strategic Management Journal* 15(S2): 167-178.** Verified (Wiley DOI
  10.1002/smj.4250151011, ~1,200 citations; free PDF circulating). The canonical chaos-to-strategy
  bridge: strange attractors, sensitivity to initial conditions, bifurcation, and fractals argued
  onto industry dynamics, with the managerial punchline that long-range planning has a hard
  horizon. This is the standard citation if you want chaos concepts (as opposed to NK concepts)
  attached to management.

## Layer 3: attractor shapes as policy, the one formal tradition that exists

- **Holling, C.S. (1973). "Resilience and Stability of Ecological Systems." *Annual Review of
  Ecology and Systematics* 4: 1-23.** Verified (publisher listing via search). Introduces
  ecological resilience as the size of the region from which a system returns, explicitly against
  the equilibrium-return notion of stability: multiple stability domains, i.e. **multiple basins
  of attraction** as the normal state of a managed system.
- **Walker, B., Holling, C.S., Carpenter, S.R., Kinzig, A. (2004). "Resilience, Adaptability and
  Transformability in Social-Ecological Systems." *Ecology and Society* 9(2): 5.** Verified
  (open access at ecologyandsociety.org/vol9/iss2/art5; ~12,900 citations). This is the closest
  existing formal treatment of "attractor shapes as policy": adaptability = capacity of actors to
  manage resilience, transformability = capacity to cross thresholds into a fundamentally new
  regime, and governance = managing the **stability landscape** itself (its latitude, resistance,
  precariousness). Translate to a portfolio: policy chooses the depth and width of basins
  (sandbox envelopes, kill criteria, escalation thresholds), not the position of the system.

## Layer 4: portfolio selection with chaos machinery (financial, not projects)

- **Spelta, A., Pecora, N., Pagnottoni, P. (2022). "Chaos based portfolio selection: A nonlinear
  dynamics approach." *Expert Systems with Applications* 188: 116055.** Verified (ScienceDirect
  DOI 10.1016/j.eswa.2021.116055; ~33 citations). Methodology based on chaos and dynamical
  systems theory for portfolio selection. The only found paper that runs attractor/dynamics
  machinery on an actual selection problem, but for investment portfolios.
- **Peters, E.E. *Chaos and Order in the Capital Markets* (Wiley, 1st ed 1991, 2nd ed 1996,
  ISBN 9780471139386) and *Fractal Market Analysis: Applying Chaos Theory to Investment and
  Economics* (Wiley, 1994).** Verified existence and publisher via Wiley/Open Library/Semantic
  Scholar listings. The practitioner canon for chaos metrics (R/S analysis, fractal dimension)
  on markets. Note these books are contested science for markets, cited here as the
  application canon, not as validated theory.

## Layer 5: the project and multi-project layer (closest to the ask)

- **Pich, M.T., Loch, C.H., De Meyer, A. (2002). "On Uncertainty, Ambiguity, and Complexity in
  Project Management." *Management Science* 48(8): 1008-1023.** Verified (INFORMS DOI
  10.1287/mnsc.48.8.1008.163, ~1,500 citations). The mainstream formal treatment of project
  uncertainty: variation / foreseen uncertainty / unforeseen uncertainty / ambiguity / complexity,
  each mapped to a management strategy (instruction, learning, selectionism). Not
  attractor-based, but it is the discipline's formal answer to bounded unpredictability, and the
  baseline any attractor treatment must beat.
- **Cooke-Davies, T., Cicmil, S., Crawford, L., Richardson, K. (2007). "We're not in Kansas
  Anymore, Toto: Mapping the Strange Landscape of Complexity Theory, and its Relationship to
  Project Management." *Project Management Journal* 38(2): 50-61.** Verified (ResearchGate,
  Bond University repository, citing journals). Landmark mapping of complexity theory onto
  project management; expanded into Cicmil, Cooke-Davies, Crawford & Richardson (2009),
  *Exploring the Complexity of Projects* (Project Management Institute). Conceptual, not
  mathematical.
- **Geraldi, J.G. (2008). "The balance between order and chaos in multi-project firms: A
  conceptual model." *International Journal of Project Management* 26(4): 348-356.** Verified
  (citation found in an ASCE library reference: DOI 10.1016/j.ijproman.2007.08.004). **This is
  the closest single hit for the ask.** A conceptual model of multi-project firms balancing
  order and chaos (edge-of-chaos framing); a ResearchGate search snippet attached mentions of
  strange attractor, Lyapunov exponent, and correlation dimension to this paper (snippet-level
  only: OWED-4). A follow-on, Geraldi (2009) "Reconciling order and chaos in multi-project
  firms," *International Journal of Managing Projects in Business* 2(1): 149-158, surfaced in
  the same search summary (snippet-level: OWED-4).
- **Braha, D., Bar-Yam, Y. (2007). "The Statistical Mechanics of Complex Product Development:
  Empirical and Analytical Results." *Management Science* 53(7): 1127-1145.** Verified (INFORMS
  DOI 10.1287/mnsc.1060.0617, NECSI, JSTOR). Formal (statistical-mechanics) treatment of real
  development task networks; the rigorous end of engineering-development dynamics, though its
  formalism is networks, not attractors.
- **Repenning, N.P. (2001). "Understanding Fire Fighting in New Product Development."
  *Journal of Product Innovation Management* 18(5): 285-300** (verified, MIT DSpace full text,
  ~420 citations) **and Repenning & Sterman (2001). "Nobody Ever Gets Credit for Fixing Problems
  that Never Happened." *California Management Review* 43(4): 64-88** (verified). System-dynamics
  formal models of development dynamics: the "tilting" resource-shift reinforcing loop and the
  capability trap. Dynamical-systems thinking applied to development, with state-space traps one
  step removed from attractor language (the trap language is theirs; the attractor reading is my
  interpretation, not their claim).
- **Dixit, A.K., Pindyck, R.S. (1994). *Investment under Uncertainty*. Princeton University
  Press.** Verified (Princeton UP, free PDF, JSTOR). Real-options theory of irreversible
  investment: the mainstream formal treatment of bounded-unpredictability in portfolio decisions
  (value of waiting under irreversibility). Included as the incumbent any attractor-based
  portfolio policy would compete with.

## Layer 6: the conceptual / popular layer (verified existence, not formal)

- **Stacey, R.D. (1996). *Complexity and Creativity in Organizations*. San Francisco:
  Berrett-Koehler.** Verified via multiple secondary citations (a 2017 Antioch dissertation, a
  leadership-practice review citing it for self-organization around attractors); his later
  *Complexity and Organizational Reality* carries an index entry "attractor strategies"
  (Google Books). Also: Stacey et al, *Complexity and Organization: Readings and Conversations*
  (Routledge, 2006) with an "Attractor of Meaning" concept (b-m-institute PDF). Conceptual
  frameworks, not mathematics.
- **Gilstrap, D.L. (2005). "Strange Attractors and Human Interaction: Leading Complex
  Organizations Through the Uncharted." *Complicity: An International Journal of Complexity and
  Education*.** Verified (open access at journals.library.ualberta.ca). Directly uses point,
  cyclic, and strange attractors for organizational leadership.
- **Wheatley, M.J. (1992). *Leadership and the New Science: Discovering Order in a Chaotic
  World*. Berrett-Koehler (3rd ed 2006).** Verified (author site, reviews). The popular
  chaos-to-management bridge; metaphor level, frequently criticized as loose with the physics.
- **Curlee, W., Gordon, R.L. (2013). *Successful Program Management: Complexity Theory,
  Communication, and Leadership*. CRC Press, ISBN 9781466568792, DOI 10.1201/b15925.** Verified
  existence, publisher, ISBN/DOI (CRC/Barnes & Noble/Semantic Scholar). One search summary
  described it as applying Lorenz attractors to program management (snippet-level only:
  OWED-2).
- **Galacgac (2016), "Implications of Chaos Theory in Management Science," CMSIM** and
  **"The utopia of order versus chaos: A conceptual framework for governance, organizational
  design and governmentality in projects" (ResearchGate)**: surfaced once each at snippet level,
  not independently verified beyond that (OWED-5).

## Gap analysis: what "attractor shapes as policy" would need

No found source does the specific move of: (a) modeling a project/R&D portfolio's composition or
cadence as a state trajectory, (b) estimating its dynamical invariants (lambda1, dimension,
attractor geometry) from portfolio telemetry, (c) then making policy acts that reshape the
attractor (basin width = sandbox budget envelope, basin depth = sunk-cost resistance,
thresholds = kill/escalate criteria). The pieces exist separately: Wolf et al give (b) for time
series, Walker et al give (c) for ecological governance, Levinthal/Rivkin give basin-shaped
search in strategy, Geraldi gestures at the balance conceptually, Spelta does (a)+(b) only for
financial portfolios. Assembling them for engineering portfolios appears to be open territory.
Caveat: this absence claim is bounded by the queries listed below, not by an exhaustive survey.

## OWED ledger (unverified or snippet-level)

1. **OWED-1, full texts:** none of the papers above were fetched and read in full this session;
   all bibliographic details come from publisher/repository/index listings returned by search.
   Page-level quotes exist only where the search output itself quoted text (noted inline, e.g.
   Wolf et al). The Lorenz 1963 and Wolf 1985 full-text PDFs were located (cdanfort.w3.uvm.edu,
   hal.science) but not fetched.
2. **OWED-2:** the claim that Curlee & Gordon (2013) applies Lorenz attractors to program
   management came from one search summary; the verified publisher description mentions only
   complexity theory, communication, leadership. Treat the attractor-specific claim as unconfirmed.
3. **OWED-3:** Siggelkow & Rivkin (2006) and Dosi et al (2015/2017) basin-of-attraction language
   verified only from search-result snippets, not from the papers.
4. **OWED-4:** the association of strange attractor / Lyapunov exponent / correlation dimension
   with Geraldi (2008) came from a ResearchGate search snippet, and the 2009 follow-on paper's
   details from a search summary. Verify against the paywalled full texts before relying on them.
5. **OWED-5:** Galacgac (2016, CMSIM) and the "utopia of order versus chaos" project-governance
   paper: titles/venues from search snippets only.
6. **OWED-6:** the predictability-horizon formula t ~ (1/lambda1) ln(C/delta) was stated in
   search output via lecture notes citing Wolf et al; verify the exact form against the primary
   or a dynamics textbook if it is to be quoted formally.

## Method note

Research run 2026-09-28 by gopher r-attractor-portfolio inside the Mag Resource Harness repo,
using the WebSearch tool (15 queries, backend Z.ai web_search_prime; intermittent 1302
rate-limit responses, resolved by retry). Queries, in order: chaos attractors + project portfolio
management formal treatment; Levy 1994 chaos theory and strategy; Cooke-Davies "We're not in
Kansas anymore"; basin of attraction NK landscape Kauffman Rivkin; Pich Loch De Meyer 2002;
Spelta 2022 chaos based portfolio selection; Rivkin 2000 + Levinthal 1997; Holling 1973 +
Walker 2004 resilience basins; Wolf et al 1985 Lyapunov predictability horizon; Stacey attractor
organizations; Curlee Gordon program management complexity; project/R&D portfolio strange
attractor engineering management; Geraldi balance order chaos multi-project; Braha Bar-Yam
statistical mechanics product development; Repenning firefighting + Dixit Pindyck 1994; Peters
capital markets fractal; Lorenz 1963 deterministic nonperiodic flow; Wheatley leadership new
science. No local corpus search was run and no full-text fetches were made; this item is
external-literature research. Negative findings are stated against these queries only.
