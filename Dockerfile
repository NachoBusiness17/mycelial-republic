# Mag sovereign stack — container boundary (not a host desktop pet).
# Agent tools, backend, and subprocesses run inside this cage.
# Host exposes only localhost ports + mounted operator dirs (memory/, watch/, …).

FROM python:3.12-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    MAG_CONTAINER=1 \
    MAG_BIND_HOST=0.0.0.0 \
    MAG_NO_MIRROR=1

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
        git \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN chmod +x scripts/container/entrypoint.sh \
    && mkdir -p memory/biography memory/briefs logs state watch queue/handoff queue/results

EXPOSE 8765 8000

# B7 (2026-09-29, tablet incident root cause #2): the old probe hit
# /api/v1/health on :8765, but that route is the dashboard's DEEP sanity
# sweep (mag.health.sanity) whose B2-375 powershell.exe resolution can never
# pass on Linux -- the app served 200 on / while the check 500'd and the
# container sat UNHEALTHY for 8h. Probe the pure liveness surface instead
# (same URL mag_launch.py uses for its dashboard gate). curl/wget are absent
# from python:*-slim, so python urllib is the in-image binary.
HEALTHCHECK --interval=15s --timeout=5s --start-period=30s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://127.0.0.1:8765/', timeout=4)"

ENTRYPOINT ["/app/scripts/container/entrypoint.sh"]
