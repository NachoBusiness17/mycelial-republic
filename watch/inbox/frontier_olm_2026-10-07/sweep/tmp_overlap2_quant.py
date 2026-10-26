"""Single-pass overlap grep: walk memory/ text files once, test all patterns
per line. Prints hit counts + up to 2 samples per pattern, flushed live."""
import os
import re
import io
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
ROOT = r'C:\Users\foste\Documents\projects\local_sovereign_agent'
PATTERNS = {
    'JakeKAllDay/llamAmpere': r'JakeKAllDay|llamAmpere|JakeATX',
    'TQ5/TQ4 KV quant': r'TQ5/TQ4|TurboQuant 5/5|8-13 bits',
    'Reading KLD article': r'Reading KLD|BrandonMusicKy|brandonmuskcy',
    'zettelkastten guide': r'zettelkastten|How to Run Large Models Locally',
    'EVO-X3 / gmktec': r'EVO-X3|gmktec',
    'above_spec R4': r'above_spec',
    'Fermonroyh bench': r'Fermonroyh|single file agentic benchmark',
    'ankit_appy KV': r'ankit_appy',
    'Qwen-Image-2.1 12GB': r'Qwen-Image-2\.1',
    'Dynamic FP8 6GB': r'Dynamic FP8',
    '500M downloads GGUF': r'500M model downloads',
    'VeriLoop (banked marker)': r'VeriLoop',
    'BreadthKV (banked marker)': r'BreadthKV',
    '70B@Q4 vs 8B@FP16 rule': r'70B@Q4',
    'E4M3 vs E5M2': r'E4M3.{0,20}E5M2',
}
TEXT_EXT = {'.md', '.json', '.jsonl', '.txt', '.py', '.html', '.yaml', '.yml', '.rst', '.csv'}
rxs = {k: re.compile(v, re.I) for k, v in PATTERNS.items()}
counts = {k: 0 for k in PATTERNS}
samples = {k: [] for k in PATTERNS}


def scan(path):
    try:
        with open(path, encoding='utf-8', errors='ignore') as f:
            for i, line in enumerate(f, 1):
                for k, rx in rxs.items():
                    if rx.search(line):
                        counts[k] += 1
                        if len(samples[k]) < 2:
                            rel = os.path.relpath(path, ROOT)
                            samples[k].append(f'  {rel}:{i}: {line.strip()[:130]}')
    except OSError:
        pass


scan(os.path.join(ROOT, 'catalog', 'catalog.jsonl'))
for dirpath, _dirs, files in os.walk(os.path.join(ROOT, 'memory')):
    for fn in files:
        if os.path.splitext(fn)[1].lower() in TEXT_EXT:
            scan(os.path.join(dirpath, fn))
for k in PATTERNS:
    print(f'[{k}] hits={counts[k]}')
    for s in samples[k]:
        print(s)
    sys.stdout.flush()
