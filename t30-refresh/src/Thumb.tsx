import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const VIOLET = theme.accents.violet;
const GOLD = theme.accents.gold;
const MINT = theme.accents.mint;

const RATES: { n: string; h: number; c: string }[] = [
  { n: "60", h: 0.14, c: "#C9CDD4" },
  { n: "120", h: 0.3, c: "#2DD4BF" },
  { n: "144", h: 0.4, c: MINT },
  { n: "240", h: 0.62, c: "#FFB020" },
  { n: "360", h: 0.82, c: "#FF5C47" },
  { n: "540", h: 1.0, c: GOLD },
];

const Ladder: React.FC<{ h?: number }> = ({ h = 440 }) => (
  <div style={{ display: "flex", alignItems: "flex-end", gap: 18, height: h }}>
    {RATES.map((g) => (
      <div key={g.n} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
        <div style={{ width: 74, height: g.h * h, background: `linear-gradient(${g.c}, ${g.c}55)`, border: `2px solid ${g.c}`, borderRadius: 8, boxShadow: glow(g.c, 0.45) }} />
        <span style={{ fontFamily: fontStack.mono, fontSize: 24, fontWeight: 800, color: g.c }}>{g.n}</span>
      </div>
    ))}
  </div>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 100% 0%, ${VIOLET}24, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 130, left: 90, width: 980, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: VIOLET, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />REFRESH<br /><span style={{ color: VIOLET, textShadow: `0 0 50px ${VIOLET}` }}>RATE</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        60Hz → 540Hz
      </div>
    </div>
    <div style={{ position: "absolute", right: 120, top: 330 }}>
      <Ladder h={470} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1250, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        when do you
        <br />
        <span style={{ color: VIOLET, textShadow: `0 0 50px ${VIOLET}` }}>stop noticing?</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>…and the frame-rate catch nobody mentions</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 60 }}>
      <Ladder h={400} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
