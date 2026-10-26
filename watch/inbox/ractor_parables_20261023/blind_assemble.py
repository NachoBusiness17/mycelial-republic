import json,os
D=os.path.dirname(os.path.abspath(__file__)); R=lambda p:open(os.path.join(D,p),encoding="utf-8").read()
meta=json.load(open(os.path.join(D,"raw","blind_meta.json"))); m=json.load(open(os.path.join(D,"BLIND_MAP.json")))
o=["# BLIND JUDGE: Ractor parables batch 1 (who_we_are), DeepSeek direct, one call","",
"- Salon test (watch/SALON_STANDING_ORDER_20260907.md): 'if the cast can't re-derive it, it wasn't an invariant'.",
"- Carrier: tools.ds_workhorse.load_key -> api.deepseek.com/chat/completions, same as door_invariant ds_eval.py (blind_ds.py). Not routed via Hermes.",
"- Requested: deepseek-reasoner, max_tokens 65536. **Served model: `%s`**. finish=%s. usage=%s"%(meta.get("model"),meta.get("finish"),json.dumps(meta.get("usage"))),
"- Time (ET): %s -> %s. Attempts: %s"%(meta["start"],meta["end"],meta["attempts"]),
"- Files: BLIND_PROMPT.txt, BLIND_MAP.json (local only, never sent), raw/blind_content.md, raw/blind_reasoning.md, raw/blind_meta.json, blind_build.py, blind_ds.py","",
R("raw/blind_scoring.md"),"","## HIDDEN MAPPING (never sent)","","| ID | Ractor | Mouthpiece | Words | Redacted |","|---|---|---|---|---|"]
o+=["| %s | %s | %s | %s | %s |"%(x["id"],x["ractor"],x["mouthpiece"],x["words"],x["stripped"] or "") for x in m]
o+=["","## RAW OUTPUT (DeepSeek content, verbatim)","",R("raw/blind_content.md"),"","## PROMPT (verbatim, as sent)","","````",R("BLIND_PROMPT.txt"),"````"]
open(os.path.join(D,"BLIND_JUDGE.md"),"w",encoding="utf-8").write("\n".join(o))
