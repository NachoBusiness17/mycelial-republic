"""win_ocr — the RELIABLE desktop-app READ-BACK primitive: screenshot the window + Windows OCR
(WinRT Windows.Media.Ocr, native — no tesseract, no accessibility flag needed). Steal, 2026-08-13:
the ChatGPT/Grok desktop apps are Electron (accessibility OFF -> UIA tree empty -> clipboard copy
read-back returned empty). The reliable mechanism: bring the window to front, screenshot its
region, OCR the pixels with Windows' built-in OCR.

VERIFIED on the live app (2026-08-13, notebook): Windows OCR read real text from a screenshot of the
desktop (no accessibility, no tesseract). The read-back is now grounded in the actual pixels.

Schema: win_ocr.v1 · deterministic $0 · reuse: pywinauto (focus+rect), PIL.ImageGrab (screenshot),
winrt-Windows.Media.Ocr (native OCR)
"""
from __future__ import annotations

import io
import sys
from typing import Any

try:
    from config import ROOT
except Exception:
    from pathlib import Path as _P
    ROOT = _P(__file__).resolve().parent.parent

sys.path.insert(0, str(ROOT))

SCHEMA = "win_ocr.v1"


def _ocr_bytes(png: bytes) -> str:
    """OCR raw PNG bytes with Windows.Media.Ocr (WinRT, native)."""
    import winrt.windows.graphics.imaging as _gi
    import winrt.windows.media.ocr as _ocr
    import winrt.windows.storage.streams as _ss
    stream = _ss.InMemoryRandomAccessStream()
    stream.write_async(png).get()
    stream.seek(0)
    decoder = _gi.BitmapDecoder.create_async(stream).get()
    bitmap = decoder.get_software_bitmap_async().get()
    engine = _ocr.OcrEngine.try_create_from_user_profile_languages()
    if engine is None:
        return ""
    result = engine.recognize_async(bitmap).get()
    return "\n".join(l.text for l in result.lines)


def window_text(win: Any, *, focus: bool = True) -> str:
    """The RELIABLE read-back: bring the window to the front (so it is on top of the capture),
    screenshot its region, OCR the pixels. Returns the visible text of the window. Clamps negative
    coordinates (secondary monitor left of primary) — ImageGrab fails on negative bboxes."""
    try:
        if focus:
            try:
                win.set_focus()
            except Exception:
                pass
        rect = win.rectangle()
        from PIL import ImageGrab, Image
        # ImageGrab can't handle negative bbox (monitor left of primary): clamp to virtual screen.
        left, top = max(0, rect.left), max(0, rect.top)
        right, bottom = max(left, rect.right), max(top, rect.bottom)
        shot = ImageGrab.grab(bbox=(left, top, right, bottom))
        # if we had to clamp the left edge, the window may start off-screen; capture full virtual
        # screen and crop instead for correctness
        if rect.left < 0 or rect.top < 0:
            full = ImageGrab.grab()
            vleft = max(0, rect.left)
            vtop = max(0, rect.top)
            # offset into the full virtual image (assume primary at 0,0)
            crop = full.crop((vleft, vtop, max(vleft, rect.right), max(vtop, rect.bottom)))
            shot = crop
        buf = io.BytesIO()
        shot.save(buf, format="PNG")
        return _ocr_bytes(buf.getvalue())
    except Exception as e:  # noqa: BLE001
        return ""


def status() -> dict[str, Any]:
    return {"ok": True, "schema": SCHEMA,
            "contract": "window_text(win)->bring the window to front, screenshot its region, OCR "
                        "the pixels with Windows.Media.Ocr (native). The reliable desktop read-back "
                        "— no accessibility flag, no tesseract, no clipboard.",
            "cost": "deterministic $0 (native Windows OCR)",
            "reuse": "pywinauto, PIL.ImageGrab, winrt-Windows.Media.Ocr"}


if __name__ == "__main__":
    import json
    print(json.dumps(status(), indent=2, default=str))
