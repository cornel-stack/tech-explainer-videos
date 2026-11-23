#!/usr/bin/env python3
"""
Narrate content/styles.json (an "Every X" video of N segments) with Microsoft
Edge TTS and build render-input.json (the zInput shape).

For each segment this synthesises narration, captures edge-tts word timings,
converts them to frames (60 fps, segment-relative), maps beat/spec cue words to
the frame they're spoken (beats only emitted when the cue is found; specs stagger
if a cue is missing), lays segments end to end, and folds in any Manim clip
durations from public/manim/durations.json.

Usage:  python3 pipeline/synth.py            (defaults to content/styles.json)
        python3 pipeline/synth.py content/styles.json
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
RATE = "-4%"
TAILS = {"intro": 0.6, "interlude": 1.8, "item": 2.4, "outro": 1.4}
CHAP = {"intro": "Intro", "outro": "What's next"}
INTERLUDE_CHAP = {"timeline": "40 years in one line", "tocktick": "The every-other-one curse"}

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


def first_match_frame(cue, words, used):
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
    used, out = set(), []
    for b in beats:
        at = first_match_frame(b.get("cue", ""), words, used)
        if at is not None:
            out.append({"mark": b["mark"], "atFrame": at})
    out.sort(key=lambda x: x["atFrame"])
    return out


def map_specs(specs, words):
    """Cue word -> frame; missing cues stagger across the first 70% of the segment
    so a stack of specs doesn't all pop on the same frame."""
    used, out = set(), []
    span = words[-1]["startFrame"] if words else 0
    for i, s in enumerate(specs):
        at = first_match_frame(s.get("cue", ""), words, used)
        if at is None:
            at = round(span * 0.15 + (span * 0.55) * (i / max(1, len(specs) - 1)))
        out.append({"label": s["label"], "value": s["value"], "atFrame": at, "source": s.get("source")})
    return out


def load_json(rel):
    f = ROOT / "public" / rel
    if not f.exists():
        return {}
    try:
        return json.loads(f.read_text())
    except Exception:
        return {}


def load_manim():
    """Attach every public/manim/*.mp4 clip. Duration comes from durations.json
    (written by the scenes job's HOST ffprobe step — reliable), with mutagen then
    a safe default as fallback. We FLOOR to frames so <Loop> restarts the clip
    seamlessly (never a frozen tail). Scanning files directly means a clip is
    never silently dropped even if durations.json is missing."""
    d = ROOT / "public" / "manim"
    out = {}
    if not d.exists():
        return out
    durs = load_json("manim/durations.json")
    for clip in sorted(d.glob("*.mp4")):
        name = clip.stem
        secs = durs.get(name)
        if not secs or secs <= 0:
            secs = audio_duration_s(clip) or 0
        if not secs or secs <= 0:
            secs = 22.0
        out[name] = {"file": f"manim/{name}.mp4", "durationInFrames": max(1, int(secs * FPS))}
        print(f"  manim clip: {name} ({secs:.1f}s -> {int(secs * FPS)}f)")
    return out


async def narrate(seg_id, text, voice):
    rel = f"audio/{seg_id}.mp3"
    abs_path = ROOT / "public" / rel
    abs_path.parent.mkdir(parents=True, exist_ok=True)
    print(f"  narrate {seg_id} …")
    boundaries = await synth(text, voice, abs_path)
    dur_s = audio_duration_s(abs_path) or ((boundaries[-1]["end_s"] + 0.4) if boundaries else 3.0)
    return rel, words_from(boundaries), dur_s


async def main(script_path: str):
    data = json.loads(Path(script_path).read_text())
    voice = data.get("voice", "en-US-BrianNeural")

    cursor = 0
    out_segs = []
    chapters = []
    item_no = 0

    for idx, s in enumerate(data["segments"]):
        kind = s["kind"]
        seg_id = s.get("id") or f"{idx:02d}-{kind}"
        rel, words, dur_s = await narrate(seg_id, s["narration"], voice)
        tail = int(TAILS.get(kind, 1.5) * FPS)
        dur_frames = max(1, round(dur_s * FPS)) + tail

        seg = {
            "kind": kind,
            "narration": s["narration"],
            "audioFile": rel,
            "startFrame": cursor,
            "durationInFrames": dur_frames,
            "words": words,
            "beats": map_beats(s.get("beats", []), words),
        }
        if s.get("manim"):
            seg["manim"] = s["manim"]  # intro + interludes + item overrides
        if kind == "item":
            item_no += 1
            seg.update({
                "id": s["id"], "name": s["name"], "launched": s.get("launched", ""),
                "cat": s.get("cat", ""), "status": s.get("status", "meh"), "skin": s.get("skin", "flat"),
                "accent": s.get("accent", "#35E08A"), "icon": s.get("icon", "server"),
                "specs": map_specs(s.get("specs", []), words), "verdict": s.get("verdict", ""),
            })
            title = f"{item_no}. {s['name']}"
        elif kind == "interlude":
            title = INTERLUDE_CHAP.get(s.get("manim", ""), "Primer")
        elif kind == "outro":
            seg.update({"nextVideo": s.get("nextVideo", ""), "question": s.get("question", "")})
            title = CHAP["outro"]
        else:
            title = CHAP.get(kind, kind)

        out_segs.append(seg)
        chapters.append({"title": title, "startSeconds": round(cursor / FPS)})
        cursor += dur_frames

    total_items = item_no
    out = {
        "id": data["id"], "title": data["title"], "series": data["series"],
        "keyNoun": data["keyNoun"], "promise": data["promise"], "accent": data["accent"],
        "fps": FPS, "width": WIDTH, "height": HEIGHT, "totalFrames": cursor,
        "sources": data["sources"], "segments": out_segs,
        "manim": load_manim(), "coco": load_json("coco/manifest.json"),
        "images": load_json("images/manifest.json"),
        "logos": load_json("logos/manifest.json"),
        "chapters": chapters,
    }
    (ROOT / "render-input.json").write_text(json.dumps(out, indent=2))
    print(f"\nWrote render-input.json — {len(out_segs)} segments ({total_items} items), "
          f"{cursor} frames, {cursor / FPS:.1f}s ({cursor / FPS / 60:.2f} min)")


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "content/styles.json"
    asyncio.run(main(path))
