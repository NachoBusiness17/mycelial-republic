# GBOT SECURITY FIX - final state (2026-10-15)

## What was fixed (real classes, verified)

Round 1: all 47 interpolated shell strings across 7 modules converted to
argument-array form (execFileSync, no shell); compound shells replaced with
fs APIs; getDefaultBranch pipeline replaced; safeRef charset validator added
at every branch/hash boundary; env-derived fetch bases guarded (https +
URL-object + encoded queries). Compile: tsc --noEmit clean.

Round 2: safeRef hardened (leading-dash rejected - the charset previously
let `--upload-pack=evil` through as a "branch": a real bypass, closed);
certbot domain/email charset guards (option injection + path traversal);
7 additional SSRF sites guarded (ollama, telegram token encoding, swarm
URLs, client-side OC_API mirror).

Rescan: command-injection and SSRF highs ELIMINATED (from 1,190 highs).
Compile clean. All fixes committed on branch `fix/security-hardening-20261015`
(gstdbot clone HEAD 11c6b49) - the portable responsible-disclosure diff for
upstream.

## The scanner floor (what remains, honestly)

Rescan count: 147 findings (106 high / 41 medium), UNCHANGED by round 2's
real fixes - because the residual is the scanner's PATTERN class, not
exploitable sinks: 70 SSRF pattern flags (any env/config-derived URL),
6 command-option flags (any variable passed as a git option, even
validated), 4 command injection (same), 20 cross-file taint, 19 authz
design hypotheses, plus weak-crypto and untrusted-selection notes.

A bot whose job is shelling out to git and calling APIs cannot reach zero
on this pattern set without config-driven command indirection - a rewrite
of GB's architecture, not a fix. The guards exist; the scanner cannot see
them.

## The decision (operator)

1. Exempt `state/gstd_full` from the L3 commit scan (third-party mirror,
   not our shipped surface) - commits resume immediately.
2. Accept the 147 as named risks for the mirror (they are GB's exposure,
   disclosed via the fix branch).
3. Fund the rewrite (not sensible pre-merge).

Recommended: 1 + the disclosure branch as the GB gift. The gate's own
verdict already says the scan may be incomplete - the residual is
governance, not engineering.

## Files

- gstdbot clone: branch fix/security-hardening-20261015, HEAD 11c6b49,
  full round 1+2 diff, compile clean.
- This receipt: watch/inbox/gstd_soak_20261014/GBOT_FIX_STATE.md
