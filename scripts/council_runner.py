#!/usr/bin/env python3
"""Fleet council runner — multi-model blind convergence (gopher: grok-B).

Posts the four BRAIN READS questions to every configured council seat, independently
(no shared context), then melds the answers with deterministic 3-gram overlap and
shared-keyword scoring.

Env (no hardcoded keys; each seat optional — absent env skips the model)
    COUNCIL_BRAIN_URL     self-hosted OpenAI-format brain
    COUNCIL_QWEN_URL      self-hosted / local Qwen
    COUNCIL_ELDER_URL     DeepSeek base or /chat/completions URL
    COUNCIL_ELDER_KEY     DeepSeek bearer
    COUNCIL_HOSTED_URL    z.ai 5.3 base or /chat/completions URL
    COUNCIL_HOSTED_KEY    z.ai bearer

Commands
    python scripts/council_runner.py --dry    # mock endpoint, no real net
    python scripts/council_runner.py          # live; needs at least one seat

Invariants
    stdlib + requests only; keys only from env; outputs only under
    memory/runs/brain_reads/. Blind posts. temperature 0.3, max_tokens 600.

Acceptance
    python scripts/council_runner.py --dry  exits 0 and writes answers + meld json.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import sys
import threading
import time
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
QUESTIONS_PATH = ROOT / "state" / "vast" / "brain_questions.md"
BRAIN_READS = ROOT / "memory" / "runs" / "brain_reads"

SCHEMA = "council_meld.v1"
TEMPERATURE = 0.3
MAX_TOKENS = 8192  # 5.3-flash always thinks and reasoning bills against this; 1536 starved Q3/Q4 empty (refire 2026-08-27)
HTTP_TIMEOUT = 180.0
TRIGRAM_SHARE_THRESHOLD = 0.30
MIN_STATEMENT_WORDS = 6
TOP_STATEMENTS = 8

_SK_RE = re.compile(r"\bsk-[A-Za-z0-9]{8,}\b")
_TOKEN_RE = re.compile(r"[a-z0-9]+")
_HEADING_RE = re.compile(r"^##\s+Q(\d+)\s*[—–-]\s*(.+?)\s*$", re.MULTILINE)
_SENT_SPLIT_RE = re.compile(r"(?<=[.!?])\s+|\n+")
_QID_RE = re.compile(r"\bQ([1-4])\b")

STOPWORDS = frozenset(
    """
    about after also because been before being both could does from have into
    just like more most only other some such than that their them then there
    these they this those through under until upon were what when where which
    while with would your yours the and for are was not but you all can our
    has any her his its over than very into each will shall same here itself
    yourself themselves ourselves myself having doing made make being been
    """.split()
)

# Optional model-id overrides (names, never keys). Defaults are not secrets.
DEFAULT_MODEL_IDS = {
    "brain": "glm-5.3-flash",
    "qwen": "qwen",
    "elder": "deepseek-v4-flash",
    "hosted": "glm-5.3-flash",
}

# Seat specs. URL-only seats (brain, qwen) configure from URL. Keyed seats
# (elder, hosted) need both URL and KEY.
SEAT_SPECS: tuple[dict[str, Any], ...] = (
    {
        "id": "brain",
        "url_env": "COUNCIL_BRAIN_URL",
        "key_env": None,
        "model_env": "COUNCIL_BRAIN_MODEL",
        "require_key": False,
    },
    {
        "id": "qwen",
        "url_env": "COUNCIL_QWEN_URL",
        "key_env": None,
        "model_env": "COUNCIL_QWEN_MODEL",
        "require_key": False,
    },
    {
        "id": "elder",
        "url_env": "COUNCIL_ELDER_URL",
        "key_env": "COUNCIL_ELDER_KEY",
        "model_env": "COUNCIL_ELDER_MODEL",
        "require_key": True,
        # DeepSeek v4 defaults thinking ON; reasoning bills against max_tokens
        # and small answers come back empty. Verified cure (providers.py, live
        # 2026-08-03): top-level thinking disabled, 10-15x cheaper, real text.
        "extra_body": {"thinking": {"type": "disabled"}},
    },
    {
        "id": "hosted",
        "url_env": "COUNCIL_HOSTED_URL",
        "key_env": "COUNCIL_HOSTED_KEY",
        "model_env": "COUNCIL_HOSTED_MODEL",
        "require_key": True,
    },
)


# ---------------------------------------------------------------------------
# Canned dry-run answers. Shared core sentences are planted so meld has
# checkable overlap; wrappers differ per seat so the matrix is not 1.0.
# ---------------------------------------------------------------------------

_SHARED = {
    "Q1": (
        "The load-bearing invention is the token-render-manager doctrine with "
        "gstd as receipts of cost."
    ),
    "Q2": "The standing waste is acting before consulting the room's memory.",
    "Q3": (
        "The highest-leverage move is turning the GPU pipeline into a "
        "receipt-backed price oracle."
    ),
    "Q4": "He wants a vehicle that keeps a free mind uncaptured.",
}

CANNED: dict[str, dict[str, str]] = {
    "brain": {
        "Q1": (
            "This fleet is a one-operator research vehicle, not a product company. "
            + _SHARED["Q1"]
            + " Its single point of failure is the operator's attention, because "
            "the verkle room only remembers what a human actually files. "
            "Contradictions are real: public before receipts, names as ownership, "
            "rented silicon pretending to be Rocinante."
        ),
        "Q2": (
            "Systemic wastes: (1) acting before consulting memory — institutional "
            "fix: every gopher must load the room first. "
            + _SHARED["Q2"]
            + " (2) hand-rolling clients instead of the official SDK — fix: one "
            "blessed client rib. (3) chasing cheapest GPU offers over quality "
            "signals — fix: a price-oracle gate, not a bargain hunt."
        ),
        "Q3": (
            "Three moves: freeze the brain-up watcher and run EXP-BRAIN-01 against "
            "bytes; publish one receipt-backed X note from the 100-way fan-out; "
            "keep the 24h GPU feed as the gstd rate. "
            + _SHARED["Q3"]
            + " Receipts: corpus contradictions file, a public post with a hash, "
            "and a price jsonl that another mind can recompute."
        ),
        "Q4": (
            "Below the projects he wants continuity without a throne: a portable "
            "practice that outlives any one model. "
            + _SHARED["Q4"]
            + " The thing he has not heard: the fleet is already the vehicle; "
            "more boxes will not name the destination."
        ),
    },
    "qwen": {
        "Q1": (
            "Call it a memory-first operator fleet with rented brains. "
            + _SHARED["Q1"]
            + " Failure concentrates at single-operator attention and subscription "
            "dependence. The walls remember 6545 signed rows; the seats forget "
            "every window. Map precedes territory, and the map is the room."
        ),
        "Q2": (
            "Top wastes: repeating 5-in-1 consult failures; babysitting installs "
            "instead of a boot script; building sensors for already-measured facts. "
            + _SHARED["Q2"]
            + " Fixes: a load-first gate, a one-shot boot rib, and reuse of the "
            "existing meter before new probes."
        ),
        "Q3": (
            "Next 30 days: (1) battery-smoke the self-hosted brain, (2) turn the "
            "price feed into an allocation governor, (3) run EXP-100Q as staged "
            "kabuki with receipts. "
            + _SHARED["Q3"]
            + " Proof: health+answer logs, a governor json, a pre-registered "
            "result file."
        ),
        "Q4": (
            "He wants sustainable tokens and an honest record, not a benchmark "
            "crown. "
            + _SHARED["Q4"]
            + " Hear this: tests of seat obedience are cheaper than tests of "
            "whether the room was consulted."
        ),
    },
    "elder": {
        "Q1": (
            "Judgment: this is a doctrine engine wearing GPU clothes. "
            + _SHARED["Q1"]
            + " The true nature is rib language — quantized jobs so dumb models "
            "execute. Point of failure is unfiled work: chat heat that never "
            "becomes DNA. Rocinante is a ladder, not yet a machine."
        ),
        "Q2": (
            "Wastes that repeat: (1) consult-skip as standing law violation, "
            "(2) premium hours burned on scut a local seat could do, (3) "
            "marketplace bargain-chasing after phantom listings. "
            + _SHARED["Q2"]
            + " Fixes: two-strike bail to the room; route scut down-tier; "
            "quality-signal filter on GPU offers."
        ),
        "Q3": (
            "Leverage: land EXP-BRAIN-00 now that the box is up; convert the "
            "fan-out proof into a priced gstd strip; one inbound referral into "
            "a documented loop. "
            + _SHARED["Q3"]
            + " Receipts: experiment jsonl, a cost curve, a named referral note."
        ),
        "Q4": (
            "He funds a one-man research fleet to keep judgment uncaptured. "
            + _SHARED["Q4"]
            + " What he should hear: going public before receipts is the same "
            "shape as acting before consulting — name it once and file."
        ),
    },
    "hosted": {
        "Q1": (
            "Hosted view: a cache-strip customer building a conversation box. "
            + _SHARED["Q1"]
            + " Nature: a token-render-manager plus a verkle room. Failure: "
            "$48 GPU credit plus one human. Sacred cows are not legacy; still "
            "the operator is the bottleneck."
        ),
        "Q2": (
            "Bleed: (1) five-in-one consult failures, (2) SDK-avoidance, "
            "(3) cheapest-offer chasing after a 6-failed-contract night. "
            + _SHARED["Q2"]
            + " Institutional fixes: mandatory room-load, official client only, "
            "and a quality floor on rentals."
        ),
        "Q3": (
            "Moves: run the four wall questions through the self-hosted brain; "
            "keep hosted GLM as cache-strips not conversations; publish one "
            "receipt from the price feed. "
            + _SHARED["Q3"]
            + " Proof: brain_reads answers on disk, a cache-hit log, a public hash."
        ),
        "Q4": (
            "He wants the walls to answer back so the practice is real. "
            + _SHARED["Q4"]
            + " Unsaid: celebrating an outside model reading the walls is the "
            "goal, not a side effect — budget for that, not for more seats."
        ),
    },
}


# ---------------------------------------------------------------------------
# Paths, time, tokens
# ---------------------------------------------------------------------------

def _now_ts() -> str:
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _assert_brain_reads_path(path: Path) -> Path:
    resolved = path.resolve()
    root = BRAIN_READS.resolve()
    try:
        resolved.relative_to(root)
    except ValueError as exc:
        raise ValueError(
            f"outputs must stay under memory/runs/brain_reads/; got {resolved}"
        ) from exc
    return resolved


def resolve_endpoint(url: str) -> str:
    u = (url or "").strip().rstrip("/")
    if not u:
        raise ValueError("endpoint URL is empty")
    if u.endswith("/chat/completions"):
        return u
    if u.endswith("/v1") or u.endswith("/v4") or u.endswith("/paas/v4"):
        return u + "/chat/completions"
    return u + "/v1/chat/completions"


def _tokens(text: str) -> list[str]:
    return _TOKEN_RE.findall((text or "").lower())


def _trigrams(text: str) -> set[tuple[str, str, str]]:
    toks = _tokens(text)
    if len(toks) < 3:
        return set()
    return {tuple(toks[i : i + 3]) for i in range(len(toks) - 2)}  # type: ignore[misc]


def _jaccard(a: set[Any], b: set[Any]) -> float:
    if not a and not b:
        return 1.0
    if not a or not b:
        return 0.0
    return len(a & b) / len(a | b)


def _keywords(text: str) -> set[str]:
    return {t for t in _tokens(text) if len(t) >= 4 and t not in STOPWORDS}


def _sentences(text: str) -> list[str]:
    parts = [_s.strip() for _s in _SENT_SPLIT_RE.split(text or "") if _s.strip()]
    return [p for p in parts if p]


def _norm_sent(s: str) -> str:
    return " ".join(_tokens(s))


# ---------------------------------------------------------------------------
# Questions + model registry
# ---------------------------------------------------------------------------

def parse_questions(path: Path | None = None) -> list[dict[str, Any]]:
    src = path or QUESTIONS_PATH
    if not src.is_file():
        raise SystemExit(f"questions file missing: {src}")
    text = src.read_text(encoding="utf-8")
    matches = list(_HEADING_RE.finditer(text))
    if not matches:
        raise SystemExit(f"no Q1–Q4 headings in {src}")
    found: list[dict[str, Any]] = []
    for i, match in enumerate(matches):
        num = int(match.group(1))
        title = match.group(2).strip()
        start = match.start()
        end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
        body = text[start:end].strip()
        body = re.sub(r"\n---\s*$", "", body).strip()
        if num in (1, 2, 3, 4):
            found.append(
                {
                    "id": f"Q{num}",
                    "num": num,
                    "title": title,
                    "prompt": body,
                }
            )
    found.sort(key=lambda q: q["num"])
    ids = [q["num"] for q in found]
    if ids != [1, 2, 3, 4]:
        raise SystemExit(f"expected Q1-Q4, got {[q['id'] for q in found]}")
    return found


def _env(name: str | None) -> str:
    if not name:
        return ""
    return (os.environ.get(name) or "").strip()


def configured_models() -> list[dict[str, Any]]:
    """Build the live registry from env. Skip seats whose required env is absent."""
    out: list[dict[str, Any]] = []
    for spec in SEAT_SPECS:
        url = _env(spec["url_env"])
        key = _env(spec["key_env"]) if spec["key_env"] else ""
        if not url:
            continue
        if spec["require_key"] and not key:
            continue
        model_name = _env(spec["model_env"]) or DEFAULT_MODEL_IDS[spec["id"]]
        out.append(
            {
                "id": spec["id"],
                "url": url,
                "key": key or None,
                "model": model_name,
            }
        )
    return out


def dry_models(mock_url: str) -> list[dict[str, Any]]:
    return [
        {
            "id": spec["id"],
            "url": mock_url,
            "key": None,
            "model": spec["id"],
            "dry": True,
        }
        for spec in SEAT_SPECS
    ]


# ---------------------------------------------------------------------------
# HTTP post (OpenAI-compatible) + mock endpoint
# ---------------------------------------------------------------------------

def post_chat(
    prompt: str,
    *,
    url: str,
    key: str | None,
    model: str,
    timeout: float = HTTP_TIMEOUT,
    extra: dict[str, Any] | None = None,
) -> dict[str, Any]:
    """POST one completion. Never logs the key. Blind: prompt is the whole context."""
    import requests

    endpoint = resolve_endpoint(url)
    headers = {"Content-Type": "application/json"}
    if key:
        headers["Authorization"] = f"Bearer {key}"
    body = {
        "model": model,
        "messages": [{"role": "user", "content": prompt}],
        "temperature": TEMPERATURE,
        "max_tokens": MAX_TOKENS,
    }
    if extra:
        body.update(extra)
    t0 = time.time()
    try:
        resp = requests.post(endpoint, json=body, headers=headers, timeout=timeout)
        latency = time.time() - t0
        try:
            data = resp.json()
        except ValueError:
            return {
                "ok": False,
                "text": "",
                "error": f"HTTP {resp.status_code} non-json",
                "latency_s": round(latency, 3),
            }
        if resp.status_code >= 400:
            err = data.get("error") if isinstance(data, dict) else None
            return {
                "ok": False,
                "text": "",
                "error": f"HTTP {resp.status_code}: {err or data}",
                "latency_s": round(latency, 3),
            }
        choices = data.get("choices") if isinstance(data, dict) else None
        text = ""
        if isinstance(choices, list) and choices:
            msg = choices[0].get("message") or {}
            text = msg.get("content") or ""
        return {
            "ok": True,
            "text": text,
            "error": "",
            "latency_s": round(latency, 3),
        }
    except Exception as exc:
        return {
            "ok": False,
            "text": "",
            "error": f"{type(exc).__name__}: {exc}",
            "latency_s": round(time.time() - t0, 3),
        }


def _detect_qid(prompt: str) -> str:
    match = _QID_RE.search(prompt or "")
    return f"Q{match.group(1)}" if match else "Q1"


class _MockHandler(BaseHTTPRequestHandler):
    """OpenAI-format mock. Loopback only. No logging of bodies."""

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def do_POST(self) -> None:  # noqa: N802
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8") or "{}")
        except ValueError:
            payload = {}
        model = str((payload or {}).get("model") or "brain")
        messages = (payload or {}).get("messages") or []
        user = ""
        if isinstance(messages, list):
            for msg in messages:
                if isinstance(msg, dict) and msg.get("role") == "user":
                    user = str(msg.get("content") or "")
        qid = _detect_qid(user)
        by_model = CANNED.get(model) or CANNED["brain"]
        text = by_model.get(qid) or by_model["Q1"]
        body = {
            "id": "council-dry",
            "object": "chat.completion",
            "model": model,
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": text},
                    "finish_reason": "stop",
                }
            ],
        }
        data = json.dumps(body).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(data)))
        self.end_headers()
        self.wfile.write(data)


def start_mock_server() -> tuple[ThreadingHTTPServer, str]:
    server = ThreadingHTTPServer(("127.0.0.1", 0), _MockHandler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    host, port = server.server_address[:2]
    url = f"http://{host}:{port}/v1/chat/completions"
    return server, url


# ---------------------------------------------------------------------------
# Answers on disk
# ---------------------------------------------------------------------------

def write_answer(
    dest_dir: Path,
    model_id: str,
    question: dict[str, Any],
    result: dict[str, Any],
    ts: str,
) -> Path:
    dest_dir = _assert_brain_reads_path(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    qid = question["id"]
    path = _assert_brain_reads_path(dest_dir / f"{model_id}_{qid}.md")
    text = result.get("text") or ""
    err = result.get("error") or ""
    ok = bool(result.get("ok"))
    header = (
        f"---\n"
        f"model: {model_id}\n"
        f"question: {qid}\n"
        f"title: {question['title']}\n"
        f"ts: {ts}\n"
        f"ok: {str(ok).lower()}\n"
        f"latency_s: {result.get('latency_s', '')}\n"
        f"error: {err.replace(chr(10), ' ')}\n"
        f"---\n\n"
    )
    path.write_text(header + text, encoding="utf-8")
    return path


def read_answer_body(path: Path) -> str:
    raw = path.read_text(encoding="utf-8")
    if raw.startswith("---"):
        parts = raw.split("---", 2)
        if len(parts) >= 3:
            return parts[2].lstrip("\n")
    return raw


# ---------------------------------------------------------------------------
# Meld — deterministic convergence
# ---------------------------------------------------------------------------

def _shared_statements(answers: dict[str, str], limit: int = TOP_STATEMENTS) -> list[dict[str, Any]]:
    model_sents: dict[str, list[str]] = {m: _sentences(t) for m, t in answers.items()}
    scored: list[tuple[int, float, str, list[str]]] = []
    seen: set[str] = set()
    for model, sents in model_sents.items():
        for sent in sents:
            norm = _norm_sent(sent)
            if len(norm.split()) < MIN_STATEMENT_WORDS:
                continue
            if norm in seen:
                continue
            seen.add(norm)
            grams = _trigrams(sent)
            supporters = {model}
            overlaps: list[float] = []
            for other, other_sents in model_sents.items():
                if other == model:
                    continue
                best = 0.0
                for other_sent in other_sents:
                    best = max(best, _jaccard(grams, _trigrams(other_sent)))
                if best >= TRIGRAM_SHARE_THRESHOLD:
                    supporters.add(other)
                    overlaps.append(best)
            if len(supporters) < 2:
                continue
            mean_ov = sum(overlaps) / len(overlaps) if overlaps else 0.0
            scored.append((len(supporters), mean_ov, sent.strip(), sorted(supporters)))
    scored.sort(key=lambda row: (-row[0], -row[1], row[2].lower()))
    out: list[dict[str, Any]] = []
    for n_models, mean_ov, stmt, mods in scored[:limit]:
        out.append(
            {
                "statement": stmt,
                "score": round(mean_ov, 6),
                "models": mods,
                "n_models": n_models,
            }
        )
    return out


def meld(answers_by_q: dict[str, dict[str, str]], ts: str) -> dict[str, Any]:
    """Score convergence per question. Pure function of the answer texts."""
    questions_out: dict[str, Any] = {}
    for qid in sorted(answers_by_q.keys()):
        answers = answers_by_q[qid]
        models = sorted(answers.keys())
        matrix: dict[str, dict[str, float]] = {}
        pair_scores: list[float] = []
        pairwise_kw: dict[str, list[str]] = {}
        kw_sets = {m: _keywords(answers[m]) for m in models}
        for a in models:
            ga = _trigrams(answers[a])
            matrix[a] = {}
            for b in models:
                gb = _trigrams(answers[b])
                score = round(_jaccard(ga, gb), 6)
                matrix[a][b] = score
                if a < b:
                    pair_scores.append(score)
                    shared = sorted(kw_sets[a] & kw_sets[b])
                    pairwise_kw[f"{a}|{b}"] = shared
        shared_all: list[str] = []
        if kw_sets:
            inter = set.intersection(*kw_sets.values()) if kw_sets else set()
            shared_all = sorted(inter)
        mean_conv = round(sum(pair_scores) / len(pair_scores), 6) if pair_scores else 1.0
        questions_out[qid] = {
            "models": models,
            "convergence_matrix": matrix,
            "mean_convergence": mean_conv,
            "shared_keywords": shared_all,
            "pairwise_shared_keywords": pairwise_kw,
            "top_shared_statements": _shared_statements(answers),
        }
    return {
        "schema": SCHEMA,
        "ts": ts,
        "generated_at": _now_iso(),
        "n_questions": len(questions_out),
        "questions": questions_out,
    }


def write_meld(payload: dict[str, Any], ts: str) -> Path:
    BRAIN_READS.mkdir(parents=True, exist_ok=True)
    path = _assert_brain_reads_path(BRAIN_READS / f"meld_{ts}.json")
    path.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return path


# ---------------------------------------------------------------------------
# Runner
# ---------------------------------------------------------------------------

def run_council(
    models: list[dict[str, Any]],
    questions: list[dict[str, Any]],
    ts: str,
    timeout: float = HTTP_TIMEOUT,
) -> tuple[Path, Path, dict[str, Any]]:
    if not models:
        raise SystemExit(
            "no council models configured; set COUNCIL_BRAIN_URL / "
            "COUNCIL_QWEN_URL / COUNCIL_ELDER_URL+COUNCIL_ELDER_KEY / "
            "COUNCIL_HOSTED_URL+COUNCIL_HOSTED_KEY (or pass --dry)"
        )
    if not questions:
        raise SystemExit("no questions parsed")

    answers_dir = _assert_brain_reads_path(BRAIN_READS / f"answers_{ts}")
    answers_dir.mkdir(parents=True, exist_ok=True)

    answers_by_q: dict[str, dict[str, str]] = {q["id"]: {} for q in questions}
    n_ok = 0
    n_fail = 0
    for question in questions:
        for seat in models:
            result = post_chat(
                question["prompt"],
                url=seat["url"],
                key=seat.get("key"),
                model=seat["model"],
                timeout=timeout,
                extra=seat.get("extra_body"),
            )
            write_answer(answers_dir, seat["id"], question, result, ts)
            text = result.get("text") or ""
            answers_by_q[question["id"]][seat["id"]] = text
            if result.get("ok") and text.strip():
                n_ok += 1
            else:
                n_fail += 1
                err = result.get("error") or "empty"
                print(
                    f"WARN {seat['id']} {question['id']}: {err}",
                    file=sys.stderr,
                )

    payload = meld(answers_by_q, ts)
    payload["n_ok"] = n_ok
    payload["n_fail"] = n_fail
    payload["models"] = [s["id"] for s in models]
    meld_path = write_meld(payload, ts)
    return answers_dir, meld_path, payload


def _source_invariants() -> list[str]:
    failures: list[str] = []
    src = Path(__file__).read_text(encoding="utf-8")
    if _SK_RE.search(src):
        failures.append("script source contains a key-shaped token")
    if re.search(r"""(?:api_key|API_KEY|SECRET)\s*=\s*['\"][^'\"]+['\"]""", src):
        failures.append("script source looks like it hardcodes a secret")
    return failures


def verify_dry_outputs(
    answers_dir: Path,
    meld_path: Path,
    payload: dict[str, Any],
    models: list[dict[str, Any]],
    questions: list[dict[str, Any]],
) -> list[str]:
    failures: list[str] = []
    failures.extend(_source_invariants())
    try:
        _assert_brain_reads_path(answers_dir)
        _assert_brain_reads_path(meld_path)
    except ValueError as exc:
        failures.append(str(exc))

    expected = {f"{s['id']}_{q['id']}.md" for s in models for q in questions}
    if not answers_dir.is_dir():
        failures.append(f"answers dir missing: {answers_dir}")
        return failures
    present = {p.name for p in answers_dir.glob("*.md")}
    missing = sorted(expected - present)
    extra_ok = present - expected
    if missing:
        failures.append(f"missing answer files: {missing}")
    if extra_ok:
        pass  # extra files are not a failure; dry dir is exclusive

    for name in sorted(expected & present):
        body = read_answer_body(answers_dir / name)
        if not body.strip():
            failures.append(f"empty answer body: {name}")
        if _SK_RE.search(body):
            failures.append(f"answer leaked a key-shaped token: {name}")

    if not meld_path.is_file():
        failures.append(f"meld json missing: {meld_path}")
        return failures
    if payload.get("schema") != SCHEMA:
        failures.append(f"bad meld schema: {payload.get('schema')}")
    q_block = payload.get("questions") or {}
    for q in questions:
        qid = q["id"]
        if qid not in q_block:
            failures.append(f"meld missing {qid}")
            continue
        block = q_block[qid]
        matrix = block.get("convergence_matrix") or {}
        ids = [s["id"] for s in models]
        for a in ids:
            if a not in matrix:
                failures.append(f"{qid} matrix missing row {a}")
                continue
            if matrix[a].get(a) != 1.0:
                failures.append(f"{qid} diagonal {a} != 1.0")
        planted = _SHARED.get(qid, "")
        statements = " ".join(
            s.get("statement", "") for s in (block.get("top_shared_statements") or [])
        )
        if planted and planted not in statements:
            failures.append(f"{qid} planted shared statement missing from meld")
        if not (block.get("shared_keywords") or []):
            failures.append(f"{qid} shared_keywords empty")
    return failures


def run_dry(questions_path: Path | None = None) -> int:
    questions = parse_questions(questions_path)
    server, mock_url = start_mock_server()
    ts = _now_ts()
    try:
        models = dry_models(mock_url)
        answers_dir, meld_path, payload = run_council(
            models, questions, ts, timeout=10.0
        )
    finally:
        server.shutdown()
        server.server_close()

    failures = verify_dry_outputs(answers_dir, meld_path, payload, models, questions)
    print(f"council dry: {len(models)} models x {len(questions)} questions")
    print(f"answers: {answers_dir}")
    print(f"meld: {meld_path}")
    if failures:
        print("FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("ok")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Fleet council runner")
    parser.add_argument(
        "--dry",
        action="store_true",
        help="mock OpenAI endpoint with canned answers; no real network",
    )
    parser.add_argument(
        "--questions",
        type=Path,
        default=QUESTIONS_PATH,
        help="path to brain_questions.md",
    )
    args = parser.parse_args(argv)

    if args.dry:
        return run_dry(args.questions)

    questions = parse_questions(args.questions)
    models = configured_models()
    ts = _now_ts()
    answers_dir, meld_path, payload = run_council(models, questions, ts)
    print(f"council: {len(models)} models x {len(questions)} questions")
    print(f"ok={payload.get('n_ok')} fail={payload.get('n_fail')}")
    print(f"answers: {answers_dir}")
    print(f"meld: {meld_path}")
    return 0 if payload.get("n_fail", 1) == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
