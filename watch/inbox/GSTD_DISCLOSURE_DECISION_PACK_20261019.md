# GSTD DISCLOSURE DECISION PACK (2026-10-19)

**30-second summary:** On 10-15 our seat hardened the third-party gstdbot code: 47 shell-injection sites converted to argument-array exec, the leading-dash option bypass (`--upload-pack=evil` as a "branch") closed, SSRF class guarded (7 additional sites in round 2), tsc clean, scanner highs 1,190 -> pattern floor 147. The portable diff sits committed on branch `fix/security-hardening-20261015` (HEAD 11c6b49) at `C:\Users\foste\Documents\projects\gstd_mirrors\state_gstdbot` (relocated out-of-repo 10-15 to clear the Mimosa L3 gate). One decision is owed since 10-15: ship upstream, hold private, or rewrite. Receipts: `watch/inbox/gstd_soak_20261014/GBOT_FIX_STATE.md`, `watch/inbox/GSTD_MAP_20261016.md`, `watch/inbox/TON_EXIT_20261019.md`.

## BLOCK 1 - the decision

WHAT: pick one disposition for the disclosure branch. WHY: the moat stays unspoken until shipped and the mirror disposition has been owed since 10-15. WHEN: operator decides now; shipping is one PR from the staged branch. WHERE: upstream github.com/gstdcoin `gstdbot`; branch staged at `C:\Users\foste\Documents\projects\gstd_mirrors\state_gstdbot`.

1. **SHIP THE GIFT.** Open the disclosure PR to upstream gstdbot; credit our seat anonymously per veil law (founder/fleet never named). Blast radius: public reveal of the closed bypass class; upstream gets free hardening. Reversibility: a PR can be withdrawn; the work is already committed. Tag: RECOMMENDED.
2. **ACCEPT AS DEBT, HOLD PRIVATE.** Keep the branch private, log the 147 residual as named mirror risks. Blast radius: upstream stays vulnerable; our fixes exist only on a local mirror. Reversibility: fully reversible, ship any day. Tag: viable fallback, weaker standing.
3. **REWRITE BEFORE SHIP.** Re-architect for scanner-zero. Blast radius: days of work, no identified benefit. Reversibility: reversible but pointless. Tag: NON-OPTION. Our own receipt names it "a rewrite of GB's architecture, not a fix" and "not sensible pre-merge"; the 147 residual is the scanner's PATTERN class, not exploitable sinks.

## BLOCK 2 - meaning after the TON demotion (row 7)

WHAT: how each option reads post-demotion. WHY: the operator demoted the mainnet float on 10-19 ("we're not doing the ton", 400 TON personal funds to GB); row 7 carries the supersession. WHEN: effective 10-19. WHERE: `memory/fold_history/SUPERSEDED.md` row 7 + `watch/inbox/TON_EXIT_20261019.md`.

YES, the gift still buys standing on GB's rail. The estate still runs workers on that rail (MagGstdDrainDaily fires 08:00 daily, ~$0 cost, earning on GB's rail), and the map's one-sentence grounding holds: "gstdcoin sells the rail; the estate is the only fleet already running stateless verified workers on it" - the disclosure is reputation capital with the counterparty. The demotion removed the operator's float spend, not the rail relationship; the gift got cheaper to give since nothing financial is asked back. Option 1 banks that capital at zero marginal cost; option 2 forfeits it while the counterparty stays exposed; option 3 burns days against an unchanged relationship.

## BLOCK 3 - recommendation + falsifier

WHAT: option 1, ship the PR. WHY: the work is done, compile clean, zero marginal cost, and it buys standing with the counterparty the drain still depends on; option 3 is refuted by our own receipt. WHEN: next operator window, one PR. WHERE: PR from `fix/security-hardening-20261015` (11c6b49) to upstream gstdbot; veil law: anonymous seat credit only.

**Falsifier:** the recommendation is wrong if shipping produces hostile contact (upstream identifies the seat or fleet despite the veil, or sends legal/cease contact) or if GB's reaction turns negative before the drain's next clean cycle. Either observation means the gift cost more than the standing it bought, and option 2 becomes correct.
