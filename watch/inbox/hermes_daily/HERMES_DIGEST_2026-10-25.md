# HERMES DIGEST 2026-10-25 (lane fire 16)

- FETCHES: github atoms OK x2 (hermes-agent through 2026-10-25T12:45,
  Herald-OS quiet since 10-20); fxtwitter timelines 404 x2 - X-surface
  OWED carries (x-history miner, build-session item).

## Signals (hermes-agent, last 24h - a VAULT CUSTODY day, 8 commits)

- fix(vault) x7 + test: a failed clone ROLLS BACK only the keychain entry
  it made; migrating a vault with no key SAYS SO instead of claiming
  success; an orphaned keychain entry (no pointer naming it) is DELETED,
  never left dangling; a --clone-all copy OWNS its keychain entry before
  it is published; a copied vault's new entry is KEPT when its pointer
  did land; session teardown still fences a late unlock after the TTL;
  smoke tests against the real macOS/Windows keychains.
- MEANING: upstream spent a day on VAULT CUSTODY - the ownership and
  cleanup semantics for secrets: who owns a keychain entry, what happens
  to orphans, what a failed migration must roll back, and the difference
  between "no key" and "key not found" (the vault says which instead of
  claiming success). 
- THE RESONANCE: this is the identity-isolation law (fire 14: tokens sit
  beside, never over) extended to the FULL custody lifecycle - creation,
  migration, clone, orphan cleanup, TTL fencing. The estate's parallel:
  our key-wizard's stored tokens and the mesh client's .env fences. The
  custody rules upstream shipped are the rules our key-wizard should
  adopt verbatim: rollback only what you created, say "no key" instead
  of claiming success, delete orphans rather than leaving them dangling.
- ACTION-WATCH: diff our key-wizard's storage against these custody rules
  before the conf demo (the wizard stores tokens the same way a vault
  does - the custody laws apply to us whether we adopted them or not).

## Signals (Herald-OS)

- Quiet (nothing since 10-20).

## Triangulation summary

- Nothing breaking. One ACTION-WATCH: the vault custody rules vs our
  key-wizard storage (rollback scope, orphan deletion, no-key honesty,
  TTL fencing) - a diff is one sitting and the conf demo's credential
  story gets stronger for it. Sixteen fires, zero missed.

## Standing context

- MagHermesBurn247 hourly; conf 10/30 banked builds + rehearsal pending;
  ML moonshot riding; driving ladder unchanged.
