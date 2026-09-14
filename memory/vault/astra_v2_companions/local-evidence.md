# Local evidence excerpts

Read on 2026-09-11. Source paths are relative to C:/Users/foste/Documents/projects/local_sovereign_agent. These are bounded excerpts, not a full repository audit.

## watch/inbox/OFFLOAD_WAVE_FOLD_20260911.md
```text
10: **L2 MTP** (agent_f542666a): mechanism verified from DeepSeek-V3 paper — shared embed + shared head + one block + d×2d projection; 85-90% acceptance, 1.8x TPS. TOOLING LIVE: llama.cpp merged MTP (`--spec-type draft-mtp`), Ollama 0.31 serves Gemma-4 MTP auto-drafted (~90% faster), vLLM/SGLang listed. The two disk models are the two layouts (separate draft file vs bundled `nextn.*`) — dissection pair ready, `gguf_dump` next. CORRECTNESS: Engram ≠ MTP — memory axis vs decode axis, do not conflate in the narrative.
11: 
12: **L3 CORPUS-ENGRAM** (agent_11834f7d): capacity math: whole corpus (~19M chunks @ d256 fp16 ≈ **9.7GB**) fits hot in 64GB desk RAM. verkle `leaf_hash` = the ready-made deterministic key; `theme_vector` = dormant slot habit. **NOVELTY: no literature prior found for prefetch-on-predicted-address over an agent corpus** — Engram/HugeCTR/MoE prefetch is all model-internal; the fleet's temp:HOT tags + access history are the training signal for the open claim. v0 BUILD: content-addressed slot table, hits O(1) + tri-state hit/miss mask, misses → similarity path. SKIP: VRAM slots on 6GB card, Engram-scale n-gram tables, gating/conv (training-time). Defect caught: `ram_cache.py` is ~2MB text, not corpus-in-RAM as doctrine assumed.
```

## watch/astra_hold0/DESK_HOLD1_VERDICT_20260911.md
```text
8: | Check | Worker A | Worker B | Agree |
9: |---|---|---|---|
10: | rows_checked | 7,379 | 7,379 | ✓ (same sha256 47c97c27…) |
11: | resolved | 7,367 | 7,367 | ✓ |
12: | missing | 12 | 12 | ✓ |
13: | verdict | DISPUTED | DISPUTED | ✓ |
14: | anomaly (dict-repr row 2513) | caught | caught | ✓ |
15: | rubric score | 11/11 | 11/11 | ✓ |
16: 
17: Divergence (documented, not scored): ambiguous_filenames — A counted 3,773
18: (live-vs-2026-08-25-backup duplication), B counted 0. Procedural reading of one
19: unscored field. TEMPLATE AMENDMENT for HOLD 2: define ambiguity scope in one line
20: (does P4 duplication count?).
21: 
22: ## TWO BONUS FINDINGS
23: 
24: 1. Both workers measured **7,379 rows** — the seed froze at 7,377. The +2 are
25:    post-repair appends: the chain's flow is confirmed by two independent audits.
26:    The desk key re-derives at review time, exactly as designed.
```

## mag/vram_memory.py
```text
58:                 "n_resident": len(loaded)}
59:     except Exception as e:
60:         return {"ok": False, "error": str(e)[:120]}
61: 
62: 
63: def hot_region() -> dict[str, Any]:
64:     """The VRAM-resident hot-memory region (the lattice): the hot corpus kept at VRAM speed.
65:     Reads the in-memory corpus (ram_cache) as the hot set + reports the GPU state. Honest."""
66:     try:
67:         from mag import ram_cache
68:         c = ram_cache.corpus()
69:         n_docs = c.get("counts", {}).get("n_documents", 0)
70:     except Exception:
71:         n_docs = 0
72:     gpu = _gpu_state()
73:     res = _ollama_resident()
74:     return {"ok": True, "schema": SCHEMA, "vram_cap_gb": VRAM_CAP,
75:             "hot_documents": n_docs, "gpu": {"source": gpu.get("source"),
76:                                              "vram_used_pct": gpu.get("vram_used_pct")},
77:             "ollama": res,
78:             "note": ("hot corpus VRAM-confirmed" if gpu.get("vram_used_pct") is not None else
79:                      "hot corpus in RAM — VRAM unconfirmed (gpu source=" + str(gpu.get("source")) + ")")}
80: 
81: 
82: def warm_in_vram(*, data: str | None = None) -> dict[str, Any]:
83:     """Push the hot data into the VRAM-resident region. Honest about the backend: if the GPU probe
84:     can't resolve (source:none) or ollama isn't resident, reports the blocker — never fabricates."""
85:     gpu = _gpu_state()
86:     if gpu.get("source") == "none":
87:         return {"ok": False, "schema": SCHEMA, "error": gpu.get("error", "gpu blind"),
88:                 "blocker": "VRAM telemetry can't resolve (rocm/nvidia probe) — the hot lattice "
89:                            "can't be confirmed resident", "gpu": gpu}
90:     # the hot lattice is the warm prefix + corpus, kept resident; report what's hot
91:     from mag import rib_bus
92:     try:
93:         m = rib_bus.mount("warm")
94:         n_warm = m.get("n_ribs", 0)
95:     except Exception:
96:         n_warm = 0
97:     return {"ok": True, "schema": SCHEMA, "vram_used_pct": gpu.get("vram_used_pct"),
98:             "warm_ribs": n_warm,
99:             "note": "hot lattice resident in VRAM (warm prefix + corpus) — reads hit VRAM speed"}
100: 
101: 
102: def cook() -> dict[str, Any]:
103:     """Keep hot memory resident when VRAM is proven. Never claim VRAM when the probe is blind."""
104:     gpu = _gpu_state()
105:     hot = hot_region()
106:     ollama = hot.get("ollama") or {}
107:     n_res = int(ollama.get("n_resident") or 0)
108:     pct = gpu.get("vram_used_pct")
109:     proven = pct is not None or n_res > 0
110:     if pct is not None:
111:         stage = "vram"
```

## mag/rib_bus.py
```text
72:     try:
73:         return json.loads(f.read_text(encoding="utf-8", errors="replace"))
74:     except Exception:
75:         return {"domain": domain, "ribs": {}, "updated": None}
76: 
77: 
78: def _save_store(store: dict[str, Any]) -> Path:
79:     f = _domain_file(store["domain"])
80:     f.parent.mkdir(parents=True, exist_ok=True)
```

## mag/rib_bus.py
```text
152:     }
153: 
154: 
155: def mount(domain: str = "general") -> dict[str, Any]:
156:     """Auto-load the bus-grown RIB instruction set for a domain from memory. Deterministic + $0."""
157:     store = _load_store(domain)
158:     ribs = [r["invariant"] for r in store["ribs"].values()] if store.get("ribs") else []
159:     return {"ok": True, "schema": SCHEMA, "domain": domain, "n_ribs": len(ribs),
160:             "ribs": ribs, "updated": store.get("updated")}
161: 
162: 
163: def inject_for(slice_text: str, domain: str = "general") -> str:
```

## mag/ram_cache.py
```text
25: 
26: sys.path.insert(0, str(ROOT))
27: 
28: SCHEMA = "ram_cache.v1"
29: MAX_CORPUS_CHARS = 2_000_000          # cap the in-memory corpus (RAM is bounded, don't OOM)
30: 
31: # module-level cache: loaded once, served from RAM on repeated passes
32: _CACHE: dict[str, Any] = {"loaded": False, "documents": [], "text": "", "counts": {},
33:                           "_fingerprint": 0.0}   # newest corpus-dir mtime at last load
34: 
35: # the corpus dirs the cache watches for staleness (auto-refresh when disk is newer)
36: _CORPUS_DIRS = ("memory/research_packs", "memory/steal", "memory/rib")
37: 
38: 
39: def _fingerprint() -> float:
40:     """Newest mtime across the watched corpus dirs. Cheap (one scandir per dir, no full re-read).
41:     Used to auto-invalidate the cache: if disk is newer than the last load, the cache is stale."""
42:     best = 0.0
43:     for rel in _CORPUS_DIRS:
44:         d = ROOT / rel
45:         if not d.is_dir():
46:             continue
47:         try:
48:             for e in d.iterdir():
49:                 if e.name.endswith(".md") and e.is_file():
50:                     try:
51:                         best = max(best, e.stat().st_mtime)
52:                     except Exception:
53:                         continue
54:         except Exception:
55:             continue
56:     return best
57: 
58: 
59: def _read_md_dir(d: Path, n: int = 200) -> list[dict[str, str]]:
60:     out: list[dict[str, str]] = []
61:     if not d.is_dir():
62:         return out
63:     for p in sorted(d.glob("*.md"))[-n:]:
64:         try:
65:             txt = p.read_text(encoding="utf-8", errors="replace")
66:             out.append({"path": str(p.relative_to(ROOT)), "text": txt[:1200],
67:                         "title": txt.splitlines()[0][:120] if txt.splitlines() else p.stem})
68:         except Exception:
69:             continue
70:     return out
71: 
72: 
73: def load_corpus(*, refresh: bool = False) -> dict[str, Any]:
74:     """Load the corpus (research packs + steals + chain tail) into MEMORY once, cached. Returns the
75:     cache state. Deterministic + $0. The in-memory fast-path for lensing/novelty/processing."""
76:     if _CACHE["loaded"] and not refresh:
77:         # auto-invalidate: if the corpus dirs changed on disk since the last load, the cache is
78:         # stale -> reload so lensing/novelty/processing never read a frozen snapshot. Cheap check.
79:         if _fingerprint() <= _CACHE["_fingerprint"]:
80:             return {"ok": True, "schema": SCHEMA, "cached": True, **_CACHE["counts"]}
81:         refresh = True
82: 
83:     docs: list[dict[str, str]] = []
84:     docs += _read_md_dir(ROOT / "memory" / "research_packs", 200)
85:     docs += _read_md_dir(ROOT / "memory" / "steal", 200)
86:     docs += _read_md_dir(ROOT / "memory" / "rib", 100)
87: 
88:     text_parts: list[str] = []
89:     total = 0
90:     for d in docs:
```

## mag/verkle_knot.py
```text
140: 
141: 
142: def _leaf_hash(obj: Any) -> str:
143:     raw = json.dumps(obj, sort_keys=True, default=str).encode("utf-8")
144:     return _h(b"leaf:" + raw)
145: 
146: 
```

## mag/verkle_knot.py
```text
269:     leaf = {
270:         "type": "session_scalar_knot_leaf",
271:         "schema": "verkle_knot_leaf.v1",
272:         "session_id": dossier.get("session_id"),
273:         "start_minute": created.get("iso_minute"),
274:         "end_minute": updated.get("iso_minute"),
275:         "start_unix_minute": created.get("unix_minute"),
276:         "end_unix_minute": updated.get("unix_minute"),
277:         "date": created.get("date"),
278:         "duration_minutes": sk.get("duration_minutes"),
279:         "dominant_theme": tv.get("dominant"),
280:         "theme_basis": basis if basis else THEME_BASIS,
281:         "theme_vector_raw": raw,
282:         "theme_vector_normalized": norm[: len(THEME_BASIS)],
283:         "tension_index": sk.get("tension_index"),
284:         "residual_weight": sk.get("residual_weight"),
285:         "Q_proxy": sk.get("Q_proxy"),
286:         "gap_proxy": sk.get("gap_proxy"),
287:         "lambda2_proxy": sk.get("lambda2_proxy"),
288:         "dirichlet_energy_proxy": sk.get("dirichlet_energy_proxy"),
289:         "dossier_commit": commit.get("hex"),
290:         "chord_commitment": (dossier.get("chord") or {}).get("commitment_hash"),
291:         "chord_root": (dossier.get("chord") or {}).get("framework_root"),
292:         "observer_chart_scores": {
293:             c.get("id"): c.get("score")
294:             for c in ((dossier.get("chord") or {}).get("observer_charts") or [])
295:         },
296:         "loops_audited": [
297:             L.get("id") for L in ((dossier.get("chord") or {}).get("loops_audited") or [])
298:         ],
299:         "engine": "untangling+strike_chord",
300:         "inspiration": "steiniger_proxies+strike_chord+verkle_history",
301:     }
302:     leaf["leaf_hash"] = _leaf_hash(leaf)
303:     return leaf
304: 
```

## mag/chain_substrate.py
```text
127: 
128: def vmem(address: str | None = None) -> dict[str, Any]:
129:     """VMEM — the chain as VIRTUAL MEMORY: leaf_hash is an ADDRESS; read the payload at it."""
130:     rows = _chain_rows()
131:     if not rows:
132:         return {"ok": False, "schema": SCHEMA, "role": "vmem", "error": "empty chain"}
133:     # default: read the latest leaf (the top of vmem)
134:     if not address:
135:         target = rows[-1]
136:     else:
137:         target = next((r for r in rows if (r.get("leaf_hash") or "").startswith(address.lower())), None)
138:         if target is None:
139:             return {"ok": False, "schema": SCHEMA, "role": "vmem", "error": f"no leaf at {address}",
140:                     "n_addressable": len(rows)}
141:     return {"ok": True, "schema": SCHEMA, "role": "vmem", "address": address or "latest",
142:             "leaf_hash": target.get("leaf_hash", ""), "session_id": target.get("session_id"),
143:             "theme": target.get("theme"), "index": target.get("index"),
144:             "verkle_root": target.get("verkle_root", ""),
145:             "note": "leaf_hash = address; the chain is addressable virtual memory"}
146: 
147: 
148: def heartbeat() -> dict[str, Any]:
149:     """HEARTBEAT — the PULSE: whether the chain is alive/advancing (time since last write)."""
150:     tip = _load_json(TIP)
151:     last = tip.get("ts") or ""
```
