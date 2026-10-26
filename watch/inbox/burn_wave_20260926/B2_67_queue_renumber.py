# B2-67: insert self-feeds into QUEUE.md with runtime numbering (concurrent lanes take numbers fast)
import re

QUEUE = 'watch/inbox/burn_wave_20260926/QUEUE.md'

FEEDS = [
    ('qmap', 'Build a verified q_num -> qdrops drop_no map for the Q corpus: qdrops.jsonl drop_no is a '
     '4plebs renumbering with anon posts interleaved (anchors: q14->15, q75->80, q109->125, q174->200, '
     'q200->235), so any census or ts claim keyed on naive row index is wrong (audit batch 1.2 defect 4 died '
     'on exactly this); match on text+media to map all qagg q_nums and file the map as jsonl next to the '
     'register; falsifier = the map reproduces the B1 window (q1 2017-10-28T19:33:50Z, q200 '
     '2017-11-22T22:45:01Z) and the 14 filed anchors round-trip; pointers '
     'watch/inbox/qdrop_export/qdrops.jsonl + watch/inbox/qdrop_export/Q_VISION_TRIAGE_B1.json audit_fix block.'),
    ('reaudit', 'Re-audit MICKEY17_WAVE2_QUALITY batch 1.2 for index-rule approvals: the auditor indexed '
     'qdrops.jsonl by drop_no as if it equaled qagg q_num (its 2017-11-21 window-end claim, refuted in B2-67) '
     'and blessed filed motif counts (crumbs 27, HUMA 19, rothschild 12) that no stated rule reproduces; sweep '
     'the other 5 artifacts audited in that batch for the same naive-index or unstated-ruler approvals before '
     'any remaining notes get applied as fixes; pointers '
     'watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md:45-47 + '
     'watch/inbox/burn_wave_20260926/B2_67_qvision_fixes_20260926.md.'),
]

text = open(QUEUE, encoding='utf-8').read()
nums = [int(m) for m in re.findall(r'^- \[ \] B2-(\d+)', text, re.M)]
n1 = max(nums) + 1
n2 = n1 + 1
assert f'B2-{n1}' not in text and f'B2-{n2}' not in text

header = '## Standing law note (operator, 2026-09-26, binds every lane)'
assert text.count(header) == 1
entries = [f'- [ ] B2-{n1} {FEEDS[0][1]}', f'- [ ] B2-{n2} {FEEDS[1][1]}']
text = text.replace('\n' + header, '\n' + '\n'.join(entries) + '\n\n' + header)
open(QUEUE, 'w', encoding='utf-8', newline='\n').write(text)

check = open(QUEUE, encoding='utf-8').read()
assert f'- [ ] B2-{n1} Build a verified q_num' in check
assert f'- [ ] B2-{n2} Re-audit MICKEY17_WAVE2_QUALITY' in check
print('queue feeds landed as B2-%d and B2-%d' % (n1, n2))
