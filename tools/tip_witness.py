#!/usr/bin/env python3
"""tip_witness.py - external witness for the verkle chain tip (W3, 2026-09-30).

The chain is tamper-evident against OUTSIDERS but writer-only: the writer can
rewrite the whole chain and no in-repo byte survives to contradict the
rewrite. An external checkpoint - a GitHub gist holding one line - breaks the
economics of laundering. The publish path is a RATCHET: the witness only
ADVANCES on leaf-count growth, never backward (shrunk chain) and never
sideways (same-count root change). A rewritten chain cannot drag the witness
with it; it can only trip WITNESS-DIVERGENT.

Witness line: MAG-TIP-WITNESS.v1 root=<64-hex> n_leaves=<int> ts=<ISO-UTC>
Gist law: ONE gist, id in memory/biography/tip_witness_state.json; a lost
state file re-adopts by the gist description marker, never a second gist.
Trust boundary: reads memory/biography/verkle_tip.json as the live tip;
tip-vs-chain consistency is AG5's job, not recomputed here.

  python tools/tip_witness.py                  # dry-run plan + verify (read-only)
  python tools/tip_witness.py --verify         # fetch gist, compare, report
  python tools/tip_witness.py --publish --go   # real publish (operator gate)

Exit codes: 0 ok (MATCH/LAG/NONE/clean publish); 1 ALARM (DIVERGENT =
chain rewritten = laundering alarm); 2 cannot verify (no token, network,
gist-scope denial, unparseable witness line, unreadable tip).

Token: GITHUB_TOKEN via mag.key_law.get("github_token") (declared in
configs/keys.json; load_dotenv feeds it from .env). Never printed. Scope
probe 2026-09-30: the current fine-grained PAT has gist READ but gist WRITE
denied (POST /gists 403, GET /gists 200). First real publish fails exit 2
with the SCOPE note until the operator widens the PAT (Account permissions
-> Gists: Read and write) or swaps a classic PAT with the gist scope.
"""
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Callable, Optional

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))  # script-mode: make mag.key_law importable
TIP_FILE = ROOT / "memory" / "biography" / "verkle_tip.json"
STATE_FILE = ROOT / "memory" / "biography" / "tip_witness_state.json"

API = "https://api.github.com"
GIST_DESC = ("MAG-TIP-WITNESS verkle tip witness "
             "(auto-published by tools/tip_witness.py - do not edit)")
GIST_MARKER = "MAG-TIP-WITNESS"
GIST_FILENAME = "tip_witness.txt"
HTTP_TIMEOUT = 30
STATE_SCHEMA = "tip_witness_state.v1"

LINE_RE = re.compile(
    r"^MAG-TIP-WITNESS\.v1 root=([0-9a-f]{64}) n_leaves=(\d+) ts=(\S+)$"
)


class WitnessError(Exception):
    """Cannot-verify class (exit 2). Message is printed, never guesses."""


# ── tip + line ──────────────────────────────────────────────────────

def _utc_now_iso() -> str:
    return dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def load_tip(path: Optional[Path] = None) -> dict:
    """Read root + n_leaves from the verkle tip file. Fail closed.

    ``path`` resolves the module global at CALL time (never a def-time
    default): tests retarget TIP_FILE via monkeypatch and must see it.
    """
    path = path or TIP_FILE
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError:
        raise WitnessError(f"cannot verify: tip file missing: {path}")
    except (OSError, ValueError) as e:
        raise WitnessError(f"cannot verify: tip file unreadable: {e}")
    root = data.get("root") or ""
    n = data.get("n_leaves")
    if not isinstance(root, str) or not re.fullmatch(r"[0-9a-f]{64}", root):
        raise WitnessError("cannot verify: tip root is not 64-hex")
    if not isinstance(n, int) or isinstance(n, bool) or n < 0:
        raise WitnessError("cannot verify: tip n_leaves is not a non-negative int")
    return {"root": root, "n_leaves": n}


def build_line(root: str, n_leaves: int, ts: str) -> str:
    return f"MAG-TIP-WITNESS.v1 root={root} n_leaves={n_leaves} ts={ts}"


def parse_line(text: str) -> Optional[dict]:
    """Parse the witness line out of gist content (first match wins)."""
    for raw in (text or "").splitlines():
        m = LINE_RE.match(raw.strip())
        if m:
            return {"root": m.group(1), "n_leaves": int(m.group(2)),
                    "ts": m.group(3)}
    return None


def compare(witnessed: dict, live: dict) -> tuple:
    """(verdict, detail). MATCH | LAG (live ahead, publish due) |
    DIVERGENT (chain rewritten - the laundering alarm)."""
    if witnessed["root"] == live["root"] and witnessed["n_leaves"] == live["n_leaves"]:
        return ("WITNESS-MATCH",
                f"witnessed root==live root, {live['n_leaves']} leaves "
                f"(witnessed {witnessed['ts']})")
    if live["n_leaves"] > witnessed["n_leaves"]:
        return ("WITNESS-LAG",
                f"live tip ahead of witness: {live['n_leaves']} leaves live vs "
                f"{witnessed['n_leaves']} witnessed (normal growth; publish due)")
    if live["n_leaves"] < witnessed["n_leaves"]:
        return ("WITNESS-DIVERGENT",
                f"chain SHRANK: {witnessed['n_leaves']} leaves witnessed vs "
                f"{live['n_leaves']} live - chain rewritten, laundering alarm")
    return ("WITNESS-DIVERGENT",
            f"same count ({live['n_leaves']} leaves) but root differs - "
            f"same-length rewrite, laundering alarm")


# ── token (value never printed; key_law is the one door) ────────────

def load_token() -> str:
    """GITHUB_TOKEN through mag.key_law (declared in configs/keys.json).

    Key law 2026-09-23: no reader guesses env names; the manifest entry
    feeds the env var name, load_dotenv feeds .env into os.environ.
    """
    from mag import key_law  # exempt reader per ENV_EXEMPT_FILES
    try:
        return key_law.get("github_token") or ""
    except KeyError as e:
        raise WitnessError(
            f"cannot verify: {e} - declare it in configs/keys.json "
            f"(key law: one key, one canonical name)")


# ── gist API (transport-injectable; tests never touch the network) ──

Transport = Callable[[urllib.request.Request, int], tuple]


def _urllib_transport(req: urllib.request.Request, timeout: int) -> tuple:
    """Default transport: returns (status, body_bytes, headers_dict).

    HTTPError is normalized into the tuple so 403/404 flow as statuses,
    not exceptions; only transport-level failures (URLError, timeout)
    raise, and those become exit-2 WitnessError upstream.
    """
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            status = getattr(r, "status", None) or r.getcode()
            return (status, r.read(), dict(r.headers))
    except urllib.error.HTTPError as e:
        return (e.code, e.read(), dict(e.headers or {}))


class GistAPI:
    def __init__(self, token: str, transport: Optional[Transport] = None):
        self.token = token
        self.transport = transport or _urllib_transport

    def _req(self, method: str, url: str, body: Optional[dict] = None) -> tuple:
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = urllib.request.Request(
            url, data=data, method=method,
            headers={
                "Authorization": f"Bearer {self.token}",
                "Accept": "application/vnd.github+json",
                "Content-Type": "application/json",
                "X-GitHub-Api-Version": "2022-11-28",
                "User-Agent": "mag-tip-witness/1",
            })
        try:
            status, raw, headers = self.transport(req, HTTP_TIMEOUT)
        except Exception as e:  # URLError, timeout, DNS - transport-level
            raise WitnessError(f"cannot verify: network failure: {e}")
        try:
            parsed = json.loads(raw.decode("utf-8", "replace")) if raw else {}
        except ValueError:
            parsed = {}
        return status, parsed, headers

    def list_gists(self) -> list:
        status, data, _ = self._req("GET", f"{API}/gists?per_page=100")
        if status != 200:
            raise WitnessError(f"cannot verify: gist list returned HTTP {status}")
        return data if isinstance(data, list) else []

    def get_gist(self, gist_id: str) -> dict:
        status, data, _ = self._req("GET", f"{API}/gists/{gist_id}")
        if status != 200:
            raise WitnessError(
                f"cannot verify: gist fetch returned HTTP {status}")
        return data

    def gist_content(self, gist: dict) -> str:
        try:
            return gist["files"][GIST_FILENAME]["content"] or ""
        except (KeyError, TypeError):
            return ""

    def _publish_body(self, line: str, public: bool) -> dict:
        return {"description": GIST_DESC, "public": public,
                "files": {GIST_FILENAME: {"content": line}}}

    def create_gist(self, line: str, public: bool = False) -> dict:
        status, data, _ = self._req("POST", f"{API}/gists",
                                    self._publish_body(line, public))
        if status == 403 or status == 401:
            raise WitnessError(
                f"cannot verify: SCOPE - token cannot create gists "
                f"(HTTP {status}). Fix: fine-grained PAT needs Account "
                f"permissions -> Gists: Read and write, or a classic PAT "
                f"with the gist scope.")
        if status not in (200, 201):
            raise WitnessError(f"cannot verify: gist create returned HTTP {status}")
        return data

    def patch_gist(self, gist_id: str, line: str) -> dict:
        status, data, _ = self._req("PATCH", f"{API}/gists/{gist_id}",
                                    self._publish_body(line, False))
        if status == 403 or status == 401:
            raise WitnessError(
                f"cannot verify: SCOPE - token cannot edit the witness gist "
                f"(HTTP {status}). Same fix as create: gist write permission.")
        if status != 200:
            raise WitnessError(f"cannot verify: gist patch returned HTTP {status}")
        return data


# ── state + single-gist law ─────────────────────────────────────────

def load_state(path: Optional[Path] = None) -> dict:
    path = path or STATE_FILE  # call-time, same law as load_tip
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}  # missing/corrupt state = no witness adopted yet (adopt scan)
    if isinstance(data, dict) and data.get("gist_id"):
        return data
    return {}


def save_state(state: dict, path: Optional[Path] = None) -> None:
    path = path or STATE_FILE  # call-time, same law as load_tip
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n",
                   encoding="utf-8")
    tmp.replace(path)


def resolve_gist_id(api: GistAPI, state: dict) -> Optional[str]:
    """State first; else adopt the one gist whose description carries the
    marker (state-file loss must never spawn a second witness gist)."""
    gid = state.get("gist_id")
    if gid:
        return str(gid)
    for g in api.list_gists():
        if str(g.get("description") or "").startswith(GIST_MARKER):
            return str(g.get("id"))
    return None


def fetch_witness_line(api: GistAPI, gist_id: str) -> dict:
    gist = api.get_gist(gist_id)
    line = parse_line(api.gist_content(gist))
    if line is None:
        raise WitnessError(
            "cannot verify: witness gist has no parseable "
            "MAG-TIP-WITNESS.v1 line (hand-edited gist?)")
    return line


# ── commands ────────────────────────────────────────────────────────

def _api_or_die(transport: Optional[Transport]) -> GistAPI:
    token = load_token()
    if not token:
        raise WitnessError("cannot verify: no GITHUB_TOKEN (env or .env)")
    return GistAPI(token, transport)


def run_verify(transport: Optional[Transport] = None) -> int:
    api = _api_or_die(transport)
    live = load_tip()
    state = load_state()
    gid = resolve_gist_id(api, state)
    if gid is None:
        print("WITNESS-NONE (no gist witnessed yet; "
              "first --publish --go creates the single witness gist)")
        return 0
    witnessed = fetch_witness_line(api, gid)
    verdict, detail = compare(witnessed, live)
    print(f"{verdict}: {detail}")
    if verdict == "WITNESS-DIVERGENT":
        print("LAUNDERING ALARM: the live tip contradicts the external "
              "witness. Do NOT re-publish. Audit with `python main.py "
              "verkle-audit --dry` and the gist revision history first.")
        return 1
    return 0


def run_publish(go: bool, public: bool,
                transport: Optional[Transport] = None) -> int:
    live = load_tip()
    line = build_line(live["root"], live["n_leaves"], _utc_now_iso())

    if not go:
        print("DRY-RUN (default): publish is operator-gated.")
        print(f"would publish: {line}")
        print("gate: re-run with --publish --go to write the gist")
        print("-- verify (read-only) follows --")
        return run_verify(transport)

    api = _api_or_die(transport)
    state = load_state()
    gid = resolve_gist_id(api, state)

    if gid is None:
        gist = api.create_gist(line, public=public)
        _save_publish_state(gist, line, state)
        print(f"WITNESS-CREATED gist={gist.get('id')} "
              f"url={gist.get('html_url')}")
        print(line)
        return 0

    # Ratchet: verify FIRST. The witness advances on leaf-count growth only.
    witnessed = fetch_witness_line(api, gid)
    verdict, detail = compare(witnessed, live)
    if verdict == "WITNESS-DIVERGENT":
        print(f"{verdict}: {detail}")
        print("PUBLISH REFUSED: the witness never moves backward or "
              "sideways. A rewritten chain cannot re-launder the external "
              "checkpoint. Audit the chain before any witness write.")
        return 1
    if verdict == "WITNESS-MATCH":
        print(f"WITNESS-MATCH: witness already current, no write ({detail})")
        _save_publish_state({"id": gid}, line, state)
        return 0

    gist = api.patch_gist(gid, line)  # WITNESS-LAG: advance the witness
    _save_publish_state(gist, line, state)
    print(f"WITNESS-ADVANCED gist={gist.get('id', gid)} "
          f"url={gist.get('html_url')}")
    print(line)
    return 0


def _save_publish_state(gist: dict, line: str, prev: dict) -> None:
    gid = str(gist.get("id") or prev.get("gist_id"))
    save_state({
        "schema": STATE_SCHEMA,
        "gist_id": gid,
        "gist_url": gist.get("html_url") or prev.get("gist_url"),
        "last_line": line,
        "published_at": _utc_now_iso(),
        "note": "single-gist law: adopt by MAG-TIP-WITNESS description "
                "marker if this file is lost; never create a second gist",
    })


def main(argv: Optional[list] = None,
         transport: Optional[Transport] = None) -> int:
    ap = argparse.ArgumentParser(
        prog="tip_witness.py", description="External gist witness for the "
        "verkle chain tip (dry-run default; --publish --go is the gate).")
    ap.add_argument("--verify", action="store_true",
                    help="fetch gist, compare live tip, report verdict")
    ap.add_argument("--publish", action="store_true",
                    help="publish to the single witness gist (gated)")
    ap.add_argument("--go", action="store_true",
                    help="operator gate: actually write the gist")
    ap.add_argument("--public", action="store_true",
                    help="create the gist public instead of secret")
    args = ap.parse_args(argv)

    try:
        if args.verify:
            return run_verify(transport)
        # Default = dry-run publish plan (no write) + read-only verify.
        # --publish without --go hits the same gate explanation.
        return run_publish(go=args.go, public=args.public,
                           transport=transport)
    except WitnessError as e:
        print(f"WITNESS: {e}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
