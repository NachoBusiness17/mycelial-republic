import os, re, json, random, glob
D = os.path.dirname(os.path.abspath(__file__))
files = sorted(f for f in glob.glob(os.path.join(D, "who_we_are", "*.md")) if "FAILED" not in f)
cs = [f for f in glob.glob(os.path.join(D, "claude_sample", "**", "*.md"), recursive=True) if "who_we_are" in f and "FAILED" not in f]
files += sorted(cs)
NAMES = ["Foucault","Fermat","Ellul","Bernays","McLuhan","Jung","Stuart Hall","Hall","Wallas","Baudrillard","Plato","Kirk","Diogenes","Freud",
 "fostertron","Fostertron","agy","GLM","glm","Gemini","Claude","Opus","Argon","DeepSeek","Ractor","Ractors","Bob","Sancho","T90","Hermes","Pixel","Senate"]
items = []
for f in files:
    t = open(f, encoding="utf-8").read()
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = t.split("---KEY---")[0].strip()
    hits = []
    for n in NAMES:
        pat = r"\b%s\b" % re.escape(n)
        if n in ("Hall",):  # only strip as name if capitalized standalone surname context
            pass
        c = len(re.findall(pat, t))
        if c:
            hits.append((n, c)); t = re.sub(pat, "[—]", t)
    t = re.sub(r"\bQ\b", "[—]", t)
    base = os.path.basename(f)[:-3]
    r, m = base.split("__")[-2:]
    items.append({"file": os.path.relpath(f, D), "ractor": r, "mouthpiece": m, "body": t, "stripped": hits, "words": len(t.split())})
random.Random(20261023).shuffle(items)
for i, it in enumerate(items, 1): it["id"] = "P%02d" % i
subjects = open(os.path.join(D, "SUBJECT_LIST.txt"), encoding="utf-8").read().strip()
head = """You are an independent blind reader. Below are %d short parables, labeled only by neutral IDs (P01..P%02d) in random order. They were written by several unnamed authors, each writing through one of several unnamed lenses, about the first subject in the list below. Each parable buries a set of rules or invariants inside its story; none are stated outright. You get no key.

SUBJECT LIST (the project's subjects; these parables address subject 1):
%s

TASKS
1. SHARED INVARIANTS: List every rule/invariant you can infer that recurs across parables. For each: a one-line normalized statement, the IDs that encode it (be exhaustive), and a count. Order by count descending. Mark which you judge common to ALL or nearly all.
2. PER-PARABLE: For each ID, one line: the scene, the rules it encodes, and any rule unique or rare to it.
3. STATUS SPLITS: Where parables encode the same rule with different epistemic status (e.g. settled law vs. held as doubtful/unproven), say which IDs fall on which side.
4. GROUPINGS BY LENS: Group the parables by apparent intellectual lens / thinker-style worldview (what theme or obsession each one adds beyond the shared rules). Give each group a descriptive label, and if you can, guess the thinker it evokes. Expect several parables per lens.
5. GROUPINGS BY VOICE: Separately, group the parables by apparent authorial voice (prose style, length, density, habits), as if identifying different writers. State how many voices you think there are and the members of each.
6. OUTLIERS and anything that looks like leakage of a hidden spec or roster.
Be concrete and cite IDs everywhere. Some proper names were redacted as [—].

PARABLES
""" % (len(items), len(items), subjects)
body = "\n\n".join("===== %s =====\n%s" % (it["id"], it["body"]) for it in items)
open(os.path.join(D, "BLIND_PROMPT.txt"), "w", encoding="utf-8").write(head + body + "\n\n===== END =====\n")
json.dump([{k: it[k] for k in ("id","file","ractor","mouthpiece","stripped","words")} for it in items], open(os.path.join(D, "BLIND_MAP.json"), "w"), indent=1)
print(len(items), sum(it["words"] for it in items), [ (it["id"], it["stripped"]) for it in items if it["stripped"]])

