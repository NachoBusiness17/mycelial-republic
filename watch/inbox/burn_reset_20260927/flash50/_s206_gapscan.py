"""s2-06 gap scanner - secret shapes the 31-rule secret gate does NOT cover.

Item s2-06 (flash50). Reads the gate's own rule table (tools/secret_gate_rules.py,
31 named rules + ENT branch) and scans the git repo surface (tracked +
untracked-not-ignored + root .env) with 14 gap patterns chosen OUTSIDE the
gate's rule shapes: base64 blobs, two-segment JWTs, extra-scheme connection
strings, basic-auth URLs, ODBC/SQLServer-style creds, Azure keys/SAS, kube
*-data blobs, docker auth, _authToken, .netrc, PuTTY PPK, and vendor token
shapes absent from the 31 rules.

Every finding carries its own verdict against the gate:
  gate_token_rules - which of the 31 rule regexes match the token itself
  gate_line_kinds  - which rules the gate engine would fire on the line
                     (blockable-per-rule pass + COMBINED pass, span-overlap
                     skip, exact replica of tools/secret_gate_scan.py logic)
  ent              - ENT-visible if the gate entropy branch would fire on the
                     token (run >= 25 chars, shannon >= 4.3), else ENT-blind
  baseline         - path-scoped baseline acceptance if any
Values are masked everywhere: first 6 chars + length. Never printed in full.

Spawn law (win32): git is spawned with creationflags CREATE_NO_WINDOW.
"""
import base64
import hashlib
import json
import math
import os
import re
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
sys.path.insert(0, REPO)
from tools.secret_gate_rules import (  # noqa: E402
    ALLOW_RE, BLOCKABLE_RES, COMBINED, ENT_RE_RAW, ENT_LEN_MIN, ENTROPY_MIN,
    GITLEAKS_ALLOW, MAX_FILE_BYTES, RULES, RULE_NAMES, SELF_SKIP_RELPATHS,
    SNIFF_BYTES, load_baseline,
)

OUT_JSON = os.path.join(HERE, "_s206_findings.json")
STORE_CAP = 400  # stored rows per gap rule; counts stay exact


def _run(cmd):
    kw = {}
    if sys.platform == "win32":
        kw["creationflags"] = 0x08000000  # CREATE_NO_WINDOW
    p = subprocess.run(cmd, capture_output=True, shell=False, **kw)
    if p.returncode != 0:
        raise SystemExit("spawn failed (%s): %s"
                         % (cmd[0], p.stderr.decode("utf-8", "replace").strip()))
    return p.stdout


def shannon(s):
    counts = {}
    for ch in s:
        counts[ch] = counts.get(ch, 0) + 1
    n = len(s)
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h


def is_binary(chunk):
    if b"\x00" in chunk or not chunk:
        return True
    textish = sum(1 for b in chunk if 9 <= b <= 13 or 32 <= b <= 126 or b >= 128)
    return textish / len(chunk) < 0.85


def mask(tok):
    return tok[:6] + "..." + "(len=%d)" % len(tok)


# --- gap patterns (each chosen OUTSIDE the gate's 31 rule shapes) -----------

PLACEHOLDER_VALS = {
    "user", "username", "pass", "password", "foo", "bar", "baz", "admin",
    "root", "test", "example", "myuser", "mypassword", "john", "jane", "doe",
    "changeme", "secret", "yourpassword", "yourpass", "mypass", "sample",
    "postgres", "mysql", "dummy", "placeholder", "xxxxxx", "abc123",
}


def _ph_ok(user, pw):
    u = user.lower().strip()
    p = pw.lower().strip()
    if u in PLACEHOLDER_VALS or p in PLACEHOLDER_VALS:
        return False
    if u.startswith("example") or p.startswith("example"):
        return False
    if u == p:
        return False
    return True


def _jwt2_ok(tok):
    """Header segment must decode to a JSON object naming alg/typ."""
    head = tok.split(".")[0]
    try:
        pad = head + "=" * (-len(head) % 4)
        raw = base64.urlsafe_b64decode(pad.encode())
        obj = json.loads(raw.decode("utf-8", "strict"))
        return isinstance(obj, dict) and ("alg" in obj or "typ" in obj)
    except Exception:
        return False


def _docker_ok(tok):
    try:
        pad = tok + "=" * (-len(tok) % 4)
        raw = base64.b64decode(pad.encode(), validate=False)
        return b":" in raw
    except Exception:
        return False


def _bauth_ok(tok):
    try:
        creds = tok.split("://", 1)[1].split("@")[0]
        user, pw = creds.split(":", 1)
    except (IndexError, ValueError):
        return False
    return _ph_ok(user, pw)


def _b64_decodable(tok):
    """Classify: does this blob base64-decode to mostly-printable bytes."""
    for dec in ("urlsafe", "std"):
        try:
            pad = tok + "=" * (-len(tok) % 4)
            raw = (base64.urlsafe_b64decode if dec == "urlsafe"
                   else base64.b64decode)(pad.encode())
            if not raw:
                continue
            printable = sum(1 for b in raw if 32 <= b <= 126 or b in (9, 10, 13))
            if printable / len(raw) >= 0.85:
                return dec
        except Exception:
            continue
    return ""


GAP_RULES = [
    ("JWT2-UNSIGNED",
     re.compile(r"\beyJ[A-Za-z0-9_\-]{8,}\.[A-Za-z0-9_\-]{8,}(?!\.[A-Za-z0-9_\-])"),
     "two-segment JWT (header.payload, no signature); gate JWT-TRIPLE needs 3",
     _jwt2_ok),
    ("CONN-EXTRA-SCHEME",
     re.compile(r"\b(?:mssql|sqlserver|oracle|cassandra|snowflake|clickhouse|"
                r"trino|presto|elasticsearch|opensearch|db2|firebird|sybase|"
                r"influxdb|influx|rediss|amqps|sftp|ftps|ftp|smtps|smtp|ldaps|"
                r"ldap|mqtt)://[^\s:@/\"']+:[^\s@/\"']+@"),
     "creds-in-URL for schemes outside CONNSTRING-CRED's six (incl rediss/amqps)",
     None),
    ("BASICAUTH-URL",
     re.compile(r"\b(?:https?|wss?)://[^\s:@/\"'<>()]{1,64}:"
                r"[^\s@/\"'<>()]{1,128}@[A-Za-z0-9.\-_]+"),
     "user:password@ in http/https/ws URLs (no rule covers web schemes)",
     _bauth_ok),
    ("ODBC-CRED",
     re.compile(r"(?i)(?:\bpassword\b|\bpwd)\s*=\s*([^;'\x22@\s]{4,128})"),
     "SQLServer/ODBC/ADO style password= inside a server=/data source= line",
     None),
    ("AZURE-ACCTKEY",
     re.compile(r"(?i)AccountKey=([A-Za-z0-9+/=]{40,})"),
     "Azure storage connection string AccountKey (88-char base64 blob)",
     None),
    ("AZURE-SAS",
     re.compile(r"(?i)\bsig=([A-Za-z0-9%/+=]{20,})"),
     "Azure Shared Access Signature token (sig= on a line carrying sv=)",
     None),
    ("B64-CTX-STD",
     re.compile(r"[A-Za-z0-9+/]{40,}={0,2}"),
     "base64 blob >=40 chars on a line with a credential keyword",
     None),
    ("B64-CTX-URL",
     re.compile(r"[A-Za-z0-9_\-]{43,}={0,2}"),
     "base64url blob >=43 chars on a line with a credential keyword",
     None),
    ("KUBE-DATA",
     re.compile(r"(?i)(?:client-certificate-data|client-key-data|"
                r"certificate-authority-data|private-key-data|token-data)"
                r"\s*:\s*([A-Za-z0-9+/=]{40,})"),
     "kubeconfig embedded cert/key blobs (base64, no rule touches them)",
     None),
    ("DOCKER-AUTH",
     re.compile(r"\"auth\"\s*:\s*\"([A-Za-z0-9+/=]{16,})\""),
     "docker config.json auth field = base64 user:password",
     _docker_ok),
    ("NPMRC-AUTHTOKEN",
     re.compile(r"_authToken\s*[:=]\s*['\"]?([A-Za-z0-9_.\-]{16,})"),
     ".npmrc _authToken; GENERIC-KEYASSIGN name list has no authToken form",
     None),
    ("NETRC-CRED",
     re.compile(r"(?im)^machine\s+(\S+)\s+login\s+(\S+)\s+password\s+(\S+)"),
     ".netrc machine/login/password triplet",
     None),
    ("PPK-HEADER",
     re.compile(r"PuTTY-User-Key-File-\d"),
     "PuTTY PPK private key container (not a BEGIN PRIVATE KEY block)",
     None),
    ("VENDOR-GAP",
     re.compile(
         r"\b(?:"
         r"[MN][A-Za-z0-9_\-]{23}\.[A-Za-z0-9_\-]{6}\.[A-Za-z0-9_\-]{27}"
         r"|GOCSPX-[A-Za-z0-9_\-]{28}"
         r"|1//[A-Za-z0-9_\-]{30,}"
         r"|dop_v1_[a-f0-9]{64}"
         r"|shp(?:at|ca|pa|ss)_[a-f0-9]{32}"
         r"|dapi[a-f0-9]{32}"
         r"|hf_[A-Za-z0-9]{34}"
         r"|fig[dou]_[A-Za-z0-9_\-]{22,}"
         r"|ATATT[A-Za-z0-9_\-]{60,}"
         r"|ATBB[A-Za-z0-9+/=_.\-]{30,}"
         r"|lin_api_[A-Za-z0-9_]{40}"
         r"|secret_[A-Za-z0-9]{43}"
         r"|hvs\.[A-Za-z0-9]{24,}"
         r"|glsa_[A-Za-z0-9]{32}_[a-f0-9]{8}"
         r"|PMAK-[a-f0-9]{24}-[a-f0-9]{34}"
         r"|ya29\.[0-9A-Za-z_\-]{20,}"
         r"|gl(?:rt|dt|oas|cb)-[A-Za-z0-9_\-]{20,}"
         r")"),
     "vendor token shapes with no gate rule: discord, GCP oauth, digitalocean, "
     "shopify, databricks, huggingface, figma, atlassian, bitbucket, linear, "
     "notion, vault, grafana, postman, google access, gitlab non-PAT",
     None),
]

KEYWORD_LINE = re.compile(
    r"(?i)(secret|token|password|passwd|credential|api[_-]?key|apikey|"
    r"private[_-]?key|auth[_-]?token|access[_-]?key|bearer|signing[_-]?key|"
    r"conn(ection)?[_-]?string)")


# --- gate replica helpers ---------------------------------------------------

def gate_token_rules(tok):
    """Which of the 31 named rule regexes match this exact token."""
    hits = []
    for rid, _sev, pat in RULES:
        if rid == "ENV-ASSIGN":  # line-anchored generic; meaningless on a token
            continue
        try:
            if re.search(pat, tok):
                hits.append(rid)
        except re.error:
            pass
    return hits


def gate_line_kinds(line):
    """Exact replica of the scan() line engine: per-rule blockable pass with
    span skip, then COMBINED pass skipping overlaps. Returns {rule: True}
    (ENT tracked separately as the boolean return)."""
    kinds = {}
    spans = []
    for rid, rex in BLOCKABLE_RES:
        for m in rex.finditer(line):
            tok = m.group()
            if ALLOW_RE.search(tok) or ALLOW_RE.search(line[:120]):
                continue
            spans.append((m.start(), m.end()))
            kinds[rid] = True
    for m in COMBINED.finditer(line):
        idx = m.lastindex
        if idx is None:
            continue
        if any(m.start() < e and s < m.end() for s, e in spans):
            continue
        if idx > len(RULE_NAMES):
            return kinds, True
        kinds[RULE_NAMES[idx - 1]] = True
    return kinds, False


ENT_RE = re.compile(ENT_RE_RAW)


def ent_status(tok):
    for m in ENT_RE.finditer(tok):
        run = m.group()
        if len(run) >= ENT_LEN_MIN and shannon(run) >= ENTROPY_MIN:
            return "ENT-visible"
    return "ENT-blind"


# --- file list: tracked + untracked-not-ignored + root .env -----------------

files = []
for out in (_run(["git", "-C", REPO, "ls-files", "-z"]),
            _run(["git", "-C", REPO, "ls-files", "--others",
                  "--exclude-standard", "-z"])):
    for f in out.decode("utf-8", "replace").split("\0"):
        if f:
            files.append(os.path.normpath(os.path.join(REPO, f)))
env_path = os.path.join(REPO, ".env")
if os.path.isfile(env_path):
    files.append(env_path)
files = sorted(set(files))

# baseline (named acceptance): accepted dict + path rules
baseline_path = os.path.join(REPO, "configs", "secret_gate_baseline.json")
accepted, path_rules = load_baseline(baseline_path)

census = {"files_seen": len(files), "self_skipped": 0, "large_skipped": 0,
          "binary_skipped": 0, "read_error": 0, "scanned": 0,
          "bytes_scanned": 0, "long_lines_skipped": 0,
          "gitleaks_allow_lines": 0, "total_lines": 0}
counts = {rid: 0 for rid, _r, _n, _v in GAP_RULES}
stored = {rid: 0 for rid, _r, _n, _v in GAP_RULES}
files_per_rule = {rid: set() for rid, _r, _n, _v in GAP_RULES}
findings = []
seen_fp = set()
t0 = time.time()

for fi, path in enumerate(files, 1):
    # same nul-device guard as tools/secret_gate_scan.py rel_of(): the tree
    # carries literal "nul" files whose relpath resolves to \\.\nul
    try:
        rel = os.path.relpath(path, REPO).replace("\\", "/")
    except (ValueError, OSError):
        rel = path.replace("\\", "/")
    top = rel.split("/")[0] if "/" in rel else "(root)"
    if rel in SELF_SKIP_RELPATHS or "/secret_gate_results/" in "/" + rel:
        census["self_skipped"] += 1
        continue
    try:
        size = os.path.getsize(path)
    except OSError:
        census["read_error"] += 1
        continue
    if size > MAX_FILE_BYTES:
        census["large_skipped"] += 1
        continue
    try:
        with open(path, "rb") as fh:
            chunk = fh.read(SNIFF_BYTES)
            if is_binary(chunk):
                census["binary_skipped"] += 1
                continue
            fh.seek(0)
            data = fh.read(MAX_FILE_BYTES)
    except OSError:
        census["read_error"] += 1
        continue
    census["scanned"] += 1
    census["bytes_scanned"] += len(data)
    text = data.decode("utf-8", errors="ignore")
    for i, line in enumerate(text.splitlines(), 1):
        census["total_lines"] += 1
        if not line or len(line) > 4000:
            if line:
                census["long_lines_skipped"] += 1
            continue
        if GITLEAKS_ALLOW in line:
            census["gitleaks_allow_lines"] += 1
            continue
        if not KEYWORD_LINE.search(line):
            # keyword gate applies only to the two B64 rules, but skipping
            # the rest of the engine this early is safe: every other gap
            # pattern carries its own trigger inside the token itself.
            gap_iter = [(rid, rex, note, val) for rid, rex, note, val
                        in GAP_RULES if rid not in ("B64-CTX-STD", "B64-CTX-URL")]
        else:
            gap_iter = GAP_RULES
        line_baseline = any(pr["re"].search(rel) for pr in path_rules)
        for rid, rex, note, validator in gap_iter:
            for m in rex.finditer(line):
                tok = m.group(1) if m.groups() else m.group()
                if len(tok) < 16 and rid not in ("PPK-HEADER",):
                    continue
                if validator is not None and not validator(tok):
                    continue
                key = (rid, rel, hashlib.sha256(
                    (line.strip() + "|" + tok).encode("utf-8", "ignore")
                ).hexdigest()[:16])
                if key in seen_fp:
                    continue
                seen_fp.add(key)
                counts[rid] += 1
                files_per_rule[rid].add(rel)
                if stored[rid] < STORE_CAP:
                    stored[rid] += 1
                    ent = ent_status(tok) if rid != "PPK-HEADER" else "n/a"
                    findings.append({
                        "gap_rule": rid, "file": rel, "line": i, "top": top,
                        "masked": mask(tok), "ent": ent,
                        "gate_token_rules": gate_token_rules(tok),
                        "gate_line_kinds": sorted(gate_line_kinds(line)[0]),
                        "allow_re": bool(ALLOW_RE.search(tok)
                                         or ALLOW_RE.search(line[:120])),
                        "baseline_path": line_baseline,
                        "b64_decodable": _b64_decodable(tok)
                        if rid.startswith("B64") or rid == "KUBE-DATA" else "",
                    })
    if fi % 5000 == 0:
        sys.stderr.write("... %d files %ds\n" % (fi, time.time() - t0))
        sys.stderr.flush()

summary = {
    "census": census,
    "counts": counts,
    "files_per_rule": {k: len(v) for k, v in files_per_rule.items()},
    "gap_rules": [{"id": rid, "note": note} for rid, _r, note, _v in GAP_RULES],
    "runtime_sec": round(time.time() - t0, 1),
    "findings_stored": findings,
    "store_cap": STORE_CAP,
}
with open(OUT_JSON, "w", encoding="utf-8") as fh:
    json.dump(summary, fh, indent=1)
print(json.dumps({k: v for k, v in summary.items() if k != "findings_stored"},
                 indent=1))
print("stored rows: %d -> %s" % (len(findings), OUT_JSON))
