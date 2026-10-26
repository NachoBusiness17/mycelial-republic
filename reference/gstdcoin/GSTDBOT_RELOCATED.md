# RELOCATED 2026-10-15

The gstdbot clone that lived here moved to:
`C:\Users\foste\Documents\projects\gstd_mirrors\reference_gstdbot`

Why: the Mimosa L3 commit gate counts this tree in every scan; after the
security hardening (branch fix/security-hardening-20261015, the ported
command-injection and SSRF fixes, compile clean), the residual pattern
flags kept blocking main-repo commits. Reference mirrors of third-party
code now live outside the repo tree, in
C:\Users\foste\Documents\projects\gstd_mirrors\.

pull_gstdcoin_repos.cmd: update your target paths or re-clone fresh —
the old location is intentionally retired.
