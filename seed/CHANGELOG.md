# Changelog

## 3.3.0 repack (2026-09-25)
- seal hygiene: the builder purges and excludes __pycache__/*.pyc before sealing
  (bytecode bakes compile-time absolute paths; a08 caught 3 of 59 sealed rows shipping
  the author path inside the 3.3.0 zip) and now emits the zip itself from the sealed
  rows, so zip contents equal seal contents by construction

## 3.3.0 — 2026-09-25
- STACK.md: the harness, tiered (stdlib -> editor -> ollama -> FastAPI/SQLite ->
  Docker cage -> k3s), each with a when-you-need-it honesty marker; the framing:
  own your own surveillance state, turned inward — every meter points at your own
  machine, nothing phones home
- templates/: docker-compose cage (loopback-only ports, record dirs mounted on your
  disk) + api_server_example.py (the estate gateway shape rebuilt at minimum size)

## 3.2.0 — 2026-09-25
- the enhancement salon's convergent #1: engines/seed_init.py — one-command estate
  scaffolder (12-file skeleton, honest all-DARK first meter, next-commands printed)
- SKILLS.md: machine-parseable discovery index (one block per engine, name/description/
  run/fails-when) — harnesses index the file, never crawl the directory
- AGENTS.md v2: this file IS the load order (agent tools auto-load the method)

## 3.1.0 — 2026-09-25
- the discovery-window cook: 17 estate-mined items shipped by the full cast —
  laws-as-config (configs/law_registry.json + mode_budgets.json), process supervisor +
  flight recorder engines, receipt/cost/capability-gate/trust-bytes/campaign-discipline
  docs, activity trail, boot budget card, training spine templates
- spine_walk docstring scrubbed (the cook resurrected the author's path — the post-cook
  spot check caught it, which is why the check runs after every cook)

## 3.0.0 — 2026-09-25
- the self-steal diff answered — six missing pieces embedded: ACCOUNTS.md (2x signup
  playbook, $5 float rule), VSCODE.md (editor + free-models + opencode browser path),
  DATA_TIERS.md (T0-T3 — what may leave your disk), SALON.md (the portable decision
  instrument), MORNING_LOOP.md (the daily rhythm recipe), TOUR.md (estate → seed map)

## 2.2.0 — 2026-09-25
- item 4 DONE: task_wall + model_bakeoff read keys through the one door (keys.py)
- item 5: stranger-authored chores — configs/chores.json loads into the wall; example shipped
- item 8: self-citation sweep — docstrings point at shipped paths; grep 'law 15|@gmail|-m tools.|mag/*' CLEAN
- lane_supervisor exists in the estate (15-min probes, failover, phone escalation on orphan classes)

## 2.1.0 — 2026-09-25
- keys.py: the one door for lane engines (law 7); stealth_sweep wired through it
- tests/: stdlib unittest suite — cooker month-edge (the V1 crash), relay exact-token
  decisions (the 'deny'-approves bug), seal integrity
- honest meters: checkpoint organ is DARK on no evidence, never DELIVERING on nothing (law 4)
- versioning: SEED_VERSION + this changelog

## 2.0.0 — 2026-09-25
- build-book items 1-2: every engine boots cold (12 PASS / 2 readable / 0 crashes),
  LF seal passes stock sha256sum, walker ships (spine_walk.py), SETUP/LICENSE/
  verify_seal/keys-template/AGENTS.md, readable-failure guards everywhere

## 1.0.0 — 2026-09-24
- first seed: 11 laws + 12 engines; failed its own cold-boot audit (2 of 7 steps)
