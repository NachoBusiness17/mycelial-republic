ROW
pointer: /mag/watch/room.jsonl
claim: room log alive, 2944 lines, last event ts 2026-08-31T04:59:27.417Z (agent:bootstrap)
type: probe
confidence: H
status: VERIFIED
evidence: wc -l = 2944; tail ts 04:59:27.417Z via tail -c 300 (keys/ts only, no content mined)
ROW
pointer: /board/.chat_offset, /board/.blade_room_bridge_state.json, /board/.deepseek_room_state.json
claim: tailer state pointers exist; mtimes Aug 31 04:30 (.chat_offset), Aug 29 08:30 (blade bridge), Aug 29 08:22 (deepseek room)
type: probe
confidence: H
status: VERIFIED
evidence: ls -la shows all three present; .chat_offset mtime latest (Aug 31 04:30)
