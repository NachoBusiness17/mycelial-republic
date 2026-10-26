# RELOCATED 2026-10-15

The gstdbot clone that lived here moved to:
`C:\Users\foste\Documents\projects\gstd_mirrors\state_gstdbot`

Why: the Mimosa L3 commit gate counts this tree in every scan; after the
security hardening (branch fix/security-hardening-20261015, highs 1,190 ->
pattern-floor), the residual pattern flags kept blocking ALL main-repo
commits. Reference mirrors of third-party code now live outside the repo
tree, in C:\Users\foste\Documents\projects\gstd_mirrors\.

The disclosure branch (fix/security-hardening-20261015, HEAD 11c6b49) is
the responsible-disclosure diff for upstream gstdbot.
