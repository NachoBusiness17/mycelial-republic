"""lattice_build.py — THE LATTICE: the estate map, warmed for hot-swap.

Operator law (2026-09-22): "how are you going to remember a damn thing if you
can't access it — map the estate, warm it in our lattice for hot swapping."
This tool compiles the map + doctrine + instruments + state into ONE bounded
file (memory/lattice/latest.md) that every seat can read at boot. Load-prewarm
law, productized: the map precedes the territory, so the map ships first.

Run: .venv/Scripts/python.exe tools/lattice_build.py
Output: memory/lattice/latest.md (~bounded; safe to inject in any boot pack)
"""
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "memory" / "lattice" / "latest.md"
RIB_DIR = ROOT / "memory" / "rib"
BRIEF = ROOT / "memory" / "briefs" / "latest.md"

MAX_BYTES = 16_000
STALE_HOURS = 48

INSTRUMENTS = [
    ("Smith chart (fleet health)", "tools/estate_smith_chart.py",
     "Gamma = 1 - delivered/claimed per organ, from bytes; bar 0.5; 2h windows. REFLECTING = fixes only."),
    ("Wave smith (meter any lift)", "tools/kv50_smith_chart.py",
     "Point it at a findings JSON; Gamma per lane; no-prose list = re-ask or die."),
    ("Curvature scan (topology)", "tools/curvature_scan.py",
     "Cathedral regions as hill/saddle/dark; 5/6 saddle; eigen vote: water-first."),
    ("Light walk (maze organs)", "tools/light_walk.py",
     "Walks the step tape; gate organs earn light by DEPENDENCE, not fire rate."),
    ("Eigen-map", "watch/inbox/CATHEDRAL_CURVATURE_SCAN_*.json",
     "eigen_centroids per region = coordinates; render maps FROM the metric."),
    ("THE 50 / lift pattern", "dynamic-workflow + dogfood doubling",
     "Fan out N lanes (2-4-8-16-32), gopher-ractor relay per lane, Mickey-17: re-seed or tombstone, never silent."),
    ("Wave bridge (estate width)", "tools/wave_lift.py",
     "Multi-provider round-robin lanes into the orchestrator queue; self-sealing receipts; pipes to smith chart."),
    ("Blind differential probe", "tools/blind_probe.py",
     "Same prompt to free lanes; the delta between models is the trainable signal; SSRF-guarded."),
    ("East/West lens", "tools/eastwest_thorn_20260920.py (pattern)",
     "RS pattern: file West (contract/precision) and East (walk/long-game) separately, then compose ti-yong."),
    ("Ractor chairs (adversarial salon)", "corpus/ractor_ribs/ + salon cards",
     "Chairs: Lessig, Economist, Aristophanes, von Franz, Weil, Elder, Comedian. One candidate must DIE or it was theater."),
    ("72-step pipeline", "OBSTACLE_WAVE_FOLD_20260913 / mag/paste_pipeline.py",
     "INGEST-MAP-ASSERT-ATTACK-MEASURE-CORRECT-CROP; falsifier per stage; step 72 = DISPOSITIONS."),
    ("Portable salon prompt", "watch/inbox/SALON_PROMPT_MANUAL_20260920.md",
     "RIB-format copy-paste salon for zero-context seats; determinism clause: anchors decide, model drafts."),
    ("Needs manifest v2 (operator interface)", "watch/inbox/THE_NEEDS_MANIFEST_20260921.md",
     "Context decides. No GO-waiting for $0 work. Operator owns the stochastic; seat owns the deterministic. Engage human channels when routed."),
    ("Kifu + verkle chain", "memory/ribs + verkle tools",
     "8,819-knot append-only chain; RECORD CLEAN audits; two self-reconstructions."),
    ("Ghost (autonomous layer)", "mag/ghost.py",
     "Copilot lane: exec/steer/read/write/sense; janitor FKB signals; lives in the record, survived the purge."),
    ("Decode scoreboard (2-for-1)", "watch/inbox/SELF_STEAL_TEST_TIME_COMMUNICATION_20260921.md",
     "Papailiopoulos test-time-communication (10 days after our decode) + Mooncake/LMCache KV-cache-as-OS. Dated prior-art maps on file."),
    ("Ten asks + ten-barred-asks", "watch/inbox/kv50_findings.json + ten-asks artifact",
     "The barred asks are operator-ranked tiers; A1 dedupe, A2 freeze_system_prompt, A3 ox heartbeat were the $0 triangle."),
    ("Law lattice (existing organ)", "dashboard/static/lattices/law_lattice.json",
     "lattice_logic.v1: 58 registered laws + law_registry + invariants + field — the fleet's own law graph, self-stolen into this map."),
    ("Corpus index for bots", "watch/CORPUS_INDEX_FOR_BOTS_20260906.md",
     "1,040-card index built to feed external agents — the cold-tier corpus map that predates this lattice."),
    ("Beacon (GWAP v1)", "site/dist/work.html -> https://nacho-business-mag-d961.vercel.app/work.html",
     "6-room walkable site: beacon/play/ledger/fresh/craft/gate; HUD = thought GPS; minimap = eigen-map; shader hero; email gate."),
]

MAP = [
    ("Estate root", "C:/Users/foste/Documents/projects/local_sovereign_agent",
     "mag/ organs, tools/, watch/inbox cards + index_events.jsonl, memory/{rib,runs,game_modules,briefs}, corpus/, dashboard/static."),
    ("Cards register", "watch/inbox/",
     "Every intake/decode/fix card; index_events.jsonl is the register; unregistered writes are tooth marks."),
    ("Runs + judicial record", "memory/runs/",
     "orchestrator/tasks (task records are truth), elder_asks/ (the judicial institution), mickey17/MASTER_INDEX (2,493-row estate digest)."),
    ("RIB doctrine library", "memory/rib/ (43 files)",
     "GRAMMAR_SEED, MAP_PRECEDES_TERRITORY, CATHEDRAL_WORLD_V1, DOCTRINE_CANONICAL + the rest; one-liners below."),
    ("Games (prod)", "games-mag-d961.vercel.app (source: games-site/)",
     "10 games live; estate copies in dashboard/static/games; current builds synced 09-22."),
    ("Beacon (prod)", "site/ -> nacho-business-mag-d961.vercel.app",
     "GWAP v1; build with site/build.py; deploy dir Documents/projects/nacho-business (Vercel team mag-d961)."),
    ("Weights home", "C:/Users/foste/models/ + MANIFEST.json",
     "athena-class-31B keeper (sha on file); saelis grave; dedupe executed; consult MANIFEST before any model question."),
    ("Runtime world", "Windows host stack (since 09-22)",
     "backend :8000, dashboard :8765, mirror :8743, drainer pid in state/autodrain.pid; docker containers RETIRED (stopped, not removed)."),
    ("Free lanes", "deepseek (Swarm key) delivers; MiMo/opencode :4096 (mimo-v2.6-flash-free); ollama night-window only",
     "flash z_ai3 needs operator recharge; family-box law: no local inference while family is on the box."),
]

SECTIONS = [
    ("Load-prewarm law", "feedback-load-prewarm-first.md",
     "L0 pack-first at boot; grep the RIB library before reinventing; state/CURRENT.md + BOOT_4_7.md are stale-boot traps."),
    ("Meters not prose", "feedback-meters-not-prose.md",
     "Unhealthy = fix via the system's own write patterns or build a meter with a pre-stated bar. Meters read NOW (2h windows), never history."),
    ("Decode not invent", "feedback-decode-not-invent.md",
     "foste decodes register-encoded doctrine; convergence = validation receipt (scoreboard 2-for-1). Never 'prior art by him'."),
    ("Plain English", "feedback-plain-english-lessig.md",
     "Chat: plain, short, a little funny. Cards keep the formal register. Lead with what changed and what to do."),
    ("Receipt or CLAIMED", "md record law",
     "Everything md + tracked + registered; a registration without a run date is a lie with good manners; supersede-mark, never delete."),
    ("No local inference while family on box", "feedback-no-local-inference-family-box.md",
     "Heavy local work rides the night window; remote lanes cost the machine nothing."),
    ("One body, many seats", "elder ruling 09-22",
     "Read the newest record + sign your seat before touching shared organs; supersede, never contradict in place."),
]


def rib_lines(limit: int = 40) -> list[str]:
    out = []
    for p in sorted(RIB_DIR.glob("RIB_*.md")):
        try:
            txt = p.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        line = ""
        for ln in txt.splitlines():
            s = ln.strip()
            if s.startswith("# ") and not s.startswith("# The"):
                line = s[2:].strip()
                break
            if s and not s.startswith("#") and not s.startswith("_") and len(s) > 20:
                line = s[:150]
                break
        if line:
            out.append(f"- **{p.stem}** — {line}")
        if len(out) >= limit:
            break
    return out


def meters_block() -> str:
    if not BRIEF.is_file():
        return "(brief missing)"
    txt = BRIEF.read_text(encoding="utf-8", errors="replace")
    i = txt.find("## METERS")
    if i < 0:
        return "(no meters in brief)"
    j = txt.find("\n## ", i + 1)
    block = txt[i:j if j > 0 else len(txt)].strip()
    return "\n".join(block.splitlines()[:8])


def build() -> str:
    now = datetime.now(timezone.utc)
    parts = [
        "# THE LATTICE — estate map, warmed for hot-swap",
        "",
        f"_Generated {now.isoformat(timespec='seconds')} by tools/lattice_build.py · "
        f"load this FIRST at boot; older than {STALE_HOURS}h = STALE, regenerate with "
        f"`.venv/Scripts/python.exe tools/lattice_build.py`_",
        "",
        "## 1. Where everything is",
    ]
    for name, path, note in MAP:
        parts.append(f"- **{name}** — `{path}` — {note}")
    parts.append("")
    parts.append("## 2. The instruments (steal these before building anything)")
    for name, path, note in INSTRUMENTS:
        parts.append(f"- **{name}** — `{path}` — {note}")
    parts.append("")
    parts.append("## 3. Standing doctrine (the laws that bind every seat)")
    for name, _, note in SECTIONS:
        parts.append(f"- **{name}** — {note}")
    parts.append("")
    parts.append("## 4. RIB doctrine library (one-liners; full text in memory/rib/)")
    parts.extend(rib_lines())
    parts.append("")
    parts.append("## 5. Live state (from the brief)")
    parts.append(meters_block())
    parts.append("")
    parts.append("## 6. The beacon")
    parts.append("- **Live:** https://nacho-business-mag-d961.vercel.app/work.html — GWAP v1: "
                 "6 walkable rooms, arrow-key walker, thought-GPS HUD, eigen-minimap, shader hero, email gate.")
    parts.append("- **Arcade:** https://games-mag-d961.vercel.app — 10 games, playtested on prod.")
    parts.append("")
    parts.append("_Hot-swap contract: any seat, any session, any machine — read this file and you are warm. "
                 "Regenerate after material state changes. If it is missing, build it before you work._")
    return "\n".join(parts) + "\n"


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    text = build()
    if len(text.encode("utf-8")) > MAX_BYTES:
        # trim rib lines first (bounded law)
        parts = text.split("## 5. Live state")
        text = parts[0]
        rib_i = text.find("## 4. RIB doctrine library")
        head = text[:rib_i]
        rib_txt = text[rib_i:].splitlines()
        keep = max(8, len(rib_txt) - (len(text.encode("utf-8")) - MAX_BYTES) // 120)
        text = head + "\n".join(rib_txt[:keep]) + "\n_(rib one-liners trimmed for size — full library in memory/rib/)_\n\n## 5. Live state" + parts[1]
    OUT.write_text(text, encoding="utf-8")
    print(f"lattice written: {OUT} ({len(text.encode('utf-8'))} bytes)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
