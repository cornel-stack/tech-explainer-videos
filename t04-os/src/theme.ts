// Design system for T04 "Every Operating System" — a premium, dark "OS archive"
// look with per-FAMILY colour coding. Near-black, off-white ink, no flat blue/white.
// Accent KEY NAMES kept stable so shared components compile; values recoloured.
export const theme = {
  bg: "#09090C",
  bgDeep: "#050507",
  ink: "#E9E8E4",
  inkSoft: "#90908C",
  inkFaint: "#5C5C58",
  line: "#22222A",
  paper: "#121218",
  paperHi: "#1A1A22",
  onAccent: "#09090C",

  // Accent palette (keys reused from prior videos; recoloured for OS families).
  accents: {
    amber: "#FFB020", // Google family
    coral: "#FF6B4A", // other / accent
    mint: "#35FF9E", // Linux family / primary
    violet: "#9B8CFF", // Microsoft family
    magenta: "#2DD4BF", // UNIX/BSD family (teal)
    gold: "#C9CDD4", // Apple family (silver)
  },

  // OS family colours (the taxonomy spine).
  families: {
    unix: "#2DD4BF", // teal
    linux: "#35FF9E", // green
    ms: "#9B8CFF", // violet
    google: "#FFB020", // amber
    apple: "#C9CDD4", // silver
    other: "#FF6B4A", // coral
  },

  client: "#35FF9E",
  api: "#FFB020",
  server: "#9B8CFF",
  ok: "#35FF9E",
  warn: "#FFB020",
  err: "#FF6B4A",

  radius: 20,
  radiusLg: 32,
  shadow: "0 22px 60px rgba(0,0,0,0.72)",
  shadowSoft: "0 10px 30px rgba(0,0,0,0.58)",
} as const;

export const glow = (c: string, strength = 0.5) =>
  `0 0 0 1px ${c}44, 0 0 30px ${c}${Math.round(strength * 255).toString(16).padStart(2, "0")}`;

export const fontStack = {
  sans: "Inter, system-ui, sans-serif",
  mono: "'IBM Plex Mono', ui-monospace, monospace",
};

export const CANVAS = { width: 1920, height: 1080, fps: 60 } as const;

// Map an OS family key -> colour (for item accents).
export const familyColor = (f?: string): string =>
  (theme.families as Record<string, string>)[f ?? "other"] ?? theme.families.other;
