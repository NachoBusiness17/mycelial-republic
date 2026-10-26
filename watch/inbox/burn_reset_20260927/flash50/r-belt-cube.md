# r-belt-cube - Deep-dive: real (non-CGI) builds of a belt-driven forever-rotating cube

Date: 2026-09-28. Item: "Deep-dive: real (non-CGI) builds of a belt-driven forever-rotating cube. Kinetic sculpture, Zipper-ride carriage mechanics, escalator corner chains, planetary corner gears, patents. OWED if unverifiable."

## 0. Verdict up front

**No verified real (non-CGI) build of a belt-driven forever-rotating cube was found on any surface reachable this session.** The forever-rotating cube lives, as far as I could reach, in the CGI looping-render genre (Wannerstedt-style perpetual machines). Every real artifact adjacent to it solves cube rotation a different way: reaction wheels (Cubli), internal flywheels (M-Blocks), hand-spun nested cubes (Turner's cube), motorized display bases (LED cube on a lazy susan), or gear-integrated cube bodies (Gear Cube puzzle). The three mechanism families the ask names (Zipper carriages, escalator corner chains, planetary corner gears) all exist and are verified below, but as analogs, not as prior cube builds.

Absence is scoped honestly: this is absence on the indexes I could reach on 2026-09-28 (see section 5 for what was walled off). It is not a claim that no build exists anywhere on Earth.

## 1. Method and receipts (what I actually ran)

Ran 2026-09-28, session "gopher-r-belt-cube", harness WebSearch + WebFetch tools.

Direct fetches that returned content:

| # | URL | What it gave |
|---|-----|--------------|
| F1 | `https://hackaday.com/?s=tumbling+cube` | 7 posts, all CubeSat/rocket noise; one tangential real build: LED cube on a motorized lazy susan (2019-11-04, "Ambitious LED Cube Provides Endless Video Game Scrolling") |
| F2 | `https://en.wikipedia.org/wiki/Zipper_(ride)` | Zipper mechanics + patent 3,596,905 (quoted in section 3) |
| F3 | `https://en.wikipedia.org/wiki/Escalator` | Corner-chain/track mechanics + full patent lineage (quoted in section 4) |
| F4 | `https://patents.google.com/patent/US3596905A/en` | Zipper patent full text quotes (section 3) |
| F5 | `https://en.wikipedia.org/wiki/Square_wheel` | Stan Wagon catenary tricycle 1997, Winckler 2006, MythBusters 2012 |

Fetches that failed (recorded because the negative space is part of the finding):

- `https://en.wikipedia.org/wiki/Cubli` - HTTP 404 (no such article; Cubli facts below come from a search-surfaced copy of the IROS 2012 paper)
- `https://en.wikipedia.org/wiki/Gear_cube` - HTTP 404
- `https://patents.justia.com/search?q=%22rotating+cube%22+belt` - HTTP 403
- `https://html.duckduckgo.com/html/?q=...` (2 queries) - bot-detection CAPTCHA, no results
- `https://www.mojeek.com/search?q=...` - JavaScript CAPTCHA, no results
- YouTube results page via web reader - backend network error (-500), no results
- `https://www.instructables.com/howto/kinetic+sculpture/` - HTTP 404
- One WebSearch call timed out at the tool level (60 s); several WebSearch sub-calls returned backend 429/1302 rate-limit errors (parallel search storms; sequential batches worked)

Search queries that returned link-backed results are named inline below. Queries that returned ZERO link-backed hits for the core question: "tumbling cube" machine reddit belt build; "forever rotating cube" belt machine build; "rolling cube" machine belt conveyor treadmill build video; "rotating cube" display apparatus drive mechanism patent (exact phrase); "tumbling cube" kinetic sculpture physical build motor; ball-rolls-forever-on-treadmill variants (x3). Eight-plus phrasings of "a real machine that tumbles a cube forever with belts" surfaced no build.

## 2. The CGI side (the genre the ask is contrasting against)

- Andreas Wannerstedt, Swedish 3D artist (Stockholm), documented maker of looping "oddly satisfying" perpetual machines where "gravity does not exist" and objects (including cubes) "move in endless loops" - Clot Magazine interview, 2021-02-02 (surfaced via WebSearch, clotmag.com). His genre is exactly the referent class: physically plausible-looking machines that could not run as shown.
- I could NOT pin the specific viral "belt-driven forever-rotating cube" render to a named artist or piece. Marked OWED in section 6. The general finding stands: the genre is documented; the specific viral artifact is not identified in anything I reached.

## 3. Real cube-rotation machines that DO exist (all non-CGI, none belt-driven)

1. **The Cubli (ETH Zurich, 2012).** "The Cubli: A Cube that can Jump Up and Balance" - Mohanarajah Gajamohan, Michael Merz, Igor Thommen, Raffaello D'Andrea, IROS 2012 (pp. 3722-3727); follow-up "The Cubli: A Reaction Wheel Based 3D Inverted Pendulum", ECC 2013. 15 cm cube; three orthogonal internal reaction wheels spun up and braked to jump onto an edge/corner, then hold a 3D inverted-pendulum balance, and "walk". Actuation is momentum exchange, NOT belts or ground contact. Receipt: search surfaced a copy of the IROS paper (Scribd) with title/author page; Wikipedia article does not exist (404 above).
2. **M-Blocks (MIT CSAIL, Oct 2013).** John Romanishin with Daniela Rus and John Wojtasicky; ~50 mm self-reconfiguring cubes with an internal flywheel spinning up to 20,000 rpm; braking the flywheel makes the cube jump/tumble/roll; magnets on faces and edges couple modules. Again momentum exchange, not belts. Receipt: WebSearch results (parts-people.com writeup quoting the 20,000 rpm figure; Ars Technica and ZDNet coverage dated 2013-10-07).
3. **Turner's cube (1970s).** Machined nested-cubes sculpture, ~8.9 in, rotated on a stand (hand-spun). Receipt: WebSearch hit (gadgetify.com, "1970s Spinning Turner's Cube Kinetic Sculpture"). Closest classic "rotating cube sculpture", zero drive train.
4. **Motorized LED cube on a lazy susan (Hackaday, 2019-11-04).** A real, motorized rotating cube display (LED cube + emulator), but rotation is a display base, not a belt tumbling the cube. Receipt: F1.
5. **Gear Cube puzzle (2009).** Oskar van Deventer with Meffert's Puzzles: a twisty cube with visible interlocking gears integrated into the cube body; corners carry gear teeth; mass-produced (Meffert's), Maltese Gear Cube variant 2013. This is the closest REAL artifact for "corner gears integrated in a cube". Receipt: WebSearch hit, Twisty Puzzles Wiki (twistypuzzles2.fandom.com). Wikipedia article 404s.
6. **Rolling square vehicles (real rolling-square machines).** Stan Wagon (Macalester College) built the first catenary-square-wheel tricycle prototype in 1997 (rebuilt April 2004): "A square wheel can roll smoothly if the ground consists of evenly shaped inverted catenaries of the right size and curvature." Jason Winckler (Global Composites, 2006) built linked square wheels offset 22.5 degrees that roll on FLAT ground. MythBusters (2012) rode a square-tire truck. Receipt: F5, Wikipedia "Square wheel". These prove the rolling-polygon-in-a-shaped-path principle with real builds.
7. **Jacob's ladder toy (documented 1889).** The original real "forever-tumbling blocks" mechanism: ribbon-hinged blocks where the cascade illusion is driven by one block repeatedly flipping in place. 1889 Scientific American: "the second block in reality only falls back into its original position". Origins unknown; many US patent variants (one 1940s penny-holding version). Receipt: fetched `https://en.wikipedia.org/wiki/Jacob%27s_ladder_(toy)`. This is the mechanical grandparent of every "forever" tumbling illusion.
8. **Tri-vision / Prismavision billboards (real, commercial, motorized forever-flipping panels).** Vertical triangular prisms mounted on a frame rotate in unison by 120 degrees, driven by a central motor through a gear/shaft system (trade specs describe a "double-gear steps driving system"); dwell-then-flip cycling, ~6-15 s transitions; municipal sign codes literally name "tri-vision or multi-prism sign faces" as a regulated class. Receipt: WebSearch hits (bmediagroup.com Prismavision technology pages, 2020-04-05; made-in-China spec listings). Closest industrial cousin of a forever-cycling rigid-body display face.

Note on "perpetual": every real artifact above is motorized or hand-powered. Nothing found runs unpowered forever; the desk-toy "perpetual motion" market (Amazon/AliExpress/Walmart listings surfaced in search) is all hidden-drive.

## 4. The three mechanism families the ask names

### 4a. Zipper-ride carriage mechanics - VERIFIED, with the patent

Wikipedia (F2): designed by Joseph Brown under Chance Rides, Wichita, 1968; 222 units built 1968-2001; an oblong rotating boom with a cable pulling 12 cars around its perimeter; boom rotates 7.5 rpm while "the passenger capsules travel around the perimeter of the boom at 4 revolutions per minute (rpm), allowing the compartments to flip at each end of the boom"; the first fourteen Zippers ran faster (boom 11 rpm, cable 7 rpm) and speeds "were permanently lowered after injuries". Patent: US 3,596,905 (1971).

The patent itself (F4): **US3596905A, "Plural horizontal axis roundabout having sheave driven carriage," inventor Joseph M. Brown, assignee Chance Manufacturing Co., Inc., filed 1969-05-02, issued 1971-08-03.** Mechanism quotes: "Connected to the boom 22 by transverse brace members 24 are a pair of spaced channel members 28... which define guide tracks for roller carriages 30"; carriages carry "a pair of freely rotatable passenger cages 36, 38"; drive is "a positively driven propeller shaft 47 operates the transmission gearing to rotate the two sets of sheaves 44, 44 and drive endless flexible cables 43, 49"; and the orientation trick: "The pivot points 42 of the individual cages are selected so that gravity causes the cages to remain more or less in their proper orientation", with cages swinging "freely about the pivot points 42 to increase the excitement of the ride".

What transfers to a cube build: the Zipper solves "carriage rides a closed path around a rotating body while the body itself rotates" with (1) a positive cable/sheave drive along a shaped closed path and (2) passive gravity pivots for carriage orientation. Its own words say "more or less" - passive pivots tolerate slop a carnival rider enjoys and a display cube cannot. A belt-driven forever-cube carrying its own corners would need actively phase-locked carriages, not gravity pivots.

### 4b. Escalator corner chains - VERIFIED, with the patent lineage

Wikipedia (F3): steps ride "on a pair of tracks which keep the step tread horizontal"; each step has four wheels on two axles; the front wheels run in the "step-wheel track", the rear in the "trailer-wheel track". On the incline the two tracks hold the step geometry so the back of one step stands 90 degrees to the next. At the landing, "the two tracks converge so that the front and back wheels of the steps are almost in a straight line", flattening the steps into a sheet so they can round the corner; the chain "continuously pulls the steps from the bottom platform and back to the top in an endless loop".

This is the exact mechanical answer to "how does a rigid body's support points traverse a curve while the body's orientation stays controlled": SEPARATE GUIDE TRACKS PER WHEEL PAIR, converging through the corner.

Patent lineage (all from F3, with numbers): Nathan Ames, US 25,076, "Revolving Stairs", 1859-08-09 (never built); Leamon Souder, US 406,314 "Stairway" (1889) plus 723,325 and 792,623 (spiral designs); Jesse W. Reno, US 470,918, "Endless Conveyor or Elevator", patented 1892-03-15, working ride at Coney Island 1896; George A. Wheeler, US 479,864, "Elevator", 1892-08-02 (never built, patents bought by Seeberger); Charles Seeberger trademarked "escalator" 1900 (US TM 34724), built first commercial unit with Otis 1899; later: Spriggs/Evans handrail drive US 5,427,221 (1995); Karl-Heinz Pahl spiral escalators EP0415953 / US 5,158,167 (1992).

What transfers to a cube build: for each cube face pair, run two belt lanes (or two tracks) that converge near the loop corners, so the carriage set crosses the corner with the cube's face flat instead of pivoting freely. The escalator is 130 years of field-proven corner-traversal for belt-carried rigid bodies.

### 4c. Planetary corner gears - NO direct prior art found

I searched for built instances of gear-on-corner schemes for rotating cubes and found none. What the search DID verify as closest real artifacts: (1) the Gear Cube (van Deventer/Meffert's 2009, gears integrated in the cube body, section 3 item 5); (2) tri-vision billboard gear/shaft drives rotating all prism faces in sync (section 3 item 8); (3) general planetary gearsets, but no built "corner carriages as planets riding a belt ring" instance surfaced on any reachable index. Marked OWED-scoped in section 6: absence on reachable indexes, not proof of nonexistence. The kinematic idea itself (corner carriages as planets, cube center as sun, belt path as ring) is coherent and would give constant corner-path speed without free-fall gaps, but I found nobody who built it.

### 4d. Patents

Verified directly by fetch: **US3596905A** (Zipper, section 4a). Verified via Wikipedia citations: the escalator lineage in section 4b (Ames 25,076 through Pahl EP0415953).

Searched for, NOT found: any patent for a belt-driven forever-rotating cube, tumbling-cube machine, or rotating-cube display with a belt/corner-carriage drive. Exact-phrase patent queries returned only tangential link-backed hits: US20140213140A1 ("Tangible user interface", Cube World-style LCD cubes); US7703924B2 (rotating swept-screen volumetric display); KR101487904B1 (flip-dot display element). No Google Patents full-index text search was available to me (the patents.google.com search UI needs JavaScript; Justia returned 403; see section 5), so patent absence is scoped to what the general web index surfaced.

## 5. Blocked surfaces (limits of this dive)

- Google Patents full-text search: JS-only UI, unreachable from this fetch path (individual patent pages fetch fine; search does not).
- Justia patent search: 403.
- DuckDuckGo HTML and Mojeek: CAPTCHA walls.
- YouTube search: web-reader backend error; could not enumerate video results directly, which is the most likely home for a real build if one exists. This is the single biggest OWED gap.
- Reddit: not directly reachable this session (search-engine hits only, and the relevant queries 429'd).
- The WebSearch backend itself threw repeated 429/1302 rate-limit errors under parallel calls; sequential batches recovered it. Two queries may have been under-served because of this.

## 6. OWED ledger (explicitly unverifiable from this session)

1. **OWED: the specific viral "forever-rotating cube" render** - could not be attributed to a named artist or video. The CGI looping-machine genre is documented (Wannerstedt), the artifact is not.
2. **OWED: any real belt-driven forever-rotating cube build** - eight-plus query phrasings, zero link-backed hits. If one exists, it is below the search-index floor (YouTube unindexed text, TikTok, private shop pages, or untranslated non-English web).
3. **OWED: ball-on-two-counter-rotating-treadmill-belts** - the alleged real sibling of the concept; my three queries on it timed out or returned no link-backed hit, so I neither confirm nor deny it. Do not cite this file for it.
4. **OWED: exhaustive patent-class search** - restricted to general-index surfacing; Google Patents full search and Justia were unreachable.
5. **Single-source, unopened:** a TikTok/ArtConnect item crediting @jonnyhawaiii with an "18th International" work combining "a treadmill, a fan, and a tumbleweed" as perpetual-motion-themed art. Mentioned for completeness, not verified by opening it.
6. Turner's Cube (1970s), tri-vision gear-drive details, and Gear Cube history rest on single search-surfaced pages each (gadgetify.com, bmediagroup.com, twistypuzzles2.fandom.com); consistent across the snippets I saw, but I did not open second sources for each.

## 7. Engineering read (my analysis, grounded in the verified mechanisms)

A belt-driven forever-rotating cube is buildable in principle; "forever" just means "as long as the motor runs" (every real analog in section 3 confirms energy comes from a drive; none is perpetual). The four hard problems, each with a verified real solution in an adjacent machine:

1. **Corner traversal with orientation control** - escalator two-track convergence (section 4b) is the 130-year-old proven answer: give each support point its own guide path and converge the paths through corners.
2. **Positive drive around a shaped closed path** - Zipper sheave-and-cable drive (section 4a): "positively driven propeller shaft... endless flexible cables" timed to the body's rotation. Belts instead of cables, four lanes instead of two.
3. **Carriage orientation through the flip** - Zipper shows passive gravity pivots give only "more or less" orientation; a display-grade cube needs active control, which is what the Cubli and M-Blocks bring to cube attitude, just from inside the body rather than from carriages.
4. **Phase-locking eight corners 90 degrees apart** - tri-vision billboards phase-lock dozens of prism faces through one gear/shaft drive (section 3 item 8); the same single-positive-drive discipline, applied to corner carriages, is the closest verified precedent.

Nothing I found combines these four into one machine. That combination is the gap the deep-dive was hunting, and as of 2026-09-28, on everything I could reach, it is still open.

## 8. Source list

Fetched: hackaday.com/?s=tumbling+cube - en.wikipedia.org/wiki/Zipper_(ride) - en.wikipedia.org/wiki/Escalator - patents.google.com/patent/US3596905A/en - en.wikipedia.org/wiki/Square_wheel - en.wikipedia.org/wiki/Jacob%27s_ladder_(toy).

Search-surfaced (link-backed): clotmag.com (Wannerstedt interview, 2021-02-02) - Scribd copy of Gajamohan et al., IROS 2012 Cubli paper - parts-people.com M-Blocks writeup (20,000 rpm) - gadgetify.com Turner's Cube - twistypuzzles2.fandom.com Gear Cube (van Deventer/Meffert's 2009) - bmediagroup.com Prismavision pages - made-in-China tri-vision specs - patents.google.com/patent/US20140213140A1/en - patents.google.com/patent/US7703924B2/en - patents.google.com/patent/KR101487904B1/en - thekidshouldseethis.com (Tom Harold rolling ball sculptures; LEGO kinetic sculptures) - stephenjendro.com - woodthatworks.com (David C. Roy kinetic wall sculptures, weight-driven).

Walled off (attempted, no data): html.duckduckgo.com x2 - mojeek.com - patents.justia.com - youtube.com results via web reader - en.wikipedia.org/wiki/Cubli (404) - en.wikipedia.org/wiki/Gear_cube (404) - instructables.com howto search (404).
