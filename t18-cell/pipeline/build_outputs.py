#!/usr/bin/env python3
"""
From render-input.json produce the upload kit:
  out/captions.srt     — word-grouped subtitles, absolute timing
  out/chapters.txt     — YouTube chapter list from segment starts
  out/description.txt   — title, promise, chapters, sources, asset credits

Usage:  python3 pipeline/build_outputs.py
"""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FPS = 60
CHUNK = 7


def ts(frames: int) -> str:
    s = frames / FPS
    h = int(s // 3600); m = int((s % 3600) // 60); sec = s % 60
    return f"{h:02d}:{m:02d}:{sec:06.3f}".replace(".", ",")


def mmss(seconds: int) -> str:
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    return (f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}")


def segments(data):
    for s in data["segments"]:
        yield s


def main():
    data = json.loads((ROOT / "render-input.json").read_text())
    out_dir = ROOT / "out"
    out_dir.mkdir(exist_ok=True)

    # ---- SRT -------------------------------------------------------------
    cues, n = [], 1
    for seg in segments(data):
        words = seg.get("words", [])
        base = seg["startFrame"]
        for i in range(0, len(words), CHUNK):
            grp = words[i:i + CHUNK]
            if not grp:
                continue
            start = base + grp[0]["startFrame"]
            end = base + grp[-1]["endFrame"]
            text = " ".join(w["text"] for w in grp)
            cues.append(f"{n}\n{ts(start)} --> {ts(end)}\n{text}\n")
            n += 1
    (out_dir / "captions.srt").write_text("\n".join(cues))

    # ---- chapters --------------------------------------------------------
    chap = "\n".join(f"{mmss(c['startSeconds'])} {c['title']}" for c in data["chapters"])
    (out_dir / "chapters.txt").write_text(chap + "\n")

    # ---- description -----------------------------------------------------
    src_lines = "\n".join(f"• {s['label']} — {s['url']}" for s in data["sources"])
    items = " · ".join(s["name"] for s in data["segments"] if s.get("kind") == "item")
    desc = f"""{data['title']}

{data['promise']}

Covered: {items}

CHAPTERS
{chap}

SOURCES (every number on screen is traced to one of these)
{src_lines}

CREDITS
• Characters: Open Peeps (CC0) via DiceBear · Machine avatars: DiceBear (MIT).
• Diagrams animated with Manim Community · 3D with three.js.
• Composited and rendered with Remotion. Voice: Microsoft Edge TTS.
"""
    (out_dir / "description.txt").write_text(desc)
    print(f"Wrote out/captions.srt ({n - 1} cues), out/chapters.txt, out/description.txt")


if __name__ == "__main__":
    main()
