"""secret_gate_rules - rule table, thresholds and block sets for the secret gate.

Split out of tools/secret_gate.py 2026-09-27 (ratchet file-too-long fix, debt
e3b7845ea79cf553f-adjacent): a pure code MOVE, the borrowed-verbatim regions
keep their bytes and their provenance comments. Behavior contract unchanged;
proved by the split falsifier in state/fuel/sg_split_ref/ (pre/post counts on
a fixed scope, prefilter on and off, must match exactly).

Borrowed, verbatim (do not rewrite, do not improve): the rule table, ALLOW_RE
exemption, combined matcher and its self-checks come from
watch/inbox/burn_wave_20260926/B2_73_secret_scan.py per PACK_SECRET_GATE_20260926
section 2. Provenance detail lives in the tools/secret_gate.py header.

Baseline acceptance (load_baseline) lives here since the second ratchet pass
the same day: what matches, what blocks and what is accepted are one domain.
"""
from __future__ import annotations

import json
import os
import re

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MAX_FILE_BYTES = 10 * 1024 * 1024      # skip single files above 10MB, counted
MAX_FINDINGS_PER_RULE = 60000          # stored rows per rule; counts stay exact
MAX_ENT_STORED = 20000                 # stored entropy rows; counts stay exact
MAX_BLOCKING_STORED = 2000             # stored blocking rows; counts stay exact
SNIFF_BYTES = 8192

# --- gitleaks-derived provider rules (concrete token shapes) ----------------
# VERBATIM from B2_73_secret_scan.py lines 28-60. Do not improve the regexes.
RULES = [
    ("AWS-ACCESS-KID", "high", r"\bAKIA[0-9A-Z]{16}\b"),
    ("AWS-SECRET-40", "high", r"\b(?<![A-Za-z0-9/+=])[A-Za-z0-9/+=]{40}(?![A-Za-z0-9/+=])"),
    ("GOOGLE-API-KEY", "high", r"\bAIza[0-9A-Za-z_\-]{35}\b"),
    ("GOOGLE-OAUTH-AQ", "high", r"\bAQ[a-zA-Z0-9_\-]{30,}\b"),
    ("GITHUB-TOKEN", "high", r"\bgh[pousr]_[A-Za-z0-9]{36,255}\b"),
    ("GITHUB-FINEGRAIN", "high", r"\bgithub_pat_[A-Za-z0-9_]{20,255}\b"),
    ("GITLAB-PAT", "high", r"\bglpat-[A-Za-z0-9_\-]{20,}\b"),
    ("OPENAI-CLASSIC", "high", r"\bsk-[A-Za-z0-9_\-]{20,}T3BlbkFJ[A-Za-z0-9_\-]{20,}\b"),
    ("OPENAI-PROJ", "high", r"\bsk-proj-[A-Za-z0-9_\-]{20,200}\b"),
    ("ANTHROPIC-KEY", "high", r"\bsk-ant-[A-Za-z0-9_\-]{20,200}\b"),
    ("OPENROUTER-KEY", "high", r"\bsk-or-v1-[a-f0-9]{64}\b"),
    ("GROQ-KEY", "high", r"\bgsk_[A-Za-z0-9]{20,80}\b"),
    ("XAI-KEY", "high", r"\bxai-[A-Za-z0-9]{18,80}\b"),
    ("DEEPSEEK-KEY", "high", r"\bsk-[a-f0-9]{32}\b"),
    ("ZHIPU-ZAI-KEY", "high", r"\b[0-9a-f]{32}\.[0-9a-f]{16}\b"),
    ("SLACK-TOKEN", "high", r"\bxox[abposr]-[A-Za-z0-9\-]{10,250}\b"),
    ("STRIPE-KEY", "high", r"\b(?:sk|pk|rk)_(?:live|test)_[0-9a-zA-Z]{10,}\b"),
    ("SENDGRID-KEY", "high", r"\bSG\.[A-Za-z0-9_\-]{16,}\.[A-Za-z0-9_\-]{16,}\b"),
    ("TELEGRAM-BOT", "high", r"\b[0-9]{8,10}:AA[A-Za-z0-9_\-]{33}\b"),
    ("TWILIO-SID", "medium", r"\b(?:SK|AC)[0-9a-f]{32}\b"),
    ("MAILGUN-KEY", "high", r"\bkey-[a-f0-9]{32}\b"),
    ("NPM-TOKEN", "high", r"\bnpm_[A-Za-z0-9]{36}\b"),
    ("PYPI-TOKEN", "high", r"\bpypi-[A-Za-z0-9_\-]{50,}\b"),
    ("VERCEL-TOKEN", "high", r"\bvercel_[A-Za-z0-9]{24}\b"),
    ("JWT-TRIPLE", "medium", r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b"),
    ("PRIVATE-KEY-BLOCK", "critical", r"-----BEGIN [A-Z0-9 ]*PRIVATE KEY(?: BLOCK)?-----"),
    ("CONNSTRING-CRED", "high", r"\b(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://[^\s:@/]+:[^\s@/]+@"),
    ("GENERIC-KEYASSIGN", "medium", r"(?i:\b(?:api[_\-]?key|apikey|secret|access[_\-]?token|auth[_\-]?token|password|passwd)\b\s*[:=]\s*['\"]?[A-Za-z0-9+/_\-]{16,})"),
    ("ENV-ASSIGN", "low", r"^[A-Z][A-Z0-9_]{3,}\s*=\s*['\"]?[^\s'\"]{8,}"),
    ("HEROKU-API", "medium", r"\bHRKU-[0-9a-fA-F\-]{36}\b"),
    ("GENERIC-BEARER", "medium", r"(?i:\bbearer\s+[A-Za-z0-9_\-\.=+/]{20,})"),
]

# entropy branch runs last so concrete rules win their positions
ENT_RE_RAW = r"[A-Za-z0-9+/_\-]{25,}"

ALLOW_RE = re.compile(
    r"(?i)("
    r"your[_\-]?api[_\-]?key|your[_\-]?token|<[^>\n]{1,40}>|\$\{[^}\n]{1,40}\}"
    r"|x{4,}|\.{4,}|\*{3,}|REDACTED|MASKED|PLACEHOLDER|EXAMPLE[_A-Z]*|DUMMY|FAKE"
    r"|abcd1234|1234567890|0123456789abcdef"
    r")"
)

# --- industry-steal amendments 2026-09-27 (card: SECRET_GATE_INDUSTRY_STEAL) --
# Steal 1 (gitleaks): exact industry inline marker; a line carrying it
# suppresses its own finding. Ecosystem-compatible with gitleaks configs.
GITLEAKS_ALLOW = "gitleaks:allow"
# Steal 3 (truffleHog keyword-index, adapted): one fast-pass regex of
# NECESSARY conditions covering every rule (each rule's token is a 16+ run of
# this charset incl ':' for telegram ids, or a conn scheme, an ENV-var head,
# the PEM literal, or bearer). A line matching none of these cannot match any
# rule or the entropy branch, so the heavy COMBINED matcher is skipped.
# Parity is enforced by test (SG_NO_PREFILTER=1 disables for A/B runs).
NO_PREFILTER = os.environ.get("SG_NO_PREFILTER") == "1"
FAST_PASS_RE = re.compile(
    r"[A-Za-z0-9+/_=:-]{16}"
    r"|-----BEGIN"
    r"|eyJ"
    r"|(?i:(?:postgres(?:ql)?|mysql|mongodb(?:\+srv)?|redis|amqp)://)"
    r"|(?i:bearer)"
    r"|[A-Z][A-Z0-9_]{3,}\s*="
)

COMBINED = re.compile(
    "|".join("(%s)" % pat for _rid, _sev, pat in RULES)
    + "|(" + ENT_RE_RAW + ")"
)
RULE_SEV = {rid: sev for rid, sev, _p in RULES}
RULE_NAMES = [rid for rid, _s, _p in RULES]
assert COMBINED.groups == len(RULES) + 1, (
    "group count drift: %d compiled vs %d expected (stray capture group)"
    % (COMBINED.groups, len(RULES) + 1)
)
# Routing self-check probe: the AWS documentation EXAMPLE access-key id
# (public fixture, not a credential; ALLOW_RE exempts it from findings).
# Concatenated so no key-shaped run exists in this source line; the runtime
# string is byte-identical to the original single-file self-check.
_PROBE_TOKEN = "AKIA" + "IOSFODNN7" + "EXAMPLE"
_probe = COMBINED.search(_PROBE_TOKEN)
assert _probe and RULE_NAMES[_probe.lastindex - 1] == "AWS-ACCESS-KID", (
    "routing self-check failed")

# "secret_gate_results" is this gate's own output dir (reserved name): a
# detector scanning its own results would count findings about findings.
SKIP_DIR_PARTS = {".git", "node_modules", "__pycache__", ".venv",
                  "secret_gate_results"}

ENTROPY_MIN = 4.3
ENT_LEN_MIN = 25

SEV_RANK = {"low": 0, "medium": 1, "high": 2, "critical": 3}

# Pack section 4 ruling 3: only specific provider shapes may ever block.
BLOCKABLE_RULES = {
    "AWS-ACCESS-KID", "GOOGLE-API-KEY", "GOOGLE-OAUTH-AQ", "GITHUB-TOKEN",
    "GITHUB-FINEGRAIN", "GITLAB-PAT", "OPENAI-CLASSIC", "OPENAI-PROJ",
    "ANTHROPIC-KEY", "OPENROUTER-KEY", "GROQ-KEY", "XAI-KEY", "DEEPSEEK-KEY",
    "ZHIPU-ZAI-KEY", "SLACK-TOKEN", "STRIPE-KEY", "SENDGRID-KEY",
    "TELEGRAM-BOT", "TWILIO-SID", "MAILGUN-KEY", "NPM-TOKEN", "PYPI-TOKEN",
    "VERCEL-TOKEN", "HEROKU-API", "CONNSTRING-CRED", "PRIVATE-KEY-BLOCK",
}
# AWS-SECRET-40: 48,427 hits = 80% of all findings in the one real run.
# GENERIC-KEYASSIGN: 99.5% false-positive rate in a separate audit (pack 4.3).
# ENV-ASSIGN / JWT-TRIPLE / GENERIC-BEARER: generic shapes, report only.
NEVER_BLOCK_RULES = {"AWS-SECRET-40", "GENERIC-KEYASSIGN", "ENV-ASSIGN",
                     "JWT-TRIPLE", "GENERIC-BEARER"}
assert not (BLOCKABLE_RULES & NEVER_BLOCK_RULES), "block sets must be disjoint"
assert NEVER_BLOCK_RULES <= set(RULE_NAMES), "never-block names must be rules"

# GATE_DEFECT_ASSIGNMENT_BYPASS fix (2026-09-27; receipt
# watch/inbox/audit_20260926/GATE_DEFECT_ASSIGNMENT_BYPASS_20260927.md):
# the blockable provider rules are ALSO compiled per-rule so the scan can
# evaluate them independently of COMBINED. Cause: COMBINED ORs all rules
# into one alternation and finditer is non-overlapping, so the generic
# NAME=value alternatives at the tail swallow the whole line and the
# provider rule never fires — XAI_API_KEY=xai-... landed low and did NOT
# block. Fix shape: per-rule evaluation for the blockable set, highest
# specificity wins; COMBINED stays for the report tier only.
BLOCKABLE_RES = [
    (rid, re.compile(pat)) for rid, _sev, pat in RULES if rid in BLOCKABLE_RULES
]

# Detector family self-skips: the CLI entry, the two split modules (this file
# carries the same routing self-check probe and rule-table bytes as the
# original single file did), the borrowed original and its one-run results
# artifact (scanning the detector's own output would double-count).
SELF_SKIP_RELPATHS = {
    "tools/secret_gate.py",
    "tools/secret_gate_rules.py",
    "tools/secret_gate_scan.py",
    "watch/inbox/burn_wave_20260926/B2_73_secret_scan.py",
    "watch/inbox/burn_wave_20260926/B2_73_secret_scan_results.json",
}

RESULTS_DIR = os.path.join(REPO, "watch", "inbox", "secret_gate_results")


class GateError(Exception):
    """Scanner-side failure: caller must see exit 2, never a silent 0.

    Lives in this bottom-of-chain module since the 2026-09-27 second ratchet
    pass (load_baseline moved here): secret_gate_scan imports it, and
    tools/secret_gate.py catches ONE class for both scanner and baseline
    failures instead of two exceptions with drifting contracts."""


def load_baseline(path):
    """Named acceptance, B3 shape: {"accepted": {<16-hex fp>: {...}}}.

    Day one ships ZERO baseline. Missing or malformed file is a scanner
    error (exit 2), never a silently empty pass.
    """
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except OSError as e:
        raise GateError("baseline unreadable: %s" % e)
    except json.JSONDecodeError as e:
        raise GateError("baseline not valid JSON: %s" % e)
    if not isinstance(data, dict) or not isinstance(data.get("accepted"), dict):
        raise GateError("baseline shape must be {\"accepted\": {...}} (B3 shape)")
    # Steal 2 (gitleaks [allowlist] paths): optional path-scoped entries,
    # {"paths": [{"rule": RID, "path_re": REGEX, "by": WHO, "reason": WHY}]}.
    # Survives line churn where the line-fingerprint key does not. Entries
    # without a reason or author are a scanner error: named acceptance means
    # named, and a reasonless allowlist is how gates get silently emptied.
    path_rules = []
    raw_paths = data.get("paths", [])
    if not isinstance(raw_paths, list):
        raise GateError("baseline \"paths\" must be a list")
    for entry in raw_paths:
        if not isinstance(entry, dict):
            raise GateError("baseline path entry must be an object")
        rule = entry.get("rule")
        path_re = entry.get("path_re")
        if rule not in RULE_SEV or not isinstance(path_re, str):
            raise GateError("baseline path entry needs a known rule and path_re")
        if not entry.get("by") or not entry.get("reason"):
            raise GateError("baseline path entry needs by + reason (named acceptance)")
        try:
            compiled = re.compile(path_re)
        except re.error as e:
            raise GateError("baseline path_re does not compile: %s" % e)
        path_rules.append({"rule": rule, "re": compiled})
    return data["accepted"], path_rules
