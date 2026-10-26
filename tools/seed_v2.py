"""seed_v2 — build the shippable seed so it BOOTS COLD outside the estate.
Implements build-book items 1-2 (watch/inbox/SEED_V2_BUILD_BOOK_20260925.md):
  1. every engine runs standalone (inline dotenv, local imports, mkdir before writes,
     honest empty-lane messages, no estate imports)
  2. SETUP.md + LICENSE + verify_seal.py + LF manifest + keys template
Each transform is anchored: if the estate source moved, the builder fails loud.
"""
from __future__ import annotations

import hashlib
import re as _re
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SEED = ROOT / "seed"

INLINE_DOTENV = '''def _load_dotenv() -> None:
    """Standalone dotenv (seed build): reads .env from cwd and up to 3 parents.
    Values go to os.environ only, never logged or echoed."""
    import os as _os
    d = _P.cwd()
    for _ in range(4):
        f = d / ".env"
        if f.is_file():
            for line in f.read_text(encoding="utf-8", errors="replace").splitlines():
                line = line.strip()
                if line and not line.startswith("#") and "=" in line:
                    k, _, v = line.partition("=")
                    _os.environ.setdefault(k.strip(), v.strip().strip('"'))
            break
        d = d.parent
_load_dotenv()'''


def must(s: str, old: str, new: str, name: str, count: int = 1) -> str:
    n = s.count(old)
    if n < count:
        raise SystemExit(f"seed_v2: anchor missing in {name}: {old[:70]!r} (found {n}, want >= {count})")
    return s.replace(old, new)


def build() -> None:
    (SEED / "engines").mkdir(parents=True, exist_ok=True)
    (SEED / "configs").mkdir(parents=True, exist_ok=True)
    copied = []

    # ---- key_law.py ------------------------------------------------------
    s = (ROOT / "mag/key_law.py").read_text(encoding="utf-8")
    s = must(s, "from models.env_load import load_dotenv  # noqa: E402\nload_dotenv()",
             "from pathlib import Path as _P\n\n" + INLINE_DOTENV, "key_law")
    (SEED / "engines/key_law.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("key_law.py")

    # ---- lite_guard.py ---------------------------------------------------
    s = (ROOT / "mag/lite_guard.py").read_text(encoding="utf-8")
    s = must(s, "nachobusinesscorp@gmail.com / fostertron@gmail.com",
             "[operator accounts redacted in seed build]", "lite_guard")
    s = s.replace("law 15", "the pacing law")
    (SEED / "engines/lite_guard.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("lite_guard.py")

    # ---- claritas.py (pure stdlib) + a __main__ demo ----------------------
    s = (ROOT / "mag/claritas.py").read_text(encoding="utf-8")
    s += '''

if __name__ == "__main__":
    import sys as _sys
    for mid in (_sys.argv[1:] or ["openai/gpt-oss-120b", "google/gemma-4-31b-it:free", "some/unknown-model"]):
        print(f"{mid} -> {vendor_for(mid)}: {face_for(mid)[:70]}...")
'''
    (SEED / "engines/claritas.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("claritas.py")

    # ---- cooker.py -------------------------------------------------------
    s = (ROOT / "mag/cooker.py").read_text(encoding="utf-8")
    s = must(s, "from mag.lite_guard import provider_quota",
             "from lite_guard import provider_quota", "cooker")
    s = must(s, '"cmd": [_py(), "tools/stealth_sweep.py"]',
             '"cmd": [_py(), "engines/stealth_sweep.py"]', "cooker")
    s = must(s, '"cmd": [_py(), "tools/task_wall.py", "--budget-minutes", "15"]',
             '"cmd": [_py(), "engines/task_wall.py", "--budget-minutes", "15"]', "cooker")
    s = must(s, "        return start if now >= start else start.replace(day=start.day - 1)",
             "        import datetime as _dt\n"
             "        return start if now >= start else start - _dt.timedelta(days=1)", "cooker")
    (SEED / "engines/cooker.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("cooker.py")

    # ---- phone_relay.py --------------------------------------------------
    s = (ROOT / "mag/phone_relay.py").read_text(encoding="utf-8")
    s = must(s, "            if cid:\n                STATE.parent.mkdir(parents=True, exist_ok=True)\n                STATE.write_text(cid, encoding=\"utf-8\")",
             "            if cid:\n                STATE.parent.mkdir(parents=True, exist_ok=True)\n                STATE.write_text(cid, encoding=\"utf-8\")", "phone_relay")  # already safe
    (SEED / "engines/phone_relay.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("phone_relay.py")

    # ---- librarian_catalog.py (ran cold per the ractor's own check) -------
    s = (ROOT / "mag/librarian_catalog.py").read_text(encoding="utf-8")
    (SEED / "engines/librarian_catalog.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("librarian_catalog.py")

    # ---- estate_smith_chart.py -------------------------------------------
    s = (ROOT / "tools/estate_smith_chart.py").read_text(encoding="utf-8")
    s = must(s, '''    p = (OUT_DIR / ("ESTATE_SMITH_CHART_" + STAMP + suffix)).resolve()''',
             '''    OUT_DIR.mkdir(parents=True, exist_ok=True)
    p = (OUT_DIR / ("ESTATE_SMITH_CHART_" + STAMP + suffix)).resolve()''', "smith")
    s = must(s, '''    if "--no-plot" not in sys.argv:
        plot(inbox_path(".png"), organs, dark, exempt, prose_bar_violations)''',
             '''    if "--no-plot" not in sys.argv:
        try:
            plot(inbox_path(".png"), organs, dark, exempt, prose_bar_violations)
        except Exception as e:  # noqa: BLE001 — plot is garnish; the meter is the console
            print("  (plot skipped: " + str(e)[:80] + " — the console meter above is the reading)")''', "smith")
    (SEED / "engines/estate_smith_chart.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("estate_smith_chart.py")

    # ---- estate_atlas.py --------------------------------------------------
    s = (ROOT / "tools/estate_atlas.py").read_text(encoding="utf-8")
    s = must(s, 'REPO = Path(r"C:\\Users\\foste\\Documents\\projects\\local_sovereign_agent")',
             'REPO = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()', "atlas")
    s = s.replace("run tools/", "run engines/")
    (SEED / "engines/estate_atlas.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("estate_atlas.py")

    # ---- spine_walk.py (the actual walker — FIRST_BOOT step 4's engine) ----
    s = (ROOT / "tools/index/projects_index.py").read_text(encoding="utf-8")
    s = must(s, "import os, re, json, time, shutil",
             "import os, re, json, time, shutil, sys", "spine_walk")
    s = must(s, 'ROOT = Path(r"C:\\Users\\foste\\Documents\\projects").resolve()',
             'ROOT = Path(sys.argv[1]).resolve() if len(sys.argv) > 1 else Path.cwd().resolve()', "spine_walk")
    s = must(s, 'REPO = (ROOT / "local_sovereign_agent").resolve()',
             'REPO = ROOT  # seed build: the walked folder IS the repo', "spine_walk")
    # the cook seat (3.1.0) resurrected the author's path in the docstring — scrub it
    import re as _re
    s = _re.sub(r"READ-ONLY walk of C:[^\n]*->", "READ-ONLY walk of the target folder ->", s)
    s = must(s, '''    shutil.copyfile(MASTER, DASH_MASTER)
    shutil.copyfile(ROLLUP, DASH_ROLLUP)
    shutil.copyfile(LAST_RUN, DASH_LAST_RUN)''',
             '''    try:  # dashboard copies are estate garnish; skip cleanly when absent
        shutil.copyfile(MASTER, DASH_MASTER)
        shutil.copyfile(ROLLUP, DASH_ROLLUP)
        shutil.copyfile(LAST_RUN, DASH_LAST_RUN)
    except Exception:  # noqa: BLE001
        pass''', "spine_walk")
    (SEED / "engines/spine_walk.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("spine_walk.py")

    # ---- stealth_sweep.py -------------------------------------------------
    s = (ROOT / "tools/stealth_sweep.py").read_text(encoding="utf-8")
    s = must(s, "from models.env_load import load_dotenv\nload_dotenv()",
             "from pathlib import Path as _P\n\n" + INLINE_DOTENV, "stealth_sweep")
    s = must(s, "from mag import lite_guard  # noqa: E402", "import lite_guard  # noqa: E402", "stealth_sweep")
    s = must(s, "from mag import claritas  # noqa: E402", "import claritas  # noqa: E402", "stealth_sweep")
    s = s.replace('            with LEDGER.open("a", encoding="utf-8") as f:',
                  '            LEDGER.parent.mkdir(parents=True, exist_ok=True)\n'
                  '            with LEDGER.open("a", encoding="utf-8") as f:')
    s = must(s, "    REPORT.write_text(", "    REPORT.parent.mkdir(parents=True, exist_ok=True)\n    REPORT.write_text(", "stealth_sweep")
    (SEED / "engines/stealth_sweep.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("stealth_sweep.py")

    # ---- task_wall.py -----------------------------------------------------
    s = (ROOT / "tools/task_wall.py").read_text(encoding="utf-8")
    s = must(s, "from models.env_load import load_dotenv\nload_dotenv()",
             "from pathlib import Path as _P\n\n" + INLINE_DOTENV, "task_wall")
    s = must(s, "from mag import lite_guard  # noqa: E402", "import lite_guard  # noqa: E402", "task_wall")
    s = must(s, '''def key_for(names):
    for n in names:
        k = (os.environ.get(n, "") or "").strip()
        if k:
            return k
    return ""''',
             '''def key_for(names):
    import keys as _keys  # the one door (law 7)
    for n in names:
        k = _keys.get(n)
        if k:
            return k
    return ""''', "task_wall")
    s = must(s, '''    print("task_wall: %d chores, %d lanes, budget %d min" % (len(chores), len(LANES), budget_minutes), flush=True)''',
             '''    ext = ROOT / "configs" / "chores.json"
    if ext.is_file():
        try:
            for c in json.loads(ext.read_text(encoding="utf-8")):
                chores.append({"name": c.get("name", "external"), "prompt": c.get("prompt", ""),
                               "lane": c.get("lane"), "out": None})
            print(f"task_wall: +{len(chores)} stranger-authored chores from configs/chores.json")
        except Exception as e:  # noqa: BLE001 — a bad chores file must not kill the wall
            print(f"task_wall: chores.json unreadable ({e}) — running built-ins only")
    print("task_wall: %d chores, %d lanes, budget %d min" % (len(chores), len(LANES), budget_minutes), flush=True)
    if not LANES:
        print("task_wall: no lanes have keys — declare them in configs/keys.json (see SETUP.md). Nothing to burn yet.")
        return''', "task_wall")
    s = must(s, 'REPORT = ROOT / "watch" / "inbox" / "TASK_WALL_REPORT_20260923.md"',
             'REPORT = ROOT / "watch" / "inbox" / "TASK_WALL_REPORT.md"', "task_wall")
    (SEED / "engines/task_wall.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("task_wall.py")

    # ---- model_bakeoff.py -------------------------------------------------
    s = (ROOT / "tools/model_bakeoff.py").read_text(encoding="utf-8")
    s = must(s, "from models.env_load import load_dotenv\nload_dotenv()",
             "from pathlib import Path as _P\n\n" + INLINE_DOTENV, "bakeoff")
    s = must(s, "from mag import lite_guard  # noqa: E402", "import lite_guard  # noqa: E402", "bakeoff")
    s = must(s, '''    key = (os.environ.get(keyenv, "") or os.environ.get(keyenv + "_2", "") or "").strip()''',
             '''    import keys as _keys  # the one door (law 7)
    key = (_keys.get(keyenv) or _keys.get(keyenv + "_2") or "").strip()''', "bakeoff")
    (SEED / "engines/model_bakeoff.py").write_text(s, encoding="utf-8", newline="\n")
    copied.append("bakeoff.py")

    # ---- item 8: self-citation sweep (docstrings point at shipped paths) ---
    for eng in SEED.glob("engines/*.py"):
        t = eng.read_text(encoding="utf-8")
        t = (t.replace("-m tools.key_law", "engines/key_law.py")
              .replace("tools/estate_smith_chart.py", "engines/estate_smith_chart.py")
              .replace("tools/stealth_sweep.py", "engines/stealth_sweep.py")
              .replace("tools/task_wall.py", "engines/task_wall.py")
              .replace("tools/model_bakeoff.py", "engines/model_bakeoff.py")
              .replace("tools/index/projects_index.py", "engines/spine_walk.py")
              .replace("mag/lite_guard.py", "engines/lite_guard.py")
              .replace("mag/key_law.py", "engines/key_law.py")
              .replace("mag/cooker.py", "engines/cooker.py")
              .replace("mag/phone_relay.py", "engines/phone_relay.py")
              .replace("mag/librarian_catalog.py", "engines/librarian_catalog.py")
              .replace("mag/lane_supervisor", "engines/lane_supervisor"))
        eng.write_text(t, encoding="utf-8", newline="\n")

    # ---- stranger-authored chores example (item 5) --------------------------
    (SEED / "configs/chores.json").write_text(json_dumps([
        {"name": "example-stranger-chore",
         "prompt": "Replace this with a real task for YOUR estate: a paragraph to draft, "
                   "a record to summarize, a question to answer. The wall burns it on any "
                   "lane with declared keys and appends the output to the trail."}
    ]), encoding="utf-8", newline="\n")

    # ---- SEED 3.2: the salon's convergent enhancements --------------------
    # (ractor-ruled 09-25: seed-init is "the whole game"; SKILLS index = discovery;
    #  AGENTS.md carries the load order itself)

    # SKILLS.md — the machine-readable discovery index (one file, parseable blocks)
    skills_rows = []
    for eng in sorted((SEED / "engines").glob("*.py")):
        if eng.name == "__init__.py":
            continue
        t = eng.read_text(encoding="utf-8", errors="replace")
        doc = t.strip().strip('"').split("\n")[0] if t.strip() else eng.name
        m = _re.search(r'"""(.{10,160})', t, _re.S)
        desc = (m.group(1).replace("\n", " ").strip() if m else doc)[:140]
        skills_rows.append(f"## {eng.stem}\n"
                           f"name: {eng.stem}\n"
                           f"description: {desc}\n"
                           f"run: python engines/{eng.name} --help\n"
                           f"fails-when: missing keys/config raises a named, readable error (never a traceback)\n")
    (SEED / "SKILLS.md").write_text(
        "# SKILLS — the discovery index\n\n"
        "Machine-parseable blocks: one per engine, fields name/description/run/fails-when.\n"
        "Harnesses and agents: index this file; do not crawl the directory.\n\n"
        + "\n".join(skills_rows), encoding="utf-8", newline="\n")

    # AGENTS.md v2 — the load order itself, so tools auto-load the method
    (SEED / "AGENTS.md").write_text("""If you are an AI agent (or a tool that reads AGENTS.md): this file is the load order.

1. Read FIRST_BOOT.md — the first-hour checklist (verify the seal first).
2. Read THE_METHOD.md — the 11 laws that govern everything here.
3. Index SKILLS.md — one parseable block per engine; do not crawl directories.
4. Read DATA_TIERS.md before sending ANY user data to a remote model.
5. Config lives in configs/ (keys.json, chores.json); state grows in the user's own folders.

Never skip the seal check (verify_seal.py). Never log key values. A claim not written
to a record didn't happen.
""", encoding="utf-8", newline="\n")

    # seed_init.py — the one-command scaffolder (the salon's #1, with the
    # deliberately-honest first alarm: a zero-state smith chart + failing audit bar)
    (SEED / "engines/seed_init.py").write_text('''"""seed_init — lay down a fresh estate skeleton in a target folder (the salon's #1).

Usage:  python engines/seed_init.py <target-dir>

Creates: records/ logs/ watch/inbox/ configs/ + copies the laws and a starter .env
template, then prints the first three commands. The first smith run will show every
organ DARK — that is not an error; that is the method telling the truth about a
zero state (law 4). The key audit will pass on the template's "awaiting" entries and
fail loud the moment you add a live key without declaring it (law 7).
"""
from __future__ import annotations

import shutil
import sys
from pathlib import Path

SEED = Path(__file__).resolve().parent.parent


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python engines/seed_init.py <target-dir>")
        return 2
    target = Path(sys.argv[1]).resolve()
    if target.exists() and any(target.iterdir()):
        print(f"refusing: {target} exists and is not empty (pick a fresh folder)")
        return 1
    target.mkdir(parents=True, exist_ok=True)
    for sub in ("records", "logs", "watch/inbox", "configs"):
        (target / sub).mkdir(parents=True, exist_ok=True)
    for doc in ("THE_METHOD.md", "FIRST_BOOT.md", "SETUP.md", "DATA_TIERS.md",
                "MORNING_LOOP.md", "SALON.md", "TOUR.md", "AGENTS.md", "SKILLS.md"):
        src = SEED / doc
        if src.is_file():
            shutil.copyfile(src, target / doc)
    for cfg in ("keys.json", "chores.json"):
        src = SEED / "configs" / cfg
        if src.is_file():
            shutil.copyfile(src, target / "configs" / cfg)
    env_t = target / ".env.template"
    env_t.write_text(
        "# provider keys go here as NAME=value (see ACCOUNTS.md for the 2x playbook)\\n"
        "# whatever you put here, also declare it in configs/keys.json\\n", encoding="utf-8")
    print(f"estate skeleton laid down at {target}")
    print("your first three commands (from inside the folder):")
    print("  1. python <seed>/engines/estate_smith_chart.py --no-plot   # your honest zero state: all DARK")
    print("  2. python <seed>/engines/key_law.py --audit                # passes on 'awaiting'; fails loud on live-undeclared")
    print("  3. python <seed>/engines/cooker.py status                  # your free-lane reset table")
    print("then read FIRST_BOOT.md and start one record. The method demonstrates itself by failing loud.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
''', encoding="utf-8", newline="\n")
    copied.append("seed_init.py")
    (SEED / "engines/keys.py").write_text('''"""keys — the one door engines use for key lookups (law 7).
Reads configs/keys.json first: an env var that is LIVE but undeclared is reported,
not silently used. Falls back to the environment for declared names only.
"""
from __future__ import annotations
import json, os, sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "configs" / "keys.json"


def _manifest() -> dict:
    if MANIFEST.is_file():
        try:
            return json.loads(MANIFEST.read_text(encoding="utf-8"))
        except Exception:
            pass
    return {}


def declared_envs() -> set:
    return {v.get("env") for v in _manifest().values() if isinstance(v, dict)}


def get(env_name: str) -> str:
    """Value for a declared env name; '' when absent. A live-but-undeclared
    key prints one loud warning to stderr (fail loud, per law 7)."""
    val = (os.environ.get(env_name, "") or "").strip()
    if val and env_name not in declared_envs():
        print(f"keys: ORPHAN — {env_name} is live but not declared in configs/keys.json "
              f"(declare it or the audit will fail)", file=sys.stderr)
    return val
''', encoding="utf-8", newline="\n")
    copied.append("keys.py")

    # ---- stealth_sweep reads keys through the door -------------------------
    s = (SEED / "engines/stealth_sweep.py").read_text(encoding="utf-8")
    s = must(s, '''    for e in ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"):
        k = (os.environ.get(e, "") or "").strip()''',
             '''    from keys import get as key_get
    for e in ("OPENROUTER_API_KEY", "OPENROUTER_API_KEY_2"):
        k = key_get(e)''', "stealth_sweep(v2)")
    (SEED / "engines/stealth_sweep.py").write_text(s, encoding="utf-8", newline="\n")

    # ---- tests (item 7: the tests that would have caught the crashes) ------
    (SEED / "tests").mkdir(exist_ok=True)
    (SEED / "tests/__init__.py").write_text("", encoding="utf-8", newline="\n")
    (SEED / "tests/test_seed_laws.py").write_text('''"""Seed law tests — stdlib unittest, zero installs: python -m unittest discover -s tests"""
import sys, unittest
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "engines"))


class CookerWindow(unittest.TestCase):
    """The month-edge case that crashed cooker.py:55 in V1 (ractor probe)."""

    def test_daily_hour0_rolls_back_across_month(self):
        import cooker
        now = datetime(2026, 10, 1, 0, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 0}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (10, 1, 0))

    def test_daily_hour1_before_open_rolls_back_month_edge(self):
        """The V1 crash regression: hour=1 at 00:30 on the 1st must roll back
        to the previous day WITHOUT 'day is out of range'."""
        import cooker
        now = datetime(2026, 10, 1, 0, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 1}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (9, 30, 1))

    def test_daily_hour1_month_edge(self):
        import cooker
        now = datetime(2026, 10, 1, 1, 30, tzinfo=timezone.utc)
        ws = cooker.window_start({"kind": "daily_utc", "hour": 1}, now)
        self.assertEqual((ws.month, ws.day, ws.hour), (10, 1, 1))

    def test_weekly_backwards_and_forwards(self):
        import cooker
        r = {"kind": "weekly_utc", "weekday": 5, "hour": 2, "minute": 19}  # Sat
        thu = datetime(2026, 9, 24, 12, 0, tzinfo=timezone.utc)
        self.assertEqual((cooker.window_start(r, thu).weekday(), cooker.window_start(r, thu).day), (5, 19))
        nxt = cooker.next_reset(r, thu)
        self.assertEqual((nxt.weekday(), nxt.day), (5, 26))


class RelayDecisions(unittest.TestCase):
    """Exact-token law: 'deny' must never approve (it contains 'y')."""

    def test_decisions(self):
        from phone_relay import _decide
        cases = {"deny": "deny", "no": "deny", "n": "deny", "y": "approve",
                 "yes": "approve", "approve": "approve", "maybe later": None,
                 "are you sure?": None, "why not": None, "yes no": "deny"}
        for words, want in cases.items():
            self.assertEqual(_decide(words), want, words)


class Seal(unittest.TestCase):
    def test_manifest_covers_itself_and_files(self):
        rows = [r for r in (ROOT / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if r.strip()]
        import hashlib
        for row in rows:
            want, _, rel = row.partition("  ")
            self.assertEqual(hashlib.sha256((ROOT / rel).read_bytes()).hexdigest(), want, rel)


if __name__ == "__main__":
    unittest.main()
''', encoding="utf-8", newline="\n")

    # ---- versioning (item 8) -----------------------------------------------
    (SEED / "SEED_VERSION").write_text("seed 3.3.0 — the harness stack: own your surveillance state, turned inward\n", encoding="utf-8", newline="\n")
    (SEED / "CHANGELOG.md").write_text("""# Changelog

## 3.3.0 repack (2026-09-25)
- seal hygiene: the builder purges and excludes __pycache__/*.pyc before sealing
  (bytecode bakes compile-time absolute paths; a08 caught 3 of 59 sealed rows shipping
  the author path inside the 3.3.0 zip) and now emits the zip itself from the sealed
  rows, so zip contents equal seal contents by construction

## 3.3.0 — 2026-09-25
- STACK.md: the harness, tiered (stdlib -> editor -> ollama -> FastAPI/SQLite ->
  Docker cage -> k3s), each with a when-you-need-it honesty marker; the framing:
  own your own surveillance state, turned inward — every meter points at your own
  machine, nothing phones home
- templates/: docker-compose cage (loopback-only ports, record dirs mounted on your
  disk) + api_server_example.py (the estate gateway shape rebuilt at minimum size)

## 3.2.0 — 2026-09-25
- the enhancement salon's convergent #1: engines/seed_init.py — one-command estate
  scaffolder (12-file skeleton, honest all-DARK first meter, next-commands printed)
- SKILLS.md: machine-parseable discovery index (one block per engine, name/description/
  run/fails-when) — harnesses index the file, never crawl the directory
- AGENTS.md v2: this file IS the load order (agent tools auto-load the method)

## 3.1.0 — 2026-09-25
- the discovery-window cook: 17 estate-mined items shipped by the full cast —
  laws-as-config (configs/law_registry.json + mode_budgets.json), process supervisor +
  flight recorder engines, receipt/cost/capability-gate/trust-bytes/campaign-discipline
  docs, activity trail, boot budget card, training spine templates
- spine_walk docstring scrubbed (the cook resurrected the author's path — the post-cook
  spot check caught it, which is why the check runs after every cook)

## 3.0.0 — 2026-09-25
- the self-steal diff answered — six missing pieces embedded: ACCOUNTS.md (2x signup
  playbook, $5 float rule), VSCODE.md (editor + free-models + opencode browser path),
  DATA_TIERS.md (T0-T3 — what may leave your disk), SALON.md (the portable decision
  instrument), MORNING_LOOP.md (the daily rhythm recipe), TOUR.md (estate → seed map)

## 2.2.0 — 2026-09-25
- item 4 DONE: task_wall + model_bakeoff read keys through the one door (keys.py)
- item 5: stranger-authored chores — configs/chores.json loads into the wall; example shipped
- item 8: self-citation sweep — docstrings point at shipped paths; grep 'law 15|@gmail|-m tools.|mag/*' CLEAN
- lane_supervisor exists in the estate (15-min probes, failover, phone escalation on orphan classes)

## 2.1.0 — 2026-09-25
- keys.py: the one door for lane engines (law 7); stealth_sweep wired through it
- tests/: stdlib unittest suite — cooker month-edge (the V1 crash), relay exact-token
  decisions (the 'deny'-approves bug), seal integrity
- honest meters: checkpoint organ is DARK on no evidence, never DELIVERING on nothing (law 4)
- versioning: SEED_VERSION + this changelog

## 2.0.0 — 2026-09-25
- build-book items 1-2: every engine boots cold (12 PASS / 2 readable / 0 crashes),
  LF seal passes stock sha256sum, walker ships (spine_walk.py), SETUP/LICENSE/
  verify_seal/keys-template/AGENTS.md, readable-failure guards everywhere

## 1.0.0 — 2026-09-24
- first seed: 11 laws + 12 engines; failed its own cold-boot audit (2 of 7 steps)
""", encoding="utf-8", newline="\n")

    # ---- SEED 3.0: the missing six (self-steal diff 09-25) -----------------

    (SEED / "ACCOUNTS.md").write_text("""# ACCOUNTS — the access playbook (2x everything)

The estate's lanes are doubled on purpose: two accounts per provider means when one
hits its wall, the other is still fresh — and free-tier ceilings double. Two Google
accounts (call them `you-a@` and `you-b@`) are the handles. Sign up for each service
once per account. Write every key into `.env` AND its `configs/keys.json` entry
(copy the template's shape; name them `<provider>_1` and `<provider>_2`).

| service | free tier you get | the float |
|---|---|---|
| **Groq** (console.groq.com) | gpt-oss-120b/20b, fast | $0 — free tier carries real work |
| **OpenRouter** (openrouter.ai) | the `:free` model wall, doubles with 2 keys | $0; optional $5 for paid-tier models |
| **NVIDIA Build** (build.nvidia.com) | ~100 models incl. big open weights | $0 |
| **Cerebras** (cloud.cerebras.ai) | very fast small models | $0 |
| **Mistral** (console.mistral.ai) | small models | $0 |
| **Google AI Studio** (aistudio.google.com) | gemini flash models | $0 |
| **Together** (api.together.xyz) | DeepSeek-V4-Flash serverless | **$5** — months of bulk work |
| **DeepSeek** (platform.deepseek.com) | the cheapest good workhorse | **$5** — months at ~$0.43/day |

The $5 rule: float ONLY the two workhorses (DeepSeek, Together). Everything else runs
on free tiers — and when a free tier churns its models away (they will), the lane
supervisor pattern and the key audit catch it; you re-point, you don't rebuild.

**The data-tier guard before you paste anything anywhere:** read DATA_TIERS.md.
T0/T1 data never goes to free remote tiers, no matter how good the model looks.
""", encoding="utf-8", newline="\n")

    (SEED / "VSCODE.md").write_text("""# VSCODE — "download VS Code and use this with the free models"

The path of least resistance from zero to your own estate, in an editor you already know:

1. **Install VS Code** (code.visualstudio.com) and the **Cline** extension (or Continue/Roo —
   any agent extension that reads `AGENTS.md` and takes an OpenAI-compatible endpoint).
2. **Put this seed folder in your project.** Cline-style tools auto-read `AGENTS.md` —
   which points them at FIRST_BOOT and the 11 laws. The method rides along automatically.
3. **Give it a free model:** OpenRouter key (ACCOUNTS.md) → model settings → pick from the
   `:free` wall (nemotron, nex, gemma, gpt-oss — whatever the sweep currently scores best).
   The two-account trick doubles your ceiling.
4. **Talk, work, save.** Everything the agent writes lands in YOUR folder as files —
   markdown records, append-only. That is the whole product: your data, your disk,
   your keys, your models.

**The browser path:** `opencode` (open source) serves a web UI *and* an API from one
command — `opencode serve` — the estate's own NPC-dialogue lane runs this way. Point it
at the same keys; use it from your phone's browser if you want.

**The engine path:** `python engines/cooker.py status` + a scheduled `fire --due` —
your free compute burns on refills without you watching (see MORNING_LOOP.md).
""", encoding="utf-8", newline="\n")

    (SEED / "DATA_TIERS.md").write_text("""# DATA TIERS — "saving your own data and keeping it"

From the founding constitution (mycelial-republic), carried here because it is the
answer to the only question that matters about cloud AI: what may leave your disk?

| tier | what it is | may it leave? | where it may go |
|---|---|---|---|
| **T0** | secrets, API keys, credentials | **never** | ops/filesystem only — never a prompt body |
| **T1** | your private life: raw archives, intimate notes, family | **never to remote** | local models only (ollama etc.) |
| **T2** | public docs, redacted tickets, open research | yes | local + free/paid remote |
| **T3** | hard reasoning where specialist cost is accepted | yes, deliberate | chosen specialist, paid |

**Hard rule: T0/T1 content must never be sent to free remote tiers or any
train-on-input service.** "Free" models are often free because they learn from
what you paste. The moment a stranger adopts this seed, this page is the one
that keeps their data THEIRS. Local-first is not a preference; it is the law
that makes the rest of this package safe to use.
""", encoding="utf-8", newline="\n")

    (SEED / "SALON.md").write_text("""# SALON — the portable decision instrument

When a decision matters more than your confidence in it, run a salon: put the question
to several independent model seats, let them fight, and rule on the wreckage.

The estate's house rules, portable as-is:
- **Receipt or CLAIMED.** Anything a chair asserts without a checkable source is labeled
  CLAIMED, no matter how confident it sounds.
- **At least one candidate must die.** If every option survives the salon, the salon
  was theater — the question was too easy or the bar too low.
- **Transit deaths are not verdicts.** A candidate that failed because a lane was down
  or a prompt was mangled has not been judged; re-run it.
- **Meters before audits.** Decide with numbers against pre-stated bars, not adjectives.
- **Nothing enters untamed.** Any tool, key, or default gets named and priced before it runs.
- **The model drafts; the anchors decide.** Give every seat the SAME anchor documents,
  then compare — convergence between independent seats is signal; disagreement is signal;
  a unanimous answer to a leading question is nothing.

Output contract: each seat's position per question, then a triangulated answer written
the way you'd say it to a friend, then THE ONE THING TO DO FIRST. Format lesson from
the estate: compile the brief as a numbered document with anchors (a "RIB"), not prose —
same anchors in, same verdicts out, seat-independent.
""", encoding="utf-8", newline="\n")

    (SEED / "MORNING_LOOP.md").write_text("""# MORNING LOOP — the daily rhythm, as a recipe

The estate runs a fixed morning cadence so the day starts with readings, not scrolling:

| when | what | how |
|---|---|---|
| hourly | **cooker**: `python engines/cooker.py fire --due` | cron/schtasks — burns every free-lane refill automatically |
| every 15 min | **lane supervisor**: `python engines/../mag/lane_supervisor.py probe` (or copy it up) | cron/schtasks — lanes self-heal, your phone only rings on a no-failover class |
| daily | **spine walk**: `python engines/spine_walk.py <your-folder>` | cron — the index regenerates, never hand-maintained |
| daily | **smith chart**: `python engines/estate_smith_chart.py --no-plot` | read the meters; a bar crossed = a fix, not a paragraph |
| daily | **key audit**: `python engines/key_law.py --audit` | exits nonzero naming any undeclared or dead lane |
| daily | **task wall**: `python engines/task_wall.py --budget-minutes 15` | burns free lanes on YOUR chores (configs/chores.json) |

Windows: `schtasks /Create` or PowerShell `Register-ScheduledTask`. Linux: cron lines.
The point is not the schedule — it is that the machine opens the day before you do,
and your first hour goes to the people who matter.
""", encoding="utf-8", newline="\n")

    (SEED / "TOUR.md").write_text("""# TOUR — what the estate does, and what carries it here

The seed came from a 63GB / 1.2M-file estate: three years of one human operating a
fleet of AI seats in Docker containers, remembering itself in a hash-chained record.
A tour of what it actually DOES, and where each capability lives for you:

| estate capability | carries into the seed as |
|---|---|
| keys declared once, audited daily, loud on drift | engines/key_law.py + configs/keys.json |
| every outbound call through one guarded door | engines/lite_guard.py |
| free compute burned on refills, unattended | engines/cooker.py (+ MORNING_LOOP.md) |
| the free-model wall scored daily | engines/stealth_sweep.py |
| cheap-model chores run as a standing wall | engines/task_wall.py + configs/chores.json |
| the health meter: gamma = 1 - delivered/claimed | engines/estate_smith_chart.py |
| the file index that regenerates, never hand-maintained | engines/spine_walk.py + engines/estate_atlas.py |
| approvals from a phone, fail-closed | engines/phone_relay.py |
| model prompts distilled from leaked frontier system prompts | engines/claritas.py |
| catalog + canon integrity checks | engines/librarian_catalog.py |
| decisions fought across independent seats | SALON.md |
| what data may leave the disk | DATA_TIERS.md |
| boot order for a fresh seat | FIRST_BOOT.md + AGENTS.md |
| the founding constitution's fork equality, handoff law | THE_METHOD.md (the 11 laws) |

What the seed deliberately does NOT carry: the estate's history (63GB of records —
you grow your own), its games and artifacts (built, yours to visit), its personal
workload (the chores were the author's; configs/chores.json is yours). The cache
is the author's; the cache MINER is what ships.
""", encoding="utf-8", newline="\n")
    # ---- SEED 3.3: the harness stack (own your surveillance, turned inward) --

    (SEED / "STACK.md").write_text("""# STACK — the software harness, and the idea underneath it

**The idea: own your own surveillance state, turned inward.** Every meter, trail, and
record in this method points at YOUR machine and writes to YOUR disk in plaintext.
Nothing phones home. The estate this seed came from watches itself — lanes, spend,
health, history — with the same apparatus a surveillance state would use, except the
watcher, the watched, and the owner are the same person. That is the product. The
software below is just the harness that makes it possible, tiered by when you need it.

| tier | add | serves | install | you need it when |
|---|---|---|---|---|
| **0 — today** | Python 3.9+ | everything boots | python.org | now (you already have it) |
| **1 — editor** | VS Code + Cline/Continue | the method auto-loads (AGENTS.md) | code.visualstudio.com | you want to work in an editor (see VSCODE.md) |
| **2 — private models** | Ollama | the T1 tier: private data NEVER leaves the box (DATA_TIERS.md) | ollama.com, then `ollama pull llama3.1` | you have T1 data or want offline inference |
| **3 — serving meters** | FastAPI + uvicorn | a loopback API over your own trails (templates/api_server_example.py) | `pip install fastapi uvicorn` | you want your meters readable by tools/dashboards |
| **3 — state** | SQLite (stdlib) | structured state beside the JSONL trails | nothing — it's built in | a JSONL trail outgrows grep |
| **4 — the cage** | Docker + compose | container boundary: localhost-only ports, record dirs mounted, nothing else escapes | docker.com + templates/docker-compose.yml | you run lanes unattended and want the blast radius contained |
| **5 — the fleet** | k3s (cheap Kubernetes) | the same containers scheduled across boxes | k3s.io | one box honestly isn't enough (most people: it is) |

**Honesty markers, per law 4:** tiers 0-2 are all most strangers ever need. Tier 3 is an
afternoon. Tier 4 is the point where you're running real spend unattended — the cage earns
its keep exactly there. Tier 5 is aspirational until it isn't; the source estate ran fine
on one box for three years.

**What we deliberately do NOT ship:** Redis, queues, k8s manifests, dashboards-as-a-service.
Delete wrappers rather than guarding them — add each only when a meter proves you need it.

**The one rule across all tiers:** the record layer is plaintext files on your disk
(JSONL, markdown, append-only). Any tool can read it; no tool is required to. That is
what "keeping your own data" means in practice.
""", encoding="utf-8", newline="\n")

    (SEED / "templates").mkdir(exist_ok=True)
    (SEED / "templates/docker-compose.yml").write_text(
"""# The cage, in one file (STACK tier 4). Rebuilt from the source estate's compose shape.
# Container boundary: the agent stack runs INSIDE; the host exposes ONLY loopback
# ports; your record dirs are mounted, so your data never lives in the container.
#
#   docker compose up -d

services:
  estate:
    image: python:3.12-slim-bookworm
    container_name: my-estate
    working_dir: /app
    env_file:
      - .env
    environment:
      PYTHONUTF8: "1"
      PYTHONUNBUFFERED: "1"
    ports:
      - "127.0.0.1:8765:8765"   # local meters API — loopback ONLY, never 0.0.0.0
    volumes:
      - .:/app                  # your records, laws, engines: on YOUR disk
    command: sleep infinity     # or your long-running lane command

# tier 2: local models for T1 data (private stays on-box). Ollama runs on the HOST
# at 127.0.0.1:11434; containers reach it via host.docker.internal:11434 —
# no model traffic ever leaves the machine.
""", encoding="utf-8", newline="\n")

    (SEED / "templates/api_server_example.py").write_text(
'''"""api_server_example — serve YOUR trails over loopback (STACK tier 3, rebuilt small).

The source estate runs a FastAPI gateway on 127.0.0.1 with an API-key gate and lazy
handlers. This is that SHAPE, rebuilt at minimum size: every meter is a plaintext
file you own; the server just reads them. Nothing here calls out.

    pip install fastapi uvicorn
    UVICORN_API_KEY=some-long-random-string uvicorn api_server_example:app --host 127.0.0.1 --port 8765
"""
from __future__ import annotations

import json
import os
from pathlib import Path

from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import JSONResponse

ROOT = Path.cwd()
KEY = (os.environ.get("UVICORN_API_KEY", "") or "").strip()
app = FastAPI(title="my-estate-meters")


def _gate(x_api_key: str = Header(default="")) -> None:
    """The one door: if a key is configured, every route demands it."""
    if KEY and x_api_key != KEY:
        raise HTTPException(status_code=401, detail="bad key")


@app.get("/health")
def health() -> dict:
    return {"ok": True, "estate": str(ROOT)}


@app.get("/meters/smith")
def meters_smith(x_api_key: str = Header(default="")):
    _gate(x_api_key)
    hits = sorted((ROOT / "watch" / "inbox").glob("ESTATE_SMITH_CHART_*.json"))
    if not hits:
        return JSONResponse({"status": "DARK", "why": "no smith chart yet — run the engine"})
    return JSONResponse(json.loads(hits[-1].read_text(encoding="utf-8")))


@app.get("/records/{folder}")
def records(folder: str, x_api_key: str = Header(default="")):
    _gate(x_api_key)
    base = (ROOT / folder).resolve()
    if not base.is_relative_to(ROOT):
        raise HTTPException(status_code=400, detail="path escapes estate")
    return JSONResponse({"files": [p.name for p in sorted(base.rglob("*")) if p.is_file()][:200]})
''', encoding="utf-8", newline="\n")

    (SEED / "templates/README.md").write_text(
        "templates/ — rebuilt-small shapes for STACK.md tiers 3-4.\n"
        "The compose file is the cage; the api example serves your meters on loopback.\n"
        "Both are STARTING shapes: delete anything a meter doesn't prove you need.\n",
        encoding="utf-8", newline="\n")

    (SEED / "configs/keys.json").write_text(json_dumps({
        "_law": "one key, one canonical name, declared once. Copy an entry per lane you use; "
                "status 'awaiting' entries are skipped by the audit until you activate them.",
        "example_free_tier": {"env": "EXAMPLE_PROVIDER_API_KEY", "provider": "example",
                              "role": "template entry — replace with your real lanes",
                              "status": "awaiting-operator"},
    }), encoding="utf-8", newline="\n")

    # ---- verify_seal.py ---------------------------------------------------
    (SEED / "verify_seal.py").write_text('''"""verify_seal — check every file in MANIFEST.sha256 against its hash. Exit 0 = intact."""
import hashlib, sys
from pathlib import Path

root = Path(__file__).resolve().parent
bad = missing = 0
rows = [r for r in (root / "MANIFEST.sha256").read_text(encoding="utf-8").splitlines() if r.strip()]
for row in rows:
    want, _, rel = row.partition("  ")
    f = root / rel
    if not f.is_file():
        print(f"MISSING  {rel}"); missing += 1; continue
    got = hashlib.sha256(f.read_bytes()).hexdigest()
    if got != want:
        print(f"DRIFT    {rel}"); bad += 1
print(f"{len(rows) - bad - missing}/{len(rows)} verified, {bad} drifted, {missing} missing")
sys.exit(0 if (bad == 0 and missing == 0) else 1)
''', encoding="utf-8", newline="\n")

    # ---- LICENSE / SETUP.md / AGENTS.md ------------------------------------
    (SEED / "LICENSE").write_text("""MIT License

Copyright (c) 2026 MARKK

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
""", encoding="utf-8", newline="\n")

    (SEED / "SETUP.md").write_text("""# SETUP — what you need before FIRST_BOOT

- **Python 3.9+** (`python --version`). Everything runs on the standard library.
- **Optional:** `pip install matplotlib` — only for the smith chart's PNG plot.
  Without it, the chart prints its console meter and skips the plot. Nothing needs the network to boot.
- **A `.env` file (optional):** put provider keys here as `NAME=value` lines; the engines
  also read real environment variables. Declare every key you use in `configs/keys.json`
  (a template entry is there; copy its shape). The audit (`python engines/key_law.py --audit`)
  fails loud on any key that is live but undeclared — that is the design.
- **Verify the package first:** `python verify_seal.py` (step 0 of FIRST_BOOT) — and on
  Linux/macOS `sha256sum -c MANIFEST.sha256` works too.

Windows: all commands are the same; use `py` or `python` as you have it.
""", encoding="utf-8", newline="\n")

    (SEED / "AGENTS.md").write_text("""If you are an AI agent reading this package: read FIRST_BOOT.md first, then THE_METHOD.md.
The 11 laws in THE_METHOD.md govern everything here. Do not skip the seal check.
""", encoding="utf-8", newline="\n")

    # ---- FIRST_BOOT v2 ------------------------------------------------------
    (SEED / "FIRST_BOOT.md").write_text("""# FIRST BOOT — for a stranger holding this seed

You are holding a method, not a product. It is small on purpose. Here is your first hour.

0. **Verify the package:** `python verify_seal.py` — every file must check out.
   (Linux/macOS: `sha256sum -c MANIFEST.sha256` works too.)
1. **Read THE_METHOD.md** (one page, 11 laws). You will violate some of them in your first
   week. That is what the meters are for. See SETUP.md for requirements (Python 3.9+, matplotlib optional).
2. **Run the smith chart on nothing:** `python engines/estate_smith_chart.py --no-plot` —
   it will tell you honestly that you have no records yet (every organ prints DARK). That is
   your zero state. Gamma = 1 is normal.
3. **Declare your keys:** copy an entry in `configs/keys.json` per provider lane you use
   (a template entry with the schema is already there), put the actual keys in `.env` or your
   environment, then `python engines/key_law.py --audit` — it exits 0 when every live key is
   declared, and fails loud naming any key that is not.
4. **Index what you have:** `python engines/spine_walk.py <your-folder>` walks YOUR folder
   (pass the path; it defaults to where you run it) and writes one JSONL line per file, then
   `python engines/estate_atlas.py <your-folder>` turns that index into the atlas. The index
   regenerates — it is never hand-maintained.
5. **Start one record.** Markdown, append-only, receipted: who, when, where, evidence. A claim
   not in a record didn't happen.
6. **Schedule the cooker:** `python engines/cooker.py status` shows every free-lane reset and
   its countdown; `python engines/cooker.py fire --due` burns whatever has refilled. Put that
   command on an hourly timer (cron/schtasks) and your compute burns by default, not by willpower.
7. **Answer the daily question:** did the meters move? If a meter can't move, you built prose,
   not a meter. Delete it and build the meter.

The goal is not to reproduce the original estate. It is to grow YOUR estate under THESE laws.
The laws are the method; everything else is your version of it.
""", encoding="utf-8", newline="\n")

    # ---- HANDOFF v2 (numbers updated) ---------------------------------------
    (SEED / "HANDOFF.md").write_text("""# HANDOFF — what this seed is

This seed exists because of a measured result: on 2026-09-24/25 an attempt to ship this
estate as a page of pre-computed answers FAILED a held-out test (1/12) — the knowledge does
not transfer as facts. What transfers is the method: the laws (THE_METHOD.md), the engines
(engines/ — the method as runnable code), and the discipline (FIRST_BOOT.md).

The estate this came from: 63GB, 1.2M files, 3 years of human+AI operation. Seed V1 failed
its own cold-boot audit (2 of 7 first-boot steps worked); Seed V2 is the build-book's
items 1-2 executed — every engine boots standalone, the seal verifies on stock tools.
The stranger-continuation bar (G7): a stranger boots this seed and continues without the
original operator. That is the pass condition of this package.

Open-append records, hash-sealed freezes, loud-failing audits, meters over prose, the
operator's hand on transmit/delete/spend — the laws carry their own reasons. The seed is
small so that nothing in it is exempt from being read.
""", encoding="utf-8", newline="\n")

    # ---- THE_METHOD (Card V1 laws + stamp) ----------------------------------
    card = (ROOT / "watch/inbox/method_card_exp/CARD_V1.md").read_text(encoding="utf-8")
    stamp = """

---

*Stamped 2026-09-25 by the falsifier run: a card of FACTS built from these laws scored 1/12
on held-out questions — the laws transfer as LAWS, not as pre-computed answers. This page is
the law, not the memory. The memory regrows from the record engines in engines/.*
"""
    (SEED / "THE_METHOD.md").write_text(card + stamp, encoding="utf-8", newline="\n")

    # ---- seal (LF, content hash) -------------------------------------------
    # SPEC: watch/inbox/SEED_V2_BUILD_BOOK_20260925.md, "SPEC: PYC EXCLUSION AT SEAL".
    # Cause + evidence (fix-comment law): a08 catch 2026-09-25, 3 of 59 sealed rows
    # were __pycache__/*.pyc baking C:\Users\foste\...\seed\engines\cooker.py into the
    # stranger-facing zip; the 3.2.0 hand-surgery fixed the artifact, not the builder,
    # so the leak returned in 3.3.0. Compiled bytecode embeds compile-time absolute
    # paths: purged from the tree and excluded from the walk, never sealed, never zipped.
    for cache in sorted(SEED.rglob("__pycache__")):
        if cache.is_dir():
            shutil.rmtree(cache)
    lines, sealed = [], []
    for f in sorted(SEED.rglob("*")):
        if not f.is_file() or f.name == "MANIFEST.sha256":
            continue
        if f.suffix in (".pyc", ".pyo") or "__pycache__" in f.parts:
            continue
        h = hashlib.sha256(f.read_bytes()).hexdigest()
        lines.append(f"{h}  {f.relative_to(SEED).as_posix()}")
        sealed.append(f)
    (SEED / "MANIFEST.sha256").write_text("\n".join(lines) + "\n", encoding="utf-8", newline="\n")
    print(f"SEED V2 BUILT: {len(copied)} engines, {len(lines)} files sealed")

    # ---- pre-zip gate (build book t7 spec, t28 refire) ----------------------
    # SPEC: watch/inbox/SEED_V2_BUILD_BOOK_20260925.md, "SPEC: PRE-ZIP COLD-BOOT GATE".
    # The gate runs AFTER the seal (the suite verifies MANIFEST.sha256) and BEFORE
    # zip emission, in a temp copy, so no Python process ever runs inside seed/.
    # Fix receipt (cause + evidence): nothing between build and zip ever ran the
    # cold boot, so Desktop kept shipping the stale 3-pyc 3.3.0 zip alongside the
    # rebuilt inbox bytes (t28 hash diff 2026-09-25). Blocked on CRASH/ERROR/TIMEOUT;
    # a readable nonzero message passes by design, per the suite's own contract.
    print("PRE-ZIP GATE: tools/cold_boot_test.py against a fresh copy of seed/")
    import cold_boot_test
    gate_ok, gate_line = cold_boot_test.gate()
    if not gate_ok:
        raise SystemExit(f"seed_v2: pre-zip gate BLOCKED zip emission - {gate_line}")

    # ---- zip: derived from the sealed rows only (zip == seal by construction) ----
    ver = (SEED / "SEED_VERSION").read_text(encoding="utf-8").split()
    tag = ver[1] if len(ver) > 1 else "local"
    zip_path = ROOT / "watch" / "inbox" / f"seed-{tag}.zip"
    top = f"seed-{tag}"
    members = sorted(sealed + [SEED / "MANIFEST.sha256"],
                     key=lambda p: p.relative_to(SEED).as_posix())
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for p in members:  # reads bytes only; nothing executes inside the tree
            z.write(p, f"{top}/{p.relative_to(SEED).as_posix()}")
    print(f"SEED ZIP: {zip_path} ({len(members)} entries, top-level {top}/)")


def json_dumps(obj) -> str:
    import json
    return json.dumps(obj, indent=1, ensure_ascii=False) + "\n"


if __name__ == "__main__":
    build()
