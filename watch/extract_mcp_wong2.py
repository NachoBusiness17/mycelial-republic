import re, os, socket, tempfile, urllib.request, urllib.parse, ipaddress

URL = "https://raw.githubusercontent.com/wong2/awesome-mcp-servers/main/README.md"
ALLOWED_HOSTS = {"raw.githubusercontent.com"}

assert URL.startswith("https://"), "https only"
host = urllib.parse.urlsplit(URL).hostname
assert host in ALLOWED_HOSTS, "host not allowlisted"
for fam, _, _, _, sockaddr in socket.getaddrinfo(host, 443):
    ip = sockaddr[0]
    if ipaddress.ip_address(ip).is_private or ipaddress.ip_address(ip).is_loopback or ipaddress.ip_address(ip).is_reserved:
        raise SystemExit("resolved to private/reserved IP: " + ip)

p = os.path.join(tempfile.gettempdir(), "wong2_readme.md")
try:
    txt = open(p, encoding="utf-8", errors="ignore").read()
    print("cached", len(txt))
except FileNotFoundError:
    txt = urllib.request.urlopen(urllib.request.Request(URL, headers={"User-Agent": "Mozilla/5.0"}), timeout=30).read().decode("utf-8", "ignore")
    open(p, "w", encoding="utf-8").write(txt)
    print("fetched", len(txt))

entries = re.findall(r"^- \[([^\]]+)\]\((https?://[^)]+)\)", txt, re.M)
cats = [re.sub(r"<[^>]+>|[*`]", "", c).strip() for c in re.findall(r"^###\s+(.+)$", txt, re.M) if not c.strip().startswith("!")]
urls = {u for _, u in entries}
print("wong2 entries:", len(entries), "| unique repo urls:", len(urls), "| categories:", len(cats))

p2 = os.path.join("watch", "MCP_AWESOME_DIGEST.md")
txt2 = open(p2, encoding="utf-8", errors="ignore").read()
e2 = re.findall(r"^- \[([^\]]+)\]\((https?://[^)]+)\)", txt2, re.M)
u2 = {u for _, u in e2}
inter = urls & u2
print("punkpeye entries:", len(e2), "| union:", len(urls | u2), "| overlap:", len(inter))
print("overlap pct of wong2:", round(100 * len(inter) / max(1, len(urls))), "%")
p2cats = set(re.sub(r"<[^>]+>|[*`]", "", c).strip().lower() for c in re.findall(r"^###\s+(.+)$", txt2, re.M))
wonly = [c for c in cats if c.lower() not in p2cats]
print("wong2-only categories:", wonly[:15])
