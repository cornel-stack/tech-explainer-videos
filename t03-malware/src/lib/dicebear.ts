import { createAvatar, type Style } from "@dicebear/core";
import {
  openPeeps,
  bottts,
  shapes,
  identicon,
  icons,
} from "@dicebear/collection";

// createAvatar is deterministic; memoise by (style+options) so we build each SVG once.
const cache = new Map<string, string>();

function svg(style: Style<any>, name: string, options: Record<string, unknown>) {
  const key = name + JSON.stringify(options);
  const hit = cache.get(key);
  if (hit) return hit;
  // Make the root <svg> fill its container (DiceBear sets its own width/height).
  const out = createAvatar(style, options as any)
    .toString()
    .replace(/<svg([^>]*)>/, (_m, attrs: string) => {
      const cleaned = attrs
        .replace(/\swidth="[^"]*"/, "")
        .replace(/\sheight="[^"]*"/, "");
      return `<svg${cleaned} width="100%" height="100%" preserveAspectRatio="xMidYMid meet">`;
    });
  cache.set(key, out);
  return out;
}

// ---- Human cast: Open Peeps ------------------------------------------------
export function peepSvg(seed: string, opts: Record<string, unknown> = {}) {
  return svg(openPeeps, "peep", {
    seed,
    backgroundColor: ["transparent"],
    radius: 0,
    ...opts,
  });
}

// ---- Machine / code layer: DiceBear --------------------------------------
// Servers get a robot face (bottts); APIs get an abstract geometric mark
// (shapes); raw endpoints get an identicon. Each is deterministic from its name
// so the Weather API always looks like the Weather API.
export function serverSvg(seed: string, bg = "#8B5CF6") {
  return svg(bottts, "server", {
    seed,
    backgroundColor: [bg.replace("#", "")],
    backgroundType: ["solid"],
    radius: 20,
  });
}

export function apiMarkSvg(seed: string, bg = "#F59E0B") {
  return svg(shapes, "api", {
    seed,
    backgroundColor: [bg.replace("#", "")],
    radius: 20,
  });
}

export function endpointSvg(seed: string) {
  return svg(identicon, "endpoint", { seed, backgroundColor: ["transparent"] });
}

export function iconSvg(seed: string, bg = "#2563EB") {
  return svg(icons, "icon", {
    seed,
    backgroundColor: [bg.replace("#", "")],
    radius: 20,
  });
}
