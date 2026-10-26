# B2-67: fix the 4 audit defects in watch/inbox/qdrop_export/Q_VISION_TRIAGE_B1.json
# cause: wave-2 audit batch 1.2 (watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md:45-47)
# defects 1-3 fixed as filed; defect 4 refuted on bytes (qdrops drop_no != qagg q_num)
import json, re, sys

PATH = 'watch/inbox/qdrop_export/Q_VISION_TRIAGE_B1.json'
doc = json.load(open(PATH, encoding='utf-8'))
rows = doc['rows']
assert len(rows) == 200

PATTERNS = {
    'crumbs': r'\bcrumbs?\b',
    'alice_and_wonderland': r'alice\s*(?:&|and)\s*wonderland',
    'snow_white': r'\bsnow\s*white\b',
    'godfather_iii': r'godfather\s*(?:iii|lll|3)\b',
    'HUMA': r'\bhuma\b',
    'soros': r'\bsoros\b',
    'rothschild': r'\broths?childs?\b',
    'mockingbird': r'\bmockingbird\b',
    'pray': r'\bpray(?:ers?|ing|ed)?\b',
    'classified': r'\bclassified\b',
    'owl': r'\bowls?\b',
    'great_awakening': r'\bgreat\s*awakening\b',
    'disinformation_is_real': r'\bdisinformation\s+is\s+(?:real|necessary)\b',
    'plus_countdown': r'\+\+\+',
    'follow_the_money': r'\bfollow\s*the\s*money\b',
    'iron_eagle': r'\biron\s*eagle\b',
    'fantasy_land': r'\bfantasy\s*land\b',
    'false_flag': r'\bfalse\s*flags?\b',
    'wizards_and_warlocks': r'\bwizards?\s*(?:&|and)\s*warlocks?\b',
    'the_storm': r'\bthe\s*storm\b',
    'keystone': r'\bkeystones?\b',
    'epstein_island': r'\bepstein\b',
    'spirit_cooking': r'\bspirit\s*cooking\b',
}

ORDER = list(PATTERNS.keys())

def census_entry(pattern):
    cre = re.compile(pattern, re.I)
    pres, occ = [], 0
    for r in rows:
        hits = cre.findall(r['reading'])
        if hits:
            pres.append(r['q_num'])
            occ += len(hits)
    return {
        'presence_drops': len(pres),
        'occurrences': occ,
        'range': [pres[0], pres[-1]] if pres else [],
        'drops': pres,
    }

new_census_entries = {name: census_entry(p) for name, p in PATTERNS.items()}

# audit batch 1.2 defect 2: owl must be presence 6 / occurrences 20
owl = new_census_entries['owl']
assert owl['presence_drops'] == 6 and owl['occurrences'] == 20, owl
assert owl['drops'] == [182, 184, 185, 188, 189, 192], owl

# defect 1 support: types census byte check
types = {}
for r in rows:
    t = r['reading'].split('\n')[0].replace('TYPE: ', '').strip()
    types.setdefault(t, []).append(r['q_num'])
nonshot = sum((v for k, v in types.items() if k != 'screenshot'), [])
assert sorted(nonshot) == [14, 51, 75, 109, 125, 130, 149, 185, 193, 196], nonshot
assert len(types['screenshot']) == 190

new_census = {
    'note': ('drop-level motif census, recomputed 2026-09-26 from the 200 readings in this file '
             '(audit batch 1.2 defects 2-3): rule = case-insensitive regex (see patterns) over each '
             "row's reading; presence_drops = rows with at least one hit; occurrences = total hits; "
             'range = [first, last] q_num with a hit; drops = full q_num list. The filed 2026-09-19 '
             'hand counts are superseded where they differ under this rule: crumbs 27 -> 26, '
             'HUMA 19 -> 16, rothschild 12 -> 13 (Rothchild variant row 187), owl 9 -> 6, '
             'wizards_and_warlocks 4 -> 6 (& forms in rows 80, 81). The old owl 9 came from substring '
             'matches inside knowledge (row 25), prowl (row 109) and acknowledgment (row 186).'),
    'rule': 'case-insensitive regex per pattern; counts, ranges and drop lists are machine-recomputable from rows[].reading',
    'patterns': dict(PATTERNS),
}
for name in ORDER:
    new_census[name] = new_census_entries[name]
doc['text_motif_census'] = new_census

# defect 1: reconcile numerator and list in findings[1]
F = doc['findings']
assert F[1].startswith('only 10/200'), F[1][:40]
F[1] = ('pictorial-content numerator reconciled (audit batch 1.2): 10/200 rows are non-screenshot TYPE '
        '(art 2: 14, 109; meme 2: 51, 75; photo 5: 125, 130, 185, 193, 196; image-post 1: 149) and 15/200 '
        'carry independent pictorial content once 5 screenshot-typed renders embedding photos/maps are '
        'included: drops 14, 28, 51, 75, 106, 109, 115, 125, 130, 149, 185, 188, 191, 193, 196 (the 5 adds: '
        '28 Spy.png, 106 phone UI, 115 Manila street map, 188 owl-outline map, 191 Vatican audience hall); '
        'the Q corpus visual register is TEXT-first, the inverse of the Mr Pool image set')

# defect 4: window end stands at 2017-11-22; anchor it to content-matched qdrops rows
assert F[6].startswith('window 1-200'), F[6][:30]
F[6] = ('window 1-200 = the /pol/ era, byte-anchored 2017-10-28T19:33:50Z (q_num 1) to 2017-11-22T22:45:01Z '
        '(q_num 200, Rizvi Traverse) per qdrops.jsonl ts read off content-matched rows; qdrops.jsonl drop_no '
        'is a 4plebs renumbering that diverges from qagg q_num (naive row 200 is q_num 174, ts '
        '2017-11-21T01:12:32, which is how audit batch 1.2 got 2017-11-21), so window dates must use content '
        'matches, not row indexes; anchors q_num->drop_no: 1->1, 14->15, 28->28, 51->52, 75->80, 109->125, '
        '131->149, 149->169, 174->200, 182->210, 184->215, 192->226, 193->227, 200->235; batch 2 continues at '
        'q_num 201; drop_00589_0.jpg (the 4plebs Patriots.jpg) should be folded into the batch covering drop 589')

# audit_fix provenance block
doc['audit_fix'] = {
    'date': '2026-09-26',
    'cause': ('wave-2 audit batch 1.2, watch/inbox/MICKEY17_WAVE2_QUALITY_20260925.md:45-47 '
              '(Q_VISION_TRIAGE_B1.json PASS-with-notes, 4 defects); repaired by burn lane B2-67'),
    'defects': [
        {'n': 1,
         'claim': "findings numerator says 10/200 but lists 15 drops",
         'resolution': ('reconciled from rows: 10 = non-screenshot TYPE rows (byte-checked), 15 = rows '
                        'carrying independent pictorial content (5 screenshot-typed renders embed photos/maps); '
                        'findings[1] rewritten with both counts and per-TYPE drop lists'),
         'status': 'fixed'},
        {'n': 2,
         'claim': 'text_motif_census owl=9 irreproducible (audit recount: presence 6 / occurrences 20)',
         'resolution': ('confirmed on bytes: word-boundary recount gives presence 6 (182, 184, 185, 188, 189, '
                        '192) and occurrences 20; the filed 9 was substring matching inside knowledge (25), '
                        'prowl (109), acknowledgment (186); whole census recomputed for all 23 motifs under one '
                        'documented regex rule (text_motif_census.rule + patterns)'),
         'status': 'fixed'},
        {'n': 3,
         'claim': 'census note promises per-motif range values, none present',
         'resolution': ('every motif entry now carries presence_drops, occurrences, range [first, last] and the '
                        'full drops list, machine-recomputable from rows[].reading'),
         'status': 'fixed'},
        {'n': 4,
         'claim': "findings window end 2017-11-22 off by a day: qdrops.jsonl drop 200 ts 2017-11-21",
         'resolution': ('REFUTED ON BYTES: qdrops.jsonl drop_no is not qagg q_num; drop_no 200 is q_num 174 '
                        '(ts 2017-11-21T01:12:32) while q_num 200 (Rizvi Traverse) is drop_no 235, ts '
                        '2017-11-22T22:45:01; window end 2017-11-22 stands, now anchored to content-matched rows '
                        'with the divergence mapping filed in findings[6] and here; the audit premise (row index '
                        '= drop number) is the defect'),
         'status': 'refuted_on_bytes'},
    ],
}

# receipt.validation updated
doc['receipt']['validation'] = (
    '200 rows, q_num unique and gap-free 1..200, four-line schema verified on every row, zero em-dashes; '
    'motif census recomputed 2026-09-26 under text_motif_census.rule, owl presence 6 / occurrences 20 '
    'byte-verified (audit batch 1.2)')

text = json.dumps(doc, indent=1, ensure_ascii=False) + '\n'
for bad in ('\u2014', '\u2013'):
    assert bad not in text, 'dash law violated'
open(PATH, 'w', encoding='utf-8', newline='\n').write(text)

# re-verify from disk
doc2 = json.load(open(PATH, encoding='utf-8'))
owl2 = doc2['text_motif_census']['owl']
assert owl2['presence_drops'] == 6 and owl2['occurrences'] == 20
assert doc2['text_motif_census']['alice_and_wonderland']['presence_drops'] == 22
assert doc2['text_motif_census']['snow_white']['presence_drops'] == 21
assert doc2['text_motif_census']['godfather_iii']['presence_drops'] == 20
assert len(doc2['rows']) == 200
print('FIX OK')
print('owl:', owl2)
for k in ('crumbs', 'HUMA', 'rothschild', 'wizards_and_warlocks', 'disinformation_is_real', 'the_storm'):
    e = doc2['text_motif_census'][k]
    print(k, 'presence', e['presence_drops'], 'occ', e['occurrences'], 'range', e['range'])
