# F2_GAME_CANON — game-design free canon, round 2 (receipt)

- **Date:** 2026-09-16
- **Lane:** F2 (game-design canon fetch, round 2)
- **Corpus root:** `memory/corpus/game_design_docs/` (append to existing `manifest.jsonl`, round 1 filed by N7)
- **Law:** receipt FIRST (this file) · append as you go · **no git** · **free+legal only** · nothing behind a paywall; blockers recorded honestly · trust bytes not reports (sha256 per file)

## Targets (assigned)

1. Chris Crawford, *The Art of Computer Game Design* (1984) — first game-design book ever, legally free (washington.edu class archive claim to verify)
2. Greg Costikyan, "I Have No Words & I Must Design" — free on costik.com
3. Costikyan, *Uncertainty in Games* — free excerpts/essay versions only
4. Raph Koster free essays — theory of fun chapters he's released, "A Grammar of Gameplay"
5. GDC Vault FREE list — game-design classics (Soren Johnson civ talks, Jon Blow 2005-06 talks if free)
6. Daniel Cook, Lost Garden essays — free, foundational

## Log (appended as work proceeds)

- [start] Receipt laid down before any fetch. Round-1 manifest read: 25 entries, schema = `{url, file, sha256, title, era, bytes}`.
- Crawford: `vancouver.wsu.edu/fac/peabody/game-book/` (the historic author-sanctioned 1997 web edition, cited as "washington.edu class archive") is DEAD — 301s to a generic WSU page. Pivoted to the full public Internet Archive scan `artofcomputergam00chri.pdf` (132 pp; p1/p5 text extracted and verified: "THE ART OF COMPUTER GAME DESIGN — Chris Crawford — Osborne/McGraw-Hill"). No paywall hit.
- Costikyan: `nowords.html` (1994) 404 on costik.com; `nowords2002.pdf` LIVE on costik.com (25 pp, PDF 1.6) and byte-size-identical copy open-access at dl.digra.org. Fetched author-hosted copy.
- Costikyan uncertainty: MIT Press *Uncertainty in Games* = PAYWALLED (mitpress.mit.edu 403; no legal free copy taken). Free stand-ins secured: `randomness-blight-or-bane.htm` (GDC Austin 2009 presentation text, author-hosted, 57KB real content) — the seed of the book. "Games are Uncertain.ppt" slides: dead 404 on costik.com despite being linked; Wayback returned no file → blocker recorded.
- Koster: `theoryoffun.com/theoryoffun.pdf` (51 pp text-only theory release, author-hosted) + `raphkoster.com/gaming/atof/grammarofgameplay.pdf` (A Grammar of Gameplay, GDC 2005) + Laws of Online World Design page. Grammar URL recovered from Koster's own "Recommended posts 1998-2012" index. Both PDFs content-verified via pypdf.
- GDC Vault FREE: scanned /free year listings 2005-2012. Soren Johnson's "Playing to Lose: AI and Civilization" NOT in the current free lists (checked 05/06/07/08/10/11/12) → blocker recorded. Jon Blow's 2005 design talks ARE free as the Experimental Gameplay Workshop 2005 series (Parts 1-4, /play/1019968-1019971, Blow listed as speaker) — all four Vault pages saved. Blow's solo "Designing to Reveal the Nature of the Universe" not in free lists.
- Lost Garden: "The Chemistry of Game Design" (skill atoms) live at gamedeveloper.com — saved, headline+skill-atom content verified. Old `loops-and-arcs.html` 404s on the migrated site; Wayback/CDX fetch attempted — Internet Archive temporarily OFFLINE during this pass → blocker recorded, not fetched. Added live classic "How to bootstrap your indie art needs" (2007) instead.
- [filed] 12 new files hashed (sha256), 12 manifest.jsonl lines appended (25 → 37). No git operations. All fetched content free/legal at time of fetch; every paywall/dead-link recorded above.

## Fetched table (round 2, all at `memory/corpus/game_design_docs/`)

| # | File | Source | Era | Bytes | Target |
|---|------|--------|-----|-------|--------|
| 1 | crawford_acgd_1984_scan_ia.pdf | archive.org (public full scan) | 1984 | 4,606,406 | Crawford, Art of Computer Game Design |
| 2 | costik_i_have_no_words_2002.pdf | costik.com/nowords2002.pdf | 1994/2002 | 694,141 | Costikyan, I Have No Words & I Must Design |
| 3 | costik_randomness_blight_or_bane_essay.html | costik.com | 2009 | 57,419 | Costikyan Uncertainty (free precursor essay) |
| 4 | koster_theoryoffun_pdf.pdf | theoryoffun.com | 2004 | 4,974,833 | Koster, Theory of Fun (text release) |
| 5 | koster_grammar_of_gameplay_2005.pdf | raphkoster.com | 2005 | 16,225,358 | Koster, A Grammar of Gameplay |
| 6 | koster_laws_of_online_world_design.html | raphkoster.com | 1990s/2000s | 377,300 | Koster free essays |
| 7-10 | blow_egp2005_part1..4_vaultpage.html | gdcvault.com (FREE) | 2005 | 111,115 ea | Blow / Experimental Gameplay Workshop 2005 |
| 11 | lostgarden_chemistry_of_game_design_2007.html | gamedeveloper.com | 2007 | 605,611 | Daniel Cook, Lost Garden |
| 12 | lostgarden_bootstrap_indie_art_2007.html | lostgarden.com | 2007 | 273,427 | Daniel Cook, Lost Garden |

*authoritative bytes are in manifest.jsonl (source of truth); table sizes rounded from disk.

## Blockers (honest)

- MIT Press *Uncertainty in Games* book — paywalled; not fetched. Free precursor essay + 2002 paper cover the argument.
- costik.com "Games are Uncertain.ppt" — dead (404), no Wayback copy returned.
- Crawford 1997 WSU/Vancouver web edition — dead (301 to generic page).
- Costikyan 1994 nowords.html — 404 (2002 revised PDF supersedes).
- Soren Johnson "Playing to Lose: AI and Civilization" — not in GDC Vault FREE lists today.
- Blow "Designing to Reveal the Nature of the Universe" — not in GDC Vault FREE lists today (EGP 2005 workshop sessions are).
- Lost Garden "Loops and Arcs" — 404 on migrated site; Wayback temporarily offline during pass → not fetched.
- Web search rate-limited mid-pass; URL discovery done by direct probing + site-own indexes instead.

## Single most design-changing free document this pass

**Costikyan, "I Have No Words & I Must Design" (2002 author-hosted PDF, `costik_i_have_no_words_2002.pdf`).** It converts "gameplay" from mystique into a checklist of mechanics — goals, opposition, uncertainty, resources, game-state information, decision-management — and its uncertainty thesis is the direct seed of *Uncertainty in Games*. For a corpus already built on Rogue/NetHack/DF/StS procedural design, that vocabulary (especially the primacy of uncertainty) is the highest-leverage canon item fetched this pass. Runner-up: Crawford's ACGD scan (the 1984 foundation the whole field argues with).
