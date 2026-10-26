# Steering-review verification for the open-local-language-models via x steal card.
# Pure file I/O, no subprocess spawns. Reviewer seat, 2026-10-05.
import json, os, sys, unicodedata

ROOT = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
CARD = os.path.join(ROOT, r"watch\inbox\frontier_olm_2026-10-05\steal\open-local-language-models via x.md")
RAW = os.path.join(ROOT, r"watch\inbox\frontier_olm_2026-10-05\sweep\_raw")

def read(p, mode="r", enc="utf-8"):
    with open(p, mode, encoding=enc if mode == "r" else None) as f:
        return f.read() if mode == "r" else f.read()

card = read(CARD)
lines = card.splitlines()

print("== 1. Em-dash / en-dash byte scan of the whole card ==")
for i, ln in enumerate(lines, 1):
    for ch, name in (("\u2014", "EM DASH"), ("\u2013", "EN DASH")):
        if ch in ln:
            print(f"  line {i}: {name} found")
print("  scan done (no output above = none found)")

print("\n== 2. chars claim (20893) ==")
# prose body = everything before the '## Machine-readable card' header line
idx = next(i for i, ln in enumerate(lines) if ln.startswith("## Machine-readable card"))
prose_incl = "\n".join(lines[:idx]) + "\n"      # incl trailing newline before header
prose_excl = "\n".join(lines[:idx])
print(f"  header at line {idx+1}; prose lines 1..{idx}")
print(f"  chars with trailing newline: {len(prose_incl)}")
print(f"  chars without trailing newline: {len(prose_excl)}")
print(f"  claimed: 20893")

print("\n== 3. Machine-readable JSON validity + field list ==")
json_line = lines[idx + 2] if len(lines) > idx + 2 else lines[-1]
try:
    j = json.loads(json_line)
    print(f"  VALID JSON; keys: {sorted(j.keys())}")
    print(f"  area: {j.get('area')!r}")
    print(f"  source_url: {j.get('source_url')!r}")
    print(f"  chars field: {j.get('chars')!r}")
    for k in ("steal", "estate_map", "probe"):
        print(f"  {k}: {len(j.get(k, ''))} chars")
except Exception as e:
    print(f"  JSON PARSE FAILED: {e}")

def norm_variants(s):
    # return the string plus common unicode-normalized variants for apostrophes/quotes
    return s

def check(name, hay, needle):
    if needle in hay:
        print(f"  [EXACT] {name}")
        return True
    # try curly->straight normalization on both sides
    def flat(x):
        return (x.replace("\u2019", "'").replace("\u2018", "'")
                 .replace("\u201c", '"').replace("\u201d", '"'))
    if flat(needle) in flat(hay):
        print(f"  [NORMALIZED-ONLY] {name} (unicode apostrophe/quote differs)")
        return True
    print(f"  [MISSING] {name}")
    return False

print("\n== 4. fx_AA_2063059212532642193.json ==")
aa = read(os.path.join(RAW, "fx_AA_2063059212532642193.json"))
try:
    aaj = json.loads(aa)
    tw = aaj.get("tweet", aaj)
    print(f"  created: {tw.get('created_at')!r}; likes: {tw.get('likes')}; views: {tw.get('views')}")
    txt = tw.get("text", {}).get("full_text") if isinstance(tw.get("text"), dict) else tw.get("text", "")
    print(f"  text field len: {len(txt) if txt else 0}")
    check("family sentence", txt or aa,
          "Gemma 4 12B is the largest in the Gemma 4 family to support transcription, alongside Gemma 4 E4B and Gemma 4 E2B, with Gemma 4 31B and Gemma 4 26B A4B supporting text, image and video input only.")
    check("platforms sentence", txt or aa, "available on a variety of platforms including Hugging Face, Ollama and LMStudio")
    for frag in ("8.8% on AA-WER (#58)", "Voxtral Mini Transcribe 2 (3.6% WER, with 4B parameters)", "Voxtral Small (2.8% WER, with 12B parameters)"):
        check(f"WER frag: {frag[:40]}...", aa, frag)
except Exception as e:
    print(f"  parse note: {e}; falling back to raw substring checks")
    for frag in ("largest in the Gemma 4 family to support transcription",
                 "Hugging Face, Ollama and LMStudio", "8.8", "Voxtral"):
        check(f"raw frag {frag[:40]}", aa, frag)

print("\n== 5. fx_GDM_2039735446628925907.json ==")
gdm = read(os.path.join(RAW, "fx_GDM_2039735446628925907.json"))
try:
    gj = json.loads(gdm)
    tw = gj.get("tweet", gj)
    print(f"  created: {tw.get('created_at')!r}; likes: {tw.get('likes')}; bookmarks: {tw.get('bookmarks')}; views: {tw.get('views')}")
    txt = tw.get("text", {}).get("full_text") if isinstance(tw.get("text"), dict) else tw.get("text", "")
    check("launch quote", txt or gdm,
          "Meet Gemma 4: our new family of open models you can run on your own hardware. Built for advanced reasoning and agentic workflows, we're releasing them under an Apache 2.0 license.")
except Exception as e:
    print(f"  parse note: {e}")

print("\n== 6. fx_leo_2043631410045452360.json ==")
leo = read(os.path.join(RAW, "fx_leo_2043631410045452360.json"))
try:
    lj = json.loads(leo)
    tw = lj.get("tweet", lj)
    print(f"  created: {tw.get('created_at')!r}; likes: {tw.get('likes')}; bookmarks: {tw.get('bookmarks')}; views: {tw.get('views')}")
    art = tw.get("article") or {}
    if isinstance(art, dict):
        print(f"  article title: {art.get('title')!r}")
        pt = art.get("preview_text") or ""
        check("preview_text quote", pt,
              "I moved everything to a headless Mac Mini M4, the base $599 model with 16GB of RAM. Started with smaller Qwen models for message classification and context")
    else:
        print(f"  article field type: {type(art)}")
except Exception as e:
    print(f"  parse note: {e}")

print("\n== 7. rlamma_top_month.rss ==")
rss = read(os.path.join(RAW, "rlamma_top_month.rss"))
import re
m = re.search(r"<updated>([^<]+)</updated>", rss)
print(f"  feed <updated>: {m.group(1) if m else 'NOT FOUND'}")
cat_count = rss.count('category term="LocalLLaMA"')
print(f"  category LocalLLaMA lines: {cat_count}")
check("bonsai title", rss, "Ternary Bonsai 2 (27B) just released on Hugging Face. At <6GB in size, it can even run locally in-browser on WebGPU.")
check("qwen4 apsara title", rss, "Qwen 4 Announced at Apsara Conference")

print("\n== 8. HAD abs page on disk? ==")
hits = []
for dirpath, dirnames, filenames in os.walk(os.path.join(ROOT, "watch\inbox\frontier_olm_2026-10-05")):
    for fn in filenames:
        p = os.path.join(dirpath, fn)
        try:
            b = read(p, enc="utf-8", mode="r")
        except Exception:
            try:
                b = read(p, enc="utf-8", mode="r")
            except Exception:
                continue
        if "Harness-Aware" in b or "2610.02858" in b:
            hits.append(p)
for h in hits:
    print(f"  on-disk mention: {h}")

print("\n== 9. state/arxiv/2026-10-02/ listing ==")
d = os.path.join(ROOT, "state", "arxiv", "2026-10-02")
if os.path.isdir(d):
    for fn in sorted(os.listdir(d)):
        print(f"  {fn}")
else:
    print(f"  {d} DOES NOT EXIST")
