# ONIONCLAW SECURITY REVIEW + ADOPTION VERDICT (2026-10-04, ~03:00Z)

Operator GO received (the re-dropped link after the GO question). Repo
fetched to the review sandbox: corpus/steal/onionclaw_review/OnionClaw-main/
(10 python files, 5,808 lines, OUTSIDE the key tree, never executed).

## THE REVIEW

- **Clean.** No eval/exec/base64-decode/pickle anywhere. subprocess is Tor
  process management only. Every endpoint matches the README (check.
  torproject.org, GitHub releases, 12 .onion search engines incl. Ahmia and
  OnionLand). Apache-2.0, SPDX headers, CI, SECURITY.md, and the engine
  ships its own content blocklist (sicry.py:517).
- setup.py is an interactive wizard that patches /etc/tor/torrc and can
  sudo-add groups - legitimate for its purpose, and it never runs silently.
- The engine (sicry.py, 3,598 lines) fetches .onion over a local Tor SOCKS
  proxy (127.0.0.1:9050) - no key-bearing egress, no phone-home beyond the
  release check.

## THE VERDICT: PATTERN-STEAL NOW, RUN OPERATOR-GATED

The capability is real and the estate has three legitimate uses: the
librarian's dark-web primaries, threat-intel self-search, privacy routing.
The risks are structural, not malicious: (1) Tor egress defeats our endpoint
fences by design - a Tor allowance must be EXPLICIT in any lane config;
(2) dark-web claims are maximally unverifiable - the no-fabrication law
means every row banks its fetched bytes or does not exist; (3) it is a new
cage - cage law requires operator GO, which this receipt records as given
for the PATTERN STEAL and the SANDBOXED REVIEW, not for production arming.

## THE ADOPTION PATH (each gated)

1. DONE: sandboxed review (this receipt).
2. Next sitting: the librarian reads sicry.py's 12 engine definitions and
   steals the search-engine list + the Tor SOCKS fetch pattern into a
   librarian-only tool - pattern-steal, not a vendor dependency.
3. Any run: a dedicated venv outside the key tree, TOR-only egress, receipts
   banking every fetched byte (the no-fabrication law at maximum strength).
4. Operator GO required again before step 3 fires for real.

## THE SUPPLY-CHAIN NOTES

- Post credits christinminor459's repo; the code is JacobJandon's (fork or
  re-post - unverified which is upstream). The tarball reviewed is
  christinminor459/main. JacobJandon's repo was not diffed.
- The SICRY engine is vendored as sicry.py with a sync script - upstream
  updates flow through a third-party sync script, so pin the version if
  adopted.

Filed by the flash seat. The review sandbox stays at
corpus/steal/onionclaw_review/ - bytes retained for re-audit.
