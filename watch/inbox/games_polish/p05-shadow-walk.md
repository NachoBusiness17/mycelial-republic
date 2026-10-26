**File audited:** `dashboard/static/shadow_walk.html` (1,018 lines, 112,293 bytes). `dashboard/static/games/shadow_walk.html` does not exist — the only other copies are build artifacts (`site/dist/games/shadow_walk.html`, `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/shadow_walk.html`), which I did not audit.

## Juice

- **RUN OFF — the default mode — has zero audio.** `chime()` (`shadow_walk.html:286-300`) is only called from the run loop: warden correct `:409`, wrong `:421`, death `:468`, forge `:476`. `objectiveTick` (`:214-241`) fires `flash()` only — so anchor reaches (`:221`), doctrine pickups (`:238`), and THE ELEVENTH ROOM opening (`:230`) are silent. A first-time player who never presses R hears nothing, ever.
- **Milestone feedback is buried in telemetry.** `flash()` (`:813-814`) only appends to the HUD string at `:965`, and the HUD re-renders at 2 Hz (`:936`). "THE ELEVENTH ROOM OPENS" renders as ~1 line of gold text at the tail of a 4-line stats wall — no center banner, no screen-space event.
- **No low-runtime juice.** Fog drain (`:450-453`) is the game's core threat, but feedback is a text bar (`runtimeBar` `:492-495`) that only turns orange under 30 (`:957`). No vignette, pulse, or heartbeat. Death (`:466-473`) gets a chime + panel but no flash/shake/red wipe.
- **Wayfinding marks are 1–5 px.** Compass tick draws 3 rows (`:576-581`); doctrine diamonds are a 5-pixel cross (`:531-537`). The single most important navigation device is nearly invisible at 320×200.

## Difficulty

- **Core fairness bug: warden judgment is decoupled from the answer text.** `wardenQ` shuffles `order` and sets `correct: order.indexOf(0)` with `opts: order.map(j=>t.a[j])` (`:391-393`), but renders buttons from **`t.a` in original order** (`:396`) — `opts` is computed and never used. Since every template's correct answer is index 0 (`:381-388`), the button that *displays* the right answer is judged correct only when `order.indexOf(0)===0` ≈ **1/3 of the time**; a distractor wins the other 2/3. Wrong answers cost `w.t=12` (`:420`) while the standing-in-fog drain continues at 5/s (`:452`) — so honest players get punished ~twice as often as guessers. Keyboard path (`:738-741`) inherits the same indices.
- Fog economy itself is legible: 5/s moving, 2.2/s idle, +10/s on validated (`:451-449`), and `panelOpen` freezes the clock (`:445`) so reading is free. That part is well-tuned.
- Objective 1 auto-completes frame 1: `anchors[0]` is `WALK.SPAWN_B` (`:184`) and spawn teleports to `WALK.SPAWN_B` (`:165`), radius 6.25 (`:219`). Harmless, but "OBJECTIVE 1/5" ticks with no input.

## Onboarding

- **HUD teaches a wrong key.** Lens moved to **O** (`:743`, keys strip `:26`, help `:981`), but the HUD still prints `off (L)` (`:951`). Pressing L as instructed opens the lore log (`:744`).
- No first-run overlay — `:1008-1017` boots straight into `newRun()`; all guidance is behind H. First contact is the jargon wall at `:23` (useful OBJECTIVES span buried mid-sentence) plus a 12-binding key strip at `:26`.
- THE RUN — the actual game — is `runMode=false` by default (`:252`); entering it requires H → button (`:1004`) or knowing R.
- Pointer lock needs a **double**-click (`e.detail===2`, `:764`), documented only inside the hidden help panel.

---

## ONE highest-value polish patch

The warden judgment bug is the top pick: it is the difficulty/fairness defect at the center of the mode the game ships as, it is one line, and `w.pending.opts` already exists — the shuffle was half-wired and simply never reached the render.

**File:** `dashboard/static/shadow_walk.html`
**Exact insertion point:** line 396, inside `wardenQ` — the middle line of the `helpEl.innerHTML` assignment (between `:395` `<h2>…<p>'+t.q+'</p>'+` and `:397` the `.mut` footer).

**Replace (current, `:396`):**
```js
    t.a.map((x,i)=>'<button class="wopt" data-i="'+i+'">'+(i+1)+') '+x+'</button>').join('<br>')+
```

**With:**
```js
    w.pending.opts.map((x,i)=>'<button cla