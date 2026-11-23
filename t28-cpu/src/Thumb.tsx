import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const AMBER = theme.accents.amber;
const TEAL = theme.accents.magenta;
const METAL = "#C9CDD4";

// A drawn CPU chip — core grid in a metal frame with gold pins.
const Chip: React.FC<{ s?: number }> = ({ s = 420 }) => (
  <div style={{ position: "relative", width: s, height: s }}>
    {/* pins */}
    {[0, 1, 2, 3].map((side) =>
      Array.from({ length: 10 }).map((_, i) => {
        const pos = (i + 0.5) * (s / 10);
        const st: React.CSSProperties = { position: "absolute", width: 10, height: 20, background: "#C9A64B", borderRadius: 2 };
        if (side === 0) return <div key={`t${i}`} style={{ ...st, left: pos, top: -18 }} />;
        if (side === 1) return <div key={`b${i}`} style={{ ...st, left: pos, bottom: -18 }} />;
        if (side === 2) return <div key={`l${i}`} style={{ ...st, top: pos, left: -18, width: 20, height: 10 }} />;
        return <div key={`r${i}`} style={{ ...st, top: pos, right: -18, width: 20, height: 10 }} />;
      })
    )}
    <div style={{ width: s, height: s, background: "#0c0f13", border: `6px solid ${METAL}`, borderRadius: 18, padding: 22, display: "grid", gridTemplateColumns: "repeat(5,1fr)", gridTemplateRows: "repeat(5,1fr)", gap: 10, boxShadow: glow(MINT, 0.5) }}>
      {Array.from({ length: 25 }).map((_, i) => (
        <div key={i} style={{ background: i % 7 === 0 ? TEAL : MINT, opacity: 0.25 + ((i * 37) % 10) / 13, borderRadius: 4 }} />
      ))}
    </div>
    <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 30, fontWeight: 900, color: "#fff", letterSpacing: 4, textShadow: "0 0 20px #000" }}>CPU</div>
    </div>
  </div>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 100% 0%, ${MINT}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW A<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>CPU</span> WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: AMBER, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(AMBER, 0.5) }}>
        just switches + a loop
      </div>
    </div>
    <div style={{ position: "absolute", right: 200, top: 320 }}>
      <Chip s={440} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 190, left: 90, width: 1150, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        <span style={{ color: AMBER, textShadow: `0 0 50px ${AMBER}` }}>3 billion</span>
        <br />
        switches a second
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>fetch · decode · execute</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 70 }}>
      <Chip s={380} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
