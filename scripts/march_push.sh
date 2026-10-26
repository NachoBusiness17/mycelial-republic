#!/bin/bash
# march_push - push a long--lived branch to GitHub in small commit chunks.
# The 408 law (2026-10-16): a 1,028-commit branch over HTTPS dies mid-pack
# ("unexpected disconnect"); small chunks land, each success sticks.
# Usage: bash scripts/march_push.sh [chunk_size]
set -u
cd "C:/Users/foste/Documents/projects/local_sovereign_agent"
BR="mag/run-beta1-factory-build-audi-20260806T231709Z"
STEP="${1:-50}"
mapfile -t shas < <(git rev-list --reverse HEAD)
n=${#shas[@]}
echo "total commits: $n (step $STEP)"
# resume from the remote tip if the branch already carries commits
remote_tip=$(git ls-remote github "refs/heads/$BR" | cut -f1)
i=0
if [ -n "$remote_tip" ]; then
  for idx in "${!shas[@]}"; do
    if [ "${shas[$idx]}" = "$remote_tip" ]; then i=$((idx + 1)); break; fi
  done
  echo "remote tip found at index $((i)) - resuming (remote head ${remote_tip:0:10})"
fi
fail=0
while [ "$i" -lt "$n" ]; do
  j=$((i + STEP - 1)); [ "$j" -ge "$n" ] && j=$((n - 1))
  sha="${shas[$j]}"
  d=$(git log -1 --format=%ad --date=short "$sha")
  # the mirrors organ ticks constantly: re-seal by name before EVERY push
  .venv/Scripts/python.exe tools/config_seal.py update --by zcode-seat-20261016 --note "mirrors tick re-seal (march push)" > /dev/null 2>&1
  if git push github "${sha}:refs/heads/$BR" > /tmp/push_chunk.log 2>&1; then
    echo "OK [$((j + 1))/$n] $d ${sha:0:10}"
    i=$((j + 1))
  else
    small=$((i + 24)); [ "$small" -ge "$n" ] && small=$((n - 1))
    sha2="${shas[$small]}"
    echo "retry small at [$((i + 1))..$((small + 1))]"
    .venv/Scripts/python.exe tools/config_seal.py update --by zcode-seat-20261016 --note "mirrors tick re-seal (march push small)" > /dev/null 2>&1
    if git push github "${sha2}:refs/heads/$BR" > /tmp/push_chunk.log 2>&1; then
      echo "OK-small [$((small + 1))/$n] ${sha2:0:10}"
      i=$((small + 1))
    else
      echo "HARD FAIL at index $i - see /tmp/push_chunk.log"
      fail=1
      break
    fi
  fi
done
echo "MARCH DONE fail=$fail landed_through=${shas[$((i - 1))]:0:12}"
exit $fail
