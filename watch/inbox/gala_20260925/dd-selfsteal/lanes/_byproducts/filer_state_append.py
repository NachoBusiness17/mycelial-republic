# filer: append ONE STATE entry (GALA DD-SELFSTEAL CLOSE) to memories/session/next-window-handoff.md
# single-writer append, em/en-dash scan, tail verify
import sys
from datetime import datetime, timezone

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
HANDOFF = ROOT + "/memories/session/next-window-handoff.md"
TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ENTRY = (
    "- GALA DD-SELFSTEAL CLOSE " + TS + " - GALA dd-selfsteal banked: danced count 10 "
    "(dd-mountain-bridge, dd-actualplay-intel, dd-games-audit, selfsteal-24h-builds, "
    "hermes-burn-patterns, dd-corpus-holdings, hermes-burn-economics, hermes-intelligent-burn, "
    "selfsteal-24h-laws all division B + synthesis division A; no fold_gate output exists in "
    "watch/inbox/gala_20260925/dd-selfsteal/ (dir holds only lanes/), so the count basis is the "
    "lane JSON finish flags, same rule as the hitler-dig close). Mined rows: 52 law rows "
    "(selfsteal-24h-laws 10, selfsteal-24h-builds 9, dd-actualplay-intel 8, hermes-burn-patterns 7, "
    "hermes-intelligent-burn 6, synthesis 5, dd-games-audit 4, dd-mountain-bridge 3; "
    "dd-corpus-holdings and hermes-burn-economics rows [] file decision changes only). "
    "Decisions changed: 10 by lane content (every lane JSON carries a decision_changed key): "
    "(1) dd-mountain-bridge changes the Mountain post-slice roadmap to a DD-shaped next content layer "
    "(not_clear encounter gates, tick-keyed loot/riddle tables, GWAP-boss Drought) naming the dormant "
    "Z1 verdict feed as the activation target instead of new netcode; "
    "(2) dd-actualplay-intel confirms the 2026-10-03 intel as the SECOND WBN pass whose new bankable "
    "content is PvP-as-engine + cadence-as-carrier-law landing via the already-in-flight "
    "PODCAST_STRUCTURE_spec, keeps the WBN transcript hunt OWED as a librarian-expedition pickup, and "
    "records that the named dd_dogfood receipt does not exist; "
    "(3) dd-games-audit moves the DD encounter acceptance bar from solvability-only to "
    "mechanic-load-bearing plus trait wiring (design gate on the pack, st.sb binding + def scoping fix, "
    "fold-or-delete the 2 orphaned DD files and fix the dd_riddle-door filename, re-run the worldline "
    "teller, wire-or-shelve oracle_dice.js); "
    "(4) selfsteal-24h-builds starts the next build cycle from the rails table (queue/STANDING_RAILS.md) "
    "and mag.route_chat, not bespoke carriers, routes byte-check audits fifty-wide, and names tavern's "
    "0.0-report channel as the first arena adapter fix; "
    "(5) synthesis orders next-cycle burn: repair the measuring instrument (opening-tag grammar A/B + "
    "void accounting) and fold the arena-day laws into corpus/steal BEFORE any new module content, new "
    "model-calling code starts at mag.route_chat per STANDING_RAILS default-to-rails; "
    "(6) dd-corpus-holdings closes the DD corpus-holdings inventory question and sets the module-builder "
    "gap order (SRD lookup cache first, then encounter-budget math, then a progression schema); "
    "(7) hermes-burn-economics closes the descent-driver-twins double-spend question (twins billed "
    "$2.2521 for $1.1229 of real work, total ledger waste $25.9998 of $63.5824 = 40.9 percent, next "
    "money-adjacent fix the tavern/dungeon run-id tag collision, not another driver guard); "
    "(8) hermes-intelligent-burn downgrades the raw 62 percent waste reading to ROUTING CHANGE and sets "
    "the next-24h card (tavern GWAP report-channel fix first, structured tavern turn contract, one PvP "
    "dungeon session, tavern route_chat migration + id stamp, mechanic-load-bearing level gate; single "
    "flip named: the transcript-vs-ledger join on tavern rows); "
    "(9) selfsteal-24h-laws closes the 24h law inventory and hands the next sitting four named gaps "
    "(land the three blind-audit engine laws or give them owner+clock, fold the Task-50 width amendment "
    "into AGENTS.md line 33, file the ouroboros hermes-judgment queue rows recorded as owed 2026-10-02, "
    "mint a falsifier for the lyric law); "
    "(10) hermes-burn-patterns declines a decision change and arms two operator calls (sonnet-first "
    "routing for paid design asks, the one-line tavern id-stamp owned by tools/tavern.py). "
    "B-division finish: 9/9 finished per lane JSON finish flags (8 ok:true - dd-mountain-bridge ok "
    "status done, dd-games-audit, selfsteal-24h-builds, hermes-burn-patterns, dd-corpus-holdings, "
    "hermes-burn-economics, hermes-intelligent-burn ok status landed, selfsteal-24h-laws - plus "
    "dd-actualplay-intel which carries no ok key and closes on its exit-0 two-block check battery with "
    "source_read_in_full true); division A 1/1 (synthesis: no ok key, finish line the exit-0 check set, "
    "dungeon dry session exit 0 with golden vectors byte-identical to committed pins and 3/3 "
    "REAL_SCROLLS pass; its head chapter watch/inbox/dd_dogfood/SYNTHESIS.md was not landed at lane "
    "close and is still absent at filing). Graves filed: 0 (grep -ril GALA_GRAVE over "
    "watch/inbox/gala_20260925/dd-selfsteal/ and watch/inbox/dd_dogfood/ returned no matches at filing "
    + TS + "). 10 LINKS rows (GALA-dd-selfsteal-*) appended to memory/corpus/LINKS.jsonl after src "
    "dedupe (pre-append grep for dd-selfsteal under any field: 0 rows; ledger 274 -> 284, whole-ledger "
    "re-parse 284/284 OK, 10 appended ids unique, 10 appended srcs each exactly once, em/en-dash scan "
    "on the appended block 0; titles = lane top laws except dd-corpus-holdings and hermes-burn-economics "
    "whose top law is null (rows []) so their titles are their changed decisions verbatim). Receipts at "
    "filing: watch/inbox/dd_dogfood/ (mountain-bridge.md 14,772 B, games-audit.md 12,756 B, "
    "selfsteal-builds.md 16,078 B, hermes-patterns.md 9,858 B, hermes-economics.md 8,052 B, "
    "corpus-holdings.md 18,100 B, selfsteal-laws.md 20,229 B, hermes-verdict.md 21,425 B + "
    "hermes-verdict.reasoning-dump.md 65,294 B; actualplay-intel.md does not exist per the "
    "dd-actualplay-intel lane's own negative finding and is still absent at filing). Lane JSONs + check "
    "evidence: watch/inbox/gala_20260925/dd-selfsteal/lanes/. Owed entering the next window: the "
    "hermes-intelligent-burn next-24h card above plus the dd-games-audit named one-sittings and the "
    "dd-actualplay-intel WBN transcript hunt."
)

# guards
assert "\u2014" not in ENTRY and "\u2013" not in ENTRY, "em/en-dash in STATE entry"
with open(HANDOFF, "r", encoding="utf-8") as f:
    body = f.read()
assert body.endswith("\n"), "handoff file does not end with newline"
assert "GALA DD-SELFSTEAL CLOSE" not in body, "STATE entry already present, refusing duplicate"

with open(HANDOFF, "a", encoding="utf-8", newline="\n") as f:
    f.write(ENTRY + "\n")

with open(HANDOFF, "r", encoding="utf-8") as f:
    post = f.read()
lines = post.splitlines()
print("handoff lines: pre 495 -> post", len(lines))
print("entry appended once:", post.count("GALA DD-SELFSTEAL CLOSE") == 1)
print("em/en-dash in appended entry: 0")
print("ts:", TS)
