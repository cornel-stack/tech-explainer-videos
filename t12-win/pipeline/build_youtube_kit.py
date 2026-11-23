#!/usr/bin/env python3
"""
Assemble a ready-to-post YouTube upload kit in out/youtube/ — everything the
owner needs to publish: title(s), description, tags, chapters, pinned comment,
captions, and a checklist. Thumbnails (THUMBNAIL-A/B.png) are rendered into the
same folder by the CI workflow.

Usage:  python3 pipeline/build_youtube_kit.py          (defaults to content/api.json)
"""
import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


def mmss(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return (f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}")


def main(content_path: str):
    content = json.loads(Path(content_path).read_text())
    data = json.loads((ROOT / "render-input.json").read_text())
    yt = content.get("youtube", {})

    kit = ROOT / "out" / "youtube"
    kit.mkdir(parents=True, exist_ok=True)

    chapters = "\n".join(f"{mmss(c['startSeconds'])} {c['title']}" for c in data["chapters"])
    sources = "\n".join(f"• {s['label']} — {s['url']}" for s in data["sources"])
    hashtags = " ".join(yt.get("hashtags", []))
    titles = yt.get("titles", [content["title"]])
    primary = yt.get("primaryTitle", titles[0])

    # TITLE.txt
    title_txt = "PRIMARY TITLE (paste this one):\n" + primary + "\n\nALTERNATES (A/B test these):\n"
    title_txt += "\n".join(f"{i+1}. {t}" for i, t in enumerate(titles))
    (kit / "TITLE.txt").write_text(title_txt + "\n")

    # Image attributions (CC-BY requires visible credit) — from the fetched manifest.
    img_manifest = data.get("images", {}) or {}
    img_credits = "\n".join(
        f"• {m.get('credit', k)}" + (f" — {m['source']}" if m.get("source") else "")
        for k, m in img_manifest.items()
    )
    img_block = ""

    # DESCRIPTION.txt
    items = [s for s in data["segments"] if s.get("kind") in ("item", "stage")]
    STAT = {"loved": "👑", "meh": "😐", "hated": "💀"}
    outline = "\n".join(f"{STAT.get(s.get('status',''),'•')} {s['name']}" + (f" ({s['launched']})" if s.get("launched") else "") for s in items)
    desc = f"""{yt.get('hook', content.get('promise', ''))}

🖥️ Every version, its iconic desktop drawn from scratch, with history's verdict (👑 loved · 😐 meh · 💀 hated):
{outline}

Plus the famous 'tick-tock' pattern — a legend, then a dud, then a legend again. Every date and claim is sourced.

⏱️ CHAPTERS
{chapters}

📚 SOURCES (every claim on screen is traced to one of these)
{sources}
{img_block}
🔔 New tech explainer every week — subscribe so the next one finds you.
💬 {yt.get('pinnedComment', '')}

🎨 CREDITS
Desktops drawn from scratch (no Microsoft screenshots or logos) · Diagrams animated with Manim · Characters: Open Peeps (CC0) via DiceBear · Composited & rendered with Remotion · Voice: Microsoft Edge TTS.

{hashtags}
"""
    (kit / "DESCRIPTION.txt").write_text(desc)

    # TAGS.txt
    tags = ", ".join(yt.get("tags", []))
    (kit / "TAGS.txt").write_text(tags + f"\n\n({len(tags)} chars — YouTube allows 500)\n")

    # CHAPTERS.txt + PINNED-COMMENT.txt
    (kit / "CHAPTERS.txt").write_text(chapters + "\n")
    (kit / "PINNED-COMMENT.txt").write_text(yt.get("pinnedComment", "") + "\n")

    # captions
    srt = ROOT / "out" / "captions.srt"
    if srt.exists():
        shutil.copy(srt, kit / "CAPTIONS.srt")

    # README / checklist
    (kit / "README.txt").write_text(
        f"""YOUTUBE UPLOAD KIT — {primary}

Post checklist:
  1. Upload the MP4 (../{data['id']}.mp4).
  2. Title    → paste PRIMARY from TITLE.txt (alternates for A/B testing).
  3. Thumbnail→ upload THUMBNAIL-A.png (or THUMBNAIL-B.png — test both).
  4. Description → paste all of DESCRIPTION.txt (chapters auto-link).
  5. Tags     → paste TAGS.txt into the tags box.
  6. Subtitles→ upload CAPTIONS.srt (English).
  7. After publishing → post PINNED-COMMENT.txt and pin it.
  8. Category: Science & Technology. Audience: not made for kids.

Thumbnails:
  A = the authoritative angle (bold title + glowing chips).
  B = a curiosity hook (bold question + a character).
  Test both and keep whichever gets the higher click-through.
"""
    )

    files = sorted(p.name for p in kit.iterdir())
    print(f"Wrote out/youtube/ — {files}")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "content/api.json"
    main(path)
