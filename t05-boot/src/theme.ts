// Design system for T05 "How an OS Works (the first second)" — a cinematic
// "ignition / telemetry" look: near-black with amber power, green ready, teal
// kernel, violet process. No flat blue/white. Accent KEY NAMES kept stable so
// shared components compile; values recoloured per boot phase.
export const theme = {
  bg: "#08080B",
  bgDeep: "#040406",
  ink: "#EDECE6",
  inkSoft: "#8E8E8A",
  inkFaint: "#55554F",
  line: "#21212A",
  paper: "#111117",
  paperHi: "#1A1A22",
  onAccent: "#08080B",

  // Accent palette — recoloured to boot-phase colours (keys reused).
  accents: {
    amber: "#FFB020", // firmware / power / POST
    coral: "#FF6B4A", // interrupt / warning
    mint: "#35FF9E", // kernel / ready / running
    violet: "#9B8CFF", // init / processes / user space
    magenta: "#2DD4BF", // bootloader (teal)
    gold: "#C9CDD4", // neutral / silver
  },

  // Boot-phase colours (the spine of this video).
  phases: {
    firmware: "#FFB020",
    bootloader: "#2DD4BF",
    kernel: "#35FF9E",
    init: "#9B8CFF",
    userspace: "#C9CDD4",
    running: "#35FF9E",
  },

  client: "#35FF9E",
  api: "#FFB020",
  server: "#9B8CFF",
  ok: "#35FF9E",
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

export const phaseColor = (p?: string): string =>
  (theme.phases as Record<string, string>)[p ?? "running"] ?? theme.phases.running;
