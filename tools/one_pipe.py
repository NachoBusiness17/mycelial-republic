import sys, json
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from dashboard import rest

pipe_id = 'paf73656cb2'
code, out = rest.h_agents_pipe_one({'id': pipe_id}, None)
print('CODE', code)
print(json.dumps(out, indent=2, default=str))

code2, out2 = rest.h_agents_pipe_collect({'id': pipe_id}, {'wait':1, 'tail':10})
print('\nCOLLECT CODE', code2)
print(json.dumps(out2, indent=2, default=str))
