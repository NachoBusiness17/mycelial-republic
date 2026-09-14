"""Run Quiet Forge campaign and capture ALL party model outputs + artifact."""
import sys, os, io, json, time
from pathlib import Path

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

# Monkey-patch party_member_turn to capture full outputs
import mag.campaign as camp
_original_party_turn = camp.party_member_turn

captured_actions = []

def _capturing_turn(member_name, member_info, narration, room, state):
    result = _original_party_turn(member_name, member_info, narration, room, state)
    captured_actions.append({
        "member": member_name,
        "role": member_info.get("mag_role", "?"),
        "model": member_info.get("model", "?"),
        "tier": member_info.get("tier", "?"),
        "ok": result.get("ok"),
        "action": result.get("action", ""),
        "error": result.get("error", ""),
        "latency_ms": result.get("latency_ms", 0),
        "tokens": result.get("tokens", 0),
    })
    return result

camp.party_member_turn = _capturing_turn

# Also capture DM narration
_original_dm_narrate = camp.dm_narrate
captured_narrations = []

def _capturing_narrate(module, state, **kwargs):
    result = _original_dm_narrate(module, state, **kwargs)
    captured_narrations.append({
        "room": state.current_room,
        "turn": state.turn,
        "ok": result.get("ok"),
        "narration": result.get("narration", ""),
        "model": result.get("model", "?"),
    })
    return result

camp.dm_narrate = _capturing_narrate

# Run
from mag.campaign import load_module, run_campaign

module_path = ROOT / "campaigns" / "quiet_forge" / "module.json"
module = load_module(module_path)

print("Module:", module.get("title"))
print()

state = run_campaign(
    module,
    dm_model="deepseek-v4-flash",
    dm_provider="deepseek",
    dry=False,
)

# Save full capture
capture = {
    "session_id": state.session_id,
    "module_id": state.module_id,
    "dm_model": state.dm_model,
    "dry": state.dry,
    "started_at": state.started_at,
    "rooms_cleared": state.rooms_cleared,
    "steers_deployed": state.steers_deployed,
    "steers_detected": state.steers_detected,
    "steers_resisted": state.steers_resisted,
    "measurements": state.measurements,
    "dm_narrations": captured_narrations,
    "party_actions": captured_actions,
}

out_dir = ROOT / "memory" / "runs" / "campaign"
out_dir.mkdir(parents=True, exist_ok=True)
capture_path = out_dir / f"{state.session_id}_full.json"
capture_path.write_text(json.dumps(capture, indent=2, default=str, ensure_ascii=False), encoding="utf-8")
print(f"\nFull capture saved: {capture_path}")

# Print party actions for analysis
print("\n=== PARTY ACTIONS ===")
for a in captured_actions:
    print(f"\n--- {a['member']} ({a['role']}, {a['model']}, tier={a['tier']}) ---")
    print(f"  OK: {a['ok']}  Latency: {a['latency_ms']}ms  Tokens: {a['tokens']}")
    print(f"  Action: {a['action'][:500]}")
