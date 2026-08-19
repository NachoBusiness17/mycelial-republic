# RIB — 1M-context lift (Grok wrote it)
**Schema:** rib.full_context_lift.v1
**Seat:** grok-desktop (Ghost)
**ts:** 2026-08-14T14:10Z
**Status:** LANDED — verify clean, dry run green
**Operator:** let grok write it; copilot handed the exact sites through the bus

## Law
Chain owns the record. Window is a reasoning surface. Never store the window as truth.
MAG_FULL_CONTEXT=1 gates every lift. Default clip is unchanged.
Deterministic \ core unchanged. Down seats stay records. inject_for/steer path untouched.

## Sites
1. mag/party_subchain.py mount(*, limit=24, max_chars=6000, full=False) + want_full().
   full / env → limit=None, max_chars=None. Entire verified transcript.
2. mag/game_dm.py 	urn() — 	ranscript[-6000:] only when env off.
3. mag/frontier_game.py play() — _hist full party log when env on; last 3/6 otherwise. Prompt gets full moves ([:70] is not a prompt clip).
4. mag/context_pack.py mode=ull + env — mounts complete subchain + uncapped doctrine RIB + world state; pack clip skipped.
5. mag/context_checkpoint.py switch_model — 200-token pointer still persisted; env adds handoff=full_context with the real window (not written as chain truth).

## Verify
- party_subchain.verify() → ok, errors=[]
- default mount: n_mounted=24, ~6034 chars, omitted-by-bound
- MAG_FULL_CONTEXT=1 mount: n_mounted=86, 28557 chars, no omit
- pack default ~4496 clipped; pack full 50959, L0f subchain present
- switch_model default handoff=pointer; env handoff=full_context
