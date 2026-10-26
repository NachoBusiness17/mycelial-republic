import json, re, sys

pats = {
    "MiMo-V2": re.compile(r"MiMo-V?2", re.I),
    "mimo": re.compile(r"\bMiMo\b"),
    "MobileGym": re.compile(r"MobileGym|agent_eval|liangyuRen", re.I),
    "unsloth_docker": re.compile(r"Unsloth Docker|docker image", re.I),
    "500m": re.compile(r"500M|500 million", re.I),
    "qwen_image_21": re.compile(r"Qwen-Image-2", re.I),
    "structured_output_recipe": re.compile(r"structured-output compliance|structured output compliance", re.I),
    "construct_validity": re.compile(r"construct validity", re.I),
    "freiesleben": re.compile(r"Freiesleben", re.I),
    "eggroll": re.compile(r"EGGROLL", re.I),
    "distill_qwen_9b": re.compile(r"Distill-Qwen|distill.qwen", re.I),
    "self_improvement_rl": re.compile(r"Scaling Reinforcement Learning Towards Self-Improvement|Towards Self-Improvement", re.I),
    "pinned_offload": re.compile(r"pinned offload|pinned.offload|offloading to RAM", re.I),
}

def scan(root, label):
    import os
    hits = {k: [] for k in pats}
    for dirpath, dirnames, filenames in os.walk(root):
        # bound the walk: skip giant binary dirs
        dirnames[:] = [d for d in dirnames if d not in (".git", "node_modules", "__pycache__")]
        for fn in filenames:
            if not fn.endswith((".md", ".jsonl", ".json", ".txt", ".py")):
                continue
            p = os.path.join(dirpath, fn)
            try:
                if os.path.getsize(p) > 20_000_000:
                    continue
                with open(p, encoding="utf-8", errors="replace") as f:
                    for i, line in enumerate(f, 1):
                        for k, pat in pats.items():
                            if pat.search(line):
                                hits[k].append(f"{p}:{i}")
            except Exception:
                continue
    print(f"== {label} ==")
    for k, v in hits.items():
        shown = v[:4]
        print(f"  {k}: {len(v)}" + (f" e.g. {'; '.join(shown)}" if shown else ""))

scan("memory", "MEMORY/")
scan("catalog", "CATALOG (names only via jsonl lines)")
