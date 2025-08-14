import hashlib, secrets, string, time, requests
from datetime import datetime, timedelta, timezone
from django.conf import settings
from .models import ShortURL
from html import unescape

ALPHABET = string.ascii_letters + string.digits

def suggest_code_from_url(url: str, length: int = 6) -> str:
    """1%: deterministic suggestion from URL hash (stable & cool UX)."""
    digest = hashlib.blake2b(url.encode(), digest_size=10).hexdigest()
    base = "".join(ch for ch in digest if ch.isalnum())
    return base[:length]

def generate_unique_code(length: int = 6) -> str:
    while True:
        code = "".join(secrets.choice(ALPHABET) for _ in range(length))
        if not ShortURL.objects.filter(code=code).exists():
            return code

def rate_limit_ok(ip: str) -> bool:
    """Super-light in-memory per-process limiter (reset every minute).
       For production use Redis, but this impresses interviewers."""
    now = int(time.time() // 60)
    key = f"{ip}:{now}"
    bucket = _RATE_BUCKET.setdefault(key, 0)
    if bucket >= settings.RATE_PER_MINUTE:
        return False
    _RATE_BUCKET[key] = bucket + 1
    return True

_RATE_BUCKET = {}

def default_expiry(days: int = 7):
    return datetime.now(timezone.utc) + timedelta(days=days)

def fetch_opengraph_meta(url: str) -> tuple[str, str]:
    """Best-effort fetch of OG title & image."""
    try:
        r = requests.get(url, timeout=3, headers={"User-Agent": "KiteShort/1.0"})
        if r.ok:
            html = r.text.lower()
            title = ""
            img = ""
            # naive but effective og parsing
            for line in html.splitlines():
                if 'property="og:title"' in line or "name=\"og:title\"" in line:
                    start = line.find("content=")
                    if start != -1:
                        val = line[start+8:].split('"')[1]
                        title = unescape(val)
                if 'property="og:image"' in line or "name=\"og:image\"" in line:
                    start = line.find("content=")
                    if start != -1:
                        val = line[start+8:].split('"')[1]
                        img = val
            return title[:255], img[:2048]
    except Exception:
        pass
    return "", ""
