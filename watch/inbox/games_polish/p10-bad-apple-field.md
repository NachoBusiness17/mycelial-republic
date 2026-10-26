## AUDIT: `bad_apple_field.html` (read-only; no files touched)

**Path note:** `dashboard/static/games/bad_apple_field.html` **does not exist**. The real file is **`dashboard/static/bad_apple_field.html`** (281,186 B, 263 lines) — audited below. Byte-identical copies: `site/dist/games/bad_apple_field.html` (built via `site/build.py:33`) and frozen `dist_audit/nacho_business_audit_20260912T214050Z/dashboard/static/bad_apple_field.html`. Served as `/static/bad_apple_field.html`. Sibling reference: falsifier harness `watch/PURPLE_HARVEST_B5_harness_20260906.mjs`.

### Findings

**Presentation**
- **P1 — ledger strip `.tot` flicker bug.** `dashboard/static/bad_apple_field.html:182` — `while(ledgerEl.children.length>8)ledgerEl.removeChild(ledgerEl.firstChild)` counts the `.tot` line (appended by `updateLedgerTotal`, :185–189, refreshed every 2 s via :260) as a child. After ~8 appends `.tot` becomes `firstChild` and is **evicted mid-playback**, recreated at the end ≤2 s later → the "N rows total" line flaps, and the cap "8" means only **7 frame rows** ever show despite `#ledger` styling a strip (:14–15).
- **P2 — non-integer upscale.** Canvas `width="480"` (:24) stretched to `min(96vw,900px)` (:9) = up to **1.875×** with `image-rendering:pixelated` — pixel columns alternate 1px/2px, softening the 1-bit aesthetic at common widths.
- Strengths: errbanner fixture complete (:20–21, matches `watch/inbox/error_banner_MAP_20260913.md:15`), live falsifier strip (:211–233), provenance/honesty footer (:29), gold-highlighted F A/B hint (:23).

**Performance (the 281 KB asset)**
- **F1 — first paint blocked by the selftest.** `selftest()` runs **before** `draw(0)` and before script end (:256): a 300-render sweep (:224) + 5 probes × (5 renders + 3× `meanAbsDiff` over 691,200 B + 2 hashes) ≈ **325 renders + ~15 full-buffer MAD passes ≈ ~1–1.7 s of synchronous main-thread work** → the entire page (281 KB parse + frame decode + worst workload) lands before any paint. Biggest single cost in the file.
- **F2 — the large asset is hashed twice per frame.** `draw()` computes `var h=FIELD.fnv1a32Bytes(DATA,CW*CH*4)` at :193 — **`h` is never used**; `ledgerRow()` recomputes the identical 691,200-B pass at :174. Redundant ≈ **20.7 MB/s of fnv1a32 at 30 fps (~0.35–0.7 ms/frame)** against the page's own "budget 8ms" claim (:206).
- **F3 — HUD rebuilt every frame.** :199 → `hud()` (:201–208): `innerHTML` reparse + `median(perfWin.slice())` (alloc+sort of 120) ~30×/s, even though values are stable.
- **F4 — dead DOM query per frame.** :183 `var total=ledgerEl.querySelector('.tot')||null;` — assigned, never read, runs every drawn frame.
- **F5 — double decode of the 181,766-byte payload.** `pxCheck()` (:160) runs `b64dec(BA.px)` **again** at boot; `decodeFrames` already decoded it at :49 (extra ~242 KB string walk + 181 KB alloc). `decodeCheck` is consumed externally by `watch/PURPLE_HARVEST_B5_harness_20260906.mjs:64`.
- **F6 (flag only):** 281 KB inline script re-parsed every load — size fix = server gzip (page's "no network" design at :32 rules out externalizing without a rewrite).
- **F7 (flag only — do not "fix"):** `LEDGER` grows unbounded (:176) **by declared design** (:188 "full log in memory", :230 "never spliced"; harness checks `4b/4g` assert contiguous ids). ~30 objects/s ≈ 16 MB/hour idle-open. Any cap breaks the page's honesty claim.
- **F8:** rAF catch-up is single-step with `dt≤100` (:245–252): under sustained slow frames `acc` grows unbounded (one `-=step` per tick) — backlog drains only ~0.6 ms/tick after recovery. Minor for a 40 s loop.

**Interactivity**
- **I1 — keyboard-only, zero pointer handlers** (:235–241). No click-to-pause on canvas, no scrub/progress bar, no buttons. Touch users get auto-play (`playing=true`, :172) but **cannot pause, seek, reseed, or A/B** — `#keys` (:26) documents keys only.
- Strengths: Space/arrow `preventDefault` (:236,:239–240) prevent scroll-steal; window-level keydown needs no focus.
- Minor: no `aria-label`