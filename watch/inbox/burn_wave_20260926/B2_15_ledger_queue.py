# B2-15: append LEDGER row (json.dumps) + QUEUE self-feed briefs. No heredoc.
import json
from datetime import datetime, timezone

TS = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

ledger_row = {
    "ts": TS,
    "slug": "B2-15-xintel-dig-20260926",
    "verdict": "56pct figure confirmed in RESEARCH_GAP_ANALYSIS_20260918.md; two thinnest families (windows/storage 4, swarm/orchestration 4) given a deep pass: 9 live-verified web sources, 11 LINKS.jsonl rows (writer x-intel-dig), 1 process-debt ALERT filed (seed denominator drift 143/88.8 -> 184/84.8 in raw.jsonl bytes)",
    "landing": "watch/inbox/burn_wave_20260926/B2_15_xintel_dig_20260926.md",
    "one_line": "Thin x-intel families (swarm economics, windows reparse law) got their prior-art floor: jitter+retry-budget+circuit-breaker and junction rules+MFT/USN refresh, all quoted live, zero synthesized sources",
}
with open("memory/burns/LEDGER.jsonl", "a", encoding="utf-8") as f:
    f.write(json.dumps(ledger_row, ensure_ascii=True) + "\n")
print("ledger row appended")

briefs = [
    "- [ ] B2-70 Catalog v3 junction policy draft: codify XIDIG-WIN rows (63 reparse points per path, 16KB reparse data, junctions local-volume dirs only never network, symlink UNC contrast) into the catalog scanner so junction pruned 189K rows becomes policy; pointers watch/inbox/LINKS.jsonl XIDIG-WIN-* 2026-09-26 + RESEARCH_GAP_ANALYSIS_20260918.md windows row.",
    "- [ ] B2-71 Driver v2 resilience spec: map XIDIG-SWARM rows onto the union driver (full jitter per AWS, 60-per-process retry budget per SRE, half-open breaker per Azure, 15x token ceiling per Vercel/Anthropic) with cost-per-completed-dig denominator from raw.jsonl 184/156 bytes; pointers watch/inbox/LINKS.jsonl XIDIG-SWARM-* 2026-09-26.",
    "- [ ] B2-72 Gap-analysis denominator refresh: re-derive all 8 gap rows of RESEARCH_GAP_ANALYSIS_20260918.md from ledger bytes (proven drift: seed said 143 attempts/88.8% ok, raw.jsonl 2026-09-26 says 184/156 = 84.8%); pointer XIDIG-SWARM-DENOMINATOR-DRIFT ALERT.",
]
with open("watch/inbox/burn_wave_20260926/QUEUE.md", "a", encoding="utf-8") as f:
    f.write("\n".join(briefs) + "\n")
print("queue briefs appended:", len(briefs))
