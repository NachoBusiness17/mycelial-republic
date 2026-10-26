# B2-67: append LEDGER row (json.dumps, never heredoc) + insert self-feeds under ## Open in QUEUE.md
import json
from datetime import datetime, timezone

LEDGER = 'memory/burns/LEDGER.jsonl'
QUEUE = 'watch/inbox/burn_wave_20260926/QUEUE.md'

row = {
    'ts': datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
    'slug': 'B2-67-qvision-b1-audit-fixes',
    'verdict': 'LANDED',
    'landing': 'watch/inbox/burn_wave_20260926/B2_67_qvision_fixes_20260926.md',
    'one_line': (
        'wave-2 audit batch 1.2 defects 1-3 fixed in Q_VISION_TRIAGE_B1.json from bytes: findings[1] numerator '
        'reconciled (10 = non-screenshot TYPE rows byte-checked, 15 = pictorial-content rows incl. 5 '
        'screenshot-typed renders); owl 9 replaced by word-boundary presence 6 (182,184,185,188,189,192) / '
        'occurrences 20 with the 3 substring false positives named (knowledge 25, prowl 109, acknowledgment 186); '
        'all 23 motifs recomputed under one documented regex rule, each entry now carrying presence_drops + '
        'occurrences + range + full drops list (deltas disclosed: crumbs 27->26, HUMA 19->16, rothschild 12->13, '
        'wizards 4->6; findings[2] counts unchanged); defect 4 REFUTED ON BYTES: qdrops.jsonl drop_no is a 4plebs '
        'renumbering, not qagg q_num (drop_no 200 = q_num 174 ts 2017-11-21, q_num 200 Rizvi = drop_no 235 ts '
        '2017-11-22T22:45:01), so the 2017-11-22 window end stands, now byte-anchored with 14 content-match '
        'anchors filed in findings[6] + audit_fix block; no code consumers, shared_surface validate run; '
        'self-feeds B2-221/222'
    ),
}

before = sum(1 for _ in open(LEDGER, encoding='utf-8'))
with open(LEDGER, 'a', encoding='utf-8', newline='\n') as f:
    f.write(json.dumps(row, ensure_ascii=False) + '\n')
after = sum(1 for _ in open(LEDGER, encoding='utf-8'))
assert after == before + 1, (before, after)
print('ledger rows:', before, '->', after)

FEEDS = [
    '- [ ] B2-221 Build a verified q_num -> qdrops drop_no map for the Q corpus: qdrops.jsonl drop_no is a '
    '4plebs renumbering with anon posts interleaved (anchors: q14->15, q75->80, q109->125, q174->200, q200->235), '
    'so any census or ts claim keyed on naive row index is wrong (audit batch 1.2 defect 4 died on exactly this); '
    'match on text+media to map all qagg q_nums and file the map as jsonl next to the register; falsifier = the '
    'map reproduces the B1 window (q1 2017-10-28T19:33:50Z, q200 2017-11-22T22:45:01Z) and the 14 filed anchors '
    'round-trip; pointers watch/inbox/qdrop_export/qdrops.jsonl + watch/inbox/qdrop_export/Q_VISION_TRIAGE_B1.json '
    'audit_fix block.',
    '- [ ] B2-222 Re-audit MICKEY17_WAVE2_QUALITY batch 1.2 for index-rule approvals: the auditor indexed '
    'qdrops.jsonl by drop_no as if it equaled qagg q_num (its 2017-11-21 window-end claim, refuted in B2-67) and '
    'blessed filed motif counts (crumbs 27, HUMA 19, rothschild 12) that no stated rule reproduces; sweep the '
    'other 5 artifacts audited in that batch for the same naive-index or unstated-ruler approvals before any '
    'remaining notes get applied as fixes; pointers watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md:45-47 + '
    'watch/inbox/burn_wave_20260926/B2_67_qvision_fixes_20260926.md.',
]

text = open(QUEUE, encoding='utf-8').read()
header = '## Standing law note (operator, 2026-09-26, binds every lane)'
assert text.count(header) == 1
assert 'B2-221' not in text and 'B2-222' not in text
text = text.replace('\n' + header, '\n' + '\n'.join(FEEDS) + '\n\n' + header)
open(QUEUE, 'w', encoding='utf-8', newline='\n').write(text)
check = open(QUEUE, encoding='utf-8').read()
assert 'B2-221' in check and 'B2-222' in check
print('queue: feeds inserted before standing-law note')
