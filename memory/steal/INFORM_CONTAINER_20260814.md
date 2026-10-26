# Inform when_closed / when_open — hung 2026-08-14

Steal: Inform Recipe Book 9.2 containers (https://ganelson.github.io/inform-website/book/RB_9_2.html).
A closed container changes the room text. Opening it is the verb.

Mapped onto existing Mag files, not a new engine:
- mag/game_campaign.py `_look_at(crate)` — sealed until temple:/shared:/slain: flag
- mag/game_campaign.py `_narrate_room` — skip census-label hooks; filter chasm ISO/`talk` leaks
- mag/wave.py idle bits — same label skip so speak is not "Crate with keep seal."

Open/share/take crate still files dungeon_dev (PLAY_AS_WORK). Closed is the ward.
