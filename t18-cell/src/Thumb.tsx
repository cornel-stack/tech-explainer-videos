import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;

const GENS: { n: string; h: number; c: string }[] = [
  { n: "1G", h: 0.14, c: "#C9CDD4" },
  { n: "2G", h: 0.26, c: "#2DD4BF" },
  { n: "3G", h: 0.42, c: "#FFB020" },
  { n: "4G", h: 0.64, c: MINT },
  { n: "5G", h: 0.84, c: "#B06BFF" },
  { n: "6G", h: 1.0, c: GOLD },
];

// A drawn generation ladder — bars growing 1G→6G.
const Ladder: React.FC<{ h?: number }> = ({ h = 440 }) => (
  <div style={{ display: "flex", alignItems: "flex-end", gap: 16, height: h }}>
    {GENS.map((g) => (
      <div key={g.n} style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10 }}>
        <div style={{ width: 70, height: g.h * h, background: `linear-gradient(${g.c}, ${g.c}66)`, border: `2px solid ${g.c}`, borderRadius: 8, boxShadow: glow(g.c, 0.45) }} />
        <span style={{ fontFamily: fontStack.mono, fontSize: 28, fontWeight: 800, color: g.c }}>{g.n}</span>
      </div>
    ))}
  </div>
);

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${MINT}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 130, left: 90, width: 960, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />MOBILE<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>NETWORK</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 42, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        1G → 6G
      </div>
    </div>
    <div style={{ position: "absolute", right: 110, top: 360 }}>
      <Ladder h={440} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 110, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        2.4 kbps <span style={{ color: theme.inkSoft }}>→</span>
        <br />
        <span style={{ color: GOLD, textShadow: `0 0 50px ${GOLD}` }}>a terabit</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>a million× in 40 years · what each changed</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
