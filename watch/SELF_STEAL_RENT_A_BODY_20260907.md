# SELF-STEAL: RENT-A-BODY — same bug, many jackets (2026-09-07)

**Trigger:** operator, watching the seat burn hours on Nous cloud-instance auth:
"lol this is the vast.ai shit wearing a different jacket — self steal."
He named the pattern before the seat did. Card written to keep the receipt.

## The jacket family (one bug, many jackets)

| jacket | era | what it promised | where it died |
|---|---|---|---|
| vast.ai blades | Sep-01 radar era | cheap on-demand GPU bodies ($0.10/hr, below covenant cap) | INFO-ONLY vetting; vendor portal owns the machine, the account, the lifecycle |
| Nous cloud instance "Q" | Sep-07 ($220 armed) | always-on Hermes body, scales to zero | 503 "Auth provider 'nous' unreachable" — the body answers to the vendor's auth provider before it answers to us |

## The root (survives translation)

**A rented body answers to its vendor's gates before it answers to the fleet.**
Auth providers, platform toggles, scale-to-zero windows, portal OAuth — every
capability sits behind a switch we do not hold. When the seat needs the body,
the seat must first negotiate with the vendor. That inverts the sovereignty
shape the fleet already paid for: files over processes, senses live in the
cage, fleet services loopback-only, no seat is load-bearing. A body whose
on-switch is a vendor dashboard is a seat that can go dark for reasons the
record cannot even read.

## The recorded correction (already on the walls — this card just re-applies it)

- **The body lives where the keys and files live.** The local gopher (hermes.exe)
  took one hour to wire and answers in 26s; the rented body took five attempts and
  answers only through its vendor's own front door.
- **Native protocols over vendor portals.** tailnet (up), `hermes serve`
  (up, loopback 9119), `hermes gateway` (Telegram/Discord/WhatsApp, built-in) —
  the pocket body needs zero strangers.
- **Rocinante (Oct 27)** is the real answer to "always-on substrate": owned
  silicon, no vendor gate between the Operator and the horse.

## Ruling

1. **Q is demoted from driving target to appliance.** It keeps exactly the
   vendor-native jobs that work through the vendor's own door: dashboard chat
   (works today) and the Chronos morning pulse (fires while scaled to zero).
   The seat stops trying to peer-drive it; no more auth archaeology.
2. **The pocket body is the native stack:** gopher + tailnet phone door (live) +
   gateway platforms on operator GO (Telegram token = 2 minutes).
3. **Keep Q running for now** (~$0.56/day ceiling, scales to zero; the pulse is
   real value). Revisit at Rocinante day — if the horse makes always-on owned
   bodies trivial, Q retires the way OpenClaw did: ideas kept, jacket retired.
4. **Status change, not a failure:** the $220 stays the Hermes work budget — it
   now routes to the LOCAL gopher's Nous lane (proven: NOUS HELM LIVE), not to
   the cloud instance.

## Falsifier (what reopens the ruling)

Any rented body that can be driven end-to-end without vendor-gate ceremony —
a peer dm that answers, an API that takes our key without an OAuth priest —
reopens "rent as burst capability" exactly the way the hardware radar kept
vast.ai as covenant-compliant burst: fine as a rental lane, never as the body
the fleet stands on.
