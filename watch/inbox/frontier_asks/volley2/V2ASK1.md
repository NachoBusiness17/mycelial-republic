# THE ASK: BUILD INSTRUCTIONS - THE AUTH TRINITY (Q03+Q04+Q19)

You are answering for an operator who runs a production agent mesh (context
in the file V2CTX.md one directory up). Three frontier-bound server-security
questions from the 52-question inventory (file FIFTY_QUESTIONS.md upstream):

- Q03: post-auth line-JSON frames carry no MAC/TLS; one flipped byte
  reattributes forged moves to a real identity (the anti-cheat receipts then
  launder the forgery - the chain faithfully records a crime it cannot see).
  Ask: design the frame-integrity layer - K-derived MAC per frame vs
  pinned-cert TLS vs both; exact wire-format change; migration path that
  does not break existing TCP clients mid-session.

- Q04: our SRP6 imports the mangos WoW variant verbatim (256-bit N, k=3,
  SHA1 throughout). Ask: the retirement-or-upgrade decision tree (RFC 5054
  2048-bit + SHA-256 port vs TLS + memory-hard hash stranger-grade vs
  OPAQUE at federation width); what each costs in GDScript-without-bigint;
  the recommended path for a one-stranger-first game.

- Q19: two transport doors (asyncio ws + blocking TCP) share one world; a
  hung ws task may leave half the peers silent while the room ticks on.
  Ask: the liveness architecture - one door or two, supervision design,
  the visible-degradation law (degrade visibly, never silently).

Deliver: buildable specs (files, functions, wire bytes), each with a
falsifier test. Tag [public]/[inference]. Name disconfirming evidence for
load-bearing choices. 1200-2500 words.
