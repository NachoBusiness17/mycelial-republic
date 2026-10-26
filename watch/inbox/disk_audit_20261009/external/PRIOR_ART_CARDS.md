# PRIOR_ART_CARDS - external prior-art, disk-storm audit lane A

- Provenance: merges the 2026-10-09 21:24Z lane draft with the 21:30-22:00Z second research pass; the 21:24 draft's cards are carried forward and verified, the second pass adds the per-call output-cap class (section 2) and primary-source quotes. Remote research only; no local disk walks. Every claim carries its source URL; unverifiable items sit in the OWED register.
- Mandate (operator, verbatim): "steal this has to be a solved problem" - find the existing solutions, not new ones.
- Monster map: (A) 309GiB / 11,079 files under the agent-cache exec dir, avg 28MB per tool-call stdout log, single files 6-12GiB, content = full-disk find dumps + FINDSTR malformed-path loops; (B) docker_data.vhdx 132GB never compacted; (C) system pagefile ballooned to 135GB; (D) HF cache 66GB dead experiments; (E) AppData Temp 53GB.

## CLASS 1 - agent-harness transcript/session growth (monster A)

### 1.1 Claude Code: age-based retention sweep
- WHO: Anthropic Claude Code.
- WHAT THEY DO: transcripts live as one .jsonl per session under ~/.claude/projects/ ("Full conversation transcript: every message, tool call, and tool result"), plus subagent transcripts and tool-result spills; docs say clients "store session transcripts locally in plaintext under ~/.claude/projects/ for 30 days by default". Knob: settings.json `cleanupPeriodDays` - "The default is 30 days and the minimum is 1; setting 0 fails with a validation error"; the sweep runs at startup, also removes orphaned worktrees, and pauses with a /status warning when retention cannot be safely determined instead of deleting blind. shell-snapshots "Removed on clean exit"; legacy dirs (todos, statsig, logs) "No longer written" but swept. Separate `desktopSessionCleanupPeriodDays` (v2.1.248+). Their controversy is the opposite failure mode (retention too short, silent loss).
- SOURCE: https://code.claude.com/docs/en/claude-directory ; https://code.claude.com/docs/en/data-usage ; https://github.com/anthropics/claude-code/issues/24207 ; too-short complaints: https://github.com/anthropics/claude-code/issues/62476 , https://www.theregister.com/ai-and-ml/2026/06/30/claude-code-users-complain-their-chat-records-are-being-mysteriously-wiped-out/5264673
- VERDICT: STEAL - age-based expiry wired into a regularly occurring process, with 0-invalid validation and fail-pause semantics.
- ADOPTION NOTE: retention flag on the daily smith task (MAG_EXEC_LOG_RETENTION_DAYS=14) sweeping exec-dir logs by mtime; refuse 0; pause-with-warning on undeterminable retention; keep an exemption list for the live window's files.

### 1.2 Claude ecosystem: community cleaner where the harness lagged
- WHO: garrickz2/claude-code-cleaner (Rust TUI); ePlus "Claude Cleaner"; Reddit scripts.
- WHAT THEY DO: Scan/Select/Preview/Clean flow over ~/.claude: cleans projects/ ("typically the largest") plus debug, file-history, telemetry, shell-snapshots, todos, paste-cache; trims history.jsonl keeping last 500 lines; protected paths (settings.json, CLAUDE.md, skills/) never touched; orphan-project detection (cache whose source path is gone); dry-run mode; 30-day default threshold.
- SOURCE: https://github.com/garrickz2/claude-code-cleaner ; https://eplus.dev/claude-cleaner-a-safer-way-to-clean-up-claude-code-sessions ; https://www.reddit.com/r/ClaudeAI/comments/1r2snly/cleanup_script_for_claude_mine_grew_to_13gb_in_4/
- VERDICT: STEAL-ADAPTED - the design worth copying is protected-paths + dry-run + orphan detection + age threshold, not the TUI.
- ADOPTION NOTE: our prune command gets --dry-run, a protected-path allowlist (inbox, receipts, rib), an age threshold, and per-directory byte totals the smith chart can trend.

### 1.3 Codex CLI: our exact twin, no shipped cure
- WHO: OpenAI Codex CLI.
- WHAT THEY DO: no built-in session cleanup or retention knob for ~/.codex/sessions. Issue #34061 ("Insane Codex Disk Usage from Subagents"): one long-running `codex resume` parent spawned 2,393 child session files, roughly 731.5GiB of 755GiB used; a 3-minute child wrote about 353,000 records (483MB); reporter's safeguard checklist: per-session/global quotas, rotation/compression/retention limits, dedupe of compaction snapshots and tool outputs, disk-exhaustion warnings, prune/report command. Sister issues: compaction re-embeds replacement_history, 42GB in a month (#41806); 268MB file with 234.6MB repeated image data, monthly 24.365GiB (#33735); 700MB-2GB sessions (#24948); 118GB computer-use logs freed on quit (#25815); checkpoint blobs 100+GB (#29388); first-class cleanup workflow request (#20230); safe bulk cleanup request (#38838). The one shipped knob is config.toml `[history]` `persistence = "save-all" | "none"` (+ max_bytes on history.jsonl), which does not touch transcripts.
- SOURCE: https://github.com/openai/codex/issues/34061 ; https://github.com/openai/codex/issues/41806 ; https://github.com/openai/codex/issues/33735 ; https://github.com/openai/codex/issues/24948 ; https://github.com/openai/codex/issues/25815 ; https://github.com/openai/codex/issues/29388 ; https://github.com/openai/codex/issues/20230 ; https://github.com/openai/codex/issues/38838 ; config: https://learn.chatgpt.com/docs/config-file/config-reference
- VERDICT: STEAL-ADAPTED - nothing shipped to steal, but the 34061 checklist is a ready-made requirements doc for our fix; we are that issue with a 309GiB head start.
- ADOPTION NOTE: implement the checklist: per-dir quotas, rotate + compress, dedupe repeated tool outputs, disk-exhaustion warning, prune subcommand with --format json listing.

### 1.4 Gemini CLI: the disease and the best-shaped knob
- WHO: Google Gemini CLI.
- WHAT THEY DO: sessions live in ~/.gemini/tmp/<project_hash>/chats/ (project-hashed). Disease documented: .gemini at 46GB mostly tmp (#21652); root cause session logs store full base64 inline binaries (#24432); checkpointing grew history to 3.8GB (#7328). Cure shipped: `general.sessionRetention` in settings.json with four fields - `enabled` (default true), `maxAge` (default "30d"), `maxCount` (default undefined/unlimited), `minRetention` (default "1d"): "Sessions newer than this period are never deleted by automatic cleanup." Deleting a session removes related plans, task trackers, tool outputs, and activity logs.
- SOURCE: https://geminicli.com/docs/cli/session-management/ ; https://geminicli.com/docs/reference/configuration/ ; https://developers.googleblog.com/pick-up-exactly-where-you-left-off-with-session-management-in-gemini-cli/ ; disease: https://github.com/google-gemini/gemini-cli/issues/21652 , https://github.com/google-gemini/gemini-cli/issues/24432 , https://github.com/google-gemini/gemini-cli/issues/7328
- VERDICT: STEAL - the four-field contract {enabled, maxAge, maxCount, minRetention} with a never-delete-newer-than floor is the cleanest retention knob in the field.
- ADOPTION NOTE: copy the shape verbatim: retention {enabled, max_age_days, max_count, min_age_days}; min_age protects in-flight window logs from the daily sweep; max_count is the cheap hard cap on tool-call stdout file count.

### 1.5 opencode: prune verb missing, gc-only cleanup insufficient
- WHO: opencode (anomalyco/opencode).
- WHAT THEY DO: official commands `opencode session list --max-count 20 --format json` and `opencode session delete <id>` (also deletes child sessions); since v1.2.0 storage is one SQLite DB (WAL) under ~/.local/share/opencode/. No prune/auto-cleanup; feature request #22110 asks for exactly that. Snapshot git objects hit 170GB (#17753, closed via PR #12856) even though an hourly scheduler ran `git gc --prune=7.days`; stray tmp_pack_* files survive crashes (#14811); the 7-day threshold was not enforced, 380GB (#10782); 533GB orphaned (#15977).
- SOURCE: https://opencode.ai/v2/docs/cli/commands ; https://github.com/anomalyco/opencode/issues/22110 ; https://github.com/anomalyco/opencode/issues/17753 ; https://github.com/anomalyco/opencode/issues/14811 ; https://github.com/anomalyco/opencode/issues/10782 ; https://github.com/anomalyco/opencode/issues/15977 ; community one-liner https://www.junian.dev/blog/opencode-delete-all-sessions
- VERDICT: STEAL-ADAPTED - steal the command shape (json listing + guarded delete); their failure teaches that producer-side gc cannot be the only sweeper.
- ADOPTION NOTE: machine-readable listing for the prune loop; the external sweeper must target mtime AND size-class (giants, crash orphans) independent of producer state.

### 1.6 OpenHands: automation workspace watchdog
- WHO: OpenHands (automation).
- WHAT THEY DO: local-mode automation runs are cleaned by a watchdog after `workspace_retention_seconds` (7 days default; issue 503 asks it to also clean retained Agent Server state); bug 7914: runtime containers never cleaned after Docker runs. Context-level caps exist too (MAX_CMD_OUTPUT_SIZE, card 2.2).
- SOURCE: https://github.com/OpenHands/automation/issues/503 ; https://github.com/OpenHands/OpenHands/issues/7914
- VERDICT: WATCH - watchdog-plus-retention-seconds pattern is right; their coverage holes are the lesson.
- ADOPTION NOTE: retention must name EVERY artifact class a run produces (logs, tool outputs, snapshots, containers), not just the primary workspace.

### 1.7 Cursor / VS Code: vendor declines, users schedule deletion
- WHO: Cursor, VS Code.
- WHAT THEY DO: per-workspace storage is never cleaned when a workspace is deleted (microsoft/vscode#32461, declined); workspaceStorage 7GB (#53552); Cursor forum: 125GB storage growth; a nested .cursor folder caused recursive indexing bloat (50GB case); community fix: weekly scheduled deletion of User/History and workspaceStorage.
- SOURCE: https://github.com/microsoft/vscode/issues/32461 ; https://github.com/microsoft/vscode/issues/53552 ; https://forum.cursor.com/t/cursor-storage-has-grown-to-125gb-on-my-mac-how-can-i-safely-reduce-it-without-losing-history-context/172127 ; https://dev.to/ttibbs/cursor-was-using-50gb-of-memory-the-cause-was-a-nested-cursor-folder-275o ; https://www.reddit.com/r/cursor/comments/1s5lf5u/cursor_took_over_my_250gb_storage_without
- VERDICT: NOT-APPLICABLE - no shipped cure to steal; the ops pattern (hand-rolled scheduled deletion) and the nested-dir recursion guard are the takeaways.
- ADOPTION NOTE: guard against nested/recursive harness cache dirs inside watched projects; schedule our own sweep, do not wait for vendors.

### 1.8 Amp: archive-on-quit only
- WHO: Sourcegraph Amp.
- WHAT THEY DO: settings docs describe automatically archiving open CLI threads on quit; archived session data persists on disk until manually deleted. Community tool seshr finds/previews sessions across Claude Code, Codex, Amp for manual cleanup.
- SOURCE: https://ampcode.com/docs/cli/settings ; https://github.com/kestermcullough/seshr
- VERDICT: WATCH - a lifecycle nicety, not a disk control.
- ADOPTION NOTE: none beyond 1.4; do not spend hours here.

## CLASS 2 - caps on a single tool call's captured stdout (the monster-A write path)

### 2.1 Claude Code: 30k-char middle truncation
- WHO: Anthropic Claude Code.
- WHAT THEY DO: "By default, the Bash tool captures a maximum of 30,000 characters of output" - middle-truncated (head and tail kept, middle cut); `BASH_MAX_OUTPUT_LENGTH` env var tunes it within a hard ceiling; issue #40100 describes overflow spilled to a temp file the model re-Reads; #19901 docs gap; #17944 env var ignored by a hardcoded threshold after v2.1.2.
- SOURCE: https://code.claude.com/docs/en/tools-reference ; https://code.claude.com/docs/en/env-vars ; https://github.com/anthropics/claude-code/issues/40100 ; https://github.com/anthropics/claude-code/issues/19901 ; https://github.com/anthropics/claude-code/issues/17944
- VERDICT: STEAL - the 30k-char middle-truncate is the industry norm; spill-to-file-plus-re-read preserves rare legit giants.
- ADOPTION NOTE: cap captured stdout per tool call at 30k chars head+tail with a "[truncated N bytes]" marker; log full byte count + spill path, never the body.

### 2.2 OpenHands: 30k hard cap with an explicit clipped marker
- WHO: OpenHands.
- WHAT THEY DO: MAX_CMD_OUTPUT_SIZE = 30,000 chars hard cap on bash outputs with marker "<response clipped><NOTE>Due to the max output limit, only part of the full response has been shown to you.</NOTE>"; prompt-level knob for "the approximate maximum number of characters in the content of an event included in the prompt to the LLM"; openhands-aci MAX_RESPONSE_LEN_CHAR defaults to 16,000 (#7115); known lossy-middle problem (#12353).
- SOURCE: https://docs.openhands.dev/openhands/usage/v0/advanced/V0_configuration-options ; https://github.com/OpenHands/OpenHands/issues/12353 ; https://github.com/OpenHands/OpenHands/issues/7115
- VERDICT: STEAL - independent convergence on 30000 confirms the norm; the marker string is a good contract to copy.
- ADOPTION NOTE: emit the clipped marker into the log file itself so downstream readers know the capture is bounded and by how much.

### 2.3 Codex: ~10KB/256-line truncation + official middle-split rule
- WHO: OpenAI Codex CLI.
- WHAT THEY DO: bash/MCP outputs truncated at roughly 256 lines / 10KB (community-measured; about 10-40KiB serialized per call); the official prompting guide states the rule: keep half the budget for the beginning and half for the end, truncating in the middle; issues #5095/#4550/#5163 request configurability.
- SOURCE: https://www.reddit.com/r/codex/comments/1oyxmys/codex_will_truncate_any_bashmcp_tool_output_to/ ; https://developers.openai.com/cookbook/examples/gpt-5/codex_prompting_guide ; https://github.com/openai/codex/issues/5095 ; https://github.com/openai/codex/issues/4550
- VERDICT: STEAL - head+tail middle truncation stated in an official guide; the shape to implement.
- ADOPTION NOTE: middle-truncate in the capture layer; make the cap a config knob; steer ask templates to redirect giant listings to a file the actor then greps.

### 2.4 THE GAP NOBODY FILLS: context caps without disk caps
- WHO: all three harnesses above.
- WHAT THEY DO: every harness caps what the model sees, yet Codex still wrote 24GiB of repeated payloads to disk sessions (#33735, #41806) because the persistence layer is unbounded. No major harness ships the write-side cap; that is why "solved problem" searches still land on 755GiB bug reports.
- SOURCE: https://github.com/openai/codex/issues/33735 ; https://github.com/openai/codex/issues/41806
- VERDICT: STEAL-ADAPTED - our 309GiB exec dir is the disk side of this exact gap; the steal is implementing the known context-cap discipline at the write layer.
- ADOPTION NOTE: cap BOTH layers: model-context truncation (30k chars) AND write-side per-file max_bytes; the write-side cap is the one that fixes disk.

## CLASS 3 - the canonical bounded-log pattern (system services)

### 3.1 logrotate: the 30-year-old shape
- WHO: logrotate (Linux standard).
- WHAT THEY DO: `size` rotates "only if they grow bigger than size bytes"; `maxsize` rotates on size "even before the additionally specified time interval"; `rotate count` bounds generations (0 removes; -1 never removes); `maxage` drops rotated logs older than N days; `compress` gzips old files; `copytruncate` will "Truncate the original log file to zero size in place after creating a copy" for writers holding the fd open; normally a daily cron job.
- SOURCE: https://man7.org/linux/man-pages/man8/logrotate.8.html ; https://man.archlinux.org/man/logrotate.8.en
- VERDICT: STEAL-ADAPTED - pattern not tool: our per-call files translate interval+size rotation into age+count+byte culling; copytruncate is the live-writer insight.
- ADOPTION NOTE: max_bytes_per_file at write time, max_files_per_dir, compress after rotation; truncate in place for files a live actor still writes, delete only aged orphans.

### 3.2 journald: three-axis budget + vacuum commands
- WHO: systemd-journald.
- WHAT THEY DO: "SystemMaxUse= and RuntimeMaxUse= control how much disk space the journal may use up at most", defaults "10% and ... 15% of the size of the respective file system", each "capped to 4G"; "SystemKeepFree= and RuntimeKeepFree= control how much disk space systemd-journald shall leave free for other uses" (journald uses the smaller of the two limits); "SystemMaxFileSize= ... control how large individual journal files may grow at most", default "one eighth of the values configured with SystemMaxUse= ... capped to 128M"; MaxFileSec default one month; SystemMaxFiles default 100; on-demand shrink: journalctl --vacuum-size= removes oldest archived files until under the size, --vacuum-time= by age.
- SOURCE: https://www.freedesktop.org/software/systemd/man/journald.conf.html ; https://man.archlinux.org/man/journalctl.1.en
- VERDICT: STEAL - total budget + per-file cap + time retention as three independent axes, each with a sane default; over a decade in production.
- ADOPTION NOTE: fleet-wide exec-dir contract enforced by the smith task: total bytes <= max(2% of C:, 4GB) AND C: free >= keep-free floor; per-file cap; oldest-first eviction, never touching the active window's files (their archived-only rule).

### 3.3 Docker json-file driver: rotation opt-in + the noop tripwire
- WHO: Docker Engine (json-file driver).
- WHAT THEY DO: `max-size` "Defaults to -1 (unlimited)"; `max-file` "Defaults to 1"; critically, max-file is "Only effective when max-size is also set." Configure page: "By default, no log-rotation is performed" for json-file and it can lead to "disk space exhaustion"; daemon.json example { "log-driver": "json-file", "log-opts": { "max-size": "10m", "max-file": "3" } } (values must be quoted strings); per-run override --log-opt max-size=10m.
- SOURCE: https://docs.docker.com/engine/logging/drivers/json-file/ ; https://docs.docker.com/engine/logging/configure/
- VERDICT: STEAL - per-unit rotation plus a documented tripwire: a count cap without a size cap is a NOOP.
- ADOPTION NOTE: our byte cap and file-count cap ship together or not at all; also set the daemon.json on the WSL backend now to stop the container-log slice of monster B.

### 3.4 Docker local driver: bounded defaults out of the box
- WHO: Docker Engine (local logging driver).
- WHAT THEY DO: `max-size` "Defaults to 20m"; `max-file` "Defaults to 5"; compression "Enabled by default" - roughly 100MB retained per container with zero configuration.
- SOURCE: https://docs.docker.com/engine/logging/drivers/local/
- VERDICT: STEAL - proof that bounded-plus-compressed defaults cost nothing and prevent the disaster class entirely.
- ADOPTION NOTE: harness default for tool-call stdout: 20MB per-file cap, keep 5, compressed - a ~100MB ceiling per lane instead of 309GiB; this default alone would have prevented the storm.

## CLASS 4 - WSL2 / Docker vhdx compaction (monster B)

### 4.1 Manual compaction: diskpart compact vdisk / Optimize-VHD
- WHO: Microsoft (WSL2 docs) + Docker community practice.
- WHAT THEY DO: WSL2 vhdx files auto-grow (default 1TB max) and never auto-shrink; documented reclamation: `wsl --shutdown` (quit Docker Desktop), free space inside first (`docker system prune`, fstrim in the distro - compaction only reclaims zeroed blocks), then either `Optimize-VHD -Path <vhdx> -Mode Full` (Hyper-V module) or diskpart: `select vdisk file="...vhdx"`, `attach vdisk readonly`, `compact vdisk`, `detach vdisk`. Gotchas: Docker build history can block docker_data.vhdx from shrinking; e2fsck repair has an ERROR_SHARING_VIOLATION case. Reports: ~50GB (Hanselman), 100-200GB+ reclaimed.
- SOURCE: https://learn.microsoft.com/en-us/windows/wsl/disk-space ; https://stackoverflow.com/questions/70946140/docker-desktop-wsl-ext4-vhdx-too-large ; https://www.hanselman.com/blog/shrink-your-wsl2-virtual-disks-and-docker-images-and-reclaim-disk-space ; https://www.reddit.com/r/docker/comments/1nhhlih/cant_shrink_docker_datavhdx/ ; https://github.com/AdnanSattar/docker-desktop-wsl-shrink ; https://github.com/kyto64/WSL2_Disk_Volume_Optimizer
- VERDICT: STEAL - fully solved, standard procedure; only the scheduling is ours.
- ADOPTION NOTE: one PowerShell script (quit Docker, shutdown, prune, compact each vhdx, log bytes reclaimed) on a monthly Task Scheduler job, same registration pattern as scripts/register_census_patrol_task.ps1.

### 4.2 Sparse VHDs: automatic reclaim going forward
- WHO: Microsoft WSL.
- WHAT THEY DO: `wsl --manage <distro> --set-sparse true` marks a distro VHD sparse so it automatically shrinks as files are deleted; .wslconfig [experimental] sparseVhd=true covers newly created VHDs; announced in the WSL September 2023 update. Caveats: reliability reports, the toggle sometimes resets after restarts; for pre-existing bloat: set-sparse false, compact, set-sparse true.
- SOURCE: https://learn.microsoft.com/en-us/windows/wsl/wsl-config ; https://devblogs.microsoft.com/commandline/windows-subsystem-for-linux-september-2023-update ; https://superuser.com/questions/1827953/reclaim-wsl2-disk-space-after-setting-it-to-sparse ; https://bwgjoseph.com/reclaim-disk-space-used-by-docker-desktop-wsl2
- VERDICT: STEAL-ADAPTED - sparse covers WSL distro disks; docker_data.vhdx is Docker-managed and not reliably covered, keep 4.1's scheduled compact for it.
- ADOPTION NOTE: set-sparse true on plain distros now; monthly compact task for docker_data.vhdx.

## CLASS 5 - pagefile sizing (monster C)

### 5.1 Microsoft's own doc: system-managed growth is the bug
- WHO: Microsoft (Windows client performance docs).
- WHAT THEY DO: "By default, page files are system-managed"; when commit charge exceeds 90% of the commit limit the pagefile surges "until the page file reaches three times the size of physical memory or 4 GB, whichever is larger", additionally bounded by "the volume size / 8" but able to grow "to within 1 GB of free space on the volume if necessary for crash dump settings"; minimum "varies based on page file usage history, amount of RAM (RAM / 8, max 32 GB) and crash dump settings". Sizing should follow crash-dump requirement + "peak usage or expected peak usage of the system commit charge", unique per system. Dump minimums: complete dump = "1 x RAM plus 257 MB"; automatic dump (default) = RAM or 32GB, whichever smaller, only after a repeat crash. A DedicatedDumpFile can decouple dumps from pagefile size. Community practice for heavy boxes: fixed initial=max, roughly 1-1.5x RAM.
- SOURCE: https://learn.microsoft.com/en-us/troubleshoot/windows-client/performance/how-to-determine-the-appropriate-page-file-size-for-64-bit-versions-of-windows ; https://learn.microsoft.com/en-us/windows-server/performance/memory-dump-file-options ; rules of thumb (secondary): https://www.ninjaone.com/blog/manage-windows-10-virtual-memory-pagefile , https://www.go-euc.com/page-file-sizing-for-virtualized-environments
- VERDICT: STEAL - the 135GB balloon is documented behavior; the fix is one settings change using MS's own sizing logic.
- ADOPTION NOTE: measure peak commit during a heavy fleet window; set fixed pagefile initial=max at peak+headroom (complete-dump floor RAM+257MB only if kernel dumps are wanted, else small-dump minimum or DedicatedDumpFile); ten minutes, reclaims 135GB permanently.

## CLASS 6 - cache retention (monsters D and E)

### 6.1 Hugging Face hub: first-class cache audit + prune
- WHO: Hugging Face (huggingface_hub CLI).
- WHAT THEY DO: the `hf` CLI (replacing huggingface-cli scan-cache/delete-cache): `hf cache ls` with `--filter "size>30g"`, `--filter "accessed>1y"`, `--sort`, `--format json/csv`, `-q`, `--cache-dir`; `hf cache rm` for repos, revision hashes, or single-file hf:// URIs with `--dry-run` and `--yes`; documented loop `hf cache rm $(hf cache ls --filter "accessed>1y" -q) -y`; `hf cache prune` removes unreferenced revisions, .incomplete files, orphaned blobs; `hf cache verify` checks checksums; cache root via HF_HOME/HF_HUB_CACHE.
- SOURCE: https://huggingface.co/docs/huggingface_hub/guides/cli ; https://huggingface.co/docs/huggingface_hub/guides/manage-cache
- VERDICT: STEAL - last-access filters + dry-run + prune-unreferenced is exactly the shape a model-heavy fleet needs; directly runnable on this box today.
- ADOPTION NOTE: weekly task: `hf cache ls --format json` as the inbox receipt, then the rm loop plus prune; keep an operator allowlist of pinned models (the janitors).

### 6.2 Package managers: the cache-prune verb convention
- WHO: pip / npm / cargo ecosystems.
- WHAT THEY DO: pip ships `pip cache info|list|remove|purge`; npm ships `npm cache clean --force`; cargo gets `cargo cache trim` / cargo-sweep; cross-manager cleanup gists exist. Convention: every cache-owning tool ships an inspect verb plus a guarded purge verb.
- SOURCE: https://barish.me/blog/linguistics-of-package-managers-cli ; https://gist.github.com/idimetrix/205f3760e5da7c94d8f31fa3e826e1da
- VERDICT: STEAL-ADAPTED - convention-level steal: audit and prune verbs for each cache class the harness owns; Temp (monster E) is just another class (age-based delete, skip-if-locked).
- ADOPTION NOTE: `main.py disk-audit` (per-dir bytes + age buckets) and `main.py disk-prune --class hf|temp|toollogs --dry-run` behind one door.

## TOP-5 STEALS (ranked by value per engineering hour)

1. PER-CALL WRITE-SIDE CAP + BOUNDED DEFAULTS (cards 2.1-2.4 + 3.4): 30k chars head+tail middle-truncate with clipped marker at the capture layer, AND a 20MB x 5 compressed per-file/per-count ceiling as the harness default - the 309GiB monster class becomes structurally impossible; about a day of work, zero invention.
2. RETENTION CONTRACT ON THE DAILY SMITH TASK (cards 1.1, 1.4, 3.2): copy Gemini's four-field knob {enabled, maxAge 30d, maxCount, minRetention 1d} plus Claude Code's sweep-at-startup validation semantics, under a journald-shaped fleet budget (total % cap + keep-free floor + per-file cap); the min_age floor is what keeps the sweeper from eating live windows.
3. PAGEFILE FIXED SIZE (card 5.1): Microsoft documents the 3x-RAM surge and the within-1GB-of-free-space growth; set initial=max from measured peak commit; ten minutes of operator config reclaims 135GB permanently.
4. WSL2 COMPACT + SPARSE PAIR (cards 4.1 + 4.2): scripted wsl --shutdown + diskpart compact on docker_data.vhdx as a monthly scheduled task with bytes-reclaimed receipt, plus set-sparse true on plain distros; an hour of work against the 132GB class, standard procedure.
5. HF CACHE ONE-LINER + PRUNE GRAMMAR (card 6.1 with 6.2): `hf cache rm $(hf cache ls --filter "accessed>1y" -q) -y` plus `hf cache prune`, JSON receipt to the inbox; an hour kills the 66GB class and the same audit/prune verb pair becomes our own disk-prune command.

## OWED register

- SWE-agent 100K-char observation cap: secondhand comparison inside OpenHands search context only; primary doc never fetched. Tried one search round; deprioritized because 2.1-2.3 already triangulate the norm.
- Claude Code `bashOutputMaxChars` settings knob: blog claim only, absent from the official docs pages fetched; the documented instrument is BASH_MAX_OUTPUT_LENGTH. Do not cite without verifying.
- Docker Desktop automatic vhdx compaction: no official feature found (forum reports growth with no built-in reclaim); sparse VHD + manual/scheduled compact remains state of practice.
- journald compact-mode nuance on the per-file cap: dropped; only the 10%/15%, 4G, 128M, one-month defaults are quoted from the fetched man page.
- Amp retention beyond archive-on-quit (card 1.8) and Codex maintainer fix status on #34061: recheck before assuming the gaps persist.
