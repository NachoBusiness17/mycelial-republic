"""model_census — walk every local model cache, parse weight headers, map the fleet's disk brain.

Operator order (2026-09-11): "LOOK AT THE NUMBER OF MODELS ON OUR DISK I HAVE PLANNED FOR YOU
TO MANUALLY NAVIGATE. I've been trying to get you to map their internals in ways humans can
understand in only ways you can see."

Header-only reads: GGUF magic/KV/tensor-info parse, safetensors JSON-header parse. No tensor
data leaves its disk slot. Stdlib + struct only. Read-only. $0.

Lineage: mag/vram_memory.py (2026-08-12, "keep it in vram so we can really make this thing
cook") — the hot lattice. DeepSeek shipped the same memory-hierarchy architecture as Engram
on 2026-09-10 (arXiv 2601.07372). This census is the navigation map he asked for: every model
on disk, its lookup-table geometry vs compute core, so internals mapping starts from truth.

Schema: model_census.v1
"""
from __future__ import annotations

import json
import struct
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOTS = [
    ("ollama", Path(r"C:/Users/foste/.ollama/models")),
    ("lmstudio", Path(r"C:/Users/foste/.lmstudio/models")),
    ("hf", Path(r"C:/Users/foste/.cache/huggingface/hub")),
]

GGUF_MAGIC = b"GGUF"
GGUF_VTYPE = {0: "u8", 1: "i8", 2: "u16", 3: "i16", 4: "u32", 5: "i32",
              6: "f32", 7: "bool", 8: "str", 9: "arr", 10: "u64", 11: "i64", 12: "f64"}
SCALAR_FMT = {"u8": "<B", "i8": "<b", "u16": "<H", "i16": "<h", "u32": "<I", "i32": "<i",
              "f32": "<f", "bool": "<?", "u64": "<Q", "i64": "<q", "f64": "<d"}
SCALAR_SIZE = {"u8": 1, "i8": 1, "u16": 2, "i16": 2, "u32": 4, "i32": 4,
               "f32": 4, "bool": 1, "u64": 8, "i64": 8, "f64": 8}

# bytes/element by GGUF tensor type (ql/qh packed sizes: main quant 2.0625bpw style omitted
# where exotic; estimates labeled ESTIMATE in report when no parameter_count metadata exists)
QUANT_BPE = {0: 4.0, 1: 2.0, 2: 1.0625, 3: 0.5625, 6: 1.0, 7: 0.5625, 8: 0.59375,
             9: 0.53125, 10: 0.5625, 11: 0.5625, 12: 0.59375, 13: 0.5625, 14: 0.53125,
             16: 2.03125, 17: 1.03125, 18: 0.53125, 19: 0.546875, 20: 0.5625,
             28: 0.25, 30: 0.53125, 32: 1.0625, 36: 0.53125}


class Buf:
    """One-shot header window: read a bounded slice once, parse from bytes.

    The hand-validated shape (no incremental refills — those desync-and-explode on
    garbage lengths). 128MB covers every known GGUF header incl. full vocabs."""

    def __init__(self, f, window=1 << 27):
        self.b = f.read(window)
        self.i = 0

    def need(self, n):
        if len(self.b) - self.i < n:
            raise EOFError(f"header window exhausted (wanted {n})")
        out = self.b[self.i:self.i + n]
        self.i += n
        return out

    def scalar(self, t):
        return struct.unpack(SCALAR_FMT[t], self.need(SCALAR_SIZE[t]))[0]

    def string(self):
        n = self.scalar("u64")
        return self.need(n).decode("utf-8", "replace")

    def value(self, t):
        t = GGUF_VTYPE[t] if isinstance(t, int) else t
        if t == "str":
            return self.string()
        if t == "arr":
            at = GGUF_VTYPE[self.scalar("u32")]
            n = self.scalar("u64")
            if at in SCALAR_SIZE:
                self.need(n * SCALAR_SIZE[at])
                return f"<arr {at}[{n}]>"
            if at == "str":
                items = [self.string() for _ in range(min(n, 4))]
                for _ in range(max(0, n - 4)):
                    self.need(self.scalar("u64"))
                return f"<arr str[{n}]> {items[:4]}"
            return f"<arr {at}>"
        return self.scalar(t)


def _gguf(path: Path):
    rec = {"format": "gguf", "gguf_version": None}
    with open(path, "rb") as f:
        if f.read(4) != GGUF_MAGIC:
            return None
        rec["gguf_version"] = struct.unpack("<I", f.read(4))[0]
        buf = Buf(f)
        n_tensors = struct.unpack("<Q", buf.need(8))[0]
        n_kv = struct.unpack("<Q", buf.need(8))[0]
        kv = {}
        for _ in range(n_kv):
            k = buf.string()
            vt = struct.unpack("<I", buf.need(4))[0]
            try:
                kv[k] = buf.value(GGUF_VTYPE[vt])
            except Exception as e:
                kv[k] = f"<parse-error {e}>"
        arch = str(kv.get("general.architecture", "?"))
        tensors = []
        for _ in range(min(n_tensors, 4096)):
            name = buf.string()
            nd = struct.unpack("<I", buf.need(4))[0]
            shape = [struct.unpack("<Q", buf.need(8))[0] for _ in range(nd)]
            ttype = struct.unpack("<I", buf.need(4))[0]
            buf.need(8)  # offset
            tensors.append((name, shape, ttype))
        rec["tensor_count"] = n_tensors
        rec["tensors_parsed"] = len(tensors)
    keep_kv = {}
    for k, v in kv.items():
        if isinstance(v, str) and v.startswith("<arr"):
            keep_kv[k] = v.split(">")[0].strip("<") if "[" in v else v
        elif isinstance(v, (int, float, bool, str)):
            keep_kv[k] = v
    rec["kv"] = {k: v for k, v in keep_kv.items() if not k.startswith("tokenizer.")}
    rec["tokenizer_kv"] = sorted(k for k in kv if k.startswith("tokenizer."))
    census_from_tensors(rec, tensors)
    return rec


def census_from_tensors(rec, tensors):
    arch = str(rec["kv"].get("general.architecture", "?"))
    n_params = 0
    expert_params = 0
    expert_tensors = 0
    embed_shape = None
    output_shape = None
    layers = set()
    max_type = 1
    for name, shape, ttype in tensors:
        nel = 1
        for s in shape:
            nel *= s
        n_params += nel
        max_type = max(max_type, ttype)
        if ".ffn_" in name and "_exps" in name:
            expert_tensors += 1
            expert_params += nel
        if name.endswith(f"{arch}.token_embd.weight"):
            embed_shape = shape
        if name.endswith(f"{arch}.output.weight"):
            output_shape = shape
        if f"{arch}.block." in name:
            try:
                layers.add(int(name.split(f"{arch}.block.")[1].split(".")[0]))
            except Exception:
                pass
    bpe = QUANT_BPE.get(max_type, 2.0)
    rec["params_total"] = n_params
    rec["params_est_note"] = "ESTIMATE-from-tensor-shapes@quant-bpe" if not rec["kv"].get("general.parameter_count") else "metadata"
    rec["params_expert"] = expert_params
    rec["expert_tensor_count"] = expert_tensors
    rec["is_moe"] = expert_tensors > 0
    rec["embed_shape"] = embed_shape
    rec["output_shape"] = output_shape
    rec["n_layers"] = len(layers) if layers else rec["kv"].get(f"{arch}.block_count")
    rec["lookup_share"] = round((expert_params + (embed_shape[0] * embed_shape[1] if embed_shape else 0)) / n_params, 4) if n_params else None
    rec["bytes_per_weight_assumed"] = bpe


def _safetensors(path: Path):
    rec = {"format": "safetensors"}
    with open(path, "rb") as f:
        n = struct.unpack("<Q", f.read(8))[0]
        if n > (1 << 28):
            return None
        header = json.loads(f.read(n))
    header.pop("__metadata__", None) and None
    meta = {}
    n_params = 0
    expert_params = 0
    expert_tensors = 0
    embed_shape = None
    layers = set()
    for name, info in header.items():
        shape = info.get("shape", [])
        nel = 1
        for s in shape:
            nel *= s
        n_params += nel
        if ".ffn" in name and ("experts" in name or ".experts." in name):
            expert_tensors += 1
            expert_params += nel
        if "embed" in name and embed_shape is None:
            embed_shape = shape
        if ".layers." in name:
            try:
                layers.add(int(name.split(".layers.")[1].split(".")[0]))
            except Exception:
                pass
    rec["kv"] = meta
    rec["tensor_count"] = len(header)
    rec["params_total"] = n_params
    rec["params_est_note"] = "EXACT-from-shapes"
    rec["params_expert"] = expert_params
    rec["expert_tensor_count"] = expert_tensors
    rec["is_moe"] = expert_tensors > 0
    rec["embed_shape"] = embed_shape
    rec["n_layers"] = len(layers)
    rec["lookup_share"] = round(expert_params / n_params, 4) if n_params else None
    return rec


def walk(source, root: Path):
    out = []
    if not root.exists():
        return out
    for p in root.rglob("*"):
        try:
            if not p.is_file():
                continue
            big = p.stat().st_size
            if big < (1 << 24):  # <16MB: not a weight shard
                continue
            name = p.name.lower()
            if not (name.endswith(".gguf") or name.endswith(".safetensors") or "sha256-" in name or name.endswith(".bin")):
                continue
            rec = None
            if name.endswith(".safetensors") or name.endswith(".bin"):
                rec = _safetensors(p)
            if rec is None:
                rec = _gguf(p)
            if rec is None:
                continue
            rec["path"] = str(p)
            rec["source"] = source
            rec["size_bytes"] = big
            rel = p.relative_to(root)
            rec["model"] = str(rel.parent) if source != "ollama" else ollama_model_name(root, p)
            out.append(rec)
        except Exception as e:
            out.append({"path": str(p), "source": source, "error": repr(e)[:200]})
    return out


def ollama_model_name(root: Path, blob: Path) -> str:
    """Map an ollama sha256 blob back to its model:tag via the manifests."""
    target = str(blob).replace("\\", "/").lower()
    man = root / "manifests"
    best = blob.name[:12]
    try:
        for m in man.rglob("*"):
            if not m.is_file():
                continue
            try:
                data = json.loads(m.read_text())
            except Exception:
                continue
            for layer in data.get("layers", []):
                if layer.get("mediaType", "").endswith("model"):
                    digest = layer.get("digest", "")
                    cand = str(root / "blobs" / digest.replace(":", "-"))
                    if cand.lower() == target:
                        rel = m.relative_to(man)
                        return "/".join(rel.parts[-3:-1] + [rel.parts[-1]])
    except Exception:
        pass
    return f"blob:{best}"


def main():
    t0 = datetime.now(timezone.utc)
    rows = []
    for source, root in ROOTS:
        rows.extend(walk(source, root))
    # aggregate shards per model
    models = {}
    for r in rows:
        if "error" in r:
            models.setdefault(r["path"], {"error": r["error"], "source": r["source"]})
            continue
        key = (r["source"], r["model"])
        m = models.setdefault(f"{r['source']}/{r['model']}", {
            "source": r["source"], "model": r["model"], "files": 0,
            "size_bytes": 0, "params_total": 0, "params_expert": 0,
            "expert_tensor_count": 0, "formats": set(), "embed_shape": None,
            "n_layers": 0, "arch": "?", "quant": "?", "paths": [],
        })
        m["files"] += 1
        m["size_bytes"] += r["size_bytes"]
        m["params_total"] = max(m["params_total"], r.get("params_total") or 0)
        m["params_expert"] = max(m["params_expert"], r.get("params_expert") or 0)
        m["expert_tensor_count"] += r.get("expert_tensor_count", 0)
        m["formats"].add(r.get("format", "?"))
        if r.get("embed_shape"):
            m["embed_shape"] = r["embed_shape"]
        m["n_layers"] = max(m["n_layers"], r.get("n_layers") or 0)
        m["arch"] = r.get("kv", {}).get("general.architecture") or m["arch"]
        m["quant"] = r.get("kv", {}).get("general.file_type") or m["quant"]
        m["paths"].append(r["path"])
    for m in models.values():
        if isinstance(m.get("formats"), set):
            m["formats"] = sorted(m["formats"])
        pt = m.get("params_total") or 0
        m["size_gb"] = round(m["size_bytes"] / 1e9, 2) if "size_bytes" in m else None
        m["lookup_share"] = round(m.get("params_expert", 0) / pt, 4) if pt else None
    out = {
        "schema": "model_census.v1",
        "generated_utc": t0.isoformat(),
        "roots": {s: str(p) for s, p in ROOTS},
        "model_count": len([m for m in models.values() if "error" not in m]),
        "disk_gb_total": round(sum(m.get("size_bytes", 0) for m in models.values()) / 1e9, 1),
        "models": dict(sorted(models.items(), key=lambda kv: -(kv[1].get("size_bytes") or 0))),
    }
    dst = Path(r"C:/Users/foste/Documents/projects/local_sovereign_agent/dashboard/static/model_census.json")
    dst.parent.mkdir(parents=True, exist_ok=True)
    dst.write_text(json.dumps(out, indent=1), encoding="utf-8")
    print(f"WROTE {dst} · {out['model_count']} models · {out['disk_gb_total']} GB · {len(rows)} weight files")
    for k, m in out["models"].items():
        if "error" in m:
            print(f"  ERROR {k}: {m['error']}")
            continue
        e = m.get("embed_shape")
        print(f"  {k:55s} {m['size_gb']:>7} GB  params={m['params_total']/1e9:8.2f}B  moe={m['expert_tensor_count']>0!s:5s} lookup={m['lookup_share']} layers={m['n_layers']} embed={e} arch={m['arch']} quant={m['quant']}")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
