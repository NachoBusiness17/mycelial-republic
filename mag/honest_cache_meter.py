#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
honest_cache_meter.py
=====================

Per-response capture of input / cache-read / cache-write / output tokens, four
headline numbers per UTC day, and a nightly reconciliation job against the
provider invoice.

The four reported numbers
-------------------------
  HIT_tok          = sum(cache_read_tokens)
                     / sum(input_tokens + cache_read_tokens + cache_write_tokens)
                     (token-weighted; 0-safe)

  SAVINGS_dollars  = counterfactual_no_cache_cost - metered_cost
                     where the counterfactual bills EVERY input token (i, r, w)
                     at the full input rate. Net of the cache-WRITE premium, so
                     an honest meter can and will report NEGATIVE savings on
                     write-heavy days.

  coverage         = #{responses with cache_read_tokens > 0} / #{responses}
                     (request-weighted complement to token-weighted HIT_tok;
                     token_coverage = (r+w)/(i+r+w) is also emitted)

  reconciliation   = metered_usd - invoiced_usd  (absolute USD and % of invoice)
                     compared nightly; drift beyond a threshold exits non-zero
                     so cron/systemd can page a human.

Honesty rules enforced by construction
--------------------------------------
  1. Tokens are NEVER estimated. Only provider-reported usage from the actual
     response body is recorded, and the raw usage blob is stored verbatim.
  2. Every response the process sees is either captured or explicitly counted
     in `capture_failures`. Silent drops are impossible.
  3. Retries/replays are deduped on the provider response id; duplicates are
     COUNTED (capture_duplicates), not silently discarded.
  4. Spend is priced through snapshotted rate cards so historical recomputation
     matches what the provider actually charged at the time.
  5. Reconciliation drift fails loudly (nonzero exit code).

Stdlib only. Python >= 3.9.

Usage
-----
  # Instrument a call (Anthropic):
  #   resp = client.messages.create(...)
  #   capture_anthropic_response(meter, model, resp)
  #
  # Instrument a call (OpenAI):
  #   resp = client.chat.completions.create(...)
  #   capture_openai_response(meter, model, resp)
  #
  # Pipe a raw response body in:
  #   cat resp.json | python honest_cache_meter.py capture \
  #       --provider anthropic --model claude-sonnet-4-5
  #
  # One-off numbers for a day:
  #   python honest_cache_meter.py report --day 2025-06-01
  #
  # Load the provider invoice line for a day, then reconcile:
  #   python honest_cache_meter.py invoice --day 2025-06-01 --amount 214.37
  #   python honest_cache_meter.py reconcile --day 2025-06-01
  #
  # Nightly daemon (or run reconcile from cron instead):
  #   python honest_cache_meter.py daemon
  #
  # Cron line:
  #   5 0 * * * python3 /opt/meter/honest_cache_meter.py reconcile >> /var/log/cache_meter.log 2>&1
  #
  # End-to-end synthetic demo:
  #   python honest_cache_meter.py demo

Exit codes (reconcile/daemon/demo): 0 OK · 1 usage-parse error · 2 drift beyond
threshold (or invoiced day with zero metered traffic) · 3 no invoice loaded.
"""

from __future__ import annotations

import argparse
import json
import os
import random
import sqlite3
import sys
import time
import uuid
from dataclasses import asdict, dataclass
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple

UTC = timezone.utc
DEFAULT_DB = os.environ.get("CACHE_METER_DB", "cache_meter.db")

EXIT_OK = 0
EXIT_PARSE = 1
EXIT_DRIFT = 2
EXIT_NO_INVOICE = 3


# --------------------------------------------------------------------------
# Small utilities
# --------------------------------------------------------------------------

def log(msg: str) -> None:
    print(f"[{datetime.now(UTC).isoformat(timespec='seconds')}] {msg}", file=sys.stderr)


def utc_now_iso() -> str:
    return datetime.now(UTC).isoformat(timespec="microseconds").replace("+00:00", "Z")


def today_str() -> str:
    return datetime.now(UTC).date().isoformat()


def yesterday_str() -> str:
    return (datetime.now(UTC) - timedelta(days=1)).date().isoformat()


def fmt_money(x: Optional[float]) -> str:
    return "n/a" if x is None else f"${x:,.4f}"


def fmt_frac(x: Optional[float], signed: bool = False) -> str:
    if x is None:
        return "n/a"
    return f"{x * 100:+.2f}%" if signed else f"{x * 100:.2f}%"


# --------------------------------------------------------------------------
# Rate cards (snapshotted so historical math matches invoice-time pricing)
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class RateCard:
    name: str
    effective_from: str          # UTC date 'YYYY-MM-DD', inclusive
    input_per_mtok: float        # USD per million tokens
    output_per_mtok: float
    cache_read_per_mtok: float
    cache_write_per_mtok: float


DEFAULT_RATE_CARDS: List[RateCard] = [
    RateCard("default",           "1970-01-01", 3.00, 15.00, 0.30, 3.75),
    RateCard("anthropic-sonnet",  "1970-01-01", 3.00, 15.00, 0.30, 3.75),
    RateCard("openai-flagship",   "1970-01-01", 2.50, 10.00, 1.25, 2.50),
]

MODEL_PREFIX_TO_CARD: Tuple[Tuple[str, str], ...] = (
    ("claude", "anthropic-sonnet"),
    ("gpt", "openai-flagship"),
    ("o1", "openai-flagship"),
    ("o3", "openai-flagship"),
    ("o4", "openai-flagship"),
)


# --------------------------------------------------------------------------
# Usage normalization (never estimate — parse what the provider reported)
# --------------------------------------------------------------------------

@dataclass
class Usage:
    input_tokens: int = 0
    cache_read_tokens: int = 0
    cache_write_tokens: int = 0
    output_tokens: int = 0


class UsageParseError(ValueError):
    pass


def _dig(d: Dict[str, Any], *path: str, default: int = 0) -> int:
    cur: Any = d
    for k in path:
        if not isinstance(cur, dict) or k not in cur:
            return default
        cur = cur[k]
    try:
        return int(cur or 0)
    except (TypeError, ValueError):
        return default


def normalize_usage(payload: Dict[str, Any]) -> Usage:
    """Normalize Anthropic / OpenAI usage shapes into Usage. Raises otherwise."""
    u = payload.get("usage", payload)
    if not isinstance(u, dict) or not u:
        raise UsageParseError("payload has no usage object")

    # Anthropic Messages API: flat cache_*_input_tokens keys.
    if any(k in u for k in ("cache_read_input_tokens", "cache_creation_input_tokens")) or (
        "input_tokens" in u and "output_tokens" in u and "prompt_tokens" not in u
        and "input_tokens_details" not in u
    ):
        return Usage(
            input_tokens=max(0, _dig(u, "input_tokens")),
            cache_read_tokens=max(0, _dig(u, "cache_read_input_tokens")),
            cache_write_tokens=max(0, _dig(u, "cache_creation_input_tokens")),
            output_tokens=max(0, _dig(u, "output_tokens")),
        )

    # OpenAI Chat Completions: prompt_tokens + prompt_tokens_details.cached_tokens.
    pt = _dig(u, "prompt_tokens")
    if pt:
        cached = min(pt, max(0, _dig(u, "prompt_tokens_details", "cached_tokens")))
        return Usage(
            input_tokens=pt - cached,
            cache_read_tokens=cached,
            cache_write_tokens=0,   # OpenAI reports no separate write bucket
            output_tokens=max(0, _dig(u, "completion_tokens")),
        )

    # OpenAI Responses API: input_tokens + input_tokens_details.cached_tokens.
    it = _dig(u, "input_tokens")
    if it and "input_tokens_details" in u:
        cached = min(it, max(0, _dig(u, "input_tokens_details", "cached_tokens")))
        return Usage(
            input_tokens=it - cached,
            cache_read_tokens=cached,
            cache_write_tokens=0,
            output_tokens=max(0, _dig(u, "output_tokens")),
        )

    raise UsageParseError(f"unrecognized usage shape; keys={sorted(u)[:12]}")


def _payload_of(response: Any) -> Dict[str, Any]:
    if isinstance(response, dict):
        return response
    for meth in ("model_dump", "to_dict", "dict"):
        fn = getattr(response, meth, None)
        if callable(fn):
            try:
                out = fn()
                if isinstance(out, dict):
                    return out
            except TypeError:
                continue
    raise UsageParseError("cannot serialize response object to a dict")


# --------------------------------------------------------------------------
# Pricing math
# --------------------------------------------------------------------------

def cost_usd(card: RateCard, u: Usage) -> float:
    return (
        u.input_tokens * card.input_per_mtok
        + u.cache_read_tokens * card.cache_read_per_mtok
        + u.cache_write_tokens * card.cache_write_per_mtok
        + u.output_tokens * card.output_per_mtok
    ) / 1_000_000.0


def counterfactual_cost_usd(card: RateCard, u: Usage) -> float:
    """What the same tokens would have cost with caching disabled entirely."""
    total_in = u.input_tokens + u.cache_read_tokens + u.cache_write_tokens
    return (total_in * card.input_per_mtok + u.output_tokens * card.output_per_mtok) / 1_000_000.0


# --------------------------------------------------------------------------
# Storage
# --------------------------------------------------------------------------

SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS rate_cards (
  name           TEXT NOT NULL,
  effective_from TEXT NOT NULL,
  spec           TEXT NOT NULL,
  PRIMARY KEY (name, effective_from)
);

CREATE TABLE IF NOT EXISTS responses (
  seq                INTEGER PRIMARY KEY AUTOINCREMENT,
  ts                 TEXT NOT NULL,          -- ISO8601 UTC instant of the response
  day                TEXT NOT NULL,          -- UTC day bucket 'YYYY-MM-DD'
  provider           TEXT NOT NULL,
  model              TEXT NOT NULL,
  response_id        TEXT NOT NULL,
  has_provider_id    INTEGER NOT NULL DEFAULT 0,
  input_tokens       INTEGER NOT NULL,
  cache_read_tokens  INTEGER NOT NULL,
  cache_write_tokens INTEGER NOT NULL,
  output_tokens      INTEGER NOT NULL,
  rate_card          TEXT NOT NULL,
  billed_usd         REAL NOT NULL,
  raw_usage          TEXT NOT NULL,          -- verbatim provider usage JSON
  UNIQUE (provider, response_id)
);
CREATE INDEX IF NOT EXISTS idx_responses_day ON responses(day);

CREATE TABLE IF NOT EXISTS invoices (
  day          TEXT PRIMARY KEY,
  invoiced_usd REAL NOT NULL,
  source       TEXT NOT NULL,
  loaded_at    TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS reports (
  day        TEXT PRIMARY KEY,
  payload    TEXT NOT NULL,
  created_at TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS capture_failures (
  day    TEXT NOT NULL,
  reason TEXT NOT NULL,
  count  INTEGER NOT NULL DEFAULT 0,
  PRIMARY KEY (day, reason)
);

CREATE TABLE IF NOT EXISTS capture_duplicates (
  day   TEXT PRIMARY KEY,
  count INTEGER NOT NULL DEFAULT 0
);
"""


class CacheMeter:
    def __init__(self, db_path: str = DEFAULT_DB):
        self.db_path = str(db_path)
        self.conn = sqlite3.connect(self.db_path, isolation_level=None)
        self.conn.executescript(SCHEMA_SQL)
        for card