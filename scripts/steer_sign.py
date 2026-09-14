#!/usr/bin/env python3
"""HMAC signing for watch/steers.jsonl (Chair 6: the steer file was an unsigned
injection channel on the driver's critical path).

Modes:
  sign    -- append a "sig" field (HMAC-SHA256 over the row's canonical content,
             sig excluded) to every row lacking one. Existing rows' fields and
             values are never altered; signing only ADDS the sig field.
  verify  -- recompute each row's signature. Prints PASS/FAIL/UNSIGNED per row,
             exits nonzero on any failure.
  test    -- self-test on TEMP COPIES (never touches the real steer file):
             (a) tampered text must verify FAIL; (b) unsigned row must flag
             UNSIGNED.

Key: state/.steer_key, created on first sign with secrets.token_hex(32).
The key is never printed or logged. Usage:
  python scripts/steer_sign.py sign
  python scripts/steer_sign.py verify
  python scripts/steer_sign.py test
Optional flags: --file PATH (default watch/steers.jsonl),
                --key PATH  (default state/.steer_key)
"""

import argparse
import copy
import hashlib
import hmac
import json
import os
import secrets
import sys
import tempfile

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_FILE = os.path.join(REPO_ROOT, "watch", "steers.jsonl")
DEFAULT_KEY = os.path.join(REPO_ROOT, "state", ".steer_key")
SIG_FIELD = "sig"


def canonical_content(row: dict) -> bytes:
    """Canonical bytes a row is signed over: the row minus its sig field,
    sorted keys, compact separators. Deterministic regardless of original
    key order or spacing."""
    content = {k: v for k, v in row.items() if k != SIG_FIELD}
    return json.dumps(content, sort_keys=True, separators=(",", ":"),
                      ensure_ascii=False).encode("utf-8")


def compute_sig(row: dict, key: bytes) -> str:
    return hmac.new(key, canonical_content(row), hashlib.sha256).hexdigest()


def load_key(key_path: str, create: bool) -> bytes:
    """Read the signing key; create it on first use. Never echo the value."""
    if os.path.exists(key_path):
        with open(key_path, "r", encoding="utf-8") as fh:
            raw = fh.read().strip()
        if not raw:
            sys.exit(f"ERROR: key file {key_path} is empty")
        try:
            return bytes.fromhex(raw)
        except ValueError:
            return raw.encode("utf-8")
    if not create:
        sys.exit(f"ERROR: key file {key_path} missing (run sign mode first)")
    os.makedirs(os.path.dirname(key_path), exist_ok=True)
    token = secrets.token_hex(32)
    fd = os.open(key_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        os.write(fd, token.encode("ascii"))
    finally:
        os.close(fd)
    print(f"key: created new key file {key_path} (value not shown)")
    return bytes.fromhex(token)


def read_rows(path: str):
    """Yield (line_number, raw_line, parsed_or_None). Blank lines pass through."""
    with open(path, "r", encoding="utf-8") as fh:
        for n, line in enumerate(fh, 1):
            stripped = line.strip()
            if not stripped:
                yield n, line, None
                continue
            try:
                yield n, line, json.loads(stripped)
            except json.JSONDecodeError as exc:
                yield n, line, exc


def write_rows(path: str, lines) -> None:
    """Atomic rewrite: temp file in same dir, then replace."""
    d = os.path.dirname(os.path.abspath(path))
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".steers_tmp_")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.writelines(lines)
        os.replace(tmp, path)
    except BaseException:
        if os.path.exists(tmp):
            os.remove(tmp)
        raise


def mode_sign(file_path: str, key_path: str) -> int:
    key = load_key(key_path, create=True)
    signed = already = 0
    out_lines = []
    for n, raw, parsed in read_rows(file_path):
        if parsed is None or isinstance(parsed, Exception):
            # blank line or malformed JSON: pass through untouched
            if isinstance(parsed, Exception):
                print(f"line {n}: MALFORMED JSON, left untouched ({parsed})")
            out_lines.append(raw)
            continue
        if SIG_FIELD in parsed:
            already += 1
            out_lines.append(json.dumps(parsed, ensure_ascii=False,
                                        separators=(",", ":")) + "\n")
            continue
        parsed[SIG_FIELD] = compute_sig(parsed, key)
        signed += 1
        out_lines.append(json.dumps(parsed, ensure_ascii=False,
                                    separators=(",", ":")) + "\n")
    write_rows(file_path, out_lines)
    print(f"SIGNED: {signed} row(s); already signed (untouched): {already}")
    return 0


def verify_file(file_path: str, key: bytes):
    """Verify every row. Returns list of (line_no, row_id, verdict, detail)."""
    results = []
    for n, _raw, parsed in read_rows(file_path):
        if parsed is None:
            results.append((n, "-", "SKIP", "blank line"))
            continue
        if isinstance(parsed, Exception):
            results.append((n, "-", "FAIL", f"malformed JSON: {parsed}"))
            continue
        row_id = parsed.get("id", "?")
        if SIG_FIELD not in parsed:
            results.append((n, row_id, "UNSIGNED", "no sig field"))
            continue
        expect = compute_sig(parsed, key)
        if hmac.compare_digest(parsed[SIG_FIELD], expect):
            results.append((n, row_id, "PASS", ""))
        else:
            results.append((n, row_id, "FAIL",
                            "signature mismatch (content altered or forged)"))
    return results


def mode_verify(file_path: str, key_path: str) -> int:
    key = load_key(key_path, create=False)
    results = verify_file(file_path, key)
    failures = 0
    for n, row_id, verdict, detail in results:
        line = f"line {n} id={row_id}: {verdict}"
        if detail:
            line += f" -- {detail}"
        print(line)
        if verdict in ("FAIL", "UNSIGNED"):
            failures += 1
    total = len(results)
    if failures:
        print(f"VERIFY: {total - failures}/{total} OK, {failures} FAILED/UNSIGNED -- exit 1")
        return 1
    print(f"VERIFY: {total}/{total} PASS")
    return 0


def mode_test(file_path: str, key_path: str) -> int:
    key = load_key(key_path, create=True)
    ok = True

    # --- TEST (a): tamper every row in a temp copy -> each previously-signed
    # row must verify FAIL. Foreign unsigned rows (concurrent appends, canaries)
    # flag UNSIGNED and are excluded from the tamper expectation.
    signed_rows = [(n, raw, parsed) for n, raw, parsed in read_rows(file_path)
                   if isinstance(parsed, dict) and SIG_FIELD in parsed]
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False,
                                     encoding="utf-8", newline="\n") as tam:
        tam_path = tam.name
        for _n, _raw, parsed in signed_rows:
            row = copy.deepcopy(parsed)  # never mutate rows shared with test (b)
            row["text"] = str(row.get("text", "")) + " TAMPERED-BY-LANE-B1"
            tam.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
    res_a = verify_file(tam_path, key)
    fails_a = [r for r in res_a if r[2] == "FAIL"]
    os.remove(tam_path)
    if signed_rows and len(fails_a) == len(signed_rows):
        print(f"TEST a (tamper detection): {len(fails_a)}/{len(signed_rows)} signed rows FAIL after tamper as expected -- OK")
        print(f"  e.g. line {fails_a[0][0]} id={fails_a[0][1]}: {fails_a[0][3]}")
    else:
        print(f"TEST a (tamper detection): UNEXPECTED -- {len(fails_a)}/{len(signed_rows)} failed; tamper NOT caught")
        ok = False

    # --- TEST (b): strip the sig from the first signed row in a temp copy ->
    # that row must flag UNSIGNED and all other signed rows must still PASS.
    with tempfile.NamedTemporaryFile("w", suffix=".jsonl", delete=False,
                                     encoding="utf-8", newline="\n") as uns:
        uns_path = uns.name
        stripped_id = signed_rows[0][2].get("id", "?") if signed_rows else "?"
        stripped_once = False
        for _n, _raw, parsed in signed_rows:
            if not stripped_once:
                parsed.pop(SIG_FIELD, None)
                stripped_once = True
            uns.write(json.dumps(parsed, ensure_ascii=False, separators=(",", ":")) + "\n")
    res_b = verify_file(uns_path, key)
    uns_b = {r[1] for r in res_b if r[2] == "UNSIGNED"}
    passes_b = [r for r in res_b if r[2] == "PASS"]
    expected_pass = len(signed_rows) - 1
    os.remove(uns_path)
    if stripped_id in uns_b and len(passes_b) == expected_pass:
        print(f"TEST b (unsigned detection): UNSIGNED flagged as expected -- OK")
        print(f"  id={stripped_id} flagged UNSIGNED ({len(passes_b)} other signed rows still PASS)")
    else:
        print(f"TEST b (unsigned detection): UNEXPECTED -- stripped row id={stripped_id} "
              f"{'flagged' if stripped_id in uns_b else 'NOT flagged'}; {len(passes_b)}/{expected_pass} others PASS")
        ok = False

    print("TEST: PASS" if ok else "TEST: FAIL")
    return 0 if ok else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="HMAC signer for watch/steers.jsonl")
    ap.add_argument("mode", choices=["sign", "verify", "test"])
    ap.add_argument("--file", default=DEFAULT_FILE)
    ap.add_argument("--key", default=DEFAULT_KEY)
    args = ap.parse_args()
    if args.mode == "sign":
        return mode_sign(args.file, args.key)
    if args.mode == "verify":
        return mode_verify(args.file, args.key)
    return mode_test(args.file, args.key)


if __name__ == "__main__":
    sys.exit(main())
