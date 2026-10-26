# INTAKE CARD — awesome-mcp-servers (2026-09-04)

**Paste**: github.com/punkpeye/awesome-mcp-servers
**Score**: 16/25 — **BUILD WINDOWED** (the senses aisle; first Gitingest dogfood logged)
**Receipts**: README pulled via raw door (1.4MB — gitingest bounced off it, two-strike,
raw door precedent applied): **3,482 MCP servers across 59 categories** — the
agent-senses supply side, counted.

## What it is for us: the SENSES AISLE
The operator's doctrine: agents are bodies, MCP servers are senses. This list
is the catalog of purchasable senses. Map against the fleet's organs:

| Sense category | Fleet organ | State |
|---|---|---|
| Browser automation | mag-browser + computer-use | HAVE (strong) |
| Knowledge & Memory | verkle chain + percolator | HAVE (own organ) |
| Version control / Code execution / Command line | git, run_python, shell | HAVE |
| Search & Data Extraction | grok decks, websearch; Search-Prime unprobed | PARTIAL |
| Databases / Data platforms | usage sqlite, event_stream | HAVE |
| Monitoring | flight recorder v0 | PARTIAL |
| OS automation | computer-use seat | HAVE |
| **Agreements & Coordination** | claim organ / spawn gate / contracts | **OUR WEAK SPOT — a whole category of prior art exists** |
| Cryptography / Security | loopback law only | THIN |
| Research | salon_runner, research_worker | OWN ORGAN, stronger than most entries |
| Communication (Slack/email/etc) | room.jsonl only, no external | MISSING (deliberate? loopback law) |
| Finance/fintech | economist + spend ledger | PARTIAL |

## The three steals
1. **Aisle-before-build law**: when an organ needs a new sense, check the
   59 categories BEFORE building a homegrown organ (right-size law applied
   to senses). Adoption filter: loopback-only, local-first, MIT/Apache.
2. **Agreements & Coordination category** = direct prior art for the
   spawn-gate/claim-semantics work the salon just ordered — mine it before
   building the lock.
3. **Public-turn stat**: 3,482 servers across 59 categories = the agent
   economy's scale, counted today (cite as "counted at the bytes, 2026-09-04").

## Axes
FIT 5 (pure composition onto MCP-senses doctrine) · PULL 3 (frontier-map arc,
public turn) · COST 4 (per-server adoption varies; loopback constrains) ·
WINDOW 3 (senses shopping rides the salon's agent-build wave) ·
NOVELTY 1 (known repo; today's artifact = the count + category map).

## Routing
1. **REMEMBER**: the aisle map (this card) = the lookup table for
   sense-shopping; consult before any new organ build.
2. **BUILD WINDOWED**: mine the Agreements & Coordination + Monitoring
   categories for the spawn-gate build (rides the claim-organ fix session).
3. **REMEMBER**: gitingest failed on awesome-list-scale READMEs (content
   extraction empty) — raw-door remains the reliable repo door for lists;
   gitingest keeps code-repo duty. Honest tool-boundary filed.

Tri-state: counts Supported (bytes counted); "prior art for spawn gate"
Unproven until the category is actually mined; adoption value of any single
server Unproven until one is wired.

## ADDENDUM — duplicate paste = free verify pass (wong2/awesome-mcp-servers)
Second canonical catalog pulled via raw door (99KB): **535 entries** (530 unique).
Cross-checked at URL level against punkpeye's 3,475: **only 39% overlap** —
wong2 adds ~324 servers punkpeye doesn't list. **Union: 3,799 unique servers.**
The aisle is bigger than the first count; two catalogs are complementary, not
duplicative (different curators, different bars for inclusion).
Security note: Mimosa (the fleet scanner) blocked the naive fetch script for
SSRF/path-traversal — rewritten with https-only + host allowlist + resolved-IP
private-range check before it ran. The scanner is watching, and the constraint
is right: senses shopping touches the network.

## ADDENDUM 2 — third catalog (appcypher) + final count
Three-catalog census, URL-normalized (tree/blob stripped, http→https):
- punkpeye 3,475 · wong2 531 · appcypher 184 (oldest format, table-based)
- appcypher overlaps: 119 with punkpeye, 105 with wong2 — still adds ~65 unique
- **THREE-WAY UNION: 3,838 unique MCP servers.**
Count methodology: raw-door pulls, dual bullet/table parsers, normalized URLs.
Mimosa SSRF guards held (fetches via curl with literal allowlisted URLs; python
counts local files only — two-strike on parameterized scripts, approach switched).
