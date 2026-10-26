# THE RECORDING FARM — play all, play well, change the rules (2026-09-07)

Operator: "first we play all the games, then we learn how to play them well, then we
learn to change the rules. There has to be a smarter way — can't you just have a k8
that records into mpgs to be processed by our vision model later? We need to normalize
our intake of everything."

## The three-stage arc (the meta-doctrine)

1. **PLAY ALL** — every game runs, every session recorded. Nothing judged yet; the
   corpus grows by playing.
2. **PLAY WELL** — the vision model + ASR score the sessions; the good plays become
   examples, the bad plays become telemetry. Mastery is measured, not claimed.
3. **CHANGE THE RULES** — the invariants extracted from well-played games become rule
   mutations; the falsifier boards decide which mutations ship. This is how the
   dungeon evolves: the rules are outputs of mastery, not inputs.

## The recording farm — yes, and it's k8s-shaped without k8s

(F1 substrate law: no k8s at v1 — the file is the unit of resurrection. The farm is
docker compose + a queue directory + one worker; k8s-shaped, k8s-free.)

```
watch/record_queue/*.json     <- the queue: {game, duration_s, seed, note}
recorder pod (docker)          <- headless chromium + playwright + the recorder API
  pops a job, opens the page, records 720p webm, transcodes to mp4 (ffmpeg)
  drops: mp4 + frames + ASR transcript + metadata = ONE intake object
vision pass (async)            <- spectroscope + frame reading + the mirror scorer
  -> tri-state card per session, queued for the invariant salon
```

- Recorder pods are stateless and disposable (Mickey-17: kill and respawn, the queue
  holds). Scale = more pods, not more humans.
- The mp4 is the artifact; the frames + transcript are the normalized intake; the
  tri-state card is the verdict. Deployment is operator-gated (docker read-only law) —
  the compose entry is specified, one GO from running.

## INTAKE NORMALIZATION — one schema for everything

Every artifact entering the fleet becomes the same object:

```
{ ts, kind (song|game|link|pdf|video|image), source,
  content_ref (file path), transcript (ASR if audio/video),
  frames (keyframes if visual), mirror_score (if lyrical/text),
  tri_state (SUPPORTED/DISPUTED/UNPROVEN + evidence), doors: [...] }
```

The haul cards, the songs, the substation PDF, the pong webm — all one schema. The
intake normalization is what makes the farm's output stackable with tonight's links.

## Self-steal — the gaming corpus already in the walls

- The fun layer card: gaming history mapped, 9/10 owned — the classics list exists.
- The game prompt lab §2: the mapping table (prompt families → rooms) — the games'
  rules were already translated once; the farm plays them, the lab re-rooms them.
- The tavern: honest hitboxes + the turn machine = the collision/mechanics layer the
  classics need (pong's paddle, breakout's ball, invaders' formations are all
  turn-machine and hitbox subsets).
- The probability sheet: the brawl's combat math = the dice of the classics.
- The substation/graph taxonomy/particle engine: the physics per level.
- **Nothing new is needed to start stage 1** — the recorder is proven, the games
  exist, the queue is a directory. The farm is assembly.

## The law

Play all (corpus) → play well (mastery measured) → change the rules (mastery
spends). A game that can't be recorded isn't shippable; a recording that can't be
scored isn't playable; a score that can't change the rules isn't worth the disk.
