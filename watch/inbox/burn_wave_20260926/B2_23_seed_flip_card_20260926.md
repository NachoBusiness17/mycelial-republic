# B2-23 Seed-3.2.0 Drive flip card - 2026-09-26

## Verdict

LANDED, card only, nothing re-zipped. Two corrections vs the brief: (1) the shipped pack's seal is 52/52, not 55/55 (55 was the pre-surgery Desktop original; receipt lines 10 vs 25); (2) no Drive bridge exists on this host, so the card gains a browser upload step and the receipt's "Drive-bridged" line is stale. No link exists yet; operator GO required.

## Evidence

- `watch/inbox/SEED_PUBLIC_PACK_20260925.md:34-35`: "53 files, 99,905 bytes" / "sha256: e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e". Re-hash today: match, 53 entries, zero .pyc.
- Same file:25: "52/52 verified, 0 drifted, 0 missing". Re-verified against zip bytes today: ok=52 drift=0 missing=0.
- Same file:40-41: "watch/inbox is Drive-bridged (fostertron transport)" - STALE. `watch/inbox/TWO_MACHINE_SYNC_20260919.md:24-27` requires Drive-for-desktop plus a junction; never executed. `QUEUE.md:52` hard finding: "no junction, no Drive client, local backup remote is same-disk". Checked today: fsutil says the repo path is not a reparse point; no Google Drive client install found; `git remote -v` shows only `local` = C:\Users\foste\Documents\projects\Mag-backup.git (same disk).
- `watch/inbox/INDEX.json`: seed-3.2.0.zip row sha256 E9F4603A... equals file bytes.
- `watch/inbox/seed-3.2.0-card.png` renders "seal 52/52", so the public card already carries the correct number.

## Work done

FLIP CARD (operator, browser only, upload the exact shipped bytes, never re-zip)

Pre-flight
- [ ] Hash gate: `.venv\Scripts\python.exe -c "import hashlib;print(hashlib.sha256(open(r'watch\inbox\seed-3.2.0.zip','rb').read()).hexdigest())"` must print e9f4603a4484dafb3d79103aef63c678774ec508f9cd573677e91f83bc78f87e. If not, STOP and file as owed.
- [ ] Upload ONLY watch\inbox\seed-3.2.0.zip. Never rebuild from source: unittest re-creates pycache and resurrects the author-path leak (receipt lines 14-19, 28-29).

Flip (drive.google.com, signed in as fostertron@gmail.com)
1. My Drive > New > File upload > watch\inbox\seed-3.2.0.zip. Wait for upload complete (100 KB, seconds).
2. Right-click seed-3.2.0.zip > Share > Share.
3. General access: Restricted -> Anyone with the link. Role: Viewer (download only; never Editor or Commenter).
4. Copy link; note FILE_ID (the segment after /d/).
5. Paste the link into the X reply draft (bottom of SEED_PUBLIC_PACK_20260925.md) replacing [link]. Do not post until verify passes.

Verify after flip (anonymous proof)
- `curl -sL "https://drive.google.com/uc?export=download&id=FILE_ID" -o seed_flip_check.zip`
- `.venv\Scripts\python.exe -c "import hashlib;print(hashlib.sha256(open('seed_flip_check.zip','rb').read()).hexdigest())"` must equal e9f4603a... Optional deep check: unzip, run `sha256sum -c MANIFEST.sha256` inside seed-3.2.0/ -> 52 OK. Anonymous fetch plus hash match proves the flip.

Rollback
- Same Share dialog -> General access -> Restricted. Re-run the curl: expect 403 or a sign-in redirect, no zip bytes.
- If the reply already posted: file a follow-up correction post with the new link; never silently edit or delete the post.
- Never delete the Drive copy or the local zip (shared-surface no-erase law); Restricted is the rollback.

## Falsifier

Card falsified if (a) a live Drive bridge exists (DriveFS process or a reparse point on the repo path -> drop the upload step and flip in place), or (b) the post-flip anonymous download hash differs from e9f4603a... (bytes mutated in transit -> stop, re-file). Both checked today: (a) absent, (b) local bytes match pre-flip.

## Bibliography closed

SEED_PUBLIC_PACK_20260925.md; TWO_MACHINE_SYNC_20260919.md; burn_wave_20260926/QUEUE.md; watch/inbox/INDEX.json; watch/inbox/SHARED_SURFACE_CONTRACT.json; seed-3.2.0.zip and seed-3.3.0.zip bytes; seed-3.2.0-card.png; fsutil reparse, DriveFS install, and git remote checks (commands quoted above).

## GATE SURFACE MIGRATION (B2-425, 2026-09-26T20:47Z)

The "operator GO required" precondition on this card now has a canonical
check: watch/inbox/OPERATOR_GO.jsonl read via `python tools/operator_go.py
seed-flip` (exit 0 = GO on file with source_transcript; exit 1 =
NO-GO-on-file, the current state). This card executes only on exit 0.
