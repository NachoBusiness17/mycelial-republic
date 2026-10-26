# w4-06: The trust game of the receipt system: grounding_wave v4 vs the Dirac bank

Item: DEEP ITEM w4-06, game theory of the receipt system. Sources read in full this session:
`mag/grounding_wave.py` (975 lines), `watch/inbox/DIRAC_BANKED_INVARIANTS.jsonl` (6 rows, 3,644 B),
plus `mag/dirac_loop.py` (bank/invariant path, lines 150-289), `mag/context_pack.py:19-31`,
and the live ledger `watch/GROUNDING_WAVE.jsonl`. This document practices what it analyzes:
every empirical claim below is a receipt from a command run during this ask.

## 0. Receipts (commands run, outputs)

1. Census of the live ledger (venv python, json load of `watch/GROUNDING_WAVE.jsonl`):
   137 rows / 127 claims / 5 voids / 5 witness rows / 0 contests.
   Seats: zcode 115, unattributed (seat=None) 13, operator 5, zcode-wave-driver-v0 2,
   grounding_wave 1, zcode-desk 1. Verdicts: SUPPORTED 60, UNPROVEN 64, DISPUTED 2, None 1.
   Rows carrying `src_sha256_12` (G2 binding): **0**. Rows carrying `warrant` (G3): **0**.
   All 5 witness rows were posted by seat `operator`, all record `checks = {g1: True, g2: None, g3_exit: None}`.
2. `.venv\Scripts\python.exe -m mag.grounding_wave verify` → exit 1:
   `FAIL LINKAGE-PASS: 137 posts intact, tip=fc3c32be6f26 | truth-gate: 11 witnessed SUPPORTED, 49 legacy-unwitnessed | row 122: hashless defect contained by void; row 123: prev defect contained by void; row 129: re-anchored past voided stretch; row 130: re-anchored past voided stretch; row 131: prev defect contained by void; row 132: re-anchored past voided stretch | ADMISSION: 3 voided, 0 contested, 0 corroborated, 0 pending voids, 3 propagation-flagged | EVIDENCE-MISSING row 75:swarm_20260912/smoke_driver.js, row 76:suno/flat_beat_loop.mp3, row 86:flygomoku_20260912/hermes_mirror_summary.json`
3. Void/witness census: all 5 void rows are `seat=zcode, witness=operator` and all activity
   (5 voids + 5 witness rows, 10 rows) sits inside one 6-minute window, 2026-09-27T18:33:50Z
   to 18:39:49Z, a single batch remediation episode, not standing policing.
   Row 134 voids hash `5b456eda969d` (SUPERSEDED) and row 132 witnesses that same hash:
   the tape records the flip.
4. The v3-style `witness` field on witnessed SUPPORTED claims is free prose, census values include:
   `"operator, live session 2026-09-08, unprompted: 'I just showed you how to build yourself didn't I'"`
   and `"Astra witness #5 (codex_seat, ANSWER sha256 5b98513a34ad68b0, 0/1 false-row baseline) ..."`.
5. `mag/dirac_loop.py:185-188`: `loop_invariant` = sha256 of `"dirac_loop:" + "|".join(sorted(set(labels)))`.
   `bank()` at `mag/dirac_loop.py:231-254`: no lock, no `prev`, no admission gate, seat defaults to `"zcode"`,
   receipt stored as an unbound string. All 6 banked rows in DIRAC_BANKED_INVARIANTS.jsonl are
   `seat: zcode`, schema `dirac_loop.v1`, none carry evidence hashes; one receipt cites a real path
   (`watch/inbox/OPENCLAW_POLICY_HANDSHAKE_20260927.md`), two receipts are one-line notes
   ("offload wired, receipt watch/inbox/PACK_OFFLOAD.jsonl").
6. `mag/context_pack.py:19-31`: `_dirac_loop_count()` computes `closed` as the **raw line count**
   of DIRAC_BANKED_INVARIANTS.jsonl and ships it into the operator's daily context pack.

Not run: any post/witness/void/contest verb against the ledger (all mutations withheld; this was
read-only plus the verify audit). I did not rerun `pytest`; no test claim is made.

## 1. The two institutions

The estate runs two receipt systems with opposite designs.

**The grounding wave** (`mag/grounding_wave.py`) is a hash-chained, append-only claim ledger with
a write-time admission gate (G1, `_admit` at grounding_wave.py:403-446, running inside the append
lock at :485-498), optional evidence byte-binding (G2, `_bind_sources` :217-231 re-hashed at verify
by `_evidence_mutated` :702-722), optional executable warrants (G3, `_run_warrant` :472-482), a
status ladder RECORDED -> CORROBORATED -> CONTESTED -> VOID (:48-53), delete-as-append with
cross-signed voids that count only when the named second seat appends its witness row
(:277-292, :432-436), and a two-eyes law (a witness seat must differ from the author,
SELF_SIGNED refusal :642-646).

**The Dirac bank** (`mag/dirac_loop.py bank()`) is an append-only list with none of that: no chain,
no gate, no lock, an invariant that hashes only the sorted label set of the loop's graph path
(:185-188), and a free-text receipt. Its function is attentional: `scan()` treats banked invariants
as solved shapes and stops re-reporting them (:191-225, the 2026-09-27 comment at :195-201 states
the design point: "adding graph edges never closes loops ... only banking the holonomy does").

The empirical punchline of this item: **the demand flows to the weak instrument.** The gated ledger
has 0 corroborated rows and an unremediated verify FAIL; the ungated bank is consumed daily by the
context pack (context_pack.py:26 counts its lines as "closed" loops). The section that follows
models why this is an equilibrium, not an accident.

## 2. Players, strategies, payoffs

Players. P1 = poster seat (observed: `zcode`, 115/137 rows; plus 13 unattributed writers who
appended directly to the file, bypassing the API). P2 = witness/verifier seats (observed active
population: exactly 1, the operator). P3 = readers, the demand side (context packs, fresh seats,
the operator's attention; observed: they consume the Dirac bank and quote the admission view).

Strategies. Poster: {verified post (with G2 binding and/or warrant), plain post, false post,
self-witness, direct file append}. Witness: {check-and-witness, rubber-stamp, abstain}.
Reader: {consume, discount-by-status (read the admission view), ignore}.

Payoffs. Posting has near-zero marginal cost and a reuse benefit b (downstream seats re-derive
nothing; the docstring's own law, :530-532: "an unwitnessed post still lands (the record keeps
moving)"). G2/G3 carry engineering cost k > 0 (immutable snapshot files; a command that must
actually exit 0/1). A caught false claim is permanently visible: the tape cannot be edited, a void
names the target's hash with a reason code from the enum (`VOID_REASONS`, :130-131, including
FORGED), and `_evidence_mutated` at verify converts any post-hoc evidence edit into a standing FAIL.
Witnessing costs c_w (read the evidence, run the checks: `witness()` genuinely executes g1/g2/g3
and records results at :647-655, so a witness row is itself falsifiable by recomputation).

## 3. Equilibrium analysis

**(a) The demotion gate is collusion-proofness.** v3's teeth (:96-105, forward-applied in
`post()` :529-535) auto-demote unwitnessed SUPPORTED to UNPROVEN, and v4's G1 refuses unseeded
SUPPORTED outright (`UNSUPPORTED_UNSEEDED` :444-446, :524-526). This converts lying from a
one-player act into a two-player conspiracy: a false claim becomes SUPPORTED only if a second seat
attaches its name and its machine-run checks. The two-eyes refusal (SELF_SIGNED :642-646) closes
self-collusion under one identity. This is Tirole (1986)'s supervisor-separation move: the
information needed to certify the agent's report must come from a party who does not share the
agent's payoff. The 60/64 SUPPORTED/UNPROVEN split is exactly the predicted signature: honest
mass posting at the demoted rung, zero incentive to lie upward because the upward lie buys nothing
without a conspirator.

**(b) Corroboration is a threshold public good, and the threshold is above the observed
volunteer count.** CORROBORATED requires >= 2 witness rows by distinct seats, neither the author,
all checks passing (:325-335). With one active witness seat, the rung is structurally unreachable:
the operator's 5 witness rows can never clear `len(seats) >= 2`. Verify reports the result:
`0 corroborated`. This is a Palfrey-Rosenthal (1984) volunteering game with threshold 2 and one
volunteer: each potential second witness's marginal contribution to the public good is zero
(two are needed), so abstaining is a dominant strategy for every seat that does not alone
internalize the value of corroboration. The estate has one player who does: the operator, the
residual claimant of the whole estate (Holmström 1982's team-moral-hazard logic predicts the
residual claimant ends up doing all the monitoring). The census confirms the prediction in a
stronger form than "one volunteer": all 10 cross-signature rows sit in a single 6-minute window on
2026-09-27, a batch remediation of the row-122/123 bypass defects, after which witnessing stops.
The v4 ladder was designed for a republic of seats and is played by two; its upper rungs are empty
not from disuse but from unreachable structure.

**(c) Two-eyes here is an attention law, not a sybil law.** The seat is a plain unauthenticated
string (`"seat": str(seat).strip()` :552, default `"zcode"` :519). Nothing prevents posting as
zcode and witnessing as zcode-2. But that is the wrong threat model for this estate, and the design
comment says so: v2's goal was that "attribution is provable, forks are attributable" (:91-94),
and the v3 attack that actually happened (docstring :96-105: a fabricated SUPPORTED row passing
verify on linkage-PASS) came through the front door of reader semantics, not through identity
forgery. Inside a single trust domain, seat names are attention addresses: the two-eyes rule
guarantees a second mind actually read the claim before the label upgrades. The empirical witness
field values (receipt 4 above) show the pre-v4 version of this: testimony as quotation. v4's
upgrade from prose field to machine-checked witness rows is a coercion-proofing move: the checks
dict is generated by the code the witness ran (:647-655), so a witness cannot be retro-quoted into
a role it did not perform.

**(d) Decay is unilateral; repair is bilateral; therefore FAIL is absorbing.** Evidence decays
when files move, which needs zero actors. Repair requires a cross-signed void: the void names a
second seat at write (:432-436) and only counts once that seat's witness row lands in the chain
(:277-279). Rows 75, 76 and 86 (dead evidence: swarm_20260912/smoke_driver.js,
suno/flat_beat_loop.mp3, flygomoku_20260912/hermes_mirror_summary.json) sit in FAIL right now
(receipt 2) because discounting is cheaper than coordinating a void: a reader who quotes the
admission view loses nothing by ignoring three dead rows, so no coalition forms to bury them.
When repair cost (two coordinated actors) permanently exceeds reader discount cost (read one more
field), the tamper-evident system converges to a state of permanent, ignored FAIL, and the
ignoring is rational. Note the verify output itself is the mechanism printing its own split
verdict, `FAIL LINKAGE-PASS: 137 posts intact ... | EVIDENCE-MISSING ...`: linkage (the tape is
intact) and truth-admission (the claims live) are orthogonal instruments, and the reader law
"quote the admission view, never bare PASS" (:43-46, :824-833) is the incentive-compatibility
condition that stops any reader from collapsing the two channels, which is precisely the exploit
v3 closed.

**(e) Zero adoption of the costly signals.** 0/137 rows carry `src_sha256_12`; 0/137 carry a
warrant. All 5 witness rows exercised exactly one of three checks (g1 structural; g2=None,
g3_exit=None). So the ledger's live informativeness rests entirely on G1, which the machine
computes and which therefore attests well-forming, not truth. G3, the only check that tests the
world rather than the tape (run the warrant, record the exit code, :29-33), is also the only one
with engineering cost k, and it is the one nobody buys. In signaling terms the ledger currently
separates only "cleanly formed" from "not": a cheap-talk regime below G2. The 60 SUPPORTED rows
are supported in exactly the weak sense the v3 author warned about (:30-33, "a Claim whose Check
is 'the author agrees' is a notary, not knowledge").

**(f) The Dirac bank is a different game: self-command across seat-instances.** There is no
principal-agent split in the bank: banker and beneficiary are both `zcode`. The relevant game is
time-inconsistency (Strotz; Schelling 1960/1984 on self-command): the present seat-instance banks a
loop to clear its attention debt (scan() stops reporting banked loops), and the future
seat-instance inherits both the saved attention and the blind spot if the receipt was false. The
invariant (dirac_loop.py:185-188) commits only to the label topology of the loop, not to the work
the receipt describes: the same hash would be banked whether or not the wiring happened. What
makes the bank non-vacuous is the identity assumption: that the name `zcode` names one continuous
agent whose future self's costs are discounted by its present self at a rate near 1. In a fleet
where "zcode" is many ephemeral processes sharing a name, the continuity assumption is the entire
trust root, and it is sociological, not cryptographic. The irony is structural: the invariant's
content-root property ("same set -> same invariant" :186) makes banked rows recomputable against
the live graph, so a banked invariant whose loop no longer exists is machine-detectable on read.
Nothing runs that check: context_pack.py:26 counts raw lines. The instrument with a real consumer
has no read-side verification; the instrument with read-side verification has almost no consumers
on its upper rungs. Trust flowed to where consumption was cheapest, not to where verification was
strongest.

## 4. The equilibrium, stated

In the stage game per claim (poster q in {verified, plain, false}; witness s in {check, abstain};
reader r in {consume, discount, ignore}), with the observed player set {zcode, operator} and all
other seats abstaining, the observed state is a Nash equilibrium:

- Poster posts plain (UNPROVEN) at zero marginal cost; deviating to "false as SUPPORTED" yields
  nothing extra (auto-demotion, G1 refusal); deviating to "verified" pays k for a rung (CORROBORATED)
  no reader currently consumes.
- Operator witnesses only when remediating structural defects that threaten the whole tape (the
  09-27 batch); per-claim witnessing buys a rung that needs two witnesses and cannot be reached
  by one player.
- Readers consume the ungated Dirac bank (context pack demand) and discount the gated ledger by
  admission status.

Every unilateral deviation is payoff-decreasing. That is the formal sense in which the estate's
receipt system is working exactly as designed and exactly below its design.

## 5. Falsifiable predictions (what would move the equilibrium)

1. A standing second witness seat with its own consumption demand makes corroboration reachable;
   SUPPORTED upgrades then pay, and the witnessing steady state should change from episodic to
   continuous. Watch for it: `ADMISSION: N corroborated` in verify output leaving 0.
2. G3 warrants on high-value SUPPORTED rows convert notarization into knowledge: any reader's
   dominant check becomes a one-subprocess rerun. Watch for: any row carrying `warrant` (today 0).
3. A read-side Dirac check (recompute each banked invariant against the live graph; count vanished
   loops as open again) prices false banking into the operator's own pack. Watch for: a `closed`
   number in context_pack that can decrease.
4. Seat-spoofing remains unpriced until the estate has heterogeneous owners; the first multi-owner
   surface (OpenClaw cage policy already touches this: DIRAC_BANKED_INVARIANTS.jsonl rows 2-3
   record the switchboard/effect-broker boundary) will need authenticated seat identity, at which
   point two-eyes must be upgraded from attention law to sybil law.

## 6. Anchors

Tirole (1986) on collusion-proof hierarchical supervision (two-eyes as supervisor separation);
Palfrey and Rosenthal (1984) on threshold public goods and volunteering (corroboration at
threshold 2 with one volunteer); Holmström (1982) on moral hazard in teams (residual claimant as
sole monitor); Schelling (1960; 1984, "The Intimate Contest for Self-Command") on commitment
devices across self-instances (the Dirac bank); Kreps and Wilson (1982) on reputation (the
immutable tape makes every caught lie a permanent type signal: FORGED as a scarlet letter at
:130-131); the Lamport/Shostak/Pease Byzantine flavor of CORROBORATED (machine-recomputed g1 plays
the cryptographic role, human seats play independent observation, quorum 2-of-N distinct).
