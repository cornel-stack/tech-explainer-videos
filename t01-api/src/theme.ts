// The one design system for the whole video. Dark, premium, slightly neon.
// No blue, no white — warm cream ink on near-black, vivid accents.
export const theme = {
  bg: "#0A0A0C",
  bgDeep: "#050506",
  ink: "#EDE7DB", // warm cream (primary text) — never pure white
  inkSoft: "#A39E94",
  inkFaint: "#6B6861",
  line: "#2A2A31",
  paper: "#17171C", // card / panel surface
  paperHi: "#20202A",
  onAccent: "#0A0A0C", // text placed on top of a bright accent fill

  // Accent palette — NO BLUE.
  accents: {
    amber: "#FFC24B",
    coral: "#FF6B4A",
    mint: "#3DE0B0",
    violet: "#B06BFF",
    magenta: "#FF3E7F",
    gold: "#E8C24A",
  },

  // Semantic colours reused across scenes.
  client: "#FFC24B", // amber
  api: "#FF3E7F", // magenta
  server: "#B06BFF", // violet
  ok: "#3DE0B0", // mint
  warn: "#E8C24A", // gold
  err: "#FF6B4A", // coral

  radius: 24,
  radiusLg: 36,
  shadow: "0 22px 60px rgba(0,0,0,0.65)",
  shadowSoft: "0 10px 30px rgba(0,0,0,0.5)",
} as const;

// A coloured glow (neon feel) for a given accent.
export const glow = (c: string, strength = 0.55) =>
  `0 0 0 1px ${c}44, 0 0 34px ${c}${Math.round(strength * 255).toString(16).padStart(2, "0")}`;

export const fontStack = {
  sans: "Inter, system-ui, sans-serif",
  mono: "'IBM Plex Mono', ui-monospace, monospace",
};

// 1080p60 canvas.
export const CANVAS = { width: 1920, height: 1080, fps: 60 } as const;
