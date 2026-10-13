# SKILLS — the discovery index

Machine-parseable blocks: one per engine, fields name/description/run/fails-when.
Harnesses and agents: index this file; do not crawl the directory.

## claritas
name: claritas
description: claritas — the canonical CLARITAS faces: system prompts distilled from the leaked frontier-lab system-prompt library (research/CL4R1T4S: Cla
run: python engines/claritas.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## cooker
name: cooker
description: cooker — fire the free-compute burn right after each provider's reset, by default (2026-09-24, operator: "we know how long we have until res
run: python engines/cooker.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## estate_atlas
name: estate_atlas
description: #!/usr/bin/env python3
run: python engines/estate_atlas.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## estate_smith_chart
name: estate_smith_chart
description: ESTATE SMITH CHART — health as |Gamma| coordinates, not prose.  Law (self-steal, 2026-09-21, from the pseudospectrum/Smith-chart wave):   A 
run: python engines/estate_smith_chart.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## flight_recorder
name: flight_recorder
description: FLIGHT RECORDER — every model call becomes one typed telemetry row.  Standalone stdlib module (no estate imports). Steal-shape rebuild of th
run: python engines/flight_recorder.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## key_law
name: key_law
description: key_law — the one loader and the audit (2026-09-23 night, KEY LAW implemented).  Law: one key, one canonical name, declared once in configs/
run: python engines/key_law.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## keys
name: keys
description: keys — the one door engines use for key lookups (law 7). Reads configs/keys.json first: an env var that is LIVE but undeclared is reported, 
run: python engines/keys.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## librarian_catalog
name: librarian_catalog
description: librarian_catalog — the record of the record (2026-09-23, operator: "we have no real record and a million files"). Sibling organ to libraria
run: python engines/librarian_catalog.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## lite_guard
name: lite_guard
description: LITE PACING GUARD — the pacing law made structural (2026-09-05).  Root failure (operator: "the lite subscription key is fucking me again"): 
run: python engines/lite_guard.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## model_bakeoff
name: model_bakeoff
description: model_bakeoff — 50 concurrent calls across the free model-lane wall (2026-09-23, operator: "call 50c of ten different models to test their o
run: python engines/model_bakeoff.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## phone_relay
name: phone_relay
description: phone_relay — approvals from the operator's phone, through the Mag DM.  Law (2026-09-24, operator GO): no estate gate may hold work hostage 
run: python engines/phone_relay.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## process_supervisor
name: process_supervisor
description: PROCESS SUPERVISOR — one-shot sub-agent processes, crash containment, file-mailbox steering.  Standalone stdlib module (no estate imports). 
run: python engines/process_supervisor.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## seed_init
name: seed_init
description: seed_init — lay down a fresh estate skeleton in a target folder (the salon's #1).  Usage:  python engines/seed_init.py <target-dir>  Creates
run: python engines/seed_init.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## spine_walk
name: spine_walk
description: #!/usr/bin/env python3
run: python engines/spine_walk.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## stealth_sweep
name: stealth_sweep
description: stealth_sweep — burn the free wall daily: live-fire OpenRouter's :free and :stealth models on a real scored chore, keep the winners (2026-09
run: python engines/stealth_sweep.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)

## task_wall
name: task_wall
description: task_wall — the standing concurrent task engine (2026-09-23, operator: "explode our throughput... test concurrency everywhere to touch the w
run: python engines/task_wall.py --help
fails-when: missing keys/config raises a named, readable error (never a traceback)
