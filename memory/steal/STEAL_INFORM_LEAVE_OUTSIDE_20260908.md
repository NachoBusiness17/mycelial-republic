# Steal: Inform Leave / outside soft (VagueGo + Exit) — never talk-belt

**Source:** Inform 6 Grammar.h Leave / Exit (Appendix A): Verb 'leave' bare→VagueGo, noun=ADirection→Go, noun→Exit, into/in/inside/through→Enter; Verb 'exit' 'out' 'outside'→Exit. DM4 §A4 VagueGo “You'll have to say which compass direction to go in.” / Exit1 “But you aren't in anything at the moment.” / GetOff “But you aren't on ‹x1› at the moment.” Field: https://jxself.org/inform-guide/appendix-a.html + https://www.inform-fiction.org/manual/html/sa4.html
**Date:** 2026-09-08 4:29 PM ET
**Weakest link:** `parse_player_speech("leave")` / `leave crate` / `outside` were `None`; `leave mira` wrongly hit talk via mira keyword.

## Field pattern
- bare `leave` → `{type: vague_go}` → You'll have to say which compass direction to go in.
- `leave|outside` bare outside → `{type: exit}` → But you aren't in anything at the moment.
- `leave [the] NOUN` → `{type: exit, target}` → But you aren't on the ‹noun› at the moment.
- `leave into|in|inside|through NOUN` → enter soft (existing)
- Do **not** steal: bare `out` / `leave the tavern|inn|bar` / `go out` (move organ); `leave north` (move); leaving gerund; pour (next cellar); Calcifer invent; room.desc dump
- Hang **BEFORE** talk catch-all (with Exit block) so `leave mira` never talk-belts

## Mag map
- **Primary:** `mag/game_campaign.py` `parse_player_speech` — Leave/outside soft before Exit take/get climb
- **Primary:** `mag/game_campaign.py` `apply_action` — existing vague_go + exit floors
- **Organs only:** `game_campaign` (no new file / no furniture organ)
- Staged on `/workspace/mag-live/game_campaign.py`; sync to Mag disk this fire (desk online)

## Proof
- `speak_proof_20260908_1629.md` — 37/0 PASS/FAIL
- Live `/wave` DOWN (8765 not listening) — silence contract
- Next cellar: pour soft (EmptyT/Fill cousin) or restart /wave so idle_tick FILE can land on keep_gate
