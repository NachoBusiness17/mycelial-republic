"""Seat-verify DeepSeek corpus-fold drafts (state/fuel/corpus_fold_out_w*.jsonl)
against their source digests (state/fuel/corpus_fold_in_w*.jsonl).

Checks per draft:
  1. parse: JSON row loads, ok flag, out text nonempty.
  2. citation check: every path/URL token in the draft's Sources section must
     appear as a substring in the source digest text (the prompt told the worker
     to cite only paths named in the text).
  3. on-disk check: how many of those cited paths exist on disk.
  4. subject check: word-overlap (Jaccard on lowercase words len>=4) between
     draft body and source body.
Verdict PASS only if citation_hits == total_citations (all citations are
grounded in the source). Anything else FAILS and must not land.
"""
import json, os, re, sys

REPO = os.path.normpath(os.path.join(os.path.dirname(__file__), '../../../../../..'))
os.chdir(REPO)
FUEL = 'state/fuel'

def load_jsonl(path):
    rows = []
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                rows.append(json.loads(line))
    return rows

drafts = {}
for w in ('w0', 'w1'):
    for row in load_jsonl(f'{FUEL}/corpus_fold_out_{w}.jsonl'):
        drafts[row['id']] = dict(row, worker=w)
sources = {}
for w in ('w0', 'w1'):
    for row in load_jsonl(f'{FUEL}/corpus_fold_in_{w}.jsonl'):
        sources[row['id']] = row['text']

# also carry the untruncated items file if longer
for row in load_jsonl(f'{FUEL}/corpus_fold_items.jsonl'):
    if len(row['text']) > len(sources.get(row['id'], '')):
        sources[row['id']] = row['text']

def citations_of(out_text):
    # backticked tokens that look like paths or URLs, plus bare URLs
    toks = set(re.findall(r'`([^`\n]+)`', out_text))
    toks |= set(re.findall(r'https?://[^\s`,)]+', out_text))
    keep = set()
    for t in toks:
        if '/' in t or t.startswith('estate://') or t.startswith('estate/'):
            keep.add(t.strip('.,;'))
    return sorted(keep)

def words(t):
    return set(w for w in re.findall(r'[a-z]{4,}', t.lower()))

fails = 0
for pid in sorted(drafts):
    d = drafts[pid]
    src = sources.get(pid, '')
    out = d.get('out') or ''
    toks = citations_of(out)
    grounded = [t for t in toks if t in src]
    on_disk = [t for t in toks
               if not t.startswith('http') and not t.startswith('estate')
               and os.path.exists(t.split(' ')[0])]
    jac = len(words(out) & words(src)) / max(1, len(words(out) | words(src)))
    ok_parse = bool(d.get('ok')) and len(out) > 0
    verdict = 'PASS' if (ok_parse and len(toks) > 0 and len(grounded) == len(toks)) else 'FAIL'
    if verdict == 'FAIL':
        fails += 1
    print(f"draft {pid} (worker {d['worker']}): parse_ok={ok_parse} "
          f"citations={len(toks)} grounded_in_source={len(grounded)} on_disk={len(on_disk)} "
          f"word_jaccard={jac:.3f} verdict={verdict}")
    un = [t for t in toks if t not in src]
    if un:
        print('  ungrounded citations (not in source text):')
        for t in un[:12]:
            print(f'    - {t}')
print()
print(f'TOTAL: {len(drafts)} drafts, {fails} FAIL, {len(drafts)-fails} PASS')
print('Spiking source digest bytes:', len(sources.get('spiking', '')),
      repr(sources.get('spiking', '')[:80]))
sys.exit(0)
