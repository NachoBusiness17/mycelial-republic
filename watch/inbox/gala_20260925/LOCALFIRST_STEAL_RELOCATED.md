# RELOCATED 2026-10-19 (night shift)

The localfirst-steal cache (third-party repo sweep, continuous-ai-main) that
lived here moved to:
`C:\Users\foste\Documents\projects\steal_caches\gala_20260925_localfirst-steal`

Why: the Mimosa L3 commit gate counts this tree in every scan; the cache's
path-traversal test fixtures (test_filereader.py highs) kept blocking ALL
main-repo commits. Precedent: GSTDBOT_RELOCATED.md (state/gstd_full/) - the
gstdbot mirrors relocated out-of-tree 2026-10-15 for the same class of block.
Third-party steal caches live outside the repo tree from now on.

The files remain in git history (pre-relocation commits) and the gala receipts
of 2026-09-25 still cite their original paths.
