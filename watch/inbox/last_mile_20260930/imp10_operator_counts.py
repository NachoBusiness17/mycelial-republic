"""IMP10 — operator-model re-base on UNFILTERED counts (2026-09-30).

N1 kill (NIGHT_BURN_RECEIPT.md): "under 0.1% quote sampling with no base-rate
contrast". This script counts the FULL operator message pool, not selected
quotes. Zero API calls, zero spend, local bytes only.

Pools (instrument named per census-denominator law):
  - grok pool  : corpus/oral_history/seat_pools/grok_sessions/*/*/chat_history.jsonl (852 files)
  - codex pool : corpus/oral_history/seat_pools/codex_sessions/**/rollout-*.jsonl (193 files)

Extraction rules (cheap, stated):
  grok user turn  : keep <user_query> inner text; keep bare text (len>5, not '<'-tagged,
                    not 'This session is being continued' = system continuation blob);
                    drop tagged boilerplate (<user_info>/<system-reminder>/...) and tiny.
  codex user msg  : response_item/payload.message/role=user; keep bare text (len>5);
                    drop known env-tag prefixes (<environment_context> etc.) and md
                    context blobs ('# ', 'AGENTS').

Tone flags (case-insensitive regex; NOT mutually exclusive):
  P profanity  : fuck*|bullshit|shit*|damn*|bitch*|bastard*|crap*|piss*|asshole*|dickhead*
                 ('hell' excluded: catches 'hello'/'hell yes'; 'hell yes/yeah' sits in APPROVAL)
  A approval   : hah+|lol|lmao|lmfao|baller|badass|'bad ass'|'i love it'|'love it'|
                 'nice work'|'good work'|'great work'|'well done'|'good shit'|
                 'fuck yes/yeah'|'hell yes/yeah'|'stamp it'|spooky|beautiful|genius
  C correction : 'why are you'|'why is this'|'why do you'|'self steal'|
                 "isn't gonna fly"|'handwavy'|'hand wavy'|'wasting'|'impatient'|'slop'|
                 'stop asking'|'stop building'|'stop doing'|'stop running'|'stop.'|
                 "you're doing"|'you are doing'|'should have'|"shouldn't"|"didn't"|
                 'wrong'|'again?'|'no.'
  CAPS         : >=70% of alpha chars uppercase AND >=8 alpha chars (doc claims
                 ALL-CAPS = correction register)

Outputs (this directory):
  imp10_operator_pool.jsonl  every counted message (pool, session, class, flags, text)
  imp10_operator_counts.json the counts the V2 doc re-bases on
  imp10_audit_sample.json    seeded stratified sample for manual error-bar audit
"""
import glob, json, os, random, re
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
POOL_OUT = os.path.join(HERE, 'imp10_operator_pool.jsonl')
COUNTS_OUT = os.path.join(HERE, 'imp10_operator_counts.json')
AUDIT_OUT = os.path.join(HERE, 'imp10_audit_sample.json')

# Tone-pool length cap. Evidence (first run of this script): keyword flags fire on
# PASTED TRANSCRIPTS, not operator chat lines -- the P-and-A-and-C cell was 90 rows
# with median length 80,905 chars (NACHO MASK drafting blobs quoting X posts).
# Flag rate by length bucket: <=100 chars A=1.8% vs >1000 chars A=15.3%. Tone base
# rates are therefore computed on messages <= TONE_CAP chars (both caps reported).
TONE_CAPS = (300, 1000)

GROK_GLOB = 'corpus/oral_history/seat_pools/grok_sessions/*/*/chat_history.jsonl'
CODEX_GLOB = 'corpus/oral_history/seat_pools/codex_sessions/**/rollout-*.jsonl'

RE_USER_QUERY = re.compile(r'<user_query>(.*?)</user_query>', re.S)
RE_DATE = re.compile(r"Today's date: (\d{4}-\d{2}-\d{2})")

RE_P = re.compile(r"\b(fuck\w*|bullshit|shit\w*|damn\w*|bitch\w*|bastard\w*|crap\w*|piss\w*|asshole\w*|dickhead\w*)\b", re.I)
RE_A = re.compile(r"(\b(?:hah+|lol|lmao|lmfao|baller|badass|spooky|beautiful|genius)\b|bad ass|i love it|love it|nice work|good work|great work|well done|good shit|fuck (?:yes|yeah)|hell (?:yes|yeah)|stamp it)", re.I)
RE_C = re.compile(r"(why are you|why is this|why do you|self steal|isn't gonna fly|is not gonna fly|handwavy|hand wavy|wasting|impatient|slop|stop asking|stop building|stop doing|stop running|stop\.|you're doing|you are doing|should have|shouldn't|didn't|wrong|again\?|no\.)", re.I)

GROK_DROPPED = Counter()
CODEX_DROPPED = Counter()


def flags(text):
    alpha = [c for c in text if c.isalpha()]
    caps = len(alpha) >= 8 and sum(c.isupper() for c in alpha) / len(alpha) >= 0.7
    return bool(RE_P.search(text)), bool(RE_A.search(text)), bool(RE_C.search(text)), caps


def grok_messages():
    for f in sorted(glob.glob(GROK_GLOB)):
        sid = os.path.basename(os.path.dirname(f))
        date = None
        try:
            lines = open(f, encoding='utf-8').read().splitlines()
        except Exception:
            GROK_DROPPED['file_err'] += 1
            continue
        for line in lines:
            try:
                o = json.loads(line)
            except Exception:
                GROK_DROPPED['parse_err'] += 1
                continue
            if o.get('type') != 'user':
                continue
            parts = o.get('content') or []
            txt = '\n'.join(p.get('text', '') for p in parts if isinstance(p, dict)).strip()
            if date is None:
                m = RE_DATE.search(txt)
                if m:
                    date = m.group(1)
            if not txt:
                GROK_DROPPED['empty'] += 1
            elif RE_USER_QUERY.search(txt):
                for q in RE_USER_QUERY.findall(txt):
                    yield ('grok', sid, date, 'user_query', q.strip())
            elif txt.startswith('This session is being continued'):
                GROK_DROPPED['continuation'] += 1
            elif txt.startswith('<'):
                GROK_DROPPED['tagged_boilerplate'] += 1
            elif len(txt) > 5:
                yield ('grok', sid, date, 'bare', txt)
            else:
                GROK_DROPPED['tiny'] += 1


CODEX_KNOWN = ('<environment_context>', '<recommended_plugins>', '<app-context>', '<system-reminder>',
               '<turn_context>', '<user_instructions>', '<permissions', '<collaboration_mode>',
               '<apps_instructions>', '<plugins_instructions>', '<skills_instructions>',
               '<multi_agent_mode>', '<env', '<user_info>',
               # added after first-run audit: auto-injected codex envelopes that reached the
               # bare path (51 rows); each declares itself system-supplied in its own text
               '<in-app-browser-context', '<turn_aborted', '<subagent_notification',
               '<realtime_delegation', '<external_codex_apps_writing_block_edits',
               '<send_user_message_question_reply')


def codex_messages():
    for f in sorted(glob.glob(CODEX_GLOB, recursive=True)):
        m = re.search(r'rollout-(\d{4}-\d{2}-\d{2})', os.path.basename(f))
        date = m.group(1) if m else None
        for line in open(f, encoding='utf-8'):
            try:
                o = json.loads(line)
            except Exception:
                CODEX_DROPPED['parse_err'] += 1
                continue
            if o.get('type') != 'response_item':
                continue
            p = o.get('payload') or {}
            if p.get('type') != 'message' or p.get('role') != 'user':
                continue
            txt = '\n'.join(c.get('text', '') for c in (p.get('content') or []) if isinstance(c, dict)).strip()
            if not txt:
                CODEX_DROPPED['empty'] += 1
            elif txt.startswith('# ') or txt.startswith('AGENTS'):
                CODEX_DROPPED['md_context'] += 1
            elif any(txt.startswith(k) for k in CODEX_KNOWN):
                CODEX_DROPPED['tagged_boilerplate'] += 1
            elif len(txt) > 5:
                yield ('codex', os.path.basename(f), date, 'bare', txt)
            else:
                CODEX_DROPPED['tiny'] += 1


def main():
    all_msgs = list(grok_messages()) + list(codex_messages())
    joint = Counter()
    per_pool = Counter()
    dates = []
    rows_dump = []
    with open(POOL_OUT, 'w', encoding='utf-8') as out:
        for i, (pool, sid, date, cls, text) in enumerate(all_msgs):
            p, a, c, caps = flags(text)
            row = dict(i=i, pool=pool, session=sid, cls=cls, date=date,
                       P=p, A=a, C=c, CAPS=caps, text=text)
            rows_dump.append(row)
            out.write(json.dumps(row, ensure_ascii=False) + '\n')
            per_pool[pool] += 1
            joint[(pool, p, a, c)] += 1
            if caps:
                joint[(pool, p, a, c, 'CAPS')] += 1
            if date:
                dates.append((date, pool))

    def cnt(pool=None, p=None, a=None, c=None, caps=None):
        # len-5 keys are the CAPS overlay rows: only counted when caps=True is asked
        n = 0
        for key, v in joint.items():
            if caps is None and len(key) == 5:
                continue
            if caps is True and (len(key) < 5 or key[4] != 'CAPS'):
                continue
            pl, pp, aa, cc = key[:4]
            if pool is not None and pl != pool: continue
            if p is not None and pp != p: continue
            if a is not None and aa != a: continue
            if c is not None and cc != c: continue
            n += v
        return n

    counts = {
        'M_total': len(all_msgs),
        'per_pool': dict(per_pool),
        'grok_dropped': dict(GROK_DROPPED),
        'codex_dropped': dict(CODEX_DROPPED),
        'grok_sessions_counted': len({m[1] for m in all_msgs if m[0] == 'grok'}),
        'codex_files_counted': len({m[1] for m in all_msgs if m[0] == 'codex'}),
    }
    for label, pool in (('rates_all', None), ('rates_grok', 'grok'), ('rates_codex', 'codex')):
        counts[label] = {
            'M': cnt(pool=pool),
            'P_any': cnt(pool=pool, p=True), 'A_any': cnt(pool=pool, a=True), 'C_any': cnt(pool=pool, c=True),
            'P_and_C': cnt(pool=pool, p=True, c=True), 'P_and_A': cnt(pool=pool, p=True, a=True),
            'A_and_C': cnt(pool=pool, a=True, c=True),
            'A_only': cnt(pool=pool, a=True, p=False, c=False),
            'C_only': cnt(pool=pool, c=True, p=False, a=False),
            'P_only': cnt(pool=pool, p=True, a=False, c=False),
            'none': cnt(pool=pool, p=False, a=False, c=False),
            'CAPS': cnt(pool=pool, caps=True),
        }

    # 8-cell joint + tone pools under each length cap (the honest base rates)
    joint8 = Counter()
    for r_rows in rows_dump:
        joint8[(r_rows['P'], r_rows['A'], r_rows['C'])] += 1
    counts['joint8_uncapped'] = {''.join(('P' if p else '-') + ('A' if a else '-') + ('C' if c else '-')): v
                                 for (p, a, c), v in sorted(joint8.items(), key=lambda x: -x[1])}
    for cap in TONE_CAPS:
        tone = [r for r in rows_dump if len(r['text']) <= cap]
        t = Counter()
        for r in tone:
            t[(r['P'], r['A'], r['C'])] += 1
        n = len(tone)
        counts[f'tone_cap_{cap}'] = {
            'M': n,
            'P': sum(v for (p, a, c), v in t.items() if p),
            'A': sum(v for (p, a, c), v in t.items() if a),
            'C': sum(v for (p, a, c), v in t.items() if c),
            'P_and_C': sum(v for (p, a, c), v in t.items() if p and c),
            'P_and_A': sum(v for (p, a, c), v in t.items() if p and a),
            'A_and_C': sum(v for (p, a, c), v in t.items() if a and c),
            'A_only': t[(False, True, False)],
            'C_only': t[(False, False, True)],
            'P_only': t[(True, False, False)],
            'none': t[(False, False, False)],
            'CAPS': sum(1 for r in tone if r['CAPS']),
        }
    if dates:
        ds = sorted(dates)
        counts['date_range'] = {'min': ds[0][0], 'max': ds[-1][0], 'dated_msgs': len(dates)}

    # duplicate structure: the pools carry fleet cron templates (top one sent 591x),
    # so tone base rates are ALSO computed on unique texts
    from collections import Counter as _C
    text_ct = _C(r['text'] for r in rows_dump)
    counts['duplicate_structure'] = {
        'rows': len(rows_dump), 'unique_texts': len(text_ct),
        'dup_extra_rows': sum(v - 1 for v in text_ct.values() if v > 1),
        'top_template_copies': text_ct.most_common(1)[0][1],
        'top_template_head': text_ct.most_common(1)[0][0][:80],
    }
    seen = set()
    uniq_rows = []
    for r in rows_dump:
        if r['text'] in seen:
            continue
        seen.add(r['text'])
        uniq_rows.append(r)
    counts['joint8_uncapped_unique'] = {
        ''.join(('P' if p else '-') + ('A' if a else '-') + ('C' if c else '-')): v
        for (p, a, c), v in sorted(_C((r['P'], r['A'], r['C']) for r in uniq_rows).items(), key=lambda x: -x[1])
    }
    for cap in TONE_CAPS:
        tone = [r for r in uniq_rows if len(r['text']) <= cap]
        t = _C((r['P'], r['A'], r['C']) for r in tone)
        counts[f'tone_cap_{cap}_unique'] = {
            'M': len(tone),
            'P': sum(v for (p, a, c), v in t.items() if p),
            'A': sum(v for (p, a, c), v in t.items() if a),
            'C': sum(v for (p, a, c), v in t.items() if c),
            'P_and_C': sum(v for (p, a, c), v in t.items() if p and c),
            'P_and_A': sum(v for (p, a, c), v in t.items() if p and a),
            'A_and_C': sum(v for (p, a, c), v in t.items() if a and c),
            'A_only': t[(False, True, False)], 'C_only': t[(False, False, True)],
            'P_only': t[(True, False, False)], 'none': t[(False, False, False)],
            'CAPS': sum(1 for r in tone if r['CAPS']),
        }

    # seeded stratified audit sample: 15 per flag-class (A / C-only / P-only / neutral)
    rng = random.Random(20260930)
    audit = {}
    for k in ('A', 'C', 'P', 'N'):
        cand = []
        for i, m in enumerate(all_msgs):
            p, a, c, _ = flags(m[4])
            if k == 'A' and a: cand.append(i)
            elif k == 'C' and c and not a: cand.append(i)
            elif k == 'P' and p and not a and not c: cand.append(i)
            elif k == 'N' and not p and not a and not c: cand.append(i)
        idxs = rng.sample(cand, min(15, len(cand)))
        audit[k] = {'pool_size': len(cand),
                    'sample': [dict(i=i, pool=all_msgs[i][0], text=all_msgs[i][4][:280]) for i in idxs]}
    counts['audit_sample_sizes'] = {k: v['pool_size'] for k, v in audit.items()}

    with open(COUNTS_OUT, 'w', encoding='utf-8') as fh:
        json.dump(counts, fh, indent=1)
    with open(AUDIT_OUT, 'w', encoding='utf-8') as fh:
        json.dump(audit, fh, indent=1, ensure_ascii=False)
    print(json.dumps(counts, indent=1))


if __name__ == '__main__':
    main()
