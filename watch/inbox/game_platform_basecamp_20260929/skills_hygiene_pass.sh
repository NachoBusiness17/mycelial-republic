#!/bin/bash
# Skills hygiene pass 2026-09-29: em-dash law across house skills + frontmatter quote fix.
# Em-dash replacement is context-safe here: " — " (spaced break) -> " - "; ranges "1—3" -> "1-3".
set -e
REPO="/c/Users/foste/Documents/projects/local_sovereign_agent"
HOUSE_U="/c/Users/foste/.agents/skills"
ZU="/c/Users/foste/.zcode/skills"
cd "$REPO"
fixed=0
for f in $(grep -rl $'\u2014' .agents/skills --include='*.md'); do
  sed -i 's/ \u2014 / - /g; s/\u2014/-/g' "$f"
  fixed=$((fixed+1)); echo "em-dash stripped: $f"
done
for f in $(grep -rl $'\u2014' "$HOUSE_U" "$ZU" --include='*.md' 2>/dev/null); do
  sed -i 's/ \u2014 / - /g; s/\u2014/-/g' "$f"
  fixed=$((fixed+1)); echo "em-dash stripped: $f"
done
# frontmatter quoting bug: name: "x" -> name: x
for f in "$ZU/imagegen/SKILL.md" "$ZU/openai-docs/SKILL.md"; do
  sed -i 's/^name: "\([^"]*\)"/name: \1/' "$f"
  echo "frontmatter unquoted: $f"
done
echo "TOTAL_FIXED=$fixed"
