// nav.js - one bar, all surfaces (2026-09-02). Single source of truth: edit links HERE.
// Repaired 2026-09-28 (FW-45): the copy at HEAD was a 532-byte truncated duplicate of
// its own prefix (landed in the 161cafffe dogfood wave) - a JS SyntaxError that killed
// the fleetnav bar on every static page that loads this file. Body restored
// byte-faithful from the last intact version (checkpoint d575bc168, 5,301 bytes) with
// exactly two edits on top: the /static/maze_arena.html entries point at
// /static/games/ (the redirect 161cafffe's own commit message records as intent) and
// the Links Library entry for the FW-45 widget (links.html + /api/v1/links/tail).
(function(){
  var LINKS = [
    ["/static/home.html", "Home"],
    ["/static/index.html", "Console"],
    ["/", "Hypervisor"],
    ["/static/dungeon.html", "The Game"],
    ["/static/games/", "Maze Arena"],
    ["/static/shadow_walk.html", "Shadow Walk"],
    ["/static/spectral_maze.html", "Spectral Maze"],
    ["/static/arrakis.html", "Arrakis"],
    ["/static/phase_particles.html", "Phase Particles"],
    ["/static/airflow_home.html", "Airflow Home"],
    ["/static/light_maze.html", "Light Maze"],
    ["/static/hardware_primer.html", "Hardware Primer"],
    ["/static/tavern_brawl.html", "Kabuki Tavern"],
    ["/static/arena_operator_field.html", "Arena Field"],
    ["/static/decks.html", "Decks"],
    ["/static/daytool.html", "Day Tool"],
    ["/static/decisions.html", "Decisions"],
    ["/static/spend.html", "Spend"],
    ["/chan", "Chan"],
    ["/static/ractor.html", "Ractor Board"],
    ["/static/museum.html", "Museum"],
    ["/static/night/index.html", "Night Book"],
    ["/static/room_lightmap.html", "Room Lightmap"],
    ["/static/lattice.html", "Lattice"],
    ["/static/wave.html", "Wave"],
    ["/static/fleet.html", "Fleet"],
    ["/static/health.html", "Health"],
    ["/static/agents.html", "Agents"],
    ["/static/seat.html", "Seat"],
    ["/static/sovereign_shell.html", "Shell"],
    ["/static/aos.html", "AOS"],
    ["/static/feed.html", "Feed"],
    ["/static/links.html", "Links"],
    ["/static/verdicts.html", "Verdicts"],
    ["/static/cast.html", "Cast"],
    ["/static/cast-voice.html", "Cast Voice"],
    ["/static/control.html", "Control"],
    ["/static/table.html", "Table"],
    ["/static/wearable.html", "Wearable"],
    ["/static/falsifiers.html", "Falsifiers"],
    ["/static/chain_check.html", "Chain Check"],
    ["/static/claim_check.html", "Claim Check"],
    ["/static/lattice_check.html", "Lattice Check"],
    ["/static/fleet_symbols.html", "Fleet Symbols"],
    ["/static/rtfm_graph.html", "RTFM Graph"],
    ["/static/calabi_yau.html", "Calabi-Yau"],
    ["/static/field_quills.html", "Field Quills"],
    ["/static/viz_gallery.html", "Viz Lab"],
    ["/static/phonesalon.html", "Phone Salon"],
    ["/static/lanes.html", "Lanes"],
    ["/static/mesh_gallery.html", "Mesh Gallery"],
    ["/static/intel.html", "Intel"],
    ["/static/art/index.html", "Quest Art"],
    ["/static/burn_board.html", "Burn Board"],
    ["/static/swarm_board.png", "Swarm Board"],
    ["/static/salons/astra/index.html", "Astra Salon"],
    ["/static/live.html", "Live"],
    ["/static/live_feed.html", "Live Feed"],
    ["/static/operator_board.html", "Operator Board"],
    ["/static/verkle_knot_wave.html", "Knot Wave"],
    ["/static/viz_3d_verkle.html", "3D Verkle"],
    ["/static/self_hologram.html", "Self Hologram"],
    ["/static/memory_map.html", "Memory Map"],
    ["/static/module_map.html", "Module Map"],
    ["/static/labs_map.html", "Labs Map"],
    ["/static/erosion_field.html", "Erosion Field"],
    ["/static/arena_operator_field.html", "Arena Field"],
    ["/static/steer_field.html", "Steer Field"],
    ["/static/games/", "Maze Arena"],
    ["/static/keeper_voice.html", "Keeper's Voice"],
    ["/static/incident_dungeon.html", "Incident Dungeon"],
    ["/static/salon_lightmap.html", "Salon Lightmap"],
    ["/static/tesuji_map.html", "Tesuji Map"],
    ["/static/shadow_walk.html", "Shadow Walk"],
    ["/static/conservation_room.html", "The Sowing Room"],
    ["/static/fable_room.html", "Fable Room #0"],
    ["/static/bad_apple_field.html", "Bad Apple Field"],
    ["/static/eraser_maze.html", "Eraser Maze"],
    ["/static/spectral_maze.html", "Spectral Maze"],
    ["/static/arrakis.html", "Arrakis"],
    ["/static/phase_particles.html", "Phase Particles"],
    ["/static/airflow_home.html", "Airflow Home"],
    ["/static/light_maze.html", "Light Maze"],
    ["/static/hardware_primer.html", "Hardware Primer"],
    ["/static/tavern_brawl.html", "Kabuki Tavern"],
    ["/static/game.html", "Necromancer"],
    ["/static/grab_write.html", "Grab Write"],
    ["/static/rib_toy.html", "Rib Toy"],
    ["/static/scout_deck.html", "Scout Deck"],
    ["/static/smith_chart.html", "Smith Chart"],
    ["/static/smith_globe.html", "Smith Globe"],
    ["/static/vislab.html", "Vislab"],
    ["/static/room.html", "The Room"],
    ["/static/steal_tools.html", "Armory"],
    ["/static/viz_spore_fish.html", "Spore Fish"],
    ["/static/index.clear-ui.html", "Clear UI"],
    ["/static/_rtfm_graph_shell.html", "RTFM Shell"],
    ["/static/doorbench.html", "DOORBENCH"]
  ];
  var css = document.createElement('style');
  css.textContent = '#fleetnav{background:#0a1412;border-bottom:1px solid rgba(0,240,255,.22);padding:6px 10px;font:11px ui-monospace,Consolas,monospace;display:flex;flex-wrap:wrap;gap:4px}'
    + '#fleetnav a{color:#7cf5ff;text-decoration:none;padding:2px 8px;border:1px solid rgba(0,240,255,.22);border-radius:9px;letter-spacing:.04em}'
    + '#fleetnav a:hover{background:#0f2019}#fleetnav a.cur{color:#e8c96a;border-color:#e8c96a}';
  document.head.appendChild(css);
  var bar = document.createElement('div'); bar.id = 'fleetnav';
  var here = location.pathname;
  bar.innerHTML = LINKS.map(function(l){
    var cur = (l[0] === here || (here !== '/' && l[0].indexOf(here) === 0)) ? ' class="cur"' : '';
    return '<a href="' + l[0] + '"' + cur + '>' + l[1] + '</a>';
  }).join('');
  document.body.prepend(bar);
})();
