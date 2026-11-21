# Tech Explainer — video render pipeline

Self-contained projects that render faceless tech-explainer videos entirely in
GitHub Actions. Each video is one folder; one JSON of narration becomes a 1080p60
MP4 plus a full YouTube upload kit (title, two clickbait thumbnails, description,
tags, chapters, captions), published as a GitHub Release.

## Videos

| Dir | Video |
|---|---|
| `t01-api/` | What Is an API? |
| `t02-styles/` | Every API Style Explained |
| `t03-malware/` | Every Type of Malware Explained |
| `t04-os/` | Every Operating System Explained |
| `t05-boot/` | How an Operating System Works (the first second) |
| `t06-gpu/` | How a GPU Works — and Why AI Can't Run Without One |

## Stack

- **Remotion** (React) composites everything into the final MP4 in headless Chromium.
- **Manim** renders the animated diagrams (separate CI job, official Docker image).
- **three.js** (`@remotion/three`) for 3D heroes; **DiceBear / Open Peeps** for characters.
- **edge-tts** for narration + word-level caption timing.
- Real imagery/logos are fetched from free/CC0 sources (Wikimedia, Openverse, Simple Icons) and credited.

## Rendering

Each `tNN-*/content/*.json` drives its video. A render runs when you push a change
under that project's folder to `main`, or by dispatching its workflow manually:

```
gh workflow run t06-render.yml
```

The pipeline (per project workflow): render Manim scenes → synth TTS + fetch assets
→ render in parallel shards → ffmpeg-concat → publish a GitHub Release with the MP4
and the `youtube/` upload kit.

Every on-screen number is traced to a source; all visuals are original or
free/credited. Public repo → unlimited free Actions minutes.
