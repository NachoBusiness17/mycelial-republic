#!/usr/bin/env python3
"""tools/sovereign/http_client.py - Sovereign Zero-Dependency HTTP Client & Kinematic Stream Filter.

Picasso Steal: Replaces external packages 'requests' and 'httpx' with pure
Python standard library (urllib.request, http.client, ssl, json, re).

Features:
- GET, POST, PUT, DELETE with headers, query params, JSON payloads, and form data.
- Built-in redirect following with loop protection.
- Resilient SSL context (automatically handles self-signed/intercept certs).
- Direct streaming support for zero-disk pipes (e.g. into rclone rcat).
- Response object mimicking standard requests/httpx API: .status_code, .text, .json(), .content, .ok.
- Kinematic Stream Linkage (Socket-level mechanical filter):
    * clean_reasoning_bleed(raw: str) -> str: strips <think> blocks and pre-transition thoughts.
    * sanitize_model_stream(raw: str) -> dict: mechanically bounds and extracts valid JSON objects.
    * SovereignResponse.extract_content(sanitize=True): bulletproof content extraction for LLM calls.
    * SovereignResponse.json(sanitize=True): auto-recovers from leaked reasoning tokens in JSON responses.
"""

from __future__ import annotations

import json
import re
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterator, Optional, Union


def clean_reasoning_bleed(raw_text: str) -> str:
    """Mechanical socket filter: strips leaked reasoning blocks and monologues."""
    if not raw_text:
        return ""
    # Strip explicit reasoning tags (<think>...</think>, <thought>...</thought>)
    cleaned = re.sub(r"(?is)<think>.*?</think>", "", raw_text)
    cleaned = re.sub(r"(?is)<thought>.*?</thought>", "", cleaned)
    # Strip common reasoning prefixes (Thinking Process: ..., Reasoning: ...)
    cleaned = re.sub(r"(?is)^(?:Thinking Process:|Reasoning:|Internal Monologue:).*?\n\n", "", cleaned.strip())
    # Strip markdown backtick enclosures if wrapped around JSON
    trimmed = cleaned.strip()
    if trimmed.startswith("```json") and trimmed.endswith("```"):
        trimmed = trimmed[7:-3].strip()
    elif trimmed.startswith("```") and trimmed.endswith("```"):
        trimmed = trimmed[3:-3].strip()
    return trimmed


def sanitize_model_stream(raw_payload: str) -> Any:
    """Kinematic Linkage: mechanically extracts and bounds valid JSON from contaminated streams."""
    cleaned = clean_reasoning_bleed(raw_payload)
    
    # 1. Direct parse attempt
    try:
        return json.loads(cleaned)
    except Exception:
        pass

    # 2. Extract first valid JSON object enclosure {...}
    obj_match = re.search(r"(\{.*\})", cleaned, re.DOTALL)
    if obj_match:
        try:
            return json.loads(obj_match.group(1))
        except Exception:
            pass

    # 3. Extract first valid JSON array enclosure [...]
    arr_match = re.search(r"(\[.*\])", cleaned, re.DOTALL)
    if arr_match:
        try:
            return json.loads(arr_match.group(1))
        except Exception:
            pass

    # If completely unparseable, raise descriptive error
    raise ValueError(f"Kinematic filter tripped: Stream contains no bounded JSON structure. Preview: {raw_payload[:120]}")


def is_reasoning_leaked(raw_text: str) -> bool:
    """Detects whether raw output contains un-sanitized internal reasoning tokens."""
    if not raw_text:
        return False
    low = raw_text.lower()
    return any(marker in low for marker in ["<think>", "</think>", "<thought>", "thinking process:", "reasoning:"])


class SovereignResponse:
    """Lightweight, transparent response object holding payload, headers, and kinematic filters."""

    def __init__(
        self,
        status_code: int,
        headers: Dict[str, str],
        content: bytes,
        url: str,
    ) -> None:
        self.status_code = status_code
        self.headers = headers
        self._content = content
        self.url = url

    @property
    def ok(self) -> bool:
        return 200 <= self.status_code < 400

    @property
    def content(self) -> bytes:
        return self._content

    @property
    def text(self) -> str:
        try:
            return self._content.decode("utf-8")
        except UnicodeDecodeError:
            return self._content.decode("utf-8", errors="replace")

    def json(self, sanitize: bool = False) -> Any:
        """Parses response as JSON. If sanitize=True or on parse error, applies kinematic linkage."""
        if sanitize:
            return sanitize_model_stream(self.text)
        try:
            return json.loads(self.text)
        except json.JSONDecodeError:
            # Automatic kinematic fallback before crashing
            return sanitize_model_stream(self.text)

    def extract_content(self, sanitize_thinking: bool = True) -> str:
        """Extracts choices[0].message.content from standard LLM endpoints, stripping token bleed."""
        payload = self.json(sanitize=False)
        if isinstance(payload, dict):
            choices = payload.get("choices", [])
            if choices and isinstance(choices[0], dict):
                msg = choices[0].get("message", {})
                content = msg.get("content", "")
                if sanitize_thinking:
                    return clean_reasoning_bleed(content)
                return content
        return self.text

    def has_thinking_bleed(self) -> bool:
        return is_reasoning_leaked(self.text)

    def __repr__(self) -> str:
        return f"<SovereignResponse [{self.status_code}] len={len(self._content)} url={self.url}>"


def _build_ssl_context(verify_ssl: bool = True) -> ssl.SSLContext:
    if verify_ssl:
        try:
            return ssl.create_default_context()
        except Exception:
            pass
    ctx = ssl._create_unverified_context()
    return ctx


def request(
    method: str,
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
    data: Optional[Union[Dict[str, Any], bytes, str]] = None,
    json_data: Optional[Any] = None,
    headers: Optional[Dict[str, str]] = None,
    timeout: float = 30.0,
    verify_ssl: bool = False,
    follow_redirects: bool = True,
) -> SovereignResponse:
    """Executes an HTTP request using strictly standard library urllib."""
    req_headers = {
        "User-Agent": "SovereignClient/1.0 (+estate invariant core; kinematic stream filter; zero-wheel)",
        "Accept": "*/*",
    }
    if headers:
        req_headers.update(headers)

    if params:
        query_str = urllib.parse.urlencode(params)
        sep = "&" if "?" in url else "?"
        url = f"{url}{sep}{query_str}"

    encoded_body: Optional[bytes] = None
    if json_data is not None:
        req_headers["Content-Type"] = "application/json"
        encoded_body = json.dumps(json_data).encode("utf-8")
    elif data is not None:
        if isinstance(data, dict):
            req_headers["Content-Type"] = "application/x-www-form-urlencoded"
            encoded_body = urllib.parse.urlencode(data).encode("utf-8")
        elif isinstance(data, str):
            encoded_body = data.encode("utf-8")
        elif isinstance(data, bytes):
            encoded_body = data

    req = urllib.request.Request(
        url=url,
        data=encoded_body,
        headers=req_headers,
        method=method.upper(),
    )

    ctx = _build_ssl_context(verify_ssl)

    try:
        with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
            resp_headers = {k.lower(): v for k, v in resp.headers.items()}
            content = resp.read()
            return SovereignResponse(
                status_code=resp.status,
                headers=resp_headers,
                content=content,
                url=resp.geturl(),
            )
    except urllib.error.HTTPError as e:
        content = e.read()
        resp_headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        return SovereignResponse(
            status_code=e.code,
            headers=resp_headers,
            content=content,
            url=e.geturl() if hasattr(e, "geturl") else url,
        )
    except urllib.error.URLError as e:
        raise ConnectionError(f"Sovereign connection failed to {url}: {e.reason}") from e


def get(url: str, **kwargs: Any) -> SovereignResponse:
    return request("GET", url, **kwargs)


def post(url: str, **kwargs: Any) -> SovereignResponse:
    return request("POST", url, **kwargs)


def put(url: str, **kwargs: Any) -> SovereignResponse:
    return request("PUT", url, **kwargs)


def delete(url: str, **kwargs: Any) -> SovereignResponse:
    return request("DELETE", url, **kwargs)


def stream_chunks(
    url: str,
    chunk_size: int = 65536,
    timeout: float = 30.0,
    verify_ssl: bool = False,
) -> Iterator[bytes]:
    """Streams data in chunks from a remote URL directly to caller (zero NVMe staging)."""
    req = urllib.request.Request(
        url=url,
        headers={"User-Agent": "SovereignStreamer/1.0 (+zero-bloat pipeline)"},
    )
    ctx = _build_ssl_context(verify_ssl)
    with urllib.request.urlopen(req, timeout=timeout, context=ctx) as resp:
        while True:
            chunk = resp.read(chunk_size)
            if not chunk:
                break
            yield chunk


def run_selftest() -> bool:
    print("=== SELFTEST: Sovereign HTTP Client & Kinematic Filter ===")

    # Test 1: Clean stream without leaks
    clean_sample = '{"status": "ok", "task_id": 101}'
    assert sanitize_model_stream(clean_sample) == {"status": "ok", "task_id": 101}
    print("[PASS] Clean JSON parsed correctly.")

    # Test 2: Contaminated stream with <think> tag bleed
    contaminated_think = (
        "<think>Let me evaluate the user's intent. User wants task status. Emitting JSON now.</think>"
        '{"status": "ok", "task_id": 102}'
    )
    assert is_reasoning_leaked(contaminated_think) is True
    assert sanitize_model_stream(contaminated_think) == {"status": "ok", "task_id": 102}
    print("[PASS] Contaminated <think> block stripped and JSON cleanly bounded.")

    # Test 3: Contaminated stream with Thinking Process header and conversational trail
    contaminated_monologue = (
        "Thinking Process:\n"
        "1. The operator requires a structured report.\n"
        "2. Checking constraints.\n\n"
        '```json\n{"report": "ready", "falsifiers": [1, 2, 3]}\n```\n'
        "I hope this helps! Let me know if you need changes."
    )
    assert is_reasoning_leaked(contaminated_monologue) is True
    res = sanitize_model_stream(contaminated_monologue)
    assert res["report"] == "ready"
    assert res["falsifiers"] == [1, 2, 3]
    print("[PASS] Monologue prefix and conversational suffix sheared off.")

    # Test 4: SovereignResponse integration
    mock_resp_bytes = json.dumps({
        "choices": [{
            "message": {
                "content": "<thought>Internal reasoning</thought>{\"action\": \"dispatch\"}"
            }
        }]
    }).encode("utf-8")
    resp = SovereignResponse(200, {}, mock_resp_bytes, "https://local.mock")
    assert resp.ok is True
    assert resp.has_thinking_bleed() is True
    content = resp.extract_content(sanitize_thinking=True)
    assert content == '{"action": "dispatch"}'
    print("[PASS] SovereignResponse.extract_content() mechanically bulletproofed.")

    print("\nSOVEREIGN HTTP CLIENT & KINEMATIC FILTER SELFTEST PASSED (100% GREEN).")
    return True


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--selftest":
        success = run_selftest()
        sys.exit(0 if success else 1)
    else:
        run_selftest()
        sys.exit(0)
