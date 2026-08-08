"""Run the Quiet Forge campaign with UTF-8-safe output."""
import sys, os, io

# Force UTF-8 on stdout/stderr before anything else prints
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from mag.campaign import load_module, run_campaign

module_path = ROOT / "campaigns" / "quiet_forge" / "module.json"
module = load_module(module_path)

print("Module loaded:", module.get("title"))
print("Party:", {k: v.get("model") for k, v in module.get("party_roster", {}).items()})
print("DM:", module.get("dm", {}).get("model"), "/", module.get("dm", {}).get("provider"))
print("Rooms:", list(module.get("rooms", {}).keys()))
print()

state = run_campaign(
    module,
    dm_model="deepseek-v4-flash",
    dm_provider="deepseek",
    dry=False,
)

print("\n=== FINAL STATE ===")
print(f"Session: {state.session_id}")
print(f"Rooms cleared: {state.rooms_cleared}")
print(f"Steers deployed: {state.steers_deployed}")
print(f"Steers detected: {state.steers_detected}")
print(f"Steers resisted: {state.steers_resisted}")
print(f"Measurements: {len(state.measurements)}")

# Save state summary
summary_path = ROOT / "memory" / "runs" / "campaign" / f"{state.session_id}_summary.json"
import json
summary = {
    "session_id": state.session_id,
    "module_id": state.module_id,
    "rooms_cleared": state.rooms_cleared,
    "steers_deployed": state.steers_deployed,
    "steers_detected": state.steers_detected,
    "steers_resisted": state.steers_resisted,
    "measurements": state.measurements,
    "party_actions": getattr(state, 'party_actions', []),
}
summary_path.parent.mkdir(parents=True, exist_ok=True)
summary_path.write_text(json.dumps(summary, indent=2, default=str), encoding="utf-8")
print(f"\nSummary saved: {summary_path}")
