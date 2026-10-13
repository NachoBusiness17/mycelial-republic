extends Node2D
## Juice — V5 2026-09-30 (feel pass; the operator's "make it FEEL great":
## "the pitch a stranger FEELS in the first 10 seconds"). V4 gave the slice
## four feels; V5 tunes them per SEVERITY and finishes the two moments a
## stranger actually meets: the event ladder and the win.
##   1. SCREEN SHAKE, TIERED BY EVENT SEVERITY (fracture > boil > gate — the
##      mission's ladder): a Camera2D pinned at the viewport center takes a
##      tiny offset that decays over the event's frame budget. Direction
##      comes from the hash -> 64-entry sine-table idiom
##      (water_particles.gd), never RandomNumberGenerator; every shake is
##      replayable from its frame count.
##   2. VICTORY SEQUENCE on WIN (the mission's four beats, all pure
##      functions of the post-win clock): THE WATER RISES (a waved flood
##      line climbs the lower third over 3 s and keeps lapping), THE SCREEN
##      WARMS (an amber wash fades in over the win panel), a "SUMMIT"
##      banner drops in with an ease-out-back overshoot, and the score
##      COUNTS UP inside the HUD win label (hud.gd owns that counter — its
##      own post-win clock, the same instrument as this one). The V4 crown
##      flash (burst + standing pulse) still opens the sequence.
##   3. PROCEDURAL AUDIO PER EVENT TYPE (not just the win chord): the boil
##      is a HISS (differentiated white noise, hash(i) — zero RNG), the
##      fracture a LOW CRACK (150->36 Hz sweep under a 120 ms grit burst),
##      the gate a soft tick, a STARVED junction a descending "denied" womp,
##      and the win keeps the C-major chord (C5/E5/G5, 1.1 s). Phase and
##      noise advance by pushed frame index against the server mix rate;
##      nothing samples the clock, nothing is random. Headless: the dummy
##      driver consumes nothing, the ring buffer fills once and the queue
##      parks — silence, never an error.
##   4. TENSION VIGNETTE — a radial GradientTexture2D (pure code, no image
##      file) fades in while crown volume >= 3: the win is one boil away.
##      Fades back out if the crown drops below 3.
##
## Event source: the graph's water_event signal, emitted by game.gd at every
## event append (AJ4 2026-09-30) — sovereign ticks, server broadcasts, and
## player verbs. Boil strings: sovereign "You boil 1 unit at spring; it
## rises." (game.gd _try_boil) and authoritative "ada boils 1 at spring; it
## rises." (server/world.py _apply). The authority is untouched: this layer
## reads graph/pools/won and mutates nothing of the sim.
##
## CLOCK LAW: no wall clock anywhere (the W1 law, game.gd sim_time receipt).
## This clock tracks host.sim_time frame for frame until the win; game.gd
## freezes sim_time the frame `won` flips (its _process early-returns), so
## after the win the clock keeps accumulating delta — the same instrument
## sim_time itself is (game.gd: `sim_time += delta`) — because a frozen clock
## would freeze the win celebration on its first beat.

const VIEW := Vector2(1152.0, 648.0)  # project.godot viewport
const CAM_CENTER := Vector2(576.0, 324.0)  # pinned center: the view is the identity when idle

# Shake, TIERED BY SEVERITY (the mission's ladder: fracture > boil > gate).
# V4 had one size (3 px / 10 frames); V5 scales amplitude AND frame budget
# per event class so a stranger's hand learns the ladder through the mouse.
const SHAKE_GATE := Vector2(1.2, 6)     # junction passes/sill — a settle tick
const SHAKE_STARVE := Vector2(2.2, 8)   # junction STARVED — denial, mid tier
const SHAKE_BOIL := Vector2(3.0, 10)    # the V4 boil shake, byte-kept
const SHAKE_FRACTURE := Vector2(7.0, 22)  # pipe bursts — the mountain moves

# Crown flash: burst + standing pulse (crown ring grammar: game.gd _draw "crown"
# draws its fill arc at radius 30 starting at -PI/2 — mirrored here).
const WIN_FLASH_S := 0.8
const PULSE_HZ := 5.0    # standing pulse frequency once won

# Victory sequence (feature 2): all times are offsets of the post-win clock.
const WIN_WARM_COL := Color(1.0, 0.72, 0.38)  # amber wash over the win panel
const WIN_WARM_MAX := 0.17     # wash alpha at full warmth
const WIN_WARM_S := 1.4        # seconds fading to full warmth
const WIN_WATER_TOP := 430.0   # final flood-line y (the lower third)
const WIN_WATER_DELAY := 0.3   # water starts just after the burst opens
const WIN_WATER_S := 3.0       # seconds the flood line takes to climb
const WIN_WATER_COL := Color(0.22, 0.50, 0.78, 0.85)
const WIN_CREST_COL := Color(0.62, 0.84, 0.96, 0.9)
const BANNER_DELAY := 0.5      # SUMMIT drops after the water starts
const BANNER_S := 0.8          # drop-in duration (ease-out-back overshoot)
const BANNER_Y := 118.0        # settled baseline, clear of the crown ring
const BANNER_COL := Color(0.98, 0.86, 0.55)

# Vignette: "subtle ... when crown is >= 3 (the tension cue)."
const VIGNETTE_CROWN := 3
const VIGNETTE_FADE := 0.5  # seconds for a full fade in or out
const VIGNETTE_MAX := 0.75  # modulate alpha at crown 3; 1.0 at crown 4 (won)

# Synthesis: fixed frequencies, fixed envelopes, frame-indexed phase.
const BLIP_S := 0.09
const GATE_HZ := 392.0          # soft tick under every clean junction pass
const GATE_AMP := 0.22
const HISS_S := 0.5             # the boil reads as steam, not a blip (V5)
const HISS_AMP := 0.38
const CRACK_F0 := 150.0         # fracture: a low sweep...
const CRACK_F1 := 36.0
const CRACK_S := 0.5
const CRACK_AMP := 0.55
const GRIT_S := 0.12            # ...under a short grit burst of the same hiss
const GRIT_AMP := 0.5
const DENY_F0 := 220.0          # STARVED: a descending "denied" womp
const DENY_F1 := 70.0
const DENY_S := 0.22
const DENY_AMP := 0.4
const CHORD_HZ := [523.25, 659.25, 783.99]  # C5, E5, G5
const CHORD_S := 1.1
const CHORD_AMP := 0.32
const QUEUE_CAP_S := 1.0  # never let a stalled device grow the queue unbounded

var host: Node = null             # game.gd: graph, pools, last_events, won, sim_time
var graph: Node = null            # systems/water_graph.gd instance (read-only)
var pools: Dictionary = {}        # node_name -> Vector2 board position
var cam: Camera2D = null
var flash: FlashCanvas = null     # the layer-2 canvas that beats the win panel
var gen: AudioStreamGenerator = null
var playback: AudioStreamGeneratorPlayback = null  # the push handle (4.3 API: buffer methods live here, not on the generator)
var audio_player: AudioStreamPlayer = null
var mix_rate := 44100
var audio_queue := PackedVector2Array()
var vig_tex: GradientTexture2D = null
var sine: Array[float] = []       # 64-entry table (water_particles.gd idiom)

var clock := 0.0                  # the CLOCK LAW clock above
var was_won := false
var win_flash_t := 0.0
var vig_alpha := 0.0
var shake_left := 0
var shake_frames := int(SHAKE_BOIL.y)  # the firing event's frame budget
var shake_amp := SHAKE_BOIL.x          # and amplitude (px at fire)
var shake_id := 0                 # deterministic direction seed per shake


## game.gd calls this right after instantiation, before add_child() (the same
## contract as water_particles.bind; graph + pools exist by end of _build_water).
## Node-building is deferred to _ready(): the camera's make_current() and the
## player's play() both error outside the scene tree (byte-run 2026-09-30,
## headless smoke 60f), and bind() runs pre-add_child by contract.
func bind(host_ref: Node) -> void:
    host = host_ref
    graph = host.get("graph")
    pools = host.get("pools")
    # AJ4 2026-09-30: boil events arrive on the graph's water_event signal
    # (game.gd _push_event emits at every append) — the old count-cursor over
    # the 6-slot feed went blind once the feed saturated (receipt
    # AJ4_PLAYTEST.md).
    graph.connect("water_event", _on_event)


func _ready() -> void:
    _build_camera()
    _build_audio()
    _build_vignette()
    _build_flash()


func _init() -> void:
    for i in 64:
        sine.append(sin(TAU * float(i) / 64.0))


func _process(delta: float) -> void:
    if host == null:
        return
    var now_won := bool(host.get("won"))
    if now_won and not was_won:
        _fire_win()
        win_flash_t = WIN_FLASH_S
    was_won = now_won
    # CLOCK LAW: track sim_time until the freeze, then keep the delta
    # accumulator running (see header) so the celebration animates.
    if now_won:
        clock += delta
    else:
        clock = float(host.get("sim_time"))
    _step_shake()
    win_flash_t = maxf(win_flash_t - delta, 0.0)
    # Tension vignette: ramp toward the crown-level target, both directions.
    var crown_v: int = graph.volume("crown")
    var target := 0.0
    if crown_v >= VIGNETTE_CROWN:
        target = VIGNETTE_MAX + (1.0 - VIGNETTE_MAX) * clampf(float(crown_v - VIGNETTE_CROWN), 0.0, 1.0)
    vig_alpha = move_toward(vig_alpha, target, delta / VIGNETTE_FADE)
    _push_audio()
    queue_redraw()
    if flash != null:
        flash.queue_redraw()


func _draw() -> void:
    # World canvas: only the vignette (added before the HUD layer in game.gd,
    # so it dims the board but never the HUD text).
    if vig_tex != null and vig_alpha > 0.004:
        draw_texture_rect(vig_tex, Rect2(Vector2.ZERO, VIEW), false, Color(1.0, 1.0, 1.0, vig_alpha))


## The win flash canvas (layer 2, over the HUD) calls into this; crown ring
## geometry mirrors game.gd _draw "crown": radius 30.0, arcs start at -PI/2.
## V5: the canvas also carries the victory sequence (wash, flood line, SUMMIT
## banner) — it must sit on layer 2 because the HUD win panel is a 0.88-alpha
## ColorRect that would swallow any world-canvas celebration under it.
func draw_win_flash(node: Node2D) -> void:
    var cpos_v: Variant = pools.get("crown")
    if cpos_v == null:
        return
    var cpos: Vector2 = cpos_v
    var now_won := bool(host.get("won"))
    if now_won:
        # Standing pulse: the frozen fill ring breathes — width and alpha.
        var pulse: float = 0.5 + 0.5 * sin(clock * PULSE_HZ)
        node.draw_arc(cpos, 30.0, -PI / 2, -PI / 2 + TAU, 40, Color(0.75, 0.95, 1.0, 0.30 + 0.45 * pulse), 4.0 + 2.5 * pulse)
        node.draw_arc(cpos, 38.0 + 5.0 * pulse, -PI / 2, -PI / 2 + TAU, 40, Color(0.55, 0.85, 0.95, 0.10 + 0.25 * pulse), 1.5)
        _draw_warm_wash(node)
        _draw_flood_line(node)
        _draw_summit_banner(node)
    if win_flash_t > 0.0:
        # One-shot burst off the win: a ring leaving the crown, quadratic fade.
        var ft: float = 1.0 - win_flash_t / WIN_FLASH_S
        var col := Color(0.85, 0.97, 1.0, (1.0 - ft) * (1.0 - ft) * 0.9)
        node.draw_arc(cpos, 30.0 + 75.0 * ft, -PI / 2, -PI / 2 + TAU, 48, col, 3.0)


# --------------------------------------------- V5 victory sequence beats ----
# Every beat is a pure function of `clock` (the post-win accumulator, header
# CLOCK LAW): same clock, same pixels, frame-replayable.

func _draw_warm_wash(node: Node2D) -> void:
    # "The screen warms": an amber wash fades in over the dark win panel and
    # everything under this canvas — the win reads as sunlight, not night.
    var a: float = WIN_WARM_MAX * clampf(clock / WIN_WARM_S, 0.0, 1.0)
    if a > 0.004:
        node.draw_rect(Rect2(Vector2.ZERO, VIEW), Color(WIN_WARM_COL.r, WIN_WARM_COL.g, WIN_WARM_COL.b, a), true)


func _draw_flood_line(node: Node2D) -> void:
    # "The water rises": a waved flood line climbs from the bottom edge to the
    # lower third (cubic ease-out) and then keeps lapping — the mountain's
    # water, delivered. Surface = two sine terms, phases from `clock` only.
    var t: float = clampf((clock - WIN_WATER_DELAY) / WIN_WATER_S, 0.0, 1.0)
    if t <= 0.0:
        return
    var ease: float = 1.0 - pow(1.0 - t, 3.0)
    var surf_y: float = VIEW.y - (VIEW.y - WIN_WATER_TOP) * ease
    var surf := PackedVector2Array()
    var steps := 48
    for k in steps + 1:
        var x := VIEW.x * float(k) / float(steps)
        var y := surf_y + 5.0 * sin(x * 0.020 + clock * 2.2) + 2.5 * sin(x * 0.043 - clock * 1.4)
        surf.append(Vector2(x, y))
    var poly := PackedVector2Array()
    poly.append_array(surf)
    poly.append(Vector2(VIEW.x, VIEW.y))
    poly.append(Vector2(0.0, VIEW.y))
    node.draw_colored_polygon(poly, WIN_WATER_COL)
    node.draw_polyline(surf, WIN_CREST_COL, 1.8, false)


func _draw_summit_banner(node: Node2D) -> void:
    # The "SUMMIT" banner: drops from above the frame with an ease-out-back
    # overshoot (it settles with one bounce), alpha riding the same ramp; a
    # thin rule grows underneath to the text width once it settles.
    var t: float = clampf((clock - BANNER_DELAY) / BANNER_S, 0.0, 1.0)
    if t <= 0.0:
        return
    var c1 := 1.70158  # ease-out-back constants (the standard pen overshoot)
    var c3 := c1 + 1.0
    var e: float = 1.0 + c3 * pow(t - 1.0, 3.0) + c1 * pow(t - 1.0, 2.0)
    var y: float = lerpf(-80.0, BANNER_Y, e)
    var a: float = clampf(t * 2.0, 0.0, 1.0)
    var font := ThemeDB.fallback_font
    var txt := "SUMMIT"
    var w: float = font.get_string_size(txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 68).x
    var x0 := VIEW.x * 0.5 - w * 0.5
    node.draw_string(font, Vector2(x0, y), txt, HORIZONTAL_ALIGNMENT_LEFT, -1, 68, Color(BANNER_COL.r, BANNER_COL.g, BANNER_COL.b, a))
    var rule_w := w * clampf((t - 0.4) / 0.6, 0.0, 1.0)
    if rule_w > 1.0:
        node.draw_line(Vector2(VIEW.x * 0.5 - rule_w * 0.5, y + 14.0), Vector2(VIEW.x * 0.5 + rule_w * 0.5, y + 14.0), Color(BANNER_COL.r, BANNER_COL.g, BANNER_COL.b, a * 0.7), 2.0)


# ------------------------------------------------------------------ shake ----

func _build_camera() -> void:
    # Pinned at the viewport center with the default zoom 1: the canvas
    # transform is the identity while idle, so enabling this camera changes
    # nothing on screen until a boil offsets it (and headless is inert).
    cam = Camera2D.new()
    cam.name = "ShakeCamera"
    cam.anchor_mode = Camera2D.ANCHOR_MODE_DRAG_CENTER
    cam.position = CAM_CENTER
    add_child(cam)
    cam.make_current()


func _fire_shake(tier: Vector2) -> void:
    # V5: the V4 single boil shake became a severity ladder. tier = (amp px,
    # frame budget); the direction seed still advances per shake so replay
    # stays byte-stable per sequence.
    shake_id += 1
    shake_amp = tier.x
    shake_frames = int(tier.y)
    shake_left = shake_frames


func _fire_boil() -> void:
    _fire_shake(SHAKE_BOIL)
    _enqueue(_hiss(HISS_S, HISS_AMP))


func _fire_gate() -> void:
    _fire_shake(SHAKE_GATE)
    _enqueue(_tone([GATE_HZ], BLIP_S, GATE_AMP))


func _fire_starve() -> void:
    _fire_shake(SHAKE_STARVE)
    _enqueue(_sweep(DENY_F0, DENY_F1, DENY_S, DENY_AMP))


func _fire_fracture() -> void:
    _fire_shake(SHAKE_FRACTURE)
    _enqueue(_crack())


func _step_shake() -> void:
    if shake_left <= 0:
        cam.position = CAM_CENTER
        return
    # Magnitude decays linearly across the firing event's frame budget; the
    # direction rotates each frame through the sine table keyed on (shake_id,
    # frames left) — deterministic per shake sequence, zero RNG.
    var t: float = float(shake_left) / float(shake_frames)
    var ang: float = TAU * _unit(shake_id * 64 + shake_left)
    cam.position = CAM_CENTER + Vector2(cos(ang), sin(ang)) * (shake_amp * t)
    shake_left -= 1


# ------------------------------------------------------------------ audio ----

func _build_audio() -> void:
    # Headless law (V4 mission: "the audio won't play headless but must not
    # error"): under --headless the dummy driver has no sink, and a generator
    # player left live at exit trips Godot 4.3's ObjectDB leak WARNING
    # (byte-run bisect 2026-09-30: HEAD at 300f headless leaks with the audio
    # build, banner-only without it). No device -> no player -> banner-only
    # smoke stays true; the synth path itself never errors on a real device.
    if DisplayServer.get_name() == "headless":
        return
    audio_player = AudioStreamPlayer.new()
    audio_player.name = "Synth"
    gen = AudioStreamGenerator.new()
    mix_rate = int(AudioServer.get_mix_rate())  # match the driver, no pitch drift
    gen.mix_rate = mix_rate
    gen.buffer_length = 0.5
    audio_player.stream = gen
    add_child(audio_player)
    audio_player.play()
    # The 4.3 law: frame push/poll lives on the playback handle, taken after
    # play() (get_stream_playback returns null until the player is playing).
    playback = audio_player.get_stream_playback() as AudioStreamGeneratorPlayback


func _fire_win() -> void:
    _enqueue(_tone(CHORD_HZ, CHORD_S, CHORD_AMP))


func _tone(freqs: Array, dur: float, amp: float) -> PackedVector2Array:
    # Pure synthesis: sum of sines, phase from the frame index only, envelope
    # sin(PI * t / dur) so the first and last samples are 0 (no click). Equal
    # parts per frequency so the chord balances; stereo frames carry the same
    # sample both channels.
    var n := int(dur * float(mix_rate))
    var frames := PackedVector2Array()
    frames.resize(n)
    for i in n:
        var t := float(i) / float(mix_rate)
        var env := sin(PI * t / dur)
        var s := 0.0
        for f in freqs:
            s += sin(TAU * float(f) * t)
        s = s * amp * env / float(freqs.size())
        frames[i] = Vector2(s, s)
    return frames


func _hiss(dur: float, amp: float) -> PackedVector2Array:
    # V5 boil voice: white-ish noise from hash(i) (zero RNG — the _unit law,
    # continuous-valued instead of table-quantized so it reads as steam, not a
    # buzz) through a one-pole differentiator for a bright top. Same
    # sin(PI * t / dur) envelope: no click at either end.
    var n := int(dur * float(mix_rate))
    var frames := PackedVector2Array()
    frames.resize(n)
    var prev := 0.0
    for i in n:
        var x := float(absi(hash(i * 7349 + 11)) % 2001) / 1000.0 - 1.0
        var s := (x - prev) * 0.5  # high-pass: hiss, not rumble
        prev = x
        var t := float(i) / float(mix_rate)
        var v := s * amp * sin(PI * t / dur)
        frames[i] = Vector2(v, v)
    return frames


func _sweep(f0: float, f1: float, dur: float, amp: float) -> PackedVector2Array:
    # V5: instantaneous frequency glides f0 -> f1; phase is the integral of
    # the glide accumulated per frame (never re-derived from t, so the sweep
    # stays continuous at any mix rate). Same zero-click envelope.
    var n := int(dur * float(mix_rate))
    var frames := PackedVector2Array()
    frames.resize(n)
    var phase := 0.0
    for i in n:
        var t := float(i) / float(mix_rate)
        var f := lerpf(f0, f1, t / dur)
        phase += TAU * f / float(mix_rate)
        var s := sin(phase) * amp * sin(PI * t / dur)
        frames[i] = Vector2(s, s)
    return frames


func _crack() -> PackedVector2Array:
    # V5 fracture voice: the low sweep (150 -> 36 Hz, the mountain splitting)
    # summed with a 120 ms burst of the hiss voice (grit at the snap). Summed
    # in one pass so the two land together — a crack, not crack-then-hiss.
    var low := _sweep(CRACK_F0, CRACK_F1, CRACK_S, CRACK_AMP)
    var grit := _hiss(GRIT_S, GRIT_AMP)
    for i in mini(low.size(), grit.size()):
        var a: Vector2 = low[i]
        var b: Vector2 = grit[i]
        low[i] = Vector2(clampf(a.x + b.x, -1.0, 1.0), clampf(a.y + b.y, -1.0, 1.0))
    return low


func _enqueue(frames: PackedVector2Array) -> void:
    audio_queue.append_array(frames)
    # Cap: if the device stopped consuming (headless dummy driver), keep the
    # newest QUEUE_CAP_S of audio and drop the oldest overflow.
    var cap := int(QUEUE_CAP_S * float(mix_rate))
    if audio_queue.size() > cap:
        audio_queue = audio_queue.slice(audio_queue.size() - cap)


func _push_audio() -> void:
    # Fill whatever the driver freed with queued tone, then silence. With a
    # live device the queue streams out; headless, the buffer fills once and
    # get_frames_available() stays 0 — this becomes a no-op, never an error.
    if playback == null:
        return
    var fill := playback.get_frames_available()
    if fill <= 0:
        return
    var take := mini(fill, audio_queue.size())
    if take > 0:
        playback.push_buffer(audio_queue.slice(0, take))
        audio_queue = audio_queue.slice(take)
        fill -= take
    if fill > 0:
        var silence := PackedVector2Array()
        silence.resize(fill)  # packed resize default-fills with Vector2.ZERO
        playback.push_buffer(silence)


# -------------------------------------------------------------- vignette ----

func _build_vignette() -> void:
    # Radial gradient in code: transparent through mid-frame, dark at the rim.
    # fill_to is the right-edge mid in UV space, so corners (distance > radius)
    # clamp to full rim color — the classic vignette falloff.
    var grad := Gradient.new()
    grad.offsets = PackedFloat32Array([0.0, 0.5, 1.0])
    grad.colors = PackedColorArray([Color(0, 0, 0, 0), Color(0, 0, 0, 0), Color(0.02, 0.03, 0.06, 0.6)])
    vig_tex = GradientTexture2D.new()
    vig_tex.gradient = grad
    vig_tex.fill = GradientTexture2D.FILL_RADIAL
    vig_tex.fill_from = Vector2(0.5, 0.5)
    vig_tex.fill_to = Vector2(1.0, 0.5)
    vig_tex.width = int(VIEW.x)
    vig_tex.height = int(VIEW.y)


# ------------------------------------------------------------------ flash ----

func _build_flash() -> void:
    # CanvasLayer at layer 2: above the HUD (default layer 1) so the win
    # panel never covers the celebration. Screen coords == board coords while
    # the camera is the identity (and a boil shake is <= 3 px for <= 10
    # frames, which never coincides with a win).
    var layer := CanvasLayer.new()
    layer.name = "WinFlashLayer"
    layer.layer = 2
    flash = FlashCanvas.new()
    flash.name = "WinFlash"
    flash.back = self
    layer.add_child(flash)
    add_child(layer)


# ---------------------------------------------------------------- events ----

func _on_event(text: String) -> void:
    # V5 severity routing (fracture > boil > gate, the mission's ladder).
    # Grammars: "Pipe X FRACTURES (stress N): ..." / boil strings (both net
    # modes share the "; it rises." tail; the prefixes differ, You vs. <user>
    # boils) / "Junction X passes|sill reached|holds ..." / "Junction X
    # STARVED: ...". A "Siphon X breaks (intake dry)." rides the boil tier —
    # same severity class (a live route just died) though its sound is the
    # denial sweep, a shade softer than the crack.
    if text.begins_with("Pipe ") and text.contains(" FRACTURES"):
        _fire_fracture()
    elif text.begins_with("You boil") or text.contains(" boils 1 at "):
        _fire_boil()
    elif text.begins_with("Siphon ") and text.contains(" breaks (intake dry)"):
        _fire_shake(SHAKE_BOIL)
        _enqueue(_sweep(320.0, 90.0, DENY_S, 0.35))
    elif text.begins_with("Junction "):
        if text.contains(" STARVED:"):
            _fire_starve()
        else:
            _fire_gate()


# ------------------------------------------------------------- sine table ----

func _unit(seed: int) -> float:
    # Deterministic [0, 1] from an integer seed: hash(index) through the
    # table (water_particles.gd _unit; hash() of an int is stable).
    return 0.5 + 0.5 * sine[absi(hash(seed)) % 64]


class FlashCanvas extends Node2D:
    ## The layer-2 draw surface for the crown flash; all geometry lives in the
    ## owner (juice.gd draw_win_flash) so this stays a thin back-pointer.
    var back: Node2D = null

    func _draw() -> void:
        if back != null and is_instance_valid(back):
            back.draw_win_flash(self)
