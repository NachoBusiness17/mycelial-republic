# CLEANUP PASS 1 + REMOTE DEVICES RTFM (2026-10-23)

Two commissions: family file cleanup (his/wife's separate, classify,
quarantine) and RTFM the new ZCode Remote devices panel for mesh use.

## Cleanup pass 1 - done, manifest-first, ZERO deletions

Manifest of every move: C:/Users/foste/CLEANUP_20261023/MANIFEST.csv
(ts_utc, origin, dest). Reverse any move by reading it back.
Classification used FILENAMES ONLY; no personal file contents opened.

Results (118 moves):
- Downloads: 69GB -> 8.5GB, 910 -> 801 items
- 43 installers/ISOs -> installers_quarantine/ (Chats/Claude/Grok/ZCode
  versions, Battle.net, Steam, Docker, Ledger, Tailscale, yt-dlp...)
- 13 Google Takeout split zips -> takeout_dl_export/ (the dl/ Drive
  export: martial-arts collections, Hickman comics, movie rips -
  HIS; ~14GB, parts 001-009 + 4 drive-download parts, kept together)
- 5 Kundalini Yoga DVD sets -> wife_likely/yoga/ (strongest wife
  signal; flagged LIKELY, he can rename the bucket)
- 3 McKenna + 3 martial-arts archives -> his_mark/
- 27 camera-pattern photos/screenshots -> photos_unsorted/ (IMG_,
  Screenshot_; owner split needs EXIF or his glance - phase 2)
- Desktop: all 8 loose .py (last night's shadertoy lane) ->
  vault_staging/scratch_scripts_20261022/; extension folder "New
  folder (2)" had its PDF rescued to his_mark/docs, folder left in
  place (still contains non-pdf files - phase 2)

House rule (operator, 2026-10-23, verbatim): "if its porn its hers
lmao." Filed as the household classification law: explicit-content
signals route to wife_likely/ without further adjudication. Applied
same hour: 2 self-labeled NSFW documents (NSFW_Zaftigg.docx.pdf) moved
Downloads -> wife_likely/nsfw_docs/, appended to MANIFEST.csv. The
rule is enforced on FILENAME/label signals only - the estate does not
visually inspect family media; anything content-ambiguous waits for
his glance.

Phase 2 (proposed, awaiting go or the glance):
- photos_unsorted owner split: EXIF timestamps + one glance from him
  (IMG_ prefix is iPhone-class, PXL_ is Pixel-class, screenshots are
  desktop-class; a couple's camera roll cannot be owner-split by
  filename alone and the estate does not open family photos)
- takeout_dl_export: extract decision (extracts to dl/ tree, ~14GB;
  picture backups live inside)
- remaining ~800 Downloads items: loose media/pdfs/zips/md - name-
  cluster pass on request
- New folder (2) extension remnant + New folder internal junk

## Remote devices panel - RTFM (docs.zcode.z.ai/en/docs/remote-development)

What it is: the desktop app runs a full ZCode workspace ON a remote
host (SSH / WSL / Docker): file tree, terminal, git, and the AGENT
itself execute on the target; account/model config stay local. It
deploys a runtime to ~/.zcode/server on first connect. Skills/MCP/
plugins sync per-item, user-level only, never overwriting.

THE MESH FOLD (triangulation with tonight's fleet):
1. The panel's SSH type can drive the POSIX cells NATIVELY: t90 and
   pixel-11-pro (Termux) are valid targets - the agent runtime would
   run IN Termux with our ~/.ssh/config hosts prefillable. Bob and
   desktop are WINDOWS: the docs say native Windows remotes are
   UNSUPPORTED (POSIX shell required) - bob stays on the ssh-cli +
   mesh_router path, which is correct anyway (the vitality scheduler
   owns bodies; the panel owns interactive workspaces).
2. Division of labor, by the RTFM: panel = interactive agent
   workspaces on the Termux cells (debugging a beacon on t90 from the
   desktop UI); mesh_router = scheduled fleet work and gated routing.
   The panel is the mechanic's bay; the mesh is the fleet.
3. Sync Skill/MCP would push user-level skills to the Termux cells -
   useful AFTER the trust question: MCP secrets sync VERBATIM, so
   never sync to a body that is not ours (all four are).
4. Mobile note: his phone can RECONNECT registered workspaces but not
   create connections - the fleet is drivable from his pocket once
   workspaces are registered on the desktop.

## OPS ADDENDUM: zero-blink sweep (same evening)

Operator reported continuous headed popups. Diagnosis: five scheduled
tasks ran visible console hosts on cadence. Three were the continuous
offenders and are FIXED (rewrapped through scripts/run_hidden.vbs,
verified in the task store, schedules untouched):
- MotoCronWatch (every 5 min, bare python - the main offender, new
  tonight with the moto phone)
- MagCommitSweeper (every 10 min, bare powershell)
- MagNightCrew (every 30 min, bare venv python)
Two remain OWED-ADMIN (Set-ScheduledTask access denied non-elevated;
both registered from the elevated/etfag context):
- MagCheckpointV2Hourly (hourly powershell blink) - the same admin
  /DISABLE already owed in THE_ONE_MAP section 2 covers it
- MagHermesBurn247 (15 min, cmd-host flash ~1s; its inner wscript is
  already hidden)
Lesson recorded: -WindowStyle Hidden still blinks (the window is
created then hidden); the wscript wrapper never creates one. New tasks
must use the run_hidden.vbs pattern at REGISTRATION time, not after.

## Receipt

- Consumer: the operator's household corpus; the fleet's interactive
  surface strategy.
- Verifier: MANIFEST.csv is the complete move record (118 rows); the
  docs fold cites zcode.z.ai/en/docs/remote-development fetched
  2026-10-23; fleet claims regenerate from mesh_router.py map.
