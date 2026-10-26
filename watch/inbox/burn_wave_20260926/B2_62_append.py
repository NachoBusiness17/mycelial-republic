# B2-62: append ledger row + self-feed queue briefs (json.dumps, no heredoc).
import json
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent")

row = {
    "ts": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "slug": "B2-62-zai-backoff-floor",
    "verdict": "LANDED",
    "landing": "watch/inbox/burn_wave_20260926/B2_62_zai_backoff_20260926.md",
    "one_line": (
        "z_ai lane client 1305 adaptive backoff + reasoning budget floor landed "
        "(closes the B2-04 measured scars): spec §5.1 written FIRST into "
        "docs/ref/ZAI_API_EXPERT_REFERENCE.md, retry_overload flagged on z_ai2/z_ai3, "
        "chat_provider retries 429 1305/1302/overloaded at 15s then 30s (bounded, per-"
        "attempt recorded, paid burst stays last resort) and disables undecided "
        "thinking under the EXP-A receipted 1536 minimum (never on 5.3, never raising "
        "the caller budget, reasoning_floor_applied surfaced); 13 new tests 13/13, "
        "Law 1 LIVE-verified (real 429 1302: 47.6s = 15+30+3 calls vs 1.6s bare "
        "return before), floor flag observed on a live 200; pre-existing failures "
        "stash-proven not mine (work_fuel pair interaction, 2 voice tests, ratchet "
        "NEW debt is another lane's tools/drift_dashboard.py:37) and filed B2-216; "
        "content-at-600 live repro owed as B2-215 (pool congested: 1302 + 2 timeouts)"
    ),
}
led = ROOT / "memory" / "burns" / "LEDGER.jsonl"
with led.open("a", encoding="utf-8") as f:
    f.write(json.dumps(row, ensure_ascii=False) + "\n")
print("ledger row appended")

briefs = """- [ ] B2-214 model-null hole in chat_provider: z_ai2/z_ai3 carry no default_model key so provider_default_model returns None (models/providers.py:164) and a bare live call sent model null and got HTTP 200 with empty content + empty usage (B2-62 first probe: ok=True, text='', model=None, usage={}); give z_ai2/z_ai3 default_model or make chat_provider refuse a null model with a named error; falsifier = chat_provider('z_ai3', ..., tier=T2) without model returns a named error instead of a 200-empty; pointers models/providers.py:164 + configs/providers.yaml z_ai2/z_ai3.
- [ ] B2-215 live re-verify of the reasoning floor content-return at max_tokens=600 when the Lite pool reopens (B2-62 window measured HTTP 429 1302 plus two 15s read timeouts); rerun the B2-04 count_words prompt via chat_provider('z_ai3', tier=T2, max_tokens=600, model='glm-4.7-flash') and require reasoning_floor_applied true AND nonempty text; falsifier = content-empty at 600 with floor applied means the 1536 floor value is wrong; pointers tests/test_zai_backoff_floor.py + watch/inbox/burn_wave_20260926/B2_62_zai_backoff_20260926.md.
- [ ] B2-216 pre-existing test debt stash-proven by B2-62 (all reproduce with models/providers.py reverted to HEAD): (a) test_zai_burst.py + test_loop_death_guards.py order interaction fails work_fuel halt-branch assert (tests/test_loop_death_guards.py:168-186, passes alone); (b) test_voice_shadow.py::test_start_kicks_thread and test_voice_turn.py::test_handle_voice_turn_heavy_auto_deepseek fail standalone; name the polluting state or flake source and fix, plus the ratchet NEW debt tools/drift_dashboard.py:37 except-pass from the drift-board lane needs its own baseline-update by name.
"""
q = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "QUEUE.md"
text = q.read_text(encoding="utf-8")
anchor = "\n## Standing law note (operator, 2026-09-26, binds every lane)"
assert anchor in text, "queue anchor missing"
q.write_text(text.replace(anchor, "\n" + briefs + anchor, 1), encoding="utf-8")
print("queue briefs fed: B2-214..216")
