"""e06-fidelity-audit lane join script: run dwfrun-3484c5eb-7c7b-4601-979e-951c004687cf.

Join steps.jsonl (session_id minus 'sess_' prefix) to memory/worldline/<actor>/SEED.json
slabs; diff intended-vs-executed per actor; print the per-actor verdict table.
One run, deep. Reads only; writes nothing.
"""
import json, re, hashlib, os, collections, datetime

ROOT = r"C:/Users/foste/Documents/projects/local_sovereign_agent"
RUN = "3484c5eb-7c7b-4601-979e-951c004687cf"
STREAM = os.path.join(ROOT, "memory", "trajectory", "steps.jsonl")
WL = os.path.join(ROOT, "memory", "worldline")
DEAD_TAPE = os.path.join(ROOT, "memory", "runs", "trajectory", "steps.jsonl")
LIVE_AGENTS_MD = os.path.join(ROOT, "AGENTS.md")
PROJ_AGENTS_MD = "C:/Users/foste/Documents/projects/AGENTS.md"

actor_re = re.compile(r"^dwf-dwfrun-" + RUN + r"-actor_(\d+)_(\d+)$")

# ---- executed side: stream the live steps.jsonl once, keep this run's rows
steps = collections.defaultdict(lambda: {"n": 0, "exits": collections.Counter(),
    "faces": collections.Counter(), "first": None, "last": None,
    "cmd_sample": [], "corridor_null": 0})
with open(STREAM, encoding="utf-8", errors="replace") as f:
    for line in f:
        if RUN not in line:
            continue
        try:
            d = json.loads(line)
        except Exception:
            continue
        sid = str(d.get("session_id", ""))
        if not sid.startswith("sess_"):
            continue
        bare = sid[len("sess_"):]
        m = actor_re.match(bare)
        if not m:
            continue
        a = steps[bare]
        a["n"] += 1
        res = d.get("result") or {}
        ex = res.get("exit")
        a["exits"][str(ex)] += 1
        a["faces"][str(d.get("face"))] += 1
        ts = d.get("ts", "")
        if a["first"] is None or ts < a["first"]:
            a["first"] = ts
        if a["last"] is None or ts > a["last"]:
            a["last"] = ts
        if a["n"] <= 3 or ex not in (0,):
            a["cmd_sample"].append((d.get("command") or "")[:160])

# ---- intended side: worldline actor dirs + SEED.json slabs
seeds = {}
for name in sorted(os.listdir(WL)):
    m = actor_re.match(name)
    if not m:
        continue
    sp = os.path.join(WL, name, "SEED.json")
    row = {"dir": name, "seed_path": sp, "seed_exists": os.path.isfile(sp),
           "session_match": None, "genome_agents_sha": None, "genome_agents_path": None,
           "skill_count": None, "tape_ref_path": None, "tape_rows": None,
           "tape_tip": None, "created": None, "seed_hash": None}
    if row["seed_exists"]:
        try:
            d = json.load(open(sp, encoding="utf-8"))
            row["session_match"] = (d.get("session_id") == name)
            g = (d.get("slabs") or {}).get("genome") or {}
            am = g.get("agents_md") or {}
            row["genome_agents_sha"] = am.get("sha256")
            row["genome_agents_path"] = am.get("path")
            row["skill_count"] = g.get("skill_count")
            rec = (d.get("slabs") or {}).get("record") or {}
            tr = rec.get("tape_ref") or {}
            row["tape_ref_path"] = tr.get("path")
            row["tape_rows"] = tr.get("rows")
            row["tape_tip"] = tr.get("tip_step_hash")
            row["created"] = d.get("created_utc")
            row["seed_hash"] = d.get("seed_hash")
        except Exception as e:
            row["session_match"] = f"PARSE-ERR {e}"
    seeds[name] = row

# ---- genome fidelity: live sha of both AGENTS.md candidates
def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()

live_shas = {}
for label, p in [("repo", LIVE_AGENTS_MD), ("projects", PROJ_AGENTS_MD)]:
    try:
        live_shas[label] = sha256(p)
    except Exception as e:
        live_shas[label] = f"ERR {e}"

# ---- dead tape: does ANY row of the small tape belong to this run?
dead_run_rows = 0
with open(DEAD_TAPE, encoding="utf-8", errors="replace") as f:
    for line in f:
        if RUN in line:
            dead_run_rows += 1

# ---- verdict join
all_actors = sorted(set(steps) | set(seeds), key=lambda n: (int(actor_re.match(n).group(1)), int(actor_re.match(n).group(2))))
verdicts = []
for a in all_actors:
    s, sd = steps.get(a), seeds.get(a)
    if sd is None:
        v = "UNSEEDED-EXECUTED"
    elif s is None:
        v = "SEEDED-SILENT"
    else:
        v = "SEEDED-EXECUTED"
    verdicts.append({"actor": a, "verdict": v, "steps": (s or {}).get("n", 0),
        "created": (sd or {}).get("created")})

n_seeded = sum(1 for v in verdicts if v["verdict"] != "UNSEEDED-EXECUTED")
n_exec = sum(1 for v in verdicts if v["verdict"] != "SEEDED-SILENT")
print(f"RUN {RUN}")
print(f"window: {min((v['steps'] and steps[v['actor']]['first']) or '9' * 40 for v in verdicts if v['verdict'] == 'SEEDED-EXECUTED')} .. "
      f"{max((v['steps'] and steps[v['actor']]['last']) or '' for v in verdicts if v['verdict'] == 'SEEDED-EXECUTED')}")
print(f"actors: joined={len(all_actors)} seeded={n_seeded} executed={n_exec}")
print(f"steps rows total: {sum(v['steps'] for v in verdicts)}")
print(f"dead-tape rows for this run: {dead_run_rows}")
print(f"live AGENTS.md sha: repo={live_shas['repo'][:16]} projects={live_shas['projects'][:16]}")
print()
# class census
print("VERDICT CLASSES:", dict(collections.Counter(v["verdict"] for v in verdicts)))
print()

# per-lane census (actor_N_M: N = lane, M = actor index)
lanes = collections.defaultdict(lambda: {"actors": 0, "steps": 0, "verdicts": collections.Counter()})
for v in verdicts:
    lane = actor_re.match(v["actor"]).group(1)
    lanes[lane]["actors"] += 1
    lanes[lane]["steps"] += v["steps"]
    lanes[lane]["verdicts"][v["verdict"]] += 1
for lane in sorted(lanes, key=int):
    L = lanes[lane]
    print(f"lane {lane}: actors={L['actors']} steps={L['steps']} {dict(L['verdicts'])}")
print()

# intended-side invariant checks across seeds
bad_match = [a for a, r in seeds.items() if r["seed_exists"] and r["session_match"] is not True]
no_seed = [a for a in all_actors if a not in seeds]
tape_paths = collections.Counter(r["tape_ref_path"] for r in seeds.values() if r["seed_exists"])
genome_shas = collections.Counter(r["genome_agents_sha"] for r in seeds.values() if r["seed_exists"])
genome_paths = collections.Counter(r["genome_agents_path"] for r in seeds.values() if r["seed_exists"])
skill_counts = collections.Counter(r["skill_count"] for r in seeds.values() if r["seed_exists"])
print("SEED session_id != dirname:", len(bad_match), bad_match[:5])
print("SEED tape_ref path census:", dict(tape_paths))
print("SEED tape_ref rows census:", dict(collections.Counter(r["tape_rows"] for r in seeds.values() if r["seed_exists"])))
print("SEED genome.agents_md path census:", dict(genome_paths))
print("SEED genome.agents_md sha census:", dict(genome_shas))
print("SEED skill_count census:", dict(skill_counts))
gsh = [a for a, r in seeds.items() if r["seed_exists"] and r["genome_agents_sha"] and r["genome_agents_sha"] not in live_shas.values()]
print("genome sha != live AGENTS.md (repo+projects):", len(gsh), "of", sum(1 for r in seeds.values() if r["seed_exists"]))
print()

# exit census executed side
ex_census = collections.Counter()
for a in steps.values():
    ex_census.update(a["exits"])
print("exit census over run steps:", dict(ex_census.most_common(12)))
face_census = collections.Counter()
for a in steps.values():
    face_census.update(a["faces"])
print("face census:", dict(face_census))

print()
print("== PER-ACTOR VERDICT TABLE ==")
for v in verdicts:
    a = v["actor"]
    s = steps.get(a)
    sd = seeds.get(a) or {}
    exs = ""
    if s:
        exs = " ".join(f"{k}x{c}" for k, c in s["exits"].most_common(4))
    print(f"{a} | {v['verdict']} | steps={v['steps']} | exits[{exs}] | "
          f"seed_created={sd.get('created')} | tape_rows={sd.get('tape_rows')} | "
          f"genome_sha={(sd.get('genome_agents_sha') or '')[:12]} | skills={sd.get('skill_count')}")

# non-zero exit rows with command samples for the diff section
print()
print("== NON-ZERO EXIT SAMPLES (executed vs intended zero-exit work) ==")
shown = 0
for a in all_actors:
    s = steps.get(a)
    if not s:
        continue
    for cmd in s["cmd_sample"]:
        shown += 1
        if shown > 25:
            break
        print(f"{a} :: {cmd!r}")
    if shown > 25:
        break
