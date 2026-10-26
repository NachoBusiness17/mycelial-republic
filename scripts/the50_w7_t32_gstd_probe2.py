#!/usr/bin/env python3
"""THE 50, task 32 (W7): GSTD T0 probe v2.

v1 (watch/inbox/GSTD_T0_PROBE_20260918.json) probed app.gstdtoken.com only:
host resolved but every API path 404 -> verdict DARK-FRONT-DOOR.
v2 moves one layer down: probe the public TON explorer / API endpoints for the
GSTD jetton master with alternate endpoints, honest DEAD/ALIVE per endpoint.

T0 = tier 0, local: python stdlib HTTP only, no LLM, no API keys.

Verdicts (defined once, applied to every endpoint):
  ALIVE           HTTP 200 and the response carried the expected evidence
                  (documented JSON shape resolving the address, or HTML echo).
  DEAD            transport death (DNS, refused, reset, TLS, timeout) after one
                  retry, or HTTP 5xx after one retry, or HTTP 404 on the route.
  LIVE_UNVERIFIED the server answered but evidence could not be verified
                  (401/403/429 auth or rate limit, 400 query rejected, or 200
                  without the expected fields). Named gray state instead of
                  guessing a binary.
Nothing that did not actually answer is called ALIVE; nothing that answered is
called DEAD for auth reasons.

Usage: .venv/Scripts/python.exe scripts/the50_w7_t32_gstd_probe2.py
Writes: memory/runs/the50/w7_t32_gstd_probe2.json
"""

import json
import ssl
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone

REPO = r"C:\Users\foste\Documents\projects\local_sovereign_agent"
JETTON = "EQDv6cYW9nNiKjN3Nwl8D6ABjUiH1gYfWVGZhfP7-9tZskTO"
OUT = REPO + r"\memory\runs\the50\w7_t32_gstd_probe2.json"

HEADERS = {
    "User-Agent": "MagFleet-T0Probe/2.0 (THE50 T32; local_sovereign_agent)",
    "Accept": "application/json,text/html;q=0.8,*/*;q=0.5",
}
TIMEOUT_S = 15
RETRY_SLEEP_S = 2.0


def fetch(url, method="GET", body=None, extra_headers=None):
    """One HTTP attempt. Returns dict, never raises."""
    hdrs = dict(HEADERS)
    if extra_headers:
        hdrs.update(extra_headers)
    data = body.encode("utf-8") if isinstance(body, str) else body
    t0 = time.monotonic()
    try:
        req = urllib.request.Request(url, data=data, headers=hdrs, method=method)
        with urllib.request.urlopen(req, timeout=TIMEOUT_S) as resp:
            raw = resp.read(65536)
            return {
                "ok": True,
                "status": resp.status,
                "latency_ms": int((time.monotonic() - t0) * 1000),
                "body": raw.decode("utf-8", errors="replace"),
            }
    except urllib.error.HTTPError as e:
        try:
            raw = e.read(65536)
            body_text = raw.decode("utf-8", errors="replace")
        except Exception:
            body_text = ""
        return {
            "ok": False,
            "status": e.code,
            "latency_ms": int((time.monotonic() - t0) * 1000),
            "body": body_text,
            "err": "HTTPError %d" % e.code,
        }
    except Exception as e:
        return {
            "ok": False,
            "status": None,
            "latency_ms": int((time.monotonic() - t0) * 1000),
            "body": "",
            "err": "%s: %s" % (type(e).__name__, e),
        }


def probe(name, kind, url, method="GET", body=None, extra_headers=None, check=None):
    """Probe one endpoint with one retry on transport death / 5xx / 429."""
    attempts = []
    for i in range(2):
        r = fetch(url, method=method, body=body, extra_headers=extra_headers)
        attempts.append(r)
        transport_death = r["status"] is None
        server_unstable = (r["status"] or 0) >= 500 or r["status"] == 429
        if not (transport_death or server_unstable):
            break
        if i == 0:
            time.sleep(RETRY_SLEEP_S)
    last = attempts[-1]
    row = {
        "name": name,
        "kind": kind,
        "url": url,
        "http_method": method,
        "attempts": len(attempts),
        "http_status": last["status"],
        "latency_ms": last["latency_ms"],
        "checked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
    }
    # Classify
    if last["status"] is None:
        row["verdict"] = "DEAD"
        row["verdict_basis"] = "transport death after retry: %s" % last.get("err")
    elif last["status"] == 404:
        row["verdict"] = "DEAD"
        row["verdict_basis"] = "route not found (HTTP 404)"
    elif last["status"] is not None and last["status"] >= 500:
        row["verdict"] = "DEAD"
        row["verdict_basis"] = "HTTP 5xx after retry: %s" % last["status"]
    elif last["status"] == 200 and check is not None:
        ev = check(last["body"])
        row.update(ev)
        if ev.get("evidence_verified"):
            row["verdict"] = "ALIVE"
            row["verdict_basis"] = ev.get("verdict_basis", "HTTP 200 + expected evidence")
        else:
            row["verdict"] = "LIVE_UNVERIFIED"
            row["verdict_basis"] = ev.get("verdict_basis", "HTTP 200 but expected evidence absent")
    elif last["status"] == 200:
        row["verdict"] = "LIVE_UNVERIFIED"
        row["verdict_basis"] = "HTTP 200 but no evidence check defined"
    else:
        row["verdict"] = "LIVE_UNVERIFIED"
        row["verdict_basis"] = "server answered HTTP %s: %s" % (
            last["status"],
            (last.get("body") or "")[:120].replace("\n", " "),
        )
    # Bounded evidence quote, ASCII-safe
    quote = (last.get("body") or "")[:400]
    row["body_quote"] = quote.encode("ascii", errors="replace").decode("ascii")
    return row


def chk_jsonrpc_addrinfo(text):
    """toncenter v2 jsonRPC getAddressInformation."""
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if not (isinstance(j, dict) and j.get("ok") is True and isinstance(j.get("result"), dict)):
        return {"evidence_verified": False, "verdict_basis": "JSON without ok:true+result"}
    res = j["result"]
    code_len = len(res.get("code") or "")
    data_len = len(res.get("data") or "")
    return {
        "evidence_verified": True,
        "verdict_basis": "jsonRPC ok:true, address resolved",
        "balance_nano": res.get("balance"),
        "code_len": code_len,
        "data_len": data_len,
        "onchain_deployed": code_len > 0 and data_len > 0,
        "last_tx_lt": res.get("last_transaction_lt"),
    }


def chk_v3_addrinfo(text):
    """toncenter v3 returns flat fields (balance/code/data), address may be absent."""
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if not isinstance(j, dict):
        return {"evidence_verified": False, "verdict_basis": "JSON not an object"}
    if "balance" not in j and "code" not in j:
        return {"evidence_verified": False,
                "verdict_basis": "JSON without balance/code fields: %s" % list(j)[:6]}
    code_len = len(j.get("code") or "")
    data_len = len(j.get("data") or "")
    row = {
        "evidence_verified": True,
        "verdict_basis": "v3 answered with account fields",
        "resolved_address": j.get("address"),
        "balance_nano": j.get("balance"),
        "code_len": code_len,
        "data_len": data_len,
        "onchain_deployed": code_len > 0 and data_len > 0,
    }
    return row


def chk_masterchain(text):
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    seqno = None
    if isinstance(j, dict):
        res = j.get("result", j)
        if isinstance(res, dict):
            seqno = res.get("seqno") or res.get("last", {}).get("seqno") if isinstance(res.get("last"), dict) else res.get("seqno")
    if isinstance(seqno, int) and seqno > 0:
        return {"evidence_verified": True, "verdict_basis": "masterchain seqno %d" % seqno, "seqno": seqno}
    return {"evidence_verified": False, "verdict_basis": "no positive seqno in body"}


def chk_v3_jetton_wallets(text):
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if not isinstance(j, dict):
        return {"evidence_verified": False, "verdict_basis": "JSON not an object"}
    wallets = j.get("jetton_wallets") or j.get("wallets")
    if isinstance(wallets, list):
        first = wallets[0] if wallets else {}
        return {
            "evidence_verified": True,
            "verdict_basis": "v3 jetton wallets endpoint answered, %d rows (limit 1)" % len(wallets),
            "rows_returned": len(wallets),
            "sample_jetton": first.get("jetton"),
            "sample_balance": first.get("balance"),
            "address_book_present": "address_book" in j,
        }
    return {"evidence_verified": False, "verdict_basis": "no jetton_wallets list in body"}


def chk_tonapi_jetton(text):
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if not isinstance(j, dict):
        return {"evidence_verified": False, "verdict_basis": "JSON not an object"}
    meta = j.get("metadata") or {}
    sym = meta.get("symbol")
    if sym:
        return {
            "evidence_verified": True,
            "verdict_basis": "tonapi jetton metadata resolved",
            "symbol": sym,
            "jetton_name": meta.get("name"),
            "decimals": meta.get("decimals"),
            "resolved_address": j.get("address") or meta.get("address"),
            "total_supply": j.get("total_supply"),
            "mintable": j.get("mintable"),
            "verification": j.get("verification"),
            "jetton_indexed": True,
        }
    return {"evidence_verified": False, "verdict_basis": "JSON without jetton metadata"}


def chk_tonapi_account(text):
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if not isinstance(j, dict):
        return {"evidence_verified": False, "verdict_basis": "JSON not an object"}
    if j.get("address"):
        status = j.get("status")
        code = j.get("code")
        code_len = len(code) if code else 0
        return {
            "evidence_verified": True,
            "verdict_basis": "tonapi resolved account, status %s" % status,
            "resolved_address": j.get("address"),
            "balance_nano": j.get("balance"),
            "status": status,
            "interfaces": j.get("interfaces"),
            "code_field_present": code is not None,
            "code_len": code_len,
            # tonapi does not echo contract code here; deployment signal is status+interfaces
            "onchain_deployed": (status == "active") if status else code_len > 0,
        }
    return {"evidence_verified": False, "verdict_basis": "JSON without address field"}


def chk_tonapi_status(text):
    """tonapi service status control."""
    try:
        j = json.loads(text)
    except Exception:
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 body is not JSON"}
    if isinstance(j, dict) and ("rest_online" in j or "status" in j):
        return {
            "evidence_verified": True,
            "verdict_basis": "tonapi status answered: rest_online=%s" % j.get("rest_online"),
            "rest_online": j.get("rest_online"),
        }
    return {"evidence_verified": False, "verdict_basis": "no status fields in body"}


def chk_html_echo(addr):
    def f(text):
        if addr in text:
            return {"evidence_verified": True, "verdict_basis": "HTTP 200, address echoed in page HTML"}
        return {"evidence_verified": False, "verdict_basis": "HTTP 200 but address not echoed (SPA shell?)"}
    return f


def main():
    stamp = datetime.now(timezone.utc).isoformat(timespec="seconds")
    endpoints = []

    J = JETTON
    rpc_body = json.dumps({
        "id": 1,
        "jsonrpc": "2.0",
        "method": "getAddressInformation",
        "params": {"address": J},
    })

    # 1. toncenter v2 jsonRPC (the repos' own endpoint, deploy-mainnet.ts:41)
    endpoints.append(probe(
        "toncenter_v2_jsonrpc_getAddressInformation", "api",
        "https://toncenter.com/api/v2/jsonRPC", method="POST",
        body=rpc_body, extra_headers={"Content-Type": "application/json"},
        check=chk_jsonrpc_addrinfo))

    # 2. toncenter v2 GET masterchain info (network liveness control)
    endpoints.append(probe(
        "toncenter_v2_getMasterchainInfo", "api_control",
        "https://toncenter.com/api/v2/getMasterchainInfo",
        check=chk_masterchain))

    # 3. toncenter v2 plain GET route (alternate route on same service)
    endpoints.append(probe(
        "toncenter_v2_getAddressInformation_GET", "api",
        "https://toncenter.com/api/v2/getAddressInformation?address=" + J,
        check=chk_jsonrpc_addrinfo))

    # 4. toncenter v3 addressInformation (alternate API version)
    endpoints.append(probe(
        "toncenter_v3_addressInformation", "api",
        "https://toncenter.com/api/v3/addressInformation?address=" + J,
        check=chk_v3_addrinfo))

    # 5. toncenter v3 jetton wallets (jetton population evidence)
    endpoints.append(probe(
        "toncenter_v3_jetton_wallets", "api",
        "https://toncenter.com/api/v3/jetton/wallets?jetton_address=" + J + "&limit=1",
        check=chk_v3_jetton_wallets))

    # 6. tonapi v2 jetton metadata (the web app's own API, ai/.env.example)
    endpoints.append(probe(
        "tonapi_v2_jetton_metadata", "api",
        "https://tonapi.io/v2/jettons/" + J,
        check=chk_tonapi_jetton))

    # 7. tonapi v2 account state
    endpoints.append(probe(
        "tonapi_v2_account", "api",
        "https://tonapi.io/v2/accounts/" + J,
        check=chk_tonapi_account))

    # 8. tonapi v2 service status (network liveness control)
    endpoints.append(probe(
        "tonapi_v2_status", "api_control",
        "https://tonapi.io/v2/status",
        check=chk_tonapi_status))

    # 9. tonviewer HTML explorer
    endpoints.append(probe(
        "tonviewer_html", "explorer_html",
        "https://tonviewer.com/" + J,
        check=chk_html_echo(J)))

    # 10. tonscan HTML explorer
    endpoints.append(probe(
        "tonscan_html", "explorer_html",
        "https://tonscan.org/address/" + J,
        check=chk_html_echo(J)))

    # 11. v1 continuity: the dark front door, one route, is it still dark
    endpoints.append(probe(
        "app_gstdtoken_front_door_continuity", "continuity_v1",
        "https://app.gstdtoken.com/"))

    counts = {"ALIVE": 0, "DEAD": 0, "LIVE_UNVERIFIED": 0}
    for e in endpoints:
        counts[e["verdict"]] += 1

    # Jetton-level findings pulled out of the endpoint rows
    jetton = {"address": J, "sources": [
        "reference/gstdcoin/contracts/deployment-mainnet.json (contracts.GSTDJetton, deployedAt 2026-07-08)",
        "reference/gstdcoin/contracts/README.md:155",
        "reference/gstdcoin/gstd-bridge/bridge.toml:17",
        "reference/gstdcoin/web/src/content/config.ts:2",
    ]}
    for e in endpoints:
        if e["name"] == "toncenter_v2_jsonrpc_getAddressInformation":
            jetton["toncenter_v2_onchain"] = {
                k: e[k] for k in ("code_len", "data_len", "onchain_deployed", "balance_nano")
                if k in e}
        if e["name"] == "tonapi_v2_jetton_metadata" and e.get("evidence_verified"):
            jetton["tonapi_metadata"] = {
                k: e[k] for k in ("symbol", "jetton_name", "decimals", "total_supply",
                                  "mintable", "verification", "resolved_address")
                if k in e}
        if e["name"] == "tonapi_v2_account" and e.get("evidence_verified"):
            jetton["tonapi_account"] = {
                k: e[k] for k in ("status", "interfaces", "balance_nano", "onchain_deployed")
                if k in e}

    # Honest overall verdict
    alive = counts["ALIVE"]
    if alive >= 2:
        overall = ("EXPLORER-LAYER-ALIVE: %d of %d endpoints verified alive for the jetton; "
                   "jetton findings below carry the real on-chain truth." % (alive, len(endpoints)))
    elif counts["LIVE_UNVERIFIED"] > 0:
        overall = "PARTIAL: services answered but no endpoint verified the jetton (see LIVE_UNVERIFIED rows)."
    else:
        overall = "EXPLORER-LAYER-DEAD: no endpoint answered with evidence."

    artifact = {
        "task": "THE50 T32 W7 GSTD T0 probe v2",
        "when_utc": stamp,
        "probe_script": "scripts/the50_w7_t32_gstd_probe2.py",
        "method": "python stdlib urllib, 15s timeout, one retry on transport death / 5xx / 429, no API keys (T0)",
        "target": jetton,
        "v1": {
            "artifact": "watch/inbox/GSTD_T0_PROBE_20260918.json",
            "context": "watch/inbox/ORPHAN_RACTOR_PANEL_20260918.md",
            "finding": "app.gstdtoken.com resolved but all 6 probed API paths 404; verdict DARK-FRONT-DOOR",
        },
        "verdict_defs": {
            "ALIVE": "HTTP 200 + expected evidence verified (documented JSON shape or HTML echo)",
            "DEAD": "transport death or 5xx after one retry, or route 404",
            "LIVE_UNVERIFIED": "server answered but evidence unverifiable (auth/rate limit/shape mismatch)",
        },
        "endpoints": endpoints,
        "counts": counts,
        "overall": overall,
        "limits": [
            "No API keys used: toncenter without a key is rate limited; a LIVE_UNVERIFIED 429 does not mean the service is dead.",
            "HTML explorer check is echo-of-address in first 64KB; a JS-only shell would look unverified even if the coin renders in a browser.",
            "T0 probe observes public HTTP only; it cannot verify the repos' contract claims beyond what explorers index.",
        ],
    }

    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(artifact, f, indent=1, ensure_ascii=True)
    print("WROTE", OUT)
    print("counts:", counts)
    for e in endpoints:
        print("%-42s %s %s %sms" % (e["name"], e["verdict"], e["http_status"], e["latency_ms"]))
    return 0


if __name__ == "__main__":
    sys.exit(main())
