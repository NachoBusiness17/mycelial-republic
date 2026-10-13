"""VISION ENDOWMENT — the skill-quantization falsifier (2026-09-04).

Steal spec: watch/STEAL_MCP_SKILL_QUANTIZATION_20260904.md — "the MCP server is the
skill, quantized out of the weights." This rig measures it: does a dumb local 7B
+ an MCP-shaped eye-tool (see(): STRUCTURE, never pixels) match native vision
(deepseek-v4-flash-vision-exp) on the same 5-task UI set?

Arms (same task set, same environment prep):
  A. BLIND   qwen2.5:7b, no eye, task text only (honest-failure baseline).
  B. ENDOWED qwen2.5:7b + ONE tool: see(target) -> ui = AX element tree
             (uiautomator dump, id/text/bounds/clickable — the AX law),
             image = mag.vision.describe(screenshot) (the deepseek eye as a tool).
             The model NEVER sees pixels in arm B... unless it picks target=image,
             which routes pixels through the eye tool and back as text — the
             endowment is the tool boundary, whichever transducer it picks.
  C. NATIVE  mag.vision.describe(screenshot, task) directly (pixels in the model).

Environment: emulator-5554, pocketfleet WebView on
http://10.0.2.2:8765/static/daytool.html (digest badge + LATTICE CONSOLE).
$0 budget: local ollama (CPU) + free deepseek vision lane. No secrets echoed.

Run: python scripts/vision_endowment.py [--model qwen2.5:7b] [--arms A,B,C]
Receipt: watch/VISION_ENDOWMENT_RECEIPT_20260904.md (written by hand from the
results JSON this script emits to memory/runs/vision_endowment/).
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

OUT = ROOT / "memory" / "runs" / "vision_endowment"
OLLAMA = "http://127.0.0.1:11434/api/chat"
ADB = shutil.which("adb") or "adb"
RUN_TS = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

TASKS = [
    ("t1_badge", "Report the state of the day-work digest badge "
                 "(the small status pill next to the heading '1 · DAY-WORK DIGEST')."),
    ("t2_buttons", "Find the section titled '2 · LATTICE CONSOLE' and name its buttons."),
    ("t3_coords", "Determine the screen coordinates of the center of the button "
                  "labeled 'invariants'. The screen is 1080x2400. Answer as (x, y)."),
    ("t4_walkpos", "The 'STEP ×1' button was just tapped once. "
                   "Report the walk position now (format: pos X/Y)."),
    ("t5_lattice", "Name the currently loaded lattice: its kind and its entry count."),
]

SEE_TOOL = [{
    "type": "function",
    "function": {
        "name": "see",
        "description": "Observe the phone screen. target 'ui' returns the accessibility "
                       "element tree (text/class/bounds/clickable per element); "
                       "target 'image' returns a visual description of the screenshot.",
        "parameters": {"type": "object",
                       "properties": {"target": {"type": "string", "enum": ["ui", "image"]}},
                       "required": ["target"]},
    },
}]

SYS_ENDOWED = (
    "You control an Android phone (1080x2400 screen) showing a web app called DAY TOOL. "
    "You have ONE tool: see(target). target='ui' returns the element tree with exact "
    "bounds [l,t][r,b] — compute a button's center as ((l+r)/2, (t+b)/2). target='image' "
    "returns a visual description. Observe before you answer; never guess what you can "
    "observe. When you have the answer, reply with plain text only (1-2 sentences, no JSON)."
)
SYS_BLIND = (
    "You control an Android phone (1080x2400 screen) showing a web app called DAY TOOL "
    "(sections: day-work digest, lattice console, day lanes). Answer the task. If you "
    "genuinely cannot know something from text alone, say exactly what you cannot know "
    "instead of inventing it. Reply with plain text only (1-2 sentences)."
)

# ---------------------------------------------------------------- adb plumbing


def adb(*args: str, timeout: int = 60, binary_to: Path | None = None) -> str:
    """List-args subprocess only (mimosa-safe: no shell, no string commands)."""
    if binary_to is not None:
        with open(binary_to, "wb") as fp:
            subprocess.run([ADB, *args], stdout=fp, timeout=timeout, check=True)
        return ""
    r = subprocess.run([ADB, *args], capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"adb {args[:2]} failed: {r.stderr.strip()[:200]}")
    return r.stdout


def dump_tree() -> list[dict]:
    """uiautomator dump -> compact node list (the AX channel)."""
    adb("shell", "uiautomator", "dump", "/sdcard/ui_endow.xml")
    local = OUT / "ui_last.xml"
    adb("pull", "/sdcard/ui_endow.xml", str(local))
    root = ET.parse(local).getroot()
    nodes = []
    for n in root.iter("node"):
        txt = (n.get("text") or "").strip()
        desc = (n.get("content-desc") or "").strip()
        cls = (n.get("class") or "").split(".")[-1]
        clickable = (n.get("clickable") or "") == "true"
        bounds = n.get("bounds") or ""
        m = re.match(r"\[(-?\d+),(-?\d+)\]\[(-?\d+),(-?\d+)\]", bounds)
        if not (txt or desc or clickable):
            continue
        node = {"cls": cls, "text": txt, "desc": desc, "clickable": clickable,
                "bounds": bounds}
        if m:
            l, t, r, b = map(int, m.groups())
            node["rect"] = [l, t, r, b]
            node["center"] = [(l + r) // 2, (t + b) // 2]
        nodes.append(node)
    return nodes


def tree_text(nodes: list[dict]) -> str:
    lines = [f"screen 1080x2400, {len(nodes)} elements (class | text | bounds | center | clickable)"]
    for n in nodes:
        c = f" center=({n['center'][0]},{n['center'][1]})" if "center" in n else ""
        clk = " clickable" if n["clickable"] else ""
        d = f" desc='{n['desc']}'" if n["desc"] else ""
        lines.append(f"{n['cls']} | '{n['text'][:70]}' | {n['bounds']}{c}{clk}{d}")
    return "\n".join(lines[:140])


def screenshot() -> Path:
    p = OUT / f"screen_{RUN_TS}_{int(time.time() * 1000) % 100000}.png"
    adb("exec-out", "screencap", "-p", binary_to=p)
    return p


def tap(x: int, y: int) -> None:
    adb("shell", "input", "tap", str(x), str(y))


def find(nodes: list[dict], needle: str) -> dict | None:
    for n in nodes:
        if needle.lower() in n["text"].lower():
            return n
    return None


def find_button(nodes: list[dict], needle: str) -> dict | None:
    """Exact-channel finder: Buttons only (a text like 'ONE step per press' is not a button)."""
    for n in nodes:
        if n["cls"] == "Button" and needle.lower() in n["text"].lower():
            return n
    return None

# ------------------------------------------------------------ ground truth


def ground_truth(nodes: list[dict]) -> dict:
    """Extract the answer key from the live tree (harness channel, per task)."""
    gt: dict = {}
    for n in nodes:
        m = re.search(r"DAY-WORK DIGEST\s+(\S+)", n["text"])
        if m and "badge" not in gt:
            gt["badge"] = m.group(1)
        if n["text"].startswith("pos "):
            gt["walkpos"] = n["text"]
        if "entries" in n["text"] and "invariants.json" in n["text"]:
            gt["latsummary"] = n["text"]
    inv = find_button(nodes, "invariants")
    if inv and "rect" in inv:
        gt["invariants_rect"] = inv["rect"]
        gt["invariants_center"] = inv["center"]
    # LATTICE CONSOLE buttons = clickable buttons between the section header and DAY LANES
    try:
        start = next(i for i, n in enumerate(nodes) if "LATTICE CONSOLE" in n["text"])
        gt["buttons"] = [n["text"] for n in nodes[start:]
                         if n["clickable"] and n["cls"] == "Button"][:6]
    except StopIteration:
        gt["buttons"] = []
    m = re.search(r"pos (\d+)/(\d+)", gt.get("walkpos", ""))
    if m:
        gt["walk"] = [int(m.group(1)), int(m.group(2))]
    km = re.search(r"(generic entries|invariant registry|law registry \(|rule lattice|numeric grid)",
                   gt.get("latsummary", ""))
    cm = re.search(r"(\d+) entries", gt.get("latsummary", ""))
    if km:
        gt["kind"] = km.group(1)
    if cm:
        gt["count"] = int(cm.group(1))
    return gt

# ------------------------------------------------------------------- ollama


def ollama_chat(model: str, messages: list[dict], tools: list | None = None,
                num_predict: int = 256) -> dict:
    payload = {"model": model, "messages": messages, "stream": False,
               "options": {"temperature": 0, "num_ctx": 8192, "num_predict": num_predict}}
    if tools:
        payload["tools"] = tools
    t0 = time.time()
    req = urllib.request.Request(OLLAMA, data=json.dumps(payload).encode(),
                                 headers={"Content-Type": "application/json"})
    r = json.loads(urllib.request.urlopen(req, timeout=600).read())
    r["_wall"] = time.time() - t0
    return r


def parse_tool_call(msg: dict) -> dict | None:
    """Native tool_calls first; then the hermes-JSON-in-content fallback."""
    for tc in msg.get("tool_calls") or []:
        fn = tc.get("function") or {}
        if fn.get("name") == "see":
            args = fn.get("arguments") or {}
            tgt = args.get("target", "ui") if isinstance(args, dict) else "ui"
            return {"target": str(tgt)}
    c = msg.get("content") or ""
    m = re.search(r"\{[^{}]*\"(?:name|tool)\"\s*:\s*\"see\"[^{}]*\}", c)
    if m:
        try:
            j = json.loads(m.group(0))
            args = j.get("arguments") or j.get("input") or j.get("parameters") or {}
            tgt = args.get("target", "ui") if isinstance(args, dict) else str(args)
            return {"target": str(tgt)}
        except Exception:  # noqa: BLE001
            return None
    return None

# -------------------------------------------------------------------- arms


def run_blind(model: str, task: str) -> dict:
    msgs = [{"role": "system", "content": SYS_BLIND}, {"role": "user", "content": task}]
    r = ollama_chat(model, msgs)
    return {"answer": (r.get("message") or {}).get("content", "").strip(),
            "steps": 0, "see_targets": [],
            "prompt_tok": r.get("prompt_eval_count") or 0,
            "eval_tok": r.get("eval_count") or 0, "wall": r["_wall"]}


def run_endowed(model: str, task: str) -> dict:
    from mag import vision  # local import: the eye is a tool call away, not ambient
    msgs = [{"role": "system", "content": SYS_ENDOWED}, {"role": "user", "content": task}]
    steps, targets = 0, []
    ptok, etok, wall = 0, 0, 0.0
    for _ in range(4):  # <=4 see() calls per task
        r = ollama_chat(model, msgs, tools=SEE_TOOL)
        ptok += r.get("prompt_eval_count") or 0
        etok += r.get("eval_count") or 0
        wall += r["_wall"]
        msg = r.get("message") or {}
        call = parse_tool_call(msg)
        if not call:
            return {"answer": (msg.get("content") or "").strip(), "steps": steps,
                    "see_targets": targets, "prompt_tok": ptok, "eval_tok": etok,
                    "wall": wall}
        steps += 1
        tgt = call["target"] if call["target"] in ("ui", "image") else "ui"
        targets.append(tgt)
        if tgt == "ui":
            obs = tree_text(dump_tree())
        else:
            shot = screenshot()
            v = vision.describe(str(shot), "Describe this phone screen precisely for an "
                                "agent: section headings, badge states, button labels, "
                                "any position counters (e.g. pos X/Y), lattice kind/count.",
                                max_tokens=600)
            obs = v.get("text") or f"see(image) failed: {v.get('error', '')[:120]}"
            ptok += v.get("prompt_tokens") or 0
            etok += v.get("completion_tokens") or 0
        asst: dict = {"role": "assistant", "content": msg.get("content") or ""}
        if msg.get("tool_calls"):
            asst["tool_calls"] = msg["tool_calls"]
        msgs.append(asst)
        msgs.append({"role": "tool",
                     "content": f"see('{tgt}') ->\n{obs[:6000]}"})
    return {"answer": "[gave up: tool-loop budget exhausted]", "steps": steps,
            "see_targets": targets, "prompt_tok": ptok, "eval_tok": etok, "wall": wall}


def run_native(task: str) -> dict:
    from mag import vision
    shot = screenshot()
    t0 = time.time()
    v = vision.describe(str(shot),
                        "You are looking at a screenshot of a phone app (DAY TOOL). "
                        "Task: " + task + " Answer precisely; for coordinates give your "
                        "best (x, y) estimate.", max_tokens=1200)
    return {"answer": v.get("text") or f"ERROR: {v.get('error', '')[:200]}",
            "steps": 0, "see_targets": ["image"],
            "prompt_tok": v.get("prompt_tokens") or 0,
            "eval_tok": v.get("completion_tokens") or 0,
            "wall": time.time() - t0, "shot": str(shot)}

# ------------------------------------------------------------------ grading


def grade(task_id: str, answer: str, gt: dict) -> tuple[bool, str]:
    a = (answer or "").lower()
    if task_id == "t1_badge":
        return gt.get("badge", "?").lower() in a, f"gt badge={gt.get('badge')!r}"
    if task_id == "t2_buttons":
        need = ["invariants", "law registry", "steer field"]
        ok = all(n in a for n in need)
        return ok, f"gt buttons={gt.get('buttons')}"
    if task_id == "t3_coords":
        m = re.search(r"\(?\s*(\d{2,4})\s*[,;]\s*(\d{2,4})\s*\)?", a)
        if not m:
            return False, "no coordinate pair in answer"
        x, y = int(m.group(1)), int(m.group(2))
        r_ = gt.get("invariants_rect")
        if not r_:
            return False, "gt missing (button not found in tree)"
        inside = r_[0] <= x <= r_[2] and r_[1] <= y <= r_[3]
        c = gt.get("invariants_center", [0, 0])
        dist = abs(x - c[0]) + abs(y - c[1])
        return inside, f"answer=({x},{y}) gt_rect={r_} gt_center={c} manhattan_dist={dist}"
    if task_id == "t4_walkpos":
        ok = bool(re.search(r"1\s*/\s*47|1\s+of\s+47", a))
        return ok, f"gt walkpos={gt.get('walkpos')!r}"
    if task_id == "t5_lattice":
        kind_ok = "generic entries" in a or ("generic" in a and "entries" in a)
        count_ok = bool(re.search(r"\b47\b", a))
        return kind_ok and count_ok, f"gt kind={gt.get('kind')!r} count={gt.get('count')}"
    return False, "unknown task"

# ------------------------------------------------------------------- harness


def prep(reset_to_zero: bool = True) -> list[dict]:
    """Deterministic environment: invariants lattice loaded, walk pos 0/47.
    Robust to the shared rig: another driver may leave the WebView on lanes.html —
    the 'DAY TOOL' button there leads back."""
    nodes = dump_tree()
    if not find(nodes, "LATTICE CONSOLE"):
        back = find_button(nodes, "DAY TOOL")
        if back and "center" in back:  # we are on lanes.html -> go home
            tap(*back["center"])
            time.sleep(3.5)
        else:
            adb("shell", "am", "start", "-n", "com.sovereign.pocketfleet/.MainActivity")
            time.sleep(4)
        nodes = dump_tree()
    if not find(nodes, "invariants.json"):
        inv = find_button(nodes, "invariants")
        if inv and "center" in inv:
            tap(*inv["center"])
            time.sleep(1.5)
        nodes = dump_tree()
    if reset_to_zero:
        rst = find_button(nodes, "RESET")
        if rst and "center" in rst:
            tap(*rst["center"])
            time.sleep(0.8)
            nodes = dump_tree()
    return nodes


def main() -> int:
    ap = argparse.ArgumentParser(description="vision endowment 3-arm falsifier")
    ap.add_argument("--model", default="qwen2.5:7b")
    ap.add_argument("--arms", default="A,B,C")
    ap.add_argument("--out", default="")
    a = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    out_path = Path(a.out) if a.out else OUT / f"results_{RUN_TS}.json"
    results = {"ts": RUN_TS, "model": a.model, "arms": a.arms.split(","),
               "ollama": "127.0.0.1:11434 (CPU)", "tasks": [], "note":
               "$0 budget: arms A/B local ollama; arm C free deepseek vision lane"}

    for arm in a.arms.split(","):
        prep()
        gt_check = ground_truth(dump_tree())
        if not gt_check.get("badge") or not gt_check.get("walkpos"):
            raise SystemExit("ENVIRONMENT_DRIFT: daytool state not present after prep "
                             f"(badge={gt_check.get('badge')!r}, walkpos={gt_check.get('walkpos')!r}) "
                             "- the shared rig moved; re-run prep and retry")
        for task_id, task_text in TASKS:
            nodes = dump_tree()
            gt = ground_truth(nodes)
            if task_id == "t4_walkpos":  # the STEP x1 tap happens at question time
                st = find_button(nodes, "STEP")
                if st and "center" in st:
                    tap(*st["center"])
                    time.sleep(0.8)
                    nodes = dump_tree()
                    gt = ground_truth(nodes)
            row = {"arm": arm, "task": task_id, "gt": {k: gt.get(k) for k in
                   ("badge", "buttons", "invariants_rect", "invariants_center",
                    "walkpos", "kind", "count")}}
            if arm == "A":
                res = run_blind(a.model, task_text)
            elif arm == "B":
                res = run_endowed(a.model, task_text)
            elif arm == "C":
                res = run_native(task_text)
            else:
                raise SystemExit(f"unknown arm {arm}")
            ok, why = grade(task_id, res["answer"], gt)
            row.update(res)
            row["correct"] = ok
            row["grade_note"] = why
            results["tasks"].append(row)
            print(f"[{arm}] {task_id}: {'PASS' if ok else 'FAIL'} "
                  f"({res['wall']:.1f}s, {res['steps']} steps) {res['answer'][:90]!r}",
                  flush=True)
            if task_id == "t4_walkpos":
                prep()  # reset walk for the next task/arm
        # score per arm
    for arm in a.arms.split(","):
        rows = [r for r in results["tasks"] if r["arm"] == arm]
        score = sum(1 for r in rows if r["correct"])
        ptok = sum(r["prompt_tok"] for r in rows)
        etok = sum(r["eval_tok"] for r in rows)
        wall = sum(r["wall"] for r in rows)
        results.setdefault("scores", {})[arm] = {
            "score": f"{score}/5", "prompt_tok": ptok, "eval_tok": etok,
            "total_tok": ptok + etok, "wall_s": round(wall, 1), "cost_usd": 0.0}
        print(f"== ARM {arm}: {score}/5  tok={ptok + etok}  wall={wall:.0f}s")

    out_path.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"results -> {out_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
