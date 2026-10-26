# B5 SOURCE PROVENANCE — Bad Apple!! frames (2026-09-06)

## What is here

- `badapple.mp4` — 9,820,855 bytes, 480x360 @ 30fps, 219.03s. Downloaded 2026-09-06 from
  `https://github.com/Felixoofed/badapple-frames` (raw.githubusercontent.com), file
  `badapple.mp4` @ commit blob 5a7c603. Verified with ffprobe (480x360, 30/1, 219.03s).
- `pack_frames.mjs` — the local extractor/packer: ffmpeg scale to 96x72 gray ->
  threshold 128 -> 1-bit packed -> consecutive-frame dedup -> bit-RLE (alternating
  runs, LEB128 varints) -> base64 embed (`frames_embed.txt`).
- `seg.raw` — the ffmpeg rawvideo intermediate for the 0:00-0:40 segment (1200 frames
  x 96x72 gray). KEPT: the B5 harness re-derives embedded bits from it bit-for-bit
  (provenance falsifier).
- `frames_embed.txt` — the packed embed injected into
  `dashboard/static/bad_apple_field.html` (1200 frames, 1145 unique, 181,766 RLE bytes,
  248,541 bytes JSON with base64).

## GitHub-first note

Per house law GitHub was searched FIRST for a frames dataset. Found:
`Felixoofed/badapple-frames` — a community frame-dump repo (96 stars, used by
r/badapple) containing BOTH `frames.zip` (15.8MB pre-extracted PNGs, full 6572 frames)
and the source `badapple.mp4`. We took the repo's mp4 (smaller transfer, same ground
truth) and extracted our own segment at our target resolution with the local ffmpeg
8.1.2 build — a pre-extracted PNG dump at full res would have been 15.8MB down for
frames we then had to downsample anyway.

## License status (honest)

- The repo has **no LICENSE file** (GitHub license API returns none). It is a
  fan-distribution resource, explicitly offered "for all kind of your bad apple
  projects".
- The video itself is the famous Niconico shadow-art PV of "Bad Apple!!" (song:
  Alstroemeria Records, Touhou arrangement, vocals Nomico; PV by the Niconico
  collab team). It is distributed freely by its creators and is THE canonical
  substrate-stress video of the genre (played on connectomes, LEDs, Excel,
  oscilloscopes...), but it carries **no formal open license**.
- Our use: non-commercial, local, attributed here and on the surface footer.
  Status recorded honestly: fan-use under the genre's own norms, not under an
  open license.
