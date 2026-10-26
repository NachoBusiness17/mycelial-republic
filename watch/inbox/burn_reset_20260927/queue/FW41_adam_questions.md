# FW-41 — Adam rulings packet: names / meta / storyline questions

**2026-09-28 · Q-027 (burn-reset gopher) · task: fifty-wide 09-17 board §H**
The operator asked (09-15 board, re-seeded) for a draft question list needing his ruling before
the game estate goes further public. Every question is grounded in code/doc state read this
session; each carries a default so silence is also an answer. Related receipts: FW-40 (ascension
curve), FW-42 (public deploy card), both in this directory.

## A. Names

1. **The MUD's real name.** The file is `games/mud.html`; the game calls itself THE CRIMSON
   MONASTERY (mud.html:107). Which name is canon for the site, the arcade card, and speech?
   *Default if silent:* the monastery title is canon, `mud.html` stays as the file name.
2. **Champion and horde names.** MARSHAL QETH, SISTER HALVANE, VERAK THE UNSEEN, MAGUS OLDRIN
   (mud.html:151-156) and the dwarf-roll name pools (Uzol Cavernmurder, …, :438-441) are
   placeholders that stuck. Canon, or do you want naming passes before public eyes?
   *Default:* canon as-is.
3. **"Nacho Business / Nacho Quixotic" as the operator's public face** (site/build.py:14, :300,
   :396) vs the letter page addressed "For Adam — from the machine room" (build.py:26,
   LETTER_ADAM_CRIGLER.md). Both personas ship in one build. Is the Adam identity meant to be
   public on the same site, or should the letter be anonymized/pulled?
   *Default:* leave both as built (they already deploy together).
4. **The games-count stat.** The work page claims "10/10 games live & playtested on prod"
   (build.py:412) while the build ships 22 games (GAMES list, build.py:30-33). Which number is
   the honest one to publish — and does "playtested on prod" hold for all 22?
   *Default:* recount and republish the stat before the next deploy.

## B. Meta (progression, privacy, deployment)

5. **"ASCENSION" is a Slay the Spire term** (spawnEnemy comment says so, mud.html:775). Keep the
   homage or rename the ladder (e.g. "DEPTHS", "PENANCE") before the public deploy?
   *Default:* keep; the steal is acknowledged in code comments.
6. **Does the ladder top?** FW-40's sweep (same directory): the curve never caps, the UI lies
   past A20 (`min(G.ng,20)`), and speed double-dips so everything outruns the player from A4.
   Ruling requested on FW-40's three recommendations (honest cap, speed decouple, truthful
   label).
   *Default:* apply recommendation 1+2 at the next mud code-touch.
7. **The bones of strangers.** The monastery raises the actual dead — `localStorage` bones carry
   real prior players' names and causes into new runs as hauntings (BONES-ROLL, mud.html:914-922;
   the courtyard is "sanctified", :915). When Melissa/Marque/Adam play (TEAM.md door), whose
   deaths become canon in someone else's game, and is a browser-local graveyard OK for the public
   build?
   *Default:* local-only bones; no cross-device sync, so no privacy exposure beyond your own
   machine.
8. **The presence relay's reach.** FW-37's ws spike (same directory) is LAN-only by intent
   (mud_relay.py bind guard, no auth). Should a public relay ever exist (needs a real server +
   auth), or is multi-lantern play forever a same-Wi-Fi/Tailscale party trick?
   *Default:* LAN-only forever; the relay docstring keeps the guard.
9. **Where do games live on the public site?** The walkable work page iframes a rotating few
   (build.py ROOMS "PLAY THE PROOF"); the other ~17 ride `dist/games/` with no index page. Build
   the arcade index (`games/index.html` exists on the dashboard side, absent from the GAMES copy
   list) or leave the long tail semi-hidden?
   *Default:* ship the arcade index next deploy.

## C. Storyline

10. **The First Dragon.** The nave is "The Nave of the First Dragon" (mud.html:156); the banners
    shout "THE DRAGON REMEMBERS" / "LANTERN, BURN" (:199); victory is the dragon's fall. What is
    the dragon in fleet canon — the backlog of unpaid attention, the corpus, the operator
    himself? One paragraph of canon would let the ending screen say something true.
    *Default:* the dragon stays unnamed and unexplained (it already works as opaque myth).
11. **The monastery's homage.** Scarlet-Monastery structure is acknowledged in the continuity
    notes; the room names (refectory/infirmary/scriptorium/crypt/forge/nave) are generic enough,
    but the crimson palette + seal-then-fight loop is a WoW read. Homage kept, or reskin before
    the stranger-facing deploy?
    *Default:* kept.
12. **Who were the four champions in life?** Qeth/Halvane/Verak/Oldrin have ranks and moods (the
    grudge telegraph system, W4) but no history. One line each would make the sigil economy mean
    something (four champions → four sigils → the nave gate, mud.html:945-948).
    *Default:* write them in-engine from their grudge lexicon, no backstory doc.
13. **One universe or anthology?** The estate ships the monastery, frontier_souls, arrakis,
    swarm, ruins_go, spectral_maze, wipeout… Does the public face claim a shared canon (the
    "estuary shore" already gestures at it, build.py:67-69) or present each game as its own
    world?
    *Default:* anthology with a shared footer, no forced canon.
14. **The letter's final text.** `letter.html` builds from LETTER_ADAM_CRIGLER.md verbatim on
    every `site/build.py` run. Is the text final/approved for the public deploy FW-42 arms, or
    does it need one operator pass first?
    *Default:* one pass requested at deploy time; FW-42's card lists it as a pre-deploy check.

## How to answer

Any subset, any order — reply inline (Q#: answer). Defaults above apply where the desk never
frees. The only ones that BLOCK the FW-42 deploy are Q3/Q4/Q14 (all on the public face); the
rest gate future game work, not the push.
