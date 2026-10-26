# B2-54 operator card: arm the Sunday 06:30 weekly pack refresh cron (2026-09-26)

## Verdict

Card only; nothing was armed or created here. Arming is one operator step: open a FRESH chat and paste Prompt A. Until armed, Command B is the manual fallback. Existing pack verified today by bytes: sha256 82a4efed7745a3ace2dec8fa8915d765b9508ae7946384bd8b6aa70c3f4e35e9 matches INDEX.json:5892; OneDrive copy on record (steps.jsonl:22168). First cron fire: 2026-09-27 06:30 local if armed before then, else 2026-10-04.

## Evidence

- watch/inbox/ESSENTIALS_RESTORE.md:39-40: "Refresh weekly (dispatcher automation) or after any landmark day." Custody law :37: "Three copies minimum, one off the Drive account entirely."
- watch/inbox/FLEET_IMPRINT_20260917.md:1231: "a session owning a scheduled task CANNOT CronCreate a second; fold duties into the existing automation via CronUpdate": why the arming chat must be fresh.
- memory/trajectory/steps.jsonl:22162 (ts 2026-09-26T11:38:20Z) holds the verbatim build pipeline: find list (prunes memory/ghost, memory/runs, mrpool_export, dashboard/data, __pycache__; 80M cap; media extensions excluded; explicit adds ledger_full.jsonl, seed-3.2.0.zip, .env) then `tar --ignore-failed-read -czf - -T $L | openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:configs/secrets/pack_key.txt -out $OUT`, roundtrip listing count, OneDrive copy. The row's exit field is null; success is proven by bytes, not the row: the pack on disk reproduces the INDEX-registered sha exactly (1,706,466,964 bytes).
- configs/secrets/pack_key.txt exists, 44 bytes (token_urlsafe(33) shape per steps.jsonl:22162). Contents never read or printed by this lane.

## Work done

Prompt A (paste verbatim into a fresh chat):

> Read watch/inbox/ESSENTIALS_RESTORE.md and memory/trajectory/steps.jsonl line 22162 (the exact pipeline that built ESSENTIALS_PACK_20260926.tar.gz.enc). CronCreate ONE weekly automation firing Sundays 06:30 local. Each fire, repo C:/Users/foste/Documents/projects/local_sovereign_agent, Git Bash: rebuild the file list exactly per that step (same finds, prunes, 80M cap, media exclusions, explicit adds); OUT=watch/inbox/ESSENTIALS_PACK_$(date +%Y%m%d).tar.gz.enc; run that tar|openssl line verbatim; roundtrip-verify (decrypted tar listing count equals list count), on mismatch STOP and file the failure, never ship unverified; copy OUT to /c/Users/foste/OneDrive/; register the new artifact (path, class artifact, purpose, sha256) in watch/inbox/INDEX.json plus a one-line watch/inbox/ receipt; never delete prior packs (operator prunes). NEVER print, move, or regenerate configs/secrets/pack_key.txt; if missing STOP and file owed (a new key orphans every existing pack). Report sha256 prefix only.

Command B (manual fallback this week; Git Bash at repo root; overwrites the same-name artifact, so re-register the new sha in INDEX.json after):

```
L=$TEMP/ess.list; { find . -maxdepth 1 -type f -print; find mag tools scripts tests githooks configs docs queue research state training dashboard corpus/steal corpus/founding_law corpus/lore corpus/prose corpus/library canon/podcast_corpus memory watch/inbox \( -path memory/ghost -o -path 'memory/biography_backup*' -o -path memory/runs -o -path memory/corpus/shadertoy21k -o -path memory/corpus/training_pdfs -o -path watch/inbox/mrpool_export -o -path dashboard/data -o -name __pycache__ \) -prune -o -type f -size -80M ! -iregex '.*\.\(jpg\|jpeg\|png\|gif\|bmp\|webp\|mp4\|mp3\|wav\|webm\|mkv\|avi\|mov\|pdf\|epub\|whl\|exe\|dll\|so\|dylib\|7z\|gz\|tgz\|bz2\)' -print; echo watch/inbox/mrpool_export/ledger_full.jsonl; echo watch/inbox/seed-3.2.0.zip; echo .env; } | sed 's|^\./||' | sort -u > "$L"; OUT=watch/inbox/ESSENTIALS_PACK_$(date +%Y%m%d).tar.gz.enc; tar --ignore-failed-read -czf - -T "$L" | openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:configs/secrets/pack_key.txt -out "$OUT" && [ "$(openssl enc -d -aes-256-cbc -pbkdf2 -pass file:configs/secrets/pack_key.txt -in "$OUT" | tar -tzf - | wc -l)" -eq "$(wc -l < "$L")" ] && cp "$OUT" /c/Users/foste/OneDrive/ && sha256sum "$OUT"
```

No automation was created by this lane.

## Falsifier

Card fails if: (1) pack_key.txt changes or vanishes, then `openssl enc -d -aes-256-cbc -pbkdf2 -pass file:configs/secrets/pack_key.txt -in watch/inbox/ESSENTIALS_PACK_20260926.tar.gz.enc | tar -tzf - | wc -l` errors (bad decrypt) or returns 0; it must return the list count. (2) The fresh chat rejects CronCreate with the one-automation message: the chat was not fresh; retry in a truly clean one. (3) INDEX.json:5892 sha stops matching disk bytes: pack drifted; rebuild via Command B.

## Bibliography closed

watch/inbox/ESSENTIALS_RESTORE.md; watch/inbox/INDEX.json:5888-5893; watch/inbox/FLEET_IMPRINT_20260917.md:1231; watch/inbox/RECAP_7D_20260926.md; watch/inbox/burn_wave_20260926/QUEUE.md:54; memory/trajectory/steps.jsonl:22161-22168; configs/secrets/ listing (names only, key never read); memory/burns/LEDGER.jsonl tail.
