import os, json, hashlib, collections

root = r"C:\Users\foste\.ollama\models\manifests"
if not os.path.isdir(root):
    print("NO OLLAMA MANIFESTS DIR at", root)
    raise SystemExit

mhash = {}   # manifest sha -> [tags]
gguf = collections.defaultdict(set)  # weights blob digest -> tags
for dirpath, dirs, files in os.walk(root):
    for fn in files:
        fp = os.path.join(dirpath, fn)
        rel = os.path.relpath(fp, root).split("manifests")[-1].lstrip("\\/").replace("\\", "/")
        data = open(fp, "rb").read()
        h = hashlib.sha256(data).hexdigest()
        mhash.setdefault(h, []).append(rel)
        try:
            m = json.loads(data)
            for layer in m.get("layers", []):
                mt = layer.get("mediaType", "")
                if "image.model" in mt or "gguf" in mt.lower():
                    gguf[layer["digest"]].add(rel)
        except Exception as e:
            print("unparsed manifest", rel, e)

print("== manifest-level aliases (byte-identical manifest files) ==")
aliased = False
for h, tags in sorted(mhash.items()):
    if len(tags) > 1:
        aliased = True
        print(h[:16], "->", tags)
if not aliased:
    print("(none)")

print("== weights-blob-level aliases (same GGUF digest, different manifests) ==")
aliased2 = False
for d, tags in sorted(gguf.items()):
    if len(tags) > 1:
        aliased2 = True
        print(d[:30], "->", sorted(tags))
if not aliased2:
    print("(none)")

print("total manifests:", sum(len(v) for v in mhash.values()),
      "distinct manifest sha:", len(mhash),
      "distinct gguf blobs:", len(gguf))
