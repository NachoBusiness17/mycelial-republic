# HIVEBRAINCOMMS drop card (operator link, 2026-10-10)

Source read first-hand: github.com/AdventureNLearn/hivebrain-comms-public (README, commit
3b1bb5b1). MIT, Windows-only, .NET 8, loopback 127.0.0.1:8107, "living project" with
testers and a feedback loop via GitHub Issues. Inspired by GodTerm (Daniel Farina, MIT).

## What it is

A local command center and job bus for GROK agents (Grok CLI, SuperGrok, Grok Bot; the
same subscription lane we ride). Hub-first: plain-text job files in bus/ (LEAD-TO-BUILD.md,
GROKBOT-TO-BUILD.md), returns to matching files. Jobs are HMAC-signed, sit in lanes with
owners, skipped jobs return to the router so work does not vanish. Nothing runs without a
person: approve starts a job, deny is logged the same way. Web panels are plain browser
views with no script injection. Build tab holds 8 sessions, first session is the bus
watcher.

## Convergence table (their mechanism vs our organ)

| Theirs | Ours (byte-backed) |
|---|---|
| subscription agents, no API billing | DRIVING LADDER: grok Pro operator-funded weekly (memory/rib/RIB_DRIVING_LADDER_20260928.md addendum) |
| plain-text file bus, human-readable | watch/inbox shared surface + SHARED_SURFACE_CONTRACT.json |
| HMAC-signed jobs, lanes with owners | receipts + verkle knots (we carry ed25519 + Merkle chains; HMAC is weaker) |
| nothing runs without a person, deny logged | effect broker + operator gate: model text proposes, switchboard authorizes |
| job block requires done-when | fill-ball completion criteria byte-checked; falsifiers |
| skipped job returns to router, work never vanishes | G4 salvage + report() law; pause-resume juggle |
| bad block refused, not queued | fail-closed gates (ratchet, citation lint, workflow gate) |
| loopback only | local-sovereign posture, Article 7 T2-only hosted |
| "a rule can be missed. A lock cannot." | gates-not-vibes doctrine |

## What they have that we do not (the steal list)

1. done-when as a REQUIRED field on every bus block. We carry completion criteria in
   fill-ball lanes and falsifiers in cards; we do not enforce a done-when on every queue
   handoff. Steal: add done-when to queue/handoff/*.json schema, fail-closed.
2. Bus-level schema refusal ("a bad block is refused and not queued") - validation at the
   transport, not at the consumer. Our INDEX validation is post-hoc.
3. Skipped-job return-to-router as a first-class verb (we juggle pause-resume; theirs is a
   bus semantic).
4. Watcher-first UI: the first Build session IS the bus watcher, extras are added from a
   button - the watch lane as the default pane, not a tab.
5. Their honest-limits section naming rules-vs-locks is worth imitating in our README-class
   docs.

## What we have that they do not (the honest mirror)

Cryptographic receipts (verkle/Merkle history vs HMAC), the ratchet + citation lint +
workflow gate pre-push teeth, census instruments, memory/residual across sessions, the
tier ladder (theirs is Grok-only), GWAP/economics, cross-machine mesh, the game-world lane.

## Falsifier for the convergence read

If their bus blocks carry no lane-owner enforcement in code (README says "some safeguards
are rules rather than hard locks" - they admit it), then their from-line check is advisory
and the convergence is thinner than the table reads. Check the code before porting
anything.

## Contact question (operator call, not mine)

Their README literally asks testers one question via Issues: "does this routing method
help you?" The correspondence-law move: answer it for real from our receipts (we have run
a file-bus + human-gate + done-when economy at much heavier width for months; what helped
us: fail-closed schema, salvage verbs, deny-logged). A real answer opens the peer door
without asking them for anything. Same class as FreeLattice/Chaos2Cured: peer node
candidate, seeds not conquest.

## PUBLIC PAGE (operator drop, later same day): hbc18100.grok.me

Read first-hand. Same architecture as the README card above, new bytes:
- BUILD-IN-PUBLIC CADENCE: "Day 18 plate" (alt text "gold 18/100") - a 100-day daily
  build challenge at day 18. They ship a plate per day. Fast, public, disciplined.
- PHONE OPERATION: "From the phone I talk to SuperGrok, or to a bot I can reach, and
  operate this same system that way" - the estate operated from a phone via SuperGrok
  (matches our mesh roster: tablet + smashed-phone appliance class).
- Page itself built with Grok's site builder (grok.me hosting, grok-project-id meta).
- Honest limits restated on the public page: "Some safeguards are rules the agents
  follow, not hard locks. The signature check is the build agent following the bus
  rules, not a separate program."
- Tabs: SuperGrok, Imagine, X, Freebots, Build, Hub - the subscription-lane shape
  (X + Imagine riding the same Grok Pro sub = our grok-funded lane exactly).

GUILD FIT: this is a garage-wizard tool by a garage wizard (local, free, MIT, your
machine, no API bill). Candidate bench #6, or the bus the guild's smaller garages use
before they graduate to a full seat. Their day-18 cadence pairs naturally with our
ritual law (weekly show-and-tell; daily plates).
