# THE BREAKING PASS — dogfooding the night's builds (2026-09-07, post-dinner-shift)

Method: hostile-but-fair user against every surface the night shipped — pages, organs,
automation, ledger. Culture law: report what fails first.

## VERDICT: no true breaks in shipped code. 12 passes, 3 quirks, 1 seat-side lesson.

## PASSES (12)

1. nav.js syntax + render — both new room links live, zero console errors
2. Console page loads clean with the wiring
3. Dissector on EMPTY corpus — fails clean (empty report, no crash)
4. suno_zeitgeist on non-mirror text — verdict NOISE, density 0.0 (the instrument
   discriminates; it does not flatter)
5. kabuki cast rotation renders (6 personas, hashed order)
6. Grounding wave verify — PASS, 45 posts, tip intact
7. Airflow: run REFUSES without a logged prediction (the gate holds)
8. Airflow: margin puffs become outside-plume particles, fade gracefully, no NaN
9. Airflow: mid-run reset clean, no orphaned run state
10. Phase room: 10 violent energy sweeps (0↔3.4) — zero NaN particles, zero errors,
    lattice re-forms when the heat returns to zero
11. Tortoise re-run: chain tip unchanged → theme unchanged (deterministic on the
    record; the chain composes, exactly as designed)
12. ASR lane (200 on first fire, earlier) + grounding post (SUPPORTED)

## QUIRKS (v1 scope, not breaks)

1. **Airflow margin puffs**: clicking the canvas margin silently creates
   already-outside smoke. Harmless (fades as plume) — but v1 should either constrain
   puffs to the house or own it as a feature ("the yard exists").
2. **Airflow is mouse-only; phase has no keyboard** — the PLAY organ is
   pointer-shaped. WASD/keys ride with R2.
3. **Debug convention split**: airflow (classic script, globals visible) vs phase
   (module, needs __DBG). Probe hygiene cost the seat two misfires tonight. v1:
   every room exposes the same __DBG surface.

## SEAT-SIDE LESSON (the only real break was in the probe, not the build)

Playwright evaluate failed twice on module-scoped pages — the probe used classic-
script assumptions on a module page. The rooms are fine; the instrumentation wasn't
uniform. Recorded so the next dogfood pass doesn't re-learn it.
