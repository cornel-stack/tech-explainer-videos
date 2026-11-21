import { loadFont as loadInter } from "@remotion/google-fonts/Inter";
import { loadFont as loadMono } from "@remotion/google-fonts/IBMPlexMono";

// Loaded once at module import; Remotion blocks the render until fonts are ready.
export const inter = loadInter("normal", {
  weights: ["400", "600", "700", "800", "900"],
});
export const plexMono = loadMono("normal", { weights: ["400", "500", "600"] });

export const fontsReady = Promise.all([
  inter.waitUntilDone(),
  plexMono.waitUntilDone(),
]);
