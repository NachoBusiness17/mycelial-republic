"""COLD-1 helper: arm sizes + liveness of divergence-class cold carriers. Throwaway."""
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[3]
hot = ['scripts/descent_driver.sh', 'watch/inbox/SHARED_SURFACE_CONTRACT.json',
       'mag/switchboard_v2.py', 'tools/hermes_burn.py', 'mag/steer_seal.py',
       'tools/ocean_v2_pilot.py', 'tools/roblox_npc_gateway.py', 'tools/reverse_map.py',
       'mag/preload_selector.py', 'mag/desk_model_probe.py']
cand = ['mag/orchestrator.py', 'mag/training_events.py', 'mag/verkle_knot.py',
        'mag/operator_inbox.py', 'mag/skill_ledger.py', 'mag/preferences.py',
        'mag/chain_query.py', 'mag/registry.py', 'mag/policy_engine.py',
        'mag/switchboard.py', 'mag/verkle_bus.py', 'mag/health.py']
tot_h = tot_c = 0
for f in hot + cand:
    p = ROOT / f
    if p.is_file():
        t = p.read_text(encoding='utf-8', errors='replace')
        tag = 'HOT ' if f in hot else 'cand'
        print(f'{tag} {len(t.splitlines()):5d} {len(t):7d} {f}')
        if f in hot:
            tot_h += len(t)
        else:
            tot_c += len(t)
print('HOT total chars', tot_h, ' cand total chars', tot_c)

files = (list((ROOT / 'mag').glob('*.py')) + list((ROOT / 'tools').glob('*.py'))
         + list((ROOT / 'scripts').glob('*.py')) + list((ROOT / 'tests').glob('*.py'))
         + [ROOT / 'main.py'])
srcs = {p.as_posix(): p.read_text(encoding='utf-8', errors='replace') for p in files}
for mod in ('mag.switchboard', 'mag.policy_engine'):
    modfile = mod.replace('.', '/') + '.py'
    hits = [f for f, s in srcs.items() if mod in s and f != modfile]
    print(f'importers of {mod}:', len(hits), hits[:8])
