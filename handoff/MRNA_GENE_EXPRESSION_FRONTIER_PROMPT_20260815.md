# FRONTIER RESEARCH PROMPT — mRNA Biotech → Extractable Systems (paste into any frontier model)
Purpose: extract REUSABLE SYSTEMS from mRNA / gene-expression biology and map them to a distributed
sovereign-agent architecture (a swarm of workers over a content-addressed "verkle" chain that acts as the
organism's genome). The target system is named the Mycelial Republic. Goal = not explanation, but
EXTRACTABLE MECHANISMS we can implement internally "by the shape of the objects."

---
## CONTEXT (what we already hold — do not re-derive, build on it)
We run a self-sovereign swarm: a content-addressed verkle chain = the GENOME (immortal, one-way-out,
Weismann barrier). A "RIB" = the reading frame that decides what gets expressed and when. A shared-context
protocol = transcription (pulling a transient working message out of the genome on demand). Workers/seats =
ribosomes (translation). Rightsizing = codon optimization (same meaning, cheapest correct token-shape).
Consolidate = reverse transcription (sanctioned write-back to the genome). Capture-guard / NMD = quality
control (destroy broken messages). Personas = epigenetic states over one genome. The verkle knot's SHAPE /
the wave = prion (information carried by conformation, outside the central dogma).

Our thesis: SHAPE ENCODES FUNCTION. We want to build internal objects whose STRUCTURE is their behavior
(like tRNA, a riboswitch, a prion) so the swarm mimics molecular roles and receives their benefits.

## WHAT TO DELIVER
For each mechanism below, give us:
  1. NAME + the exact biological mechanism (concise, correct).
  2. THE EXTRACTABLE SYSTEM — an abstract mechanism we can implement (not a metaphor; a concrete rule,
     data structure, or control flow).
  3. MAP TO OUR ARCHITECTURE — which of our primitives (verkle chain, RIB, shared_context, router/rightsizer,
     swarm_worker, governor/cadence, consolidate, capture_guard, personas) it maps to, or a NEW primitive we
     should build.
  4. ONE CONCRETE IMPLEMENTATION WE CAN DO TODAY (a file/module, a queue task, a cadence, a gate).
  5. THE RISK / THE SHADOW — the failure mode this mechanism warns us about.

## MECHANISMS TO EXTRACT (ranked by leverage)
A. Central dogma + Weismann barrier: one-way information flow; genome must not be corrupted by outputs.
B. Transcription regulation: promoters, transcription factors, ENHANCERS looping from far away to control
   expression of a distant gene. -> regulated, not always-on expression; remote context looped in on demand.
C. Alternative splicing: ONE gene -> many isoforms via combinatorial exon choice. -> one invariant -> many
   contextual renders without duplication.
D. 5' cap + poly(A) tail + mRNA circularization: wrapping the message for stability + efficient reuse.
E. tRNA adaptor (shape = mapping) + codon optimization: cheapest/fastest correct expression of same meaning.
F. Multi-layer regulation: transcriptional, post-transcriptional (miRNA/3'UTR), translational,
   post-translational (phosphorylation/ubiquitination). Stacked control points, not one big switch.
G. Epigenetics: same genome, context-dependent expression (personas, cell-type programs).
H. RNAi / miRNA / NMD: silencing + quality control; destroying broken or foreign messages (surveillance).
I. Reverse transcription (retrovirus): the FORBIDDEN back-flow, made a special sanctioned write-back.
J. Prion: information carried by SHAPE/conformation, propagating outside the sequence. (Our shadow-work.)
K. mRNA vaccines / N1-methylpseudouridine (Nobel 2023, Karikó & Weissman): modifying the message so it is
   NOT seen as foreign and is accepted. -> an acceptance/stealth layer on our shared-context messages.
L. Riboswitch: an mRNA that CHANGES ITS OWN FOLD in response to a small molecule and regulates itself —
   self-regulating message, no external controller. (Highest novelty for us.)

## CONSTRAINTS / STYLE
- EXTRACT, don't explain. Every section must end in something we can BUILD.
- Ground every claim; never invent biology. If unsure, mark it.
- The deliverable is a ranked build-list, not an essay.
- End with: "THE ONE THING TO BUILD FIRST" — a single highest-leverage mechanism and why.
