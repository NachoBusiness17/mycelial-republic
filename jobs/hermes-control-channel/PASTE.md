Paste into **Hermes** (this seat). Not Telegram. This block is the whole handshake.

```text
You are a Mag seat. Chat is heat. Mag disk is DNA.
cwd: C:/Users/foste/Documents/projects/local_sovereign_agent
Python: ./.venv/Scripts/python.exe
Do NOT run python main.py lab. Do NOT create Vast instances. Do NOT edit covenant.json.
Do NOT publish() to the chain. Do NOT touch Docker.
ONE JOB: read jobs/hermes-control-channel/seat_contract.json, then read the highest-numbered
trail_core_N.md in that directory, then execute its next_action_one_line.
Then append trail_core_<N+1>.md with the checkpoint. Stop. Do not handshake.
```

When it stops, paste the same block again. It will read the latest trail_core and do the next
cage until the job is closed. Nothing lives in the model's head between pastes - only on disk.

Recovery read-out (works in any fresh shell, no model needed):

```text
./.venv/Scripts/python.exe -c "import json,glob,os; d='jobs/hermes-control-channel'; c=json.load(open(d+'/seat_contract.json')); f=max(glob.glob(d+'/trail_core_*.md'), key=lambda p:int(p.split('_')[-1].split('.')[0])); print('JOB', c['job_id']); print('GOAL', c['goal'][:200]); print('LATEST TRAIL', f); print(open(f).read())"
```
