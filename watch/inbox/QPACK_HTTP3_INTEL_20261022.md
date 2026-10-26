# INTEL: HTTP/3 QPACK flaws - 4000x memory amplification (2026-10-22)

Source: The Hacker News, Oct 22 2026. Newly disclosed QPACK flaws (HTTP/3
header compression): a single unauthenticated HTTP/3 connection crashes
vulnerable servers via up to 4,000x memory amplification. 7 affected
implementations. Public PoC exists. Bun, aioquic, and h3 remain unpatched.

## The three reads

1. **Estate exposure check:** the fleet's public surfaces ride Cloudflare
   (dashboard, gstdcoin web) - Cloudflare's HTTP/3 stack is maintained
   upstream, not self-implemented. Local services are loopback HTTP/1.1.
   Direct exposure: minimal. Any future self-hosted HTTP/3 endpoint goes
   on the do-not-deploy-until-patched list.
2. **Bounty recon window (the money tie):** newly disclosed + public PoC +
   7 implementations + weeks-before-patches = the classic hunting ground.
   HTTP/3 QPACK implementations across the ecosystem are the target class;
   the PoC teaches the pattern. First-recon skill match: memory
   amplification via compression algorithms - the same class as the HPACK
   attacks of prior years.
3. **The pattern note:** compression-ratio weaponization (HPACK then
   QPACK) - the same physics as the estate's own compression lessons: any
   ratio that amplifies input can be weaponized into amplification DoS.
   The seam law again: the gap between what the protocol assumes and what
   the attacker sends.

## Standing order

The PoC lands in the bounty recon queue as the pattern study. No estate
action required tonight.
