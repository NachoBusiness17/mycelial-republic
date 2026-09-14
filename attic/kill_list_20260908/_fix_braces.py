from pathlib import Path
p = Path("dashboard/static/wave.html")
h = p.read_text(encoding="utf-8")
# 1) close refresh try/finally at the real end of refresh (before graph click)
old_end = '''      }
    }
    graph.addEventListener("click", (e) => {
'''
new_end = '''      }
      } finally { inflight = false; }
    }
    graph.addEventListener("click", (e) => {
'''
if old_end not in h:
    raise SystemExit("refresh end missing")
h = h.replace(old_end, new_end, 1)
# 2) remove stray finally after boot
old_boot = '''    boot(); /* gpu module below */
    } finally { inflight = false; }
    }
    setInterval(refresh, 4000);
'''
new_boot = '''    boot(); /* gpu module below */
    setInterval(refresh, 4000);
'''
if old_boot not in h:
    raise SystemExit("stray finally missing:\n" + h[h.find("boot();"):h.find("boot();")+200])
h = h.replace(old_boot, new_boot, 1)
p.write_text(h, encoding="utf-8")
# brace balance in script
script = h.split("<script>",1)[1].split("</script>",1)[0]
print("braces", script.count("{"), script.count("}"))
print("stray", "} finally { inflight" in h[h.find("boot();"):h.find("boot();")+120])
print("ok")
