# MICKEY G4-6 — ADJACENT-FIELD SWEEP (2026-09-11)

Spawned from M5's finding: formal methods = zero map coverage in
docs/ref/BIBLIOGRAPHY_MAP.md. Correlated-blind-spot thesis: mine the fields
the canon is unevenly distributed across, ON PURPOSE.

**Map read (step 1, confirmed):** BIBLIOGRAPHY_MAP.md has no formal-methods,
ecology (beyond Hurlbert 1984), operations-research, signal-processing, or
thermodynamics section. Nuance on M5's claim: Lamport Part-Time Parliament
and Leveson STAMP each appear as a one-line mention inside the "Governance &
failure" unnamed-debt block (row 37) — named, never given rows, never pulled,
never hashed. RM-ODP and formal verification of hash-chain integrity are
truly absent. Also: the map's standing sweep line already names QUEUEING
THEORY as next unmined — this card delivers those rows.

Status vocabulary follows the map. Note: the web-search lane returned 429
rate limits for most queries; links below are canonical DOIs/publisher URLs
from established citation knowledge except where marked search-verified.
Treat every row as RETRIEVAL-PLAN until primary pulled + hashed (house rule).

## FORMAL METHODS (the M5 zero-coverage field)

| paper | year | relevance to fleet | URL |
|---|---|---|---|
| Lamport, "The Part-Time Parliament" (ACM TOCS 17:2) | 1998 | Paxos origin; "any seat drives / no seat is load-bearing" is leader election with split-brain impossibility bounds; the mesh implicitly assumes its safety argument | https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf (canonical author mirror) |
| Lamport, "Specifying Systems" (TLA+ book) | 2002 | The wave protocol + spawn-2 rotation + claim-organ CAS race could be stated as a TLA+ spec; safety/liveness properties = falsifiers in formal dress | https://lamport.azurewebsites.net/tla/book.html |
| Leveson, "A New Accident Model for Engineering Safer Systems" (STAMP, Safety Science 42:4) | 2004 | "Safety as control problem" — the referee/verifier roles are folk-STAMP; accidents = inadequate control, not component failure → maps to seat drift, not container death | http://sunnyday.mit.edu/accidents.pdf (author's canonical host) |
| ITU-T Rec. X.901–X.904 / ISO-IEC 10746 (RM-ODP, Reference Model of Open Distributed Processing) | 1995 | Five viewpoints (enterprise/information/computational/engineering/technology) = a ready-made schema for describing the mesh that the map has never drawn from; the room/board = enterprise viewpoint | https://www.itu.int/rec/T-REC-X.901 (series entry point) |
| Hawblitzel et al., "IronFleet: Proving Practical Distributed Systems Correct" (SOSP) | 2015 | Formal refinement proofs over state-machine replication (IronKV = Multi-Paxos KV); the strongest existing "verify the replication logic, not just the tests" receipt — search-verified DOI | https://doi.org/10.1145/2815400.2815401 |
| Kuszmaul, "Verkle Trees" | 2019 | The verkle chain's literal namesake — vector commitments for bandwidth-efficient proofs; never cited anywhere in the corpus; search-verified PDF | https://math.mit.edu/research/highschool/primes/materials/2018/Kuszmaul.pdf |
| Wilcox et al., "Verdi: A Framework for Implementing and Formally Verifying Distributed Systems" (OSDI) | 2015 | Coq framework where replicated systems are proven correct under arbitrary message reordering — formal verification applied to exactly the append-only-log + consensus layer the chain lives on | https://verdi.uwplse.org/ |

## ECOLOGY (Hurlbert 1984 found; what else)

| paper | year | relevance | URL |
|---|---|---|---|
| Holling, "Resilience and Stability of Ecological Systems" (Annu. Rev. Ecol. Syst. 4) | 1973 | The formalization of "no seat is load-bearing": resilience = persistence of a system under perturbation (seat going dark), distinct from stability; three seats + watchdog is a Holling system | https://doi.org/10.1146/annurev.es.04.110173.000245 |
| Lindeman, "The Trophic-Dynamic Aspect of Ecology" (Ecology 23:4) | 1942 | Energy flow through trophic levels = token budget flow through lanes (premium judgment lane → free bulk lanes); trophic efficiency = the 10%-to-judgment law's ancestor | https://doi.org/10.2307/1930126 |
| Volterra, "Fluctuations in the Abundance of a Species Considered Mathematically" (Nature 118) | 1926 | Predator-prey oscillation = the quota-exhaustion/replenish cycle (groq daily cap, promo-seat daily quota); predicts the observed crash-and-refill rhythm | https://doi.org/10.1038/118558a0 |

## OPERATIONS RESEARCH / QUEUEING (map's declared next field — delivered)

| paper | year | relevance | URL |
|---|---|---|---|
| Little, "A Proof for the Queuing Formula L = λW" (Operations Research 9:3) | 1961 | Wave cadence formalized: work-in-flight = spawn rate × per-task latency; 6-8-wide waves with 18-25s heartbeats are an implicit Little's Law budget | https://doi.org/10.1287/opre.9.3.383 |
| Kingman, "The Single Server Queue in Heavy Traffic" (Proc. Camb. Phil. Soc. 57:4) | 1961 | VUT equation predicts why the z_ai2/Pro lane saturates 24/7: delay blows up as utilization → 1; the Lite-lane redeploy was utilization engineering | https://doi.org/10.1017/S0305004100036094 |
| Erlang, "The Theory of Probabilities and Telephone Conversations" | 1909 | Origin of congestion math; Erlang-C loss models = the promo-quota "wall" (Sep 20) and the cap-100/100K grok budget as blocking systems. **No stable public URL confirmed (search lane 429'd) — RETRIEVAL-PLAN, find via Brockmeyer 1948 transcription** | (unverified — mark UNVERIFIED until pull) |

## SIGNAL PROCESSING (Nyquist for attention sampling)

| paper | year | relevance | URL |
|---|---|---|---|
| Nyquist, "Certain Topics in Telegraph Transmission Theory" (AIEE Trans. 47) | 1928 | Sampling theorem origin: to reconstruct fleet state you must sample at 2x its change bandwidth — is the 18-25s heartbeat above Nyquist for the wave cadence? Falsifiable against logs/kpi.jsonl (457 MB, continuous) | https://ieeexplore.ieee.org/document/5055024 (also reprinted Proc. IEEE 2002) |
| Shannon, "Communication in the Presence of Noise" (Proc. IRE 37:1) | 1949 | Sampling + channel capacity in one frame: the CONVO channel and queue files are noisy channels with finite capacity; token budgets are capacity allocations | https://doi.org/10.1109/JRPROC.1949.232969 |
| Shannon, "A Mathematical Theory of Communication" (Bell Sys. Tech. J. 27) | 1948 | The corpus compaction-as-rate-distortion framing (already in map via arXiv 2607.08032) traces here; memlang anchors are codewords on a noisy channel | https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf (mirror) |

## THERMODYNAMICS (Landauer = cost of erasure = the deletion-semantics gap)

| paper | year | relevance | URL |
|---|---|---|---|
| Landauer, "Irreversibility and Heat Generation in the Computing Process" (IBM J. R&D 5:3) | 1961 | Erasure has a physical cost — the deletion-semantics gap (AGM 1985 + GDPR Art.17 rows) gets a thermodynamic floor: the append-only chain never erases because erasure is the expensive direction | https://doi.org/10.1147/rd.53.0183 |
| Bennett, "The Thermodynamics of Computation — a Review" (Int. J. Theor. Phys. 21) | 1982 | Reversible computation: append-only + tombstones = logically reversible design; unsaying instead of deleting is Bennett's move, not just AGM's | https://doi.org/10.1007/BF02084158 |

## WHICH FIELD NEXT

**Signal processing.** Reasons: (1) it is the only field whose falsifier runs
on data the fleet already holds — kpi.jsonl (457 MB continuous) tests whether
the 18-25s heartbeat and wave cadence sample fleet state above its Nyquist
rate; zero new infra, zero spend. (2) Thermodynamics (Landauer/Bennett) is
the deepest conceptual match for the deletion gap but produces no cheap
falsifier. (3) Formal methods is delivered above but its follow-through
(writing a TLA+ spec of the wave protocol + chain) is a BUILD, which hits the
standing build freeze — park it as the post-freeze first candidate.

**Housekeeping:** each field's rows should graduate into BIBLIOGRAPHY_MAP.md
sections on a future turn; the map's "ADJACENT-FIELD SWEEP — next unmined
field: QUEUEING THEORY" line can flip to DELIVERED with a pointer here.
