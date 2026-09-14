# DECK SETUP CARD — 8 decks, 16 columns, ~5 minutes (2026-09-04)

One-time manual setup on X Pro (the option-list click defeats automation — that is why this
card is paste-and-click). Sources: DECK QUERIES v2 (TRI_PARTY_ARCHITECTURE_20260904.md) +
the X Pro steal (STEAL_XPRO_HARVEST_20260904.md). Deck ids: X_SCOUT_DOCTRINE_20260904.md.

**THE CLICK PATH — same for every column below:**
open the deck → **+ Add column** → **Search** → paste the query → **click the query option**
in the dropdown (click the option itself, not Enter — that click is what loads the column).

**PAIR LAW:** each deck gets TWO adjacent columns — RAW then FILLED. First reports carry
zero engagement, so the RAW lane catches the breaking signal and the FILLED lane catches the
signal worth reading. Never merge them, never valve the RAW lane.

---

### 1. Leigons — swarm-at-scale
- **RAW:** `(agent swarm OR multi-agent) -filter:replies`
- **FILLED:** `(agent swarm OR multi-agent) -filter:replies min_faves:30`
- Guard: RAW stays unvalved; valve lives in FILLED only.

### 2. Rocinante — local inference / MLX / spec-dec
- **RAW:** `MLX OR speculative decoding`
- **FILLED:** `MLX OR speculative decoding min_faves:20`
- Guard: same pair rule. If MLX noise floods RAW, mute spam accounts inside the column, not globally.

### 3. Mesh 3d — image-to-3D / WebGPU / point clouds
- **RAW:** `TRELLIS OR image-to-3D WebGPU`
- **FILLED:** `TRELLIS OR image-to-3D WebGPU min_faves:20`
- Guard: same pair rule.

### 4. GLM Watch — GLM / z.ai news + benchmarks
- **RAW:** `GLM-5.3 OR z.ai`
- **FILLED:** `GLM-5.3 OR z.ai since:2026-08-28 min_faves:15`
- Guard: same pair rule. `since:` is the rolling 7-day window — bump it +7d at each weekly refresh.

### 5. Cache Econ — KV cache / prompt economics
- **RAW:** `KV cache OR prompt caching`
- **FILLED:** `KV cache OR prompt caching min_faves:25`
- Guard: same pair rule.

### 6. Game Build — game-building agents
- **RAW:** `AI game builder OR city builder agent`
- **FILLED:** `AI game builder OR city builder agent min_faves:30`
- Guard: same pair rule.

### 7. Grok — grok/xAI ecosystem (queries DERIVED — first rotation may prove them wrong; adjust freely)
- **RAW:** `(grok OR xAI) -filter:replies`
- **FILLED:** `(grok OR xAI) -filter:replies min_faves:30`
- Guard: same pair rule. "grok" catches verb-usage noise; that is what the FILLED valve is for.

### 8. MAG — legacy/general (queries DERIVED — stands in for the general agent-protocol lane)
- **RAW:** `("agent protocol" OR MCP OR A2A) -filter:replies`
- **FILLED:** `("agent protocol" OR MCP OR A2A) -filter:replies min_faves:40`
- Guard: same pair rule. MCP is high-volume — expect the RAW lane hot; the monitor triages it.

---

**UNIVERSAL BAN GUARDS (every column, every deck):**
1. The deck is a NET, not a STORE — bookmark + archive (Wayback/archive.today) anything worth keeping, on discovery.
2. No geo filters, no engagement valve on RAW, no list columns unless PRIVATE (public lists notify targets).
3. No automation on this account — no daemons, no auto-posting; human-paced reads only. Column dead? Delete it.

Optional 17th: homepage follows column + the mute-words algorithm purge (steal §1) if the For You lane injects junk.
