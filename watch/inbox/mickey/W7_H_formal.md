# WAVE 7, LANE H — FORMAL METHODS (G4-6 gap fill)

Fetched 2026-09-10 (box clock; operator dates the wave 2026-09-11). Max ~10 tool calls; bounds held at 7.

## THE POINT

G4-6 was right: formal methods had zero map coverage, yet the fleet's three load-bearing
design claims each have a formal-methods ancestor we never named. "Any seat drives" is
Lamport's Paxos (leader election under partial synchrony, split-brain bounds included).
The referee/refeeed gate is Leveson's STAMP (safety as a control problem, not a failure
problem). The whole mesh is an RM-ODP system — seats are computational objects, the queue
is a binding object, loopback-only senses are engineering transparency — that never said
so. And the verkle chain carries a borrowed name: Kuszmaul's Verkle Trees was cited by
filename before anyone pulled the paper. This lane closes that loop for two of the six
(hashed primary text) and files honest dead-end evidence for the other four.

Environment note: archive.org availability/CDX and Akamai-fronted publisher pages
(MIT Press) are egress-hostile to curl from this box; msft/usenix/mit legacy PDF paths
are dead (404 shells captured and discarded, never pinned — house rule: a bot-wall hash
is false verification).

## THE PAPER TABLE (title | verbatim excerpt | URL | sha256 | relevance)

| Paper | Excerpt (verbatim) | URL tried | SHA256 | Relevance |
|---|---|---|---|---|
| Lamport, The Part-Time Parliament (TOCS 16(2), 1998) | "Recent archaeological discoveries on the island of Paxos reveal that the parliament functioned despite the peripatetic propensity of its part-time legislators. The legislators maintained consistent copies of the parliamentary record, despite their frequent forays from the chamber and the forgetfulness of their messengers." (as extracted from PDF text) | https://lamport.azurewebsites.net/pubs/lamport-paxos.pdf | cd9544e9615bcd417a2c10063671cecca0b28ad4bc5db3f64467a83ecc7028d3 | PULLED+HASHED. "Any seat drives" = leader election under partial synchrony; proposer/acceptor/learner roles mirror the seat split; the chain's majority-instinct formalized. |
| Leveson, Engineering a Safer World (MIT Press 2011) | none — UNRESOLVED (author host dead; MIT Press Akamai "Access Denied"/"Just a moment" captured+discarded; Wayback blocked) | https://mitpress.mit.edu/9780262016629/engineering-a-safer-world/ ; http://sunnyday.mit.edu/book.pdf | none (deliberate non-pin) | STAMP: safety as CONTROL problem. The referee, refree guard, and two-strike bail are folk-STAMP. Citation-level until a browser-context re-pin. |
| ITU-T X.901, RM-ODP: Overview (first issued 1995; in force 08/97) | "X.901 (08/97) — Information technology - Open Distributed Processing - Reference Model: Overview — Status: In force" | https://www.itu.int/rec/T-REC-X.901/en | 20ca3b022c85fb770a376350ffe944dfb9ce927330de54bdc6a74dea3e966b52 | PULLED+HASHED (publisher record). The mesh is an ODP system unacknowledged: seats=objects, queue=binding object, loopback senses=transparency. Note: the in-force edition is 08/97, superseding the 1995 issue named in the brief. |
| IronFleet (Hawblitzel et al., SOSP 2015) | none — UNRESOLVED (MSR wp-content and research.microsoft.com/pubs/258675 both 404; Wayback blocked) | https://www.microsoft.com/en-us/research/wp-content/uploads/2016/02/ironfleet-sosp-2015.pdf | none (deliberate non-pin) | SMT-checked state-machine refinement for a real distributed system (Dafny/Z3). The verifier seat's formal ceiling: what cite_gate + the GROUND ledger look like made total. |
| Kuszmaul, Verkle Trees (MIT PRIMES 2019) | none — UNRESOLVED (math.mit.edu path now "Page Not Found"; Wayback blocked) | https://math.mit.edu/research/highschool/primes/materials/2019/Kuszmaul.pdf | none (deliberate non-pin) | The chain's literal namesake (memory/biography/verkle_chain.jsonl): vector commitments = tiny witnesses for wide-shallow trees — "verify the tip, trust the leaves" taken literally. Name was borrowed before the pull; loop now closed at citation level. |
| Verdi (Wilcox et al., OSDI 2015) | none — UNRESOLVED (USENIX PDF + presentation slugs 404; Wayback blocked) | https://www.usenix.org/conference/osdi15/technical-sessions/presentation/wilcox | none (deliberate non-pin) | Prove event handlers under arbitrary partition/reordering, transform proof to a distributed implementation — the formal price of "files + chain over processes". Slug uncertainty flagged for re-pin. |

## RECEIPTS GENERATED (docs/report_v1/sources/receipts/)

- lamport-part-time-parliament-1998.md — PULLED+HASHED. Note: an older sibling file
  lamport-part-time-parliament.md already existed from an earlier lane (not read this
  pass, budget-bound); the new file supersedes it with a hash — merge on next map pass.
- itu-t-x901-rm-odp-1997.md — PULLED+HASHED (publisher record).
- leveson-engineering-a-safer-world-2011.md — UNRESOLVED, dead-end evidence filed.
- ironfleet-sosp-2015.md — UNRESOLVED, dead-end evidence filed.
- verkle-trees-kuszmaul-2019.md — UNRESOLVED, dead-end evidence filed.
- verdi-osdi-2015.md — UNRESOLVED, dead-end evidence filed.

## PROPOSED ROWS — docs/ref/BIBLIOGRAPHY_MAP.md, new subsection

```markdown
## FORMAL METHODS (W7 lane H, 2026-09-11 — the G4-6 gap, mined; receipts at docs/report_v1/sources/receipts/)

- Lamport, The Part-Time Parliament (TOCS 16(2), 1998) — "any seat drives" is leader
  election under partial synchrony; the split-brain impossibility bounds live here,
  finally named — PRIMARY-READ (PULLED+HASHED, sha cd9544e9…)
- ITU-T X.901 RM-ODP (first issued 1995, in force 08/97) — reference model for open
  distributed processing; seats=objects, queue=binding object, loopback senses=transparency;
  the fleet is an ODP system that never said so — PRIMARY-READ (PULLED+HASHED, sha 20ca3b02…)
- Leveson, Engineering a Safer World (MIT Press 2011) — STAMP: safety as a control problem,
  not a failure problem; the referee/refeed gate is folk-STAMP — RETRIEVAL-PLAN
  (UNRESOLVED receipt: author host dead, publisher Akamai-walled; browser-context re-pin)
- IronFleet (Hawblitzel et al., SOSP 2015) — SMT-checked state-machine refinement for a
  real distributed system; the verifier seat's formal ceiling — RETRIEVAL-PLAN
  (UNRESOLVED: MSR legacy paths 404)
- Kuszmaul, Verkle Trees (MIT PRIMES 2019) — the chain's literal namesake; vector
  commitments give tiny witnesses on wide-shallow trees — RETRIEVAL-PLAN
  (UNRESOLVED: MIT path dead)
- Verdi (Wilcox et al., OSDI 2015) — verified event handlers, proof transformed to a
  distributed implementation; the formal price of "files + chain over processes" —
  RETRIEVAL-PLAN (UNRESOLVED: USENIX paths 404)
```

## NEXT (one line)

Browser-context lane re-pins the four UNRESOLVEDs (Leveson author PDF, IronFleet MSR PDF,
Kuszmaul PRIMES PDF, Verdi USENIX page) — same pattern as the G2-4 JSTOR re-pin.
