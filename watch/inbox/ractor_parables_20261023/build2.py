# Builds per-ractor prompts for subject N. Reads repo files read-only. Run on PC from the out dir.
import os, re, sys, json
REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
D = os.path.dirname(os.path.abspath(__file__))
R = ["FOUCAULT","FERMAT","ELLUL","BERNAYS","MCLUHAN","JUNG","HALL","WALLAS","BAUDRILLARD","PLATO_KIRK","DIOGENES","FREUD"]
def rtext(n):
    p = os.path.join(REPO,"docs","ref","ractors",n+".md")
    if os.path.exists(p): return open(p,encoding="utf-8",errors="replace").read()[:3000], "docs/ref/ractors/%s.md"%n
    if n=="FERMAT":
        s=open(os.path.join(REPO,"mag","fermat_ractor.py"),encoding="utf-8",errors="replace").read()
        m=re.search(r'"""(.*?)"""',s,re.S); return (m.group(1) if m else s[:2500])[:3000], "mag/fermat_ractor.py docstring"
    if n=="DIOGENES":
        return open(os.path.join(REPO,"queue","handoff","ractors","DIOGENES_primer_20260911.md"),encoding="utf-8",errors="replace").read(), "queue/handoff/ractors/DIOGENES_primer_20260911.md"
subj, slug = int(sys.argv[1]), sys.argv[2]
B = open(os.path.join(D,"SUBJECT_BRIEFS.md"),encoding="utf-8").read()
brief = re.search(r"## %d %s\n(.*?)(?=\n## |\Z)"%(subj,slug),B,re.S).group(1).strip()
door = open(os.path.join(D,"door_story.md"),encoding="utf-8").read()
src={}
for n in R:
    t, s = rtext(n); src[n]=s
    P = f"""You are the Ractor {n}. Your character brief (lens, voice, signature question) is below. Speak only in that Ractor's voice.

=== RACTOR BRIEF ({n}) ===
{t}
=== END BRIEF ===

TASK: write a PARABLE-AS-SPEC about the subject "{slug.replace('_',' ')}" of the estate described in the facts below. A parable-as-spec is a story in which the rules and situations are buried in the narrative and NEVER stated: no moral, no explanation, no lists, no technical vocabulary from the facts (no "seat", "lane", "ledger", "hash", "model", "API"). Use NO real device, seat, machine, or person names from the estate (for example never write Sancho, Q, Bob, T90, Pixel, Hermes, Moto, Nacho, or any other proper name that appears in the facts); invent neutral names or use roles. A cold reader should be able to re-derive the rules from the story alone. The example below ("The Door") shows the form; do not copy its plot, images, or objects.

=== SUBJECT FACTS (ground truth; encode, do not quote) ===
{brief}
=== END FACTS ===

=== FORM EXAMPLE: The Door (excerpt) ===
{door}
=== END EXAMPLE ===

OUTPUT FORMAT, exactly:
1. A title line starting with "# ".
2. The parable, 500-900 words, in {n}'s voice and lens.
3. Then a line containing only: ---KEY---
4. Under it, 5-9 numbered lines: each rule you buried, one sentence, with the scene that carries it in parentheses.
Do not use any further tools, do not read or list any other files, do not add anything else."""
    od=os.path.join(D,"prompts",slug); os.makedirs(od,exist_ok=True)
    open(os.path.join(od,n+".txt"),"w",encoding="utf-8").write(P)
json.dump(src,open(os.path.join(D,"prompts",slug,"_sources.json"),"w"),indent=1)
print("built",len(R))

