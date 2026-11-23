import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const LOVED = "#35E08A";
const HATED = "#FF5C47";
const MEH = "#FFB020";

// Version tiles tinted by history's verdict — our own flat marks (no MS flag).
const VERS: { n: string; c: string }[] = [
  { n: "95", c: LOVED },
  { n: "XP", c: LOVED },
  { n: "ME", c: HATED },
  { n: "Vista", c: HATED },
  { n: "7", c: LOVED },
  { n: "8", c: HATED },
  { n: "11", c: MEH },
];

const Tile: React.FC<{ n: string; c: string; size?: number }> = ({ n, c, size = 40 }) => (
  <div style={{ position: "relative", display: "flex", alignItems: "center", gap: size * 0.28, padding: `${size * 0.35}px ${size * 0.6}px`, background: theme.paper, border: `2px solid ${c}`, borderRadius: 12, boxShadow: glow(c, 0.4) }}>
    <span style={{ width: size * 0.42, height: size * 0.42, borderRadius: 999, background: c, boxShadow: `0 0 ${size * 0.5}px ${c}`, flex: "none" }} />
    <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: theme.ink }}>{n}</span>
  </div>
);

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${LOVED}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 118, left: 90, width: 1020, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: LOVED, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 126, lineHeight: 0.86, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />WINDOWS<br /><span style={{ color: LOVED, textShadow: `0 0 50px ${LOVED}` }}>RANKED</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: HATED, color: "#fff", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 24px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(HATED, 0.6) }}>
        …and Windows ME 💀
      </div>
    </div>
    <div style={{ position: "absolute", right: 90, top: 170, display: "flex", flexDirection: "column", gap: 16, alignItems: "flex-end", width: 540, justifyContent: "center", height: 780 }}>
      {VERS.map((v) => <Tile key={v.n} n={v.n} c={v.c} size={46} />)}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        was <span style={{ color: HATED, textShadow: `0 0 50px ${HATED}` }}>Windows ME</span>
        <br />
        really that bad?
      </div>
      <div style={{ display: "flex", gap: 16, marginTop: 34, flexWrap: "wrap" }}>
        {VERS.slice(0, 4).map((v) => <Tile key={v.n} n={v.n} c={v.c} size={34} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${LOVED}`, boxShadow: glow(LOVED, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
