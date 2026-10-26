# W2-A: APB open-source claim — BURIED (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore W2-A) · **Class:** RECEIPT / debt burial
**Closes:** design-precedents debt #1 (APB primary-source hunt) and debt #5 (rAPB viability).

## Verdict: the "APB Reloaded will be open-sourced" claim is DEAD FOLKLORE. No primary source exists.

Fetch-only evidence trail (no search engines):
- **Wikipedia** (APB: All Points Bulletin): full IP chain documented (Realtime Worlds shutdown 2010 -> K2/GamersFirst 1.5M GBP 2010 -> Little Orbit 2018 -> Unit Game bought IP Aug 2019, Little Orbit retains Reloaded PC/console). ZERO open-source mention. Consoles shut down 2024.
- **Massively Overpowered**: full APB tag archive swept (7 pages, bottoms out Feb 2015). Coverage 2015-2025 = acquisitions, outages, New Horizon roadmap, console shutdowns. No open-source article EVER.
- **GitHub**: LittleOrbit org 0 public repos; unitgame 0 public repos; github/mattscott is an unrelated Unity hobbyist. Repo search "apb reloaded" (36 results) = graphics configs and fan tools only.
- **Live GamersFirst forums**: guest search "open source" = 57 hits, ALL community-side wishing (2023 roadmap replies, 2019 Fallen Earth shutdown wishes); the Feb 2020 "The End? Or The Beginning?" thread proposes community help while explicitly NOT open-sourcing. Announcements subforum's latest post is Feb 2025 downtime. No code-release announcement ever.
- Best explanation: garbled echo of player wishes during the 2019 Unit Game sale or the Fallen Earth shutdown. Buried from the lit review; retaining it would require a citation that does not exist (no-fabrication law applied to our own priors).

## rAPB (ivan-draga/rAPB) assessment

GPL-3.0, **9 stars**, 8 forks, last push **2017-08-07**, abandoned at birth. Contents: real skeleton (LobbyServer, DistrictServer, WorldServer, MyDB in C#/C++, 153MB) but README pins the 2016-era client (1.19.4.775380) and admits "You cannot enter districts yet": login/lobby-level emulation only, no missions/driving/combat. Viability for a private-server study: LOW (pre-2017 protocol vs updated client + GFAC anti-cheat, core gameplay never emulated, legal gray zone). Useful only as evidence the APB protocol was partially reverse-engineered.

## One-line APB verdict for the design doc

APB Reloaded is a closed-source cops-and-robbers shooter, PC limps along, consoles dead since 2024, no open-source path exists or was ever promised, and the lone fan emulator is an abandoned login-level stub: design inspiration for the CnR GWAP (faction-pair + witness-issued missions), never a platform.

## Seat note

This closes the noir pack's APB thread for good and upgrades the design-precedents receipt: its "unverified lead" is now a documented negative with a trail, which is the no-fabrication law working in reverse (we bury our own unverified priors with evidence, not silently).
