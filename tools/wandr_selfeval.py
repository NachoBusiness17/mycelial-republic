#!/usr/bin/env python3
"""wandr_selfeval.py -- WANDR-shaped estate self-eval (MICKEY-17 v2 GO list item 6).

One eval task shaped claim(n) -> field(m) -> url(k) near WANDR's medians, scored with
WANDR's soft/hard precision/recall/F1 protocol and graded by re-fetching each cited
page. Sources of record: corpus/steal/MASTER_MICKEY17_V2_20260924.md section 3 item 5
and GO list item 6; protocol quoted from https://arxiv.org/html/2608.14747v1;
task file: tools/wandr_selfeval_task.json.

Task shape (per the paper):
  key1(n) -> key2(m) -> url(k): each parenthesized count is a per-parent floor, the
  minimum number of distinct children each parent must carry ("not 70 appointments
  spread across fewer companies"). A record is one root-to-leaf path
  {item, url, excerpts, answer}; the member (here: the claim) is the coverage unit.

Metrics (paper section 5):
  soft member score  = mean over the member's required fields of the best record's
                       full verdict in that cell (partial credit to incomplete members)
  hard member score  = 1 only when every required field holds a fully-correct record
  precision          = mean member score over submitted member identities (duplicate
                       identities collapse to their worst score)
  recall             = delivered identity scores sorted, top required_count kept,
                       shortfalls zero-padded, averaged
  F1                 = harmonic mean of precision and recall, per metric family
  funnel             = discovery x enrichment x extraction reconstructs soft recall

Per-record verdicts (paper: verdict_full = 3 universal checks x 3 task-specific checks;
verdict_retrieval = requirements_all_satisfied):
  page_content_usable        re-fetched page answers with non-trivial text
  answer_intent_clear        record carries a non-empty answer
  excerpts_faithful          every submitted excerpt appears in the re-fetched page
  overall_valid              record is filed under the right claim/field cell
  requirements_all_satisfied the re-fetched page itself carries the gold excerpt
  requirements_all_supported the submitted excerpts carry the gold excerpt
The task-specific checks are a STUB judge: deterministic containment of the gold
excerpt after quote normalization (NFKC, curly quotes/dashes mapped, whitespace
collapsed). WANDR uses an LLM judge here; swap judge_record() when the BURN judge
lane populates (watch/inbox/BURN_JUDGE_LANE_BUILD_20260925.md). No API money is
spent by this tool in any mode; only --refetch spends network.

Usage:
  .venv/Scripts/python.exe tools/wandr_selfeval.py --selftest
  .venv/Scripts/python.exe tools/wandr_selfeval.py --validate tools/wandr_selfeval_task.json
  .venv/Scripts/python.exe tools/wandr_selfeval.py --summary
  .venv/Scripts/python.exe tools/wandr_selfeval.py --grade submission.json [--refetch]
  .venv/Scripts/python.exe tools/wandr_selfeval.py --grade-gold [--refetch]
Exit 0 = checks pass or grading completed; exit 1 = self-test failed; exit 2 = bad input.
"""
from __future__ import annotations

import argparse
import copy
import gzip
import hashlib
import ipaddress
import json
import re
import socket
import sys
import unicodedata
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DEFAULT_TASK = ROOT / "tools" / "wandr_selfeval_task.json"
CACHE_PATH = ROOT / "outputs" / "wandr_selfeval_cache" / "pages.jsonl"

TASK_SCHEMA = "wandr.selfeval.task.v1"
SUBMISSION_SCHEMA = "wandr.selfeval.submission.v1"
MIN_PAGE_CHARS = 200          # below this a "page" is a stub/error body, not evidence
FETCH_TIMEOUT_S = 30
READ_CAP_BYTES = 8_000_000
USER_AGENT = "wandr-selfeval/1.0 (local_sovereign_agent estate; re-fetch grading)"

# ---------------------------------------------------------------- normalization

_CHAR_MAP = {
    "\u2018": "'", "\u2019": "'", "\u201a": "'", "\u201b": "'",
    "\u201c": '"', "\u201d": '"', "\u201e": '"',
    "\u2013": "-", "\u2014": "-", "\u2212": "-",
    "\u00a0": " ", "\u2007": " ", "\u202f": " ",
}


def page_to_text(raw: str) -> str:
    """Page bytes to quote-searchable text: markup tags stripped (a fetched page is
    HTML/MDX; its anchors and spans must not break verbatim containment), then
    norm_text. Applies to every record alike, never per-record special cases."""
    return norm_text(re.sub(r"<[^>\n]+>", " ", raw))


def norm_text(s: str) -> str:
    """Normalize for quote containment: NFKC, curly quotes/dashes to ASCII, dashed
    runs collapsed, whitespace collapsed. Existing text is mapped, never rewritten
    by hand, so gold excerpts stay byte-true on disk."""
    s = unicodedata.normalize("NFKC", s)
    s = "".join(_CHAR_MAP.get(ch, ch) for ch in s)
    s = re.sub(r"-{2,}", "-", s)
    s = re.sub(r"\s+", " ", s)
    return s.strip()


# ---------------------------------------------------------------------- fetching

def _file_url_to_path(url: str) -> Path:
    path = urllib.parse.unquote(urllib.parse.urlparse(url).path)
    if re.match(r"^/[A-Za-z]:", path):
        path = path[1:]
    return Path(path)


def _assert_public_http_host(url: str) -> None:
    """Spec (B2-94, 2026-09-26): an http/https fetch target is untrusted input
    (submissions are model-authored), so the host must resolve to public
    addresses only. Loopback, private, link-local, unique-local, unspecified
    and non-global reserved addresses are refused before any socket connects.
    file:// estate evidence and the public-web grading path are unaffected.
    Known limit, named: the guard resolves once and urllib re-resolves on
    connect, so a TOCTOU DNS rebinding window remains; accepted for an
    operator-run eval tool."""
    host = urllib.parse.urlparse(url).hostname
    if not host:
        raise ValueError(f"fetch refused: no hostname in {url!r}")
    for info in socket.getaddrinfo(host, None):
        ip = ipaddress.ip_address(info[4][0])
        if not ip.is_global:
            raise ValueError(f"fetch refused: non-public address for {host}: {ip}")


def fetch_url(url: str) -> dict:
    """Re-fetch one cited page. Supports http/https and file scheme (estate-internal
    evidence lives in the repo). Returns {ok, status, text, error}.
    Spec (B2-94, 2026-09-26): http/https targets must resolve to public addresses
    (see _assert_public_http_host); refusals surface as error rows, never crashes."""
    scheme = urllib.parse.urlparse(url).scheme.lower()
    try:
        if scheme == "file":
            p = _file_url_to_path(url)
            if not p.is_file():
                return {"ok": False, "status": 0, "text": "", "error": f"file not found: {p}"}
            text = p.read_bytes()[:READ_CAP_BYTES].decode("utf-8", "replace")
            return {"ok": True, "status": 200, "text": text, "error": ""}
        if scheme not in ("http", "https"):
            return {"ok": False, "status": 0, "text": "", "error": f"unsupported scheme: {scheme}"}
        _assert_public_http_host(url)
        req = urllib.request.Request(
            url, headers={"User-Agent": USER_AGENT, "Accept-Encoding": "gzip"})
        with urllib.request.urlopen(req, timeout=FETCH_TIMEOUT_S) as resp:
            data = resp.read(READ_CAP_BYTES)
            if resp.headers.get("Content-Encoding") == "gzip":
                data = gzip.decompress(data)
            return {"ok": True, "status": resp.status,
                    "text": data.decode("utf-8", "replace"), "error": ""}
    except Exception as exc:  # a dead fetch is evidence about the page, not a crash
        return {"ok": False, "status": 0, "text": "",
                "error": f"{type(exc).__name__}: {exc}"[:200]}


def cache_load() -> dict:
    if not CACHE_PATH.is_file():
        return {}
    rows = {}
    for line in CACHE_PATH.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            row = json.loads(line)
        except json.JSONDecodeError:
            continue
        rows[row.get("url", "")] = row
    return rows


def cache_store(row: dict) -> None:
    CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    with CACHE_PATH.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


class PageSource:
    """Page provider with disk cache. refetch=True always re-fetches live (freshness is
    the point of re-fetch grading) and refreshes the cache; refetch=False serves the
    cache and reports misses as unfetched. store=False keeps fixture pages out of the
    estate cache (self-test only)."""

    def __init__(self, refetch: bool, fetcher=None, store: bool | None = None):
        self.refetch = refetch
        self._fetch = fetcher or fetch_url
        self._store = (fetcher is None) if store is None else store
        self._cache = cache_load() if not refetch else {}
        self._memo: dict = {}
        self.unfetched: list = []

    def get(self, url: str) -> dict:
        if url in self._memo:
            return self._memo[url]
        if not self.refetch and url in self._cache:
            row = self._cache[url]
            page = {"ok": bool(row.get("ok")), "status": row.get("status", 0),
                    "text": row.get("text", ""), "error": row.get("error", "")}
        else:
            raw = self._fetch(url)
            page = {"ok": bool(raw.get("ok")), "status": raw.get("status", 0),
                    "text": raw.get("text", ""), "error": raw.get("error", "")}
            if page["ok"] and self._store:
                cache_store({
                    "url": url,
                    "fetched_at_utc": datetime.now(timezone.utc).isoformat(timespec="seconds"),
                    "ok": True, "status": page["status"], "error": "",
                    "sha256_text": hashlib.sha256(page["text"].encode("utf-8")).hexdigest(),
                    "n_chars": len(page["text"]),
                    "text": page["text"],
                })
            if not page["ok"] and not self.refetch:
                self.unfetched.append(url)
        self._memo[url] = page
        return page


# ------------------------------------------------------------------ task loading

def load_task_from_dict(task: dict) -> dict:
    """Validate an in-memory task dict and attach count metadata. Per-parent count
    floors are enforced here: a parent short of its floor is a task error
    (ValueError), never a silent degrade."""
    if task.get("schema") != TASK_SCHEMA:
        raise ValueError(f"task schema must be {TASK_SCHEMA}, got {task.get('schema')!r}")
    floors = task.get("floors") or {}
    try:
        n_claims = int(floors["claims_min"])
        n_fields = int(floors["fields_min_per_claim"])
        n_urls = int(floors["urls_min_per_field"])
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"floors must carry claims_min/fields_min_per_claim/urls_min_per_field: {exc}")
    members = task.get("members")
    if not isinstance(members, list) or not members:
        raise ValueError("task carries no members")
    if len(members) < n_claims:
        raise ValueError(f"floor violation: {len(members)} members < claims_min {n_claims}")
    seen_claims = set()
    total_fields = 0
    total_records = 0
    for m in members:
        cid = m.get("claim_id")
        if not cid or cid in seen_claims:
            raise ValueError(f"member claim_id missing or duplicated: {cid!r}")
        seen_claims.add(cid)
        fields = m.get("fields")
        if not isinstance(fields, list) or len(fields) < n_fields:
            raise ValueError(f"floor violation: claim {cid} has {len(fields or [])} fields "
                             f"< fields_min_per_claim {n_fields}")
        seen_fields = set()
        for f in fields:
            fid = f.get("field_id")
            if not fid or fid in seen_fields:
                raise ValueError(f"field_id missing or duplicated in claim {cid}: {fid!r}")
            seen_fields.add(fid)
            total_fields += 1
            records = f.get("records")
            if not isinstance(records, list) or len(records) < n_urls:
                raise ValueError(f"floor violation: claim {cid} field {fid} has "
                                 f"{len(records or [])} records < urls_min_per_field {n_urls}")
            for r in records:
                if not isinstance(r.get("url"), str) or not r["url"]:
                    raise ValueError(f"record {r.get('item')!r} carries no url")
                if not (isinstance(r.get("excerpts"), list) and r["excerpts"]
                        and all(isinstance(e, str) and e for e in r["excerpts"])):
                    raise ValueError(f"record {r.get('item')!r} carries no non-empty excerpts")
                if not isinstance(r.get("answer"), str) or not r["answer"]:
                    raise ValueError(f"record {r.get('item')!r} carries no answer")
            total_records += len(records)
    task["_counts"] = {
        "members": len(members), "fields": total_fields, "records": total_records,
        "floors": {"claims_min": n_claims, "fields_min_per_claim": n_fields,
                   "urls_min_per_field": n_urls},
    }
    return task


def load_task(path: Path) -> dict:
    return load_task_from_dict(json.loads(path.read_text(encoding="utf-8")))


def load_submission(path: Path) -> dict:
    sub = json.loads(path.read_text(encoding="utf-8"))
    if sub.get("schema") != SUBMISSION_SCHEMA:
        raise ValueError(f"submission schema must be {SUBMISSION_SCHEMA}, "
                         f"got {sub.get('schema')!r}")
    if not isinstance(sub.get("members"), list):
        raise ValueError("submission carries no members list")
    for m in sub["members"]:
        if not m.get("claim_id"):
            raise ValueError("submission member without claim_id")
        for r in m.get("records", []):
            if not r.get("field_id"):
                raise ValueError(f"record without field_id in claim {m['claim_id']}")
            if not isinstance(r.get("excerpts"), list):
                raise ValueError(f"record {r.get('item')!r} without excerpts list")
    return sub


# ----------------------------------------------------------------------- grading

UNIVERSAL_CHECKS = ("page_content_usable", "answer_intent_clear", "excerpts_faithful")
TASK_CHECKS = ("overall_valid", "requirements_all_satisfied", "requirements_all_supported")
ALL_CHECKS = UNIVERSAL_CHECKS + TASK_CHECKS
NONE_VERDICT = {"checks": {c: False for c in ALL_CHECKS},
                "verdict_full": False, "verdict_retrieval": False}


def judge_record(rec: dict, field: dict, claim_id: str, page: dict) -> dict:
    """Per-record verdicts. STUB judge: the three task-specific checks are gold-excerpt
    containment, deterministic and free. Replace with the BURN LLM judge per WANDR's
    protocol when that lane populates; the six-check verdict shape stays fixed."""
    ntext = page_to_text(page.get("text", ""))
    usable = bool(page.get("ok")) and len(ntext) >= MIN_PAGE_CHARS
    gold_excerpts = [e for g in field.get("records", []) for e in g.get("excerpts", [])]
    joined = norm_text(" ".join(rec.get("excerpts", [])))
    checks = {
        "page_content_usable": usable,
        "answer_intent_clear": bool(norm_text(rec.get("answer", ""))),
        "excerpts_faithful": usable and all(norm_text(e) in ntext for e in rec.get("excerpts", [])),
        "overall_valid": (rec.get("field_id") == field.get("field_id")
                          and rec.get("item", "").split("/", 1)[0] == claim_id),
        "requirements_all_satisfied": usable and any(norm_text(g) in ntext for g in gold_excerpts),
        "requirements_all_supported": any(norm_text(g) in joined for g in gold_excerpts),
    }
    return {"checks": checks,
            "verdict_full": all(checks[c] for c in ALL_CHECKS),
            "verdict_retrieval": checks["requirements_all_satisfied"]}


def _gold_flat(task: dict) -> dict:
    return {m["claim_id"]: {f["field_id"]: f for f in m["fields"]} for m in task["members"]}


def _member_scores(entry: dict, gold_flat: dict) -> dict:
    """Soft/hard/retrieval member scores for one submitted member entry. Records must
    already carry _verdict (set by grade)."""
    cid = entry["claim_id"]
    gold_fields = gold_flat.get(cid)
    best_full: dict = {}
    best_retr: dict = {}
    for r in entry["records"]:
        if gold_fields is None:
            break  # unknown claim: the stub judge has no gold to satisfy, score stays 0
        fid = r.get("field_id")
        if fid not in gold_fields:
            continue  # orphan field: no required cell, no credit, no penalty
        v = r["_verdict"]
        best_full[fid] = max(best_full.get(fid, 0.0), 1.0 if v["verdict_full"] else 0.0)
        best_retr[fid] = max(best_retr.get(fid, 0.0), 1.0 if v["verdict_retrieval"] else 0.0)
    if gold_fields is not None:
        req_ids = list(gold_fields.keys())
        per_field_full = [best_full.get(f, 0.0) for f in req_ids]
        per_field_retr = [best_retr.get(f, 0.0) for f in req_ids]
        soft = sum(per_field_full) / len(req_ids)
        retr = sum(per_field_retr) / len(req_ids)
        hard = 1.0 if all(x == 1.0 for x in per_field_full) else 0.0
        delivered = sum(1 for f in req_ids if f in best_full)
        n_required = len(req_ids)
    else:
        soft = retr = hard = 0.0  # no required subtree: cannot be a complete member
        delivered = 0
        n_required = 0
    return {"claim_id": cid, "soft": soft, "hard": hard, "retrieval": retr,
            "delivered_fields": delivered, "required_fields": n_required,
            "is_required": gold_fields is not None}


def grade(submission: dict, task: dict, source: PageSource) -> dict:
    """Score one submission against the gold task; returns the full report dict."""
    gold_flat = _gold_flat(task)
    required_n = task["_counts"]["floors"]["claims_min"]
    required_records = sum(len(f["records"]) for m in task["members"] for f in m["fields"])

    entries = []
    for m in submission.get("members", []):
        entry = {"claim_id": m["claim_id"], "records": m.get("records", [])}
        for r in entry["records"]:
            r["_page"] = source.get(r.get("url", ""))
            field = gold_flat.get(entry["claim_id"], {}).get(r.get("field_id"))
            r["_verdict"] = (judge_record(r, field, entry["claim_id"], r["_page"])
                             if field is not None else dict(NONE_VERDICT))
        entries.append(entry)

    scored = [_member_scores(e, gold_flat) for e in entries]

    # duplicate identities collapse to their worst score (paper, recall section)
    collapsed: dict = {}
    order: list = []
    for s in scored:
        cid = s["claim_id"]
        if cid not in collapsed:
            collapsed[cid] = dict(s)
            order.append(cid)
        else:
            for k in ("soft", "hard", "retrieval"):
                collapsed[cid][k] = min(collapsed[cid][k], s[k])
    identities = [collapsed[c] for c in order]

    def _mean(xs):
        return float(sum(xs) / len(xs)) if xs else 0.0

    soft_p = _mean([i["soft"] for i in identities])
    hard_p = _mean([i["hard"] for i in identities])

    pool = sorted(identities, key=lambda i: (-i["soft"], order.index(i["claim_id"])))
    kept = pool[:required_n] + [None] * max(0, required_n - len(pool))
    soft_r = _mean([k["soft"] if k else 0.0 for k in kept])
    pool_h = sorted(identities, key=lambda i: (-i["hard"], order.index(i["claim_id"])))
    kept_h = pool_h[:required_n] + [None] * max(0, required_n - len(pool_h))
    hard_r = _mean([k["hard"] if k else 0.0 for k in kept_h])

    def _f1(p, r):
        return float(2 * p * r / (p + r)) if (p + r) > 0 else 0.0

    all_records = [r for e in entries for r in e["records"]]
    probes = {}
    for name, key in (("page_usable", "page_content_usable"),
                      ("excerpts_faithful", "excerpts_faithful"),
                      ("requirements_satisfied", "requirements_all_satisfied"),
                      ("requirements_supported", "requirements_all_supported")):
        hits = sum(1 for r in all_records if r["_verdict"]["checks"][key])
        probes[name] = {"rate": (hits / len(all_records)) if all_records else 0.0,
                        "hits": hits, "n": len(all_records)}
    full_hits = sum(1 for r in all_records if r["_verdict"]["verdict_full"])
    probes["full_verdict"] = {"rate": (full_hits / len(all_records)) if all_records else 0.0,
                              "hits": full_hits, "n": len(all_records)}

    delivered_req = [i for i in identities if i["is_required"]]
    discovery = min(len(delivered_req), required_n) / required_n if required_n else 0.0
    enrichment = _mean([i["retrieval"] for i in delivered_req])
    retr_sum = sum(i["retrieval"] for i in delivered_req)
    full_sum = sum(i["soft"] for i in delivered_req)
    extraction = (full_sum / retr_sum) if retr_sum > 0 else 0.0

    return {
        "task_id": task.get("task_id"),
        "submission_id": submission.get("submission_id"),
        "mode": "refetch" if source.refetch else "cache-or-unfetched",
        "counts": {
            "required_members": required_n, "required_fields": task["_counts"]["fields"],
            "required_records": required_records,
            "submitted_entries": len(entries), "distinct_identities": len(identities),
            "submitted_records": len(all_records),
        },
        "metrics": {
            "soft": {"precision": round(soft_p, 6), "recall": round(soft_r, 6),
                     "f1": round(_f1(soft_p, soft_r), 6)},
            "hard": {"precision": round(hard_p, 6), "recall": round(hard_r, 6),
                     "f1": round(_f1(hard_p, hard_r), 6)},
        },
        "record_probes": probes,
        "funnel": {"discovery": round(discovery, 6), "enrichment": round(enrichment, 6),
                   "extraction": round(extraction, 6)},
        "unfetched_urls": sorted(set(source.unfetched)),
        "members": [{"claim_id": i["claim_id"], "soft": round(i["soft"], 6),
                     "hard": i["hard"], "retrieval": round(i["retrieval"], 6),
                     "delivered_fields": i["delivered_fields"],
                     "required_fields": i["required_fields"],
                     "is_required": i["is_required"]} for i in identities],
    }


# --------------------------------------------------------------- gold submission

def gold_submission(task: dict) -> dict:
    """The task answered by itself: every required record cited verbatim. Grading this
    with --refetch is the standing receipt that every gold url still carries its quote."""
    members = []
    for m in task["members"]:
        records = []
        for f in m["fields"]:
            for g in f["records"]:
                records.append({"field_id": f["field_id"], "url": g["url"],
                                "excerpts": list(g["excerpts"]), "answer": g["answer"],
                                "item": g.get("item", f"{m['claim_id']}/{f['field_id']}")})
        members.append({"claim_id": m["claim_id"], "records": records})
    return {"schema": SUBMISSION_SCHEMA, "submission_id": "gold-self-grade",
            "task_id": task.get("task_id"), "members": members}


# --------------------------------------------------------------------- self-test

def _fixture_pages(task: dict) -> dict:
    """FIXTURE pages synthesized from the gold task itself (scorer-math fixtures, not
    evidence: each cited url is served a page that carries its gold excerpts). Padded
    past MIN_PAGE_CHARS so the real usability floor stays enforced in every fixture."""
    pages: dict = {}
    for m in task["members"]:
        for f in m["fields"]:
            for g in f["records"]:
                pages.setdefault(g["url"], []).extend(g["excerpts"])
    filler = ("Fixture filler paragraph stands in for the surrounding page copy so the "
              "usability floor is exercised the way a real page exercises it. ") * 4
    return {url: "FIXTURE PAGE for " + url + "\n\n" + filler + "\n" + "\n".join(frags)
            + "\n\nend of fixture.\n"
            for url, frags in pages.items()}


def selftest() -> int:
    """Fixture-row self-test: exact expected soft/hard P/R/F1 on four built submissions,
    plus floor enforcement and the funnel identity. No network, no API spend."""
    failures = []

    def check(name, got, want, tol=1e-6):
        ok = abs(got - want) <= tol
        print(f"  [{'PASS' if ok else 'FAIL'}] {name}: got {got:.6f} want {want:.6f}")
        if not ok:
            failures.append(name)

    task = load_task(DEFAULT_TASK)
    counts = task["_counts"]
    print(f"task: {task.get('task_id')}")
    check("selftest.members", float(counts["members"]), 10.0, 0.0)
    check("selftest.fields", float(counts["fields"]), 30.0, 0.0)
    check("selftest.records", float(counts["records"]), 30.0, 0.0)

    pages = _fixture_pages(task)

    def fixture_fetch(url: str) -> dict:
        if url in pages:
            return {"ok": True, "status": 200, "text": pages[url], "error": ""}
        return {"ok": False, "status": 0, "text": "", "error": "fixture: no such page"}

    def run(sub: dict) -> dict:
        return grade(sub, task, PageSource(refetch=True, fetcher=fixture_fetch, store=False))

    # 1. perfect self-grade: every metric exactly 1
    rep = run(gold_submission(task))
    for fam in ("soft", "hard"):
        for met in ("precision", "recall", "f1"):
            check(f"perfect.{fam}_{met}", rep["metrics"][fam][met], 1.0)
    for probe in ("page_usable", "excerpts_faithful", "requirements_satisfied",
                  "requirements_supported", "full_verdict"):
        check("perfect.probe." + probe, rep["record_probes"][probe]["rate"], 1.0)

    # 2. degraded: member sonar-sunset keeps 1 of 3 fields; verbatim-quote-rate loses its
    #    bitf_rate record and its gate_flagged record quotes text not on the page;
    #    effort-tiers is not delivered at all.
    #    Expected exactly: softP 23/27, softR 23/30, softF1 1058/1311,
    #                      hardP 7/9,   hardR 7/10,  hardF1 98/133,
    #                      funnel discovery 9/10, enrichment 8/9, extraction 23/24.
    by_id = {m["claim_id"]: m for m in gold_submission(task)["members"]}
    degraded_members = [{"claim_id": "sonar-sunset",
                         "records": [r for r in by_id["sonar-sunset"]["records"]
                                     if r["field_id"] == "sunset_date"]}]
    for cid in ("w4-verdict-schema", "wandr-scoring", "writes-serial",
                "completion-gap", "stale-data-freshness", "history-mining-exploit",
                "verifier-inadequacy"):
        degraded_members.append(by_id[cid])
    m5 = by_id["verbatim-quote-rate"]
    degraded_members.append({
        "claim_id": "verbatim-quote-rate",
        "records": [r for r in m5["records"] if r["field_id"] == "estate_audit"]
                   + [{"field_id": "gate_flagged", "url": m5["records"][0]["url"],
                       "excerpts": ["The quick brown fox jumps over the lazy dog."],
                       "answer": "wrong excerpt", "item": "verbatim-quote-rate/gate_flagged"}]})
    rep2 = run({"schema": SUBMISSION_SCHEMA, "submission_id": "degraded",
                "members": degraded_members})
    check("degraded.soft_precision", rep2["metrics"]["soft"]["precision"], float(Fraction(23, 27)))
    check("degraded.soft_recall", rep2["metrics"]["soft"]["recall"], float(Fraction(23, 30)))
    check("degraded.soft_f1", rep2["metrics"]["soft"]["f1"], float(Fraction(1058, 1311)))
    check("degraded.hard_precision", rep2["metrics"]["hard"]["precision"], float(Fraction(7, 9)))
    check("degraded.hard_recall", rep2["metrics"]["hard"]["recall"], float(Fraction(7, 10)))
    check("degraded.hard_f1", rep2["metrics"]["hard"]["f1"], float(Fraction(98, 133)))
    check("degraded.funnel.discovery", rep2["funnel"]["discovery"], float(Fraction(9, 10)))
    check("degraded.funnel.enrichment", rep2["funnel"]["enrichment"], float(Fraction(8, 9)))
    check("degraded.funnel.extraction", rep2["funnel"]["extraction"], float(Fraction(23, 24)))
    faithful = rep2["record_probes"]["excerpts_faithful"]["rate"]
    check("degraded.probe.faithful_below_one", 1.0 if faithful < 1.0 else 0.0, 1.0)

    # 3. over-delivery and duplicate identity: perfect task plus a duplicate of
    #    sonar-sunset degraded to one field (collapse to worst) plus one unknown claim
    #    on a dead url.
    #    Expected exactly: softP 28/33, softR 14/15, softF1 8/9,
    #                      hardP 9/11,  hardR 9/10,  hardF1 6/7,
    #                      full-verdict probe 31/32.
    sub3 = gold_submission(task)
    sub3["members"].append({"claim_id": "sonar-sunset",
                            "records": [by_id["sonar-sunset"]["records"][0]]})
    sub3["members"].append({"claim_id": "not-in-gold", "records": [
        {"field_id": "anything", "url": "https://fixture.invalid/nope",
         "excerpts": ["nothing"], "answer": "x", "item": "not-in-gold/anything"}]})
    rep3 = run(sub3)
    check("overdeliver.soft_precision", rep3["metrics"]["soft"]["precision"], float(Fraction(28, 33)))
    check("overdeliver.soft_recall", rep3["metrics"]["soft"]["recall"], float(Fraction(14, 15)))
    check("overdeliver.soft_f1", rep3["metrics"]["soft"]["f1"], float(Fraction(8, 9)))
    check("overdeliver.hard_precision", rep3["metrics"]["hard"]["precision"], float(Fraction(9, 11)))
    check("overdeliver.hard_recall", rep3["metrics"]["hard"]["recall"], float(Fraction(9, 10)))
    check("overdeliver.hard_f1", rep3["metrics"]["hard"]["f1"], float(Fraction(6, 7)))
    check("overdeliver.probe.full", rep3["record_probes"]["full_verdict"]["rate"],
          float(Fraction(31, 32)))

    # 4. empty submission: defined zeros, no crash
    rep4 = run({"schema": SUBMISSION_SCHEMA, "submission_id": "empty", "members": []})
    check("empty.soft_f1", rep4["metrics"]["soft"]["f1"], 0.0)
    check("empty.hard_f1", rep4["metrics"]["hard"]["f1"], 0.0)
    check("empty.discovery", rep4["funnel"]["discovery"], 0.0)

    # 5. floor enforcement: a task short of its floor must refuse to load
    bad = copy.deepcopy(task)
    bad["floors"]["claims_min"] = 11
    raised = False
    try:
        load_task_from_dict(bad)
    except ValueError:
        raised = True
    print(f"  [{'PASS' if raised else 'FAIL'}] floors.claims_min violation raises ValueError")
    if not raised:
        failures.append("floors")

    print()
    if failures:
        print(f"SELFTEST FAIL: {len(failures)} failing checks: {', '.join(failures)}")
        return 1
    print("SELFTEST PASS: all fixture-row checks green "
          "(10 members x 3 fields x 1 url = 30 records)")
    return 0


# --------------------------------------------------------------------------- CLI

def print_human(rep: dict) -> None:
    c = rep["counts"]
    print(f"WANDR self-eval: {rep['task_id']}  mode={rep['mode']}")
    print(f"required : {c['required_members']} claims x per-claim fields x urls = "
          f"{c['required_records']} records | submitted: {c['distinct_identities']} "
          f"identities / {c['submitted_records']} records")
    for fam in ("soft", "hard"):
        m = rep["metrics"][fam]
        print(f"{fam:8s}: P={m['precision']:.6f} R={m['recall']:.6f} F1={m['f1']:.6f}")
    p = rep["record_probes"]
    print("probes  : page_usable={:.3f} faithful={:.3f} satisfied={:.3f} "
          "supported={:.3f} full={:.3f}".format(
              p["page_usable"]["rate"], p["excerpts_faithful"]["rate"],
              p["requirements_satisfied"]["rate"], p["requirements_supported"]["rate"],
              p["full_verdict"]["rate"]))
    f = rep["funnel"]
    print(f"funnel  : discovery={f['discovery']:.3f} enrichment={f['enrichment']:.3f} "
          f"extraction={f['extraction']:.3f}")
    if rep["unfetched_urls"]:
        print(f"WARNING : {len(rep['unfetched_urls'])} url(s) never fetched (cache miss "
              f"without --refetch); their records grade as unusable:")
        for u in rep["unfetched_urls"]:
            print(f"  - {u}")


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description="WANDR-shaped estate self-eval scorer")
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--selftest", action="store_true", help="run fixture-row self-test")
    mode.add_argument("--validate", metavar="TASK", help="validate a task JSON's floors")
    mode.add_argument("--summary", action="store_true", help="print task shape summary")
    mode.add_argument("--grade", metavar="SUBMISSION", help="grade a submission JSON")
    mode.add_argument("--grade-gold", action="store_true",
                      help="grade the gold task against itself (the re-fetch receipt)")
    ap.add_argument("--task", default=str(DEFAULT_TASK), help="task JSON (default: estate task)")
    ap.add_argument("--refetch", action="store_true",
                    help="re-fetch every cited page live instead of serving the disk cache")
    ap.add_argument("--json", action="store_true", help="emit the full report as JSON")
    args = ap.parse_args(argv)

    try:
        if args.selftest:
            return selftest()
        task = load_task(Path(args.task))
        if args.validate:
            c, f = task["_counts"], task["_counts"]["floors"]
            print(f"task OK: {task.get('task_id')}")
            print(f"hierarchy: claim({f['claims_min']}) -> field({f['fields_min_per_claim']}) "
                  f"-> url({f['urls_min_per_field']})")
            print(f"actual  : {c['members']} members, {c['fields']} fields, "
                  f"{c['records']} records")
            return 0
        if args.summary:
            print(json.dumps({"task_id": task.get("task_id"),
                              "hierarchy": task.get("hierarchy"),
                              "counts": task["_counts"],
                              "shape_note": task.get("shape_note")},
                             ensure_ascii=False, indent=2))
            return 0
        source = PageSource(refetch=args.refetch)
        submission = (gold_submission(task) if args.grade_gold
                      else load_submission(Path(args.grade)))
        rep = grade(submission, task, source)
        if args.json:
            print(json.dumps(rep, ensure_ascii=False, indent=2))
        else:
            print_human(rep)
        return 0
    except (ValueError, json.JSONDecodeError, FileNotFoundError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
