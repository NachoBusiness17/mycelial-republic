import io

t = io.open("watch/inbox/mates_leave_protocol/receipts/receipt_20261014_cartographer.md", encoding="utf-8").read()
print("emdash:", t.count(chr(0x2014)))
print("dollars2:", "$$" in t)
print("os_environ:", "os.environ" in t)
print("GetEnvironmentVariable:", "GetEnvironmentVariable" in t)
print("bytes:", len(t.encode("utf-8")))
c = io.open("logs/mates/missions/mission_20261014_01_cartographer.claim", encoding="ascii").read()
print("claim:", c.strip())
