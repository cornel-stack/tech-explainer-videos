#!/usr/bin/env python3
"""
Pull a few Coco Material illustrations (CC BY 4.0) for the "figure doing an
activity" scenes and write public/coco/manifest.json. Fully best-effort: any
failure is skipped so the render never depends on it.

Usage:  python3 pipeline/fetch_coco.py
"""
import json
import socket
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "public" / "coco"
API = "https://cocomaterial.com/api/vectors/"
UA = {"User-Agent": "tech-explainer/1.0 (+https://github.com)"}

# name used in the Remotion scenes  ->  candidate Coco tags to search
WANT = {
    "restaurant": ["restaurant", "waiter", "eating", "dinner"],
    "developer": ["developer", "computer", "coding", "programmer"],
    "phone": ["smartphone", "phone", "mobile"],
    "airplane": ["airplane", "plane", "flight"],
}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        return json.loads(r.read().decode("utf-8"))


def download(url, dest):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=20) as r:
        data = r.read()
    if b"<svg" not in data[:2000].lower():
        return False
    dest.write_bytes(data)
    return True


def find_svg(tags):
    for tag in tags:
        try:
            q = urllib.parse.urlencode({"tags": tag, "page_size": 8})
            data = get_json(f"{API}?{q}")
        except Exception as e:
            print(f"    query '{tag}' failed: {e}")
            continue
        for item in data.get("results", []):
            svg = item.get("svg")
            if svg:
                return svg, tag, item.get("id")
    return None, None, None


def main():
    socket.setdefaulttimeout(20)
    OUT.mkdir(parents=True, exist_ok=True)
    manifest = {}
    for name, tags in WANT.items():
        svg, tag, vid = find_svg(tags)
        if not svg:
            print(f"  {name}: no match, skipping")
            continue
        dest = OUT / f"{name}.svg"
        try:
            if download(svg, dest):
                manifest[name] = f"coco/{name}.svg"
                print(f"  {name}: {tag} #{vid} -> {dest.name}")
        except Exception as e:
            print(f"  {name}: download failed ({e}), skipping")

    (OUT / "manifest.json").write_text(json.dumps(manifest, indent=2))
    (OUT / "CREDITS.txt").write_text(
        "Illustrations by Coco Material (https://cocomaterial.com), CC BY 4.0.\n"
    )
    print(f"Wrote public/coco/manifest.json ({len(manifest)} illustrations)")


if __name__ == "__main__":
    main()
