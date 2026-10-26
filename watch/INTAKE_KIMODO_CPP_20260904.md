# INTAKE CARD — KIMODO.CPP: TEXT-TO-MOTION, LOCAL, GGML (bookmarks batch 1, item 3, 2026-09-04)

ITEM: x.com/Stefan_3D_AI/status/2091531753966240016 + parent 2091531702183350276 (2026-08-23, parent 105.9K views / 2,150 bookmarks). Claim (verbatim): "kimodo.cpp is live. NVIDIA's Kimodo, the best AI animation model right now, running natively on CPU or Vulkan." + "Type a sentence, get character animation, locally on your own machine." GGML/C++ port, GGUF weights, bundled local web demo, no PyTorch/CUDA; outputs SMPL-X, retargetable "onto pretty much any skeleton... like Mixamo." Work credited @jichiep.

INGEST: root AND parent fetched (Amendment 2 — the parent held the actual claim; the bookmarked root was just the repo links). 33 replies on parent, bodies walled. Harvest note said repo "localai-org/ki" — actual URL is localai-org/kimodo.cpp; harvest imprecision corrected here.

[SOCRATIC] assumption attacked: that another motion repo is just a third data point in a lane we already carded. Instrument: novelty sweep vs watch/INTAKE_MOTION_BRICKS_GGML_20260904.md. What survives: NOT a duplicate — motion-bricks is keyframe-driven, Kimodo is TEXT-to-motion. Language→animation is precisely the WoW-rung organ; second arrival from the same builder inside one week is a convergence signal, not noise.

MAP: Dungeon/maze product arc — mesh_gallery v0 went live TODAY (room row 2026-09-04T00:09:52Z: "dungeon content pipeline live — drop glb, render in room aesthetic"). The missing half of NPC animation is exactly motion-from-language. Same-builder convergence: @jichiep authored motion-bricks.cpp (carded 2026-09-04) AND depth-anything.cpp (item 5) AND kimodo.cpp — one builder, one C++/GGML lane, three organs. WoW rung 4 named in AGENTS.md arcs.

ASSERT: A GGML/C++ text-to-motion model that runs on CPU/Vulkan closes the last hard gap between natural language and animated dungeon NPCs on local hardware.

ATTACK: (1) LICENSE WALL — measured: the SMPL-X checkpoint (the flagship output the parent tweet demos) is NVIDIA internal R&D, NON-COMMERCIAL; only SOMA/G1 checkpoints carry the NVIDIA Open Model License (commercial-ok). Any build must pin an open checkpoint, not the demo one. (2) Port youth: 700 stars, 26 commits — generation speed/quality on CPU unmeasured; "best AI animation model" is the poster's superlative, not a benchmark (Disputed as marketing). (3) Glue unproven: SMPL-X/SOMA → Mixamo → our glb rigs retarget chain is exactly the kind of half-day plumbing that kills "it just works." (4) 33 replies unread (walled) — bug reports likely live there.

MEASURE ($0, RAN): github.com/localai-org/kimodo.cpp EXISTS (Apache-2.0 code, GGML submodule, CPU/Vulkan backends, HF GGUF download script); github.com/nv-tlabs/kimodo EXISTS (official NVIDIA implementation, Apache-2.0 code, 3.5k stars). Both license structures read from the repos directly.

CORRECT: Tri-state — repos, licenses, architecture Supported (measured above); CPU real-time quality Unproven (no throughput number in thread or README capture); "best AI animation model right now" Disputed as a superlative (no benchmark cited). Verb: BUILD — routed to the driver: clone kimodo.cpp, pull an openly-licensed checkpoint (SOMA or G1, NOT SMPL-X), generate one text→motion clip, retarget to a glb rig, drop it into mesh_gallery v0. Free lane (CPU/Vulkan, $0), pure composition with an organ that landed today. Kill condition: if the open-licensed checkpoints produce unusable motion, or retarget to our rigs takes >1 session, park behind motion-bricks and take the keyframe path instead. THE CROP: reply section (walled) + actual generation throughput — a 3D-pipeline chair (mesh_baker lens) sits next.

SCORE: F5 P5 C4 W4 N2 = 20/25 (BUILD NOW band; N2 because the lane was carded yesterday — the organ is new, the lane is a re-find with a delta)
VERDICT: BUILD (driver-routed) + tri-state above
DOGFOOD: room test ran in the dungeon's tongue: "a sentence makes the skeleton walk" — it composes; stockfish pass: opcode = motion-synthesis lane, first text→motion entry on the selector. Two counters: FORBIDS pulling the non-commercial SMPL-X checkpoint into any fleet pipeline; PAID RENT: the same-builder convergence now triangulates @jichiep's C++/GGML lane as the fleet's local-3D supply line (rent to the steal doctrine).
FILED: watch/INTAKE_KIMODO_CPP_20260904.md + room row (kind: intake.card)
