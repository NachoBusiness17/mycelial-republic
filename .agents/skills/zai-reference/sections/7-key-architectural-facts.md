## 7. KEY ARCHITECTURAL FACTS

1. **5.3-flash is multimodal; 5.3-full is text-only.** The cheap model SEES.
2. **5.3-flash gets 3× the coding plan quota** of 5.3-full (lower multipliers).
3. **5.3 and 5.3-flash: thinking cannot be disabled.** Only 4.7-flash and below can turn it off.
4. **The free models (4.7-flash, 4.5-flash, 4.6v-flash) are free at ALL tiers** — no credits consumed.
5. **Off-peak (weekends all day, weekdays off-peak hours) = 50% credits.**
6. **Cached input is 50% of standard input price** — the standing wave halves the cost even on paid models.
7. **Model routing:** requests for 5.2/5.1 → 5.3; 5-turbo/4.7 → 5.3-flash. The API silently upgrades.
8. **5.3-flash was tested as "ox-alpha"** on OpenCode and OpenRouter — most popular model of the week.
9. **Native MCP servers included:** Vision, Web Search, Web Reader, Zread — free with all plans.
10. **Context window on all current models: 1M tokens** (except 4.7-flash at 200K, 4.5 at 128K).
