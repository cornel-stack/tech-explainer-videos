// Flip hero3D to false and re-dispatch if a CI render ever fails inside WebGL —
// the Intro has a full 2D fallback, so the video still builds.
// hero3D off for T09: a 3D chip hero is off-topic for an OS video; the Intro shows
// the animated Manim legend behind the title instead (2D, always builds).
export const FEATURES = {
  hero3D: false,
};
