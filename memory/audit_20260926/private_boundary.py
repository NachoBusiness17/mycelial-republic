"""CORRECTED private-surface inventory for the 2026-09-26 network audit.

The parent seat's first recon pass used a name-substring filter and reported
"18,733 private files skipped". That number was WRONG — it conflated real
secrets with the English word "private" appearing in C/C++ headers, pytest temp
artifacts, and DFHack source. This script produces the honest number.

Run: python memory/audit_20260926/private_boundary.py
"""
import os, json
from pathlib import Path

ROOT = Path(r"C:\Users\foste\Documents\projects")
SKIP_DIRS = {".git", "node_modules", ".venv", "venv", "__pycache__", "site-packages",
             ".mypy_cache", ".pytest_cache", ".ruff_cache"}

# Tier 1: filenames that are unambiguously secret-bearing, not English words.
HARD = {".env", ".env.local", ".env.production", ".env.development",
        "id_rsa", "id_dsa", "id_ecdsa", "id_ed25519", "credentials",
        "credentials.json", "secrets.json", "service-account.json"}
HARD_EXT = {".pem", ".pfx", ".p12", ".key", ".keystore", ".jks", ".ppk",
            ".asc", ".gpg", ".kdbx", ".netrc", ".htpasswd"}

# Tier 2: name contains these AND looks like a config/credential artifact.
# The word "private" alone is NOT a signal — it matched 17,933 C/C++ headers.
SIGNALS = ("secret", "credential", "password", "passwd", "apikey", "api_key",
           "api-key", "token", "auth", "oauth", "session_key", "private_key",
           "privkey", "id_rsa", "wallet", "keystore", "bip39", "mnemonic",
           "seed_phrase", "cookies")

rows = {"hard": [], "hard_ext": [], "signal": [], "dotenv_any": []}

for dp, dn, fn in os.walk(ROOT, topdown=True):
    dn[:] = [d for d in dn if d not in SKIP_DIRS and not d.startswith(".pytest_cache")]
    for f in fn:
        lf = f.lower()
        ext = Path(f).suffix.lower()
        p = str(Path(dp) / f).replace("\\", "/")
        if lf in HARD:
            rows["hard"].append(p)
        if ext in HARD_EXT:
            rows["hard_ext"].append(p)
        if lf.startswith(".env"):
            rows["dotenv_any"].append(p)
        if any(s in lf for s in SIGNALS) and lf not in HARD and ext not in HARD_EXT:
            rows["signal"].append(p)

total_hard = len(rows["hard"]) + len(rows["hard_ext"]) + len(rows["dotenv_any"])
print(f"{'tier':22} {'count':>7}")
print(f"{'HARD (exact name)':22} {len(rows['hard']):7d}")
print(f"{'HARD (secret ext)':22} {len(rows['hard_ext']):7d}")
print(f"{'dotenv (.env*)':22} {len(rows['dotenv_any']):7d}")
print(f"{'SIGNAL (name match)':22} {len(rows['signal']):7d}")
print(f"{'REAL secret surface':22} {total_hard:7d}")
print(f"\n(compare: the flawed first pass claimed 18,733 'private' files —")
print(f" that number included 17,933 C/C++ headers matching the word 'private')")

print("\n--- HARD: exact secret filenames (paths only, no contents) ---")
for p in rows["hard"][:40]:
    print("  ", p)
print("\n--- dotenv files ---")
for p in rows["dotenv_any"][:30]:
    print("  ", p)
print("\n--- SIGNAL: top 40 (name-matched) ---")
for p in rows["signal"][:40]:
    print("  ", p)

out = Path(__file__).resolve().parent / "private_boundary.json"
out.write_text(json.dumps({"counts": {k: len(v) for k, v in rows.items()},
                           "real_secret_surface": total_hard,
                           "flawed_first_pass_claim": 18733,
                           "false_positive_word_private": 17933,
                           "paths": rows}, indent=1), encoding="utf-8")
print(f"\nwrote {out}")
