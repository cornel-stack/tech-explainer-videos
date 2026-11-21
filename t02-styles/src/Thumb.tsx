import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const STYLES: { n: string; c: string }[] = [
  { n: "REST", c: theme.accents.amber },
  { n: "SOAP", c: theme.accents.violet },
  { n: "GraphQL", c: theme.accents.magenta },
  { n: "gRPC", c: theme.accents.mint },
  { n: "WebSocket", c: theme.accents.coral },
  { n: "SSE", c: theme.accents.gold },
  { n: "Webhook", c: theme.accents.amber },
  { n: "WebRTC", c: theme.accents.violet },
];

const ThumbBg: React.FC<{ accent: string; corner?: "tr" | "tl" }> = ({ accent, corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${accent}33, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.5 }} />
  </>
);

const Chip: React.FC<{ n: string; c: string; size?: number }> = ({ n, c, size = 46 }) => (
  <div
    style={{
      background: theme.paper,
      color: theme.ink,
      border: `2px solid ${c}`,
      borderRadius: 16,
      padding: "14px 24px",
      fontFamily: fontStack.sans,
      fontWeight: 800,
      fontSize: size,
      boxShadow: glow(c, 0.45),
      whiteSpace: "nowrap",
    }}
  >
    {n}
  </div>
);

// ── A — the authoritative list + "when to use each" ─────────────────────────
export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <ThumbBg accent={theme.accents.magenta} corner="tr" />
    <div style={{ position: "absolute", top: 110, left: 96 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: theme.accents.mint, fontWeight: 700 }}>EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 168, lineHeight: 0.9, color: theme.ink, letterSpacing: -6, marginTop: 4 }}>
        EVERY<br />
        <span style={{ color: theme.accents.magenta, textShadow: `0 0 50px ${theme.accents.magenta}` }}>API</span> STYLE
      </div>
      <div style={{ display: "inline-block", marginTop: 26, background: theme.accents.mint, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 44, padding: "12px 28px", borderRadius: 16, transform: "rotate(-3deg)", boxShadow: glow(theme.accents.mint, 0.6) }}>
        WHEN TO USE EACH
      </div>
    </div>
    {/* chips cluster, right */}
    <div style={{ position: "absolute", right: 80, top: 150, width: 760, display: "flex", flexWrap: "wrap", gap: 20, justifyContent: "flex-end", alignContent: "center", height: 780 }}>
      {STYLES.map((s) => <Chip key={s.n} n={s.n} c={s.c} size={52} />)}
    </div>
  </AbsoluteFill>
);

// ── B — curiosity: "you're picking the wrong one" ──────────────────────────
export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <ThumbBg accent={theme.accents.coral} corner="tl" />
    <div style={{ position: "absolute", top: 120, left: 96, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.92, color: theme.ink, letterSpacing: -5 }}>
        REST? GraphQL?
        <br />
        <span style={{ color: theme.accents.coral, textShadow: `0 0 50px ${theme.accents.coral}` }}>WHICH ONE?!</span>
      </div>
      <div style={{ display: "flex", gap: 16, marginTop: 34, flexWrap: "wrap" }}>
        {STYLES.slice(0, 5).map((s) => <Chip key={s.n} n={s.n} c={s.c} size={40} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 50 }}>
      <div style={{ position: "absolute", right: -20, top: -20, width: 520, height: 520, borderRadius: 999, border: `12px solid ${theme.accents.coral}`, boxShadow: glow(theme.accents.coral, 0.6) }} />
      <Peep seed={CAST.dev} size={470} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
