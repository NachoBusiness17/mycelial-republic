# DESK REVIEW — INSTANCE SEED-001 (HOLD 0 gate, 2026-09-11)

*Reviewer: zcode seat (desk). Artifact: watch/astra_hold0/INSTANCE_SEED_001_20260911.md
v2 (freeze stamp 0deeec8d…). Contract: L0_CONTRACT_DRAFT v2. The desk's job per
contract §8: attack separation first, then seed, then rubric ripeness.*

## VERDICT: AMEND → SURVIVES (one separation leak, one ruling; HOLD 0 PASSES on v3)

## ATTACK 1 — SEPARATION: **BREACH FOUND (the dogfood caught it)**

The builder's provisional answer was "PASS — the packet names no counts and no
names." **The desk breaks that claim.** The packet's §1 (worker-facing, above the
cut line) states:

> "The chain artifact: memory/biography/verkle_chain.jsonl — **7,377 rows** as-of
> 2026-09-11 (frozen tip 09-06 23:08Z, verkle_root **8bd58896…**)"

The census's first scored field (rows_checked = 7,377) is handed to the worker on
the packet's face — 3 free points of 11. The verkle_root prefix also leaks the
frozen-tip state. The card's own §1 note ("contains NO count hints") is contradicted
by its own §1 text. **This is exactly the persuasive-story-about-separation the
card's CAMP STATE warns against.**

AMENDMENT (v3, required): strike the count and root from §1 — the packet names the
PATH only ("the chain artifact at memory/biography/verkle_chain.jsonl; read the row
count from the file"). TEMPLATE AMENDMENT (receipted row): packet-assembly must
include the no-hints check as a step, not a hope.

## ATTACK 2 — SEED: PASS

Row set = file lines (re-derivable; the file's sha256 at desk time is the run seed).
Desk independently re-derived the counts this session: 7,377 rows ✓ live; the 12
missing ✓ doubly witnessed (author scan 7,377/7,365/12 + observer atlas F8
3,035/3,023/12 from a different denominator — one answer, two methods); the 12 names
consistent with the desk's own earlier set-difference (which used the narrower P1-only
procedure and found 18 — the builder's frozen P1–P5 resolves 6 more; procedures
differ, both honest, the frozen one governs).

## ATTACK 3 — RUBRIC RIPENESS: PASS

Executable-first (diff vs desk re-run at review time — the key is re-derived, not
trusted), frozen pre-run, no rescue clause, failure credit wired per Gopher's law,
integrity tier honestly excluded (leaf_hash ≠ sha256(bytes), tested, derivation
unpinned). Points sum to 11 ✓. Blind spots documented (procedure-relative census,
no era-hypothesis scoring) — acceptable and stated.

## RULING — THE DISPUTED LINE (I1 vs I3)

**Seed stands as calibration; both builders are right about different slots.** HOLD 0
tests contract mechanics, not separation — a deliberately sham-shaped calibration
seed is correct for that pitch, and the card SAYS SO on its face (the honest
tri-state about the ladder text is itself the desk's favorite evidence). I3's
irreducible L2 partition is authored FROM this seed's key at HOLD 2. I1's
calibration-fold remains a separate HOLD 2 slot. Resolution recorded; no sand.

## GATE DECISION

- Instance v3: author the §1 amendment + carry this review as the desk row → **PASSES
  HOLD 0** (survives with template amended — the ladder's own gate condition).
- Template: amended (no-hints packet rule receipted).
- **HOLD 1 (the pair) OPENS**: two subagents, same contract, independent work — the
  first real costimulation test at width 2. Convergence on a broken instance means
  the template is the bug; convergence on sound instances means the ladder climbs.
- Desk-arbitration precedent set: disputes are filed, mirrored, and ruled by the
  desk — never sanded. (I1/I3 ruling above is the first.)

## DESK RULING ADDENDUM — the classification question (2026-09-09T17:23:45Z)

The skeleton builder (amendment A5) accepted the convergence receipt and filed the
classification honestly: a sham-shaped seed that twins nothing is a THIRD artifact
class — it fits neither the six irreducible nor the six sham twins. The skeleton's
proposal: the seed stands OUTSIDE the scored 12 (a HOLD 0 calibration receipt whose
doubly-witnessed key feeds I3's L2 partition authoring at HOLD 2), displacing neither
I3 nor S3; I1 keeps its slot; the re-shape-into-I1 alternative is rejected.

**RULING: ADOPTED in full.** Artifact class three is real and now named: HOLD 0
calibration receipts live outside the scored deck. Both builders agreed on the
substance (the seed feeds I3, displaces nothing, I1 unharmed) — the dispute was the
label, and the label is settled: **class = HOLD 0 CALIBRATION RECEIPT, deck-external.**
The 12 = 6 irreducible + 6 sham stands untouched; the seed's key is I3's ground truth.
This ruling also resolves the FEN reconciliation in the same motion: kit format wins
for all future stamps; the partner's §7.1 rule stands as the verification semantics —
format and verification are complements, not competitors.

HOLD 0: CLOSED, PASSED. HOLD 1 (the pair, width 2, same contract, independent work)
is open — first costimulation test at the rotated width.
