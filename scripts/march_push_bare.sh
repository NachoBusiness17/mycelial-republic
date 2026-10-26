#!/bin/bash
# march_push_bare - chunked push of the CLEANED branch from the bare clone.
# The full-history pack 500s at GitHub's edge; small packs pass. Each
# success sticks; the loop resumes from the remote tip on rerun.
set -u
GD="/c/Users/foste/mag_rewrite_tmp.git"
BR="mag/run-beta1-factory-build-audi-20260806T231709Z"
STEP="${1:-50}"
mapfile -t shas < <(git --git-dir="$GD" rev-list --reverse "$BR")
n=${#shas[@]}
echo "total cleaned commits: $n (step $STEP)"
remote_tip=$(git --git-dir="$GD" ls-remote github "refs/heads/$BR" | cut -f1)
i=0
if [ -n "$remote_tip" ]; then
  for idx in "${!shas[@]}"; do
    if [ "${shas[$idx]}" = "$remote_tip" ]; then i=$((idx + 1)); break; fi
  done
  echo "remote tip at index $i - resuming"
fi
fail=0
while [ "$i" -lt "$n" ]; do
  j=$((i + STEP - 1)); [ "$j" -ge "$n" ] && j=$((n - 1))
  sha="${shas[$j]}"
  d=$(git --git-dir="$GD" log -1 --format=%ad --date=short "$sha")
  if git --git-dir="$GD" push --force github "${sha}:refs/heads/$BR" > /tmp/push_bare.log 2>&1; then
    echo "OK [$((j + 1))/$n] $d ${sha:0:10}"
    i=$((j + 1))
  else
    small=$((i + 24)); [ "$small" -ge "$n" ] && small=$((n - 1))
    sha2="${shas[$small]}"
    echo "retry small [$((small + 1))/$n]"
    if git --git-dir="$GD" push --force github "${sha2}:refs/heads/$BR" > /tmp/push_bare.log 2>&1; then
      echo "OK-small [$((small + 1))/$n] ${sha2:0:10}"
      i=$((small + 1))
    else
      echo "HARD FAIL at $((i + 1)) - see /tmp/push_bare.log"
      tail -3 /tmp/push_bare.log
      fail=1
      break
    fi
  fi
done
echo "MARCH DONE fail=$fail"
exit $fail
