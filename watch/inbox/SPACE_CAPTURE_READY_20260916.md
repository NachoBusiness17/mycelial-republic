# SPACE CAPTURE — ready to run (2026-09-16)

Recorder: .venv/Scripts/twspace_dl.exe (installed, verified — module: python -m twspace_dl)
Target: https://x.com/i/spaces/1oJMvNqLZDlxQ
Transcriber: faster-whisper 1.2.1 (local, verified) — runs after capture.

## The one missing piece: cookies

Twitter killed guest access to Spaces metadata (2023-07 API change). twspace-dl now
REQUIRES a cookie file in Netscape format from a logged-in x.com session.

### Operator step (2 minutes, stays on this box):
1. In your logged-in Chrome/Edge on x.com: install/use a "Get cookies.txt LOCALLY" style
   extension (or dev tools > Application > Cookies), export cookies for x.com in
   Netscape format.
2. Save to: C:\Users\foste\Downloads\x_cookies.txt
3. Tell the fleet. Done.

HOUSE LAW: the cookie file contains your auth_token — it stays on this box, is never
committed, never leaves the machine, and is deleted after capture. Keys stay local.

## Capture command (fleet runs on your word)

.venv/Scripts/python.exe -m twspace_dl -i "https://x.com/i/spaces/1oJMvNqLZDlxQ" -c C:\Users\foste\Downloads\x_cookies.txt --write-url C:\Users\foste\Downloads\space_url.txt -m -l

(mixed capture: records the live stream as it runs, m4a output, logfile on)

## After capture

faster-whisper 1.2.1 transcribes the m4a locally (free) into the corpus:
memory/corpus/podcast_transcripts/<date>/ — then the fold reads it like every receipt.
