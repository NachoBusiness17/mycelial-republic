# HERMES DIGEST 2026-10-16 (lane fire 7)

- FETCHES: github atoms OK x2 (hermes-agent through 2026-10-16T13:05,
  Herald-OS through 10-16T11:07); fxtwitter timelines 404 x2 - X-surface
  OWED carries (x-history miner, build-session item).

## Signals (hermes-agent, last 24h - an INSTALLER day, six macOS git fixes)

- fix(install) x5 + test: macOS git/CLT-stub detection (install git when
  /usr/bin/git is the Command Line Tools stub, report errors when CLT is
  already present, treat dev tools as present only when they work,
  prerequisites stop point, git-required message on PATH failure).
  MEANING: upstream is hardening THEIR installer's detection logic on
  exactly the class our install_into_cli.py lives in (present-but-broken
  toolchains). The lesson travels: detect-and-verify functionality, not
  path existence. ACTION: our installer's CLI detection checks PATH
  presence only - add the same present-only-when-working posture (run a
  --version probe) when corpus v2 touches it.
- fix(cli) + test: classify unmapped container paths in the requested
  profile; drive-letter volume parse tested on Windows lanes. MEANING:
  upstream carries Windows drive-letter handling in tests - the
  cross-platform posture our installer will need if the conf demo runs
  on a mixed room.

## Signals (Herald-OS - alpha 5 + the voice fallback chain)

- Release 0.1.0 alpha 5 (three days after alpha 3 - daily-to-biweekly
  shipping cadence holding).
- Voice fallback chain: when Hermes's voice fails, the computer's own
  voice says the line (a stopped clip's wait ends at once); docs for the
  fallback chain and an Edge fix. MEANING: the degradation-ladder
  pattern - primary fails, fall down the chain, never silence - is OUR
  overflow routing law (funded -> deepseek -> free fleet -> local) in
  their voice domain. Convergence, not gap.
- Studio home-folder boundary fix; Calc time-of-day parsing - WATCH.

## Triangulation summary

- Nothing breaking. One carried ACTION: installer detection gains the
  present-only-when-working posture at corpus v2 (upstream precedent:
  the macOS CLT-stub class). Seven fires, zero missed.

## Standing context

- MagHermesBurn247 hourly; conf 10/30 banked builds + rehearsal pending;
  ML moonshot riding; driving ladder unchanged.
