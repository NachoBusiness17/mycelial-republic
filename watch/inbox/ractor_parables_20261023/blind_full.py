# Full-grid blind judge: one DeepSeek direct call per subject (resumable).
# Key via tools.ds_workhorse.load_key, held in-process only; never printed/logged/written.
import sys, os, re, json, random, glob, time, datetime, urllib.request, urllib.error, itertools
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
D = os.path.dirname(os.path.abspath(__file__)); RAW = os.path.join(D, "raw")
SUBJ = ["who_we_are","what_we_are","the_invariants","standing_wave_gate","parable_as_spec","six_lane_run",
        "water_governor","the_congress","moto_cron","keyed_verse","rib_renderman_mapping","dirac_loops"]
MP = ("fostertron_max", "agy_pc")
NAMES = ["Foucault","Fermat","Ellul","Bernays","McLuhan","Jung","Stuart Hall","Hall","Wallas","Baudrillard","Plato","Kirk","Diogenes","Freud",
 "fostertron","Fostertron","agy","GLM","glm","Gemini","Claude","Opus","Argon","DeepSeek","Ractor","Ractors","Bob","Sancho","T90","Hermes","Pixel","Senate"]
LENSKW = {"baudrillard":["baudrillard","simulacr","hyperreal"],"bernays":["bernays","propaganda","public relations","pr "],
 "diogenes":["diogenes","cynic"],"ellul":["ellul","technique"],"fermat":["fermat","proof","margin"],"foucault":["foucault","panopt","discipline","surveil"],
 "freud":["freud","psychoanal","repress","unconscious"],"hall":["stuart hall","hall","encoding/decoding","encoding","decoding"],
 "jung":["jung","archetyp","shadow","persona"],"mcluhan":["mcluhan","medium is","media"],"plato_kirk":["plato","kirk","cave","philosopher-king","republic","star trek"],
 "wallas":["wallas","incubation","illumination","creative process","stages of thought"]}
PROG = os.path.join(D, "BLIND_FULL_PROGRESS.json")
def now(): return datetime.datetime.now().astimezone().isoformat()
def build(subj):
    files = sorted(f for f in glob.glob(os.path.join(D, subj, "*.md")) if "FAILED" not in f and os.path.basename(f)[:-3].split("__")[-1] in MP)
    items = []
    for f in files:
        t = open(f, encoding="utf-8").read(); t = re.sub(r"<!--.*?-->", "", t, flags=re.S).split("---KEY---")[0].strip(); hits = []
        for n in NAMES:
            pat = r"\b%s\b" % re.escape(n); c = len(re.findall(pat, t))
            if c: hits.append((n, c)); t = re.sub(pat, "[-]", t)
        t = re.sub(r"\bQ\b", "[-]", t)
        r, m = os.path.basename(f)[:-3].split("__")[-2:]
        items.append({"file": os.path.relpath(f, D), "ractor": r, "mouthpiece": m, "body": t, "stripped": hits, "words": len(t.split())})
    random.Random("20261023" + subj).shuffle(items)
    for i, it in enumerate(items, 1): it["id"] = "P%02d" % i
    subjects = open(os.path.join(D, "SUBJECT_LIST.txt"), encoding="utf-8").read().strip()
    head = """You are an independent blind reader. Below are %d short parables, labeled only by neutral IDs (P01..P%02d) in random order. They were written by one or more unnamed authors (you are not told how many), each writing through one of several unnamed lenses (thinker-style worldviews), about subject "%s" from the list below. Each parable buries a set of rules or invariants inside its story; none are stated outright. You get no key.

SUBJECT LIST (the project's subjects):
%s

TASKS
1. BASE RULES: Re-derive the shared invariants/rules. For each: one-line normalized statement, the IDs that encode it (exhaustive), count. Order by count descending; mark which are common to ALL or nearly all.
2. PER-PARABLE: one line per ID: scene, rules encoded, any rule unique or rare to it.
3. STATUS SPLITS: same rule held with different epistemic status (settled vs doubtful); which IDs on which side.
4. GROUPINGS BY LENS: group parables by intellectual lens / thinker-style worldview; descriptive label and your best guess of the specific thinker each evokes.
5. GROUPINGS BY VOICE: separately, group parables by authorial voice (prose style, length, density, habits) as if identifying different writers. State how many voices and members of each. Every ID must be in exactly one voice group.
6. OUTLIERS and anything that looks like leakage of a hidden spec or roster.
Cite IDs everywhere. Some proper names were redacted as [-].

FINALLY, end your answer with one fenced ```json block exactly of this shape (every ID in exactly one voice group; lens groups may cover every ID):
{"base_rules": ["..."], "voices": {"V1": ["P01", "..."], "V2": ["..."]}, "lenses": [{"label": "...", "thinker_guess": "...", "ids": ["P.."]}]}

PARABLES
""" % (len(items), len(items), subj.replace("_", " "), subjects)
    prompt = head + "\n\n".join("===== %s =====\n%s" % (it["id"], it["body"]) for it in items) + "\n\n===== END =====\n"
    return items, prompt
def call(prompt, key):
    body = json.dumps({"model": "deepseek-reasoner", "messages": [{"role": "user", "content": prompt}], "max_tokens": 65536,
                       "thinking": {"type": "enabled"}}).encode()
    attempts = []; r = None
    for i in range(2):
        try:
            req = urllib.request.Request("https://api.deepseek.com/chat/completions", body, {"Content-Type": "application/json", "Authorization": "Bearer " + key})
            r = json.load(urllib.request.urlopen(req, timeout=1800)); attempts.append("ok"); break
        except urllib.error.HTTPError as e:
            attempts.append("HTTP %s %s" % (e.code, e.read()[:300])); r = None; break
        except Exception as e:
            attempts.append("transport " + repr(e)[:200]); r = None; time.sleep(15)
    return r, attempts
def main():
    only = sys.argv[1:] or SUBJ
    prog = json.load(open(PROG)) if os.path.exists(PROG) else {}
    todo = [s for s in only if prog.get(s, {}).get("status") != "done"]
    if not todo: print("nothing to do"); return
    sys.path.insert(0, REPO); from tools.ds_workhorse import load_key
    key = load_key()
    for s in todo:
        items, prompt = build(s)
        open(os.path.join(RAW, "blind_full_%s_prompt.txt" % s), "w", encoding="utf-8").write(prompt)
        json.dump([{k: it[k] for k in ("id","file","ractor","mouthpiece","stripped","words")} for it in items], open(os.path.join(RAW, "blind_full_%s_map.json" % s), "w"), indent=1)
        st = now(); print(s, len(items), "start", st, flush=True)
        r, att = call(prompt, key)
        meta = {"subject": s, "n": len(items), "model_req": "deepseek-reasoner", "thinking": "enabled", "max_tokens": 65536, "start": st, "end": now(), "attempts": att, "http_calls": len(att)}
        if r:
            m = r["choices"][0]["message"]; meta.update(model=r.get("model"), usage=r.get("usage"), finish=r["choices"][0].get("finish_reason"))
            open(os.path.join(RAW, "blind_full_%s_content.md" % s), "w", encoding="utf-8").write(m.get("content") or "")
            open(os.path.join(RAW, "blind_full_%s_reasoning.md" % s), "w", encoding="utf-8").write(m.get("reasoning_content") or "")
        json.dump(meta, open(os.path.join(RAW, "blind_full_%s_meta.json" % s), "w"), indent=1)
        prog[s] = {"status": "done" if r and (m.get("content") or "").strip() else "failed", "end": meta["end"], "model": meta.get("model"), "attempts": att}
        json.dump(prog, open(PROG, "w"), indent=1); print(s, prog[s], flush=True)
    del key
if __name__ == "__main__": main()
