#!/usr/bin/env bash
# scripts/safe_commit.sh - serialized commit helper for the shared estate tree.
#
# Why this exists: two stale .git/index.lock files were removed by hand on
# 2026-10-03 (one 11h old, one 38min old, neither with an owner process alive)
# after lane commit races - multiple seats running bare "git add + git commit"
# against the same tree with no serialization. This is the commit-queue law
# that was named but never built (gala build-it-all, commit-queue lane).
#
# Contract:
#   1. If .git/index.lock exists and is FRESH, wait up to SAFE_COMMIT_WAIT
#      seconds (default 60) for it to clear.
#   2. A lock is STALE when older than SAFE_COMMIT_STALE_SECS (default 300,
#      i.e. 5 min). A stale lock is removed when we can prove no process
#      holds it:
#        - no git process alive on the host (the ask's spec condition), or
#        - on Windows/MSYS only: a delete attempt of the lock fails with
#          "Device or resource busy" while a live git holds the lock (git's
#          CRT handle has no FILE_SHARE_DELETE - measured 2026-10-03 on a
#          live estate lock), so a delete attempt that SUCCEEDS proves the
#          lock is ownerless debris even while foreign lanes run git in
#          other repositories. On POSIX no such proof exists (unlink
#          always succeeds), so there the no-git-process check is required
#          and a foreign git means we wait, never steal.
#      A fresh lock is always waited on, never stolen.
#   3. Runs git add + git commit with the message as arg. Paths given after
#      "--" are passed to BOTH git add and git commit, so only the named
#      paths land (the safe mode on a shared tree - "git commit -- paths"
#      ignores unrelated staged files). With no "--" paths it runs
#      "git add -A" - only use that mode when you own the whole tree.
#   4. Cleans up on failure and retries: a failed add/commit whose lock is
#      provably ownerless (same stale/ownership rules, created during this
#      run) is removed and the add+commit retried, up to SAFE_COMMIT_ATTEMPTS
#      attempts (default 5), before giving up.
#
# Usage:
#   scripts/safe_commit.sh -m "commit message"               # add -A mode
#   scripts/safe_commit.sh -m "commit message" -- path1 path2  # path-limited
#
# Env:
#   SAFE_COMMIT_WAIT        seconds to wait on a fresh lock   (default 60)
#   SAFE_COMMIT_STALE_SECS  lock age that makes it stale      (default 300)
#   SAFE_COMMIT_ATTEMPTS    add+commit attempts               (default 5)

set -u

WAIT_SECS="${SAFE_COMMIT_WAIT:-60}"
STALE_SECS="${SAFE_COMMIT_STALE_SECS:-300}"
MAX_ATTEMPTS="${SAFE_COMMIT_ATTEMPTS:-5}"
POLL_INTERVAL=1

msg() { printf '[safe_commit] %s\n' "$*" >&2; }
die() { msg "ERROR: $*"; exit 1; }

usage() {
  cat >&2 <<'USAGE'
Usage:
  scripts/safe_commit.sh -m "commit message"               # git add -A + commit
  scripts/safe_commit.sh -m "commit message" -- p1 [p2 ..] # add+commit ONLY p1 p2
Env:
  SAFE_COMMIT_WAIT (default 60)  SAFE_COMMIT_STALE_SECS (default 300)
  SAFE_COMMIT_ATTEMPTS (default 5)
A stale lock is removed only when provably ownerless: no git process alive,
or (Windows/MSYS) a delete attempt succeeds because a live git would refuse
it. A fresh lock is waited on, never stolen.
USAGE
}

GIT_DIR="$(git rev-parse --absolute-git-dir 2>/dev/null)" \
  || GIT_DIR="$(git rev-parse --git-dir 2>/dev/null)" \
  || die "not inside a git repository"
LOCK="$GIT_DIR/index.lock"

is_windows() {
  case "$(uname -s)" in
    MINGW*|MSYS*|CYGWIN*) return 0 ;;
    *) return 1 ;;
  esac
}

now_s() { date +%s; }

lock_mtime() {
  stat -c %Y "$LOCK" 2>/dev/null || stat -f %m "$LOCK" 2>/dev/null || echo ""
}

# 0 = a git process may be alive. Fails closed: any probe error answers
# "alive" so the process-list condition is never satisfied on a guess.
git_procs_alive() {
  if is_windows; then
    local tl
    tl="$(tasklist //FO CSV //NH 2>/dev/null)"
    if [ -z "$tl" ]; then
      msg "tasklist probe returned nothing; assuming a git process may be alive"
      return 0
    fi
    printf '%s\n' "$tl" | grep -qiE '"git[^"]*\.exe"'
  else
    if command -v pgrep >/dev/null 2>&1; then
      pgrep -x git >/dev/null 2>&1
    else
      msg "no pgrep available; assuming a git process may be alive"
      return 0
    fi
  fi
}

# Attempt to remove the lock. Returns 0 iff the lock is gone afterwards.
# On a live git-held Windows lock this fails with "Device or resource busy",
# which is exactly the ownership proof we want.
rm_lock_quiet() {
  rm -f -- "$LOCK" 2>/dev/null
  [ ! -e "$LOCK" ]
}

# Remove a stale lock when provably ownerless. Returns 0 iff removed.
#   path A (spec): no git process alive anywhere -> remove.
#   path B (Windows only): git processes exist, but the delete attempt
#          succeeds, proving no process holds this lock -> remove.
#   path C: delete attempt refused -> a live process holds it -> keep it.
try_remove_stale_lock() {
  local age="$1"
  if ! git_procs_alive; then
    if rm_lock_quiet; then
      msg "removing stale index.lock (age ${age}s >= ${STALE_SECS}s, no git process alive)"
      return 0
    fi
    msg "stale index.lock (age ${age}s) resisted deletion despite empty git process list - leaving it"
    return 1
  fi
  if is_windows && rm_lock_quiet; then
    msg "removing stale index.lock (age ${age}s; delete attempt succeeded, so no process holds it despite git processes elsewhere)"
    return 0
  fi
  if is_windows; then
    msg "stale index.lock (age ${age}s) is held by a live process (delete refused) - waiting"
  else
    msg "stale index.lock (age ${age}s) while git processes are alive on POSIX - waiting, never stealing"
  fi
  return 1
}

# Returns 0 when the way is clear (no lock). Returns 1 when a lock outlived
# WAIT_SECS without ever being provably ownerless.
wait_for_lock() {
  local start; start="$(now_s)"
  while [ -e "$LOCK" ]; do
    local mt age
    mt="$(lock_mtime)"
    if [ -n "$mt" ]; then age=$(( $(now_s) - mt )); else age=0; fi
    if [ "$age" -ge "$STALE_SECS" ]; then
      try_remove_stale_lock "$age" && return 0
    fi
    if [ $(( $(now_s) - start )) -ge "$WAIT_SECS" ]; then
      msg "index.lock still held after ${WAIT_SECS}s (lock age ${age}s) - refusing to steal a lock that may be owned"
      return 1
    fi
    sleep "$POLL_INTERVAL"
  done
  return 0
}

# Remove lock debris left by OUR OWN failed git run: created during this run
# (mtime >= DEBRIS_FROM) and provably ownerless by the same rules as above.
clean_own_debris() {
  [ -e "$LOCK" ] || return 0
  local mt
  mt="$(lock_mtime)"
  if [ -z "$mt" ] || [ "$mt" -lt "$DEBRIS_FROM" ]; then
    return 0
  fi
  if ! git_procs_alive; then
    if rm_lock_quiet; then
      msg "removing index.lock debris from our failed git run (mtime >= run start, no git process alive)"
    fi
    return 0
  fi
  if is_windows && rm_lock_quiet; then
    msg "removing index.lock debris from our failed git run (mtime >= run start; delete attempt succeeded, no process holds it)"
  fi
  return 0
}

announce_sha() {
  local sha
  sha="$(printf '%s\n' "$1" | sed -nE 's/^\[[^]]* ([0-9a-f]{7,})\].*/\1/p' | head -n 1)"
  [ -n "$sha" ] || sha="$(git rev-parse --short HEAD 2>/dev/null || echo UNKNOWN)"
  printf 'committed %s\n' "$sha"
}

# ---- argument parsing ----
COMMIT_MSG=""
PATHS=()
GAVE_DASH_DASH=0
while [ $# -gt 0 ]; do
  case "$1" in
    -m)  [ $# -ge 2 ] || die "-m needs a message argument"
         COMMIT_MSG="$2"; shift 2 ;;
    -m*) COMMIT_MSG="${1#-m}"; shift ;;
    --)  shift; GAVE_DASH_DASH=1; PATHS=("$@"); break ;;
    -h|--help) usage; exit 0 ;;
    *)   usage; die "unknown argument: $1" ;;
  esac
done
[ -n "$COMMIT_MSG" ] || { usage; die "a commit message is required (-m \"...\")"; }
if [ "$GAVE_DASH_DASH" = "1" ] && [ "${#PATHS[@]}" -eq 0 ]; then
  die "-- given but no paths followed it"
fi

# ---- main: wait, commit, retry on failure, clean own debris ----
DEBRIS_FROM="$(now_s)"

attempt=0
while :; do
  wait_for_lock || exit 1
  if [ "${#PATHS[@]}" -gt 0 ]; then
    set -- "${PATHS[@]}"
    if git add -- "$@" && { out="$(git commit -m "$COMMIT_MSG" -- "$@" 2>&1)"; } ; then
      printf '%s\n' "$out"
      announce_sha "$out"
      exit 0
    fi
  else
    if git add -A && { out="$(git commit -m "$COMMIT_MSG" 2>&1)"; }; then
      printf '%s\n' "$out"
      announce_sha "$out"
      exit 0
    fi
  fi
  attempt=$((attempt + 1))
  clean_own_debris
  if [ "$attempt" -ge "$MAX_ATTEMPTS" ]; then
    die "commit did not land after $attempt attempt(s); see git output above"
  fi
  msg "git add/commit failed (attempt $attempt/$MAX_ATTEMPTS) - waiting for any lock, then retrying"
  sleep 1
done
