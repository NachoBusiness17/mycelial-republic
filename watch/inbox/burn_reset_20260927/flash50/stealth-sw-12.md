# stealth-sw-12: Biological network metaphors in distributed computing (mycelium, slime mold, coral)

Provenance: research ask sw-12, 2026-09-28, seat stealth-sw-12. Method: 10 WebSearch queries (search backend hit 1302 rate limits twice mid-session, cleared on retry per the estate's HOLD-on-first-contact law), plus direct repo reads (ls, grep -n, wc) for the in-repo example. No paper full texts fetched this session: every external claim is pinned to what search surfaced (title, author, year, citation count as reported). Claims marked [snippet] rest on the search result summary alone.

## 1. Slime mold (Physarum polycephalum): the deepest metaphor-to-algorithm line

Origin pair:

- Nakagaki, Yamada and Toth (2000), "Intelligence: Maze-solving by an amoeboid organism", Nature 407(6803):470, one page. A single-celled slime mold reorganizes its plasmodial tube network to find the shortest maze path. Citation string verified from a scitepress.org reference list in search results.
- Tero et al. (2010), "Rules for Biologically Inspired Adaptive Network Design", Science, doi 10.1126/science.1177894, cited ~1,444 per search. Physarum grown on oat flakes placed at Tokyo subway station locations produced a network statistically comparable to the real rail system (total length 1.75 +/- 0.30 times the minimum spanning tree over 21 trials, vs the real system's ~1.8), then the behavior was distilled into a mathematical model: tube conductance grows with flux and decays without it. This model is the "Physarum solver".

Who turned it into distributed-systems machinery:

- IEEE Transactions on Computers 64(3) pp 819-832, "Physarum optimization: a biology-inspired algorithm for the Steiner tree problem in networks" [snippet, surfaced via an ACM paper's reference list]. The standard bridge from biology to provable network-design algorithms.
- "Physarum-Inspired Enterprise Network Redesign" (ResearchGate) [snippet]: a redesign algorithm for existing enterprise networks minimizing traffic, using slime-mold network formation principles.
- PANDA, a Physarum-inspired algorithm for the Multi-Objective Discrete Network Design Problem (ACM/Expert Systems) [snippet]; a multi-agent Physarum simulation applied to multimodal transportation planning (rishivanukuru.com) [snippet].
- PR-APC (Physarum Routing based Adaptive Power Control), Physarum routing optimization for obstacle-heavy wireless scenarios [snippet].
- X. Zhang (2014), improved Physarum algorithm (PMC, cited 50): faster convergence than prior Physarum-inspired approaches. Search returned a domain-level PMC link only, full URL not surfaced.
- Living hardware: EU project PhysarumChip, "Growing Computers from Slime Mould", led by Andrew Adamatzky (UWE Bristol); Adamatzky, Erokhin, Grube, Schubert and Schumann (2012), Int. J. Unconventional Computing. Whiting et al. (2014, cited 74) define a Physarum chip as "a network of processing elements made of the slime mould's protoplasmic tubes coated with conductive substances". Adamatzky's "Physarum Machines" frame the plasmodium as a programmable amorphous biological computer (maze solving, transport networks, sensing).
- Robotics and swarm networks: D. Martinelli (2025, Nature-hosted) Physarum bioinspired decentralized coordination in multi-robot systems, simulated port scenario [snippet]; E.H. Vergara (2025, bncss.org) Physarum-inspired parallel, i.e. distributed, routing for cave and catacomb navigation [snippet]; Agnes Cameron (agnescameron.info), cellular-automata slime mould models for studying self-organising swarm networks [snippet]; Y. Sun's review "Physarum-inspired Network Optimization" (yahuisun.github.io, cited 17) as the field overview.

Verdict: slime mold is the only one of the three with the complete arc: organism experiment, then math model, then provable network algorithm, then applied redesigns of real infrastructure, then living computing substrate.

## 2. Mycelium: robust transport biology, thinner protocol record

Biology anchor: Fricker et al. (2017), "The Mycelium as a Network" (PMC11687498, cited 216): fungal mycelia as interconnected transport networks whose growth pattern shapes transport and cellular events. The paper biologists cite when engineers borrow the metaphor.

Direct uses to design systems:

- Routing protocol: "A Novel Bio-inspired Trusted Routing Protocol for Mobile Wireless Sensor Networks" (ResearchGate) [snippet]: reproduces fungal mycelium expansion to derive low-stretch Steiner graphs with self-healing shortcuts, combined with trust mechanisms. The clearest case found where mycelium growth dynamics were engineered into a routing algorithm rather than name-checked.
- Computation framing: "Mycorrhizal Networks as Distributed Computational Systems" (Scribd-hosted) [snippet only; author and venue UNVERIFIED because the verification query hit persistent 1302 rate limits]: presents a formal computational framework modeling mycorrhizal networks as distributed computing systems that solve optimization problems. Treat as a lead, not a confirmed citation.
- Fungal computing: Adamatzky (2022), "Logics in Fungal Mycelium Networks" (Springer): decision-making in fungal networks modeled as Boolean gates and logical computation.

In-repo example (first-hand, lines read this session): this harness is itself a mycelium-designed distributed agent system. docs/ref/MYCELIAL_SCIENCE_MAP.md (242 lines, verified by wc): line 49 maps Hypha to "one REST hop or one handoff file, single seat action"; line 50 maps Mycelium to "the seat graph: Grok, Cursor, Ollama, DeepSeek, janitor, scheduler"; line 94 maps lateral hyphal fusion to REST handoffs between seats; lines 109-114 define the hypha_plan_down / hypha_problem_up / hypha_prune verbs; line 58 maps hyphal self-repair ("regrow around damage") to desk auto-heal and the improve loop. docs/ref/MAG_MYCELIAL_REPUBLIC_COMPASS.md line 34 opens "Vision - Mycelial Republic"; line 254: "law and loops on your disk - agents that coordinate through files". Here the metaphor is load-bearing, not decorative: no central organ, tiered hyphal tips that explore and exit, prune verbs for abandoned routes, file-surface coordination instead of a coordinator.

Verdict: as engineering method, mycelium yielded one real routing-protocol family plus fungal-logic computing; as institutional design metaphor for distributed systems it is far more widespread (this repo included) than it is as an algorithm.

## 3. Coral: population-based placement and task allocation

- Salcedo-Sanz et al. (2014), "The Coral Reefs Optimization Algorithm: a novel bioinspired metaheuristic" (Wiley; free at PMC4132328), cited 300+ per search: simulates reef formation (larvae settling, sexual and asexual reproduction, depredation) as a population optimizer. Official page maintained at University of Alcala (agamenon.tsc.uah.es).
- CRO-SL, the substrate-layers variant for large-scale global optimization (sci2s.ugr.es, cited ~65).
- Network-flavored applications: CRO for mobile network deployment with electromagnetic-pollution control (ResearchGate 264386476); CRO for optimal service placement in network deployment minimizing investment cost (scispace) [snippet]; statistically-driven CRO for time series reduction (Duran-Rosal et al. 2018, cited 41).
- Distributed swarms: Ramesh et al. (2025), MDPI Journal of Marine Science and Engineering, comprehensive review of bio-inspired underwater swarm robotics: frames CRO as adaptive task allocation "through competitive reef dynamics, where corals vie for space based on fitness" [snippet]. Context neighbors in the same review: artificial fish swarm, whale optimization; foundational stigmergy-based multi-robot coordination sits in the same literature (Hsieh 2008 biologically inspired swarm redistribution, cited 149).

Verdict: coral is the weakest of the three as distributed-systems design and the strongest as a population and competition metaphor for placement, scheduling, and task allocation. Nothing surfaced where a coral reef's structural topology, as opposed to its competitive ecology, shaped a protocol.

## 4. Cross-cutting synthesis

- Strength ordering for actual distributed-systems artifacts: slime mold (routing and topology, with convergence results and real infrastructure redesigns) > mycelium (one routing protocol family, plus a real deployed agent harness using it institutionally) > coral (optimization metaheuristics for placement and allocation, no protocol record surfaced).
- The common mechanism all three export: local rules, no central controller, links reinforced or pruned by usage. That is also exactly the shape of swarm fan-out architectures, including this estate's own dispatch laws: width without a coordinator, backpressure on first rate-limit contact.
- Session note: the search lane's 1302/429 contact matches the ENVELOPE_50W finding in this repo (watch/inbox/ENVELOPE_50W_HIT_20260926.md): rolling throughput cap, HOLD and retry, not a width problem. No search data lost.

## Honest gaps

- No paper full texts fetched this session; everything external is search-snippet or citation-string level and marked as such.
- Author and venue of "Mycorrhizal Networks as Distributed Computational Systems" unverified (rate-limited); flagged above rather than filled in.
- Mirjalili's Slime Mould Algorithm metaheuristic is known to the field but was not surfaced or verified this session, so it is deliberately excluded.
- Name-coincidence systems (e.g. CoralCDN, Mycelium wallet) excluded absent a biological design rationale in anything surfaced this session.

## Sources (surfaced by search this session)

- https://www.science.org/doi/10.1126/science.1177894 (Tero 2010) and https://pubmed.ncbi.nlm.nih.gov/20093467
- https://yahuisun.github.io (Physarum-inspired network optimization review)
- https://pmc.ncbi.nlm.nih.gov (Zhang 2014 improved Physarum; domain-level link only)
- http://www.bncss.org (Vergara 2025 cave routing) and https://agnescameron.info (slime mould cellular automata)
- https://pmc.ncbi.nlm.nih.gov/articles/PMC11687498 (Fricker 2017)
- https://link.springer.com/article/10.1007/s11787-022-00318-4 (Adamatzky 2022 fungal logics)
- https://www.scribd.com/document/1073945294/Mycorrhizal-Networks-as-Distributed-Computational-Systems (unverified authorship)
- https://www.researchgate.net/publication/278077949 (mycelium-expansion trusted routing for MWSN)
- https://onlinelibrary.wiley.com/doi/abs/10.1155/2014/739768 and https://pmc.ncbi.nlm.nih.gov/articles/PMC4132328 (Salcedo-Sanz 2014 CRO)
- http://agamenon.tsc.uah.es/Personales/sancho/CRO.html (official CRO page)
- https://sci2s.ugr.es/sites/default/files/ficherosPublicaciones/2352_07744242.pdf (CRO-SL)
- https://www.mdpi.com/2077-1312/14/1/59 (Ramesh 2025 underwater swarm review)
- https://www.researchgate.net/publication/264386476 (CRO mobile network deployment)
- https://scispace.com/papers/a-coral-reef-optimization-algorithm-for-the-optimal-service-3j0u54juj (CRO service placement)
- https://www.sciencedirect.com/science/article/abs/pii/S1568494617307007 (Duran-Rosal 2018)
- https://users.cs.fiu.edu/~iyengar/images/publications/Bio_Ins_Routing.pdf (Iyengar 2007, context)
- https://asknature.org (two accessible overviews: Physarum smart networks, fungal resource distribution)
