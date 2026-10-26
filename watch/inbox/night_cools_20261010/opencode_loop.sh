#!/usr/bin/env bash
# OpenCode headless builder loop: mine the repo for cool upgrade ideas and BUILD one.
# Bounded: 5 cycles x ~12min. Env sourced from the estate .env (ZAI_API_KEY).
cd "$(dirname "$0")"
OC_OUT="opencode_builds.md"
: > "$OC_OUT"
export $(grep -E "^(ZAI_API_KEY)=" /c/Users/foste/Documents/projects/local_sovereign_agent/.env | xargs)

ASKS=(
"Read the sibling grokbot_finds.md if present, else pick any instrument in this repo that sounds cool (disk_smith, babelfish, pheromone). Propose ONE small delightful upgrade a night-shift operator would grin at. Do not code - describe it in 8 lines with file paths."
"Design (no code) a tiny 'cools dashboard' static HTML page for this folder: reads the finds files and renders them as trading cards. 10 lines of spec max."
"Now BUILD the smallest version of the thing you proposed: a single new file in this folder, self-contained, no deps. Test it runs. Bank what you built."
"Review what you built last cycle. Make it cooler by ONE increment (better output, a tiny easter egg, ASCII art header). Re-test."
"Write a 6-line poem about a fleet of sovereign agents mining cool shit at night while their operator sleeps. Append it to opencode_builds.md as the sign-off."
)

echo "# OPENCODE BUILDER LOG $(date -u +%Y-%m-%dT%H:%MZ)" >> "$OC_OUT"
for i in "${!ASKS[@]}"; do
  echo -e "\n--- cycle $((i+1))/5 $(date -u +%H:%MZ) ---" >> "$OC_OUT"
  opencode run -m zai/glm-5.3 "${ASKS[$i]}" >> "$OC_OUT" 2>&1
  [ "$i" -lt 4 ] && sleep 600
done
echo -e "\n# OPENCODE LOOP COMPLETE $(date -u +%H:%MZ)" >> "$OC_OUT"
