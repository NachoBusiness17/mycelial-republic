# FREE-LANE BRIEFS — GAME PLATFORM PROGRAM (2026-09-29)

For the stealth driver / free-lane runner rotation. Each brief is SELF-CONTAINED per estate law: no conversation context needed. Outputs are banked as findings (sensed, never done) and land under `watch/inbox/game_platform_basecamp_20260929/` with the brief id in the filename. Sensing surface only; verification climbs to the funded tier.

Context capsule every brief inherits: the estate is building (a) a WoW clone: Godot 4.3 client + CMaNGOS mangos-wotlk server (GPL-2, checkout at corpus/library/mod-playerbots, core @ 49dfc1f, bots @ b685d7eb) and (b) a game platform where its GWAP verification machinery (agreement-as-anti-cheat payloads, frozen-tape replay graders, verkle ledger) is the product other developers build on. Constraint: roblox-like distribution WITHOUT predatory monetization or child-safety failures. Meters weighted to rare byte-backed artifacts, never match-early volume.

## BRIEF FL-1 — CMaNGOS Windows build checklist
Produce a step-by-step checklist to build mangos-wotlk (CMaNGOS, C++17-era CMake project) on Windows 10 x64 in 2026: exact winget/choco package names and versions (CMake, Visual Studio 2022 Build Tools C++ workload components, MariaDB or MySQL Community, Git, OpenSSL if required), the CMake generator flags that work with MSVC for this tree, the MySQL service setup steps, and the three most common build failures for this era of CMaNGOS with fixes. Output: checklist only, cited to doc pages.

## BRIEF FL-2 — wow protocol 3.3.5 auth survey
Survey the WoW 3.3.5 (build 12340) client-server protocol as documented by the emulation community: realmd logon challenge/response (SRP6), world-server auth session, movement opcode subset (MSG_MOVE_* player movement + acknowledged), packet structure (header sizes, encryption after auth: RC4/ARC4 session keys), and which documentation projects are authoritative (TrinityCore doc pages, protocol.woad.com or successors, MangosTwo sources). Output: an opcode map for a minimal "walk around the world" client + citations.

## BRIEF FL-3 — Godot 4.3 networking APIs for an MMO client
Survey Godot 4.3 stable APIs relevant to writing a from-scratch game client for a raw TCP protocol (not Godot's high-level multiplayer): StreamPeerTCP / PacketPeerStream, StreamPeerBuffer for little-endian struct packing, PacketPeerUDP, WebSocketPeer, Crypto/HashingContext (SHA1/SHA256/HMAC for SRP6 if needed), threading model for a network thread vs main thread (WorkerThreadPool, call_deferred, MessageQueue), and known pitfalls (packed byte order, varints). Output: API notes + a recommended client architecture sketch (network thread -> ring buffer -> main-thread apply) + citations.

## BRIEF FL-4 — mangosbot-bots architecture read
From the checked-out module at corpus/library/mod-playerbots/src/modules/Bots (mangosbot-bots @ b685d7eb): read the README + botpch/ahbot + main source dirs and summarize the architecture: how bots join the world (are they real player sessions?), the AI strategy layers, the AH bot economy, config surface (bot_account etc.), and what it would take for an EXTERNAL process (our Godot client or a seat) to drive a bot. Output: architecture brief with file paths.

## BRIEF FL-5 — agreement payload JSON schema v0
Draft JSON Schema (draft 2020-12) for the estate's noir GWAP payload, from this spec: {scene_id, intent_struct, report_struct, agreement_score, blocker_taboo_list, witness_clue_chain, verdict}, append-only per session. Add: participant roles (author/reporter/witness), consent flag, meter_credit object (artifact_rarity, byte_backed bool, receipt hash), replay_tape_ref (sha256 + engine version), and a signature block (ed25519 pubkey + sig). Output: the schema file contents + 3 worked example payloads (one clean agreement, one collusion-detected, one witness-dispute).

## BRIEF FL-6 — Roblox FTC consent order + safety specifics
Verify and summarize the FTC v. Roblox situation as of 2026 and Roblox's safety architecture (age estimation, chat filters, parental controls, DevEx economics): exact consent-order obligations if it exists, the DevEx cash-out rate vs. Robux purchase price (the scrip squeeze numbers), and the creator-economics criticism. Output: fact sheet with URLs, every number sourced.

## BRIEF FL-7 — reCAPTCHA pattern API map
Map reCAPTCHA as the closest GWAP-as-backend precedent: what sites integrate (the API contract), what Google harvested (labels for books/street views), the volumes achieved, how value flowed (free service for labels), and the 2020s deprecation/transition to paid Enterprise. Then: the design question — can a "verify-the-play" API be sold the same way reCAPTCHA gave away captcha? Output: the pattern map + 5 lessons for the estate's verification-as-a-service.

## BRIEF FL-8 — play-to-earn post-mortems
Post-mortem research: Axie Infinity economy collapse (numbers: DAU peak->trough, SLP price, scholarship model), other P2E failures (StepN, native-token MMOs), and what survived (Steam Workshop paid mods, Fortnite creator payouts, CS:GO/Dota2 marketplace item economies). Extract the design law: which player-earning designs survived and why (real demand? external currency? capped sinks?). Output: the law table + citations.

## BRIEF FL-9 — grok-4.7 dry run of the Opus ask (free stealth lane)
Run the fired-version ask (OPUS_ASK_DRAFT_20260929.md, Amendment 2 shape: baseline-attached, XML-structured, hostile-second-pass) through grok 4.7 on the free lane, at its max effort. Purpose: find where the ask is ambiguous BEFORE frontier money burns. Output: the ask returned verbatim problems — every place grok misread the ask, plus its best spec attempt. File as FL9_GROK_DRYRUN.md. Compare signal: if grok's return already matches BASELINE_SPEC quality, the Opus ask needs sharpening (the ask should be hard enough that mid-tier visibly fails).

## BRIEF FL-10 — local fleet dry run (gemma/glm-flash seats)
Same ask through 2 local/cheap seats (gemma:2b via ollama, glm flash via stealth lane). Purpose: calibration floor — the distance between local-attempt and BASELINE_SPEC is the visual proof of what frontier tokens buy. File FL10_LOCAL_FLOOR.md with the two attempts and a one-line delta verdict each.
