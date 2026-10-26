# B2-104: INDEX.json receipt registration (tail-anchored insert, json-valid gate).
import hashlib
import io
import json
import sys

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
RECV_REL = "watch/inbox/burn_wave_20260926/B2_104_freshness_policy_20260926.md"
IDX = ROOT + "/watch/inbox/INDEX.json"

sha = hashlib.sha256(io.open(ROOT + "/" + RECV_REL, "rb").read()).hexdigest().upper()

with io.open(IDX, "r", encoding="utf-8") as f:
    idx = f.read()

marker = "burn_wave_20260926/B2_104_freshness_policy_20260926.md"
if marker in idx:
    sys.exit("INDEX already registers receipt")

# Tail anchor: the document ends with the last item, then "  ]\n}" (2-space
# indent, matching the B2-97 anchored-insert convention).
ANCHOR = '}\n  ]\n}'
if idx.count(ANCHOR) < 1:
    sys.exit("INDEX tail anchor fail: %d" % idx.count(ANCHOR))
cut = idx.rfind(ANCHOR)
purpose = (
    "B2-104 corpus map freshness policy LANDED: three arms one module each "
    "(mag/catalog_rescan.py incremental append-upsert rescan + dated atomic-replace "
    "rebuild + manifest, mag/catalog_tags.py salon Appendix B tag pass verbatim + "
    "dated TAG_REPORT, mag/catalog_freshness.py disclosure arm map_asof/map_stale on "
    "corpus_search both engines and corpus_stats, missing manifest never reads fresh, "
    "48h budget), who fires it: MagCorpusRescanDaily Task Scheduler 03:30 local "
    "registered State Ready (scripts/register_corpus_rescan_task.ps1), live run 2m01s "
    "over the 19:01:27Z base map 489,455 rows (added 17 refreshed 76 unchanged 489,194 "
    "vanished 27 base_dups 158, tags re-run 489,548 rows, manifest sha12 1371A1DB3005), "
    "C6 falsifier both directions (qdrop 0 hits 757,667 rows at 18:44Z on the Sep-18 "
    "map, hits on the fresh map both engines post), mid-lane estate mutation named "
    "(19:01:27Z atomic replace by unnamed flow, B2-332 still Open, kind-count parity "
    "Unproven, rules pinned fixture-first, 26 tests), tools/corpus.py rebased on B2-102 "
    "landed bytes per the claim law, ratchet NEW=0, em-dash 0, self-fed B2-510 to B2-512 "
    "unchecked"
)
entry = (
    '    {\n'
    '      "path": "burn_wave_20260926/B2_104_freshness_policy_20260926.md",\n'
    '      "class": "receipt",\n'
    '      "purpose": "' + purpose.replace('"', "'") + '",\n'
    '      "sha256": "' + sha + '"\n'
    '    }\n  ]\n}'
)
out = idx[:cut] + ',\n' + entry + idx[cut + len(ANCHOR) + 1:]
# The original ANCHOR started with '}' at an item's close; we consumed its
# trailing '}\n  ]\n}', so rebuild: previous item close + comma + our item.
json.loads(out)  # validity gate before write
with io.open(IDX, "w", encoding="utf-8", newline="") as f:
    f.write(out)
print("INDEX item inserted, json valid, sha", sha[:12])
