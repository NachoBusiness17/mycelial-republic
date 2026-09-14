# TRAINING INDEX — the ractor corpus as signal (2026-09-04)

What this is: the local, lawful, re-runnable ground-truth shelf for the nine ractor
chairs + the elder lens. Built by `mag/ractor_corpus.py` (idempotent — re-run converges;
header-verified curated IDs; manifest lists the SHELF, not the session).

## SIGNAL DENSITY (final, 2026-09-04 — adjacent sweep converged)

| Shelf | Texts | Bytes | Chairs fed | Note |
|---|---|---|---|---|
| esoterica | 50 | ~26 MB | ELDER LENS, JUNG adjacent | Blavatsky (Secret Doctrine, Isis Unveiled), Waite, Mead, Swedenborg, Boehme, Besant, Leadbeater, Vivekananda, Ouspensky, Neoplatonists |
| cs_classics | 47 | ~25 MB | THE STACK (CS as logos) | James, Hume, Kant, Bergson, Russell, Nietzsche, Boole, Butler, Descartes, Leibniz, Eddington |
| scifi_pd | 40 | ~19 MB | all (prophetic layer) | Wells, Shelley, Stoker, Lindsay, Abbott, Hodgson, Swift, Verne, Burroughs, Morris |
| plato | 25 | ~11 MB | PLATO_KIRK | the dialogues, Jowett (PD) |
| weird_prophetic | 54 | ~8 MB | prophetic corridor | MacDonald, Machen, Blackwood, Dunsany, Bulwer-Lytton, Chesterton (incl. French-language picks from gutendex) |
| crowd_media | 14 | ~6 MB | BERNAYS/ELLUL/FOUCAULT/MCLUHAN adjacent | Lippmann's Public Opinion, Le Bon (incl. French originals), Wallas, Trotter, Tarde |
| freud | 7 | ~5 MB | FREUD | intro lectures, dream psychology, Totem, sex theory |
| jung | 4 | ~4 MB | JUNG | lawful pre-1929 layer |
| steiner | 7 | ~3 MB | ELDER LENS | Occult Science, Philosophy of Spiritual Activity, Way of Initiation, Christianity as Mystical Fact + Kybalion |
| bernays | 2 | ~0.5 MB | BERNAYS | **Propaganda (1928)** + Crystallizing Public Opinion; Broadway Anthology culled (reject-gated in organ) |
| hall_mp | 1 | 0.08 MB | ELDER LENS | Initiates of the Flame (1922); Secret Teachings archive.org pull owed |
| mcluhan/foucault/baudrillard/stuart_hall/ellul | 0 | 0 | the 20th-century five | WALLED (copyright); lens carried by chair briefs; tri-stated per MANIFEST |
| **TOTAL** | **251** | **~119 MB** | | convergence reached (re-runs stable) |

## HOW TO TRAIN FROM IT (the routing)
1. **Per-chair bundle** = shelf texts + `docs/ref/ractors/<CHAIR>.md` (the lens) + the
   panel folds that cite the chair (`queue/handoff/ractors/`).
2. **Route to the swarm** for digestion: `swarm_surface.route_novel` (pattern proven in
   `mag/scifi_fantasy_steal.py`) — free lanes, tri-state read-backs, results land in
   `queue/handoff/ractors/`.
3. **Panel evidence rule**: from now on, a ractor brief that cites a shelf text cites the
   file path — bytes over gloss, the corpus makes tri-state enforceable against the minds
   themselves, not just summaries of them.

## THE ESOTERIC READING
`ESOTERIC_LENS_ON_THE_STACK.md` (same dir) — rib routing as Hermes/Thoth/Valkyrie work,
CS as logos/entropy/oracle/Gödel-cave, physical computing as incarnation + the familiar,
scifi as prophetic literature, one line per mind from their own shelf.

## OWED (the honest gaps)
- Secret Teachings of All Ages (Hall 1928, PD) — archive.org fulltext pull.
- Seven Sermones ad Mortuos (Jung 1916, PD seed for the shadow chair).
- The 20th-century five stay walled; if the operator licenses them ( archive.org lending
  or purchase), the shelves take them same day.
