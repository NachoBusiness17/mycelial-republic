# W2-B: small-debt sweep (verbatim agent bank)

**Date:** 2026-09-26 · **Writer:** zcode-seat-20260926 (banking agent: Explore W2-B) · **Class:** RECEIPT / debt sweep
**Closes:** GTA-lineage report debts #4 (GMod), #6 (off-GitHub re3), #7 (alt:V health), plus LA Noire modding depth from the precedents agent. Fetch-only, no search engines.

## 1) Garry's Mod / DarkRP

$9.99 on Steam (no active discount; Facepunch Complete bundle -10%). Slots: official dedicated-server guide shows `+maxplayers` as operator-set (examples 20/32) with NO fetched hard cap (the commonly cited 128 engine ceiling NOT confirmed on fetched pages). Public servers need a GSLT token (`sv_setsteamaccount`) or ranking is penalized, plus Facepunch Server Operator Rules and `sv_location`. Repo actively maintained through 2026-09-14; 2025-26 changes with RP relevance: player-model selector overhaul + `player_manager.AddValidModel` validation (affects custom job/model RP servers), voice-chat HUD fixes (voice = core RP plumbing). Confidence: HIGH price/GSLT, MEDIUM slot ceiling, MEDIUM-HIGH updates.

## 2) alt:V

Mixed, trending weak: altv.mp itself returned HTTP 521 (origin down) on two fetches 15 minutes apart. Docs ALIVE (docs.altv.mp): free, slot limits set by hardware not license, C#/JS server scripting, built-in voice, server browser, MLO support. But the core is CLOSED: altv-server/client/docs repos 404 on the GitHub API (issues-only development), altv-issues last pushed 2024-09-07 with 477 open issues, example-resources May 2024, the ragemp bridge archived June 2025. Practical read: lighter/free alternative on paper, closed core + stale tracker vs FiveM's open ecosystem. Confidence: MEDIUM (521s may be infrastructure, not abandonment).

## 3) re3 mirrors off GitHub + legal posture

Confirmed circulating: GitHub API returns "Repository access blocked" for GTAmodding/re3 (DMCA, block created 2021-09-30, referencing Take-Two's 2021-09-29 take-down notice). Mirrors persist on smaller forges: Codeberg Jeder/re3 (updated 2024-12-03), archived keks24/re3, pac85/re3-aur, aldrinbalitbit/re3-ports (active 2026-04-16); GitLab ecosystem incl. the dca3 Dreamcast port (automated repos active through 2026-09-26) and a PSP "re3 portable" (2026-09-18). Working console ports imply compilable code circulates; mirror fidelity to the original final state unguaranteed. Legal posture: Take-Two enforcement is episodic and channel-targeted (GitHub honored; Codeberg/GitLab untouched). Public redistribution = real DMCA exposure (the exact scenario that already happened). Private study = lower-risk but NOT clean (claimed derivative of copyrighted code; re3's own license claim is precisely what Take-Two contested). Confidence: HIGH mirrors/block, MEDIUM legal posture (analysis, not legal advice). Seat note: this sharpens the noir pack's "avoid" to precise terms: private lab curiosity is one thing, any public artifact built on re3 is the 2021 scenario replayed.

## 4) L.A. Noire modding depth

"Fix-only scene" CONFIRMED: PCGamingWiki's entire Mods section lists exactly ONE content mod ("Coax, Force and Accuse", restoring original interrogation prompt labels); everything else is patches (widescreen, intro skip, FPS workaround). Deepest community artifact: LANVP (L.A. Noire V-Patch), single-maintainer open-source technical patch, 543 stars, v2.0 Aug 2024 (30FPS uncapping, ultrawide): a patch, not a modding platform. Nexus unreachable (403 Cloudflare) on both slugs, caveat noted. Confidence: HIGH for no content-creation ecosystem. Seat note: closes the "steal LA Noire grammar, never assets" loop: there are no assets or tools to steal anyway; the grammar (interrogation-under-ambiguity, desk progression) is the only import, exactly as the precedents agent ruled.

## Verdict

No ranking changes from this sweep except confirmation: FiveM remains the only live sanctioned GTA-V path (alt:V weak, GMod $10 but Source-engine map burden, re3 legally fenced, LA Noire empty). The noir substrate decision is now fully informed on every axis named in the original ask.
