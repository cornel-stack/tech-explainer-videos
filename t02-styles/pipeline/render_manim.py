#!/usr/bin/env python3
"""Render driver for the Manim scenes used in "What Is an API?".

Renders every scene in SCENES to a flat file at:

    public/manim/<name>.mp4

Manim itself writes into a nested media directory, so after each render we
locate the produced mp4 and copy it to the flat location above.

Usage (invoked with cwd = t01-api project root, inside the Manim container):

    python3 pipeline/render_manim.py            # render all scenes
    python3 pipeline/render_manim.py --probe     # no render; write durations.json

The driver is deliberately robust: a single failing scene prints a warning
and the run continues with the remaining scenes.

HARD CONSTRAINT NOTE: this script is meant to run only inside GitHub CI's
Manim container. It is never meant to be run on a developer machine.
"""

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

# --- Project layout -----------------------------------------------------------
# All paths are relative to the project root (the cwd the driver is run from).
ROOT = Path(__file__).resolve().parent.parent
SCENES_DIR = ROOT / "scenes_manim"
OUT_DIR = ROOT / "public" / "manim"
MEDIA_DIR = ROOT / ".manim_media"  # scratch dir Manim writes its tree into

# Each scene: output name -> (python file, scene class name).
# These map 1:1 to public/manim/<name>.mp4.
SCENES = {
    "axis": ("axis.py", "Axis"),
    "nplus1": ("nplus1.py", "NPlusOne"),
    "decision": ("decision.py", "Decision"),
    "montage": ("montage.py", "Montage"),
}

# Render settings: 1920x1080, 60fps, high quality.
WIDTH = 1920
HEIGHT = 1080
FPS = 60


def log(msg):
    """Print a clearly-prefixed log line and flush immediately."""
    print(f"[render_manim] {msg}", flush=True)


def ensure_out_dir():
    """Create public/manim/ if it does not already exist."""
    OUT_DIR.mkdir(parents=True, exist_ok=True)


def find_produced_mp4(name):
    """Locate the mp4 Manim just wrote under the media tree.

    Manim writes to <media>/videos/<file-stem>/<res>/<name>.mp4 but the exact
    nesting varies by version, so we search the whole media dir for a matching
    file and return the most recently modified one.
    """
    candidates = list(MEDIA_DIR.rglob(f"{name}.mp4"))
    if not candidates:
        # Fall back to any mp4 under the media tree (last resort).
        candidates = list(MEDIA_DIR.rglob("*.mp4"))
    if not candidates:
        return None
    # Most recently modified wins (this scene's fresh render).
    candidates.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return candidates[0]


def render_scene(name, filename, scene_class):
    """Render one scene and copy its mp4 to public/manim/<name>.mp4.

    Returns True on success, False on failure (never raises).
    """
    scene_path = SCENES_DIR / filename
    if not scene_path.exists():
        log(f"WARNING: scene file missing: {scene_path} — skipping '{name}'")
        return False

    log(f"Rendering '{name}' ({scene_class}) from {scene_path} ...")

    cmd = [
        "manim",
        "-qh",                      # high quality
        "--fps", str(FPS),
        "-r", f"{WIDTH},{HEIGHT}",  # explicit resolution
        "-o", f"{name}.mp4",       # output file name (stem)
        "--media_dir", str(MEDIA_DIR),
        str(scene_path),
        scene_class,
    ]
    log("  cmd: " + " ".join(cmd))

    try:
        result = subprocess.run(
            cmd,
            cwd=str(ROOT),
            capture_output=True,
            text=True,
        )
    except FileNotFoundError:
        log("WARNING: 'manim' executable not found on PATH — skipping "
            f"'{name}'")
        return False
    except Exception as exc:  # noqa: BLE001 — stay robust, never crash the run
        log(f"WARNING: unexpected error launching manim for '{name}': {exc}")
        return False

    if result.returncode != 0:
        log(f"WARNING: manim exited {result.returncode} for '{name}'.")
        # Surface the tail of stderr to aid CI debugging.
        tail = (result.stderr or "").strip().splitlines()[-20:]
        for line in tail:
            log(f"  manim: {line}")
        return False

    # Locate the mp4 Manim produced and copy it to the flat location.
    produced = find_produced_mp4(name)
    if produced is None:
        log(f"WARNING: could not locate produced mp4 for '{name}' under "
            f"{MEDIA_DIR}")
        return False

    dest = OUT_DIR / f"{name}.mp4"
    try:
        shutil.copy2(produced, dest)
    except Exception as exc:  # noqa: BLE001
        log(f"WARNING: failed copying {produced} -> {dest}: {exc}")
        return False

    log(f"  OK: {produced}  ->  {dest}")
    return True


def probe_durations():
    """Write public/manim/durations.json mapping scene name -> seconds.

    Uses mutagen if available, else ffprobe, else skips the scene. Only scenes
    whose mp4 already exists are measured. Never raises.
    """
    ensure_out_dir()
    durations = {}

    for name in SCENES:
        mp4 = OUT_DIR / f"{name}.mp4"
        if not mp4.exists():
            log(f"probe: {mp4} not present — skipping")
            continue

        seconds = _duration_mutagen(mp4)
        if seconds is None:
            seconds = _duration_ffprobe(mp4)

        if seconds is None:
            log(f"probe: could not measure duration for '{name}' — skipping")
            continue

        durations[name] = round(float(seconds), 3)
        log(f"probe: {name} = {durations[name]}s")

    out = OUT_DIR / "durations.json"
    out.write_text(json.dumps(durations, indent=2) + "\n")
    log(f"probe: wrote {out}")
    return durations


def _duration_mutagen(mp4):
    """Return duration in seconds via mutagen, or None if unavailable."""
    try:
        from mutagen.mp4 import MP4
    except Exception:  # noqa: BLE001 — library simply not installed
        return None
    try:
        info = MP4(str(mp4)).info
        return float(info.length)
    except Exception as exc:  # noqa: BLE001
        log(f"probe: mutagen failed on {mp4}: {exc}")
        return None


def _duration_ffprobe(mp4):
    """Return duration in seconds via ffprobe subprocess, or None."""
    cmd = [
        "ffprobe", "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        str(mp4),
    ]
    try:
        result = subprocess.run(cmd, capture_output=True, text=True)
    except FileNotFoundError:
        return None
    except Exception as exc:  # noqa: BLE001
        log(f"probe: ffprobe error on {mp4}: {exc}")
        return None
    if result.returncode != 0:
        return None
    try:
        return float(result.stdout.strip())
    except ValueError:
        return None


def render_all():
    """Render every scene, continuing past individual failures."""
    ensure_out_dir()
    log(f"Project root: {ROOT}")
    log(f"Output dir:   {OUT_DIR}")

    results = {}
    for name, (filename, scene_class) in SCENES.items():
        results[name] = render_scene(name, filename, scene_class)

    ok = [n for n, v in results.items() if v]
    bad = [n for n, v in results.items() if not v]
    log(f"Done. Rendered OK: {ok or '(none)'}. Failed: {bad or '(none)'}.")

    # Record durations for whatever rendered successfully.
    probe_durations()

    # Exit 0 even with partial failures so CI can inspect what did render;
    # a total failure (nothing rendered) is a hard error.
    if not ok:
        log("ERROR: no scenes rendered successfully.")
        return 1
    return 0


def main(argv):
    if "--probe" in argv:
        probe_durations()
        return 0
    return render_all()


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
