"""Build deck.html — the command deck representing what the fleet IS now.

Mines live values from real data files (wave state, physical pack, lane trails,
ledgers, receipts, blueprints) and embeds them as a JSON block inside one
self-contained HTML file. Same pattern as dashboard/static/_build_estate_walk.py:
run the builder, get a fresh surface. The deck is a REFRESH command, not a page.

Usage:
    .venv\\Scripts\\python.exe scripts\\build_deck.py

Output: dashboard/static/deck.html (zero external deps; works from file:// and /static/deck.html).
"""

import json
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "dashboard" / "static" / "deck.html"

LANE_COLORS = {
    "research": "#6fd6ff",
    "day_work": "#fff2c8",
    "builder": "#8dff7a",
    "forge": "#ff7a4d",
    "bard_ledger": "#c98bff",
    "elder": "#ffb347",
    "economist": "#7adcc8",
    "harvest": "#d9b96f",
    "night": "#8b9dff",
    "prose": "#ff9ec2",
    "android_surface": "#9aa7b5",
}

GAMES = [
    ("toy.html", "TOY", "the core-verb toy (U1, 12/12 lanes green)"),
    ("mud.html", "MUD", "the persistent world / bones referee home"),
    ("maze_arena.html", "MAZE ARENA", "arena combat"),
    ("swarm.html", "SWARM", "swarm board (FX1 storage/audio fixes)"),
    ("arrakis.html", "ARRAKIS", "desert surface"),
    ("frontier_souls.html", "FRONTIER SOULS", "U6 souls + NPC voices"),
    ("arena_operator_field.html", "OPERATOR FIELD", "arena operator view"),
]

SURFACES = [
    ("estate_walk.html", "ESTATE WALK", "the repo as a dark navigable space"),
    ("estate_walk.lod.html", "ESTATE LOD", "zone-index spectator (D21)"),
    ("vislab/catalog.html", "VISLAB CATALOG", "render catalog (build_vislab_catalog.py)"),
    ("vislab/play.html", "VISLAB PLAY", "catalog playback"),
    ("pipeline.html", "PIPELINE", "the pipeline surface"),
    ("decks.html", "DECKS", "deck index"),
]


def fleet_seed(date_str: str) -> int:
    """FNV-1a 32-bit over 'fleet-YYYY-MM-DD' — must match fleetSeedOf in the games (W1A)."""
    h = 2166136261
    for ch in "fleet-" + date_str:
        h = ((h ^ ord(ch)) * 16777619) & 0xFFFFFFFF
    return h or 1


def read(p: Path) -> str:
    try:
        return p.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def mine_lanes(now):
    lanes = []
    ldir = ROOT / "queue" / "lanes"
    for d in sorted(ldir.iterdir()) if ldir.exists() else []:
        if not d.is_dir():
            continue
        name = d.name
        rs = {}
        try:
            rs = json.loads(read(d / "runner_state.json") or "{}")
        except json.JSONDecodeError:
            pass
        trail = d / "trail.jsonl"
        rows = 0
        last_ev = ""
        if trail.exists():
            lines = [l for l in read(trail).splitlines() if l.strip()]
            rows = len(lines)
            if lines:
                try:
                    e = json.loads(lines[-1])
                    last_ev = f"{e.get('event', '')}: {e.get('detail', '')}"[:160]
                except json.JSONDecodeError:
                    last_ev = "(unparseable tail)"
        last_run = rs.get("last_run", "")
        age_days = None
        if last_run:
            try:
                t = datetime.fromisoformat(last_run)
                if t.tzinfo is None:
                    t = t.replace(tzinfo=timezone.utc)
                age_days = round((now - t).total_seconds() / 86400, 2)
            except ValueError:
                pass
        if age_days is None:
            state = "NO-RUNNER"
        elif age_days <= 1.0:
            state = "LIVE"
        elif age_days <= 3.0:
            state = "STALE"
        else:
            state = "DORMANT"
        lanes.append({
            "name": name,
            "color": LANE_COLORS.get(name, "#8fa3b8"),
            "state": state,
            "age_days": age_days,
            "last_run": last_run or "—",
            "last_result": rs.get("last_result", "—"),
            "trail_rows": rows,
            "last_event": last_ev,
        })
    return lanes


def mine_ledgers():
    led = {}
    links = ROOT / "watch" / "inbox" / "LINKS.jsonl"
    lines = [l for l in read(links).splitlines() if l.strip()]
    last5 = []
    for l in lines[-5:]:
        try:
            r = json.loads(l)
            last5.append({"ts": r.get("ts", ""), "url": r.get("canonical") or r.get("url", "")})
        except json.JSONDecodeError:
            last5.append({"ts": "?", "url": "(unparseable row)"})
    led["links"] = {"rows": len(lines), "last5": last5, "path": "watch/inbox/LINKS.jsonl"}

    gw = ROOT / "watch" / "GROUNDING_WAVE.jsonl"
    gw_lines = [l for l in read(gw).splitlines() if l.strip()]
    verify_line, verify_rc = "(verify not run)", None
    try:
        p = subprocess.run(
            [sys.executable, "-m", "mag.grounding_wave", "verify"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=120,
        )
        out = (p.stdout + p.stderr).strip().splitlines()
        verify_line = out[-1] if out else f"(exit {p.returncode}, no output)"
        verify_rc = p.returncode
    except Exception as e:  # noqa: BLE001
        verify_line = f"(verify failed: {e})"
    led["grounding"] = {"rows": len(gw_lines), "verify_line": verify_line,
                        "verify_ok": verify_rc == 0, "path": "watch/GROUNDING_WAVE.jsonl"}

    val = {}
    try:
        p = subprocess.run(
            [sys.executable, "-m", "mag.shared_surface", "validate"],
            cwd=str(ROOT), capture_output=True, text=True, timeout=180,
        )
        j = json.loads(p.stdout)
        val = {"ok": j.get("ok"), "files": len(j.get("files", [])),
               "indexed": len(j.get("indexed_items", [])),
               "unindexed": len(j.get("unindexed_items", [])),
               "errors": len(j.get("errors", [])), "warnings": len(j.get("warnings", []))}
    except Exception as e:  # noqa: BLE001
        val = {"ok": None, "error": str(e)[:120]}
    led["index"] = {**val, "path": "watch/inbox/INDEX.json (mag.shared_surface validate)"}
    return led


def mine_receipts(limit=8):
    dirs = [ROOT / "watch" / "inbox" / "wave_20260916" / "receipts",
            ROOT / "watch" / "inbox" / "physical_computing" / "receipts"]
    files = []
    for d in dirs:
        if d.exists():
            files.extend(d.glob("*.md"))
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    out = []
    for p in files[:limit]:
        body = read(p)
        m = re.search(r"(?im)^#.*$", body)
        title = m.group(0).lstrip("# ").strip()[:80] if m else p.stem
        sm = re.search(r"(?im)^status\s*:\s*(.+)$", body)
        status = sm.group(1).strip()[:140] if sm else ""
        rel = p.relative_to(ROOT).as_posix()
        out.append({"date": datetime.fromtimestamp(p.stat().st_mtime, tz=timezone.utc).strftime("%Y-%m-%d %H:%M"),
                    "name": p.stem, "title": title, "status": status, "path": rel})
    return out


def mine_wave_state():
    ws = ROOT / "watch" / "inbox" / "wave_20260916" / "WAVE_STATE_20260916.md"
    body = read(ws)
    m = re.search(r"Receipts indexed:\**\s*(\d+)", body)
    receipts_n = int(m.group(1)) if m else None
    m2 = re.search(r"Stubs/orphans requeued:\**\s*(.+)$", body, re.M)
    requeued = m2.group(1).strip() if m2 else ""
    requeue_rows = []
    in_sec = False
    for line in body.splitlines():
        if line.startswith("## §4"):
            in_sec = True
            continue
        if in_sec and line.startswith("## "):
            break
        if in_sec and line.startswith("|") and not line.startswith("| Item") and "---" not in line:
            cells = [c.strip() for c in line.strip("|").split("|")]
            if len(cells) >= 3:
                requeue_rows.append({"item": cells[0], "why": cells[1], "ask": cells[2]})
    return {"receipts_indexed": receipts_n, "requeued_summary": requeued,
            "requeue": requeue_rows, "path": "watch/inbox/wave_20260916/WAVE_STATE_20260916.md"}


def mine_context_pack():
    body = read(ROOT / "memory" / "context_pack_latest.md")
    tip = re.search(r"tip:\s*(\S+)", body)
    leaves = re.search(r"leaves=(\d+)", body)
    knot = re.search(r"last=(\S+)", body)
    return {"tip": tip.group(1) if tip else "?", "leaves": int(leaves.group(1)) if leaves else None,
            "knot": knot.group(1) if knot else "?"}


def mine_world():
    """CV3: the bones-world's walked sessions (wow_session.v1) + travelers (wow_player.v1).

    A "walk" counts only when a character is attached: the session's seed must name a
    real player ledger. Test residue (bare referee seeds) is counted but never shown
    as the first walk."""
    out = {"sessions": 0, "complete": 0, "first_walk": None, "players": [],
           "path": "memory/runs/wow_world/receipts"}
    pdir = ROOT / "memory" / "runs" / "wow_player"
    names = set()
    for p in sorted(pdir.glob("ply-*.json")) if pdir.exists() else []:
        try:
            d = json.loads(read(p))
        except json.JSONDecodeError:
            continue
        if isinstance(d, dict) and d.get("schema") == "wow_player.v1":
            t = d.get("traits") or {}
            names.add(d.get("name"))
            out["players"].append({"name": d.get("name"), "player_id": d.get("player_id"),
                                   "room": t.get("room"), "ledger_rows": len(d.get("ledger") or []),
                                   "inventory": len(t.get("inventory") or [])})
    rdir = ROOT / "memory" / "runs" / "wow_world" / "receipts"
    recs = []
    for p in sorted(rdir.glob("*.json")) if rdir.exists() else []:
        try:
            r = json.loads(read(p))
        except json.JSONDecodeError:
            continue
        if isinstance(r, dict) and r.get("schema") == "wow_session.v1":
            recs.append(r)
    out["sessions"] = len(recs)
    done = [r for r in recs if r.get("verdict") == "COMPLETE"]
    out["complete"] = len(done)
    walked = [r for r in done if r.get("seed") in names]
    if walked:
        r = walked[0]
        out["first_walk"] = {"session_id": r.get("session_id"), "seed": r.get("seed"),
                             "world": r.get("world"), "route": r.get("route"),
                             "verdict": r.get("verdict"), "moves": len(r.get("moves") or []),
                             "sha256_12": (r.get("sha256") or "")[:12]}
    return out


def mine_programs():
    progs = []
    pc = ROOT / "watch" / "inbox" / "physical_computing"

    # 1. Referee chain (Sep-20 gate)
    directive = read(ROOT / "watch" / "inbox" / "HERMES_DIRECTIVE_BONES_REFEREE_20260916.md")
    dm = re.search(r"^#\s*(.+)$", directive, re.M)
    ws_body = read(ROOT / "watch" / "inbox" / "wave_20260916" / "WAVE_STATE_20260916.md")
    a1 = re.search(r"A1_BLIND_CHALLENGE_SET\.md \| (.+?)$", ws_body, re.M)
    progs.append({
        "id": "referee", "title": "REFEREE CHAIN / BLIND EPISTEMICS",
        "gate": "SEP-20",
        "status": "A1 SEALED · A2 stone-1 FILED · B14 pre-registered, execution queued (forge/night)",
        "detail": (dm.group(1).strip() if dm else "BONES AS THE REFEREE") +
                  " — end-to-end demo a stranger can watch from a phone; scope freezes: M0 only until demo ships.",
        "facts": [
            "A1: " + (a1.group(1)[:160] if a1 else "blind challenge set"),
            "referee: mag/wow_bones_session.py + 12 tests, green 35/35 across the wow suite",
            "D20 /bones adapter: code landed, OPERATOR-BLOCKED (token rotation + #game-c-overview 403)",
        ],
        "sources": ["watch/inbox/HERMES_DIRECTIVE_BONES_REFEREE_20260916.md",
                    "watch/inbox/wave_20260916/receipts/A1_BLIND_CHALLENGE_SET.md",
                    "watch/inbox/wave_20260916/receipts/D20_BONES_ADAPTER.md"],
    })

    # 2. Cube program
    c17 = read(pc / "receipts" / "C17_CUBE_INSTRUMENT_PLAN.md")
    cm = re.search(r"(?im)^status\s*:\s*(.+)$", c17)
    shop = read(pc / "CUBE1_SHOPPING_LIST.md")
    sm = re.search(r"assembly proposed\s+(.+?)\.", shop)
    progs.append({
        "id": "cube", "title": "CUBE PROGRAM (instrumented mycelium cube)",
        "gate": "GO-PENDING",
        "status": cm.group(1).strip() if cm else "FILED 2026-09-16 — proposal tier (two-eyes pending)",
        "detail": "The ONE instrumented cube: echo-state characterization FIRST, then binary "
                  "discrimination vs random-noise baseline (n=100, α=0.05). Stage 0 = the ear, "
                  "electronics only, ~$31. Stage 1 = biology, only after a clean noise floor.",
        "facts": [
            "stage-0 assembly proposed " + (sm.group(1).strip() if sm else "2026-09-22 (fallback 09-29)"),
            "skeptic rider: artifact:signal ≈ 95:5 undefended; $45–60 with Faraday + Ag/AgCl DIY + calibration",
            "dozen cubes collapse into a dozen clonable cards (C19: Adamatzky 8× differential PCB)",
        ],
        "sources": ["watch/inbox/physical_computing/receipts/C17_CUBE_INSTRUMENT_PLAN.md",
                    "watch/inbox/physical_computing/CUBE1_SHOPPING_LIST.md"],
    })

    # 3. Ractor plugin
    p1 = read(ROOT / "watch" / "inbox" / "wave_20260916" / "receipts" / "P1_RACTOR_PACKAGE.md")
    checks = re.findall(r"^\d+\.\s+\*\*(.+?)\*\*", p1, re.M)
    ractor_repo = Path(r"C:\Users\foste\Documents\projects\ractor-salon")
    progs.append({
        "id": "ractor", "title": "RACTOR PLUGIN (open-source, standalone)",
        "gate": "OPERATOR-PUBLISH",
        "status": f"LANDED — standalone repo at ../ractor-salon{' (exists on disk)' if ractor_repo.exists() else ' (NOT FOUND on disk)'}"
                  " · publish checklist state: OPERATOR-executed, not yet run",
        "detail": "plugin.json + pyproject + src + tests + CI (3.9–3.12) + real stdio MCP server (U9). "
                  "P2 demo salon: 10 answers, 25 metered calls, $0.",
        "facts": [f"checklist step {i+1}: {c}" for i, c in enumerate(checks[:6])] or
                 ["publish checklist: venv tests → git init+tag → gh auth → repo create/push/release → catalog PR → optional PyPI"],
        "sources": ["watch/inbox/wave_20260916/receipts/P1_RACTOR_PACKAGE.md",
                    "watch/inbox/wave_20260916/receipts/U9_UNION_MCP_SERVER.md"],
    })

    # 4. Physical pack
    pack = read(pc / "PHYSICAL_COMPUTING_PACK_20260916.md")
    pv = re.search(r"Version\s+([\d.]+)", pack)
    progs.append({
        "id": "pack", "title": "PHYSICAL COMPUTING PACK",
        "gate": "v" + (pv.group(1) if pv else "1.x"),
        "status": "Folds landed through §6.8 · falsifiers §4.1–§4.5 binding",
        "detail": "Water, light, laser-etched silicon, mycelium. The sovereign physical layer: "
                  "make, etch, or grow our own. Sampler claim: CONDITIONAL-REFUTED pending formal closure.",
        "facts": [
            "§4.1 salon-ESS: probe ρ=+0.167 p=0.70 (wrong-signed) → replicate ρ=+0.327 n=36 p=0.052 — graze, closure receipt owed",
            "§4.5 DAD: no sim stone counts as substrate evidence until a physical artifact confirms/contradicts a prediction",
            "C15 verdict: PARTIAL-SUPPORT, OPTIMISTIC-EDGE · Landauer 1.05e13 ceiling STRUCK (ours, first)",
            "C19: dozen cubes → dozen clonable cards · Extropic Z1 140× replication seat OPEN ($0)",
        ],
        "sources": ["watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md"],
    })

    # 5. World build M0–M5
    bp = read(ROOT / "watch" / "inbox" / "WOW_CLONE_BETA_BLUEPRINT_20260916.md")
    miles = re.findall(r"^- \*\*(M\d) — (.+?)\.\*\*", bp, re.M)
    wfacts = [f"{mid}: {mtxt}" for mid, mtxt in miles] or ["blueprint milestones unreadable"]
    w = mine_world()
    if w["first_walk"]:
        fw = w["first_walk"]
        wfacts.append("FIRST WALK: " + " -> ".join(fw["route"]) +
                      f" · seed {fw['seed']} · {fw['moves']} moves · verdict {fw['verdict']}"
                      f" · {fw['session_id']} · receipt sha256:{fw['sha256_12']}")
    for p in w["players"]:
        wfacts.append(f"traveler {p['name']} ({p['player_id']}) at {p['room']}"
                      f" · ledger {p['ledger_rows']} rows · inventory {p['inventory']}")
    if not w["players"]:
        wfacts.append("no traveler has carried world/room yet (the world is unwalked)")
    progs.append({
        "id": "world", "title": "WORLD BUILD (M0–M5)",
        "gate": "SCOPE-FREEZE→SEP-20",
        "status": "M0 LANDED (W1 wow_world.py, atrium-ring) · M2 LANDED (W2 wow_player.py 17/17, byte-identical resume) · next M2.5+",
        "detail": "Verifiable play: every session is a receipt and every receipt replays. "
                  "The free week is the drafting sprint; the editor seat is forever.",
        "facts": wfacts,
        "sources": ["watch/inbox/WOW_CLONE_BETA_BLUEPRINT_20260916.md",
                    "watch/inbox/wave_20260916/receipts/W1_WORLD_SKELETON.md",
                    "watch/inbox/wave_20260916/receipts/W2_PLAYER_FILES.md"],
    })

    # 6. Myco-memory ladder
    mm = read(pc / "DESIGN_MYCO_MEMORY_20260916.md")
    steps = re.findall(r"^- \*\*Step (\d) — (.+?)\.\*\*", mm, re.M)
    progs.append({
        "id": "myco", "title": "MYCO-MEMORY LADDER",
        "gate": "STEPS 0–5",
        "status": "DESIGN FILED · step 0 (the ear) = cube stage-0, awaiting build",
        "detail": "Living memory hierarchy: registers (ms) → VRAM (reservoir fading memory, capacity "
                  "0.048–0.209, Telhan 2026) → disk (hyphal remodeling) → archive (sclerotia). "
                  "Every step must be CONSUMED by the fleet.",
        "facts": [f"step {n}: {t}" for n, t in steps] or ["steps unreadable"],
        "sources": ["watch/inbox/physical_computing/DESIGN_MYCO_MEMORY_20260916.md"],
    })
    return progs


# PROGRAMS.json — the machine-readable program-state ledger (N1's wished-for source).
# First candidate wins; state/ is gitignored so the durable root is watch/inbox/.
PROGRAM_JSON_CANDIDATES = [
    ROOT / "watch" / "inbox" / "wave_20260916" / "PROGRAMS.json",
    ROOT / "watch" / "inbox" / "PROGRAMS.json",
    ROOT / "state" / "programs.json",
]

PROGRAM_TITLES = {
    "referee-chain": "REFEREE CHAIN / BLIND EPISTEMICS",
    "cube-program": "CUBE PROGRAM (instrumented mycelium cube)",
    "ractor-salon": "RACTOR PLUGIN (open-source, standalone)",
    "grounding-wave": "GROUNDING WAVE (evidence chain)",
    "ractor-engine": "RACTOR ENGINE (diffusion witnesses)",
    "blind-challenge-set": "BLIND CHALLENGE SET (BCS-20260916)",
    "mud-replay-law": "MUD REPLAY LAW",
}


def load_programs():
    """PROGRAMS.json when present (the deck becomes data-driven); prose-scrape fallback.

    Ledger row schema (programs.v1): {program, status: green|amber|red,
    gate: none|operator-click|funding|decision, evidence: [paths], updated, next_stone}.
    The fold lane updates rows each wave; the deck renders them verbatim instead of
    regex-scraping prose receipts (the N1 weak point: a heading-format change silently
    degraded a scraped card to 'unreadable')."""
    for cand in PROGRAM_JSON_CANDIDATES:
        if not cand.exists():
            continue
        try:
            doc = json.loads(read(cand))
        except (json.JSONDecodeError, OSError):
            continue
        rows = doc.get("programs") if isinstance(doc, dict) else doc
        if not isinstance(rows, list) or not rows:
            continue
        cards = []
        for r in rows:
            if not isinstance(r, dict) or not r.get("program"):
                continue
            pid = str(r["program"]).strip()
            cards.append({
                "id": pid,
                "title": PROGRAM_TITLES.get(pid, pid.replace("-", " ").upper()),
                "gate": str(r.get("gate", "none")),
                "status": "NEXT STONE: " + str(r.get("next_stone", "")),
                "detail": "",
                "facts": [],
                "sources": [str(s) for s in (r.get("evidence") or [])],
                "health": str(r.get("status", "amber")).lower(),
                "ledger_updated": str(r.get("updated", "")),
            })
        if cards:
            try:
                src = str(cand.relative_to(ROOT).as_posix())
            except ValueError:
                src = str(cand)
            return cards, src
    return mine_programs(), "prose-scrape fallback (no readable PROGRAMS.json found)"


def mine_next_stones(wave):
    stones = []
    for r in wave.get("requeue", []):
        kind = "OPERATOR-GATE" if "D20" in r["item"] or "B13" in r["item"] else "GEN-2"
        stones.append({"kind": kind, "item": r["item"], "ask": r["ask"]})
    extra = [
        {"kind": "CLOSURE", "item": "sampler falsifier closure receipt",
         "ask": "file threshold provenance + variable definitions in ONE closure receipt before the word 'refuted' is earned (p=0.052 graze; U5 witness)"},
        {"kind": "OPERATOR-GATE", "item": "ractor publish checklist",
         "ask": "repo create / push / release + catalog PR vs NousResearch/hermes-agent (operator account, operator call)"},
        {"kind": "THIS-WEEK", "item": "cube stage-0 order + assembly",
         "ask": "order the $31 ear; assembly proposed 2026-09-22 (fallback 09-29)"},
        {"kind": "THIS-WEEK", "item": "union-alpha window",
         "ask": "free window closes ~2026-09-23 — spend it (pin 'Disputed' referent in tri-state asks; call non-streaming ≥180s)"},
        {"kind": "THIS-WEEK", "item": "Extropic Z1 replication seat",
         "ask": "point the fleet at the public simulator; measure ESS/compute vs digital baseline under DAD accounting ($0)"},
        {"kind": "LATER", "item": "CONCERT 002",
         "ask": "schedule after the grown-boundary assay"},
    ]
    stones.extend(extra)
    return stones


def build_html(data):
    # surfaces existence check at build time
    static = ROOT / "dashboard" / "static"
    for s in data["surfaces"]:
        s["exists"] = (static / s["href"]).exists()

    js = json.dumps(data, ensure_ascii=False, indent=1).replace("</", "<\\/")
    generated = data["meta"]["generated"]
    template = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<title>COMMAND DECK — local_sovereign_agent</title>
<meta name="viewport" content="width=device-width, initial-scale=1">
<style>
  :root{--bg:#07090d;--panel:#0b1017;--line:#1c2a3d;--txt:#8fa3b8;--hi:#d8e6f2;--dim:#5c7186;--accent:#6fd6ff;--bad:#ff5d5d;--good:#8dff7a;--warn:#ffb347}
  *{box-sizing:border-box}
  html,body{margin:0;background:var(--bg);color:var(--txt);font:13px/1.5 ui-monospace,Consolas,monospace}
  a{color:var(--accent);text-decoration:none}a:hover{text-decoration:underline}
  header{padding:26px 22px 10px;border-bottom:1px solid var(--line)}
  header h1{margin:0;font-size:16px;letter-spacing:.35em;color:var(--hi);font-weight:600}
  header .sub{margin-top:6px;font-size:11px;color:var(--dim)}
  nav{display:flex;flex-wrap:wrap;gap:6px;padding:12px 22px;border-bottom:1px solid var(--line);position:sticky;top:0;background:rgba(7,9,13,.94);backdrop-filter:blur(4px);z-index:5}
  nav a{font-size:11px;letter-spacing:.12em;padding:4px 10px;border:1px solid var(--line);border-radius:3px;color:var(--txt)}
  nav a:hover{border-color:var(--accent);color:var(--accent);text-decoration:none}
  main{max-width:1240px;margin:0 auto;padding:18px 22px 60px}
  section{margin-top:26px}
  h2{font-size:12px;letter-spacing:.3em;color:var(--hi);font-weight:600;border-bottom:1px solid var(--line);padding-bottom:6px}
  h2 .n{color:var(--dim);letter-spacing:0}
  .grid{display:grid;gap:12px}
  .cards{grid-template-columns:repeat(auto-fit,minmax(340px,1fr))}
  .card{background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:12px 14px}
  .card h3{margin:0 0 4px;font-size:12px;letter-spacing:.14em;color:var(--hi)}
  .chip{display:inline-block;font-size:10px;letter-spacing:.14em;padding:1px 8px;border-radius:3px;border:1px solid var(--line);margin-left:6px;vertical-align:1px}
  .chip.gate{color:var(--warn);border-color:#5c4a22}
  .chip.ok{color:var(--good);border-color:#2c4a22}
  .chip.bad{color:var(--bad);border-color:#5a2222}
  .card .st{font-size:11px;color:var(--accent);margin:4px 0}
  .card p{margin:6px 0;font-size:12px}
  ul{margin:6px 0 0;padding-left:16px}
  li{margin:3px 0;font-size:12px}
  .src{margin-top:8px;font-size:10px;color:var(--dim)}
  .strip{display:flex;flex-wrap:wrap;gap:10px}
  .kpi{flex:1 1 170px;background:var(--panel);border:1px solid var(--line);border-radius:6px;padding:10px 12px}
  .kpi .k{font-size:10px;letter-spacing:.18em;color:var(--dim)}
  .kpi .v{margin-top:4px;font-size:15px;color:var(--hi);word-break:break-word}
  .kpi .v.small{font-size:11px;color:var(--txt)}
  .bad{color:var(--bad)}.good{color:var(--good)}.warn{color:var(--warn)}
  table{width:100%;border-collapse:collapse;background:var(--panel);border:1px solid var(--line);border-radius:6px;overflow:hidden}
  th{font-size:10px;letter-spacing:.18em;color:var(--dim);text-align:left;padding:8px 10px;border-bottom:1px solid var(--line)}
  td{padding:7px 10px;border-bottom:1px solid #101823;font-size:12px;vertical-align:top}
  tr:last-child td{border-bottom:0}
  .lane{font-weight:600}
  .dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
  .wrap{word-break:break-all}
  footer{margin-top:40px;padding-top:12px;border-top:1px solid var(--line);font-size:11px;color:var(--dim)}
  @media (max-width:720px){.cards{grid-template-columns:1fr}}
</style>
</head>
<body>
<header>
  <h1>COMMAND DECK</h1>
  <div class="sub">local_sovereign_agent · wave_20260916 · generated __GENERATED__ · refresh: <code>.venv\\Scripts\\python.exe scripts\\build_deck.py</code></div>
</header>
<nav id="nav"></nav>
<main id="main"></main>
<script id="deck-data" type="application/json">__DATA__</script>
<script>
"use strict";
const D = JSON.parse(document.getElementById('deck-data').textContent);
const esc = s => String(s == null ? '' : s).replace(/[&<>"']/g, c => ({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
const chip = (t, cls) => `<span class="chip ${cls}">${esc(t)}</span>`;

function kpi(k, v, cls) {
  return `<div class="kpi"><div class="k">${esc(k)}</div><div class="v ${cls || 'small'}">${v}</div></div>`;
}

function standingWave() {
  const g = D.ledgers.grounding, ix = D.ledgers.index, w = D.wave, cp = D.context_pack;
  const vCls = g.verify_ok ? 'good' : 'bad';
  return `<section id="standing-wave"><h2>STANDING WAVE <span class="n">// era 003 · THE POUR</span></h2>
  <div class="strip">
    ${kpi('GROUNDING WAVE VERIFY', `<span class="${vCls}">${esc(g.verify_line)}</span>`)}
    ${kpi('GROUNDING ROWS', g.rows)}
    ${kpi('WAVE RECEIPTS INDEXED', w.receipts_indexed == null ? '?' : w.receipts_indexed)}
    ${kpi('INDEX HEALTH (the F)', ix.ok === true ? '<span class="good">OK</span>' : ix.ok === false ? '<span class="bad">NOT OK</span>' : '<span class="warn">UNKNOWN</span>',
         ix.ok ? 'good' : 'bad')}
    ${kpi('INDEX ERRORS', ix.errors == null ? esc(ix.error || '?') : ix.errors, ix.errors ? 'bad' : '')}
    ${kpi('GIT TIP', esc((D.git[0] || '?').split(' ')[0]))}
    ${kpi('CONTEXT PACK', `tip ${esc(cp.tip)} · leaves ${cp.leaves == null ? '?' : cp.leaves}`)}
  </div>
  <div class="src">sources: ${g.path} · watch/inbox/wave_20260916/WAVE_STATE_20260916.md · watch/inbox/INDEX.json · memory/context_pack_latest.md · git log -5</div>
  <ul style="margin-top:10px">${D.git.map(l => `<li class="wrap">${esc(l)}</li>`).join('')}</ul></section>`;
}

function programs() {
  const hc = h => h === 'green' ? 'ok' : h === 'red' ? 'bad' : 'gate';
  return `<section id="programs"><h2>PROGRAMS <span class="n">// ${D.programs.length} · ${esc(D.programs_source || '')}</span></h2><div class="grid cards">` +
    D.programs.map(p => `<div class="card"><h3>${esc(p.title)}${chip(p.gate, 'gate')}${p.health ? chip(p.health.toUpperCase(), hc(p.health)) : ''}</h3>
      <div class="st">${esc(p.status)}</div>` +
      (p.detail ? `<p>${esc(p.detail)}</p>` : '') +
      `<ul>${(p.facts || []).map(f => `<li>${esc(f)}</li>`).join('')}</ul>` +
      (p.id === 'world' ? '<p id="mud-relay" class="src">relay: probing :8766/mud/state …</p>' : '') +
      `<div class="src">${p.ledger_updated ? 'updated ' + esc(p.ledger_updated) + ' · ' : ''}sources: ${(p.sources || []).map(s => esc(s)).join(' · ')}</div></div>`).join('') +
    '</div></section>';
}

/* N11 live relay lens: WORLD card probes GET /mud/state at page load.
   Fire-and-forget — never blocks render; any failure (refused, timeout,
   ok:false from a squatter service) degrades to an OFFLINE line. */
async function mudRelay() {
  const el = document.getElementById('mud-relay');
  if (!el) return;
  const url = 'http://127.0.0.1:8766/mud/state';
  try {
    const ctl = new AbortController();
    const t = setTimeout(() => ctl.abort(), 1500);
    const r = await fetch(url, { signal: ctl.signal });
    clearTimeout(t);
    if (!r.ok) throw new Error('http ' + r.status);
    const s = await r.json();
    if (!s || s.ok !== true) throw new Error('not the mud relay (ok:false)');
    const ps = s.players || [];
    const n = ps.length;
    const age = n ? Math.min.apply(null, ps.map(p => (typeof p.age === 'number' ? p.age : 0))) : null;
    el.innerHTML = 'relay <span class="good">LIVE</span> · players ' + n +
      (n ? ' · last lantern ' + age.toFixed(1) + 's old' : ' · room dark (0 lanterns)') +
      ' · seen_total ' + (s.seen_total == null ? '?' : s.seen_total) +
      ' · <a href="' + url + '" target="_blank">/mud/state</a>';
  } catch (e) {
    const msg = (e && e.name === 'AbortError') ? 'timeout 1.5s' : String((e && e.message) ? e.message : e);
    el.innerHTML = 'relay <span class="bad">OFFLINE</span> (' + esc(msg) + ')' +
      ' · start: <code>.venv/Scripts/python.exe dashboard/mud_relay.py</code>';
  }
}

function lanes() {
  const order = {LIVE: 0, STALE: 1, 'NO-RUNNER': 2, DORMANT: 3};
  const rows = D.lanes.slice().sort((a, b) => (order[a.state] - order[b.state]) || a.name.localeCompare(b.name));
  const live = rows.filter(l => l.state === 'LIVE').length;
  return `<section id="lanes"><h2>LIVE LANES <span class="n">// ${live}/${rows.length} live</span></h2>
  <table><tr><th>LANE</th><th>STATE</th><th>LAST RUN</th><th>RESULT</th><th>TRAIL</th><th>LAST EVENT</th></tr>` +
    rows.map(l => `<tr><td class="lane"><span class="dot" style="background:${l.color}"></span>${esc(l.name)}</td>
      <td>${chip(l.state, l.state === 'LIVE' ? 'ok' : l.state === 'STALE' ? 'gate' : 'bad')}</td>
      <td>${esc(l.last_run) + (l.age_days == null ? '' : ` <span class="src">(+${l.age_days}d)</span>`)}</td>
      <td class="wrap">${esc(l.last_result)}</td>
      <td>${l.trail_rows} rows</td><td class="wrap">${esc(l.last_event)}</td></tr>`).join('') +
    '</table><div class="src">sources: queue/lanes/*/runner_state.json + trail.jsonl · LIVE = ran within 24h, STALE ≤ 3d, DORMANT older</div></section>';
}

function receipts() {
  return `<section id="receipts"><h2>RECEIPTS <span class="n">// latest ${D.receipts.length} by mtime</span></h2>
  <table><tr><th>WHEN</th><th>RECEIPT</th><th>STATUS</th></tr>` +
    D.receipts.map(r => `<tr><td>${esc(r.date)}</td><td><a class="wrap" href="../../${esc(r.path)}">${esc(r.name)}</a><div class="src wrap">${esc(r.title)}</div></td>
      <td class="wrap">${esc(r.status) || '<span class="src">—</span>'}</td></tr>`).join('') +
    '</table><div class="src">links resolve from file:// (repo-relative ../../watch/…); when served from /static the paths are still the canonical locations</div></section>';
}

function ledgers() {
  const L = D.ledgers, l5 = L.links.last5.map(r => `<li class="wrap">${esc(r.ts || '')} <a href="${esc(r.url)}">${esc(r.url)}</a></li>`).join('');
  return `<section id="ledgers"><h2>LEDGERS <span class="n">// counts + claim statuses</span></h2><div class="grid cards">
    <div class="card"><h3>LINKS LEDGER</h3><p><span class="v" style="font-size:20px;color:var(--hi)">${L.links.rows}</span> rows</p>
      <ul>${l5}</ul><div class="src">${esc(L.links.path)}</div></div>
    <div class="card"><h3>GROUNDING WAVE</h3><p><span class="v" style="font-size:20px;color:var(--hi)">${L.grounding.rows}</span> rows · verify: <span class="${L.grounding.verify_ok ? 'good' : 'bad'}">${esc(L.grounding.verify_line)}</span></p>
      <ul><li>chain broken at row 122 (prev-hash mismatch) — repair lane owed</li></ul><div class="src">${esc(L.grounding.path)}</div></div>
    <div class="card"><h3>SHARED SURFACE INDEX</h3><ul>
      <li>ok: <span class="${L.index.ok ? 'good' : 'bad'}">${L.index.ok == null ? 'unknown' : L.index.ok}</span></li>
      <li>files ${L.index.files == null ? '?' : L.index.files} · indexed ${L.index.indexed == null ? '?' : L.index.indexed} · unindexed ${L.index.unindexed == null ? '?' : L.index.unindexed}</li>
      <li>errors <span class="bad">${L.index.errors == null ? '?' : L.index.errors}</span> · warnings ${L.index.warnings == null ? '?' : L.index.warnings}</li>
    </ul><div class="src">${esc(L.index.path)}</div></div>
    <div class="card"><h3>SAMPLER CLAIM</h3><p>${chip('CONDITIONAL-REFUTED', 'gate')}</p>
      <ul><li>probe: ρ +0.167, n=8, p=0.70 — wrong-signed</li>
      <li>replicate: ρ +0.327, n=36, p=0.052 — past the +0.3 line, but a graze</li>
      <li>U5 witness: refutation CONDITIONAL on formal closure receipt (threshold provenance + variable definitions filed together)</li>
      <li>salon_50 = 39/50 answered, NOT 50/50 (fossil, 55 occurrences in the wild)</li></ul>
      <div class="src">watch/inbox/physical_computing/PHYSICAL_COMPUTING_PACK_20260916.md §6 · WAVE_STATE §3</div></div>
  </div></section>`;
}

function surfaces() {
  return `<section id="surfaces"><h2>SURFACES <span class="n">// ${D.surfaces.length + D.games.length} linked · existence-checked at build</span></h2>
  <div class="grid cards">` +
    D.games.map(g => `<div class="card"><h3>${esc(g.name)}</h3><p>${esc(g.desc)}</p>
      <div class="src"><a href="${esc(g.href)}">open ${esc(g.href)}</a>${g.exists ? '' : ' <span class="bad">MISSING</span>'}</div></div>`).join('') +
    D.surfaces.map(s => `<div class="card"><h3>${esc(s.name)}</h3><p>${esc(s.desc)}</p>
      <div class="src"><a href="${esc(s.href)}">open ${esc(s.href)}</a>${s.exists ? '' : ' <span class="bad">MISSING</span>'}</div></div>`).join('') +
    '</div><div class="src">relative links work from file:// and from /static/deck.html</div></section>';
}

function nextStones() {
  const cls = k => k === 'OPERATOR-GATE' ? 'bad' : k === 'GEN-2' ? 'gate' : k === 'CLOSURE' ? 'gate' : 'ok';
  return `<section id="next-stones"><h2>NEXT STONES <span class="n">// gen-2 requeue + operator gates</span></h2>
  <table><tr><th>KIND</th><th>ITEM</th><th>ASK</th></tr>` +
    D.next_stones.map(s => `<tr><td>${chip(s.kind, cls(s.kind))}</td><td class="wrap">${esc(s.item)}</td><td class="wrap">${esc(s.ask)}</td></tr>`).join('') +
    '</table><div class="src">sources: WAVE_STATE_20260916.md §4 + program receipts</div></section>';
}

const SECTIONS = [
  ['standing-wave', 'STANDING WAVE', standingWave],
  ['programs', 'PROGRAMS', programs],
  ['lanes', 'LIVE LANES', lanes],
  ['receipts', 'RECEIPTS', receipts],
  ['ledgers', 'LEDGERS', ledgers],
  ['surfaces', 'SURFACES', surfaces],
  ['next-stones', 'NEXT STONES', nextStones],
];
document.getElementById('main').innerHTML = SECTIONS.map(s => s[2]()).join('');
document.getElementById('nav').innerHTML = SECTIONS.map(s => `<a href="#${s[0]}">${s[1]}</a>`).join('');
mudRelay();
</script>
</body>
</html>"""
    html = template.replace("__DATA__", js).replace("__GENERATED__", generated)
    return html


def main():
    now = datetime.now(timezone.utc)
    wave = mine_wave_state()
    data = {
        "meta": {
            "generated": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
            "wave": "wave_20260916",
            "builder": "scripts/build_deck.py",
            "note": "regenerate with .venv/Scripts/python.exe scripts/build_deck.py",
        },
        "wave": wave,
        "context_pack": mine_context_pack(),
        "world": mine_world(),
        "lanes": mine_lanes(now),
        "ledgers": mine_ledgers(),
        "receipts": mine_receipts(),
    }
    data["programs"], data["programs_source"] = load_programs()
    data["git"] = []
    data["games"] = []
    try:
        p = subprocess.run(["git", "log", "-5", "--oneline"], cwd=str(ROOT),
                           capture_output=True, text=True, timeout=30)
        data["git"] = [l for l in p.stdout.splitlines() if l.strip()]
    except Exception:  # noqa: BLE001
        data["git"] = ["(git log unavailable — wave law: no git)"]
    data["games"] = [{"href": "games/" + h, "name": n, "desc": d} for h, n, d in GAMES]
    data["surfaces"] = [{"href": h, "name": n, "desc": d} for h, n, d in SURFACES]
    data["next_stones"] = mine_next_stones(wave)
    # fleet seed law (W1A · THE WEAVE #58): today's shared game seed. mud / frontier_souls / toy
    # auto-seed from "fleet-YYYY-MM-DD" (FNV-1a 32) — same day, same starting world on every rung.
    fleet_date = now.strftime("%Y-%m-%d")
    data["fleet"] = {
        "date": fleet_date,
        "seed": fleet_seed(fleet_date),
        "games": ["games/mud.html", "games/frontier_souls.html", "games/toy.html"],
        "law": "fleet-YYYY-MM-DD -> FNV-1a 32 -> LCG seed; explicit seeds always win",
    }

    html = build_html(data)
    OUT.write_text(html, encoding="utf-8")
    print(f"deck written: {OUT} ({OUT.stat().st_size} bytes)")
    print(f"fleet: {data['fleet']['date']} seed {data['fleet']['seed']}")
    print(f"programs={len(data['programs'])} source={data['programs_source']}")
    print(f"lanes={len(data['lanes'])} receipts={len(data['receipts'])} "
          f"links_rows={data['ledgers'].get('links', {}).get('rows')} "
          f"verify={data['ledgers'].get('grounding', {}).get('verify_line', '')[:60]}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
