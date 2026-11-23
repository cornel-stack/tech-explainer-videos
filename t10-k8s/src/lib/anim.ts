import { interpolate, spring, Easing } from "remotion";

// A soft, overshooting pop used for most entrances.
export function pop(frame: number, at: number, fps: number, damping = 14) {
  return spring({
    frame: frame - at,
    fps,
    config: { damping, mass: 0.7, stiffness: 120 },
  });
}

// Linear-ish eased ramp between two frames, clamped.
export function ramp(frame: number, from: number, to: number) {
  return interpolate(frame, [from, to], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
    easing: Easing.inOut(Easing.cubic),
  });
}

// Fade a thing in then out across a window (enter/hold/exit in frames).
export function inOut(
  frame: number,
  start: number,
  enter: number,
  hold: number,
  exit: number,
) {
  return interpolate(
    frame,
    [start, start + enter, start + enter + hold, start + enter + hold + exit],
    [0, 1, 1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );
}

// Translate helper: returns a px offset that springs from `dist` to 0.
export function slideIn(frame: number, at: number, fps: number, dist = 40) {
  return (1 - pop(frame, at, fps)) * dist;
}

export type Beat = { mark: string; atFrame: number };

// Frame at which a named beat fires (relative to the item's own start).
export function beatAt(beats: Beat[], mark: string, fallback = 0): number {
  const b = beats.find((x) => x.mark === mark);
  return b ? b.atFrame : fallback;
}

// Has a named beat happened yet at this frame?
export function beatHit(beats: Beat[], mark: string, frame: number): boolean {
  const b = beats.find((x) => x.mark === mark);
  return b ? frame >= b.atFrame : false;
}
