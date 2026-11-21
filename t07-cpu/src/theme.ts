// Design system for T07 "Every Intel CPU" — a "silicon / brushed-metal spec-
// sheet" look. Near-black with platinum ink and per-tier accent colours. No flat
// blue/white, NO brand logos (original chip tiles only). Accent KEY NAMES kept
// stable so shared components compile; values recoloured.
export const theme = {
  bg: "#0A0A0C",
  bgDeep: "#050506",
  ink: "#E8E9EC",
  inkSoft: "#8C8E92",
  inkFaint: "#55565A",
  line: "#22232A",
  paper: "#121318",
  paperHi: "#1A1B22",
  onAccent: "#0A0A0C",

  // Accent palette (keys reused; recoloured to CPU tiers).
  accents: {
    amber: "#FFB020", // i7 / primary
    coral: "#FF5C47", // i9 / "hot"
    mint: "#35E08A", // i5
    violet: "#B06BFF", // Core Ultra / NPU / AI
    magenta: "#2DD4BF", // i3 / low tier (teal)
    gold: "#C9CDD4", // neutral / silver
  },

  // Product-tier colours.
  tiers: {
    i3: "#2DD4BF",
    i5: "#35E08A",
    i7: "#FFB020",
    i9: "#FF5C47",
    ultra: "#B06BFF",
    xeon: "#E8C24A",
    low: "#C9CDD4",
  },

  client: "#35E08A",
  api: "#FFB020",
  server: "#B06BFF",
  ok: "#35E08A",
  warn: "#FFB020",
  err: "#FF5C47",

  radius: 18,
  radiusLg: 30,
  shadow: "0 22px 60px rgba(0,0,0,0.74)",
  shadowSoft: "0 10px 30px rgba(0,0,0,0.6)",
} as const;

export const glow = (c: string, strength = 0.5) =>
  `0 0 0 1px ${c}44, 0 0 30px ${c}${Math.round(strength * 255).toString(16).padStart(2, "0")}`;

export const fontStack = {
  sans: "Inter, system-ui, sans-serif",
  mono: "'IBM Plex Mono', ui-monospace, monospace",
};

export const CANVAS = { width: 1920, height: 1080, fps: 60 } as const;

export const tierColor = (t?: string): string =>
  (theme.tiers as Record<string, string>)[t ?? "low"] ?? theme.tiers.low;
