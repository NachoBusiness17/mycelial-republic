"""zoo_render.py - render THE ZOO (dashboard/static/zoo.html) from the census + ancestry map.

The HALLS table below is the seat's ancestry: for every page in dashboard/static
root, it names the hall, the one law the page steps in, its status
(LIVE = data-doored/automated, DORMANT = self-contained, unwired-not-dead,
ABSORBED = the idea now lives in a repo organ, STUB = redirect only), and a
run-with note (what to take and run with creatively).

Coverage gate: the build FAILS if any census page is unassigned or assigned
twice (lose nothing, enforced by the tool, not by hope).

Usage:
  .venv/Scripts/python.exe tools/zoo_census.py
  .venv/Scripts/python.exe tools/zoo_render.py
"""
from __future__ import annotations

import html
import json
import sys
from pathlib import Path

ROOT = Path("dashboard/static")

HALLS: list[dict] = [
    {
        "id": "laws",
        "name": "HALL OF LAWS",
        "blurb": "a law rendered as a place you can walk. the physics is the lesson; the room is the proof.",
        "pages": {
            "airflow_home": ("the house is the prompt: smoke obeys doors, not fans. force is the invoice, geometry is the pump", "DORMANT", "lesson mode: fan on/off side by side, labeled FORCE and GEOMETRY; the standing-gradient organ"),
            "chaos_refract": ("emergent, unexplained, and honest about it", "DORMANT", "anomaly-flagger face: surface unexplained deltas next to explained ones"),
            "doorbench": ("cache-invalidation falsifier, measured live: no prediction, no verdict", "DORMANT", "the same predict-then-measure gate for every benchmark claim we file"),
            "emergence_test_visualization": ("fixed wiring vs trainable heads: emergence as a visible differential", "DORMANT", "rerun on the current fleet: does the fixed-wiring law still hold"),
            "eraser_maze": ("seeing collapses the light: observation is never free", "DORMANT", "pair with the containment story: the watcher changes the watched (purge week, 10-08)"),
            "light_maze": ("light travels straight; walls end it; what you see is what you know", "DORMANT", "the light-maze-walkers founding frame; sherpa organ = the wall that shows the way"),
            "phase_particles": ("nothing here is labeled by the slider: the phase is MEASURED", "DORMANT", "the estate's sensor-over-slider law, rendered; wire to a live measured medium"),
            "rib_toy": ("a shadertoy for steering packets", "DORMANT", "render a real memlance firing as a steering packet"),
            "smith_chart": ("the fold law: half-plane to one disk, match any load without touching it", "DORMANT", "claritas as matching network: log mismatch before/after on premium asks"),
            "spectral_maze": ("three bands, one flood", "DORMANT", "multi-band sensing for the patrol: same room, three instruments"),
            "steer_field": ("the film: steering as a field you ride", "DORMANT", "retitle as the retrocausal-steering skill's demo reel"),
            "wave": ("the standing wave: the pattern persists, the medium does not accumulate", "DORMANT", "the tokens-as-disk governor; steal the wave visual for the budget page"),
        },
    },
    {
        "id": "forms",
        "name": "FORMS GALLERY",
        "blurb": "exhibits: beauty with provenance tri-state. every technique credited, nothing borrowed silently.",
        "pages": {
            "bad_apple_field": ("the room that remembers plays the video", "DORMANT", "memory-as-room: feed it one real session trail instead of bad apple"),
            "calabi_yau": ("shadow-fields, technique hand-carried, credit required on any surface", "DORMANT", "the provenance law's exhibit A"),
            "erosion_field": ("GPU erosion, provenance credited (runevision)", "DORMANT", "terrain = receipts eroding into settled law"),
            "field_quills": ("2000 instanced quills riding one vector field", "DORMANT", "render the pheromone bus as quills: heat = density"),
            "room_lightmap": ("the room of 2026-09-02 rendered as the problem it is", "DORMANT", "re-render today's room: the day the lightmap remembers"),
            "the_rings": ("one per day since 2026-08-25; tomorrow there is one more", "LIVE", "the heartbeat art: keep it running, it is the oldest daily organ"),
            "universe_within": ("the network, with music, in a dark room", "DORMANT", "the mesh as organism: soundtrack from suno/"),
            "viz_horse_run": ("spore form, the horse (reinterpreted)", "DORMANT", "spore-sharing canon rendered"),
            "viz_spore_fish": ("spore form, the fish (attempt 1)", "DORMANT", "attempt 1 of the same hunt; pair with the horse"),
        },
    },
    {
        "id": "ladder",
        "name": "THE LADDER",
        "blurb": "the classics ladder and its rungs: pong to breakout to invaders to snake to our rooms to shot-by-shot cinema. skills taught by game.",
        "pages": {
            "dungeon": ("the dungeon IS the test suite: invariants as lighting", "DORMANT", "gauntlet culture rendered; light = tests passing, dark = untested"),
            "game": ("the necromancer's swarm: k3s, dragons, and invariants", "DORMANT", "infra as boss fight; the k8s-water wave already speaks this language"),
            "grab_write": ("the tesuji: grab and write", "DORMANT", "go mechanics as the write-discipline lesson"),
            "incident_dungeon": ("the maze-arena incident, walkable; the exit is THE RUN", "DORMANT", "incidents as explorable space: build the 10-08 disk-crisis room"),
            "mag_dance": ("the estate soundtrack teaches a skeleton to dance", "DORMANT", "beat-selector organ; suno/ tracks are the score"),
            "maze": ("the maze entrance: six Socratic gates that make you derive the constitution yourself; the dialectic with the knife held by the handle", "LIVE", "the vin-dit machine: the induction organ; fired on the operator 10-09 (clearing reached, name taken, stone door open)"),
            "pipeline": ("the shader cartridges: BPM, energy, day", "DORMANT", "cartridge format for every visual room; one loader, many rooms"),
            "pong": ("rung 1: the story starts at the end. value flows backward from the final score", "DORMANT", "VONNEGUT REPLAY: slow-mo tension frames, ghost the miss, draw the value arrow; seal as primer room 0, ship in the installer"),
            "shadow_walk": ("voxel roguelite, vision-gated, JIT: the volume as a place you can stand in", "DORMANT", "epistemic fog as mechanic; the run is the lesson"),
            "shadowbonk": ("tony mczoom vs the shadow volume", "DORMANT", "geometry as opponent"),
            "spend": ("one wall: spend as arcade", "DORMANT", "wire to memory/runs/hermes_burn/usage.jsonl and the wall pays for itself"),
            "swarm": ("privlidge: a disco science skate (receipts in art/)", "DORMANT", "swarm-search skill's dream face"),
            "tavern_brawl": ("the kabuki tavern: click a ractor to provoke; real hitboxes, real lines", "DORMANT", "ractor brawl night; the dialectic workshop"),
            "tavern_test": ("tavern cartridge test", "DORMANT", "honest test page, keep as the cartridge format's proof"),
            "tesuji_map": ("GLM-5.3-flash behavior surface", "DORMANT", "feed the quant A/B spec (four pinned choices)"),
            "wipeout_lightmaze": ("wipeout: the song is the level", "DORMANT", "music-as-level, rung 3 of the same ladder"),
            "wipeout_sunset": ("wipeout v3: the music moves the mountains", "DORMANT", "music-as-terrain"),
            "wipeout_v2": ("wipeout v2: the song sets the speed", "DORMANT", "music-as-clock"),
            "worldline_dungeon": ("a telling rendered from the board", "DORMANT", "the worldline as dungeon: regenerate from today's trail.jsonl"),
        },
    },
    {
        "id": "primers",
        "name": "PRIMER HALL",
        "blurb": "teaching machines: predict before you measure, restate in one sentence, the record keeps. a seed, not a feed.",
        "pages": {
            "conservation_room": ("the sowing room: a fable of the conservation clause", "DORMANT", "the constitution as bedtime story"),
            "fable_room": ("room #0: the union of story and record", "DORMANT", "the trails/ledger union; room 0 of the primer in the other sense"),
            "falsifiers": ("paste-checkable invariants index: a falsifier is a pure function of pasted state", "ABSORBED", "the idea lives in githooks/pre-push (citation_lint, ratchet); page stays as the browser face; port the twins"),
            "hardware_primer": ("room 1, the darlington pair: whisper to shout, every hand takes its toll of 0.7 volts; predict, measure, restate, seal", "DORMANT", "room 2 = THE TOLL (the descent protocol as a dungeon room); the installer's teaching seed"),
            "hum": ("organ board: the estate's organs as instruments", "DORMANT", "estate_smith face: one row per organ, alive or dark"),
            "keeper_voice": ("the keeper's voice", "DORMANT", "herald organ; give it today's attention.md to read aloud"),
            "museum": ("the museum (previous map attempt)", "ABSORBED", "superseded as map by zoo.html; kept as exhibit of the map's own ancestry"),
        },
    },
    {
        "id": "verkle",
        "name": "VERKLE HALL",
        "blurb": "the chain as a place: genesis canvas, genome as body, pyramid as zone. browser falsifiers with python twins.",
        "pages": {
            "chain_check": ("verkle knot link verifier v1: salon_launch_law falsifier #2, python twin mag/verkle_knot.py", "ABSORBED", "the twin lives in tag-digest pinning (port wave P3); page remains the paste-door"),
            "chain_witness": ("THRESHOLD: the cold-start witness door", "DORMANT", "the GSTD node's witness face: cold start witnessed on-chain"),
            "claim_check": ("launch-law card verifier v1: falsifier #5 (claim semantics); python twin: none yet, this IS the reference impl", "DORMANT", "port the twin: the page is a reference implementation waiting for its python"),
            "lattice": ("conspiracy lattice: adjacency of ideas", "DORMANT", "corr_id joins over estate_query: the same graph, data-backed"),
            "lattice_check": ("legendre three-square invariant, twin mag/lattice_distance.py", "ABSORBED", "tests/ carry the twin; page is the paste-door"),
            "verkle_construction": ("the birth canvas: the chain through its construction", "DORMANT", "genesis animation for the republic branch"),
            "verkle_knot_wave": ("the verkle knot: the republic's genome, as a body", "DORMANT", "the RIB genome rendered"),
            "verkle_pyramid": ("the chain as a place (zone two): the laser walks the levels", "DORMANT", "zone two of the chain-as-space map"),
            "viz_3d_verkle": ("verkle chain in 3D", "DORMANT", "fold into the pyramid as its base level"),
            "viz_lattice_test": ("the constitution as a lattice", "DORMANT", "constitution.md rendered walkable"),
        },
    },
    {
        "id": "self",
        "name": "HALL OF SELF",
        "blurb": "the estate looking at itself: maps of modules, models, memory, manuals. the seat's own ancestry, browsable.",
        "pages": {
            "agents": ("sub-agent fleet board", "DORMANT", "supersede with hypervisor data"),
            "aos": ("AOS bones, live", "DORMANT", "agent-OS bones check; wire to lane health"),
            "deck": ("command deck", "LIVE", "the working surface; keep on the console"),
            "decks": ("decks index: the pro surface", "LIVE", "the decks/ wing's door"),
            "estate_walk": ("the estate as a walkable place (2.5MB self-contained)", "DORMANT", "regenerate monthly via _build_estate_walk.py; it IS the disk smith's art wing"),
            "fleet_symbols": ("the operator algebra: primitive glyph library", "LIVE", "the icon language of the whole zoo; reuse everywhere"),
            "home": ("the six destinations (previous front door)", "ABSORBED", "superseded by the console index; kept as ancestry"),
            "index": ("FLEET CONSOLE: everything, one place (the console itself)", "LIVE", "the flat surface; zoo.html is its map layer"),
            "kv_os": ("KV OS kernel status", "DORMANT", "wire to a real kv surface or fold into health"),
            "labs_map": ("competitor map: who we're racing (mapbox, paid seat)", "DORMANT", "refresh or retire under no-sacred-cows; racing map wants today's competitors"),
            "memory_map": ("categorized relational graph of the republic", "DORMANT", "feed from memory/ + corpus_fts; it wants to be the KG face"),
            "mesh_gallery": ("dungeon mesh content pipeline v1, client-side animation", "DORMANT", "content pipeline for every 3D room"),
            "model_map": ("the model shelf: every brain on this disk", "DORMANT", "wire to ollama list + HF census; the disk smith knows the shelf"),
            "module_map": ("every mag module surfaced with its real purpose", "ABSORBED", "the census patrol and rg -c carry it now; page stays as the human face"),
            "ontology_dashboard": ("ontology compiler phase 1", "DORMANT", "no sacred cows: phase 1 never became 2; harvest the ontology or archive"),
            "persistent_world": ("glyph edition v0: an interface to the hive; the tie together", "DORMANT", "the persistent layer Cognitopolis wants; check_in verb goes here"),
            "rtfm_graph": ("browsable knowledge graph of the fleet's manuals", "ABSORBED", "corpus FTS index is the living twin (daily 09:00); page is the browsable face"),
            "seat": ("ghost surface: the machine, reconciled", "DORMANT", "the seat's mirror; pair with self_hologram"),
            "self_hologram": ("the seat's self-model trajectory, mined from the signed record", "DORMANT", "zknot self-steal meter's visual twin; regenerate from the signed record"),
            "steal_tools": ("the armory: 116 steal tools", "LIVE", "corpus/steal map's face; keep counted"),
            "the_fence": ("the fence", "DORMANT", "fence-owner law (FW-11) rendered"),
            "the_index": ("estate map: open-rib spine v0", "ABSORBED", "watch/inbox/INDEX.json is the spine now; page is its face"),
            "viz_gallery": ("viz lab index", "DORMANT", "door to the vislab/ wing"),
        },
    },
    {
        "id": "watch",
        "name": "THE WATCH",
        "blurb": "ops instruments: what the fleet is doing right now, what it costs, what drifted, what it decided.",
        "pages": {
            "burn_board": ("weekend build burn board", "DORMANT", "wire to usage.jsonl or fold into spend"),
            "daytool": ("day tool", "DORMANT", "harvest its one good widget, then archive under no-sacred-cows"),
            "decisions": ("decisions: unactioned first (the PDB)", "DORMANT", "the decision debt door; wire to queue/todo.md"),
            "drift_board": ("teleo drift board T1-T6", "LIVE", "the drift patrol's face (citation debts, healings)"),
            "fleet": ("hypervisor: fleet cool/heat + real bills", "LIVE", "the cost instrument; every paid dispatch banks here"),
            "health": ("loop health: what works, what doesn't", "DORMANT", "wire to gate results or fold into drift_board"),
            "intel": ("tonight in your fleet", "DORMANT", "night-shift brief face"),
            "lanes": ("lanes: manager board", "LIVE", "queue/lanes runner state faces this"),
            "links": ("links library v1: the fleet's link library", "LIVE", "LINKS.jsonl door (FW-45)"),
            "live": ("fleet live: every window, verbose", "DORMANT", "supersede with the console's live section or wire to watch/"),
            "live_feed": ("THE FL33T: live feed", "DORMANT", "same ask as live: one of the two must die or both wire up"),
            "operator_board": ("the operator's board", "DORMANT", "his wall; give it attention.md + DAWN_REPORT doors"),
            "ractor": ("the ractor board", "LIVE", "ractor swarm faces this"),
            "reply_console": ("reply overdrive: 36 doors", "DORMANT", "reply lanes; wire to the mesh_delta plant wire"),
            "scout_deck": ("scout deck", "DORMANT", "improve --status as a surface"),
            "the_radar": ("fleet radar: blips = live seats (gmunk/Oblivion lineage)", "DORMANT", "the watch, visualized; hypervisor already knows the seats"),
            "tide": ("nightly scattershot compaction, automation-b0ebbbb9, daily 06:15", "LIVE", "the tide organ: wave persists, medium doesn't accumulate"),
            "verdicts": ("verdicts panel: data door GET /api/v1/verdicts", "LIVE", "estate organs' verdict feed (Mickey17 wave 3)"),
            "wearable": ("swarm HUD wearable", "DORMANT", "the tablet/roku roster's face; mesh expansion wants this"),
            "whale_console": ("whale console: almanac, doors, council", "DORMANT", "external-steal watch's face"),
            "whale_feed": ("whale patrol: live feed", "DORMANT", "same wiring as whale_console"),
        },
    },
    {
        "id": "salon",
        "name": "SALON & VOICE",
        "blurb": "surfaces for talk: the seat speaks, listens, and hosts. anonymous science to cast voice.",
        "pages": {
            "cast": ("mag cast", "DORMANT", "herald face"),
            "cast-voice": ("mag voice: the seat, audible", "DORMANT", "TTS twin of keeper_voice"),
            "chan": ("/keep/: anonymous science", "LIVE", "the chan skill's web face"),
            "control": ("direct mag", "LIVE", "the command surface"),
            "feed": ("mycelial republic feed", "DORMANT", "mesh_delta's read-only face; wire to the plant wire"),
            "phonesalon": ("the android free-lane deck", "LIVE", "the phone seats' deck; mesh expansion roster lives here"),
            "salon_lightmap": ("the room that remembers (salon edition)", "DORMANT", "salon skill's memory made visible"),
            "sovereign_shell": ("mag sovereign shell", "DORMANT", "shell door; pair with control"),
            "table": ("mag table: the lantern", "DORMANT", "the L0 dossier's table face"),
        },
    },
    {
        "id": "stubs",
        "name": "STUBS (dedupe 2026-09-22)",
        "blurb": "the earlier organization wave already moved these; the root copies are redirect stubs only. canonical copies live in games/.",
        "pages": {
            "arena_operator_field": ("moved to /static/games/", "STUB", "canonical: games/arena_operator_field.html"),
            "arrakis": ("moved to /static/games/", "STUB", "canonical: games/arrakis.html"),
            "maze_arena": ("moved to /static/games/", "STUB", "canonical: games/maze_arena.html"),
            "mud": ("moved to /static/games/", "STUB", "canonical: games/mud.html"),
        },
    },
]

WINGS = [
    ("night/", "the overnight mind's papers: 22 pages (sherpa spec, stockfish, titor stack, time machinery, hermes dossiers, surface atlas, orphan register)"),
    ("games/", "the arcade proper: frontier_souls, ruins_go, skifree, mud, arrakis, arena_operator_field, maze_arena, toy"),
    ("decks/", "pro decks: cacheecon, gamebuild, glmwatch, legions, mag, mesh3d, personal, rocinante"),
    ("doctrine/", "doctrine rendered: autonomy wheel, burst doctrine, swarm scale plan, tri-party, x-scout"),
    ("museum/", "the museum basement: previous map attempts and carcasses (index_old_mag_board, scan_me, viz_horse_lane2_carcass)"),
    ("vislab/", "the vis lab: belt trick, isfahan lattice, catalog"),
    ("comics/", "session comics (the stupid-model lane: JSON panel spec, deterministic SVG)"),
    ("art/", "receipts as art: forge log, privlidge receipts, puzzles, operator fire"),
    ("suno/", "the estate soundtrack; sound/, media/, tiles/, trails/, state/, lanes/, lattices/, index_data/, phonesalon/, frontdoor/, docs/, shaders/, data/ = the data floors"),
]

STATUS_COLOR = {"LIVE": "#7cf5a0", "DORMANT": "#e8b45a", "ABSORBED": "#7cf5ff", "STUB": "#66738a"}


def build() -> int:
    census_path = ROOT / "zoo_census.jsonl"
    if not census_path.is_file():
        print("run tools/zoo_census.py first")
        return 2
    census = {
        row["file"].removesuffix(".html"): row
        for row in (json.loads(line) for line in census_path.read_text().splitlines())
    }

    assigned: dict[str, tuple[dict, tuple]] = {}
    for hall in HALLS:
        for page, meta in hall["pages"].items():
            if page not in census:
                print(f"HALLS names a page with no census row: {page}.html")
                return 2
            if page in assigned:
                print(f"page assigned twice: {page}.html")
                return 2
            assigned[page] = (hall, meta)

    missing = sorted(set(census) - set(assigned))
    if missing:
        print(f"COVERAGE GATE FAILED: {len(missing)} census pages unassigned: {missing}")
        return 1

    total = len(census)
    counts: dict[str, int] = {}
    for hall, (meta) in [(h, m) for h in HALLS for m in h["pages"].values()]:
        counts[meta[1]] = counts.get(meta[1], 0) + 1

    def card(page: str, hall: dict, meta: tuple) -> str:
        law, status, runs = meta
        row = census[page]
        born = html.escape(str(row.get("birth", "?")))
        title = html.escape(row.get("title") or page)
        return (
            f'<a class="card" href="./{html.escape(page)}.html">'
            f'<div class="t"><span class="chip" style="color:{STATUS_COLOR[status]}">{status}</span>{title}</div>'
            f'<div class="law">{html.escape(law)}</div>'
            f'<div class="runs">&#9656; {html.escape(runs)}</div>'
            f'<div class="meta">{born} &middot; {row["bytes"]}b</div></a>'
        )

    parts = [
        "<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\">",
        '<meta name="viewport" content="width=device-width, initial-scale=1">',
        "<title>THE ZOO &mdash; one law per room</title><style>",
        ":root{--bg:#070b10;--panel:#0d141d;--line:#1b2532;--amber:#e8b45a;--cyan:#7cf5ff;--txt:#c9d3e0;--dim:#66738a}",
        "*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--txt);font:13px/1.5 ui-monospace,Consolas,monospace}",
        "header{padding:16px;border-bottom:1px solid var(--line);position:sticky;top:0;background:var(--bg);z-index:5}",
        "h1{margin:0;font-size:16px;color:var(--amber);letter-spacing:1px}.sub{color:var(--dim);font-size:11px;margin-top:3px}",
        "#q{margin-top:10px;width:100%;max-width:520px;background:#0c131c;border:1px solid var(--line);color:var(--txt);padding:7px 10px;font:inherit}",
        "main{padding:16px;max-width:1280px;margin:0 auto}",
        "section{margin-bottom:28px}h2{font-size:13px;color:var(--cyan);letter-spacing:1px;margin:0 0 2px}",
        ".blurb{color:var(--dim);font-size:11px;margin:0 0 10px}",
        ".grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(300px,1fr));gap:10px}",
        ".card{display:block;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px;text-decoration:none;color:var(--txt)}",
        ".card:hover{border-color:var(--amber)}",
        ".card .t{font-weight:bold;font-size:12px;margin-bottom:4px}.chip{font-size:10px;margin-right:8px;letter-spacing:1px}",
        ".card .law{font-size:11px;color:var(--txt);opacity:.85;margin-bottom:5px}",
        ".card .runs{font-size:11px;color:var(--cyan);opacity:.8;margin-bottom:5px}",
        ".card .meta{font-size:10px;color:var(--dim)}",
        ".wings{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px;font-size:12px}",
        ".wings div{margin:4px 0}.wings a{color:var(--cyan);text-decoration:none}",
        "</style></head><body><header>",
        '<h1>THE ZOO &mdash; one law per room</h1>',
        f'<div class="sub">the ancestry map of dashboard/static: {total} rooms, '
        f'{counts.get("LIVE",0)} live &middot; {counts.get("DORMANT",0)} dormant (unwired, not dead) &middot; '
        f'{counts.get("ABSORBED",0)} absorbed (the idea lives in a repo organ) &middot; {counts.get("STUB",0)} stubs. '
        'built by tools/zoo_render.py from zoo_census.jsonl &mdash; regenerate, never hand-edit.</div>',
        '<input id="q" placeholder="filter rooms (name, law, run-with)..." oninput="filter()">',
        "</header><main>",
    ]
    for hall in HALLS:
        parts.append('<section id="hall-' + hall["id"] + '">')
        parts.append(f'<h2>{html.escape(hall["name"])}</h2>')
        parts.append(f'<div class="blurb">{html.escape(hall["blurb"])}</div>')
        parts.append('<div class="grid">')
        for page, meta in hall["pages"].items():
            parts.append(card(page, hall, meta))
        parts.append("</div></section>")
    parts.append('<section><h2>THE WINGS</h2><div class="blurb">below root: the data floors and the overnight paper wing</div><div class="wings">')
    for wing, blurb in WINGS:
        parts.append(f'<div><a href="./{html.escape(wing)}">{html.escape(wing)}</a> &mdash; {html.escape(blurb)}</div>')
    parts.append("</div></section></main>")
    parts.append(
        "<script>function filter(){var q=document.getElementById('q').value.toLowerCase();"
        "document.querySelectorAll('.card').forEach(function(c){var t=c.textContent.toLowerCase();"
        "c.style.display=t.indexOf(q)>=0?'':'none';});"
        "document.querySelectorAll('section').forEach(function(s){var any=[...s.querySelectorAll('.card')].some(function(c){return c.style.display!=='none'});"
        "if(s.querySelector('.grid'))s.style.display=any?'':'none';});}</script>"
    )
    parts.append("</body></html>")

    out = ROOT / "zoo.html"
    out.write_text("".join(parts), encoding="utf-8", newline="\n")
    print(f"zoo.html built: {total}/{total} rooms mapped, statuses {counts} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(build())
