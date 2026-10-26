# REPORT: moddable GTA lineage (verbatim agent bank)

Provenance: background Explore agent "Audit moddable GTA substrates", 2026-09-26, 24 tool uses / ~12 min, banked on the 20-minute clause. Verbatim capture; the agent's own punctuation preserved. Load-bearing claims carry URLs the agent fetched live. Debts are the agent's own list.

---

All core questions are answered and I'm at the banking mark. Here is the compact banked report.

# GTA-Lineage Substrate Research — 1950s Noir Cops-and-Robbers GWAP

## 1. re3 / reVC (reverse-engineered GTA III/VC) — **DEAD END, high legal risk**
- Take-Two filed a DMCA on the re3/reVC GitHub repos on 2021-02-19; the notice (listing the GTAmodding/re3 repo plus a fork network) is a primary source at https://github.com/github/dmca/blob/master/2021/02/2021-02-19-take-two.md
- Verified today via GitHub API: `GTAmodding/re3` returns **"Repository access blocked"** and `halpz/re3` mirror is also blocked — i.e., the repos remain taken down and GitHub-hosted forks get blocked on sight (https://github.com/GTAmodding/re3, https://github.com/halpz/re3)
- Take-Two sued the developers (Sept 2021, C.D. Cal.); case **dismissed April 2023** — with prejudice vs 4 named defendants, without prejudice vs 10 John Does, **no settlement terms disclosed, no ruling on clean-room reverse engineering** (https://www.pcgamer.com/take-two-dismisses-lawsuit-against-grand-theft-auto-modders/)
- Risk profile: no legal precedent set; hosting on GitHub = guaranteed takedown; building a persistent commercial service on re3 = derivative-work exposure to Rockstar with hostile litigant history. **Avoid.**
- **OpenRW**: technically alive but near-dormant — repo now at https://github.com/rwengine/openrw (original `OpenRW/openrw` 404s), last commit **2025-06-18**; README confirms open-source GTA III reimpl requiring a legit copy; **no multiplayer at all** → not a substrate.

## 2. GTA V via FiveM / Cfx.re — **RECOMMENDED PRIMARY**
- Rockstar **acquired Cfx.re on 11 Aug 2023** = sanctioned modding platform; earlier 2015 hostility noted (https://en.wikipedia.org/wiki/FiveM). Caveat: a Feb 2025 doc "The Fall of FiveM" described post-acquisition internal conflicts and ROME-replacement speculation (same source). Core repo active: pushed **2026-09-07** (https://github.com/citizenfx/fivem)
- Licensing: each player needs a GTA V copy — homepage FAQ: validates "if you actually own GTAV"; requires "Grand Theft Auto V Legacy" (https://fivem.net/)
- Moddability: "multiplayer-enabled modification framework… make anything you wish: roleplay, drifting, racing, deathmatch"; servers stream "custom cars, maps, weapons" (https://fivem.net/). Scripting Lua/JS/C# per docs — **docs.cfx.re was unreachable today (DNS/empty), verify** (debt)
- Gamemode scaffolding exists off-the-shelf: **QBCore** (Lua, GPL-3.0, jobs/inventory/economy/SQL schema, https://github.com/qbcore-framework/qb-core) and **ESX** ("trusted by 12,000+ communities", Lua, police/EMS/mechanics jobs, https://github.com/esx-framework/esx_core) — both active
- Scale: Wikipedia cites 250k concurrent players platform-wide (Apr 2021, NoPixel-driven) (https://en.wikipedia.org/wiki/FiveM); per-server max slots with OneSync Infinity (**~2048 claimed, unverified today**) = debt
- Vice City map remakes / 1950s asset packs for FiveM: **not verified** (gta5-mods tag page 404; readers rate-limited) = debt; environmental destruction on RAGE: expected **NO** (static world), unverified = debt
- Effort: **2–6 months** to a persistent noir RP server (QBCore jobs→cop/robber roles, MySQL persistence standard; art burden = sourcing/converting 1950s vehicles + map MLOs)

## 3. Cheap GTA-likes
- **Unturned** — Free-to-play, Smartly Dressed Games, released 2017-07-07, Steam Workshop, source/project files on GitHub, BattlEye (https://store.steampowered.com/app/304930/Unturned/); Unity engine; roleplay servers explicitly called out (https://en.wikipedia.org/wiki/Unturned); dev-maintained plugin fork active (pushed 2025-10-23, https://github.com/SmartlyDressedGames/Legally-Distinct-Missile). Effort **1–3 months**, zero per-player cost — but blocky aesthetic fights 1950s noir; best as prototype
- **Garry's Mod DarkRP** — MIT Lua RP gamemode with jobs/police/economy atop GMod (https://github.com/FPtje/DarkRP); per-player GMod purchase; Source-engine sandbox, not an open city → heavy map work. Effort **2–4 months**
- **open.mp (SA-MP successor)** — **ALIVE in 2026**: pushed 2026-08-11, release v1.5.8.3079 (2025-12-17), MPL-2.0, C++, backwards-compatible with SA-MP Pawn scripts (https://github.com/openmultiplayer/open.mp); requires GTA:SA copy. Effort **3–6 months** (dated engine/art for noir)
- **MTA:SA** — alive: v1.6.0 (Jun 2023), GPLv3, Lua resources, ~600k monthly players claimed, needs legal GTA:SA (https://en.wikipedia.org/wiki/Multi_Theft_Auto). Same dated-engine drawbacks as open.mp
- **alt:V** (GTA V multiplayer, alt route to FiveM) — org shows pushes as recent as 2026-06-30 (https://github.com/altmp) but site was down (521) today (https://altv.mp/) — secondary option

## 4. Other open-source GTA-like engines
- None found alive-and-multiplayer beyond the above within budget; OpenRW is the only true open engine and it's single-player/dormant. **Search gap = debt.**

## Recommendation + Debts
**Primary: FiveM + QBCore/ESX** (sanctioned, massive RP precedent, streaming custom assets); **fallback prototype: Unturned** (free, workshop, persistence). Debts: (1) docs.cfx.re unreachable — confirm OneSync max slots & Lua/JS/C# claims; (2) Vice City map remakes & 1950s vehicle packs on FiveM unverified; (3) RAGE environmental-destruction "no" unverified by source; (4) GMod price/slot limits unverified; (5) 8,100-repo fork-network DMCA figure from a rate-limited search summary only; (6) off-GitHub re3 mirrors not checked; (7) alt:V current player count/health unverified; (8) broader open-source GTA-like engine sweep incomplete.
