# Pass 2: named-roster blind judge. Same anonymizing/shuffling as blind_full.build (imported, unchanged);
# only the instruction header differs. One DeepSeek direct call per subject (resumable).
# Key via tools.ds_workhorse.load_key, held in-process only; never printed/logged/written.
import sys, os, json, math, collections
from blind_full import build, call, now, SUBJ, REPO, D, RAW
PROG = os.path.join(D, "BLIND_ROSTER_PROGRESS.json")
ROSTER = [
 ("diogenes", "the Cynic: plain living, shamelessness, exposing pretension and convention by blunt deed"),
 ("fermat", "the proof in the margin: a claimed result whose demonstration is withheld or deferred; truth asserted ahead of its proof"),
 ("foucault", "power/knowledge regimes: who gets to name something true, surveillance, discipline, what a regime makes visible or unsayable"),
 ("plato_kirk", "the cave and the rewritten test: shadows taken for reality, leaving the cave, or rewriting an unwinnable simulator"),
 ("baudrillard", "simulacra and the hyperreal: the map replacing the territory, copies without an original, the referent gone"),
 ("bernays", "engineered consent: who benefits from a belief being held, and what holding it makes people do"),
 ("ellul", "technique as environment: a method that becomes self-justifying and makes outcomes inevitable, independent of anyone's choice"),
 ("freud", "the repressed returns: what keeps repeating, and what the repetition is a symptom of"),
 ("hall", "encoding/decoding: a message encoded one way and decoded differently by audiences: preferred vs negotiated vs oppositional readings"),
 ("jung", "shadow and archetype: what is refused a place, the shadow, persona, archetypal figures"),
 ("mcluhan", "the medium is the message: what a medium does to its users regardless of the content carried"),
 ("wallas", "desire / human nature in politics: the 'great society' run on impulse over reason; what is actually wanted, and whose machinery rides the want"),
]
LN = [k for k, _ in ROSTER]
def prompt2(subj):
    items, p1 = build(subj)
    body = p1[p1.index("\nPARABLES\n") + len("\nPARABLES\n"):]
    n = len(items); k = math.ceil(n / 12)
    head = """You are an independent blind reader. Below are %d short parables about the subject "%s", labeled only by neutral IDs (P01..P%02d) in random order. They were written by one or more unnamed authors (you are not told how many). Each parable was written through exactly ONE of the 12 lenses in the roster below. Some proper names were redacted as [-]. You get no key.

LENS ROSTER (use these exact keys):
%s

ASSIGNMENT CONSTRAINT: assign exactly one lens key to every parable. Each author wrote at most one parable per lens, so with %d parables each lens is used at most %d time(s), and lenses should be spread as evenly as the texts honestly allow (aim for every lens used). Do not force a lens onto a parable against the evidence just to fill the roster; if a parable truly fits nothing, still give your best key but low confidence and say what is missing.

For EACH parable give: lens key, confidence 0-1 (your honest probability the lens is right), the 1-2 short verbatim textual cues (quoted from the parable) that drove the pick, and if you cannot confidently place it (confidence < 0.5), what is missing (what the text would need to carry to signal its lens).
Also, separately, group parables by authorial voice (prose style, length, density, habits) as if identifying different writers; every ID in exactly one voice group.

Briefly reason in prose first if you like, then END your answer with one fenced ```json block exactly of this shape:
{"assign": {"P01": {"lens": "hall", "confidence": 0.7, "cues": ["...", "..."], "missing": ""}}, "voices": {"V1": ["P01", "..."], "V2": ["..."]}}

PARABLES
""" % (n, subj.replace("_", " "), n, "\n".join("- %s: %s" % r for r in ROSTER), n, k)
    return items, head + body
def main():
    only = sys.argv[1:] or SUBJ
    prog = json.load(open(PROG)) if os.path.exists(PROG) else {}
    todo = [s for s in only if prog.get(s, {}).get("status") != "done"]
    if not todo: print("nothing to do"); return
    sys.path.insert(0, REPO); from tools.ds_workhorse import load_key
    key = load_key()
    for s in todo:
        items, prompt = prompt2(s)
        open(os.path.join(RAW, "blind_roster_%s_prompt.txt" % s), "w", encoding="utf-8").write(prompt)
        json.dump([{k: it[k] for k in ("id","file","ractor","mouthpiece","stripped","words")} for it in items], open(os.path.join(RAW, "blind_roster_%s_map.json" % s), "w"), indent=1)
        st = now(); print(s, len(items), "start", st, flush=True)
        r, att = call(prompt, key)
        meta = {"subject": s, "n": len(items), "model_req": "deepseek-reasoner", "thinking": "enabled", "max_tokens": 65536, "start": st, "end": now(), "attempts": att, "http_calls": len(att)}
        m = {}
        if r:
            m = r["choices"][0]["message"]; meta.update(model=r.get("model"), usage=r.get("usage"), finish=r["choices"][0].get("finish_reason"))
            open(os.path.join(RAW, "blind_roster_%s_content.md" % s), "w", encoding="utf-8").write(m.get("content") or "")
            open(os.path.join(RAW, "blind_roster_%s_reasoning.md" % s), "w", encoding="utf-8").write(m.get("reasoning_content") or "")
        json.dump(meta, open(os.path.join(RAW, "blind_roster_%s_meta.json" % s), "w"), indent=1)
        prog[s] = {"status": "done" if r and (m.get("content") or "").strip() else "failed", "end": meta["end"], "model": meta.get("model"), "attempts": att}
        json.dump(prog, open(PROG, "w"), indent=1); print(s, prog[s], flush=True)
    del key
if __name__ == "__main__": main()
