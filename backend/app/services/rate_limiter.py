"""
Simple in-memory sliding-window rate limiter, per client IP. Good enough
to stop one client (or a burst of repeated testing) from draining the
shared Groq free-tier quota right before judging — not meant to be a
production-grade distributed limiter. State resets if the server
restarts/redeploys, which is fine for a hackathon demo.
"""
import time
from collections import defaultdict
from fastapi import Request

WINDOW_SECONDS = 60
MAX_REQUESTS_PER_WINDOW = 8

_request_log: dict[str, list[float]] = defaultdict(list)


def get_client_ip(request: Request) -> str:
    # Render (and most hosts) sit behind a proxy, so the real client IP
    # is in X-Forwarded-For, not request.client.host.
    forwarded = request.headers.get("x-forwarded-for")
    if forwarded:
        return forwarded.split(",")[0].strip()
    return request.client.host if request.client else "unknown"


def is_rate_limited(client_ip: str) -> bool:
    now = time.time()
    timestamps = _request_log[client_ip]
    while timestamps and timestamps[0] < now - WINDOW_SECONDS:
        timestamps.pop(0)
    if len(timestamps) >= MAX_REQUESTS_PER_WINDOW:
        return True
    timestamps.append(now)
    return False