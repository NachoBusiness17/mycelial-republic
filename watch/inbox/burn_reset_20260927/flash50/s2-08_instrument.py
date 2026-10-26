"""s2-08 instrument: one atomic context_pack build+format with a loss ledger.

Builds the pack in memory (mode=full default CLI shape), formats the text,
and reports per-layer truncation loss and dict-vs-text drops.
Writes nothing except what build_context_pack itself side-effects.
"""
from __future__ import annotations

import io
import json
from pathlib import Path

from config import ROOT
from mag.context_pack import MODE_CONFIG, build_context_pack, format_context_pack_text

R = []


def say(s: str) -> None:
    R.append(s)
    print(s)


pk = build_context_pack(mode="full")
text = format_context_pack_text(pk, mode="full")
cfg = MODE_CONFIG["full"]

say(f"instrument run: mode=full pack_ts={pk.get('ts')}")
say(f"pack dict json bytes (serialized, indent=2): {len(json.dumps(pk, indent=2, default=str))}")
say(f"rendered text chars: {len(text)} | budget max_chars={cfg['max_chars']}")
say("")

# --- layer truncation ledger: disk vs pack vs rendered ---
def disk_bytes(rel: str) -> int:
    p = ROOT / rel
    return p.stat().st_size if p.is_file() else -1


def rendered_chars(v) -> int:
    if not v:
        return 0
    i = text.find(str(v)[:60])
    return len(str(v)) if i >= 0 else 0


ledger = [
    ("memory/bonds_active.md", "bonds", "cap max_bonds=1600"),
    ("state/CURRENT.md (brief via latest.md FROZEN fallback)", "brief", "cap max_brief=1200"),
    ("memory/live_from_grok.md", "live_tail", "cap max_live=800"),
    ("memory/attention.md", "attention_tail", "clip 600 then [:400]"),
    ("memory/operator_directives.md", "directives", "clip 2800"),
    ("memory/working/OPERATOR_CONTINUITY.md", "continuity", "clip 2200"),
]
say("LAYER TRUNCATION LEDGER (disk bytes vs pack-dict chars vs chars present in rendered text):")
for rel, key, cap in ledger:
    d = disk_bytes(rel)
    v = pk.get(key, "")
    pv = len(str(v)) if v else 0
    rv = rendered_chars(v)
    say(f"  {rel}: disk={d}B pack={pv}ch rendered={rv}ch ({cap})")

todo = ROOT / "queue" / "todo.md"
td = todo.stat().st_size if todo.is_file() else -1
tn = len(pk.get("todo_open") or [])
say(f"  queue/todo.md: disk={td}B pack={tn} open items rendered={rendered_chars(chr(10).join(pk.get('todo_open') or []))}ch (clip 500 -> first 12 '- [ ]')")

obj = ROOT / "memory" / "boot" / "CURRENT_OBJECTIVE.md"
od = obj.stat().st_size if obj.is_file() else -1
oi = text.find("### L0b Current objective")
oj = text.find("### L0b Compiled laws")
orv = (oj - oi) if oi >= 0 and oj > oi else 0
say(f"  memory/boot/CURRENT_OBJECTIVE.md: disk={od}B rendered={orv}ch (no cap: full text)")
say("")

# --- per-key render accounting ---
say("DICT KEYS: never rendered by format_context_pack_text (any mode):")
never = ["compass_framework", "checkpoint_restore", "resonance_cards",
         "token_note", "layers", "commands", "for", "schema"]
present = [k for k in never if k in pk]
say(f"  {present}")
say("DICT KEYS rendered only conditionally (mode/flag gated):")
say("  directives: plan+full only; live_tail+attention_tail: heat (plan+full, dropped FIRST on overflow);")
say("  agent_state+continuity: not janitor/route; doctrine/proven_moves/solved: plan+full+build+audit;")
say("  subchain_full+world_state: MAG_FULL_CONTEXT=1 and mode=full only")
say("")

# --- heat clip evidence ---
say("HEAT/SHED accounting for THIS run:")
say(f"  bonds_meta={json.dumps(pk.get('bonds_meta'), default=str)[:200]}")
say(f"  open_loops n={len(pk.get('open_loops') or [])} todo_open n={tn}")
say(f"  trail active={ (pk.get('run_trail') or {}).get('active') } proven_moves n={(pk.get('proven_moves') or '').count(chr(10))+1 if pk.get('proven_moves') else 0}")
say(f"  skills_excerpt chars={len(pk.get('skills_excerpt') or '')} ijl={len(pk.get('ijl_skills') or '')}")
say(f"  coordination chars={len(pk.get('coordination_excerpt') or '')} behavioral={len(pk.get('behavioral_excerpt') or '')}")
say(f"  resonance_l0e chars={len(pk.get('resonance_l0e') or '')} zeitgeist={len(pk.get('zeitgeist_excerpt') or '')}")
say(f"  doctrine lines={(pk.get('doctrine') or '').count(chr(10))+1 if pk.get('doctrine') else 0} quantized_laws chars={len(pk.get('quantized_laws') or '')}")
say(f"  nervous keys={sorted((pk.get('nervous_system') or {}).keys())}")
say(f"  tip={json.dumps(pk.get('tip'), default=str)[:220]}")
say(f"  dirac={pk.get('dirac_loops')} health={pk.get('health')} models={json.dumps(pk.get('models'), default=str)[:160]}")
say(f"  agent_state first 80: {(pk.get('agent_state') or '')[:80]!r}")
say(f"  mirror_voice/clue_chain (env-gated): {len(pk.get('mirror_voice_excerpt') or '')}/{len(pk.get('clue_chain_excerpt') or '')} chars")
say(f"  build_excerpt/scope_excerpt (build-mode only keys): {len(pk.get('build_excerpt') or '')}/{len(pk.get('scope_excerpt') or '')} chars")

# what the rendered text actually retained
sections = [ln for ln in text.splitlines() if ln.startswith("## ") or ln.startswith("### ")]
say("")
say("RENDERED SECTION HEADERS in this run's text:")
for s in sections:
    say(f"  {s}")

Path("watch/inbox/burn_reset_20260927/flash50/s2-08_instrument_out.txt").write_text(
    "\n".join(R) + "\n", encoding="utf-8")
