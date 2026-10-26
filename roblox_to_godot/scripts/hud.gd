extends Control
## HUD — AA5 2026-09-30 (last-mile wave: "the game has all the systems but
## the HUD is the basic text from the original slice"). One Control, one
## _draw(): every panel below is drawn geometry + draw_string, replacing the
## four plain Labels of the old game.gd _build_hud. Receipt:
## watch/inbox/last_mile_20260930/AA5_HUD.md.
##
## Panels (the mission's four features):
##   1. WATER (top-left): a level bar per pool — spring/terrace/gate1/hollow/
##      waste — colored by fill (dry amber -> deep blue; waste lerps murky so
##      lost water reads lost), one tick per world unit (the graph's integer
##      granularity), live volume as text, and the wettest pool's name tinted
##      gold (the school gathers there — game.gd _wettest_pool). The crown is
##      the goal, not a pool: it gets a progress RING (volume / 4) instead of
##      a bar, drawn in the board's crown-arc grammar (arc start -PI/2, cyan
##      fill over a dim track — game.gd _draw "crown").
##   2. SCHOOL (top-right): total alive, tagged count (host.score), and the
##      innkeeper's last greeting IF PRESENT — the LW8 bot speaks through the
##      ordinary say channel, so its lines arrive as tick events
##      "innkeeper: <text>" (server/world.py _apply, LW6 grammar
##      "<user>: <text>"); the panel shows the newest one while it lives in
##      the host's 64-slot event ring (B2 2026-09-30: was a 6-event feed)
##      and drops it the moment the ring scrolls it
##      out (the mission's "if present"). AJ4 2026-09-30: this greeting
##      rescan stays feed-based BY DESIGN (it shows lines while they live in
##      the visible feed window); the one-shot tag events moved to the
##      graph's water_event signal (game.gd _push_event) because the old
##      count-cursor over the bounded feed went blind once the feed
##      saturated (receipt AJ4_PLAYTEST.md).
##   3. MODE (top-center): SOVEREIGN / AUTHORITATIVE / PROBING plus the head
##      law state HYDROLOGY ON/OFF (game.gd's H key / MAG_HYDROLOGY boot).
##   4. TAG POPUPS: on a fish tag the score number floats up 26 px over
##      0.9 s and fades (quadratic alpha). Sovereign: the flock's
##      fish_killed signal — game.gd's _on_fish_killed increments host.score
##      FIRST (connection order: _build_flock connects before _build_hud),
##      so the popup reads the new total. Authoritative: the server's own
##      "<user> tags a fish at <pool> (score N)" event (the local kill is
##      only a sensing proposal there — game.gd _on_fish_killed — so the
##      signal path is suppressed: one popup per tag, server-scored, other
##      players' tags included).
##
## The hint line and the event feed keep the old surfaces (same positions,
## same one-frame hint channel), and the win overlay (ColorRect + Label) is
## byte-moved here from game.gd _build_hud/_crown_filled — same colors, same
## geometry, same string (em-dash law: nothing re-authored). V5 feel pass:
## that overlay's score now COUNTS UP 0 -> N over WIN_COUNT_S on its own
## post-win clock (the victory sequence's fourth beat; juice.gd owns the
## wash, the rising flood line, and the SUMMIT banner on layer 2).
##
## LAWS. Zero RNG: no RandomNumberGenerator, no randf — the slice law
## (README "Deterministic water, organic fish"). CLOCK LAW: every animation
## is a pure function of host.sim_time (the W1 receipt: no wall clock), so a
## popup freezes with the world at the win, frame-replayable. Render-only:
## this layer reads graph/pools/flock/score/mode and mutates nothing except
## the one-frame hint_text channel it inherits from the old _update_hud
## (draw the hint, then clear it — the same bytes, relocated; game.gd
## _update_hints refills it every frame while the context holds).

const VIEW := Vector2(1152.0, 648.0)  # project.godot viewport (juice.gd idiom)

# game.gd mirrors, read-only (receipts in the comments):
const CROWN_GOAL := 4          # game.gd WIN_CROWN — the ring denominator
const WORLD_WATER := 8.0       # game.gd header "Total water in the world: 8" — the bar denominator
const MODE_PROBING := 0        # game.gd enum Mode order {PROBING=0,
const MODE_AUTHORITATIVE := 1  # AUTHORITATIVE=1, SOVEREIGN=2}; if that enum
const MODE_SOVEREIGN := 2      # ever reorders, this mirror must ride along
const INNKEEPER_PREFIX := "innkeeper: "  # say-event grammar "<user>: <text>" (server/world.py _apply)

# Panel geometry (screen space; the board is 1152x648 with pools at y<=600).
const WATER_RECT := Rect2(20.0, 12.0, 216.0, 148.0)
const SCHOOL_RECT := Rect2(940.0, 12.0, 192.0, 52.0)
const SCHOOL_GREET_EXTRA := 48.0  # the panel grows only while a greeting is present
const MODE_BASELINE := 24.0       # top-center strip baseline
const HINT_POS := Vector2(20.0, 596.0)
const EVENT_POS := Vector2(20.0, 620.0)  # the old hud_event label position

const BAR_X := 92.0    # bar slot x, relative to the water panel
const BAR_W := 92.0
const BAR_H := 7.0
const ROW_H := 17.0
const ROWS_START_Y := 60.0  # relative to the water panel (below the crown row + divider)
const POOL_ROWS: Array = ["spring", "terrace", "gate1", "hollow", "waste"]

# Palette (board-grammar colors: WET is water_particles DEEP, CROWN_RING and
# GOLD are game.gd _draw's crown arc and tired-fish gold).
const PANEL_BG := Color(0.04, 0.05, 0.07, 0.62)
const PANEL_EDGE := Color(0.55, 0.62, 0.7, 0.28)
const BAR_SLOT := Color(0.1, 0.12, 0.16, 0.9)
const BAR_EDGE := Color(0.5, 0.58, 0.68, 0.35)
const DRY := Color(0.55, 0.44, 0.28)
const WET := Color(0.30, 0.55, 0.80)
const WASTE_WET := Color(0.45, 0.34, 0.38)
const CROWN_RING := Color(0.55, 0.85, 0.95)
const CROWN_TEXT := Color(0.7, 0.9, 1.0)
const TEXT_DIM := Color(0.6, 0.65, 0.7)
const TEXT_MAIN := Color(0.85, 0.88, 0.92)
const GOLD := Color(0.95, 0.8, 0.35)
const SOVEREIGN_COL := Color(0.55, 0.85, 0.8)
const AUTH_COL := Color(0.9, 0.75, 0.4)
const PROBE_COL := Color(0.55, 0.58, 0.62)
const HYDRO_ON := Color(0.55, 0.85, 0.95)
const HYDRO_OFF := Color(0.5, 0.53, 0.58)
const INN_COL := Color(0.85, 0.7, 0.45)

# Tag popup (feature 4): pure function of host.sim_time at draw time.
const POPUP_S := 0.9     # seconds afloat
const POPUP_RISE := 26.0 # px traveled upward over POPUP_S
const POPUP_CAP := 8     # bounded history; oldest dropped

# V5 feel pass: the win label's score COUNTS UP (the victory sequence's
# fourth beat; juice.gd owns the other three). Timebase is this node's own
# post-win delta accumulator — the same instrument sim_time is (game.gd
# `sim_time += delta`) — because game.gd freezes sim_time the frame `won`
# flips and a frozen clock would freeze the count on its first frame
# (the juice.gd CLOCK LAW receipt, hud edition).
const WIN_COUNT_S := 1.2

var host: Node = null          # game.gd: graph, pools, flock, score, mode, hint_text, last_events, sim_time
var graph: Node = null         # systems/water_graph.gd instance (read-only; water_event source)
var pools: Dictionary = {}     # node_name -> Vector2 board position
var flock_ref: Node = null     # systems/flock.gd instance (fish array + fish_killed)
var popups: Array[Dictionary] = []  # {pos: Vector2, n: int, t0: float}
var greeting := ""             # newest "innkeeper: " line in the feed ("" when absent)
var win_panel: ColorRect = null  # the win overlay, byte-moved from game.gd _build_hud
var win_label: Label = null
var win_score := 0             # V5: the counted-up target (host score at show_win)
var win_clock := 0.0           # V5: post-win accumulator (see WIN_COUNT_S receipt)


## The water_particles/juice contract: called right after instantiation,
## before add_child(). graph, pools, and flock all exist by the end of
## game.gd _build_flock, which runs before _build_hud.
func bind(host_ref: Node) -> void:
    host = host_ref
    graph = host.get("graph")
    pools = host.get("pools")
    flock_ref = host.get("flock")
    # AJ4 2026-09-30: one-shot tag events arrive on the graph's water_event
    # signal (game.gd _push_event emits at every append) — the old count-
    # cursor over the 6-slot feed went blind once the feed saturated.
    graph.connect("water_event", _on_event)


func _ready() -> void:
    # Node building deferred to _ready (juice.gd fix 3: child building errors
    # outside the scene tree — its 60f smoke is the receipt).
    mouse_filter = Control.MOUSE_FILTER_IGNORE  # the shepherd IS the mouse; the HUD never eats it
    size = VIEW
    win_panel = ColorRect.new()
    win_panel.color = Color(0.04, 0.05, 0.07, 0.88)
    win_panel.size = VIEW
    win_panel.visible = false
    add_child(win_panel)
    win_label = Label.new()
    win_label.text = "THE CROWN FILLS.\nThe mountain drinks. %d fish tagged.\n\nR — climb again."
    win_label.position = Vector2(330, 250)
    win_label.add_theme_font_size_override("font_size", 30)
    win_panel.add_child(win_label)
    # Second connector, after game.gd's own (line _build_flock): when a
    # sovereign tag fires, host.score is already incremented when we read it.
    flock_ref.fish_killed.connect(_on_fish_killed)


func show_win(score: int) -> void:
    # game.gd _crown_filled hands the score over; the string is byte-moved
    # from the old _crown_filled (em-dash law: pre-existing text, moved).
    # V5: the label starts the COUNT-UP at 0 and _process walks it to score
    # over WIN_COUNT_S (the victory sequence's fourth beat).
    win_score = score
    win_clock = 0.0
    win_label.text = _win_text(0)
    win_panel.visible = true


func _win_text(n: int) -> String:
    return "THE CROWN FILLS.\nThe mountain drinks. %d fish tagged.\n\nR — climb again." % n


func _process(delta: float) -> void:
    if host == null:
        return
    if win_panel != null and win_panel.visible:
        # V5 count-up: the post-win accumulator (WIN_COUNT_S receipt above);
        # clamped at the final score, so the panel holds its number forever.
        win_clock += delta
        var t := clampf(win_clock / WIN_COUNT_S, 0.0, 1.0)
        var n := int(floor(t * float(win_score)))
        win_label.text = _win_text(n)
    _scan_greeting()
    _expire_popups()
    queue_redraw()


# ------------------------------------------------------------------ events ----

func _scan_greeting() -> void:
    # The greeting is feed-window semantics ("if present", the mission's
    # clause): a full rescan of the host's event ring (64-slot, B2; was a
    # 6-string feed) every poll, newest
    # wins, cleared exactly when the feed scrolls the line out. One-shot tag
    # events no longer ride this path — they arrive on the water_event
    # signal (AJ4; the old count-cursor was blind once the feed saturated).
    if host == null:
        return
    var evs: Variant = host.get("last_events")
    if evs == null:
        return
    var cur: Array[String] = evs
    greeting = ""
    for e: String in cur:
        if e.begins_with(INNKEEPER_PREFIX):
            greeting = e.substr(INNKEEPER_PREFIX.length())  # newest wins: the scan runs in feed order


func _on_event(text: String) -> void:
    # Authoritative tag popup: "<user> tags a fish at <pool> (score N)."
    # (server/world.py _apply). Sovereign tags emit no event string — the
    # fish_killed signal path is that mode's only popup source, so a local
    # kill in authoritative mode never double-pops.
    if not text.contains(" tags a fish at "):
        return
    var seg: PackedStringArray = text.split(" tags a fish at ")
    if seg.size() < 2:
        return
    var pool_name: String = seg[1].split(" ")[0]
    if not pools.has(pool_name):
        return
    var n := int(host.get("score"))
    var idx := text.find("(score ")
    if idx >= 0:
        var s: String = text.substr(idx + 7).split(")")[0]
        if s.is_valid_int():
            n = s.to_int()  # the server's number wins (game.gd _score_from_event grammar)
    var pos: Vector2 = pools[pool_name]
    _spawn_popup(pos, n)


func _on_fish_killed(fish_id: int) -> void:
    # Sovereign popup: position = the tagged fish's last position, number =
    # host.score AFTER game.gd's increment (connection order, see _ready).
    if int(host.get("mode")) == MODE_AUTHORITATIVE:
        return  # sensing-only school: the server's event is the real tag (header)
    var pos := Vector2(pools.get("spring", Vector2.ZERO))
    var fish_arr: Array = flock_ref.get("fish")
    if fish_id >= 0 and fish_id < fish_arr.size():
        pos = fish_arr[fish_id].get("pos", pos)
    _spawn_popup(pos, int(host.get("score")))


func _spawn_popup(pos: Vector2, n: int) -> void:
    var clamped := Vector2(clampf(pos.x, 30.0, VIEW.x - 30.0), clampf(pos.y, 30.0, VIEW.y - 20.0))
    popups.append({"pos": clamped, "n": n, "t0": float(host.get("sim_time"))})
    if popups.size() > POPUP_CAP:
        popups = popups.slice(popups.size() - POPUP_CAP)


func _expire_popups() -> void:
    var now: float = float(host.get("sim_time"))
    var live: Array[Dictionary] = []
    for p: Dictionary in popups:
        if now - float(p["t0"]) < POPUP_S:
            live.append(p)
    popups = live


# -------------------------------------------------------------------- draw ----

func _draw() -> void:
    if host == null or graph == null:
        return
    _draw_water_panel()
    _draw_school_panel()
    _draw_mode_strip()
    _draw_popups()
    _draw_events()
    _draw_hint()


func _draw_water_panel() -> void:
    var font := ThemeDB.fallback_font
    var px: float = WATER_RECT.position.x
    var py: float = WATER_RECT.position.y
    _panel(WATER_RECT)

    # The crown ring (feature 1's special case): progress toward the goal in
    # the board's crown-arc grammar — dim track first, cyan fill from -PI/2.
    var crown_v: int = graph.volume("crown")
    var center := Vector2(px + 36.0, py + 28.0)
    draw_arc(center, 11.0, -PI / 2, -PI / 2 + TAU, 28, Color(0.25, 0.3, 0.38, 0.8), 2.0)
    var cfrac: float = clampf(float(crown_v) / float(CROWN_GOAL), 0.0, 1.0)
    if cfrac > 0.0:
        draw_arc(center, 11.0, -PI / 2, -PI / 2 + TAU * cfrac, 28, CROWN_RING, 3.0)
    draw_circle(center, 2.0, CROWN_RING if crown_v > 0 else Color(0.3, 0.35, 0.42, 0.8))
    draw_string(font, center + Vector2(22.0, 4.0), "CROWN %d/%d" % [crown_v, CROWN_GOAL], HORIZONTAL_ALIGNMENT_LEFT, -1, 12, CROWN_TEXT)
    draw_string(font, center + Vector2(22.0, 17.0), "fill it to win", HORIZONTAL_ALIGNMENT_LEFT, -1, 9, TEXT_DIM)
    draw_line(Vector2(px + 12.0, py + 46.0), Vector2(WATER_RECT.end.x - 12.0, py + 46.0), PANEL_EDGE, 1.0)

    # One bar row per pool, colored by fill against the world total.
    var wettest: String = String(host.get("wettest"))
    for i in POOL_ROWS.size():
        var pool_name: String = POOL_ROWS[i]
        var v: int = graph.volume(pool_name)
        var frac: float = clampf(float(v) / WORLD_WATER, 0.0, 1.0)
        var y: float = py + ROWS_START_Y + float(i) * ROW_H
        var name_col: Color = GOLD if pool_name == wettest else TEXT_DIM
        draw_string(font, Vector2(px + 12.0, y + 9.0), pool_name, HORIZONTAL_ALIGNMENT_LEFT, -1, 11, name_col)
        var slot := Rect2(Vector2(px + BAR_X, y), Vector2(BAR_W, BAR_H))
        draw_rect(slot, BAR_SLOT, true)
        if frac > 0.0:
            var fill_col: Color = DRY.lerp(WET, frac)
            if pool_name == "waste":
                fill_col = DRY.lerp(WASTE_WET, frac)  # water at the drain reads lost
            draw_rect(Rect2(slot.position, Vector2(BAR_W * frac, BAR_H)), fill_col, true)
        # Unit ticks: one per world unit, the integer graph's granularity.
        for u in int(WORLD_WATER) - 1:
            var tx: float = slot.position.x + BAR_W * float(u + 1) / WORLD_WATER
            draw_line(Vector2(tx, slot.position.y + 1.0), Vector2(tx, slot.end.y - 1.0), Color(0.04, 0.05, 0.07, 0.55), 1.0)
        draw_rect(slot, BAR_EDGE, false, 1.0)
        draw_string(font, Vector2(slot.end.x + 8.0, y + 9.0), str(v), HORIZONTAL_ALIGNMENT_LEFT, -1, 11, TEXT_MAIN)


func _draw_school_panel() -> void:
    var font := ThemeDB.fallback_font
    var rect := SCHOOL_RECT
    if greeting != "":
        rect.size.y += SCHOOL_GREET_EXTRA
    _panel(rect)
    var alive := 0
    var fish_arr: Array = flock_ref.get("fish")
    for f: Dictionary in fish_arr:
        if bool(f.get("alive", false)):
            alive += 1
    var tagged: int = int(host.get("score"))
    var px: float = rect.position.x + 12.0
    draw_string(font, Vector2(px, rect.position.y + 20.0), "SCHOOL  %d alive" % alive, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, TEXT_MAIN)
    draw_string(font, Vector2(px, rect.position.y + 38.0), "TAGGED  %d" % tagged, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, GOLD if tagged > 0 else TEXT_DIM)
    if greeting == "":
        return
    draw_string(font, Vector2(px, rect.position.y + 58.0), "INNKEEPER", HORIZONTAL_ALIGNMENT_LEFT, -1, 9, INN_COL)
    var lines := _wrap2(greeting, 33)  # 33 chars at size 10 fits the 192 px panel with padding
    for i in lines.size():
        draw_string(font, Vector2(px, rect.position.y + 71.0 + float(i) * 12.0), lines[i], HORIZONTAL_ALIGNMENT_LEFT, -1, 10, Color(0.8, 0.78, 0.7, 0.9))


func _draw_mode_strip() -> void:
    var font := ThemeDB.fallback_font
    var mode_v: int = int(host.get("mode"))
    var mode_txt := "PROBING"
    var mode_col: Color = PROBE_COL
    if mode_v == MODE_AUTHORITATIVE:
        mode_txt = "AUTHORITATIVE"
        mode_col = AUTH_COL
    elif mode_v == MODE_SOVEREIGN:
        mode_txt = "SOVEREIGN"
        mode_col = SOVEREIGN_COL
    var hydro: bool = bool(graph.get("hydrology"))
    var hydro_txt := "HYDROLOGY ON" if hydro else "HYDROLOGY OFF"
    var hydro_col: Color = HYDRO_ON if hydro else HYDRO_OFF
    var sep := "   ·   "
    var w1: float = font.get_string_size(mode_txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 13).x
    var ws: float = font.get_string_size(sep, HORIZONTAL_ALIGNMENT_LEFT, -1, 13).x
    var w2: float = font.get_string_size(hydro_txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 13).x
    var x0: float = VIEW.x * 0.5 - (w1 + ws + w2) * 0.5
    draw_string(font, Vector2(x0, MODE_BASELINE), mode_txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, mode_col)
    draw_string(font, Vector2(x0 + w1, MODE_BASELINE), sep, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(0.45, 0.5, 0.55, 0.7))
    draw_string(font, Vector2(x0 + w1 + ws, MODE_BASELINE), hydro_txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, hydro_col)


func _draw_popups() -> void:
    var font := ThemeDB.fallback_font
    var now: float = float(host.get("sim_time"))
    for p: Dictionary in popups:
        var t: float = clampf((now - float(p["t0"])) / POPUP_S, 0.0, 1.0)
        var col := Color(GOLD.r, GOLD.g, GOLD.b, (1.0 - t) * (1.0 - t) * 0.95)
        var ppos: Vector2 = p["pos"]
        var pos := Vector2(ppos.x, ppos.y - POPUP_RISE * t - 8.0)
        var txt := str(int(p["n"]))
        var w: float = font.get_string_size(txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 14).x
        draw_string(font, pos + Vector2(-w * 0.5, 0.0), txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 14, col)


func _draw_events() -> void:
    var evs: Variant = host.get("last_events")
    if evs == null:
        return
    var cur: Array[String] = evs
    if cur.is_empty():
        return
    var tail: Array[String] = cur.slice(maxi(0, cur.size() - 2))  # the old _update_hud showed the last 2
    var txt: String = "  ·  ".join(tail)
    # B2 2026-09-30: ring overflow is surfaced, never silent — game.gd
    # _on_water_event tallies every drop-oldest in event_dropped and the
    # strip shows the count so a reader can tell a burst was clipped.
    var dropped: Variant = host.get("event_dropped")
    if dropped != null and int(dropped) > 0:
        txt += "  ·  +%d dropped" % int(dropped)
    draw_string(ThemeDB.fallback_font, EVENT_POS, txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 12, Color(0.55, 0.6, 0.66, 0.75))


func _draw_hint() -> void:
    # The one-frame hint channel, byte-moved from game.gd _update_hud: draw
    # the hint produced this frame, then clear it so a stale hint never
    # lingers once the shepherd walks away (game.gd _update_hints refills it
    # every frame while the context holds). This is the only host state the
    # HUD writes — HUD channel state, never sim state.
    var hint: String = String(host.get("hint_text"))
    if hint == "":
        return
    draw_string(ThemeDB.fallback_font, HINT_POS, hint, HORIZONTAL_ALIGNMENT_LEFT, -1, 13, Color(0.82, 0.86, 0.9, 0.95))
    host.set("hint_text", "")


# ----------------------------------------------------------------- helpers ----

func _panel(rect: Rect2) -> void:
    # Chamfered dark plate: an octagon fill + thin outline (elegant without
    # images, themes, or styleboxes — pure _draw geometry, the mission's law).
    var c := 7.0
    var pts := PackedVector2Array([
        Vector2(rect.position.x + c, rect.position.y),
        Vector2(rect.end.x - c, rect.position.y),
        Vector2(rect.end.x, rect.position.y + c),
        Vector2(rect.end.x, rect.end.y - c),
        Vector2(rect.end.x - c, rect.end.y),
        Vector2(rect.position.x + c, rect.end.y),
        Vector2(rect.position.x, rect.end.y - c),
        Vector2(rect.position.x, rect.position.y + c),
    ])
    draw_colored_polygon(pts, PANEL_BG)
    var outline := PackedVector2Array()
    for p: Vector2 in pts:
        outline.append(p)
    outline.append(pts[0])
    draw_polyline(outline, PANEL_EDGE, 1.0, false)


func _wrap2(text: String, max_chars: int) -> Array[String]:
    # Deterministic greedy word wrap to at most two lines; anything that does
    # not fit becomes a trailing ellipsis. Pure text function: no RNG, no
    # clock, same output for same bytes. Byte-run fix 2026-09-30 (hud_probe
    # FAIL "wrap long is 2 lines" → isolated wrap_probe): the candidate was
    # built as `line if line == "" else line + " " + w` — the empty case
    # assigned the EMPTY line, so the first word never landed and the wrap
    # returned [""] for every input. The empty case must assign `w`.
    var words: PackedStringArray = text.split(" ")
    var lines: Array[String] = []
    var overflow := false
    var line := ""
    for w in words:
        var cand: String = w if line == "" else line + " " + w
        if cand.length() <= max_chars:
            line = cand
            continue
        if lines.size() < 2 and line != "":
            lines.append(line)
            line = w
            continue
        overflow = true  # nowhere left to wrap onto: the word is dropped
    if lines.size() < 2:
        if line != "":
            lines.append(line)
    elif line != "":
        # Byte-run fix 2026-09-30 (hud_probe FAIL "wrap long is 2 lines"):
        # words that kept fitting `line` AFTER the second line was closed
        # were silently discarded without the ellipsis mark — the overflow
        # flag only fired on the drop-word branch. Any non-empty leftover
        # past two lines IS overflow.
        overflow = true
    if lines.is_empty():
        lines.append("")
    if overflow:
        var last: String = lines[lines.size() - 1]
        if last.length() >= max_chars:
            last = last.substr(0, max_chars - 1)
        lines[lines.size() - 1] = last + "…"
    return lines
