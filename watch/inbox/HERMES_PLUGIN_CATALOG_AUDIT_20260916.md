# HERMES PLUGIN CATALOG AUDIT — 2026-09-16

**Class:** RECEIPT (read-only audit; nothing installed, enabled, disabled or removed)
**Seat:** Hermes seat (Sancho) · **Host:** Windows box · **Profile:** `default`
**Source:** https://hermes-agent.nousresearch.com/docs/plugins (cached: `%LOCALAPPDATA%\hermes\cache\web\hermes-agent.nousresearch.com-513deead87.md`, 890 lines / 42,677 bytes)
**Corrects:** the earlier same-day claim "0 third-party plugins installed" — that read `desktop-plugins\` (empty) and missed `plugins\`.

---

## 1. LOCAL STATE — live, verified by `hermes plugins list --plain --no-bundled`

Installed **and enabled** (6). Root: `C:\Users\foste\AppData\Local\hermes\plugins\`

| plugin | origin | version | in catalogue? |
|---|---|---|---|
| `hermes-resetwatch` | user | 0.2.17.post2 | yes — Desktop20 ★69 |
| `hermes-tailscale` | user | 0.0.5.post2 | yes — Desktop20 ★40 |
| `memory-wiki` | git | 1.0.0 | yes — `hermes-memory-wiki`, ✓ Official ★4 |
| `tool-slimmer` | git | 0.6.5 | yes — Tools25 ★35 |
| `hermes-ledgerline` | user | 0.1.7.post2 | no — local/personal |
| `chrome-profiles` | git | 1.1.0 | no — not in this catalogue page |

- **Bundled plugins:** 57, **0 enabled** (all opt-in; `--no-bundled` therefore returns exactly the 6 above).
- **Third-party plugins not enabled / installed-but-idle:** 0.
- So: 4 of the 6 catalogue entries already live here are installed; the other 2 are this seat's own.

## 2. CATALOGUE — measured from the cached page

- **97 install deep links, 97 unique `catalog_name`s.**
- **9 sections** (numbers are the page's own headers): `Desktop20`, `Memory9`, `Platforms15`, `Web & Browser10`, `Tools25`, `Voice5`, `Automation5`, `Models1`, `General10` → 100 header slots vs 97 links (3 entries carry no install link; not reconciled).
- Trust markers per entry: `✓ Official` vs `❖ Community`; star counts run ★0 → ★214 (`mnemosyne-dashboard`, highest).
- Deep-link form (what the "Install in Hermes" buttons fire):
  `hermes://plugin/install?repo=<urlencoded git url>&catalog_name=<name>&sha=<40-hex>&enable=1`
- Variant seen on 4 Adolanium entries: `repo=...%23catalog` (url-encoded `#catalog` subdir), e.g. hermes-resetwatch / hermes-rss / hermes-tailscale / hermes-office.
- Portable Agent Plugins v1 entries ship as `mcp.json + skills/` (e.g. snyk, touchdesigner).

## 3. CLI WORKFLOW — verbatim, all executed this session (exit 0)

```
hermes plugins                       # interactive toggle UI
hermes plugins list                  # table; --plain for scriptable, --no-bundled to hide the 57 bundled
hermes plugins search <term>         # curated catalog search
hermes plugins browse                # every curated catalog entry
hermes plugins show <name>           # detail incl. emits/listens  (alias: info)
hermes plugins install <cat_name|git-url|owner/repo> [--ref <40-hex SHA>] [--enable|--no-enable] [--force]
hermes plugins enable|disable <name>
hermes plugins update <name>         # pull latest
hermes plugins remove|rm|uninstall <name>
hermes plugins capabilities          # declared vs GRANTED capabilities per plugin
hermes plugins doctor <name>         # validate against real runtime contracts
hermes plugins compat                # installed plugins importing paths removed by the Sep 2026 decomposition
hermes plugins pack                  # hermes-pack.yaml shareable sets
hermes plugins validate <dir>        # catalog-admission CI gate
```

Deep link → CLI, 1:1: `repo` → the identifier (or `--ref` on a clone), `sha` → `--ref <40-hex>`, `enable=1` → `--enable`. `hermes plugin` (singular) is **not** a command.
Portable packages install **disabled** by default; `--no-enable` skips the confirmation prompt.

## 4. FIT SHORTLIST — not installed here, in the order I'd take them

1. `hermes-plugin-guard` (Tools25 ★8, 1 tool) — static review of a candidate plugin; target code is never executed. Gate for any community install. `hermes plugins install hermes-plugin-guard --ref 857d881be77249c192c5fefa8254db186a7abbca --enable`
2. `hermes-telemetry` (Packaged ★0, hooks only, 0 tools) — tokens/cost/latency/tool-calls per session + cron, local SQLite, `/stats` `/budget`. Fits the credits lane (spend surfaced, not discovered later). `hermes plugins install hermes-telemetry --ref 146f6744fc4117ade784eefd7aa231c9b3f36281 --enable`
3. `hermes-memory-ui` (Desktop20 ★55, read-only) — inspects built-in / holographic / Mem0 / Honcho / Mnemosyne / Hindsight / ByteRover memory. Read-only ⇒ compatible with the read-only-memory ruling. `hermes plugins install hermes-memory-ui --ref 9472bed7e20a51ac4f6c48f882bd9f80ea54d4ee --enable`
4. `hermes-nous-prices` (Desktop20 ★3) — Nous Portal model prices + account balances. We run two Nous keys. `hermes plugins install hermes-nous-prices --ref 94f99436786e6fbbfcce161635d11c67bf094c8e --enable`
5. `hermes-newswire` (Desktop20 ★31) — news ticker; explicitly **zero API keys, zero model tokens**. `hermes plugins install hermes-newswire --ref deccdc4575ff45461fbf3f3c61e0945f188ef620 --enable`
6. `recency-anchor` (Packaged ★1) — restates the instruction you care about at the end of every user turn; relevant on a 65,536-token context model. Append-only, no API calls. `hermes plugins install recency-anchor --ref 24d1906a285fdfe37ecaf6253da8712db28f5a7b --enable`

**Caution, not recommended as-is:** `tokenwatch` — *"freeze tool/gateway activity at configured limits"*; it can stop work mid-flight and collides with the fleet's existing spend discipline. `mnemosyne` / `yantrikdb` / `lancedb` / `cashew` — these are memory *providers* (replacement models) and would touch the memory layer we're keeping read-only.

## 5. NOTES

- Nothing was installed, enabled, disabled or removed in producing this audit. The only write is this card + its register/amend events in `watch/inbox/index_events.jsonl`.
- `desktop-plugins\` is empty; Desktop20-type plugins still install into `plugins\` (all 6 live there). Not a second plugin root for this profile.
- Capability surface of the 6 installed plugins, `hermes plugins compat` result, and `hermes plugins doctor` status are NOT yet measured — next read if wanted.

## 6. PROVENANCE

`hermes plugins list --plain --no-bundled` (6 rows) · `hermes plugins list --plain` (57 bundled rows) · `hermes plugins --help` / `install --help` · cached catalogue page (97 install links, regex-counted) · `ls -1 plugins` (6 dirs).
