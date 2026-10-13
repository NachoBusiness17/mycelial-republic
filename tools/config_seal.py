#!/usr/bin/env python3
"""config_seal.py — checksum-sealed integrity register over configs/.

The migration-ledger steal (zai-org/ZCode's checksum-sealed migration registry),
recreated for the estate's machine config directory. Every file under configs/
(json/yaml/yml) is hashed; the seal file configs/.config_seal.json holds the
register. verify fails on ANY drift: modified, missing, or new unsealed file.
update is a NAMED ACT (--by + --note) — key rotations and deliberate config
changes re-seal by hand, never silently.

LAW CHANGE 2026-09-29 (W3C, receipt watch/inbox/mates_leave_protocol/
W3C_SEAL_CRLF.md): the hash is taken over a LINE-ENDING-NORMALIZED form
(CRLF -> LF) in BOTH update and verify (they share _sha256). The v1 seal
hashed raw working-tree bytes, so a seal made on a CRLF Windows checkout
mismatched 41/56 files on any LF checkout (Linux clones, gate-canary
worktrees with byte-faithful blob checkout). The register seals CONTENT,
not one machine's EOL policy.

Usage:
  python tools/config_seal.py verify
  python tools/config_seal.py update --by WHO --note WHY

Exit codes: 0 = seal matches, 1 = drift (or first run with no seal — run update), 2 = broken.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

ESTATE_ROOT = Path(__file__).resolve().parent.parent
CONFIG_DIR = ESTATE_ROOT / "configs"
SEAL_PATH = CONFIG_DIR / ".config_seal.json"
PATTERNS = ("*.json", "*.yaml", "*.yml")


def _sha256(path: Path) -> str:
    # LAW 2026-09-29 (W3C seal CRLF fix): hash the CRLF->LF normalized bytes so
    # a seal made on a CRLF checkout verifies on an LF checkout and vice versa.
    # Cause: v1 sealed raw bytes; 41/56 sealed hashes mismatched the LF git
    # blobs, so every Linux clone and every gate-canary worktree verify failed
    # with no config content changed. Evidence: re-seal + tests
    # test_config_seal_verifies_lf_flip_of_crlf_seal / _crlf_flip_of_lf_seal
    # (tests/test_gate_blocking_paths.py), receipt
    # watch/inbox/mates_leave_protocol/W3C_SEAL_CRLF.md. Lone \r is left
    # untouched: git text conversion only maps CRLF<->LF.
    data = path.read_bytes().replace(b"\r\n", b"\n")
    return hashlib.sha256(data).hexdigest()


def _config_files() -> list[Path]:
    files: list[Path] = []
    for pat in PATTERNS:
        files.extend(
            p for p in sorted(CONFIG_DIR.glob(pat))
            if p.is_file() and p != SEAL_PATH  # the seal must not seal itself
        )
    return files


def build_register() -> dict[str, str]:
    return {p.relative_to(CONFIG_DIR).as_posix(): _sha256(p) for p in _config_files()}


def cmd_verify() -> int:
    if not SEAL_PATH.exists():
        print("CONFIG-SEAL verify: no seal exists yet — run 'update' once to create it (exit 2)")
        return 2
    sealed = json.loads(SEAL_PATH.read_text(encoding="utf-8")).get("files", {})
    live = build_register()
    modified = sorted(k for k, h in live.items() if k in sealed and sealed[k] != h)
    missing = sorted(k for k in sealed if k not in live)
    unsealed = sorted(k for k in live if k not in sealed)
    print(
        f"CONFIG-SEAL verify: sealed={len(sealed)} live={len(live)} "
        f"modified={len(modified)} missing={len(missing)} unsealed={len(unsealed)}"
    )
    for k in modified:
        print(f"  MODIFIED  {k}")
    for k in missing:
        print(f"  MISSING   {k}")
    for k in unsealed:
        print(f"  UNSEALED  {k}")
    if modified or missing or unsealed:
        print("CONFIG-SEAL: FAIL — re-seal by NAME: python tools/config_seal.py update --by WHO --note WHY")
        return 1
    print("CONFIG-SEAL: PASS — every config byte matches the register.")
    return 0


def cmd_update(by: str, note: str) -> int:
    if not CONFIG_DIR.is_dir():
        print("CONFIG-SEAL update: configs/ does not exist (exit 2)")
        return 2
    files = build_register()
    seal = {
        # v2 2026-09-29: hashes are over CRLF->LF normalized bytes (W3C law
        # change above). A v1 seal is NOT comparable to a v2 register — verify
        # against a v1 seal fails until `update` re-seals, which is the
        # intended one-time migration act.
        "schema": "config_seal.v2",
        "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "by": by,
        "note": note,
        "files": files,
    }
    SEAL_PATH.write_text(json.dumps(seal, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    # Fix 2026-09-29 (gala ball3 live-state): the display path raised ValueError
    # whenever SEAL_PATH sat outside ESTATE_ROOT, which the gate tests do by
    # design (tmp_path seals; monkeypatched SEAL_PATH). The wave5 full-suite
    # run passed an external --basetemp
    # (watch/inbox/gala_20260925/wave5-repair/lanes/suite-burn.check.txt, 5
    # gate/dead-hand failures, all "not in the subpath of"), while the default
    # basetemp inside the repo (conftest.py:14) masked it. Display only: the
    # seal bytes and exit codes are unchanged.
    try:
        shown = SEAL_PATH.relative_to(ESTATE_ROOT).as_posix()
    except ValueError:  # sandbox/external-basetemp seal outside the estate
        shown = str(SEAL_PATH)
    print(f"CONFIG-SEAL update: {len(files)} files sealed → {shown}")
    print(f"  by={by} note={note}")
    return 0


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(prog="config-seal", description="Checksum-sealed integrity register over configs/")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("verify")
    up = sub.add_parser("update")
    up.add_argument("--by", required=True)
    up.add_argument("--note", required=True)
    args = ap.parse_args(argv)
    if args.cmd == "verify":
        return cmd_verify()
    return cmd_update(args.by, args.note)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
