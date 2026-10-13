import sys
from pathlib import Path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from dashboard import rest
import json

pipe_id = 'paf73656cb2'

print('LIST PIPES:')
code, out = rest.h_agents_pipes({}, None)
print(code, json.dumps(out, indent=2, default=str))

print('\nPIPE ONE:')
code, out = rest.h_agents_pipe_one({'id': pipe_id}, None)
print(code, json.dumps(out, indent=2, default=str))

print('\nCOLLECT PIPE (wait 1s, tail 20):')
code, out = rest.h_agents_pipe_collect({'id': pipe_id}, {'wait':1, 'tail':20})
print(code, json.dumps(out, indent=2, default=str))

print('\nBROADCAST STEER:')
code, out = rest.h_agents_pipe_cmd({'id': pipe_id}, {'cmd':'steer', 'context':'Focus on concise summary'})
print(code, json.dumps(out, indent=2, default=str))
