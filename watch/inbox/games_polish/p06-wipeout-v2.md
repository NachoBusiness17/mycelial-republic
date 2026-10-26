## Audit — `dashboard/static/wipeout_v2.html` (read-only)

Note: the requested path `dashboard/static/games/wipeout_v2.html` does not exist; the live file is `dashboard/static/wipeout_v2.html` (byte-identical to `site/dist/games/wipeout_v2.html`; `dist_audit/…/dashboard/static/wipeout_v2.html` is a differing older snapshot). Audited the live copy.

**Music coupling** — strongest axis, but one promise is fake. Real: measured BPM autocorrelation → world clock (`analyze` :236–244, `bpm = uBPM*iTime/60` :170), RMS→speed (:171, `uEnergy=eAvg*3` :280), bass→amber wash (:222). Broken: menu promises "the drops push the rush" (:30–31) but there is **no drop/beat detection anywhere** — energy is a heavily smoothed scalar (`eAvg*.8+e*.2`, :275) that just sits high on loud EDM. Track seed is filename **length** only: `uSeed=(f.length*7919)%1000/100` (:282) — 4 tracks ⇒ 4 fixed seeds, collision-prone, "song hash" claim is false.

**Juice** — fog/fresnel/glow exist in-shader (:196–221) but there is **zero beat- or drop-synced punch**: no flash, no FOV kick, no shake. HUD `SPEED` (:284) shows `2*(1+eAvg*3)` — omits BPM entirely, so it doesn't track actual world speed (which is `2*(bpm/60)*(1+e*.8)` units/s).

**Difficulty** — none. No fail state, no collision check at the camera, `DIST` (:285) is purely elapsed-time × BPM — a foregone number, no skill expression. `#end` / "RUN COMPLETE" (:45) is **dead HTML — never shown by any JS**; `srcNode.loop=true` (:260) also means song end never fires.

**Onboarding** — good menu/status flow (:30–36, :251–256), but HUD line :43 says "←/→ steer the camera" while **no keydown listener exists anywhere in the file** — the one advertised control does nothing. Track clicks are one-shot (`onclick=null`, :249); only escape is full reload (:45).

---

## ONE highest-value patch — **"DROP RUSH"** (delivers the advertised but missing feature)

Touches music coupling (arrangement-level drop detection), juice (FOV kick + amber surge + HUD badge), difficulty (+45% speed on drops), onboarding (visible DROP▲ RUSH teaches the coupling). 7 exact insertions, no rewrites.

**1. Shader uniforms — after line 71 (`uniform float uSeed;…`):**
```glsl
uniform float uRush;   // detected drop window — the rush the menu promises
```

**2. Speed surge — after line 176 (`speed*=2.;`), before line 177 (`ro=vec3(...)`):**
```glsl
    speed *= 1.+uRush*.45;
```

**3. FOV kick — replace line 183:**
```glsl
// OLD: rd = (o=mat3(x,cross(z,x),z))*normalize(rs=vec3(uv,.5-mix(.4,.1,trnd.x+rnd.y*.03)));
rd = (o=mat3(x,cross(z,x),z))*normalize(rs=vec3(uv*(1.-uRush*.15),.5-mix(.4,.1,trnd.x+rnd.y*.03)));
```

**4. Amber surge — after line 222 (`col += vec3(.91,.71,.35)*uBass*.12;`):**
```glsl
    col += vec3(.91,.71,.35)*uRush*.22;   // the drop washes the frame amber
```

**5. HUD badge — after line 43 (inside `#hud`, before its closing `</div>`):**
```html
  <span id="rush" style="color:#ff9a3c;font-weight:bold;opacity:0">DROP▲ RUSH</span>
```

**6. JS — line 263, add `'uRush'` to the uniform list:**
```js
for(const n of ['iResolution','iTime','uBPM','uEnergy','uBass','uSeed','uRush'])U[n]=gl.getUniformLocation(pr,n);
```

**7. JS in `tick` — after line 269 (`let eAvg=0,bAvg=0;`) add state; after line 275 (smoothing) add detection; replace line 284 (HUD speed):**
```js
  let eAvg=0,bAvg=0,eSlow=.2,rush=0;
  function tick(){
    if(!playing)return;
    if(analyzer){analyzer.getByteFrequencyData(freq);
      let e=0;for(let i=0;i<freq.length;i++)e+=freq[i];e/=(freq.length*255);
      let bs=0;for(let i=0;i<8;i++)bs+=freq[i];bs/=(8*255);
      eAvg=eAvg*.8+e*.2;bAvg=bAvg*.8+bs*.2;
      eSlow=eSlow*.998+e*.002;
      if(e>eSlow*1.22&&e>.12)rush=1; else rush*=.98;}
    gl.useProgram(pr);
    gl.uniform3f(U.iResolution,cv.width,cv.height,1);
    gl.uniform1f(U.iTime,(performance.now()-started)/1000);
    gl.uniform1f(U.uBPM,bpmMeasured);
    gl.uniform1f(U.uEnergy,eAvg*3);
    gl.uniform1f(U.uBass,bAvg);
    gl.uniform1f(U.uSeed,(f.length*7919)%10