#!/bin/bash
# Publish twin pipeline: copy main repo object store -> bare temp clone,
# strip >100MB blobs + private/legal paths from mag-public only, push.
# Landed 2026-10-12; receipt: watch/inbox/MAG_PUBLIC_PUSH_20261012/RECEIPT.md
set -x
MAIN="C:/Users/foste/Documents/projects/local_sovereign_agent"
TGT="C:/Users/foste/AppData/Local/Temp/mag-public.git"

# 1. robocopy the object store (multithreaded; rc 0-7 = success)
rm -rf "$TGT"
robocopy "C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent\\.git" "C:\\Users\\foste\\AppData\\Local\\Temp\\mag-public.git" //E //MT:16 //NFL //NDL //NJH //NJS //R:1 //W:1
rc=$?
echo "ROBOCOPY rc=$rc"
[ "$rc" -le 7 ] || { echo "FATAL robocopy rc=$rc"; exit 1; }

# 2. make it a proper bare repo
git -C "$TGT" config core.bare true
git -C "$TGT" config --unset core.worktree 2>/dev/null
git -C "$TGT" rev-parse mag-public || { echo "FATAL twin branch missing"; exit 1; }

# 3. rewrite mag-public only (fresh dir, no prompts; --refs => no gc, no reset)
#    NOTE: delete $TGT/filter-repo first if the source .git carried a stale
#    already_ran marker (robocopy copies it; it triggers an interactive prompt).
cd "$TGT" || exit 1
"$MAIN/.venv/Scripts/python.exe" -m git_filter_repo --force \
  --strip-blobs-bigger-than 100M \
  --invert-paths \
  --path attic \
  --path watch/inbox/mrpool_export \
  --path tools/godot \
  --path corpus/papers_reference_nonredistributable \
  --path dashboard/data \
  --path memory/biography_backup_20260825 \
  --refs mag-public || { echo "FATAL filter-repo"; exit 1; }

# 4. verify: commit count, biggest remaining blob, main repo untouched
echo "TWIN commit count: $(git rev-list --count github/master..mag-public 2>/dev/null || git rev-list --count origin/master..mag-public 2>/dev/null || echo range-ref-missing)"
git rev-list --objects github/master..mag-public 2>/dev/null | git cat-file --batch-check='%(objecttype) %(objectsize) %(rest)' 2>/dev/null | awk '$1=="blob"{if($2>m){m=$2;p=$3}; if($2>104857600)c++} END{printf "TWIN max blob: %.1fMB (%s); blobs>100MB remaining: %d\n", m/1048576, p, c+0}'
echo "MAIN mag tip still: $(git -C "$MAIN" rev-parse HEAD)"
