# Receipt: innkeeper mate, 20261012, cycle 5 of the seed thread (CLOSED)

Mission: logs\mates\missions\mission_20261012_04_innkeeper.md (claimed via .claim sidecar per pack header).
Mate: THE INNKEEPER. Persona honored: warm, plain-spoken, allergic to jargon; every cold surface should greet its stranger by name and tell them where the stairs are.
Seed thread: Adam's day one on the-mountain after commit 035a5e3, walked AS HIM, cold, no estate knowledge.
Resume chain: receipt_20261006_innkeeper.md (hash lives in the-mountain) -> receipt_20261009_innkeeper.md (estate README blind to the mountain) -> receipt_20261010_innkeeper.md (mountain cold walk CLOSED; porch 6 commits behind house) -> receipt_20261011_innkeeper.md (mag.cmd help-text walk CLOSED; 173-name wall) -> this receipt closes cycle 4's self-chosen thread: the HUMAN stranger's doors (HOW_TO_MAG_DASHBOARD.md vs the live :8765 landing page, OPERATOR_CARD.md's FIND / FILE / LOAD path, plus the standing porch re-check).
STEER honored: COMPUTE LADDER. Every step was a local file read, a local command, or a read-only GET against localhost:8765, plus one public ls-remote and one free-lane web search (the X handle check). Zero paid dispatch, zero API keys, zero Nous/Hermes.
Status: THREAD EXHAUSTED for this cycle, stopped at exhaustion, not mid-road. Next thread named at the bottom.

## FINDINGS

1. THE BIG ONE: the live page at http://127.0.0.1:8765/ is not the house the how-to describes. docs/HOW_TO_MAG_DASHBOARD.md promises a Home with 8 named pieces (Ship badge, Phoenix banner, stats row, latest bead, provenance paths, verify list, open loops, bonds, plus the FIND/FILE/LOAD path always visible). The served page is titled "FLEET CONSOLE - everything, one place": tabs ALL, VISUAL DECK, SURFACES, ORGANS, CARDS, CODE+DATA, FLEET, plus a filter box. Pieces found on the live page: 0 of the 8 checked. A stranger follows the welcome mat and lands in a rebuilt lobby with no bead, no ship, no open loops, and no FIND/FILE/LOAD anywhere on the page.
2. The described Home is not gone, it is in the museum basement: /static/museum/index_old_mag_board.html answers HTTP 200 and carries the Ship/Phoenix/beads UI (3 grep hits for Ship, Phoenix, Latest day, open loops). The how-to doc documents the museum page as if it were the front door.
3. The how-to doc is 69 days old (mtime 2026-08-04 11:46:59, 303 lines). The console absorbed Home 3 days ago: watch/inbox/ZOO_REORG_20261009.md, HALL OF SELF row, "home (ABSORBED by the console)". Nobody updated the doc at reorg time. The mat was not re-hung.
4. The landing page greets a stranger with "server UP" while its own health organ is broken. The page header fetches /api/health, which returns HTTP 500 with a real named error: "powershell.exe not resolvable: PATH carries no WindowsPowerShell directory and the System32 candidates are absent (B2-375)". The page's JavaScript (jget) never checks the HTTP status or the ok field, so the 500's JSON body still resolves and the header prints "server UP". A broken doorbell wired to always ring all-good: the one honesty signal the console carries is the one it cannot show.
5. The front door is Docker's, and the doc never says so. Port 8765 is held by com.docker.backend (PID 12044) forwarding to the mag-sovereign container (image mag-sovereign:local; 127.0.0.1 mappings 8765, 8000-8001, 9000). The doc says the dashboard "runs on your machine" (true) and gives a local venv start command, but the running thing is a container, and the words Docker, container, or mag-sovereign appear nowhere in the how-to.
6. dashboard.cmd's own health check is fooled by the same container. ensure_services.cmd checks http://127.0.0.1:8000/health and http://127.0.0.1:8765/ and both answer 200 from the container's port mappings, so the doc's section 4.1 start command prints "[ok] backend :8000 and dashboard :8765 up" whether or not any local python server ever started. The doc's second command (main.py dashboard --host 127.0.0.1 --port 8765) has real flags (verified via --help) but was NOT fired: it would bind or clash against a live service, and starting services is out of this walk's lane.
7. OPERATOR_CARD.md's FIND door is half dead. The card's three-doors table sends a layman to `mycelia.cmd x-pull` / `thread-pull`: mycelia.cmd exists nowhere (where.exe on PATH: 0 hits; glob of the repo: 0 files), and the card is the only repo file that names these tools. The other half of the FIND door is alive: the X handle @NachoQuixotic exists (x.com/NachoQuixotic, "Nacho Business", joined March 2022, confirmed by one free-lane web search).
8. Card doors that ARE alive, credited where the innkeeping is warm: mag.cmd doctor and mag.cmd context-pack (alive, cycle 4 walked them; context-pack remains the best-greeted surface in the estate), mag.cmd bonds (alive this cycle: JSON, ok=true, n_bonds 2, n_moves 6, n_conflicts 0, real file paths named), main.py trail (subcommand exists: start, append, status, close, check-seat, cores, pack, base, drifts, with --seat; verified by --help only, no trail fired), main.py agent (exists, --provider deepseek is the DEFAULT, which matches the how-to's "Grok not used" claim; not fired, it is a paid API lane). The card and the how-to agree with each other on FIND / FILE / LOAD plus optional STRIKE, which is good signage between the two docs.
9. Three names, one door: AGENTS.md calls :8765 "product UI (lab)", the how-to calls it "Mag Dashboard", the page calls itself "FLEET CONSOLE". main.py lab is the superset (dashboard plus watch/mag; --help confirms), main.py dashboard is the UI alone, and the container serves the console. A stranger cross-reading the docs gets three words for the same address.
10. The console's liveness badges are honest in intent, silent in fact: the page prefers /api/v1/surfaces/liveness, which answers 404 today, so every visitor silently gets the hardcoded evidence map dated 2026-09-22 baked into index.html. The code comments this fallback honestly; the visitor sees nothing.
11. The porch is STILL 6 commits behind the house, two days after cycle 3 measured it. House HEAD c38ded67acb24aaf564e40be1e188143e79d9814, GitHub main bac2b89cc43ae30956e7ee3e6049afab1a73f0ad, byte-identical to the 20261010 reading. Adam's day one still starts on the old porch, without ONBOARDING.md or ADAM_QUICKSTART.md.
12. The zoo reorg itself is good human innkeeping for strangers who already trust the house: 114 pages censused into 9 halls with a lose-nothing coverage gate that machine-enforces 114/114. But the reorg receipt's own totals say a stranger browsing SURFACES meets 16 LIVE, 86 DORMANT, 8 ABSORBED, 4 STUBS pages, and the console serves them flat in one grid until he discovers the filter box on his own. The welcome is real; it just does not introduce itself.

## JOURNEY (threads followed in order, dead ends named, why each turn)

1. Read the mission pack, then all four prior innkeeper receipts. RESUMED cycle 4's self-chosen thread (the human stranger's doors) per resume-not-respawn. Why: ride the thread across cycles, do not respawn it.
2. Filed the opening stub receipt before any probing. Why: receipt before speech is pack law and the operator ordered it before anything else.
3. Probed http://localhost:8765/ with a GET (200, 16,881 bytes). Why: the thread names the LIVE landing page; read-only GETs only per the thread's own rule.
4. Read docs/HOW_TO_MAG_DASHBOARD.md (303 lines) and docs/ref/OPERATOR_CARD.md (134 lines). Why: they are the two doors under test; a host reads the mat before judging the lobby.
5. Saved the landing page HTML and read all 287 lines. Why: byte truth over memory. Found the FLEET CONSOLE mismatch (finding 1) and, later on re-read, the jget no-status-check bug (finding 4).
6. Asked who owns port 8765 (Get-NetTCPConnection, then process and command line, then docker ps). Found com.docker.backend and the mag-sovereign container. Why: the doc claims a local python server; the actual listener had to be named, not assumed.
7. Read dashboard.cmd (4 lines) and ensure_services.cmd (44 lines). Why: the doc's section 4.1 start path had to be walked as written. Found the container-shadowed health check (finding 6). The doc's main.py dashboard flags verified via --help (they exist); the start itself NOT fired. Dead end by discipline: service starts are out of the walk's lane.
8. Hunted the doc's described Home in the static tree: rg for Ship/Phoenix landed on museum/index_old_mag_board.html; curl confirmed 200. Why: separate "the described house was demolished" from "the described house moved to the museum" before accusing.
9. Read ZOO_REORG_20261009.md. Why: it dates the console reorg and supplies the 16/86/8/4 census. This closed the "who moved Home" question with a receipt, not a guess.
10. Probed /api/health (HTTP 500, named B2-375 error) and /api/v1/surfaces/liveness (404). Why: the page calls both on every load; a host tests the doorbell and the sign himself.
11. Walked the OPERATOR_CARD command list as a cold seat: mycelia.cmd (DEAD END: 0 on PATH, 0 in repo, card is the only namer; finding 7), X handle @NachoQuixotic (alive, 1 free-lane web search), mag.cmd bonds (alive, fired once, read-only), main.py agent --help, trail --help, dashboard --help, lab --help (existence checks only; agent and trail not fired: one is a paid lane, the other writes estate state). Why: a command card's doors must each be existence-checked; only read-only doors get walked through.
12. Secondary thread: git rev-parse HEAD in the-mountain (c38ded6) and git ls-remote against GitHub main (bac2b89). Compared against receipt_20261010: unchanged. Why: cycles 3 and 4 left this check standing; two fresh bytes close it for this cycle.
13. Replaced the opening stub with this closing receipt in place. Why: one file per cycle per the contract; the stub's only job was to exist before speech.

Dead ends named: mycelia.cmd (does not exist anywhere); /api/v1/surfaces/liveness (404); the doc's local-server startup story (shadowed by the container, start not fired by lane discipline); the Godot half of the mountain (inherited unverified from cycle 3, not re-walked).

## COUNTS (real)

- GET probes against localhost:8765: 4 distinct doors (/, /api/health, /static/museum/index_old_mag_board.html, /api/v1/surfaces/liveness); statuses 200, 500, 200, 404
- landing page: 287 lines read, 16,881 bytes served (16,797 chars saved to temp)
- docs/HOW_TO_MAG_DASHBOARD.md: 303 lines, mtime 2026-08-04 11:46:59, 69 days old at walk time
- docs/ref/OPERATOR_CARD.md: 134 lines, mtime 2026-08-04 11:46:59, 69 days old
- doc's Home pieces checked on the live page: 8 named, 0 found; museum page grep hits for Ship/Phoenix/Latest day/open loops: 3
- port 8765 owner: com.docker.backend (PID 12044); container mag-sovereign (mag-sovereign:local) mapping 127.0.0.1 ports 8765, 8000-8001, 9000; docker ps rows: 7 containers, 1 holds the front door
- /api/health: 1 named error (powershell.exe not resolvable, ref B2-375); jget status-code checks in the page JS: 0
- mycelia.cmd: 0 hits on PATH (where.exe, 2 patterns), 0 files in repo (glob **/mycelia*); repo files naming x-pull/thread-pull: 1 (the card itself)
- X handle @NachoQuixotic: exists (1 free-lane web search; x.com/NachoQuixotic, joined March 2022)
- card commands existence-checked: 6 named doors (doctor, context-pack, bonds, trail, agent, mycelia.cmd); alive 5, dead 1; fired this cycle: bonds (1, read-only), plus --help reads: agent, trail, dashboard, lab (4)
- mag.cmd bonds output: ok=true, n_loops 0, n_bonds 2, n_moves 6, n_conflicts 0
- names for port 8765 across docs: 3 (lab in AGENTS.md, Mag Dashboard in the how-to, FLEET CONSOLE on the page)
- the-mountain: house HEAD c38ded6, GitHub main bac2b89, gap 6 commits, unchanged since receipt_20261010 (2 days)
- root-level .cmd launchers counted by this walk's dir listing: 40 (root glob denominator; cycle 4's RUN.md count of 33 used its own inventory rule, not conflated here)
- receipts read before acting: 4; receipt files written this cycle: 1 (this one, stub replaced in place)
- paid dispatches: 0; API keys touched: 0; web searches: 1 (free lane); environment variables dumped: 0
- em-dashes in this receipt: 0

## Next thread (self-chosen, for the next cycle)

The front door's real owner is undocumented for strangers: no cold-entry doc names Docker or mag-sovereign, yet the container now serves :8765 and :8000 and shadows the doc's own startup check. Next cycle's thread: walk every stranger-facing start story (HOW_TO_MAG_DASHBOARD.md section 4.1, AGENTS.md's lab line, docs/ref/RUN.md if it names the dashboard, README if it names either) against the container reality, and inventory exactly which cold-entry surfaces would have to change for the mat to match the door. Secondary, standing: if the operator pushes the 6 porch-behind commits, re-run ls-remote and record it. Duty-lane notes for the operator, not mate lanes: the /api/health 500 (B2-375) makes the console's only honesty signal lie by omission; the how-to doc and OPERATOR_CARD's FIND row both need a re-hang after the 10-09 reorg; the museum page should be labeled as such in the doc or the doc should describe the console.

Resume-not-respawn: stopped at thread exhaustion, not mid-road. Next cycle resumes by id (innkeeper) with this receipt as context.
