# DUEL2_train_05_r2 (anthropic/claude-sonnet-5.5, turn 1, channel: content)

# Falsification predicates for COMMON_LANGUAGE_SPEC v1

<citation_convention>
The evidence block carries no line numbers, so every file:line is UNVERIFIED. Each citation below is a section name plus the quoted bytes, which do resolve.

All thresholds (N, rates, windows) are mine. The document names no numbers for these claims, so each threshold is itself a proposal.
</citation_convention>

## 1. Claims and predicates

### C1. "Three syscalls carry the traffic"

<quote>Section ECONOMICS: "three ops carry the traffic; the rest of the brochure was workflow engines larping as primitives." Section ISA: "Everything else composes from these or was never a primitive." Heading: "identical for 1.7B and 200B".</quote>

**P1a - Exclusivity**
- Instrument: the dispatcher log at the model-facing boundary. Model self-report does not count.
- Moment: a 7-day window with at least 10,000 model-originated calls.
- Context: the production fleet, with model credentials only.
- Query: group calls by op name and by outcome.
- PASS: every call is in {store.read, intent.append, rib.exec}, and every attempt at commit, rib.compile,
