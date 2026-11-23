import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const AMBER = theme.accents.amber;
const VIOLET = theme.accents.violet;
const TEAL = theme.accents.magenta;

// A drawn Git object graph — commit boxes chained with parent arrows + a branch pointer.
const Node: React.FC<{ label: string; hash: string; c: string; size?: number }> = ({ label, hash, c, size = 150 }) => (
  <div style={{ width: size, height: size, background: "#0c0e13", border: `3px solid ${c}`, borderRadius: 14, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center", gap: 6, boxShadow: glow(c, 0.5) }}>
    <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 24, color: theme.ink, letterSpacing: 1 }}>{label}</span>
    <span style={{ fontFamily: fontStack.mono, fontSize: 22, color: c }}>{hash}</span>
  </div>
);

const Arrow: React.FC = () => (
  <div style={{ width: 64, height: 4, background: theme.inkSoft, position: "relative", alignSelf: "center" }}>
    <span style={{ position: "absolute", right: -2, top: -8, width: 0, height: 0, borderTop: "10px solid transparent", borderBottom: "10px solid transparent", borderLeft: `14px solid ${theme.inkSoft}` }} />
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
    <div style={{ position: "absolute", top: 130, left: 90, width: 1050 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 142, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>GIT</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: AMBER, color: theme.onAccent, fontFamily: fontStack.mono, fontWeight: 900, fontSize: 38, padding: "12px 24px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(AMBER, 0.6) }}>
        just hashes & pointers
      </div>
    </div>
    <div style={{ position: "absolute", right: 70, top: 330, display: "flex", alignItems: "center" }}>
      <Node label="blob" hash="a1b3f9" c={VIOLET} />
      <Arrow />
      <Node label="tree" hash="7c2e04" c={TEAL} />
      <Arrow />
      <Node label="commit" hash="e9f1a2" c={AMBER} size={166} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1200 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 120, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        a branch is
        <br />
        just a <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>pointer</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>41 bytes · blobs · trees · commits</div>
    </div>
    <div style={{ position: "absolute", right: 120, bottom: 90, display: "flex", alignItems: "center" }}>
      <Node label="C1" hash="a1b3f9" c={MINT} />
      <Arrow />
      <Node label="C2" hash="7c2e04" c={MINT} />
      <div style={{ marginLeft: 26, padding: "10px 20px", background: MINT, color: theme.onAccent, fontFamily: fontStack.mono, fontWeight: 900, fontSize: 30, borderRadius: 10, boxShadow: glow(MINT, 0.6) }}>main →</div>
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
