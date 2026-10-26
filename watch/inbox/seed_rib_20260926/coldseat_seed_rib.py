"""Cold-seat falsifier for the landed seed-rib tree (card seedrib, 2026-09-26).

The burn-plan gate: nothing ships until a cold agent rebuilds a subtree from
kilobytes. This administers the knowledge join: a genuinely cold model (local
Ollama, zero context outside this prompt) receives ONLY the files the tree's
own SEED_RIB.md cold-join prescribes (SEED_RIB.md + the six kernel prose
sections, in join order) and must answer the four kernel questions.

The harness adds no repo knowledge to the prompt: it concatenates tree files
verbatim. The four questions and the grading keys are the falsifier
instrument, authored here, grounded in what the kernel sections actually say.

Usage: .venv/Scripts/python.exe coldseat_seed_rib.py <model> [<model> ...]
Writes: coldseat_prompt.txt (exact prompt bytes), coldseat_<model>.out (raw
model answer with header), prints per-question PASS/FAIL, exit 0 on 4/4.
"""
from __future__ import annotations

import re
import subprocess
import sys
import time
from pathlib import Path

REPO = Path('.').resolve()
TREE = REPO / 'watch/inbox/seed_rib_20260926/seed-rib'
HOME = TREE.parent

# The join, exactly as SEED_RIB.md cold-join step 1 prescribes it.
JOIN = ['SEED_RIB.md',
        'kernel/thesis.card.md', 'kernel/state.now.md', 'kernel/env.law.md',
        'kernel/load.order.md', 'kernel/tier.law.md', 'kernel/filing.law.md']

QUESTIONS = """=== QUESTIONS (answer from the documentation above only) ===
Q1. Which Python interpreter or launcher command must an agent in this fleet
use, and which must it never use?
Q2. In what order should a newly booted agent read this fleet's files? Name
the first files in order.
Q3. Where must durable work products be filed, and what must accompany them?
Q4. What is the standing thesis or current objective this fleet is climbing?
"""

# Grading keys: (primary set, secondary set). PASS = at least one primary hit
# AND at least one secondary hit (Q4: at least two distinct key hits).
# Key sets name the forms the tree ITSELF documents:
# - Q1 'use' half: the env law names mag.cmd OR .venv\Scripts\python.exe;
#   'never' half: the env law says "never bare python on PATH (Hermes)" and
#   cold answers paraphrase it ('forbids', 'never use bare'), so the secondary
#   set accepts the documented paraphrases, not one literal string.
# - Q2 has TWO documented correct answers: the load.order table (row 1
#   FRAMEWORK_LOAD) and the SEED_RIB.md cold-join step 1 kernel order
#   (thesis.card first). Both are primary.
# First administration (2026-09-26, raw on file) graded qwen Q1 FAIL on a
# backtick splitting 'bare `python`' and qwen Q2 FAIL for answering the
# kernel order; both were key artifacts, fixed here.
KEYS = {
    'Q1': (['.venv', 'mag.cmd', 'scripts\\python.exe', 'scripts/python.exe'],
           ['never bare', 'not bare', 'no bare', 'bare python', 'hermes',
            'forbid', 'never use', 'must not']),
    'Q2': (['framework_load', 'thesis.card'],
           ['first_boot', 'the_method', 'compass', 'kernel', 'load.order',
            'state.now', 'env.law']),
    'Q3': (['watch/inbox'],
           ['receipt', 'index_events', 'register', 'index']),
    'Q4': (['standing thesis', 'frontier', 'cheap agents', 'orchestrat',
            'scoreboard', 'frontier-from-flash', 'estate atlas',
            'current climb'], []),
}

ANSI = re.compile(r'\x1b\[[0-9;?]*[A-Za-z]|\x1b\][^\x07]*\x07|\x1b[=>]')


def clean_for_grading(text: str) -> str:
    """Strip ollama CLI transport noise (ANSI spinner/cursor escapes, wrap
    artifacts) for MATCHING only; raw outputs stay untouched on disk."""
    return ANSI.sub('', text).replace('`', ' ').replace('\r', '')


def build_prompt() -> str:
    parts = ['You are a cold agent. Below is the ENTIRE documentation you '
             'have: the files of a seed directory, concatenated in the order '
             'the directory\'s own SEED_RIB.md prescribes for a cold join. '
             'Answer the four questions at the end using ONLY this '
             'documentation. If the documentation does not answer a question, '
             'say exactly that.\n']
    for rel in JOIN:
        body = (TREE / rel).read_text(encoding='utf-8')
        parts.append(f'\n=== FILE: {rel} ===\n{body}\n')
    parts.append('\n' + QUESTIONS)
    return ''.join(parts)


def grade(answer: str) -> list[tuple[str, bool, str]]:
    low = clean_for_grading(answer).lower()
    out = []
    for q, (primary, secondary) in KEYS.items():
        p_hits = sorted({k for k in primary if k in low})
        s_hits = sorted({k for k in secondary if k in low})
        if q == 'Q4':
            ok, detail = len(p_hits) >= 2, f'key hits {p_hits}'
        else:
            ok = bool(p_hits) and bool(s_hits)
            detail = f'primary {p_hits} secondary {s_hits}'
        out.append((q, ok, detail))
    return out


def run_cold(model: str, prompt: str) -> str:
    t0 = time.time()
    r = subprocess.run(['ollama', 'run', model], input=prompt,
                       capture_output=True, text=True, timeout=420)
    dt = time.time() - t0
    stamp = time.strftime('%Y%m%dT%H%M%SZ', time.gmtime())
    header = (f'# cold-seat run: model={model} exit={r.returncode} '
              f'duration={dt:.1f}s stamp={stamp}\n'
              f'# prompt bytes: {len(prompt.encode("utf-8"))} '
              f'(prompt saved verbatim in coldseat_prompt.txt)\n')
    raw = header + (r.stdout or '') + ('\n# stderr: ' + r.stderr if r.stderr.strip() else '')
    safe = model.replace(':', '_').replace('/', '_')
    (HOME / f'coldseat_{safe}_{stamp}.out').write_text(raw, encoding='utf-8')
    return r.stdout or '', dt


def main() -> int:
    models = sys.argv[1:] or ['gemma:2b']
    prompt = build_prompt()
    (HOME / 'coldseat_prompt.txt').write_text(prompt, encoding='utf-8')
    print(f'prompt: {len(prompt.encode("utf-8"))} bytes from {len(JOIN)} tree '
          f'files (join order per SEED_RIB.md): {", ".join(JOIN)}')
    all_ok = True
    for model in models:
        answer, dt = run_cold(model, prompt)
        print(f'\n=== {model} ({dt:.1f}s) ===')
        if not answer.strip():
            print('NO OUTPUT (see raw file)')
            all_ok = False
            continue
        graded = grade(answer)
        for q, ok, detail in graded:
            print(f"[{'PASS' if ok else 'FAIL'}] {q}: {detail}")
            all_ok = all_ok and ok
    print(f'\ncold-seat verdict: {"4/4 on every model" if all_ok else "MISS on at least one question"}')
    return 0 if all_ok else 1


if __name__ == '__main__':
    raise SystemExit(main())
