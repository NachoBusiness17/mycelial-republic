#!/usr/bin/env bash
# MICKEY-17 REPRINT LAUNCHER — wave cycle 3 (WAVE 7 wide), tender: Mag seat, 2026-09-11.
#
# Usage:  bash watch/WAVE_C7/spawn_reprint.sh <slot> "<one-line NEXT task>"
#
# Called BY THE WORKER ITSELF at the end of its lane, before it folds. It:
#   1. appends a durable queue row to watch/WAVE_C7/reprint_queue.jsonl (survives a dead launch;
#      the tender drains the queue, so a NEXT line is never lost),
#   2. writes the reprint prompt from a heredoc template,
#   3. starts ONE detached reprint worker (depth 1) after a per-slot stagger,
#      logging to watch/WAVE_C7/reprint_<slot>_out.log.
#
# DEPTH CAP 1: the reprint does the bounded task, files its own card, appends one ledger row
# (worker string "<slot>-r1") and DOES NOT spawn again.
set -u
ROOT="C:/Users/foste/Documents/projects/local_sovereign_agent"
cd "$ROOT" || exit 1
SLOT="${1:-}"
NEXT="${2:-}"
if [ -z "$SLOT" ] || [ -z "$NEXT" ]; then
  echo "usage: bash watch/WAVE_C7/spawn_reprint.sh <slot> \"<one-line next task>\"" >&2
  exit 2
fi

STAGE="$ROOT/watch/WAVE_C7"
mkdir -p "$STAGE"
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
Q="$STAGE/reprint_queue.jsonl"
P="$STAGE/reprint_${SLOT}_prompt.md"
L="$STAGE/reprint_${SLOT}_out.log"
CARD="MICKEY17_S${SLOT}_R1_20260911.md"
MODEL='glm-4.7[1m]'
# stagger: reprints do not all wake at once (bounded width discipline)
DELAY=$(( 90 + 60 * SLOT ))

# 0. one-shot guard — never launch the same slot's reprint twice
if [ -f "$STAGE/reprint_${SLOT}_fired" ]; then
  echo "REFUSED: reprint for slot $SLOT already fired ($STAGE/reprint_${SLOT}_fired). Depth cap 1 — fold."
  exit 3
fi

# 1. durable queue row FIRST (cheap, always lands, even if the launch below dies)
esc=${NEXT//\\/\\\\}
esc=${esc//\"/\\\"}
printf '{"ts":"%s","slot":"%s","worker":"w7s%s-r1","task":"%s","status":"queued"}\n' \
  "$TS" "$SLOT" "$SLOT" "$esc" >> "$Q"

# 2. reprint prompt
cat > "$P" <<EOF
You are a MICKEY-17 REPRINT — WAVE_DEPTH=1 — in the local_sovereign_agent fleet wave, cycle 3
(WAVE 7 wide). You were launched by wave worker slot ${SLOT} on the bounded task IT chose as the
next step from its own lane. Repo (and your cwd): C:/Users/foste/Documents/projects/local_sovereign_agent.

Read first (they bind you): watch/NIGHT_FOLD_20260911.md and
watch/WAVE_CYCLE_GENETICS_20260911.md, plus the parent card watch/inbox/*_20260911.md that names
lane ${SLOT}'s work if you need its evidence.

YOUR BOUNDED TASK (chosen by your parent, one line — do exactly this, do not widen it):
${NEXT}

Date now: ${TS}. Dating method: ts from this prompt (ISO Z, UTC); file mtimes are local.

BOUNDS: read-only EXCEPT (1) your one card watch/inbox/${CARD}, (2) ONE appended line in
watch/WAVE_LEDGER.jsonl, (3) files the bounded task itself requires — backup-first (.bak beside the
file) with a re-parse/round-trip after any write to an existing file. No chain writes (the verkle
chain is read-only). No credentials echoed (names only, never values). No network posting. \$0 — free
lane only, no paid API calls.

PROTOCOL: absorb first and cross-link the absorbed sources in your card's first 5 lines; measure
don't assume (enumerate witnesses beyond the named ones, one schema-peek row before any field-level
parse of an unfamiliar .jsonl, name the dating method on every count); seeded + denominated samples
(carry the denominator, "widen before promoting to law"); tri-state verdicts with a FALSIFIERS
section; no silent pass (every dead end is named); assert-then-write on any estate fold; end with one
CYCLE GENETICS paragraph. Card under ~120 lines, dense, evidence-cited, plain English.

LEDGER ROW (same turn as the card): fields {ts ISO Z, lane, worker, did, found, remains, prev, hash};
worker = "w7s${SLOT}-r1"; prev = the hash field of the file's current last line, read immediately
before the append (retry once if it moved); hash = first 16 hex of sha256(prev+"|"+ts+"|"+lane+"|"+worker),
utf-8. Single >> redirect; never rewrite rows.

DEPTH CAP 1 — HARD: you are a reprint. You DO NOT launch another reprint and you do not run
spawn_reprint.sh. Write your NEXT: line into your card, then fold.

Print as the final line of your reply: NEXT: <your one-line heir, for the record only, not launched>.
EOF

# 3. detached, staggered launch (survives the parent worker folding)
touch "$STAGE/reprint_${SLOT}_fired"
(
  sleep "$DELAY"
  cd "$ROOT" || exit 1
  timeout 3600 claude -p "$(cat "$P")" --model "$MODEL" --dangerously-skip-permissions >> "$L" 2>&1
  echo "EXIT:$? $(date -u +%Y-%m-%dT%H:%M:%SZ)" >> "$L"
) >/dev/null 2>&1 &
RPID=$!
echo "$RPID reprint-slot-${SLOT} delay=${DELAY}s card=${CARD}" >> "$STAGE/reprint_pids.txt"
echo "LAUNCHED reprint slot ${SLOT} pid=${RPID} delay=${DELAY}s task=${NEXT}"
