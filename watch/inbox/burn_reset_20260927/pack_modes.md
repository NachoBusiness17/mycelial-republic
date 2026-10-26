# Burn lane pack_modes — test_build_mode_includes_build_excerpt root cause + fix

2026-09-27 · burn reset evening, lane 5/10 · files: mag/context_pack.py

## Root cause (bytes, not reports)

`tests/test_pack_modes_steward.py::test_build_mode_includes_build_excerpt`
asserts the frozen BUILD block survives `format_context_pack_text(pack,
mode="build", max_chars=8000)`. It did not: the render came back 7996 chars
ending in `…(pack clipped)` with no `L2b Frozen BUILD` heading.

Measured section sizes in build mode at failure time (2026-09-27 ~23:10 EDT):

- objective (memory/boot/CURRENT_OBJECTIVE.md): 2198
- doctrine: 4073 · continuity: 2200 · quantized_laws: 988 (new tonight)
- coordination: 1445 · solved: 972 · behavioral: 824 · zeitgeist: 799
- proven_moves: 419 · agent_state: 404

The L0 policy tier alone summed ~12k chars against the 8000 budget. The clip
ladder only sheds downstream parts (L4 heat, brief compaction) and then hard
clips, so the final `text[:max_chars-20]` cut exactly the frozen BUILD block
the ladder's own comment says to never discard: "the frozen BUILD and scope
are the worker's actual contract". Introduced by the quantizer delivery
landing `3eb6dc251` (2026-09-27): its ~1KB compiled-laws section rode in
after L0b objective, pushing policy past the whole budget in build mode.
Pre-existing registered failure (SUITE_BURNDOWN_20260927.md, "pack_modes_steward
(build excerpt)"); confirmed pre-existing: working tree clean for
mag/context_pack.py before this lane, failure reproduces at HEAD.

## Fix (align to the ladder's own rule; nothing weakened)

`format_context_pack_text` now builds the L0 policy in two tiers:

- directive tier (never shed): header + policy lines + L0b objective +
  L0b compiled laws + nervous/ops lines (`policy`, `policy_mid`);
- contextual-history tier (droppable): L0d doctrine/proven/solved/zeitgeist,
  L0b agent_state, L0-continuity, L0c directives, behavioral, coordination,
  resonance, L0f subchain (`policy_ctx_a`, `policy_ctx_b`).

New ladder stage between brief-compaction and the hard clip: when still over
budget, render with `policy + policy_mid` only (context sheds, directives and
ops status stay), keeping the order [policy_bare, build, scope, bonds, skills,
trail, task_small]. The hard clip remains as the last resort and now only
trims tail context, never the worker contract. Fix comments carry the receipt
(cause + 3eb6dc251 + measured sizes). Per the lane brief, reconciled against
the CURRENT pack contract from its bytes; the quantized-laws contract
(test_context_pack_quantized_laws.py: laws render inside the 4500 default
budget, 1800 cap, stale-as-debt) is untouched.

## Proof

- Unclipped renders byte-identical to HEAD implementation in all five modes
  (janitor 4943, build 23936, full 27332, plan 25683, audit 20504; HEAD copy
  probed via importlib from the same repo so objective path resolution
  matched; probe file deleted after).
- Clipped build at 8000 with a real build_path: len 7996, `L2b Frozen BUILD`
  present, goal text present, objective + compiled laws + nervous kept,
  doctrine + continuity shed (the intended drop order).
- Tests: target file + neighbors 8 passed, then full neighbor set
  (test_pack_modes_steward, test_context_pack_quantized_laws,
  test_context_freeze, test_mirror_voice_pack, test_coordination,
  test_v3_modules, test_write_strip, test_census_liveness,
  test_dashboard_plugin, test_agent_repack, test_repack_integration):
  57 passed, 0 failed, 105s.
- Ratchet: `tools/violation_ratchet.py check --changed` → PASS, hits=2,
  registered=2, NEW=0.
