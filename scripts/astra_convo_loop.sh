#!/usr/bin/env bash
# ASTRA CONVO LOOP — paced, saloned, until complete.
# Operator GO 09-11 (dinner mandate): "run the astra convo paced and saloned
# then responded in a loop until complete."
# Pacing: one codex fire per round, 5-min settle between rounds, quota wall =
# 30-min backoff + one retry, then honest halt. Salon: kabuki cast ($0) folds
# each of Astra's answers before the next dispatch is composed.
# Stop: touch watch/ASTRA_LOOP_STOP to halt between rounds. Max 4 rounds.
set -u
cd "C:/Users/foste/Documents/projects/local_sovereign_agent"
RUN=memory/runs/astra_convo_20260911
mkdir -p "$RUN"
DISPATCH="$RUN/DISPATCH_1.txt"
ANSW=""; FOLD=""

for N in 1 2 3 4; do
  [ -f watch/ASTRA_LOOP_STOP ] && echo "STOP file seen — halting between rounds." && break

  # compose the dispatch
  D="$RUN/DISPATCH_${N}.txt"
  if [ "$N" -eq 1 ]; then
    cp "$DISPATCH" "$D"
  else
    {
      echo "CARRY (your own previous answer, verbatim — carry your blob forward):"
      echo "--------------------------------------------------------------"
      cat "$RUN/ANSWER_$((N-1)).md"
      echo "--------------------------------------------------------------"
      echo "FLEET SALON FOLD on your answer (three chairs, plain English):"
      echo "--------------------------------------------------------------"
      cat "$RUN/FOLD_$((N-1)).md"
      echo "--------------------------------------------------------------"
      cat "$RUN/DISPATCH_NEXT_INSTRUCTION.txt"
    } > "$D"
  fi

  # fire, paced
  echo "[ASTRA LOOP $N] firing codex ($(date -u +%H:%M:%SZ))..."
  timeout 420 codex exec --skip-git-repo-check - < "$D" > "$RUN/ANSWER_${N}.md" 2>&1
  RC=$?
  ANSW="$RUN/ANSWER_${N}.md"
  if ! grep -qi "quota\|usage limit\|rate limit" "$ANSW"; then
    echo "[ASTRA LOOP $N] answer landed ($(wc -c < "$ANSW") bytes)."
  else
    echo "[ASTRA LOOP $N] walled — 30-min backoff, one retry."
    sleep 1800
    timeout 420 codex exec --skip-git-repo-check - < "$D" > "$ANSW" 2>&1
    if grep -qi "quota\|usage limit\|rate limit" "$ANSW"; then
      echo "[ASTRA LOOP $N] still walled after retry — halting honestly. State kept."
      echo "WALLED at round $N" > "$RUN/STATE.txt"
      break
    fi
  fi
  [ $RC -ne 0 ] && [ ! -s "$ANSW" ] && echo "[ASTRA LOOP $N] empty answer — halting." && break

  # salon the answer ($0 kabuki cast, 3 chairs)
  python -m mag.kabuki_salon salon "Three chairs fold Astra's latest answer (below). Extract plain-English: (a) what she ENHANCED in our registration-bundle drafts, (b) what she DISPUTED or corrected, (c) the ONE next ask that most improves the bundle. No flattery, cite her lines. --- ASTRA'S ANSWER: $(cat "$ANSW")" --actors 3 > "$RUN/FOLD_${N}.md" 2>&1
  FOLD="$RUN/FOLD_${N}.md"
  echo "[ASTRA LOOP $N] salon fold done ($(wc -c < "$FOLD") bytes)."

  sleep 300
done
echo "[ASTRA LOOP] complete or halted — state in $RUN. Morning report carries it."
