import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const TEAL = theme.accents.magenta;
const GOLD = theme.accents.gold;
const CORAL = theme.accents.coral;
const METAL = "#C9CDD4";

// drawn connector silhouettes for the thumbnail
const Conn: React.FC<{ shape: string; label: string; c: string }> = ({ shape, label, c }) => {
  const box = (w: number, h: number, r: string) => (
    <div style={{ width: w, height: h, background: "#14171f", border: `4px solid ${METAL}`, borderRadius: r, display: "grid", placeItems: "center", boxShadow: glow(c, 0.4) }}>
      <div style={{ width: w - 28, height: h - 24, background: "#0a0c10", borderRadius: 4, display: "grid", placeItems: "center" }}>
        <div style={{ width: "66%", height: Math.min(14, h / 6), background: c, borderRadius: 3 }} />
      </div>
    </div>
  );
  const shapes: Record<string, React.ReactNode> = {
    usba: box(200, 86, "6px"),
    micro: box(150, 60, "6px 6px 16px 16px"),
    usbc: (
      <div style={{ width: 190, height: 80, background: "#14171f", border: `4px solid ${METAL}`, borderRadius: 999, display: "grid", placeItems: "center", boxShadow: glow(c, 0.5) }}>
        <div style={{ width: 130, height: 12, background: c, borderRadius: 999 }} />
      </div>
    ),
  };
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
      {shapes[shape]}
      <span style={{ fontFamily: fontStack.mono, fontSize: 24, fontWeight: 800, color: c }}>{label}</span>
    </div>
  );
};

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 100% 0%, ${TEAL}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 130, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: TEAL, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 130, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br /><span style={{ color: TEAL, textShadow: `0 0 50px ${TEAL}` }}>USB</span> TYPE
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        finally untangled
      </div>
    </div>
    <div style={{ position: "absolute", right: 120, top: 230, display: "flex", alignItems: "center", gap: 46 }}>
      <Conn shape="usba" label="USB-A" c={METAL} />
      <Conn shape="micro" label="Micro" c={CORAL} />
      <Conn shape="usbc" label="USB-C" c={TEAL} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1200, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        same plug.
        <br />
        <span style={{ color: CORAL, textShadow: `0 0 50px ${CORAL}` }}>wildly different</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>why USB-C is secretly a mess</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 110, display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
      <Conn shape="usbc" label="USB-C" c={TEAL} />
      <div style={{ fontFamily: fontStack.mono, fontSize: 30, color: GOLD }}>480 Mbps … or 40 Gbps?</div>
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
