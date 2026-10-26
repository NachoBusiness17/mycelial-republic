"""Inject memory/rtfm_graph.json into the rtfm_graph.html shell (local files only)."""
import json

graph = open("memory/rtfm_graph.json", encoding="utf-8").read()
parsed = json.loads(graph)  # validate before embedding
blob = json.dumps(parsed, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")

shell = open("dashboard/static/museum/_rtfm_graph_shell.html", encoding="utf-8").read()
assert "__RTFM_GRAPH_JSON__" in shell
html = shell.replace("__RTFM_GRAPH_JSON__", blob)
open("dashboard/static/rtfm_graph.html", "w", encoding="utf-8", newline="\n").write(html)
print("rtfm_graph.html written:", len(html), "bytes ·", len(parsed["nodes"]), "nodes ·", len(parsed["edges"]), "edges")
