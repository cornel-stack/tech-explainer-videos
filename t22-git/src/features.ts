// T16: a 3D padlock (three.js / @remotion/three) sits behind the intro title.
// Safe3D wraps it with a 2D fallback, so even if WebGL ever fails in CI the video
// still builds — flip to false and re-dispatch if that happens.
export const FEATURES = {
  hero3D: true,
};
