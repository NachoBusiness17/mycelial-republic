"""Refined classification of ALLOW_RE hits by which regex group matched."""
import math, os, re, sys
from collections import Counter

sys.path.insert(0, str(__file__).rsplit('/', 1)[0] if '/' in __file__ else '.')
from tools.secret_gate_rules import ALLOW_RE, ENTROPY_MIN, ENT_LEN_MIN

clause_patterns = {
    'your_api_key': re.compile(r'your[_\-]?api[_\-]?key', re.I),
    'your_token': re.compile(r'your[_\-]?token', re.I),
    'angle_bracket': re.compile(r'<[^>\n]{1,40}>'),
    'dollar_brace': re.compile(r'\$\{[^}\n]{1,40}\}'),
    'x_repeat': re.compile(r'x{4,}'),
    'dot_repeat': re.compile(r'\.{4,}'),
    'star_repeat': re.compile(r'\*{3,}'),
    'REDACTED': re.compile(r'REDACTED'),
    'MASKED': re.compile(r'MASKED'),
    'PLACEHOLDER': re.compile(r'PLACEHOLDER'),
    'EXAMPLE': re.compile(r'EXAMPLE[_A-Z]*'),
    'DUMMY': re.compile(r'DUMMY'),
    'FAKE': re.compile(r'FAKE'),
    'abcd1234': re.compile(r'abcd1234'),
    '1234567890': re.compile(r'1234567890'),
    '0123456789abcdef': re.compile(r'0123456789abcdef'),
}

def shannon(s):
    freq = Counter(s); n = len(s)
    return -sum((c/n)*math.log2(c/n) for c in freq.values())

repo = __import__('pathlib').Path('.').resolve()
hits = Counter()
examples = {k: [] for k in clause_patterns}
uncategorized = []

file_count = 0
for root, dirs, files in os.walk(repo):
    dirs[:] = [d for d in dirs if d not in {'.git','node_modules','__pycache__','.venv','venv'}]
    for fname in files:
        file_count += 1
        if file_count > 200: break
        ext = os.path.splitext(fname)[1].lower()
        if ext not in {'.py','.js','.ts','.json','.md','.yaml','.yml','.toml','.txt','.sh'}:
            continue
        fpath = os.path.join(root, fname)
        try:
            content = open(fpath, encoding='utf-8', errors='replace').read()
        except: continue
        for line in content.splitlines():
            for raw in line.split():
                tok = raw.strip("'\"`[],:;(){}")
                if len(tok) < ENT_LEN_MIN: continue
                if not ALLOW_RE.search(tok): continue
                h = shannon(tok)
                matched = False
                for name, pat in clause_patterns.items():
                    if pat.search(tok):
                        hits[name] += 1
                        matched = True
                        if h >= ENTROPY_MIN and len(examples[name]) < 3:
                            examples[name].append((tok, round(h,2), len(tok)))
                if not matched:
                    hits['UNCATEGORIZED'] += 1
                    if h >= ENTROPY_MIN and len(uncategorized) < 5:
                        uncategorized.append((tok, round(h,2), len(tok), os.path.basename(fpath)))

print('ALLOW hits by regex group (all entropy levels):')
for k, v in hits.most_common():
    print(f'  {k}: {v}')
print(f'\nTotal hits: {sum(hits.values())}')
print()
print('High-entropy examples by clause:')
for k, v in examples.items():
    if v:
        print(f'  {k}:')
        for tok, ent, ln in v:
            print(f'    tok={tok!r} entropy={ent} len={ln}')
if uncategorized:
    print('  UNCATEGORIZED high-entropy examples:')
    for tok, ent, ln, fname in uncategorized:
        print(f'    tok={tok!r} entropy={ent} len={ln} file={fname}')