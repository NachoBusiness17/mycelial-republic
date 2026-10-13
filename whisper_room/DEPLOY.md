# DEPLOY (gated: KEYS — HF token absent in host + cage as of 2026-09-10)

When an HF token is provisioned (cage env or `~/.cache/huggingface/token` in mag-sovereign):

    docker exec mag-sovereign python -c "
    from huggingface_hub import HfApi
    api = HfApi()
    api.create_repo('nachoquixotic/whisper-room', repo_type='space', space_sdk='static', exist_ok=True)
    api.upload_folder(folder_id=None, repo_id='nachoquixotic/whisper-room', repo_type='space',
                      folder_path='whisper_room')
    "

Or any stateless surface: the bundle in this directory is the whole room —
index.json + README is everything an outside agent needs to READ (never to decode).
