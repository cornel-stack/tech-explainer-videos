#!/usr/bin/env python3
"""
Fetch REAL, freely-licensed images for the "Every Type of Malware" explainer video.

For each KEY below we try its candidate queries in order — Wikimedia Commons first
(public-domain / CC), then Openverse (commercial + modification licenses) — and keep
the first candidate that downloads AND passes a content check (a real raster image,
not blank/solid/too small). The image is converted to JPEG with Pillow and saved to
public/images/<key>.jpg.

Outputs (only for keys that succeeded):
  public/images/<key>.jpg
  public/images/manifest.json  {key: {file, credit, source, query}}
  public/images/CREDITS.txt     one attribution line per image (required for CC-BY)

Fully best-effort: every network/parse/validation failure is caught and the key is
simply skipped — the script never crashes. Run from the project root:

    python3 pipeline/fetch_images.py
"""
import io
import json
import re
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "public" / "images"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/122.0.0.0 Safari/537.36 TechExplainerBot/1.0 (educational)")
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
OPENVERSE_API = "https://api.openverse.org/v1/images/"
TIMEOUT = 20
MIN_SIZE = 320  # minimum width AND height, in px

FREE_LICENSE_HINT = re.compile(r"(cc|creative commons|public domain|pd|pdm|no restrictions)", re.I)

# KEY -> ordered candidate queries (real, freely-licensed GPU / silicon imagery)
KEYS = {
    "gpu":        ["graphics card GPU", "video card PCB", "graphics card pcb", "graphics processing unit card"],
    "datacenter": ["data center server racks", "server room data center", "supercomputer data center"],
    "wafer":      ["silicon wafer semiconductor", "semiconductor wafer"],
    "chip":       ["microprocessor die", "integrated circuit die", "computer processor chip macro"],
}

ACCEPT_TOKENS = {}

# Generic imagery, but the bare words collide with unrelated hits, so require a
# co-occurring on-topic token in the candidate title.
BROLL_TOKENS = {
    "gpu":        ["graphics card", "video card", "gpu", "geforce", "radeon", "graphics processing"],
    "datacenter": ["data center", "data centre", "datacenter", "server room", "server rack", "supercomputer"],
    "wafer":      ["wafer", "semiconductor", "silicon"],
    "chip":       ["die", "microprocessor", "integrated circuit", "processor", "chip", "semiconductor", "cpu"],
}


def http_get(url, timeout=TIMEOUT, retries=3):
    """GET with a realistic UA and simple backoff on 429 / transient errors."""
    last = None
    for attempt in range(retries):
        req = urllib.request.Request(url, headers={"User-Agent": UA})
        try:
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            last = e
            if e.code == 429 and attempt < retries - 1:
                time.sleep(2.0 * (attempt + 1))
                continue
            raise
        except Exception as e:
            last = e
            if attempt < retries - 1:
                time.sleep(1.0 * (attempt + 1))
                continue
            raise
    if last:
        raise last


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def is_image_bytes(b):
    """Reject HTML error pages / corrupt downloads."""
    if len(b) < 2000:
        return False
    return (
        b[:3] == b"\xff\xd8\xff"                       # jpeg
        or b[:8] == b"\x89PNG\r\n\x1a\n"               # png
        or (b[:4] == b"RIFF" and b[8:12] == b"WEBP")   # webp
        or b[:6] in (b"GIF87a", b"GIF89a")             # gif
    )


def load_good_image(b, min_mean=14, max_mean=246):
    """Validate content and return a loaded RGB PIL image, or None.

    Beyond a valid format, reject images that are blacked-out, blank, a single solid
    colour, or too small (< MIN_SIZE on either axis)."""
    if not is_image_bytes(b):
        return None
    try:
        from PIL import Image, ImageStat
        im = Image.open(io.BytesIO(b))
        im.load()
        w, h = im.size
        if w < MIN_SIZE or h < MIN_SIZE:
            return None
        g = im.convert("L")
        g.thumbnail((128, 128))
        stat = ImageStat.Stat(g)
        mean, std = stat.mean[0], stat.stddev[0]
        # near-black (blacked out) / near-white (blank) / solid colour (no detail)
        if mean < min_mean or mean > max_mean or std < 10:
            return None
        return im.convert("RGB")
    except Exception:
        return None


def save_jpeg(im, key):
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    path = OUT_DIR / f"{key}.jpg"
    im.save(path, "JPEG", quality=88)
    return path


# ---- Wikimedia Commons -----------------------------------------------------

def commons_search_file(query, limit=8):
    params = {
        "action": "query", "format": "json", "list": "search",
        "srsearch": query + " filetype:bitmap", "srnamespace": 6, "srlimit": limit,
    }
    data = json.loads(http_get(f"{COMMONS_API}?{urllib.parse.urlencode(params)}"))
    return [r["title"] for r in data.get("query", {}).get("search", [])]


def commons_imageinfo(title, width=1000):
    params = {
        "action": "query", "format": "json", "titles": title,
        "prop": "imageinfo", "iiprop": "url|extmetadata|mime", "iiurlwidth": width,
    }
    data = json.loads(http_get(f"{COMMONS_API}?{urllib.parse.urlencode(params)}"))
    for _, page in data.get("query", {}).get("pages", {}).items():
        info = page.get("imageinfo")
        if info:
            return info[0]
    return None


def title_relevant(key, text):
    """A candidate's title must contain a known token for keys that have one; any other
    key passes. Guards against off-topic collisions (a "Love Letter" painting, a Toyota
    Mirai car, a public-bus "dress code" screen, a Temple of Olympian Zeus, ...)."""
    tokens = ACCEPT_TOKENS.get(key) or BROLL_TOKENS.get(key)
    if not tokens:
        return True
    low = (text or "").lower()
    return any(t in low for t in tokens)


def try_commons(query, key, min_mean):
    """Return (im, meta_dict) on success, else (None, None)."""
    try:
        titles = commons_search_file(query)
    except Exception as e:
        print(f"      commons search failed for '{query}' ({e})")
        return None, None
    for title in titles:
        if not title_relevant(key, title):
            continue
        time.sleep(0.4)  # be polite to the Commons API (avoid 429)
        try:
            info = commons_imageinfo(title)
        except Exception:
            continue
        if not info:
            continue
        mime = info.get("mime", "")
        if not mime.startswith("image/") or mime == "image/svg+xml":
            continue
        meta = info.get("extmetadata", {})
        lic = strip_html(meta.get("LicenseShortName", {}).get("value", ""))
        if not FREE_LICENSE_HINT.search(lic):
            continue
        url = (info.get("thumburl") or info.get("url") or "").split("?")[0]
        if not url:
            continue
        try:
            blob = http_get(url)
        except Exception:
            continue
        im = load_good_image(blob, min_mean=min_mean)
        if im is None:
            continue
        author = strip_html(meta.get("Artist", {}).get("value", "")) or "Unknown"
        clean_title = title.replace("File:", "")
        return im, {
            "credit": f"{clean_title} — {author} ({lic or 'free license'})",
            "source": info.get("descriptionurl", url),
        }
    return None, None


# ---- Openverse -------------------------------------------------------------

def try_openverse(query, key, min_mean):
    """Return (im, meta_dict) on success, else (None, None)."""
    params = {
        "q": query, "license_type": "commercial,modification",
        "page_size": 12, "mature": "false", "format": "json",
    }
    url = f"{OPENVERSE_API}?{urllib.parse.urlencode(params)}"
    try:
        data = json.loads(http_get(url))
    except Exception as e:
        print(f"      openverse search failed for '{query}' ({e})")
        return None, None
    for r in data.get("results", []):
        src = r.get("url") or r.get("thumbnail")
        if not src:
            continue
        if not title_relevant(key, r.get("title") or ""):
            continue
        try:
            blob = http_get(src)
        except Exception:
            continue
        im = load_good_image(blob, min_mean=min_mean)
        if im is None:
            continue
        author = strip_html(r.get("creator") or "Unknown")
        lic = f"CC {(r.get('license') or '').upper()} {r.get('license_version') or ''}".strip()
        title = strip_html(r.get("title") or query)
        return im, {
            "credit": f"{title} — {author} ({lic})",
            "source": r.get("foreign_landing_url") or src,
        }
    return None, None


# ---- main ------------------------------------------------------------------

# b-roll keys are full-frame photos; a slightly higher floor avoids all-dark frames.
BROLL = {"gpu", "datacenter", "wafer", "chip"}


def fetch_key(key, queries):
    min_mean = 40 if key in BROLL else 14
    for query in queries:
        for source_name, fn in (("commons", try_commons), ("openverse", try_openverse)):
            time.sleep(0.4)  # pace search calls to stay under API rate limits
            try:
                im, meta = fn(query, key, min_mean)
            except Exception as e:
                print(f"      {source_name} error for '{query}' ({e})")
                continue
            if im is None:
                continue
            try:
                save_jpeg(im, key)
            except Exception as e:
                print(f"      save failed for {key} ({e})")
                continue
            meta["file"] = f"images/{key}.jpg"
            meta["query"] = query
            print(f"  [ok]   {key}: {source_name} <- \"{query}\"  ({meta['source']})")
            return meta
    print(f"  [skip] {key}: no usable image found")
    return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, queries in KEYS.items():
        try:
            meta = fetch_key(key, queries)
        except Exception as e:
            print(f"  [skip] {key}: unexpected error ({e})")
            meta = None
        if meta:
            manifest[key] = meta

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    lines = ["Image attributions for 'How a GPU Works' — required for CC-BY reuse.", ""]
    for key, m in manifest.items():
        lines.append(f"{key}: {m['credit']} — {m['source']}")
    (OUT_DIR / "CREDITS.txt").write_text("\n".join(lines) + "\n")

    print(f"\nDone: {len(manifest)}/{len(KEYS)} images fetched -> {OUT_DIR}")


if __name__ == "__main__":
    main()
