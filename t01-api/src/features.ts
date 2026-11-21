// Flip hero3D to false and re-dispatch if a CI render ever fails inside WebGL —
// the Intro has a full 2D fallback, so the video still builds.
export const FEATURES = {
  hero3D: true,
};
