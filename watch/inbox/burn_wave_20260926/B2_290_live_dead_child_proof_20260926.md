# B2-290 Live-dead-child proof for the returncode law (SW-07, 2026-09-26)

## Verdict

LANDED. scripts/grounding_chain.py BASE/CHAIN_LOG are now injectable via --base/--log args and GROUNDING_CHAIN_BASE/GROUNDING_CHAIN_LOG env, and tests/test_grounding_chain.py gained test_live_dead_child_end_to_end_injected_base: a REAL scratch child (a file whose whole body is `import sys; sys.exit(3)`, no mocks) runs against a real scratch state dir through gc.main(), and the test asserts the row records exit 3 with an unchanged state delta AND the production watch/inbox/union_fullsend_20260917/grounding_chain.jsonl is byte-untouched. Full file: 7 passed in 0.82s.

## Evidence file:line quotes

- QUEUE.md row: "make scripts/grounding_chain.py CHAIN_LOG/BASE injectable (arg or env) and add an end-to-end test that runs a real scratch child designed to exit 3 against a scratch state dir, asserting the row records exit 3 with an unchanged state delta; falsifier: if the injected-base run still writes the production grounding_chain.jsonl, injection is broken".
- scripts/grounding_chain.py main() now carries (fix-comment law, cause + evidence named): "FIX 2026-09-26 (B2-290). CAUSE: BASE/CHAIN_LOG were import-time constants only, so the B2-56 returncode fire path had no end-to-end proof against a real child and scratch state ... FIX: --base/--log args plus GROUNDING_CHAIN_BASE/GROUNDING_CHAIN_LOG env rebind the module globals before the loop".
- The scratch child: `child.write_text("import sys\nsys.exit(3)\n")` then `monkeypatch.setattr(gc, "CMD_RESEARCH", [gc.PY, str(child)])`; `subprocess.run` is NOT monkeypatched in this test -- the death is real.
- Assertions: `fired["exit_code"] == 3`, `fired["state_before"] == fired["state_after"]`, `fired["state_after"]["remaining"] == 1`, production-log byte comparison (`prod_log.read_bytes() == prod_before`, and the is-file-None arm asserts the injected run must not create the production log).
- Run: `.venv/Scripts/python.exe -m pytest tests/test_grounding_chain.py -q` -> `7 passed in 0.82s`.

## Work done

- scripts/grounding_chain.py: --base/--log argparse args + env fallbacks; `global BASE, CHAIN_LOG` rebinding before the loop so evaluate(), lane_state(), queue_remaining(), build_remaining() and record() all run on injected state; comment names cause and evidence per the fix-comment law.
- tests/test_grounding_chain.py: new end-to-end test building scratch state.json/queue.jsonl (1 pending id -> real evaluate() emits the research action), scratch child exiting 3, injected run, and the two-sided falsifier (production log untouched if it exists; not created if it does not).
- Suite re-run green.

## Falsifier

The brief's falsifier is encoded as executable assertions: any future change that routes an injected run's record() to the production log fails the test on the byte comparison, and any change that breaks evaluate()'s scratch-base reading fails on remaining == 1. Reopen if test_live_dead_child_end_to_end_injected_base is skipped, deleted, or pytest reports it failing while production claims the law holds.

## Bibliography closed

Read: scripts/grounding_chain.py (full, pre/post edit), tests/test_grounding_chain.py (full), QUEUE.md B2-290 row, watch/inbox/burn_wave_20260926/B2_07_grounding_20260926.md referenced via the B2-56 comment (not re-derived). No external sources.
