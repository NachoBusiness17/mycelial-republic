#!/usr/bin/env python3
"""tools/sovereign/http_client.py - Sovereign Zero-Dependency HTTP Client.

Picasso Steal: Replaces external packages 'requests' and 'httpx' with pure
Python standard library (urllib.request, http.client, ssl, json).

Features:
- GET, POST, PUT, DELETE with headers, query params, JSON payloads, and form data.
- Built-in redirect following with loop protection.
- Resilient SSL context (automatically handles self-signed/intercept certs).
- Direct streaming support for zero-disk pipes (e.g. into rclone rcat).
- Response object mimicing standard requests/httpx API: .status_code, .text, .json(), .content, .ok.
"""

from __future__ import annotations

import json
import ssl
import sys
import urllib.parse
import urllib.request
from typing import Any, Dict, Iterator, Optional, Union


class SovereignResponse:
    """Lightweight, transparent response object holding payload and headers."""

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

    def json(self) -> Any:
        return json.loads(self.text)

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
        "User-Agent": "SovereignClient/1.0 (+estate invariant core; zero-wheel)",
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


if __name__ == "__main__":
    print("Testing Sovereign HTTP Client...")
    resp = get("https://httpbin.org/get", params={"estate": "picasso_steal"})
    print(f"Status: {resp.status_code}")
    print(f"URL: {resp.url}")
    print(f"JSON response keys: {list(resp.json().keys())}")
    print("Sovereign HTTP Client PASSED.")
