#!/usr/bin/env python3
"""
Fetch REAL, freely-licensed assets for the "Every Operating System Explained" video.

Two parts, both fully best-effort (every failure caught + skipped, never crashes):

PART 1 — LOGOS from Simple Icons (CC0). For each key we try its candidate slugs in
order, downloading the monochrome single-path SVG from the jsDelivr CDN and keeping
the first that is a real SVG. Saved to public/logos/<key>.svg.

PART 2 — IMAGES (real context photos / portraits). For each key we try its candidate
queries in order — Wikimedia Commons first (free licenses), then Openverse (commercial
+ modification) — keeping the first candidate that downloads AND passes a content check
AND a RELEVANCE-TOKEN check (title must contain a relevant token, so a name search can't
grab an off-topic image). Converted to JPEG with Pillow, saved to public/images/<key>.jpg.

Outputs (only for keys that succeeded):
  public/logos/<key>.svg
  public/logos/manifest.json   {key: {file, slug, license}}
  public/logos/CREDITS.txt
  public/images/<key>.jpg
  public/images/manifest.json  {key: {file, credit, source, query}}
  public/images/CREDITS.txt

Run from the project root:

    python3 pipeline/fetch_assets.py
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
LOGO_DIR = ROOT / "public" / "logos"
IMG_DIR = ROOT / "public" / "images"

UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) "
      "Chrome/122.0.0.0 Safari/537.36 TechExplainerBot/1.0 (educational)")
COMMONS_API = "https://commons.wikimedia.org/w/api.php"
OPENVERSE_API = "https://api.openverse.org/v1/images/"
SIMPLEICONS_CDN = "https://cdn.jsdelivr.net/npm/simple-icons/icons/{slug}.svg"
TIMEOUT = 20
MIN_SIZE = 320  # minimum width AND height, in px

FREE_LICENSE_HINT = re.compile(r"(cc|creative commons|public domain|pd|pdm|no restrictions)", re.I)


# ---- PART 1: LOGOS (Simple Icons, CC0) -------------------------------------

LOGO_KEYS = {
    "freebsd":   ["freebsd"],
    "macos":     ["apple"],
    "ios":       ["apple"],
    "windows":   ["windows", "windows11"],
    "windowsnt": ["windows", "windows11"],
    "linux":     ["linux"],
    "android":   ["android"],
    "chromeos":  ["googlechrome", "chromeos"],
    "steamos":   ["steamdeck", "steam"],
    "harmonyos": ["huawei"],
    "unix":      ["unix"],      # may 404 — skip gracefully
    "bsd":       ["freebsd"],
    "msdos":     ["dos"],       # may 404 — skip
    "kaios":     ["kaios"],     # may 404 — skip
}


# ---- PART 2: IMAGES (context photos / portraits) ---------------------------

IMAGE_KEYS = {
    "datacenter":   ["server room data center", "data center servers"],
    "steamdeck":    ["Steam Deck handheld", "Valve Steam Deck"],
    "featurephone": ["feature phone keypad", "Nokia feature phone"],
    "torvalds":     ["Linus Torvalds", "Linus Torvalds portrait"],
    "ritchie":      ["Dennis Ritchie", "Ken Thompson Dennis Ritchie"],
    "androidrobot": ["Android robot statue", "Android mascot statue Google"],
    "smartphone":   ["smartphone in hand", "modern smartphone"],
    "laptop":       ["laptop computer desk", "laptop open screen"],
}

# A candidate's title must contain one of these tokens for keys that have one; any
# other key passes. Guards against off-topic collisions (a "Torvald" ship, a random
# Ritchie, a toy Android robot, a car named after a person, ...). Generic b-roll keys
# (a laptop, a smartphone) accept any on-topic photo and are omitted here.
ACCEPT_TOKENS = {
    "torvalds":     ["torvalds"],
    "ritchie":      ["ritchie", "thompson"],
    "steamdeck":    ["steam deck", "steamdeck"],
    "androidrobot": ["android"],
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


# ---- PART 1 impl -----------------------------------------------------------

def fetch_logo(key, slugs):
    """Try candidate slugs in order; save first real SVG. Return meta or None."""
    for slug in slugs:
        url = SIMPLEICONS_CDN.format(slug=slug)
        try:
            blob = http_get(url)
        except Exception as e:
            print(f"      simple-icons miss for '{slug}' ({e})")
            continue
        try:
            text = blob.decode("utf-8", "ignore").lstrip()
        except Exception:
            continue
        if not text.startswith("<svg"):
            continue
        try:
            LOGO_DIR.mkdir(parents=True, exist_ok=True)
            (LOGO_DIR / f"{key}.svg").write_bytes(blob)
        except Exception as e:
            print(f"      save failed for {key} ({e})")
            continue
        print(f"  [ok]   {key}: simple-icons <- \"{slug}\"")
        return {"file": f"logos/{key}.svg", "slug": slug, "license": "CC0 (Simple Icons)"}
    print(f"  [skip] {key}: no logo found")
    return None


def fetch_logos():
    print("== PART 1: logos (Simple Icons, CC0) ==")
    LOGO_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, slugs in LOGO_KEYS.items():
        try:
            meta = fetch_logo(key, slugs)
        except Exception as e:
            print(f"  [skip] {key}: unexpected error ({e})")
            meta = None
        if meta:
            manifest[key] = meta

    (LOGO_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    lines = [
        "Logo attributions for 'Every Operating System Explained'.",
        "All logos are from Simple Icons (https://simpleicons.org) and are CC0 "
        "(public domain dedication). Brand marks remain trademarks of their owners.",
        "",
    ]
    for key, m in manifest.items():
        lines.append(f"{key}: slug '{m['slug']}' — {m['license']}")
    (LOGO_DIR / "CREDITS.txt").write_text("\n".join(lines) + "\n")

    print(f"Logos: {len(manifest)}/{len(LOGO_KEYS)} fetched -> {LOGO_DIR}\n")
    return manifest


# ---- PART 2 impl: content validation ---------------------------------------

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
        if mean < min_mean or mean > max_mean or std < 10:
            return None
        return im.convert("RGB")
    except Exception:
        return None


def save_jpeg(im, key):
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    path = IMG_DIR / f"{key}.jpg"
    im.save(path, "JPEG", quality=88)
    return path


def title_relevant(key, text):
    """A candidate's title must contain a known token for keys that have one; any
    other key passes. Guards against off-topic name collisions."""
    tokens = ACCEPT_TOKENS.get(key)
    if not tokens:
        return True
    low = (text or "").lower()
    return any(t in low for t in tokens)


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


# b-roll keys are full-frame photos; a slightly higher floor avoids all-dark frames.
BROLL = {"datacenter", "smartphone", "laptop", "featurephone"}


def fetch_image(key, queries):
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


def fetch_images():
    print("== PART 2: images (Wikimedia Commons + Openverse) ==")
    IMG_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for key, queries in IMAGE_KEYS.items():
        try:
            meta = fetch_image(key, queries)
        except Exception as e:
            print(f"  [skip] {key}: unexpected error ({e})")
            meta = None
        if meta:
            manifest[key] = meta

    (IMG_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    lines = ["Image attributions for 'Every Operating System Explained' — required for CC-BY reuse.", ""]
    for key, m in manifest.items():
        lines.append(f"{key}: {m['credit']} — {m['source']}")
    (IMG_DIR / "CREDITS.txt").write_text("\n".join(lines) + "\n")

    print(f"Images: {len(manifest)}/{len(IMAGE_KEYS)} fetched -> {IMG_DIR}\n")
    return manifest


# ---- main ------------------------------------------------------------------

def main():
    logos = fetch_logos()
    images = fetch_images()
    print(f"Done: {len(logos)}/{len(LOGO_KEYS)} logos, {len(images)}/{len(IMAGE_KEYS)} images.")


if __name__ == "__main__":
    main()
