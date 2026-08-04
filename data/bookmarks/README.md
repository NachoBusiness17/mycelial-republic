# X Bookmarks → training data

**X Bookmarks** (the bookmark icon on posts) are **private account data**.  
They are **not** on this PC as a folder, and this environment **cannot read them** without your login.

## What we cannot do from here

- Open `x.com/i/bookmarks` as you  
- Scrape your Bookmarks tab without your session  
- Read Bookmarks from the free public X search API  

## Ways to get them into the pipeline

### 1) Fast path — paste URLs (no API)

1. Open https://x.com/i/bookmarks  
2. Open each high-signal post → Share → **Copy link**  
3. Paste into:

```
data/bookmarks/urls.txt
```

One URL per line, e.g.:

```
https://x.com/NachoQuixotic/status/2076681679515598986
https://x.com/someone/status/1234567890
https://threadreaderapp.com/thread/1875223859315552564
```

4. Run:

```powershell
cd Documents\projects\mycelial-republic
.\.venv\Scripts\Activate.ps1

python -m mycelial_republic.cli bookmarks `
  --path data/bookmarks/urls.txt `
  --seed data/exports/nacho_merged_signal.jsonl `
  --out data/exports/from_x_bookmarks.jsonl

python -m mycelial_republic.data.annotate `
  --in data/exports/from_x_bookmarks.jsonl `
  --out data/annotated/mirror_train.jsonl --auto-heuristics

python -m mycelial_republic.data.validate `
  --in data/annotated/mirror_train.jsonl --min 50
```

### 2) X API (official, needs your keys)

Endpoint: `GET /2/users/:id/bookmarks`  
Requires **OAuth 2.0 user context** (you authorize the app once).

Env (example):

```
X_BEARER_TOKEN=...          # or user access token with bookmark.read
X_USER_ID=...               # your numeric user id
```

Then (when script is configured):

```powershell
python -m mycelial_republic.data.x_bookmarks_api --out data/exports/from_x_bookmarks.jsonl
```

See `src/mycelial_republic/data/x_bookmarks_api.py` — only runs if tokens are set.

### 3) Full account archive

X → Settings → Your account → **Download an archive**  
Includes far more than bookmarks (posts, likes, etc.). Still the volume path for 800+.

## After ingest

Tell the agent: **“bookmarks ready in urls.txt”** or drop the file and say **“run bookmarks ingest”**.
