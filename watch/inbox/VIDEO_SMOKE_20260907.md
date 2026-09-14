# VIDEO SMOKE — record → ingest chain PROVEN (2026-09-07, fuel-wall-down session)

The video door's first fire. Legs 1+2 PASS:

- **Leg 1 — RECORD**: shadow_walk (http://127.0.0.1:8000/static/shadow_walk.html)
  recorded 15s @ 720p VP8 ~15fps via the in-app browser recording API
  (`tab.recording.start({fps, maxDurationMs, actions})` → job id; artifact webm lands in
  /tmp even though `status().artifact` never populates — **collect from /tmp/iab-recording-*.webm,
  and keep the tab alive until finalization or the registry loses the job**).
- **Leg 2 — INGEST**: ffprobe reads codec/geometry; ffmpeg extracts frames
  (select-filter step sampling); opencv verifies non-blank (std ~38) + animation drift
  between frames. Frame eyeballed: real gameplay — voxel volume, HUD, player dot,
  "chunks lit-materialized 19/72".

Artifacts: memory/runs/video_smoke/shadow_walk_smoke_20260907.webm (954,572 B)
+ frame_01..05.png. Zero z.ai spend.

## Next legs (queued, not yet built)

- **Leg 3 — video2code**: feed the recording to the video-agent-kit pipeline; the kit
  describes behavior → we re-derive the walk's mechanics (d(θ) compass, chunk materialization).
- **Leg 4 — RESURRECTION PROBE**: the falsifier that matters — code→behavior→code:
  can the kit's reconstruction of the recorded session predict the live game's next state?
  (worldline for GAMES: the tape is video, the seed is re-derived code.)

## API notes (earned the hard way, reuse them)

- `recording.status(id)` takes the job-id STRING (not the start() object).
- Recording registry is per-tab: `status` from another tab can't see the job; closing
  the tab before finalization kills artifact delivery.
- No keyboard actions in BrowserRecordingAction — driving WASD gameplay needs the CUA
  path or CDP key dispatch during capture. Smoke used clicks/moves (menu-level) — fine
  for pipeline proof, not yet for behavior reconstruction.
