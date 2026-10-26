# Y3 - game_mud / game_brawl room.py offer (2026-09-30)

## game_brawl.py (FIRST)
room.py wraps the tavern as spectator fan-out: handle_brawl_voice becomes the inbound-frame handler (room.touch per frame); one Room per brawl_id (player seat + spectators); publish() broadcasts the advance/react log lines while the engine runs; sweep() expires a silent awaiting_player. Engine keeps authority - room.py moves bytes only. Already threads session_id end-to-end (latest_brawl_for_session, campaign linkage) - the closest to session semantics.

## game_mud.py (SECOND)
One Room per MUD room; members = party seats; publish = scene prose; survey() reads live presence() instead of only game_dm.ask_player. BLOCKED by the single global game.mud.player world key - needs per-seat state first.

## Verdict: game_brawl first (session-native); game_mud needs its state model split before room.py fits.
