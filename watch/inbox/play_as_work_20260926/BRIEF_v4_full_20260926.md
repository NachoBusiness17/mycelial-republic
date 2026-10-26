# Research Brief: Endogenous Capability Accumulation in Computational Games — v4.0 (verbatim capture)

**Provenance (2026-09-26, zcode-seat):** Generated in a DeepSeek session (share: https://chat.deepseek.com/share/wq0vlxko6mufedlxkh) through 5 operator-directed prompt turns (link-drop v1 -> expanded v2 -> game-theory gap fill -> journal-quality Socratic triangulation -> this v4.0 formalized reframe). Operator pasted the full text into the ZCode session mid-turn across two pastes. Stitch: paste 1 ran through the truncated opening of §7.3 Question 6; paste 2 repeats §7.3 Aporia in full and carries everything through §9 References. Overlap disclosed, no editorial repair. Source punctuation (including em-dashes and LaTeX markup) preserved byte-faithful; it is quoted artifact, not seat-authored prose. DeepSeek renders share pages client-side so the share URL did not yield full text to this seat; this file is the byte copy of what the operator pasted.

**Status: UNVERIFIED CITATION LAYER.** Two citation IDs in §9 were checked live 2026-09-26 and DO NOT match their claims (arXiv:2502.04223 = an OCR paper; arXiv:2509.06636 = a spiking-network paper). See STEAL_RECEIPT_20260926.md in this directory for the verification ledger before reusing any reference.

---

Version: 4.0 (Journal-Quality, Formalized and Reframed)
Target Audience: LLM research agents, computational social scientists, game theorists, mechanism design practitioners
Organizing Thesis: The subject of this research programme is not gamification. It is endogenous capability accumulation in computational games — the design of systems in which intrinsically motivated exploration produces verified, reusable capability as its natural byproduct.

---

## Abstract

This brief formalizes the play-as-work hypothesis as a dynamic game with endogenous action-space expansion. We separate the state into four components — competence X_t, knowledge K_t, reusable artifacts R_t, and environment E_t — and define compilation as a specific transition from verified traces to executable primitives. We introduce three operational metrics (Compilation Gain, Capability Expansion, Artifact Reuse) and one adversarial metric (Negative Compilation) that turn the conceptual Gap 8 into an experimental programme. We correct the utility decomposition to avoid notation collision, replace the additive play threshold with a conjunctive formulation, and strengthen the Socratic protocol against its own escape hatch. We propose a four-arm experiment whose crucial comparison is Play vs. Compiling Play, not Work vs. Gamification. We extend the play-as-work loop to include a Challenge → Retain/Revise/Forget phase that Factorio itself does not provide, and which we argue is the specific contribution of the MAG architecture. Factorio is demoted from centerpiece to canonical motivating example.

---

## 1. Introduction: From Play-as-Work to Endogenous Capability Accumulation

The claim that play is the highest form of work is not merely philosophical. It is an empirical hypothesis about incentive alignment. When a system's equilibrium structure makes productive contribution the best response for each participant — and when successful play expands the space of future productive actions — play and work become indistinguishable in the only sense that matters: the system produces verified capability as a byproduct of voluntary activity.

The central design question is therefore not:

"How do we make work feel like play?"

It is:

\boxed{\text{How do we design a system in which intrinsically motivated exploration produces verified, reusable capability as its natural byproduct?}}

This reframes the research programme. The object to be designed is not a gamified workflow but a computational game with endogenous capability accumulation: a dynamic environment in which successful play modifies the future action space, and in which verification prevents successful play from silently becoming permanent authority.

Factorio is the canonical motivating example — the cleanest existing demonstration that cognitive work can be compiled into durable machinery while remaining voluntary. GWAPs are the canonical human-computation example. Potential games supply distributed coordination theory. CSRO supplies strategy-as-executable-artifact. LegoNE supplies generation-under-formal-verification. And the MAG architecture supplies something none of the others do: continuous adversarial revalidation of compiled capability.

The organizing thesis of this brief is that these are not adjacent analogies. They are fragments of a single research programme on endogenous capability accumulation.

---

## 2. Formal Framework: The Skill-Compilation Game

### 2.1 State Space

We reject the compression of capability, knowledge, and artifacts into a single K_t. The state at time t is:

S_t = (X_t, K_t, R_t, E_t)

where:

· X_t — agent competence / internal state: skills, policies, learned representations, model weights
· K_t — acquired knowledge: facts, maps, discovered invariants, domain information
· R_t — executable reusable artifacts: tools, functions, compiled routines, callable primitives
· E_t — environment state: the world, other agents, available resources

This separation is not cosmetic. It distinguishes three phenomena that are currently conflated under "skill compilation":

| Change | Interpretation |
|---|---|
| \Delta X \neq 0, \Delta K = 0, \Delta R = 0 | Learning — the agent got better |
| \Delta X = 0, \Delta K \neq 0, \Delta R = 0 | Discovery — the agent found information |
| \Delta X = 0, \Delta K = 0, \Delta R \neq 0 | Compilation — yesterday's expensive reasoning becomes tomorrow's callable primitive |

The third transition is the MAG-relevant phenomenon. It is also the phenomenon Factorio demonstrates most cleanly: the player does not merely get better at mining; the player constructs a mining drill so that mining no longer requires player attention.

### 2.2 Dynamics

At each time t:

a_{i,t} \in A_i(S_t)

S_{t+1} = F(S_t, a_t, \omega_t)

where \omega_t is exogenous stochasticity. The action space itself depends on the state:

A_i(S_t) = A_i(X_t, K_t, R_t, E_t)

Crucially, R_t appears in the action space. A compiled artifact r \in R_t is a new available action that was not available at t-1. This is what makes the game endogenous: playing the game changes the game you are capable of playing.

### 2.3 Compilation as a Specific Transition

We define compilation as a transition operator:

C: (\text{trace}, \text{outcome}, \text{verification}) \rightarrow r \in R_{t+1}

The trace is the recorded sequence of actions and observations. The outcome is the observed result. The verification is the evidence that the trace-outcome pair is correct, generalizable, and safe to reuse.

The requirement of verification is what distinguishes compilation from mere caching. A cached trace is not a compiled artifact; it is a memory. A compiled artifact is a trace that has been certified to be reusable.

Formally:

C(\tau, o, v) = r \quad \text{iff} \quad v(\tau, o) = \top

where v is a verifier drawn from the system's verification apparatus (tests, receipts, formal checkers, counterfactual replays).

### 2.4 Operational Metrics

The objective

\frac{\text{future capability}}{\text{present cognitive effort}}

requires operationalization. We propose four metrics.

**Compilation Gain.** For a compiled artifact r over a task distribution T:

CG(r) = \frac{\mathbb{E}\left[C_{\text{baseline}}(T) - C_{\text{with } r}(T)\right]}{C_{\text{compile}}(r)}

where C_{\text{baseline}}(T) is the expected reasoning/computation cost on T without r, C_{\text{with } r}(T) is the cost with r available, and C_{\text{compile}}(r) is the cost of discovering, validating, and maintaining r. A compiled skill is valuable when the future reasoning it saves exceeds the cost of producing and maintaining it.

**Capability Expansion.** At time t:

CE_t = \left| A(S_{t+1}) \setminus A(S_t) \right|

or, in a weighted form that measures the value of newly reachable states rather than merely counting actions:

CE_t^w = \sum_{a \in A(S_{t+1}) \setminus A(S_t)} w(a)

where w(a) is the expected value of action a in the task distribution.

**Artifact Reuse.**

AR(r) = \frac{\text{successful downstream invocations of } r}{\text{eligible downstream situations}}

Reuse is the empirical signature of compilation. An artifact with AR(r) \approx 0 was not compiled; it was archived.

**Negative Compilation.** The adversarial metric:

NC(r) = \mathbb{E}\left[ L_{\text{with } r}(T_{\text{OOD}}) - L_{\text{baseline}}(T_{\text{OOD}}) \right]

where T_{\text{OOD}} is an out-of-distribution task set and L is loss. A strategy can work repeatedly in one region, become a skill, and subsequently create systematic errors elsewhere. This is negative transfer, and it must be measured. A system that compiles without measuring NC(r) is not accumulating capability; it is accumulating liability.

### 2.5 Utility Decomposition (Corrected Notation)

The earlier version used A_i for both agency/autonomy and action space. We rename agency to \alpha_i to eliminate the collision:

U_i(a, s) = E_i(a, s) + I_i(a, s) + \alpha_i(a, s) + L_i(a, s) - C_i(a, s)

where:

· E_i = extrinsic reward
· I_i = intrinsic enjoyment
· \alpha_i = agency / autonomy
· L_i = learning / mastery
· C_i = effort / friction / cost

System productivity is defined separately:

W(s) = Q(s) + K(s) + R(s)

where Q is useful output, K is knowledge produced, and R is reusable artifacts produced.

### 2.6 The Play Condition (Conjunctive, Not Additive)

The earlier formulation I_i + \alpha_i + L_i > \tau presupposes additive substitutability: enormous learning could theoretically compensate for zero enjoyment and zero autonomy. That is not what "play" means. A coercive environment with high learning outcomes is not play; it is coerced training.

We therefore propose a conjunctive formulation:

I_i > \tau_I \quad \text{and} \quad \alpha_i > \tau_\alpha

with L_i as an additional benefit rather than a compensating term. Learning and mastery can accompany play; they cannot launder coercion into play.

This creates an empirical question rather than burying the answer in a definition: are there domains in which I_i > \tau_I, \alpha_i > \tau_\alpha, and high W(s) are jointly achievable? The research programme exists to answer this experimentally.

---

## 3. Gap Analysis: What the Literature Omits

The seven gaps identified in v3 remain valid. We present them in compressed form and add Gap 8, now formalized.

**Gap 1: Incentive-Compatibility in GWAPs**

Filling: Jain and Parkes (2013) model the ESP game as a two-stage game of incomplete information. Under match-early preferences, low effort is a Bayesian-Nash equilibrium for all distributions on word frequencies. Under rare-words-first preferences, the equilibrium shifts toward harder images. Small changes in incentive structure shift equilibrium.

Citation: Jain, S., & Parkes, D. C. (2013). ACM Transactions on Economics and Computation, 1(1), 3:1–3:35.

**Gap 2: Mechanism Design for Human Computation**

Filling: Kang et al. (2023) model platform-worker interaction as a Stackelberg game and derive the Nash Equilibrium.

Citation: Kang, X., et al. (2023). AAAI, 37(5), 6021–6029.

**Gap 3: Equilibrium Analysis of Software Teams**

Filling: Hazzan and Dubinsky (2005) propose software team cooperation as a Prisoner's Dilemma. Rass and Pinzger (2023) apply the Shapley value to fair micro-payments for secure code.

Citations: Hazzan & Dubinsky (2005), XP 2005, LNCS 3556, 74–81; Rass & Pinzger (2023), GameSec 2023.

**Gap 4: Task Allocation as a Potential Game**

Filling: Chapman et al. (2009) formulate dynamic task allocation as a Markov game approximated by static potential games. Monderer and Shapley (1996) established that every finite potential game is isomorphic to a congestion game.

Hypothesis H-TA1: Under specified restrictions on developer expertise X, merge-conflict costs C, and communication costs M, the developer-module allocation game admits an exact or ordinal potential.

Citations: Chapman et al. (2009), AAMAS 2009; Monderer & Shapley (1996), Games and Economic Behavior, 14(1), 124–143.

**Gap 5: Code Review as a Social Dilemma**

Hypothesis H-CR1: Under specified review-cost and defect-loss inequalities, voluntary code review induces a snowdrift payoff structure.

Citation: Naserameri, M. (2026). arXiv:2607.27310.

**Gap 6: Strategic AI Agents in Game Environments**

Filling: Garcia Segura et al. (2026) on opponent shaping with LLM agents; Hennes et al. (2026) on Code-Space Response Oracles; Li et al. (2026) on LegoNE, which rediscovered the state-of-the-art two-player ANE algorithm in two rounds and improved the three-player guarantee from 0.6+\delta to 0.5+\delta.

Citations: Garcia Segura et al. (2026), ICLR 2026; Hennes et al. (2026), AAMAS 2026; Li et al. (2026), Nature Communications.

**Gap 7: The Philosophical Foundation**

Filling: Hinman (1978) argues that unalienated praxis is free, creative activity in which the split between intrinsic and extrinsic value has been overcome. Play's value is intrinsic; alienated labor's value is extrinsic; the distinction loses its foundation in Marx's envisioned post-capitalist society.

Citation: Hinman, L. M. (1978). Philosophy and Social Criticism, 5(2), 192–228.

**Gap 8: Endogenous Skill Compilation (Formalized)**

Ordinary game theory gives G = (N, A, U) with static action spaces. Factorio-like systems are not static. Playing changes the game you are capable of playing. This is formalized in §2. The three metrics (CG, CE, AR) and the adversarial metric (NC) turn this from a conceptual contribution into an experimental programme.

---

## 4. The Four-Arm Experiment

The central empirical question is not whether gamification improves productivity. It is whether compilation of verified play produces greater long-run capability per unit cognitive cost than play alone, without degrading voluntary engagement.

### 4.1 Design

Randomly assign identical tasks to four conditions in the Grey Swan Arena (or an equivalent controlled environment):

| Arm | System | Description |
|---|---|---|
| A | Work | Explicit tasks + extrinsic objective |
| B | Gamification | A + points/ranks/rewards |
| C | Play | Autonomy/exploration, no skill compilation |
| D | Compiling Play | C + verified successful strategies become reusable capabilities |

### 4.2 Measures

· Productive output Q
· Knowledge produced K
· Reusable artifacts R
· Voluntary continuation
· Intrinsic-motivation measures I_i, \alpha_i
· Reasoning/computational cost C
· Verification rate v
· Transfer to novel tasks
· Compiled-artifact reuse AR(r)
· Capability expansion CE_t
· Negative compilation NC(r)

### 4.3 The Crucial Comparison

The comparison of interest is not A vs. D. The comparison of interest is C vs. D.

If D produces greater long-run capability per unit cognitive cost without degrading voluntary engagement, the result is:

\boxed{\text{Play} + \text{Compilation} > \text{Play alone}}

on defined productivity and capability measures. This is a much more specific claim than "games motivate people." It is a claim about the incremental value of compilation as a mechanism layered on top of play.

### 4.4 Distinguishing Mechanism Failure from Fundamental Incompatibility

The four-arm experiment also provides leverage on a question the earlier Socratic protocol wrongly foreclosed. Two rival hypotheses:

· H-MD (Mechanism Design failure): GWAP failures are caused by poorly designed incentive structures and are fixable.
· H-FI (Fundamental Incompatibility): Some domains have no payoff structure under which useful computation and sustained intrinsic motivation are jointly achievable.

The four-arm design can distinguish these. If Arm D consistently outperforms Arm C across many domains, H-MD is supported. If there exist domains where no configuration of Arm D produces both high W and sustained I_i > \tau_I, \alpha_i > \tau_\alpha, H-FI gains support for those domains. The research programme's job is to map the boundary.

---

## 5. Negative Compilation and the Challenge Phase

A system that compiles without adversarial revalidation is not accumulating capability; it is accumulating authority. The distinction matters because compiled artifacts can become systematically wrong in ways their original verification did not catch.

### 5.1 Negative Compilation

NC(r) = \mathbb{E}\left[ L_{\text{with } r}(T_{\text{OOD}}) - L_{\text{baseline}}(T_{\text{OOD}}) \right]

A compiled artifact with NC(r) > 0 is actively harmful outside its training distribution. The system must measure this and act on it.

### 5.2 The Challenge → Retain/Revise/Forget Phase

Factorio's loop stops at Reuse. The MAG loop continues:

\boxed{
\text{Explore}
\rightarrow \text{Act}
\rightarrow \text{Observe}
\rightarrow \text{Verify}
\rightarrow \text{Compile}
\rightarrow \text{Reuse}
\rightarrow \text{Challenge}
\rightarrow \text{Retain/Revise/Forget}
}

The Challenge phase subjects compiled artifacts to adversarial revalidation. The Retain/Revise/Forget decision determines whether the artifact survives, is modified, or is retired. This connects directly to the Model Garden, the forgetting mandate, and the principle that successful historical behavior must not silently become permanent authority.

This final segment is what Factorio itself does not give you. Factorio demonstrates automation capital. GWAPs demonstrate incentive-compatible human computation. Potential games give distributed coordination. CSRO gives strategy as executable artifact. LegoNE gives generation under formal verification. Grey Swan gives controlled adversarial experimentation. MAG's potential contribution is the complete lifecycle, including the adversarial revalidation that prevents compiled capability from becoming compiled liability.

---

## 6. Trajectory Map: From Gap to Research Programme

### Phase 1: Foundation (Weeks 1–4)

| Step | Task | Deliverable |
|---|---|---|
| 1.1 | Reproduce Jain & Parkes ESP equilibrium analysis | Simulation + equilibrium verification |
| 1.2 | Implement iFedCrowd Stackelberg solver | Python Nash Equilibrium derivation |
| 1.3 | Build Prisoner's Dilemma software team model | Agent-based cooperation collapse simulation |

### Phase 2: Extension (Weeks 5–8)

| Step | Task | Deliverable |
|---|---|---|
| 2.1 | Implement Shapley value micro-payments | Git-integrated incentive calculator |
| 2.2 | Test H-CR1 (snowdrift code review) | Payoff inequalities + falsification |
| 2.3 | Test H-TA1 (potential task allocation) | Potential function derivation |

### Phase 3: Skill Compilation (Weeks 9–12)

| Step | Task | Deliverable |
|---|---|---|
| 3.1 | Implement Skill-Compilation Game simulator | Dynamic action-space expansion model |
| 3.2 | Deploy CSRO for policy generation | LLM-synthesized executable policies |
| 3.3 | Integrate LegoNE for verification | Formal certification pipeline |
| 3.4 | Instrument CG, CE, AR, NC | Measurement infrastructure |

### Phase 4: Experimentation (Weeks 13–20)

| Step | Task | Deliverable |
|---|---|---|
| 4.1 | Deploy four-arm experiment | Grey Swan Arena protocol |
| 4.2 | Test C vs. D | Play + Compilation > Play alone |
| 4.3 | Map H-MD / H-FI boundary | Domain classification |
| 4.4 | Implement Challenge → Retain/Revise/Forget | Adversarial revalidation pipeline |

### Phase 5: Synthesis (Weeks 21–24)

| Step | Task | Deliverable |
|---|---|---|
| 5.1 | Formalize unalienated praxis as equilibrium selection | Mathematical framework paper |
| 5.2 | Longitudinal Factorio-trained developer study | Transfer effects |
| 5.3 | Publish open-source play-as-work toolkit | GitHub repository |

---

## 7. Socratic Protocol (Corrected)

### 7.1 The Elenchus

**Question 1: If play is the highest form of work, why do most GWAPs fail?**

Corrected Triangulation: GWAP failure does not by itself distinguish mechanism failure from a fundamental incompatibility between productive computation and sustained intrinsic motivation. The research programme must distinguish these hypotheses experimentally. Some failures may be mechanism-design failures; others may mark domains where no payoff structure jointly achieves high W and sustained I_i > \tau_I, \alpha_i > \tau_\alpha. The four-arm experiment is designed to tell these apart.

**Question 2: If play is work, why does Marx describe alienated labor as the opposite of play?**

Triangulation: Marx's concept of unalienated praxis is precisely the sublation of work and play. Alienated labor is failed play-as-work, not a refutation of the thesis.

### 7.2 Maieutics

**Question 3: What is the equilibrium structure of a well-designed play-as-work system?**

Elicitation: Incentive-compatibility, potential alignment, Stackelberg optimality, Shapley fairness, and skill compilation with adversarial revalidation.

**Question 4: How does the Factorio MCP ecosystem validate the thesis?**

Elicitation: factorioctl explicitly offloads low-level operations to specialized tools, following comparative advantage. This is an instance of compilation in the formal sense: repeated reasoning becomes a callable primitive.

### 7.3 Aporia

**Question 5: Is the play-as-work thesis falsifiable?**

Doubts: The thesis is falsifiable if it specifies ex ante conditions and predicts measurable outcomes. The four-arm experiment provides such outcomes. The conjunctive play condition I_i > \tau_I \wedge \alpha_i > \tau_\alpha makes "play" itself measurable.

**Question 6: Does the rise of LLM agents change the thesis?**

Doubts: If LLM agents can shape opponents toward exploitable equilibria, play for an LLM may be zero-sum exploitation. The thesis must distinguish generative play from strategic play. The four-arm experiment measures both W and NC, which separates value creation from value capture with side effects.

### 7.4 Dialectic

Synthesis: The thesis survives scrutiny but requires refinement:

1. Play-as-work is a mechanism design problem with a conjunctive play condition.
2. The trajectory from Factorio to GWAPs to gamified SE is a trajectory of increasing formalization, culminating in endogenous capability accumulation.
3. The frontier is AI-assisted mechanism design under adversarial revalidation.

Falsifiable technical formulation:

A play-as-work mechanism succeeds when voluntary participation repeatedly produces externally useful, verifiable artifacts while increasing participants' future action capabilities, without requiring intrinsic motivation to be replaced by external compulsion, and without incurring negative compilation on out-of-distribution tasks.

---

## 8. Conclusion: The MAG Thesis

This brief has moved from description to formalization. The original research programme — cataloging Factorio tools, GWAP examples, and gamified SE platforms — was necessary but insufficient. By separating X_t, K_t, R_t, E_t, by defining compilation as a verified transition, by operationalizing CG, CE, AR, and NC, and by proposing the four-arm experiment whose crucial comparison is C vs. D, we have transformed a descriptive survey into a mechanism design research programme with falsifiable predictions.

Factorio is demoted from centerpiece to canonical motivating example. The actual subject is endogenous capability accumulation in computational games: the design of systems in which successful play modifies the future action space, in which verification prevents successful play from becoming permanent authority, and in which adversarial revalidation prevents compiled capability from becoming compiled liability.

The play-as-work loop is:

\boxed{
\text{Explore}
\rightarrow \text{Act}
\rightarrow \text{Observe}
\rightarrow \text{Verify}
\rightarrow \text{Compile}
\rightarrow \text{Reuse}
\rightarrow \text{Challenge}
\rightarrow \text{Retain/Revise/Forget}
}

Factorio stops at Reuse. MAG continues to Challenge. That continuation is the specific contribution.

The Grey Swan Arena — with its control over payoff matrices, hidden information, skill acquisition, agent populations, counterfactual runs, provenance, and deterministic replay — is the appropriate experimental substrate for testing this. It provides the instrumentation required to find out whether endogenous capability accumulation is true rather than merely beautiful.

---

## 9. References

1. Jain, S., & Parkes, D. C. (2013). A Game-Theoretic Analysis of the ESP Game. ACM Transactions on Economics and Computation, 1(1), 3:1–3:35.
2. Kang, X., Yu, G., Wang, J., Guo, W., Domeniconi, C., & Zhang, J. (2023). Incentive-Boosted Federated Crowdsourcing. AAAI, 37(5), 6021–6029.
3. Hazzan, O., & Dubinsky, Y. (2005). Social Perspective of Software Development Methods: The Case of the Prisoner Dilemma and Extreme Programming. XP 2005, LNCS 3556, 74–81.
4. Rass, S., & Pinzger, M. (2023). Incentive-Based Software Security: Fair Micro-Payments for Writing Secure Code. GameSec 2023.
5. Naserameri, M. (2026). TrustChain-Review: A Risk-Adaptive Blockchain and Game-Theoretic Framework for Trustworthy AI-Assisted Code Review. arXiv:2607.27310.
6. Chapman, A. C., Micillo, R. A., Kota, R., & Jennings, N. R. (2009). Decentralised Dynamic Task Allocation: A Practical Game-Theoretic Approach. AAMAS 2009.
7. Monderer, D., & Shapley, L. S. (1996). Potential Games. Games and Economic Behavior, 14(1), 124–143.
8. Garcia Segura, M. E., Hailes, S., & Musolesi, M. (2026). Opponent Shaping in LLM Agents. ICLR 2026.
9. Hennes, D., Li, Z., Schultz, J., & Lanctot, M. (2026). Code-Space Response Oracles: Generating Interpretable Multi-Agent Policies with Large Language Models. AAMAS 2026.
10. Li, H., Li, D., & Deng, X. (2026). Discovering Expert-Level Nash Equilibrium Algorithms with Large Language Models. Nature Communications.
11. Hinman, L. M. (1978). Marx's Theory of Play, Leisure and Unalienated Praxis. Philosophy and Social Criticism, 5(2), 192–228.
12. Marx, K. (1986). Economic and Philosophic Manuscripts of 1844. Progress Publishers.
13. MarkMcCaskey. (2026). factorioctl: CLI to control Factorio + tools for Claude code to play Factorio. GitHub.
