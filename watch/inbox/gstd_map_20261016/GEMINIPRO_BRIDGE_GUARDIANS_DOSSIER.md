# BRIDGE GUARDIANS DESIGN DOSSIER - Gemini Pro lane burn (2026-10-16)

Classification: RECEIPT (intel; SENSING-GRADE - draft for the gstd-bridge PR,
needs contract-eyes + spot-verification before anything ships)
Producer: zcode-seat-20261016
Lane: Gemini web, nachobusinesscorp@gmail.com (Pro, Gemini 4, Flash-Lite +
canvas artifact), driven end-to-end by the seat browser in the same
conversation as the bridge survey (context carried). Second burn on the Pro
lane; the free lane failed this ask twice (empty reasoning, then 429s).

Provenance: verbatim from the rendered canvas, captured 2026-10-16T23:24Z,
4,704 chars. The conversation ("October 2026 Bridge Security Survey") is
saved in the account history.

---

BRIDGE GUARDIANS DESIGN DOSSIER

(1) RED VERDICT RESTATED: 2026 EXPLOITS VS. DEFEATED GUARDS

| Exploit / Near-Miss (2026) | Root-Cause Class | The Guard Defeated |
|---|---|---|
| Liquid Network ($320M) | Range-proof verification caching bug | Strict cryptographic invariant verification guards |
| Kelp DAO / LayerZero ($292M) | RPC infrastructure compromise + 1-of-1 DVN | Multi-quorum M-of-N decentralized verifiers |
| Drift Protocol ($285M) | Administrative credential social engineering | Multi-sig and timelocked administrative boundaries |
| Syscoin Bridge ($10M) | SPV proof-validation parsing errors | Robust input parsing and formal verification guards |
| Hyperbridge ($2.5M) | Forged cross-chain messaging vulnerabilities | Cryptographic message source authentication guards |

(2) THE GUARDIAN SET

Our current architecture relies on a dangerous sole guardian model where the
owner supplies its own replay keys. To achieve robust security, we abandon
this single point of failure in favor of modular verification using LayerZero
Decentralized Verifier Networks (DVNs) or Hyperlane Interchain Security
Modules (ISMs).

M-of-N Configuration: We will enforce a 3-of-5 threshold model where no
single entity can authorize a cross-chain transfer.

Independent Verifiers for TON Jetton: The verification set will comprise
trusted institutional node operators, decentralized validator collectives,
and zero-knowledge light client proof verifiers.

Leaked Key Impact Analysis: If a single key is compromised, the attacker
cannot mint unbacked tokens or drain funds because 3 valid signatures are
strictly required. However, a single leaked key can fail liveness or attempt
spam attacks, which are mitigated by rate-limiting windows.

(3) THE REWRITE BAR

The current codebase contains SwapIn functions that are unimplemented yet
consume guards, inviting replay-map denial of service vulnerabilities.
SwapIn-class functions may only exist in production if they meet four strict
criteria:

- Fully Implemented: All logic paths must be complete, tested, and audited.
- Least-Privilege Access: Functions must not be tied to owner-controlled
  root keys.
- Replay-Guarded: Nonces and message hashes must be immutably stored to
  prevent duplicate execution.
- Timelocked: High-impact state changes must incorporate a mandatory delay
  window.

(4) LIQUIDITY DECOUPLING

To isolate our jetton bridge from messaging failures or verification set
compromises, we decouple message validation from raw liquidity pools:

- Rate-Limiting Windows: Maximum outflow caps per rolling block window will
  throttle sudden drain attempts.
- Burn-Invariant Circuit Breakers: Automated monitors will halt the bridge
  if inbound tokens do not match historical burn proofs on the source chain.

(5) DEPLOYMENT SEQUENCE

Before the first real bridge message traverses the network, the following
components must ship in exact order:

1. Audit-verified multi-quorum verification module (DVN or ISM
   configuration).
2. Rate-limiting and invariant circuit-breaker contracts.
3. Complete implementation and removal of stubbed, guard-consuming SwapIn
   code.
4. Testnet dry runs with simulated validator node offline failures.

(6) FALSIFIERS

The following observations will prove our guardian set and verification
design insufficient:

- SPECULATIVE: If two or more independent DVN operators share identical
  cloud infrastructure hosting providers, correlated outages may drop active
  quorum below safety thresholds.
- If a valid cross-chain transfer is rejected or delayed beyond the
  circuit-breaker window due to consensus staleness among verifiers.
- If gas price volatility on TON causes verifier nodes to miss signing
  windows simultaneously.

---

## Seat notes (grading)

The correlated-infrastructure falsifier (two DVNs on one cloud provider) is
genuinely good - it survived the SPECULATIVE discipline and is the kind of
row a hostile reviewer would add. The burned-invariant circuit breaker comes
straight from the survey's 90-day trend section. Spot-verify the five
exploit figures before the PR; the M-of-N 3-of-5 default is a starting
number, not a law. Add from our own side before shipping: the SwapIn
replay-map DoS mechanism detail (the dossier restates the class, our RED
verdict has the mechanism) and the TON Foundation legacy-bridge shutdown as
the timing note.
