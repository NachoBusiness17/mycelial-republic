# AGENT MEMORY COUNTER-LAW (DRAFT) 2026-09-25

**Row:** google-week. **Status:** draft for operator adoption. This file does not enact anything; adoption is an operator-gated decision.

## The law, one line

**Agent memory never leaves the box unless the user holds the keys.**

Memory is what the agent is: session handoffs, bonds, the corpus of what it learned about its operator and its work. If a copy of that lives on someone else's server under someone else's rules, then the estate's privacy is a promise, not a property. The counter-law makes it a property: the only durable copy sits on this machine, encrypted under keys the operator (and nobody else) controls.

## The receipt that triggered it (Google week)

Drop: Google DeepMind, "Advancing Private AI Compute with secure, server-side memory," deepmind.google/blog/advancing-private-ai-compute-with-secure-server-side-memory, published September 23, 2026 (fetched this session). Google announced persistent agent memory stored server-side: per-user encrypted databases inside "hardware-enforced secure enclaves," where "the cryptographic keys required to unlock it are held exclusively on your personal devices," the data is "inaccessible to anyone else, even Google," and devices verify a "tamper-proof public record of our server software" before sending anything.

Read that carefully, because it is the industry conceding our thesis. The most powerful AI company on earth had to promise: keys live on your devices, not ours. Google's answer keeps the memory in their vault and asks you to trust the vault, verified by their published records and an independent audit. Our counter-law goes one step further and costs nothing: the vault is the box. Their design is the concession; our design is the consequence.

## What the courts teach (estate case law)

- **Ajemian v. Yahoo!, Inc., 478 Mass. 169 (Oct. 16, 2017)** (full opinion read this session from masscases.com/cases/sjc/478/478mass169.html). John Ajemian died intestate, "left no instructions regarding treatment of the account," and his siblings, as personal representatives, demanded his Yahoo mail. Yahoo refused; the Massachusetts SJC held Yahoo could produce the contents: "the SCA does not stand in the way of Yahoo doing so," because the personal representatives' consent is lawful consent under 18 U.S.C. 2702(b)(3). Eleven years of litigation bought the estate the provider's plaintext. The lesson is not anti-estate: families should be able to reach a loved one's papers. The lesson is about location: everything the provider holds in readable form is one probate order (or subpoena, or breach) away. What the provider never held, no court order to the provider can reach.
- **In re Ellsworth (Oakland County Probate Court, Michigan, 2005).** A probate judge ordered Yahoo to give the family of Marine Justin Ellsworth, killed in Iraq in 2004, the contents of his email. Honest source note: this case is unreported; the description here is consistent across multiple public accounts found this session, but no primary page was fetchable, so treat it as commonly reported rather than primary-verified.
- **RUFADAA.** Per Ajemian note 25 (in the opinion above), the Revised Uniform Fiduciary Access to Digital Assets Act is enacted by a majority of states. Its default: if the user leaves no instructions, the provider's terms of service and court process decide what an estate gets. Default means: whatever you did not direct, the ToS wrote.
- **The provider-held-key receipt (UK, 2025).** In January 2025 the UK Home Office issued a secret "technical capability notice" under the Investigatory Powers Act 2016 demanding Apple give access to end-to-end encrypted iCloud data; Apple withdrew Advanced Data Protection for UK users on February 21, 2025 rather than comply (order and Apple's legal appeal documented in a post fetched this session: mjtsai.com/blog/2025/02/07/uk-orders-apple-to-break-icloud-advanced-data-protection/, Feb 7, 2025, updated April 2025; withdrawal date per contemporaneous coverage). When keys sit with the provider, governments do not ask the user; they order the provider. That is the whole argument in one news cycle.

Chain of custody, stated plainly: provider-held memory = one court order away from leaving. User-held keys = the order comes back empty, and the estate inherits ciphertext plus, if the operator planned, the keys.

## What this law means on this box (all on disk today)

- Durable agent memory lives locally: `memory/` and `memories/` (including `memories/session/next-window-handoff.md`), and `memory/OPSEC_BOUNDARY.md:20` already declares `memory/` state and secrets private, never public.
- The tiers law already forbids the worst of it: T0 (secrets) and T1 (operator private) "may leave machine? No"; T1 runs on local models only; T0 never enters a prompt body (`../mycelial-republic/docs/CONSTITUTION.md:92-99`).
- Key custody outlives the operator: the estate's dead-hand switch is armed (armed 2026-09-24), 30-day silence trigger, 2-of-3 custodian co-sign, heir key holders with a 48-hour veto (`configs/succession_contract.yaml:20,30-35`). Honest caveat from that same file, line 33: the custodian keys on disk are ceremony keys; live firing requires each custodian to escrow their own key. That escrow is an operator-gated decision and remains open.
- What this draft adds is the missing sentence tying those together: no memory file, backup, or durable corpus leaves this machine unless it is encrypted under a key the operator holds, and no third party is ever given the plaintext or the power to read it.

## Honest limit and falsifier

Not audited yet: which exact bytes ride in each outbound model call (per-window context packs are built from local state; the tier rules above are the current guard). Pre-registered falsifier, two prongs. One: build an egress check that scans outbound model-call payloads for lines originating in memory-class files; the law is violated the first time T1-class memory text travels to a remote provider unencrypted. Two: any receipt quoted above that is found misquoted or misdated voids the receipt chain and the draft gets refiled corrected. Until prong one runs and passes, this is a draft, not a fact.

## Filed

- This file is the landing for the google-week counter-law row. No promotion claimed; intake only.
