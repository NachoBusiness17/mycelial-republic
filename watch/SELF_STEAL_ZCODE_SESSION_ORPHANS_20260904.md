# SELF-STEAL — ZCode session-transcript orphan mining (2026-09-04)

**ITEM:** Mine the operator's archived ZCode sessions for ORPHANS — signals that appeared in
past sessions but never folded into the repo's record surfaces (watch/ cards,
memory/percolator/invariants.json, memory/law/registry.json, docs/). Pattern precedent: the
percolator-novel orphan shading in memory/improve/.

## METHOD

**The transcript door is OPEN and it is `db.sqlite`, not just usage metadata.**
`C:\Users\foste\.zcode\cli\db\db.sqlite` (220MB, WAL) holds full conversation text:
tables `session` (184 rows) / `message` (15,591) / `part` (text content per message).
`model_usage` is metadata-only as suspected, but `message`+`part` carry everything.
Other tree facts: `rollout/` = recent subagent model-io jsonl only; `agents/sess_*` =
per-session working dirs; `memories/projects/` = ZCode-native memory (2 project dirs);
`claude-import-*` sessions = 1-exchange stubs (import tests, no pre-ZCode history inside).

- **Population:** 184 sessions, 2026-08-25 11:01 → 2026-09-04 14:38 (43 interactive,
  144 subagent children, 2 forks). Entire ZCode era.
- **Sampled:** 29 sessions dumped to full text (~5.8MB): all 27 non-trivial interactive
  sessions (every one from Aug 25–Sep 4, oldest-first + the 15 largest by bytes), plus
  2 claude-import stubs. Subagent children were title-scanned only (their finals fold into
  parents/cards by design). The 2 "Fork of System Fresh Boot" sessions skipped as duplicates.
- **Extraction:** python over `message`⨯`part` (type="text"), roles preserved; operator
  turns isolated for the big sessions; ALL_CAPS concept sweep, law-name sweep
  ("the X law"), naming-phrase sweep, then per-candidate grep against repo record
  surfaces (watch/ incl. room.jsonl, docs/, memory/ incl. law/registry.json +
  percolator/invariants.json + runs/, handoff/, queue/, mag/; mine/raw excluded).
- **Record-surface baseline:** memory/law/registry.json = 8 laws (LAW-1..10, ids like
  rails_over_direction); percolator/invariants.json = 47 behavioral n-grams (sha-keyed,
  not named laws); watch/ = 603 files. AGENTS.md (workspace root) treated as a surface too.

## ORPHANS FOUND

### O1 — the `mcp-manifest` build spec: GO'd, pinned, never drafted — **Supported → FOLD**
- **Source:** sess_f7209b4a ("Fresh Boot Test on 5.3 Flash", Aug 26) + the recorded GO at
  `queue/handoff/zcode/CONVO.md` line 218 (2026-08-26T22:5x).
- **Signal:** Operator GO on wiring Z.AI's four official MCP servers (Vision/WebSearch/
  WebReader/Zread) as the capability layer. Spec requirements pinned in the GO: epoch-pinned
  byte-stable manifest; read-only perception packs for quantized tiers, write-capable tools
  only for the primary planner; per-call QUOTA GATE (cited example: web search 1.2 credits/call
  — "or their eyes eat the judgment lanes' 5h pool"); fail-close carryover (never cache
  privileged results by argument equality); SURFACES.md registration for the local Vision
  stdio server; distributed cache-tier machinery OUT (Rocinante blueprint only).
- **Absence evidence:** grep `mcp-manifest`/`mcp_manifest` across record surfaces → only hit
  is the CONVO GO entry itself. No spec file, no card, no law row.
- **Partial supersession (why this is still an orphan):** Sep 3–4 work covered the territory —
  `watch/INTAKE_ZAI_DEVPACK_MEMORY_20260903.md` and `watch/STEAL_ZAI_SYSTEMS_AUTOMATE_20260904.md`
  enumerate the MCP suite (search/reader/zread remote + local Vision server, 8 tools) — but
  NEITHER carries the pinned manifest/quota-gate/tiering requirements. The spec-pinned build
  decision is unexecuted and its pins exist only in a channel file.
- **Disposition: FOLD** — draft the spec (or fold its pins into STEAL_ZAI_SYSTEMS_AUTOMATE as
  the build item). Tri-state: **Supported** (GO + pins recorded verbatim in CONVO; absence grep-verified).

### O2 — the buddy letter: a complete external deliverable living only in a transcript — **Supported → FOLD**
- **Source:** sess_60d3e6c1 ("Troubleshooting Internet Connection Issues", Sep 3), operator:
  "my buddy's agent is fucking up and sending money to shit addresses... write it in my voice."
- **Signal:** A finished money-safety playbook for agent owners, human-voiced, links included:
  (1) put a cap between the agent and the money (Safe wallet allowance + address allowlist;
  provider spend limits, never the main key); (2) every transaction logs before it fires —
  "no log line, no transaction"; (3) anything above a few bucks waits for a human tap, raise
  the limit after a week of clean receipts; (4) big model decides, cheap/free model executes
  ("most people's agent bills are 90% work a free model could've done"). Links: safe.global,
  LangGraph human-in-the-loop pattern, provider spend-limit dashboards.
- **Absence evidence:** `safe.global` / `Safe wallet` / "no log line, no transaction" → 0 hits
  on all record surfaces.
- **Why it matters beyond the favor:** it is the fleet's own doctrine (operator-gates,
  receipts-before-spend, right-sizing) translated into plain-english recruit-speak — exactly
  the artifact the public-turn/recruitment arc needs. Losing it means re-deriving it.
- **Disposition: FOLD** — bank the letter text as a watch/ card (reusable template + the
  external-deliverable precedent). Tri-state: **Supported** (full text in session; absence verified).

### O3 — the capability-endowment doctrine: named in-session, unindexed in the repo — **Supported → FOLD**
- **Source:** sess_f7209b4a (Aug 26), assistant framing the operator's endowment sketch:
  "**senses for the blind, GPS for the stateless, hands for the tool-less**" + gateway shape:
  stable namespaced tool packs; only the primary planner gets write-capable tools; edge/
  quantized models get read-only perception tools.
- **Absence evidence:** `capability-endowment` / `senses for the blind` / `GPS for the stateless`
  → 0 hits on record surfaces. The GPS half is folded as DUMB_AGENT_GPS_{A,B,MAP}_20260901.md;
  the tiered endowment doctrine as a NAMED concept is not filed anywhere. docs/DOCTRINE_MAP.md
  predates it (2026-08-24).
- **Disposition: FOLD** — one doctrine row (DOCTRINE_MAP or LEXICON entry) naming the tiers;
  it is the design law the Sep 3–4 MCP/steal work keeps re-deriving without citing.
  Tri-state: **Supported**.

### O4 — "10 lite accounts vs one max": the account-count scaling question never answered — **Unproven → FOLD to economist**
- **Source:** sess_cac6dbfa ("Research", Sep 4), operator: after reading the 5.3-flash campaign
  doc — "well that makes the difference between 10 lite accounts running from 11-9 or one max."
- **Signal:** A lane-scaling hypothesis: N cheap accounts may multiply the free campaign window
  versus one Max seat. The question was asked and dropped in-session; the campaign itself got
  audited (ECONOMIST_AUDIT_20260904.md settled Sep 20 vs Sep 23) but the account-count
  arithmetic never appears.
- **Absence evidence:** `10 lite` / `ten lite` → 0 hits.
- **Disposition: FOLD** to the economist's queue (note: multi-account farms brush provider
  ToS — flag honestly if worked). Tri-state: **Unproven** (the question is on record; the
  answer was never measured).

### O5 — "there is no baking anymore — we do it live": operator cadence ruling, folded nowhere — **Supported → FOLD**
- **Source:** sess_95e7f98a ("Teasing Out Salon Systems", Sep 3), operator, twice in a row:
  "there is no baking anymore" / "we do it live" (context: salon/campaign operation — no
  offline pre-compiled passes; the system runs and is corrected live).
- **Absence evidence:** `no baking` / `do it live` / `live cadence` → 0 hits on record surfaces.
- **Disposition: FOLD** — one line in the corrections/preference record. It is the operator's
  own statement of the dogfood-live pattern the fleet already practices; cheap to bank, easy
  to lose. Tri-state: **Supported** (verbatim in session; absence verified).

### O6 — "the k-space law": content folded, NAME unindexed — **Supported → RESOLVE**
- **Source:** sess_ae2253c3 ("24h vast feed verdict", Aug 27–28): "Rows 27 and 28, banked in
  the palace: **the k-space law** (we re-instantiate the same invariant on new hardware — and
  the mapping to our machines is our only originality, which is enough)..."
- **Absence evidence:** `k-space law` → 0 hits. BUT the law itself IS folded:
  `memory/runs/lineage_audit/lessons.jsonl` row 27 ("origin law" era) carries the same content
  verbatim-adjacent ("the MRI k-space mapping; the KV-cache; the chain; the palace — one
  invariant, four substrates"), and LINEAGE_WALL_20260902.md row 0 carries the theorem.
- **Disposition: RESOLVE** (not a content orphan — a name-index gap). Optional: add "k-space
  law" as an alias so future greps find the palace row. Tri-state: **Supported**.

## DUPLICATES (checked and folded — listed so the next pass doesn't re-dig)

OX_MEGA hologram-lab lineage (folded: handoff/OX_*, LINEAGE_WALL); MORNING_SURPRISE.md +
villains_guild + GAME_VILLAIN_GUILD_DESIGN (exist); CUSTODY_AND_DISCLOSURE.md + LEXICON.md
(exist); the patience law, Mickey law, RenderMan law, prune law, conservation law, envelope
law (all ≥2 hits on surfaces); memweave (2,100 hits); "the map precedes the territory"
(1,656 — CONVO operator-doctrine landmark + ribs); tripartite; Diamond-Age/Primer framing;
mycelial republic / water computer / water familiar; ractors (2,068); Elder charter
(Steiner/Manly P Hall — 24/20 hits); OpenAI researcher-credits application (folded in
INTAKE_LEGIONS_SWEEP_20260904 + CONVO); Sep 20 vs Sep 23 campaign-date dispute (settled in
ECONOMIST_AUDIT_20260904); android-emulator free-lane scheme (ANDROID_EMULATOR_SELF_STEAL_
20260904); HERMES_DOSSIER_V1 + churn organ + BOX_READY buyer arc (watch/ files + E7 receipt);
FSYNC_STAGE (economist desk amendment); all SALON_ARTIFACT folds; the night-wheel intake-card
family (INTAKE_*_20260904, room.jsonl).

## WHAT THIS PASS DID NOT SEE (coverage gaps)

1. **Subagent depth:** 144 subagent_child sessions were title-scanned only. Their final
   reports normally fold into parents/cards, but a discovery made and never reported by a
   subagent would be invisible here.
2. **Non-text parts:** only `part.type="text"` was extracted. Tool outputs, code blocks, and
   file contents (other part types) were skipped — a signal stated only inside a tool result
   is missed.
3. **Other db tables unmined:** input_history, session_entry, todo, workflow_* — likely
   low-signal but unverified.
4. **Unexplored adjacent stores:** `.zcode/cli/agents/sess_*/agent_*` dirs (per-session
   subagent state), `rollout/` model-io jsonl (Sep 4 subagent IO only), `.zcode/v2/`
   (native state), `.zcode/workspace`. The VS Code seat's own history was declared thrashed
   in-session (Aug 26) — if any survives on disk, it is outside this pass.
5. **Truncation:** operator turns clipped at 600 chars during the big-session sweep; long
   pastes (campaign docs, X threads) were skimmed via their sessions' assistant replies, not
   fully read.
6. **The 2 fork sessions** (920 msgs each, forks of System Fresh Boot) skipped as duplicates —
   if a fork diverged with unique work, it is unmined.

**Verdict:** the fleet's folding discipline is strong — of ~60 candidates swept, 6 true
orphans survived verification, and only one (O1, the mcp-manifest spec) is a GO'd-but-unbuilt
decision. The transcript door (`db.sqlite` message/part) is now named and scriptable; a
standing re-mine after each big arc is cheap (~1h gopher pass).

*— background research gopher, 2026-09-04. Dumps + extraction script kept at
`C:\Users\foste\.zcode\cli\tmp_orphan_mine\` (scratch, safe to delete).*

---

## FOLD RECORD (zcode seat, 2026-09-04)

| Orphan | Disposition | Fold path | Tri-state |
|---|---|---|---|
| **O1** mcp-manifest spec | **FOLDED — drafted** | `docs/ref/MCP_MANIFEST_SPEC.md` — enforceable pack-manifest format (schema `mcp.pack.manifest.v1`, epoch-pinning via canonical sha256_16, `tier: perception\|hands` field, per-call quota gate with the GO's 1.2-credit example, fail-close cache rule, spawn/runtime/epoch check steps, SURFACES registration, distributed cache-tiers OUT); Aug-26 GO quoted verbatim in the provenance section; bound to `queue/lanes/*/manifest.md` as first consumers (section 9) | **Supported** (GO + pins); lane wiring itself **Supported as design / Unproven as wiring** (no lane spawned under a pinned whitelist yet) |
| **O2** buddy letter | **FOLDED — verbatim** | `docs/ref/BUDDY_LETTER.md` — 3-line source header + the letter unedited (cap/ledger/approval/cheap-lanes + safe.global, LangGraph HITL, spend-limit links) | **Supported** |
| **O3** endowment doctrine | **FOLDED** | `memory/improve/orphan-o3-endowment-doctrine-2026-09-04.md` — "senses for the blind, GPS for the stateless, hands for the tool-less" named as doctrine; maps onto lane charter clause 5 and O1 spec section 4 (perception tiering IS the doctrine) | **Supported** |
| **O4** 10 lite vs 1 max | **ROUTED — verified, no new fold** | `queue/lanes/economist/inbox.jsonl` row confirmed present (ts 2026-09-04T14:46:54Z, from zcode-manager, pointer to this card #O4, ttl 2026-09-06) — the economist lane's first task | **Unproven** (question on record; answer unmeasured — economist's to price) |
| **O5** live-cadence ruling | **FOLDED — one law row** | `docs/ref/MCP_MANIFEST_SPEC.md` section 11 (related doctrine): quotes + date; rules OUT offline/batch pre-compiled passes and baked stale history, rules IN live cadence (wire to real events NOW, verify against the live tip) | **Supported** |
| **O6** k-space name index | **RESOLVED — name index appended** | `memory/runs/lineage_audit/lessons.jsonl` (append-only new row, no row edited): "the k-space law" → row 27 of that ledger (era "origin law", 2026-08-28T13:22:34Z); LINEAGE_WALL row-0 already cites row 27 as the theorem. **Evidence correction:** the card named sess_ae2253c3 as source; the naming line ("Rows 27 and 28, banked in the palace...") is found in the **sess_10fe54a8** dump — kept as-is in the index row | **Supported** |

**Gopher pass closed: 6/6 orphans disposed** (4 folded, 1 routed-verified, 1 name-index
resolved). tmp_orphan_mine untouched.
