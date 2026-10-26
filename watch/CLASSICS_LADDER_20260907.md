# THE CLASSICS LADDER — from pong to shot-by-shot (2026-09-07, operator commission)

Operator, on quadcode_ai's shot-by-shot AI cinema (sword, shark, ruins — all imagined):
"you're gonna be doing this here in a while. Let's start with the classics and work our
way up."

## The ladder — each rung teaches the pipeline one skill

| Rung | Classic | Skill it teaches the pipeline | Status |
|---|---|---|---|
| 1 | **PONG** | motion, collision, score, autonomous play, recording | **SHIPPED** — dashboard/static/pong.html, AI-vs-AI, 18s webm recorded + frame-verified |
| 2 | BREAKOUT | destruction, levels, particle debris | next |
| 3 | SPACE INVADERS | swarms, formations — the swarm motif arrives | |
| 4 | SNAKE | growth, self-collision, the tail that follows | |
| 5 | OUR ROOMS, recorded | phase volume, airflow, light maze, tavern as video | recorder proven |
| 6 | SHOT-BY-SHOT | AI cinema: the sword, the shark, the ruins — all imagined | the quadcode target |

## The stack that makes it work (all verified tonight)

- The games: canvas pages, autonomous AI play (no human needed)
- The recorder: the in-app browser recording API (18s 720p VP8 proven on shadow_walk
  and pong; artifacts land in /tmp/iab-recording-*.webm even when the API hides them;
  hold the tab through finalization or the artifact dies)
- The finishing: ffmpeg (louddnorm, transcode, frame extraction) + opencv verification
- The ears: GLM-ASR for commentary tracks; the speech channel for narration

## The law of the ladder

Each rung ships a VIDEO, not just a page — the pipeline learns production by producing.
The classics are public domain game mechanics (rules aren't copyrightable; our code is
ours); the rooms above them are fleet-original. By rung 5 the recorder knows our own
games; by rung 6 the shot list is the only human input left.
