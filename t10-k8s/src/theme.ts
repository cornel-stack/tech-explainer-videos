// Design system for T10 "How Kubernetes Works" — a dark "architecture blueprint"
// look: near-black with a mint-green spine, violet control plane, teal pods, amber
// workers, coral failures. No flat blue/white, NO vendor logos (no Kubernetes
// wheel). Accent KEY NAMES kept stable so shared components compile.
export const theme = {
  bg: "#07090A",
  bgDeep: "#030405",
  ink: "#E9EAE6",
  inkSoft: "#8A8C88",
  inkFaint: "#55564F",
  line: "#1F2328",
  paper: "#101317",
  paperHi: "#171B20",
  onAccent: "#07090A",

  // Accent palette (keys reused; recoloured for GPU compute).
  accents: {
    amber: "#FFB020", // power / heat / VRM
    coral: "#FF6B4A", // CPU / sequential contrast
    mint: "#39FF88", // compute green — cores / parallel / primary
    violet: "#B06BFF", // tensor cores / AI
    magenta: "#2DD4BF", // teal
    gold: "#C6FF4D", // lime
  },

  client: "#39FF88",
  api: "#FFB020",
  server: "#B06BFF",
  ok: "#39FF88",
  warn: "#FFB020",
  err: "#FF6B4A",

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
