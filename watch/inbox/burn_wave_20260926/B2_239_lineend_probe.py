"""B2-239 red/green probe for the verifier's new check8 (LF-only assertion).

Red leg: run the verifier against a byte copy of the historic CRLF disease
state (B2_220_ledger_before.jsonl, 291 CRLF lines, sha 2f3afda8976fe2...)
and require the check8 FAIL line naming the CR count.
Control leg: the same content LF-normalized must PASS check8, proving the
check is endings-sensitive, not content-sensitive.
Both legs operate on temp copies; the repo ledger is never written.

Run: .venv/Scripts/python.exe watch/inbox/burn_wave_20260926/B2_239_lineend_probe.py
"""
import hashlib
import importlib.util
import io
import shutil
import sys
import tempfile
from contextlib import redirect_stdout
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
VERIFY = ROOT / "scripts" / "the50_t21_q_caption_ledger_verify.py"
CRLF_SNAPSHOT = ROOT / "watch" / "inbox" / "burn_wave_20260926" / "B2_220_ledger_before.jsonl"


def load():
    spec = importlib.util.spec_from_file_location("t21_verify_b239", VERIFY)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["t21_verify_b239"] = mod
    spec.loader.exec_module(mod)
    return mod


def run_against(path: Path) -> tuple[int, list[str]]:
    mod = load()
    mod.OUT = path
    buf = io.StringIO()
    with redirect_stdout(buf):
        rc = mod.main()
    return rc, buf.getvalue().splitlines()


def main() -> int:
    raw = CRLF_SNAPSHOT.read_bytes()
    crlf = raw.count(b"\r\n")
    sha = hashlib.sha256(raw).hexdigest()
    print(f"snapshot: {CRLF_SNAPSHOT.name} sha256 {sha[:16]}... CRLF lines {crlf}")
    assert crlf == 291 and sha.startswith("2f3afda8976fe2"), "historic disease bytes moved"

    with tempfile.TemporaryDirectory() as td:
        red = Path(td) / "crlf_copy.jsonl"
        shutil.copyfile(CRLF_SNAPSHOT, red)
        rc, lines = run_against(red)
        chk8 = [ln for ln in lines if ln.startswith("check8")]
        print("RED  leg (CRLF copy): rc", rc, "|", chk8[0] if chk8 else "NO check8 line")
        assert rc == 1, "verifier must fail on the CRLF disease bytes"
        assert chk8 and "FAIL 291 CR bytes" in chk8[0], chk8
        assert any(ln.startswith("RESULT: FAIL") for ln in lines)

        green = Path(td) / "lf_copy.jsonl"
        green.write_bytes(raw.replace(b"\r\n", b"\n"))
        rc2, lines2 = run_against(green)
        chk8b = [ln for ln in lines2 if ln.startswith("check8")]
        print("CTRL leg (same content, LF): rc", rc2, "|", chk8b[0] if chk8b else "NO check8 line")
        assert chk8b and "PASS" in chk8b[0], chk8b

    print("probe: check8 red on CRLF disease bytes, PASS on the LF-normalized same content")
    return 0


if __name__ == "__main__":
    sys.exit(main())
