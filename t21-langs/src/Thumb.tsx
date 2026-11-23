import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;

const CHIPS: { n: string; c: string }[] = [
  { n: "C", c: "#C9CDD4" },
  { n: "C++", c: "#FF5C47" },
  { n: "Python", c: MINT },
  { n: "Java", c: "#FFB020" },
  { n: "JS", c: GOLD },
  { n: "Go", c: "#2DD4BF" },
  { n: "Rust", c: "#FFB020" },
  { n: "Swift", c: "#FF5C47" },
  { n: "TS", c: "#B06BFF" },
  { n: "Ruby", c: "#FF5C47" },
];

const Chip: React.FC<{ n: string; c: string }> = ({ n, c }) => (
  <div style={{ fontFamily: fontStack.mono, fontSize: 40, fontWeight: 800, color: c, border: `3px solid ${c}`, borderRadius: 12, padding: "10px 22px", boxShadow: glow(c, 0.4) }}>{n}</div>
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
    <div style={{ position: "absolute", top: 110, left: 90, width: 1050, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 108, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />PROGRAMMING<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>LANGUAGE</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 20, background: GOLD, color: theme.onAccent, fontFamily: fontStack.mono, fontWeight: 900, fontSize: 34, padding: "10px 22px", borderRadius: 10, transform: "rotate(-2deg)", boxShadow: glow(GOLD, 0.5) }}>
        print("Hello, World!")
      </div>
    </div>
    <div style={{ position: "absolute", right: 70, top: 150, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 18, width: 640, justifyItems: "center" }}>
      {CHIPS.map((c) => <Chip key={c.n} {...c} />)}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 170, left: 90, width: 1200, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        which one should
        <br />
        <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>you learn</span> <span style={{ color: GOLD }}>first?</span>
      </div>
      <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>12 languages · what each is actually for</div>
    </div>
    <div style={{ position: "absolute", left: 90, bottom: 80, display: "flex", flexWrap: "wrap", gap: 18, width: 1740 }}>
      {CHIPS.map((c) => <Chip key={c.n} {...c} />)}
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
