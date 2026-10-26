# N7_GAME_DOCS_FETCH — gaming-history primary corpus (receipt)

- **Date:** 2026-09-16 · **Lane:** N7 (training docs for game-design vein) · **Laws:** receipt first (this file), append as you go, no git, no paid APIs, free fetches only
- **Target dir:** `memory/corpus/game_design_docs/` (+ `manifest.jsonl`)
- **Canon (reference, not re-fetched):** `watch/inbox/FROM_MUD_TO_WOW_20260914.md` (+ `_WITNESSES.md`) — Mark's MUD→WoW weave already in-repo. This corpus sits upstream of that canon (Bartle/MUD → roguelike → DF → Souls/StS) and is now the training floor for it.
- **Paywall law:** paywalled material skipped honestly and recorded as BLOCKED below, not pirated or approximated.
- **STATUS: COMPLETE.** 25 artifacts fetched (~12.2 MB), manifest sha256-verified, 4 blocked items recorded.

## Plan

1. Rogue lineage: original Rogue 5.x docs/manual; NetHack Guidebook + TILE FAQ.
2. MUD/CRPG lineage: Bartle "Interactive Multi-User Computer Games" (1990, mud.co.uk); Bartle Taxonomy original "Hearts, Clubs, Diamonds, Spades" (1996); Designing Virtual Worlds excerpts **only if legally free**; open-access scholarly CRPG/adventure history.
3. Dwarf Fortress GDC talks: free slides/transcripts only; otherwise record blocked.
4. Souls-family design analyses from serious sources (Game Developer/Gamasutra-grade).
5. Slay the Spire designer posts (Mega Crit / designer essays).
6. Manifest: one JSONL row per fetch — `url, file, sha256, title, era`; sha256 over saved bytes.

## Log (append as you go)

- (start) dirs created: `memory/corpus/game_design_docs/`, receipts dir; canon located at `watch/inbox/FROM_MUD_TO_WOW_20260914.md` — no re-fetch needed.
- Bartle IMUCG (imucg.htm, 1990) 200-OK — page splits into 8 section files (imucg0–7); all fetched and concatenated into `bartle_imucg_1990_full.html` (416,557 bytes; index kept as `bartle_imucg_1990_index.html`).
- Bartle HCDS (hcds.htm, 1996) fetched — verified ~12k words, full taxonomy paper.
- **DVW surprise:** `mud.co.uk/dvw` states New Riders **reverted rights to Bartle**, who offers the full *Designing Virtual Worlds* PDF free on his own site → fetched `bartle_designing_virtual_worlds_2003.pdf` (5,205,807 bytes). Legally free, author-sanctioned — beats "excerpts if legal" ask.
- NetHack Guidebook/dgn_comp/lev_comp fetched raw from official NetHack-3.6.7_Released source tag (255,736 / 8,115 / 17,317 bytes).
- **TILE FAQ resolution:** no document literally named "TILE FAQ" is hosted anywhere reachable today (nethack.org links page, NetHack wiki, source tree checked). Closest free standing primary: NetHack Wiki `Tiles` page (saved) + the Guidebook/dgn/lev docs. Recorded honestly, not faked.
- Rogue: `rogue.doc.in` (the original *Guide to the Dungeons of Doom* manual text) + `rogue.6.in` man page fetched from Rogue 5.4.x source mirror; classic hints card fetched from textfiles.com/rpg/rogue.txt.
- Colossal Cave: Dennis Jerz's open-access DHQ study of Crowther's original Adventure code fetched (418 KB, ~23k words).
- CRPG lineage: Matt Barton's three-part Gamasutra (now gamedeveloper.com) history — all three parts located, fetched, and title-verified (~18.8k words in Part 1 alone). Note: first-probed URL variants silently redirected to a generic listing page; caught via `<title>` check and re-fetched with correct slugs. **Trust bytes, not status codes.**
- Dwarf Fortress: GDC Vault slide PDFs for both Tarn Adams talks are paywalled (mediaProxy returns an HTML upsell) → recorded BLOCKED. Free primaries instead: GDC 2016 *Practices in Procedural Generation* Vault page (video free-to-view), GDC 2025 *What Even is 1.0?* free Vault page, and official bay12games **DF Talk #23/#24/#25 transcripts** (~12k words each) — the deepest free primary DF design text.
- Souls: two serious-source analyses fetched from Game Developer and title-verified. The strong academic pick (Andriano, *Games and Culture* 20(7), "Enjoying the Uncertainty…") is SAGE-gated (403) → BLOCKED.
- Slay the Spire: official GDC 2019 *Metrics Driven Design and Balance* slide deck fetched as free PDF (22 pp); Road-to-IGF interview (Game Developer) and Giovannetti interview (Justin Gary Substack, `isFree:true`) fetched.
- Manifest `manifest.jsonl` written: 25 rows, sha256 per file. 25/25 hashes verified over saved bytes.

## Findings

- The entire gaming-history weave (MUD→rogue→DF→Souls→StS) is now locally grounded in **primary or serious secondary text**: Bartle's own 1990 report and 1996 taxonomy paper, his full 2003 book, the original Rogue manual and NetHack compiler design docs, three official DF transcripts, and designer-voiced StS material.
- Corpus stats: 25 artifacts, **12,837,576 bytes (~12.2 MB)**, spanning era 1976→2025. 22 text-bearing artifacts saved as .txt/.html; 2 as PDF because the PDF *is* the primary artifact (DVW book, StS slides).
- Fetch-hardening notes for future lanes: (1) gamedeveloper.com returns HTTP 200 with a generic listing page for dead slugs — always verify `<title>`; (2) Wayback/CDX was fully offline tonight, so dead Gamasutra URLs had to be resolved via live-site slug discovery; (3) WebSearch rate-limits — mud.co.uk/bay12games/raw.githubusercontent probing was more reliable.

## Blocked / skipped (honest ledger)

| Item | Why |
|---|---|
| Tarn Adams GDC 2016 + GDC 2025 **slide decks** (gdcvault.com) | Slides paywalled; mediaProxy returns upsell HTML. Free Vault pages saved instead. |
| Andriano, "Enjoying the Uncertainty…" (*Games and Culture* 20(7), SAGE) | Publisher-gated (HTTP 403). Recorded as the Souls-family academic follow-up to buy/borrow, not fetched. |
| Barton Part 3 alternate slugs / older Gamasutra originals | Wayback offline tonight; live-site Part III (correct slug) fetched instead — nothing lost. |
| "Designing Virtual Worlds" excerpts | N/A — moot: full book is author-sanctioned free, so fetched whole. |

## Close-out

- **Fetched count + total size:** 25 artifacts · 12,837,576 bytes (~12.2 MB) in `memory/corpus/game_design_docs/`.
- **Manifest summary:** `manifest.jsonl` — 25 rows, fields `url, file, sha256, title, era, bytes`; sha256 computed over saved bytes at manifest time; rows cover Bartle ×4, NetHack ×4, Rogue ×3, adventure history ×1, CRPG history ×3, Dwarf Fortress ×5, Souls ×2, Slay the Spire ×3.
- **Canon linkage:** `watch/inbox/FROM_MUD_TO_WOW_20260914.md` referenced (not re-fetched); this corpus is its upstream source layer.
- **Top-3 documents that most change how the estate's games should be designed:**
  1. **`bartle_designing_virtual_worlds_2003.pdf`** — the whole discipline of virtual-world/player-category design from the source, and it is *legally free* (rights reverted). Estate seats/games should be designed around Bartle's player-type dynamics and "both world and game" frame, not around content volume.
  2. **`rogue_guide_dungeons_of_doom.txt` + NetHack `dgn_comp`/`lev_comp` docs** (roguelike set, counted as one move) — procedurally generated dungeons described as *compilable design language*. This is the direct blueprint for the estate's procedural veins: express the dungeon as data + grammar the janitors can generate, not as hand-placed content.
  3. **`df_talk23/24/25_transcript_bay12.html`** — Tarn Adams narrating his actual design decisions (failure as content, simulation-first, "losing is fun"). Validates the estate's local-janitor-first economy: the design the Adamses ran on one developer scales to the harness's tier ladder.
  *(Honorable mention: `sts_gdc2019_metrics_slides.pdf` — metrics-driven balance on a tiny team; the operational how-to complement to the DF philosophy.)*
