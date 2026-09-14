"""Audit test: ensure callers do not discard the return value of
_translate_model_name_for_response (it returns a shallow copy; callers must
use the return to avoid leaking internal routing keys).

Evidence: tests/test_litellm/proxy/proxy_server/test_team_model_name_translation.py
warns callers: "callers MUST use the return value -- the /v1/model/info list
path historically discarded it, leaking the internal routing key (#28382)."

This test parses repository .py files (under mine/raw and repo root) and fails
if it finds expression statements that call the translate function without
assignment (i.e. the call is an Expr node in the AST)."""

from pathlib import Path
import ast

REPO_ROOT = Path(__file__).resolve().parents[3]
SEARCH_DIRS = [REPO_ROOT / 'mine', REPO_ROOT]
TARGET_NAME = '_translate_model_name_for_response'


def _py_files(paths):
    seen = set()
    for base in paths:
        for p in base.rglob('*.py'):
            # skip typical virtualenv site-packages under .venv to reduce noise
            if '.venv' in p.parts:
                continue
            if p.resolve() in seen:
                continue
            seen.add(p.resolve())
            yield p


def test_no_discarded_translate_calls():
    offenders = []
    for p in _py_files(SEARCH_DIRS):
        try:
            src = p.read_text(encoding='utf-8')
        except Exception:
            continue
        try:
            tree = ast.parse(src)
        except Exception:
            # skip files that don't parse
            continue
        for node in ast.walk(tree):
            # expression statements like: _translate_model_name_for_response(x)
            if isinstance(node, ast.Expr) and isinstance(node.value, ast.Call):
                func = node.value.func
                name = None
                if isinstance(func, ast.Name):
                    name = func.id
                elif isinstance(func, ast.Attribute):
                    name = func.attr
                if name == TARGET_NAME:
                    offenders.append((str(p), node.lineno))
    assert not offenders, (
        "Found calls to _translate_model_name_for_response used as bare expression (return discarded).\n"
        + "Offenders:\n"
        + "\n".join(f"{f}:{l}" for f, l in offenders)
    )
