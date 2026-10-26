#!/usr/bin/env python3
"""chrome_cookie_pull.py - pull x.com session cookies from the operator's
Chrome profile into a local injector file (values never printed).

Operator order 2026-10-18: post the campaign yourself via headless browsers,
the API is credits-depleted. Runs as the operator's user; DPAPI decrypts
Chrome's v10/v11 cookie rows. v20 app-bound rows are reported, not
decryptable from user context. Superseded draft: chrome_cookie_pull.ps1.
Receipt: watch/inbox/CHURCH_CAMPAIGN_POSTED_20261018.md
"""
import base64
import ctypes
import ctypes.wintypes as wt
import json
import shutil
import sqlite3
import sys
from pathlib import Path

UD = Path(r"C:\Users\foste\AppData\Local\Google\Chrome\User Data")
OUT = Path(r"C:\Users\foste\Documents\projects\local_sovereign_agent"
           r"\memory\runs\x_church_campaign\x_cookies.json")


class DATA_BLOB(ctypes.Structure):
    _fields_ = [("cbData", wt.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]


def dpapi(data: bytes) -> bytes:
    pin = DATA_BLOB(len(data), ctypes.cast(ctypes.create_string_buffer(data),
                                           ctypes.POINTER(ctypes.c_char)))
    pout = DATA_BLOB()
    if not ctypes.windll.crypt32.CryptUnprotectData(
            ctypes.byref(pin), None, None, None, None, 0, ctypes.byref(pout)):
        raise OSError("DPAPI decrypt failed")
    return ctypes.string_at(pout.pbData, pout.cbData)


def aes_gcm(key: bytes, nonce: bytes, data: bytes) -> bytes:
    import ctypes.wintypes  # noqa: F401
    class BCRYPT (ctypes.Structure):
        _fields_ = []
    bcrypt = ctypes.windll.bcrypt
    halg = ctypes.c_void_p()
    if bcrypt.BCryptOpenAlgorithmProvider(ctypes.byref(halg), "AES", None, 0):
        raise OSError("open alg")
    if bcrypt.BCryptSetProperty(halg, "ChainingMode",
                                ctypes.create_unicode_buffer("ChainingModeGCM"),
                                len("ChainingModeGCM") * 2 + 2, 0):
        raise OSError("gcm property")
    hkey = ctypes.c_void_p()
    if bcrypt.BCryptGenerateSymmetricKey(halg, ctypes.byref(hkey), None, 0,
                                         key, len(key), 0):
        raise OSError("gen key")
    out = ctypes.create_string_buffer(len(data))
    done = ctypes.c_int(0)
    st = bcrypt.BCryptDecrypt(hkey, data, len(data), None, nonce, len(nonce),
                              out, len(data), ctypes.byref(done), 0)
    bcrypt.BCryptDestroyKey(hkey)
    bcrypt.BCryptCloseAlgorithmProvider(halg, 0)
    if st:
        raise OSError("gcm auth tag failed")
    return out.raw[:done.value]


def main() -> int:
    prof = sys.argv[1] if len(sys.argv) > 1 else "Default"
    pdir = UD / prof
    src = pdir / "Network" / "Cookies"
    tmp = OUT.parent / "cookies_copy.db"
    shutil.copyfile(src, tmp)
    ls = json.loads((UD / "Local State").read_text(encoding="utf-8"))
    key = dpapi(base64.b64decode(ls["os_crypt"]["encrypted_key"])[5:])
    con = sqlite3.connect(str(tmp))
    rows = con.execute(
        "SELECT host_key, name, encrypted_value FROM cookies "
        "WHERE host_key LIKE '%x.com%'").fetchall()
    con.close()
    tmp.unlink(missing_ok=True)
    pulled, ok = [], []
    for host, name, enc in rows:
        if not enc or len(enc) < 6:
            continue
        ver = enc[:3].decode("ascii", "replace")
        if ver in ("v10", "v11"):
            try:
                plain = aes_gcm(key, enc[3:15], enc[15:])
                val = plain.decode("utf-8", "replace")
                pulled.append({"host": host, "name": name, "value": val})
                if name in ("auth_token", "ct0"):
                    ok.append(name)
            except OSError as e:
                pulled.append({"host": host, "name": name, "error": str(e)})
        elif ver == "v20":
            pulled.append({"host": host, "name": name, "error": "app-bound-v20"})
    OUT.write_text(json.dumps({"pulled": pulled}, ensure_ascii=False),
                   encoding="utf-8")
    names = [p.get("name") for p in pulled]
    print("x.com cookies:", len(pulled), "| names:", names,
          "| decryptable auth rows:", sorted(set(ok)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
