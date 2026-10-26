#!/usr/bin/env bash
# Night cools miner: two bounded loops (grokbot + opencode) per operator order
# 2026-10-10 "launch opencode headless and grokbot to mine for cool shit enjoy and build out cool shit".
# Bounded: GROK_CYCLES x 7min and OC_CYCLES x 12min, then both exit (never unbounded).
cd "$(dirname "$0")"
GROK_OUT="grokbot_finds.md"
OC_OUT="opencode_builds.md"
: > "$GROK_OUT"; : > "$OC_OUT"

THEMES=(
"weird frontier AI research from the last 48h that almost nobody noticed - one find, why it is cool, link"
"a wild open-source repo that shipped this week - what it does, why it is underrated, link"
"an X post from the last 3 days with an idea worth stealing for a personal sovereign AI agent - verbatim quote + why"
"an unexpected cross-domain steal: something from biology/physics/music/old craft that maps onto AI agent design"
"a tool, technique or trick for local-first AI that changed this month - what and why it matters"
"one math or geometry idea (recent or ancient) that would make an AI agent instrument cooler - concrete"
"something hilarious or beautiful from AI twitter this week worth banking"
"an automation or agent trick from any community (r/selfhosted, HN, discords) that a home sovereign agent fleet should steal"
)

echo "# GROKBOT NIGHT MINES $(date -u +%Y-%m-%dT%H:%MZ)" >> "$GROK_OUT"
for i in "${!THEMES[@]}"; do
  echo -e "\n--- cycle $((i+1))/8 $(date -u +%H:%MZ) ---" >> "$GROK_OUT"
  echo "THEME: ${THEMES[$i]}" >> "$GROK_OUT"
  grok -p "You are mining for a sovereign AI agent estate at night. Theme: ${THEMES[$i]}. Return ONE best find: title, one-paragraph why-it-is-cool, the link, and one concrete way the estate could use it tonight. No lists of five - pick one and commit." >> "$GROK_OUT" 2>&1
  [ "$i" -lt 7 ] && sleep 420
done
echo -e "\n# GROKBOT LOOP COMPLETE $(date -u +%H:%MZ)" >> "$GROK_OUT"
