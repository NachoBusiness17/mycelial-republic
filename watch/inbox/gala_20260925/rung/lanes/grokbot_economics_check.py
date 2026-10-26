# CHECK: grokbot-economics lane (gala 20261003, division A)
# The head's method is the Delta Register (watch/inbox/frontier_delta_steal_20261003.md):
# route on MEASURED capability from replayed production asks, priced per arm.
# This parser applies that method to the register bytes and prices bot-task classes
# against on-disk unit costs. Exit 0 = register parses, all rows computable,
# routing table derivable. Exit 1 = structural failure. Verdict is the exit code.
import json, sys

REGISTER = "watch/inbox/frontier_delta_register_20261003.json"

# On-disk unit costs (each carried by an estate byte, cited in the lane JSON):
PRICES = {
    "opus_rails":   {"usd_per_delivered": 0.55,  "src": "economics.md:43 $7.74/14 asks"},
    "deepseek":     {"usd_per_ask":       0.14,  "src": "frontier_delta_steal_20261003.md:31"},
    "flash_seat":   {"usd_per_delivered": 0.00,  "seat_tokens_per_deliv": 582000, "src": "economics.md:116 (ask-given)"},
    "grok_bot":     {"usd_per_chore":     0.086, "attempts": 2, "src": "GROK47_CLI_BURN_RECEIPT_20260925.md:50-52"},
    "arena_play":   {"usd_per_run":       0.43,  "src": "economics.md:84 38 dirs ~$0.43/run"},
}

try:
    with open(REGISTER, "r", encoding="utf-8") as f:
        rows = json.load(f)
except Exception as e:
    print(f"STRUCTURAL FAIL: cannot read register: {e}")
    sys.exit(1)

if not isinstance(rows, list) or len(rows) == 0:
    print("STRUCTURAL FAIL: register is not a non-empty list")
    sys.exit(1)

need = ["id", "frontier_chars", "frontier_cites", "frontier_unver",
        "flash_chars", "flash_cites", "flash_unver", "contract_parts"]
bad = [r.get("id", "?") for r in rows if not all(isinstance(r.get(k), int) or k == "id" for k in need)]
if bad:
    print(f"STRUCTURAL FAIL: rows missing numeric fields: {bad}")
    sys.exit(1)

print(f"REGISTER PARSED: {len(rows)} rows from {REGISTER}")
print()
print(f"{'task':34s} {'fr_chars':>8s} {'fl_chars':>8s} {'fr_cites':>8s} {'fl_cites':>8s} "
      f"{'fr_unver':>8s} {'fl_unver':>8s} {'contract':>8s}  class")
print("-" * 118)
fr_pays, fl_pays, frontier_only = [], [], []
for r in rows:
    # deltas: positive cite delta = frontier advantage; positive unver delta = frontier DISADVANTAGE
    if r["flash_chars"] == 0:
        cls = "FRONTIER-ONLY (flash never ran)"
        frontier_only.append(r["id"])
    elif r["frontier_unver"] < r["flash_unver"] and r["contract_parts"] > 0:
        cls = "frontier-pays (fewer unver + contract held)"
        fr_pays.append(r["id"])
    else:
        cls = "flash-pays (ties or beats frontier on unver)"
        fl_pays.append(r["id"])
    print(f"{r['id']:34s} {r['frontier_chars']:8d} {r['flash_chars']:8d} "
          f"{r['frontier_cites']:8d} {r['flash_cites']:8d} {r['frontier_unver']:8d} "
          f"{r['flash_unver']:8d} {r['contract_parts']:8d}  {cls}")

tot = {k: sum(r[k] for r in rows) for k in
       ["frontier_chars", "flash_chars", "frontier_cites", "flash_cites",
        "frontier_unver", "flash_unver"]}
n = len(rows)
print("-" * 118)
print(f"{'TOTAL/MEAN':34s} {tot['frontier_chars']:8d} {tot['flash_chars']:8d} "
      f"{tot['frontier_cites']:8d} {tot['flash_cites']:8d} {tot['frontier_unver']:8d} "
      f"{tot['flash_unver']:8d}")
print()
print("PRICED ROUTING TABLE (register deltas x on-disk unit costs)")
print(f"  frontier-pays class   ({len(fr_pays):2d} tasks): {', '.join(fr_pays)}")
print(f"    -> route {PRICES['opus_rails']['usd_per_delivered']:.2f} USD/delivered opus rails ({PRICES['opus_rails']['src']})")
print(f"  flash-pays class      ({len(fl_pays):2d} tasks): {', '.join(fl_pays)}")
print(f"    -> route flash/seat 0.00 USD cash, ~{PRICES['flash_seat']['seat_tokens_per_deliv']} seat tokens/deliv ({PRICES['flash_seat']['src']})")
print(f"  frontier-only class   ({len(frontier_only):2d} task):  {', '.join(frontier_only)}")
print(f"    -> flash arm ABSENT: register cannot price the swap for this class")
print(f"  deepseek default rung: {PRICES['deepseek']['usd_per_ask']:.2f} USD/ask priced, ZERO rows in register "
      f"(economics.md FINDING 4) - cascade 'ds first' rests on price alone")
print(f"  grok bot: {PRICES['grok_bot']['usd_per_chore']:.3f} USD/chore measured, {PRICES['grok_bot']['attempts']}-attempt shape, "
      f"ZERO rows in register - bot class unpriced by the instrument")
print(f"  arena opportunity cost: {PRICES['arena_play']['usd_per_run']:.2f} USD/play-run, 65 pct of 10-03 burn was play "
      f"(economics.md:81-84)")
print()
unver_share = tot['flash_unver'] / max(1, tot['frontier_unver'] + tot['flash_unver'])
cite_share = tot['flash_cites'] / max(1, tot['frontier_cites'] + tot['flash_cites'])
print(f"AGGREGATE: flash carries {unver_share:.0%} of unverified-claim load on "
      f"{cite_share:.0%} of the citation load")
print(f"VERDICT: exit 0 - register parses, {n} rows, all fields computable,")
print(f"  {len(fr_pays)} frontier-pays / {len(fl_pays)} flash-pays / {len(frontier_only)} frontier-only")
sys.exit(0)
