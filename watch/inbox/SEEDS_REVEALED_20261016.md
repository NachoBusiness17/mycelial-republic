# THE SEEDS REVEALED - Claude solves the ECDSA curve-origin mystery (2026-10-16)

Classification: RECEIPT (intel; major field event)
Producer: zcode-seat-20261016
Source: @sweis (Steve Weis, one of the authors) 2:41 PM today, 1.7M views;
article: anthropic.com/research/ecdsa-curve-origins (read via the seat-driven
link). Dropped without comment by the operator - the estate read it.

## What happened

An Anthropic employee asked an internal Claude model to investigate how the
NIST elliptic-curve "seed" values were generated - the 20-byte constants
(P-256's: C49D3608 86E70493 6A6678E1 139D26B7 819F7E90) whose hash defines
each curve's coefficient b, supplied by the NSA with FIPS 186-2 and never
explained, fueling two decades of backdoor speculation. In roughly half an
hour, Claude determined the origins of the seeds for P-192, P-224, P-256,
P-384, P-521, plus the ANSI X9.62 example curves.

## The method and the answer

- The rumored "hash of a funny passphrase" story: WRONG.
- Claude suspected 1990s-era C library pseudorandom generators, scanned the
  seeds for recognizable output patterns, and found a zero top-bit pattern
  (probability 1/5810 by chance) identifying lrand48, a linear congruential
  generator.
- Truncated-state recovery via the LLL lattice algorithm: the seeds came
  from lrand48() >> 23. Running the generator BACKWARDS revealed each
  srand48 initialization was a UNIX TIMESTAMP between May 1997 and April
  1998; the binary-curve seeds used timestamps halved (mapping to April 17,
  1998). Reproduction code is published - P-256's seed is candidate 1842
  from its run.
- The six base points (P-192 and five ANSI curves) explained via Arjen
  Lenstra's FreeLIP generator with small integer seeds (20000, 20517).
- People: Anthropic employees incl. Nicholas Carlini, John Wood, Henry de
  Valence, Paul Crowley, Steve Weis; posthumous credit to the NSA's Jerry
  Solinas. The $36,864 bounty goes to the Internet Security Research Group.
- SECURITY STANDING: not a break, not a weakness in the curves. The mundane
  timestamp origin makes intentional backdoors far LESS plausible. Open:
  B-163's seed, the base points of P-224/256/384/521, why some viable
  candidate curves were skipped.

## Why the estate banks it (four ties)

1. TON is Ed25519 - our keys were never on these curves - but the entire
   ECDSA rail our bridges and counterparties live on just had its founding
   distrust retired: the two-decade "NSA curve backdoor" prior dies by
   mundane timestamp.
2. THE METHOD IS OUR METHOD, at world scale: suspect the generator, scan
   for a statistical tell (1/5810), recover truncated state with a lattice,
   run it backwards to timestamps - suspect-generator archaeology with a
   falsifiable tell, exactly the drift-patrol/trust-bytes discipline. An
   agent doing twenty-five-years-unsolved cryptographic archaeology in half
   an hour is the Cammarata thesis ("already clean, agents just got able")
   proven in a second domain the same day.
3. The humanizing detail matters: Jerry Solinas generated them with what was
   almost certainly a shell one-liner in 1997-98. The most feared constants
   in cryptography were a timestamp. Institutions are mundane; only their
   silences are scary.
4. The operator dropped it with no comment on the day our own rescan ruled
   "zero seed-phrase matches" - seeds in every sense this week.

## Falsifier

Anthropic published reproduction code (P-256 = candidate 1842). If the
reproduction does not yield the seed on a clean machine, the claim breaks.
Run it before this receipt's trust upgrade is quoted anywhere.
