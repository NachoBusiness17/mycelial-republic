"""B2-251 checkbox truth audit: queue edit pass 2.

Second sweep against live bytes after concurrent writers re-checked rows
mid-audit: flips the re-checked and newly pre-checked receipt-less rows,
attaches this lane's own landing receipt pointer to the B2-251 row, and
self-feeds two unchecked briefs. Unique-prefix keyed, aborts without writing
on any key anomaly. Append-only on row text.
"""
import re
import sys

QUEUE = 'watch/inbox/burn_wave_20260926/QUEUE.md'
RECEIPT = 'watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md'

FLIP_NOTE = (
    ' (2026-09-26 B2-251 checkbox audit, second pass: [x] flipped to [ ],'
    ' no resolvable landing receipt on disk; no bytes erased, prior checked'
    ' state recorded in ' + RECEIPT + ')'
)

# (unique row key, extra honesty clause or '')
FLIPS = [
    ('- [x] B2-247 Reconcile collected-files vs disk-candidates gap',
     ' re-checked [x] over this audit\u2019s first-pass flip by a concurrent'
     ' writer with no receipt filed'),
    ('- [x] B2-214 Dungeon lore census fossil',
     ' the fossil is still on disk at'
     ' memory/game_modules/audit_dungeon.v1.json:147'),
    ('- [x] B2-73 Secret-scan estate pass', ''),
    ('- [x] B2-74 QLoRA recipe from real sources', ''),
    ('- [x] B2-75 G', ''),
    ('- [x] B2-76 Catalog v3 junction policy draft', ''),
    ('- [x] B2-77 Driver v2 resilience spec', ''),
    ('- [x] B2-279 Fold event sort is non-transitive',
     ' no landing receipt on disk; comparator code sits at'
     ' scripts/index_fold_host.mjs compareBySeqTs'),
    ('- [x] B2-280 Retire the 2^53 inexact seq band',
     ' no landing receipt on disk; MAX_SAFE_SEQ handling sits at'
     ' scripts/index_fold_host.mjs:172-204'),
]

B251_POINTER = (
    ' Landed 2026-09-26 by the row\u2019s own lane: 7+9 rows flipped unearned,'
    ' 71 receipt pointers attached, falsifier re-run clean on post-edit bytes;'
    ' receipt watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md.'
)


def main():
    with open(QUEUE, encoding='utf-8', newline='') as f:
        raw = f.read()
    lines = raw.split('\n')

    # highest existing lane number, for the self-feed ids
    nums = [int(m.group(1)) for l in lines
            for m in [re.search(r'B2-(\d+)', l)] if m]
    highest = max(nums)
    s1 = highest + 1
    s2 = highest + 2

    brief1 = (
        f'- [ ] B2-{s1} Checkbox-receipt gate on the queue: (self-fed by'
        f' B2-251) the B2-251 audit proved a checked Open row mutes the'
        f' dispatcher refill denominator with no trace, and the sweep itself'
        f' was hand-run, so turn it into a standing check: extend'
        f' mag.shared_surface validate (or a tools/ checker wired beside it)'
        f' so a checked Open row in'
        f' watch/inbox/burn_wave_20260926/QUEUE.md that names no receipt path'
        f' resolving on disk fails as NEW debt, with the B2-251-attached rows'
        f' accepted as the named baseline keyed on the attachment marker;'
        f' falsifier: append a checked row with no resolvable receipt pointer'
        f' and validate must fail naming it, today it passes; pointers'
        f' watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md,'
        f' watch/inbox/burn_wave_20260926/B2_251_queue_edit.py,'
        f' mag/shared_surface.py validate.'
    )
    brief2 = (
        f'- [ ] B2-{s2} Audit-attached receipt verification pass: (self-fed by'
        f' B2-251) the B2-251 audit attached receipt pointers to 71 landed'
        f' rows by lane-id plus receipt-title subject match (title + Verdict'
        f' heading), which is weaker evidence than the B2-238 law\u2019s'
        f' landing-lane flip; an independent pass re-reads each of the 71'
        f' attached pointers, checks the receipt\u2019s Verdict and Falsifier'
        f' actually claim the row\u2019s brief rather than merely sharing the'
        f' lane id, and files per-row confirm or erratum, flipping any row'
        f' whose receipt claims different work; falsifier: an attached pointer'
        f' whose receipt Verdict names a different brief\u2019s subject'
        f' survives the pass; pointers'
        f' watch/inbox/burn_wave_20260926/B2_251_checkbox_audit_20260926.md'
        f' Work done 3, watch/inbox/burn_wave_20260926/B2_251_audit_probe.py.'
    )

    actions = []
    abort = []

    def find_rows(prefix):
        return [i for i, l in enumerate(lines) if l.startswith(prefix)]

    for key, extra in FLIPS:
        hits = find_rows(key)
        if len(hits) != 1:
            abort.append(f'FLIP key matched {len(hits)} lines: {key}')
            continue
        i = hits[0]
        clause = FLIP_NOTE
        if extra:
            clause = clause[:-1] + ';' + extra + ')'
        lines[i] = '- [ ]' + lines[i][5:] + clause
        actions.append(f'FLIP line {i+1}: {key[7:60]}')

    # this lane earns its own row: attach the landing receipt pointer
    key = '- [x] B2-251 Open checkbox truth audit'
    hits = find_rows(key)
    if len(hits) != 1:
        abort.append(f'B2-251 key matched {len(hits)} lines')
    else:
        i = hits[0]
        lines[i] = lines[i] + ' ' + B251_POINTER
        actions.append(f'ATTACH own receipt pointer, line {i+1}')

    # self-feed 2 briefs, UNCHECKED, at the Open tail (end of file)
    tail = len(lines)
    while tail > 0 and lines[tail - 1].strip() == '':
        tail -= 1
    lines.insert(tail, brief1)
    lines.insert(tail + 1, brief2)
    actions.append(f'SELF-FEED B2-{s1} and B2-{s2} unchecked at Open tail')

    if abort:
        print('ABORT, no bytes written:')
        for a in abort:
            print('  ' + a)
        sys.exit(2)

    with open(QUEUE, 'w', encoding='utf-8', newline='') as f:
        f.write('\n'.join(lines))
    for a in actions:
        print(a)
    print(f'self-feed ids: B2-{s1}, B2-{s2} (highest was B2-{highest})')


if __name__ == '__main__':
    main()
