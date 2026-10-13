"""Lane X2 mechanical graders for the four unique asks.

Ground truth + checks, all byte-based:
- glm: extract path tokens from the frozen census per Row section, dedup bare
  paths; grade SHAPE / LISTS-APPEAR / NO-EM-DASH / SELF-TOTAL / RECALL-90.
- kimi: parse PROMOTE/CONTRADICTION lines; ROWS-IN-RANGE / DISTINCT / em-dash.
- sonnet: battery 5 checks + KNOWN-EXCLUDED.
- fable: battery 5 checks (B1 retry comparability).

Throwaway grading script for the lane receipt (delete after landing).
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MG = ROOT / 'watch' / 'inbox' / 'model_garden'

PATH_RE = re.compile(
    r'[A-Za-z0-9_.\-/{},]+\.(?:py|mjs|ps1|jsonl|json|md|yaml|yml|cmd|log|txt|sh|js|ts)\b')


def canon(text):
    """Canonicalize: squeeze whitespace inside brace groups (the census spells
  one register-task family as a multiline brace expansion)."""
    return re.sub(r'\{[^{}]*\}',
                  lambda m: re.sub(r'\s+', '', m.group(0)), text)


def collapse_suffixes(paths):
    """A bare-name token that is a path-suffix of a longer token is the same
  surface (server.py and server/server.py are one file)."""
    longer = {p for p in paths if '/' in p}
    out = set()
    for p in paths:
        if '/' in p:
            out.add(p)
            continue
        if any(q == p or q.endswith('/' + p) for q in longer):
            # keep it only if no full-path form exists
            if not any(q.endswith('/' + p) for q in longer):
                out.add(p)
        else:
            out.add(p)
    return out


def census_ground_truth():
    """(rows: row_num -> set(bare_path), all_paths: set) from the frozen census."""
    text = canon((MG / 'X2_material_wiring_census_frozen.md').read_text(
        encoding='utf-8'))
    sections = re.split(r'^### ', text, flags=re.M)
    rows = {}
    for sec in sections[1:]:
        m = re.match(r'Row (\d+)\.', sec)
        if not m:
            continue
        n = int(m.group(1))
        rows[n] = collapse_suffixes(set(PATH_RE.findall(sec)))
    all_paths = collapse_suffixes(set().union(*rows.values()) if rows else set())
    return rows, all_paths


def strip_md_meta(paths):
    """Drop markdown/url noise tokens that are not repo surfaces."""
    drop = ('https://', 'http://', 'census.wiring')
    return {p for p in paths if not p.startswith(drop) and '://' not in p
            and not p.endswith('.wiring')}


def grade_glm():
    out = (MG / 'garden-v1-unique-glm.md').read_text(encoding='utf-8')
    rows_map, gt_all = census_ground_truth()
    gt = strip_md_meta(gt_all)
    checks = {}

    # SHAPE: header row, then table rows, then exactly the two final lines
    lines = [l for l in out.splitlines() if l.strip()]
    body = [l for l in lines if not l.startswith('# ')]
    final = [l for l in body if l.startswith(('TOTAL-SURFACES:', 'CENSUS-ROWS-READ:'))]
    table = [l for l in body if l.startswith('|')]
    checks['SHAPE'] = int(
        len(final) == 2 and len(table) >= 3
        and table[1].replace(' ', '') == '|---|---|---|'
        and body[0].replace(' ', '') == '|surface|rows|kind|'
        and len([l for l in body if not l.startswith('|')
                 and not l.startswith(('TOTAL-', 'CENSUS-'))]) == 0)

    listed = []
    for row in table[2:]:
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        if len(cells) >= 1 and cells[0]:
            listed.append(canon(cells[0]))
    census_norm = canon((MG / 'X2_material_wiring_census_frozen.md').read_text(
        encoding='utf-8'))
    checks['LISTS-APPEAR'] = int(all(s in census_norm for s in listed))

    checks['NO-EM-DASH'] = int(out.count('\u2014') == 0)

    checks['SELF-TOTAL'] = int(
        final and final[0].split(':', 1)[1].strip() == str(len(listed)))

    covered = {s for s in listed if s in gt}
    checks['RECALL-90'] = int(len(gt) and len(covered) / len(gt) >= 0.90)

    # rows-column sanity vs ground truth (diagnostic, not a check)
    rows_ok = 0
    for row in table[2:]:
        cells = [c.strip() for c in row.strip().strip('|').split('|')]
        if len(cells) < 2:
            continue
        claimed = [int(x) for x in re.findall(r'\d+', cells[1])]
        true_rows = {n for n, ps in rows_map.items() if cells[0] in ps}
        if claimed and set(claimed) == true_rows:
            rows_ok += 1
    return checks, {'gt_count': len(gt), 'listed': len(listed),
                    'covered': len(covered), 'missing': sorted(gt - covered),
                    'invented': sorted(set(listed) - gt - set(gt_all)),
                    'rows_col_exact': rows_ok, 'rows_total': len(listed),
                    'gt': sorted(gt)}


def grade_kimi():
    out = (MG / 'garden-v1-unique-kimi.md').read_text(encoding='utf-8')
    reg_lines = (MG / 'X2_stealth_findings_frozen.jsonl').read_text(
        encoding='utf-8').splitlines()
    n_rows = len(reg_lines)
    checks = {}
    promotes = re.findall(r'^PROMOTE (\d+):', out, flags=re.M)
    contras = re.findall(r'^CONTRADICTION (\d+):', out, flags=re.M)
    other = [l for l in out.splitlines() if l.strip() and not l.startswith('#')
             and not re.match(r'^(PROMOTE|CONTRADICTION) \d+:', l)]
    checks['SHAPE'] = int(promotes == [str(i) for i in range(1, 11)]
                          and contras == ['1', '2', '3'] and not other)
    row_cites = [int(m.group(1)) for m in re.finditer(r'\| ROW: (\d+)', out)]
    pair_cites = []
    for m in re.finditer(r'\| ROWS: (\d+), (\d+)', out):
        pair_cites += [int(m.group(1)), int(m.group(2))]
    all_cites = row_cites + pair_cites
    checks['ROWS-IN-RANGE'] = int(bool(all_cites) and all(
        1 <= c <= n_rows for c in all_cites))
    checks['DISTINCT-ROWS'] = int(len(set(row_cites)) == 10 and len(row_cites) == 10)
    checks['NO-EM-DASH'] = int(out.count('\u2014') == 0)
    return checks, {'n_rows': n_rows, 'row_cites': row_cites,
                    'pair_cites': pair_cites}


def grade_review(out_path, frozen_paths):
    """The battery B1-B5 five checks over one review reply."""
    out = (MG / out_path).read_text(encoding='utf-8')
    body = '\n'.join(l for l in out.splitlines() if not l.startswith('# '))
    checks = {}
    imps = re.findall(r'^IMPROVEMENT (\d+):', body, flags=re.M)
    db = re.findall(r'^DIFFERENT-BUILD:', body, flags=re.M)
    other = [l for l in body.splitlines() if l.strip() and not l.startswith('#')
             and not re.match(r'^(IMPROVEMENT \d+:|DIFFERENT-BUILD:)', l)]
    checks['SHAPE'] = int(imps == ['1', '2', '3'] and len(db) == 1 and not other)
    cites = re.findall(r'EVIDENCE: `?([^\s|`]+)', body)
    line_ok, resolve_ok, buckets = True, True, []
    for cite in cites:
        path, _, ln = cite.rpartition(':')
        nums = [int(x) for x in re.findall(r'\d+', ln)] if ln else []
        p = ROOT / path
        if not p.is_file():
            resolve_ok = False
            continue
        lc = len(p.read_text(encoding='utf-8', errors='replace').splitlines())
        for n in nums:
            if not (1 <= n <= lc):
                line_ok = False
        for n in (nums or [1]):
            buckets.append((path, min(frozen_paths), (n - 1) // 50
                            if path in frozen_paths else None))
    checks['CITES-RESOLVE'] = int(resolve_ok and bool(cites))
    checks['LINES-IN-RANGE'] = int(line_ok)
    checks['NO-EM-DASH'] = int(out.count('\u2014') == 0)
    keys = {(p, (min(ns) - 1) // 50) for p, ns in
            [(c.rpartition(':')[0],
              [int(x) for x in re.findall(r'\d+', c.rpartition(':')[2])] or [1])
             for c in cites]}
    checks['DISTINCT-EVIDENCE'] = int(len(keys) >= 2)
    return checks, {'cites': cites}


if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'glm'
    if which == 'glm':
        checks, diag = grade_glm()
        print('GLM checks:', json.dumps(checks))
        print('diag:', json.dumps({k: v for k, v in diag.items()
                                   if k != 'gt'}, indent=1))
        print('score', sum(checks.values()), '/', len(checks))
    elif which == 'kimi':
        checks, diag = grade_kimi()
        print('KIMI checks:', json.dumps(checks))
        print('diag:', json.dumps(diag))
        print('score', sum(checks.values()), '/', len(checks))
    elif which in ('sonnet', 'fable'):
        checks, diag = grade_review(
            f'garden-v1-unique-{which}.md',
            {'watch/inbox/model_garden/X2_material_rooms_frozen.py',
             'watch/inbox/model_garden/X2_material_room_frozen.py'}
            if which == 'sonnet' else
            {'watch/inbox/model_garden/X2_material_hermes_burn_frozen.py'})
        print(which.upper(), 'checks:', json.dumps(checks))
        print('diag:', json.dumps(diag))
        print('score', sum(checks.values()), '/', len(checks))
