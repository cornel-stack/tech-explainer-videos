#!/usr/bin/env python3
"""
Narrate content/api.json with Microsoft Edge TTS and build render-input.json.

For the intro, every stage, and the outro this:
  1. synthesises narration -> public/audio/<seg>.mp3 (free neural voice, no key),
  2. captures edge-tts word-boundary timings,
  3. converts them to frames (60 fps), relative to each segment's own start,
  4. maps each beat's cue word and each spec's cue word to the frame it's spoken
     (beats are only emitted when their cue is actually found, so scenes fall
     back to their own defaults otherwise),
  5. lays the segments end to end and writes render-input.json (the zInput shape),
  6. folds in any Manim clip durations from public/manim/durations.json.

Usage:  python3 pipeline/synth.py            (defaults to content/api.json)
        python3 pipeline/synth.py content/api.json
"""
import asyncio
import json
import re
import sys
from pathlib import Path

import edge_tts
import mutagen

FPS = 60
WIDTH, HEIGHT = 1920, 1080
RATE = "-4%"                       # slow the voice a touch for comprehension
INTRO_TAIL = int(0.6 * FPS)
STAGE_TAIL = int(2.8 * FPS)        # room for the verdict + breathing after narration
OUTRO_TAIL = int(1.4 * FPS)

ROOT = Path(__file__).resolve().parent.parent


def norm(w: str) -> str:
    return re.sub(r"[^a-z0-9]", "", w.lower())


def audio_duration_s(path: Path):
    try:
        f = mutagen.File(str(path))
        return float(f.info.length) if f and f.info else None
    except Exception:
        return None


async def synth(text: str, voice: str, out_path: Path):
    communicate = edge_tts.Communicate(text, voice, boundary="WordBoundary", rate=RATE)
    audio = bytearray()
    boundaries = []
    async for chunk in communicate.stream():
        if chunk["type"] == "audio":
            audio.extend(chunk["data"])
        elif chunk["type"] == "WordBoundary":
            boundaries.append({
                "text": chunk["text"],
                "start_s": chunk["offset"] / 1e7,
                "end_s": (chunk["offset"] + chunk["duration"]) / 1e7,
            })
    out_path.write_bytes(bytes(audio))
    return boundaries


def words_from(boundaries):
    return [{
        "text": b["text"],
        "startFrame": round(b["start_s"] * FPS),
        "endFrame": round(b["end_s"] * FPS),
    } for b in boundaries]


def first_match_frame(cue: str, words, used: set):
    c = norm(cue)
    if not c:
        return None
    for i, w in enumerate(words):
        if i in used:
            continue
        nw = norm(w["text"])
        if nw == c or c in nw or nw in c:
            used.add(i)
            return w["startFrame"]
    return None


def map_beats(beats, words):
    """Emit a beat only if its cue word was actually spoken."""
    used, out = set(), []
    for b in beats:
        at = first_match_frame(b.get("cue", ""), words, used)
        if at is not None:
            out.append({"mark": b["mark"], "atFrame": at})
    out.sort(key=lambda x: x["atFrame"])
    return out


def map_specs(specs, words):
    used, out = set(), []
    for s in specs:
        at = first_match_frame(s.get("cue", ""), words, used)
        if at is None:
            at = words[int(len(words) * 0.3)]["startFrame"] if words else 0
        out.append({
            "label": s["label"], "value": s["value"],
            "atFrame": at, "source": s.get("source"),
        })
    return out


def load_coco():
    f = ROOT / "public" / "coco" / "manifest.json"
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text())
    except Exception:
        return {}


def load_manim():
    f = ROOT / "public" / "manim" / "durations.json"
    if not f.exists():
        return {}
    try:
        durs = json.loads(f.read_text())
    except Exception:
        return {}
    out = {}
    for name, secs in durs.items():
        clip = ROOT / "public" / "manim" / f"{name}.mp4"
        if clip.exists() and secs:
            out[name] = {"file": f"manim/{name}.mp4", "durationInFrames": round(float(secs) * FPS)}
    return out


async def narrate(seg_id, text, voice):
    rel = f"audio/{seg_id}.mp3"
    abs_path = ROOT / "public" / rel
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  narrate {seg_id} …")
    boundaries = await synth(text, voice, abs_path)
    dur_s = audio_duration_s(abs_path) or ((boundaries[-1]["end_s"] + 0.4) if boundaries else 3.0)
    return rel, words_from(boundaries), max(1, round(dur_s * FPS))


async def main(script_path: str):
    data = json.loads(Path(script_path).read_text())
    voice = data.get("voice", "en-US-BrianNeural")
    cursor = 0
    chapters = []

    # intro
    rel, words, dur = await narrate("intro", data["intro"]["narration"], voice)
    intro = {
        "narration": data["intro"]["narration"], "audioFile": rel,
        "startFrame": cursor, "durationInFrames": dur + INTRO_TAIL,
        "words": words, "beats": map_beats(data["intro"].get("beats", []), words),
    }
    chapters.append({"title": "Intro", "startSeconds": round(cursor / FPS)})
    cursor += intro["durationInFrames"]

    # stages
    stages = []
    for st in data["stages"]:
        rel, words, dur = await narrate(st["id"], st["narration"], voice)
        stages.append({
            "id": st["id"], "scene": st["scene"], "chapter": st["chapter"],
            "icon": st["icon"], "accent": st["accent"],
            "narration": st["narration"], "audioFile": rel,
            "startFrame": cursor, "durationInFrames": dur + STAGE_TAIL,
            "words": words,
            "beats": map_beats(st.get("beats", []), words),
            "specs": map_specs(st.get("specs", []), words),
            "verdict": st.get("verdict", ""),
            "request": st.get("request"),
            "styles": st.get("styles"),
        })
        chapters.append({"title": st["chapter"], "startSeconds": round(cursor / FPS)})
        cursor += stages[-1]["durationInFrames"]

    # outro
    rel, words, dur = await narrate("outro", data["outro"]["narration"], voice)
    outro = {
        "narration": data["outro"]["narration"], "audioFile": rel,
        "startFrame": cursor, "durationInFrames": dur + OUTRO_TAIL,
        "words": words, "beats": map_beats(data["outro"].get("beats", []), words),
        "nextVideo": data["outro"]["nextVideo"], "question": data["outro"]["question"],
    }
    chapters.append({"title": "What's next", "startSeconds": round(cursor / FPS)})
    cursor += outro["durationInFrames"]

    out = {
        "id": data["id"], "title": data["title"], "series": data["series"],
        "keyNoun": data["keyNoun"], "promise": data["promise"], "accent": data["accent"],
        "fps": FPS, "width": WIDTH, "height": HEIGHT, "totalFrames": cursor,
        "sources": data["sources"],
        "intro": intro, "stages": stages, "outro": outro,
        "manim": load_manim(), "coco": load_coco(), "chapters": chapters,
    }
    (ROOT / "render-input.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote render-input.json — {len(stages)} stages, "
          f"{cursor} frames, {cursor / FPS:.1f}s ({cursor / FPS / 60:.2f} min)")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "content/api.json"
    asyncio.run(main(path))
