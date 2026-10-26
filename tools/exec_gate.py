"""L1 pre-exec static path gate for the shell door (tools/code_execution.py).

Port-order lane P4 (2026-10-07, watch/inbox/port_wave_20261007/p4_shell_door.md).
Parses the snippet AST before any process exists, resolves + normalizes every
literal path used in a write-capable call, and flags absolute paths outside the
owned run root. This is the layer that catches the original exploit class (the
2026-10-07 steal probe: open() with a variable-bound literal absolute path, the
five-pattern substring ban structurally blind to it). Computed paths are
intentionally NOT covered here: they are L4's job (canary + audit walk) and the
L3 job caps; pretending this gate sees them would be the fallback-branch creep
the build discipline bans.
"""
from __future__ import annotations

import ast
import os
from pathlib import Path
from typing import Optional

# dotted name -> which positional args carry paths that get written/moved
_WRITE_CALLS = {
    "os.open": (0,), "os.mkdir": (0,), "os.makedirs": (0,), "os.remove": (0,),
    "os.unlink": (0,), "os.rename": (0, 1), "os.replace": (0, 1),
    "os.rmdir": (0,), "os.truncate": (0,), "os.link": (0, 1), "os.symlink": (0, 1),
    "shutil.copy": (0, 1), "shutil.copy2": (0, 1), "shutil.copyfile": (0, 1),
    "shutil.copytree": (0, 1), "shutil.move": (0, 1),
}
_METHOD_WRITES = {
    # obj.method -> writes through the object (Path instances etc.); the write
    # TARGET is the receiver's constructor argument, not the method payload.
    "write_text", "write_bytes", "mkdir", "touch", "unlink", "rmdir",
    "rename", "replace", "symlink_to", "hardlink_to",
}


def normalized(p: str) -> str:
    """Resolve + normalize a candidate path (junctions/symlinks resolved)."""
    return os.path.normcase(os.path.realpath(os.path.normpath(os.path.abspath(p))))


# Backwards-compatible alias for the private name the door module historically
# used at split time.
_normalized = normalized


def _literal_str(node: ast.AST, env: Optional[dict] = None,
                 max_depth: int = 6) -> Optional[str]:
    """Evaluate an AST node that is statically a plain string.

    Covers Constant str, JoinedStr with all-Constant parts, BinOp Add of two
    literals, os.path.join(...) calls with all-literal parts, and names bound
    by a single literal assignment (env). Anything computed (reassigned or
    non-literal-bound names, format args, Path("/") / "x") is intentionally
    NOT covered: computed paths are L4's job, not this gate's.
    """
    if max_depth <= 0:
        return None
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.Name):
        if env is None:
            return None
        val = env.get(node.id)
        return val if isinstance(val, str) else None
    if isinstance(node, ast.JoinedStr):
        parts = []
        for v in node.values:
            if isinstance(v, ast.Constant) and isinstance(v.value, str):
                parts.append(v.value)
            else:
                return None
        return "".join(parts)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal_str(node.left, env, max_depth - 1)
        right = _literal_str(node.right, env, max_depth - 1)
        if left is not None and right is not None:
            return left + right
    if isinstance(node, ast.Call):
        func = node.func
        fname = None
        if isinstance(func, ast.Name):
            fname = func.id
        elif isinstance(func, ast.Attribute):
            fname = func.attr
        if fname == "join":
            parts = [_literal_str(a, env, max_depth - 1) for a in node.args]
            if parts and all(p is not None for p in parts):
                return os.path.join(*parts)
    return None


def _const_env(tree: ast.AST) -> dict:
    """Single-binding constant table: names assigned exactly one literal string
    anywhere in the snippet. Any other assignment to the name (non-literal,
    second value, augmented) poisons it to unknown. Conservative on purpose."""
    env: dict = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            val = _literal_str(node.value)
            for tgt in node.targets:
                if isinstance(tgt, ast.Name):
                    if tgt.id in env and env[tgt.id] != val:
                        env[tgt.id] = None  # conflicting bindings: unknown
                    else:
                        env[tgt.id] = val
        elif isinstance(node, (ast.AugAssign, ast.AnnAssign)):
            if isinstance(node, ast.AnnAssign) and node.value is None:
                continue
            tgt = node.target
            if isinstance(tgt, ast.Name):
                env[tgt.id] = None  # augmented/annotated-with-value: unknown
    return env


def _receiver_target_args(receiver: ast.AST):
    """Yield the constructor args of a receiver expression (Path("/x").write_text)."""
    if isinstance(receiver, ast.Call):
        yield from receiver.args


def _open_mode_node(call: ast.Call, env: Optional[dict], positional: bool) -> Optional[str]:
    """Resolve an open() mode argument to its literal, 'r' when absent, or None
    when present but computed. positional=False for builtin open (mode is arg
    1), True for Path.open (mode is arg 0)."""
    node = None
    if positional:
        if call.args:
            node = call.args[0]
    else:
        if len(call.args) > 1:
            node = call.args[1]
    if node is None:
        for kw in call.keywords:
            if kw.arg == "mode":
                node = kw.value
                break
    if node is None:
        return "r"  # absent mode: the read-only default
    lit = _literal_str(node, env)
    return lit


def _path_arg_nodes(call: ast.Call, env: Optional[dict] = None):
    """Yield the AST nodes of args that would carry write-target paths."""
    func = call.func
    if isinstance(func, ast.Attribute):
        attr = func.attr
        if attr == "open":
            # Path.open(): no mode is read-only (allowed); a write-ish literal
            # mode gates the target; a computed mode is treated as write-ish.
            mode = _open_mode_node(call, env, positional=True)
            if mode is None or any(c in mode for c in "wax+"):
                yield from _receiver_target_args(func.value)
            return
        if attr in _METHOD_WRITES:
            yield from _receiver_target_args(func.value)
            return
        dotted = None
        value = func.value
        if isinstance(value, ast.Name):
            dotted = f"{value.id}.{attr}"
        elif isinstance(value, ast.Attribute) and isinstance(value.value, ast.Name):
            dotted = f"{value.value.id}.{value.attr}.{attr}"
        if dotted in _WRITE_CALLS:
            for i in _WRITE_CALLS[dotted]:
                if i < len(call.args):
                    yield call.args[i]
        return
    if isinstance(func, ast.Name):
        name = func.id
        if name == "open":
            # builtin open: no mode is the READ default and stays allowed; an
            # explicit read-only mode stays allowed; a write-ish or computed
            # mode gates the target (conservative), L4 watches the rest.
            mode = _open_mode_node(call, env, positional=False)
            if mode is None or any(c in mode for c in "wax+"):
                if call.args:
                    yield call.args[0]
            return
        if name in _WRITE_CALLS:
            for i in _WRITE_CALLS[name]:
                if i < len(call.args):
                    yield call.args[i]


def static_path_gate(code: str, allowed_root: str) -> list[dict]:
    """L1: return violation rows for literal write paths outside allowed_root.

    allowed_root is the owned run root (the run dir's parent), NOT the whole OS
    temp prefix: a marker dropped as a sibling of the run root is still an
    escape, and the gate refuses it pre-exec.
    """
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return []  # the real interpreter will refuse it; not a containment event
    env = _const_env(tree)
    allowed = normalized(allowed_root)
    hits = []
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        for arg in _path_arg_nodes(node, env):
            lit = _literal_str(arg, env)
            if lit is None:
                continue
            expanded = os.path.expandvars(os.path.expanduser(lit))
            if not os.path.isabs(expanded):
                continue  # relative: resolves to the child's cwd (the run dir), allowed
            norm = normalized(expanded)
            if not norm.startswith(allowed + os.sep) and norm != allowed:
                hits.append({
                    "kind": "static_path_gate",
                    "path": norm,
                    "detail": "literal write path outside the allowed run root",
                })
    return hits
