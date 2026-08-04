# Full threads + media (high-fidelity)

You were right: **roots alone are not the corpus**. Signal lives in:

1. **Subposts** (self-replies that make the thread)  
2. **Images** (screenshots, docs, photos)  
3. **Video** (long cuts, primary source, voice)

## What we do now

```powershell
python -m mycelial_republic.cli thread-pull `
  --ids-file data/bookmarks/ids.txt `
  --out data/exports/threads_full.jsonl
```

For each root ID:

| Layer | Source | In training text |
|-------|--------|------------------|
| Root body | fxtwitter | Full note/post text |
| Subposts | Threadreader unroll (when not noise) | Stitched under `## Full thread unroll` |
| Media | fxtwitter media catalog | `[IMAGE n] url` / `[VIDEO n duration=…] url` + alt if any |

## Limits (honest)

| Gap | Workaround |
|-----|------------|
| Unroll fails ~half the time (wrong page noise) | Save Threadreader **PDF** or “unroll” links that work; re-pull |
| Video audio not transcribed | Later: Whisper on `meta.media[].url` |
| Image text not OCR’d | Later: download + OCR / multimodal caption |
| Nested reply trees incomplete | X API `conversation_id` with your token is complete |

## Media-as-training

LoRA text models only see **text**. So for now media enters as:

- explicit URL blocks  
- operator captions you add  
- later OCR/transcript fields

Multimodal fine-tunes can load `meta.media` paths once files are local under `data/media/`.

## Best operator workflow for max fidelity

1. Keep pasting root links into `urls.txt`  
2. For crown jewels: open Threadreader → **Save as PDF** → drop in `data/raw/threads/`  
3. Optional: download key videos offline and note filenames  
4. We re-run `thread-pull` + annotate  

That’s how subposts + media become first-class without your full archive password.
