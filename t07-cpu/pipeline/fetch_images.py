#!/usr/bin/env python3
"""
Fetch REAL, freely-licensed photographs of actual Intel processors — one per chip
in the "Every Intel CPU" explainer. For each KEY (= the content item id) we try its
candidate queries in order — Wikimedia Commons first (public-domain / CC), then
Openverse (commercial + modification licenses) — and keep the first candidate that
downloads AND passes a content check (a real raster image, not blank/solid/tiny).
The image is converted to JPEG with Pillow and saved to public/images/<key>.jpg.

Every item has a specific query first (e.g. "Intel Core i7") and then generic
Intel-silicon fallbacks, so even the newest lines resolve to a real Intel photo
rather than a blank panel. A `hero` key supplies a striking CPU macro for the
thumbnail / intro.

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

# Reject brand logos / badges / stickers / wordmarks / slides — we want PHOTOS of
# silicon, not trademark artwork. Applied to every candidate title.
REJECT_TITLE = re.compile(
    r"(badge|logo|wordmark|sticker|icon|symbol|emblem|brandmark|roadmap|"
    r"slide|chart|graph|diagram|schematic|infographic|\.svg)", re.I)

# Reject COMPETITOR silicon — the generic "die/CPU macro" fallbacks otherwise pull
# AMD/Nvidia/etc. This is an Intel video; every chip photo must be Intel.
REJECT_BRAND = re.compile(
    r"\b(amd|ryzen|phenom|athlon|opteron|threadripper|epyc|radeon|nvidia|geforce|"
    r"qualcomm|snapdragon|mediatek|powerpc|motorola|cyrix|via nano)\b", re.I)

# Generic Intel-silicon fallbacks appended to every chip so a real photo always lands.
GENERIC = ["Intel CPU processor", "Intel processor chip", "Intel microprocessor", "Intel processor macro"]

# KEY (= content item id) -> ordered candidate queries. Specific photo first, then
# the generic Intel-silicon fallbacks so every line resolves to a real Intel photo.
KEYS = {
    "hero":    ["Intel CPU macro", "microprocessor die macro", "Intel processor pins macro"] + GENERIC,
    "i3":      ["Intel Core i3 processor", "Intel Core i3 CPU"] + GENERIC,
    "i5":      ["Intel Core i5 processor", "Intel Core i5 CPU"] + GENERIC,
    "i7":      ["Intel Core i7 processor", "Intel Core i7 CPU"] + GENERIC,
    "i9":      ["Intel Core i9 processor", "Intel Core i9 CPU"] + GENERIC,
    # Core Ultra family (modern) — NO generic tail, so a scarce line reuses a
    # Core-Ultra-family photo rather than falling back to an ancient Intel chip.
    "ultra":   ["Intel Meteor Lake die", "Intel Meteor Lake processor", "Intel Core Ultra processor", "Intel Core Ultra laptop"],
    "ultrax":  ["Intel Lunar Lake die", "Intel Lunar Lake processor", "Intel Arc graphics chip", "Intel Core Ultra laptop"],
    "series3": ["Intel Panther Lake processor", "Intel Core Ultra processor", "Intel Core Ultra laptop", "Intel Lunar Lake processor"],
    "nseries": ["Intel N100 processor", "Intel NUC mini PC", "mini PC computer"] + GENERIC,
    "atom":    ["Intel Atom processor", "Intel Atom CPU"] + GENERIC,
    "celeron": ["Intel Celeron processor", "Intel Pentium processor", "silicon wafer semiconductor"] + GENERIC,
    "vpro":    ["Intel vPro laptop", "business laptop computer", "laptop motherboard"] + GENERIC,
    "xeon":    ["Intel Xeon processor", "server CPU Xeon", "data center server rack"] + GENERIC,
    "wafer":   ["silicon wafer semiconductor", "semiconductor wafer"],
}

ACCEPT_TOKENS = {}

# A candidate's title must contain one of these on-topic tokens (guards off-topic
# collisions) AND survive the brand/logo rejectors above. Chip keys REQUIRE the
# "intel" brand token so a generic "die macro" can't pull a competitor's silicon;
# platform/budget keys also allow device-context tokens (laptop, mini PC, wafer).
BROLL_TOKENS = {
    "hero":    ["intel"],
    "i3":      ["intel", "i3"],
    "i5":      ["intel", "i5"],
    "i7":      ["intel", "i7"],
    "i9":      ["intel", "i9"],
    # modern keys require a FAMILY token (not bare "intel") so an empty search for a
    # brand-new line can't fuzzy-match an ancient Intel chip (e.g. a Pentium MMX).
    "ultra":   ["meteor lake", "core ultra", "lunar lake"],
    "ultrax":  ["lunar lake", "intel arc", "core ultra"],
    "series3": ["panther lake", "core ultra", "lunar lake", "meteor lake"],
    "nseries": ["intel", "n100", "n150", "n270", "nuc", "mini pc", "mini-pc"],
    "atom":    ["intel", "atom", "n270"],
    "celeron": ["intel", "celeron", "pentium", "wafer", "semiconductor", "silicon"],
    "vpro":    ["intel", "laptop", "motherboard", "thinkpad", "business"],
    "xeon":    ["intel", "xeon"],
    "wafer":   ["wafer", "semiconductor", "silicon"],
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


def load_good_image(b, min_mean=14, max_mean=248):
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
    # cap the long edge so bundled frames stay lean (product photos are plenty at 1600px)
    w, h = im.size
    cap = 1600
    if max(w, h) > cap:
        if w >= h:
            im = im.resize((cap, round(h * cap / w)))
        else:
            im = im.resize((round(w * cap / h), cap))
    path = OUT_DIR / f"{key}.jpg"
    im.save(path, "JPEG", quality=86)
    return path


# ---- Wikimedia Commons -----------------------------------------------------

def commons_search_file(query, limit=10):
    params = {
        "action": "query", "format": "json", "list": "search",
        "srsearch": query + " filetype:bitmap", "srnamespace": 6, "srlimit": limit,
    }
    data = json.loads(http_get(f"{COMMONS_API}?{urllib.parse.urlencode(params)}"))
    return [r["title"] for r in data.get("query", {}).get("search", [])]


def commons_imageinfo(title, width=1200):
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
    """A candidate's title must contain a known token for keys that have one AND must
    not be a logo/badge/wordmark/slide. Guards off-topic collisions + trademark art."""
    low = (text or "").lower()
    if REJECT_TITLE.search(low) or REJECT_BRAND.search(low):
        return False
    tokens = ACCEPT_TOKENS.get(key) or BROLL_TOKENS.get(key)
    if not tokens:
        return True
    return any(t in low for t in tokens)


def try_commons(query, key, min_mean, used=frozenset()):
    """Return (im, meta_dict) on success, else (None, None). Skips any source URL
    already claimed by another key (used) so chips don't share one photo."""
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
        source = info.get("descriptionurl", url)
        if source in used:
            continue  # already used for another chip — keep looking for a distinct shot
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
            "source": source,
        }
    return None, None


# ---- Openverse -------------------------------------------------------------

def try_openverse(query, key, min_mean, used=frozenset()):
    """Return (im, meta_dict) on success, else (None, None). Skips sources in `used`."""
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
        source = r.get("foreign_landing_url") or src
        if source in used:
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
            "source": source,
        }
    return None, None


# ---- main ------------------------------------------------------------------


def fetch_key(key, queries, used=frozenset()):
    # product photos are mostly bright (white backdrops); a modest floor just rejects
    # all-dark frames while allowing the bright shots through (max_mean guards blanks).
    min_mean = 30
    # try to land a DISTINCT photo first; if nothing distinct passes, allow reuse so
    # the key is never left blank (scarce lines like the newest Core Ultra may share).
    for allow_reuse in (False, True):
        pool = frozenset() if allow_reuse else used
        for query in queries:
            for source_name, fn in (("commons", try_commons), ("openverse", try_openverse)):
                time.sleep(0.4)  # pace search calls to stay under API rate limits
                try:
                    im, meta = fn(query, key, min_mean, pool)
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
                tag = "" if not allow_reuse else " (shared)"
                print(f"  [ok]   {key}: {source_name} <- \"{query}\"{tag}  ({meta['source']})")
                return meta
    print(f"  [skip] {key}: no usable image found")
    return None


def main():
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    manifest = {}
    used = set()  # source URLs already claimed — keeps each chip's photo distinct
    for key, queries in KEYS.items():
        try:
            meta = fetch_key(key, queries, used)
        except Exception as e:
            print(f"  [skip] {key}: unexpected error ({e})")
            meta = None
        if meta:
            manifest[key] = meta
            used.add(meta["source"])

    (OUT_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))

    lines = ["Image attributions for 'Every Intel CPU Explained' — required for CC-BY reuse.", ""]
    for key, m in manifest.items():
        lines.append(f"{key}: {m['credit']} — {m['source']}")
    (OUT_DIR / "CREDITS.txt").write_text("\n".join(lines) + "\n")

    print(f"\nDone: {len(manifest)}/{len(KEYS)} images fetched -> {OUT_DIR}")


if __name__ == "__main__":
    main()
