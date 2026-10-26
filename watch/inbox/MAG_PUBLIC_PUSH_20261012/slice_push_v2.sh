#!/bin/bash
# Sliced push of mag-public twin under GitHub's 2GB push cap, with automatic
# GH013 push-protection handling: on a flagged secret, parse the path from
# stderr (trimming GitHub's trailing-space padding!), strip it from the twin
# via filter-repo, refetch base, continue. Base = remote tip.
# Landed 2026-10-12; receipt: watch/inbox/MAG_PUBLIC_PUSH_20261012/RECEIPT.md
set -u
cd "C:/Users/foste/AppData/Local/Temp/mag-public.git" || exit 1
VENV_PY="C:/Users/foste/Documents/projects/local_sovereign_agent/.venv/Scripts/python.exe"

fetch_base () {
  git fetch github mag-public:refs/remotes/github/mag-public 2>/dev/null \
    || echo github/master
}

strip_paths () {
  # $@ = paths to remove from twin history (mag-public only)
  local args=()
  for p in "$@"; do args+=(--path "$p"); done
  "$VENV_PY" -m git_filter_repo --force --invert-paths "${args[@]}" --refs mag-public
}

round=0
while : ; do
  round=$(( round + 1 ))
  base_ref=$(fetch_base)
  mapfile -t commits < <(git rev-list --reverse github/mag-public..mag-public 2>/dev/null)
  total=${#commits[@]}
  [ "$total" -eq 0 ] && { echo "DONE: remote up to date at round $round"; break; }
  echo "== round $round: $total commits left after remote tip"

  K=3; i=0; fails=0
  while [ "$i" -lt "$total" ]; do
    step=$(( (total - i) < K ? (total - i) : K ))
    target=$(( i + step - 1 ))
    sha="${commits[$target]}"
    errf="serr.log"
    echo "-- slice $((i+1))..$((target+1))/$total -> ${sha:0:10} (K=$K)"
    if git push github "$sha:refs/heads/mag-public" 2>"$errf"; then
      i=$(( target + 1 )); fails=0
    elif grep -q GH013 "$errf"; then
      echo "PUSH PROTECTION hit:"
      grep -oE 'path: .*' "$errf" | sed -E 's/^path: //; s/[[:space:]]+$//; s/:[0-9]+$//' | sort -u > paths_to_strip.txt
      cat paths_to_strip.txt
      mapfile -t sp < paths_to_strip.txt
      strip_paths "${sp[@]}" || { echo "FATAL: strip failed"; exit 1; }
      rm -f paths_to_strip.txt
      break   # restart outer loop: base refetch picks up new hashes after remote tip
    else
      fails=$(( fails + 1 ))
      echo "   push failed: $(grep -m1 'error\|fatal' "$errf" | head -c 120)"
      if [ "$fails" -ge 2 ]; then
        K=$(( K / 2 )); [ "$K" -lt 1 ] && K=1
        fails=0
        [ "$K" -eq 1 ] && [ "$step" -le 1 ] && { echo "FATAL: single-commit push failing"; exit 1; }
      fi
      sleep 3
    fi
  done
  [ "$round" -ge 80 ] && { echo "FATAL: round limit"; exit 1; }
done

git push github mag-public 2>&1 | tail -1
echo "=== FINAL REMOTE STATE ==="
git ls-remote github refs/heads/mag-public
git rev-parse mag-public
