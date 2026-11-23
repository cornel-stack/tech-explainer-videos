import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;
const VIOLET = theme.accents.violet;

// A drawn "body in silicon" grid — labelled part tiles with their body-analogy.
const PARTS: { n: string; a: string; c: string }[] = [
  { n: "CPU", a: "brain", c: MINT },
  { n: "RAM", a: "desk", c: MINT },
  { n: "GPU", a: "studio", c: VIOLET },
  { n: "SSD", a: "cabinet", c: GOLD },
  { n: "PSU", a: "heart", c: "#FF5C47" },
  { n: "FANS", a: "lungs", c: "#2DD4BF" },
];

const Tile: React.FC<{ n: string; a: string; c: string }> = ({ n, a, c }) => (
  <div style={{ width: 250, height: 150, background: "#0c0e12", border: `3px solid ${c}`, borderRadius: 14, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", gap: 6, boxShadow: glow(c, 0.5) }}>
    <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 56, color: theme.ink, letterSpacing: -1 }}>{n}</span>
    <span style={{ fontFamily: fontStack.mono, fontSize: 24, color: c, letterSpacing: 1 }}>= {a}</span>
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
    <div style={{ position: "absolute", top: 110, left: 90, width: 900, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />COMPUTER<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>PART</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        a body in silicon
      </div>
    </div>
    <div style={{ position: "absolute", right: 70, top: 150, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 22 }}>
      {PARTS.map((p) => <Tile key={p.n} {...p} />)}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1740 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        what does a <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>CPU</span>
        <br />
        actually <span style={{ color: GOLD, textShadow: `0 0 50px ${GOLD}` }}>do?</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>every part of a PC, in plain English</div>
    </div>
    <div style={{ position: "absolute", left: 90, bottom: 70, display: "flex", gap: 22 }}>
      {PARTS.slice(0, 5).map((p) => <Tile key={p.n} {...p} />)}
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
