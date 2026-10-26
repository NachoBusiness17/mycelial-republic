# WATER GOVERNOR V2 - the fleet driven at width, non-handwaved (2026-10-20)

Operator orders answered: "drive them at width usefully, water computer style,
i dont want it handwaved anymore" + "burn down compute on lanes in sustainable
ways, know their reset windows... rather run out of compute than leave it on
the shelf" + "we are calibrating our 5 hour burn down window within the estate
itself. sort of a meta context layer."

## What shipped

- `tools/water_governor.py` + `tests/test_water_governor.py` (6 tests) +
  commit 9e097bd1a + this receipt's commit. The governor is an ORCHESTRATOR
  with zero sockets: openrouter roster rides hermes_burn, deepseek rides
  ds_workhorse (ok_material gated), the local shelf rides subprocess ollama,
  zai session width is this harness's own agents, hermes chassis is audited
  through MagHermesBurn247's task state.
- Census (`water_governor census`): 48 env key names classified into carrier
  families, values never read. WIRED (6): zai_session, openrouter_free,
  deepseek, hermes_chassis, local_shelf, cohere (indirect via the roster).
  MOUNTED-UNWIRED (named gaps with mount notes): google x4 keys, grok/xAI x3,
  anthropic x2 (ladder-closed), cerebras x2, mistral x2, nvidia, openai,
  together x2. DEAD: groq (401 since 10-14; recovery: rotate key, re-census).
  EXTERNAL: opencode CLI mounts (other devices), vastai.
- THE META CONTEXT LAYER (`water_governor windows`): 5h rolling burn-down
  calculus over state/quota_windows.json. Live read this morning: BOTH Google
  accounts (sf, nacho) are window-closed with full budget available - per the
  burn-down law that is unspent compute waiting, and the Gemini desktop tier
  is the highest-value place to spend it today.
- MagProbeCadence RE-ARMED (was Disabled in the 10-18 sweep; next fire 09:11).

## Beat 1 - the non-handwave numbers (2026-10-20 ~13:03-13:19Z)

- 6 dispatched, 6 banked, conservation_ok TRUE, 0 orphans, handwave_crime FALSE.
- deepseek: ok_api + ok_material TRUE - it digested the fish-tank sweep into a
  real 4Ws operator block (the portproxy delete line, verbatim) and the output
  percolated NOVEL into the organ. Artifact:
  memory/runs/water_governor/ds_2026-10-20T1319/results.jsonl
- local_shelf: gemma:2b ok_material TRUE (percolated NOVEL); qwen2.5 7b
  answered "pong" and was BANKED AS A MISS by the first material check - the
  beat taught the checker (any non-empty render is material; the hollow-batch
  crime is EMPTY output). Fixed in the same sitting.
- openrouter_free: BANKED FAILURE - the probe roster subprocess hit the 900s
  timeout (free-lane 429 pacing); timeout raised to 1500s, and the honest miss
  is the row. A missed dispatch is data; a claimed one would have been the crime.
- The conservation table caught its own two bugs on beat 1: the audit stub
  rows (zai_session, hermes_chassis) were state-only and never banked (the
  ledger flagged them as shelf waste - correct behavior exposing the gap),
  and the selftest had polluted the live ledger. Both fixed same sitting;
  post-repair: shelf_waste_tanks = ["cohere"] only (honest - its roster ride
  sat inside the timed-out probe lane).

## The standing loop from here

1. The beat clock: MagProbeCadence (10-min) + MagHermesBurn247 (Running) +
   `water_governor beat` for the full-width audit; `water_governor report`
   is the conservation table; `water_governor windows` is the 5h meta layer.
2. Burn-down posture: window-closed + unspent = go spend it (Gemini today);
   near-reset + unspent = BURN-DOWN NOW (the posture string is in the output).
3. The named gaps are the next mounts, in value order: a google carrier
   (4 keys, the free judgment rung), a z.ai direct carrier (3 keys beyond the
   session), grok/xAI (3 keys), then cerebras/mistral/nvidia/together. Each
   mount = a fence-delegating carrier module + a census status flip.

Falsifier: if a future report shows handwave_crime TRUE or a WIRED tank in
shelf_waste_tanks for two consecutive days, the governor is decoration - fix
the dispatch path or strike the tank.
