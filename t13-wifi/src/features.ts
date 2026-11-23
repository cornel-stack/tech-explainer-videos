// Flip hero3D to false and re-dispatch if a CI render ever fails inside WebGL —
// the Intro has a full 2D fallback, so the video still builds.
// hero3D off for T10: ComputeGrid3D is a GPU motif. The Kubernetes intro shows the
// animated reconciliation Manim clip behind the title instead (2D, always builds).
export const FEATURES = {
  hero3D: false,
};
