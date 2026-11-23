import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;

const GENS: { n: string; h: number; c: string }[] = [
  { n: "4", h: 0.22, c: "#FFB020" },
  { n: "5", h: 0.42, c: "#2DD4BF" },
  { n: "6", h: 0.7, c: MINT },
  { n: "6E", h: 0.74, c: "#B06BFF" },
  { n: "7", h: 1.0, c: GOLD },
];

const Ladder: React.FC<{ h?: number }> = ({ h = 440 }) => (
  <div style={{ display: "flex", alignItems: "flex-end", gap: 20, height: h }}>
    {GENS.map((g) => (
      <div key={g.n} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
        <div style={{ width: 86, height: g.h * h, background: `linear-gradient(${g.c}, ${g.c}55)`, border: `2px solid ${g.c}`, borderRadius: 10, boxShadow: glow(g.c, 0.45) }} />
        <span style={{ fontFamily: fontStack.sans, fontSize: 30, fontWeight: 900, color: g.c }}>Wi-Fi {g.n}</span>
      </div>
    ))}
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
    <div style={{ position: "absolute", top: 140, left: 90, width: 950, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 116, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />WI-FI<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>STANDARD</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        4 · 5 · 6 · 6E · 7
      </div>
    </div>
    <div style={{ position: "absolute", right: 130, top: 320 }}>
      <Ladder h={460} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1250, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        802.11n = <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>Wi-Fi 4?</span>
        <br />
        <span style={{ color: GOLD }}>decoded.</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>names · speeds · bands · the real numbers</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 50 }}>
      <Ladder h={400} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
