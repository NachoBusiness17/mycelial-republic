"""Overlap greps for sweep candidates: catalog.jsonl + text files under memory/
skipping binaries. Prints per-pattern hit counts and sample lines."""
import os
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

ROOT = r'C:\Users\foste\Documents\projects\local_sovereign_agent'
PATTERNS = {
    'Reading KLD': r'Reading KLD',
    'KLD nats quant': r'KLD.{0,40}(nats|quant)|\bKLD\b',
    'zettelkastten': r'zettelkastten',
    'How to Run Large Models Locally': r'How to Run Large Models Locally',
    'Dev_trader0': r'Dev_trader0',
    'BrandonMusicKy': r'BrandonMusicKy|brandonmuskcy',
    'above_spec R4': r'above_spec|R4 quant',
    'ik_llama.cpp': r'ik_llama\.cpp',
    'Fermonroyh agentic benchmark': r'Fermonroyh|single file agentic benchmark',
    'ankit_appy KV': r'ankit_appy',
    'Q4_K_M vs Q8_0 (ours, dedup marker)': r'Q4_K_M vs Q8_0|Q4_K_M vs q8_0',
    'bits/weight 4.89': r'4\.89 bits|bits/weight',
    '70B@Q4 beats 8B@FP16': r'70B@Q4|Q4 usually beats',
    'E4M3 E5M2 KV': r'E4M3.{0,30}E5M2',
    'MoE routing quant KLD': r'routing choices differ',
    'Qwen-Image-2.1 GGUF 12GB': r'Qwen-Image-2\.1.{0,80}12GB',
    'EmbeddingGemma 2 740M': r'EmbeddingGemma 2',
    'GLM-5.3-Flash 3.3x (sibling dedup marker)': r'GLM-5\.3-Flash.{0,40}3\.3x',
}

TEXT_EXT = {'.md', '.json', '.jsonl', '.txt', '.py', '.html', '.yaml', '.yml', '.rst', '.csv'}


def iter_files():
    yield os.path.join(ROOT, 'catalog', 'catalog.jsonl')
    memroot = os.path.join(ROOT, 'memory')
    for dirpath, _dirs, files in os.walk(memroot):
        for fn in files:
            ext = os.path.splitext(fn)[1].lower()
            if ext in TEXT_EXT:
                yield os.path.join(dirpath, fn)


files = list(iter_files())
for label, pat in PATTERNS.items():
    rx = re.compile(pat, re.I)
    hits = 0
    samples = []
    for path in files:
        try:
            with open(path, encoding='utf-8', errors='ignore') as f:
                for i, line in enumerate(f, 1):
                    if rx.search(line):
                        hits += 1
                        if len(samples) < 3:
                            rel = os.path.relpath(path, ROOT)
                            samples.append(f'  {rel}:{i}: {line.strip()[:150]}')
        except OSError:
            pass
    print(f'[{label}] hits={hits}')
    for s in samples:
        print(s)
