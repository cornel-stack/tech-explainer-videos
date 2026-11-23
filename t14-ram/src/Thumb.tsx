import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;
const SILVER = "#C9CDD4";

// A drawn performance-vs-RAM curve: a coral cliff (too little → swap) rising to a
// flat green plateau (enough), then flat silver (more = wasted). Our own mark.
const Curve: React.FC = () => (
  <div style={{ position: "relative", width: 520, height: 360, border: `3px solid ${theme.line}`, borderRadius: 12, background: "#0b0d10", padding: 20 }}>
    <svg viewBox="0 0 480 300" width="100%" height="100%">
      {/* axes */}
      <line x1={30} y1={270} x2={470} y2={270} stroke={theme.inkFaint} strokeWidth={2} />
      <line x1={30} y1={20} x2={30} y2={270} stroke={theme.inkFaint} strokeWidth={2} />
      {/* cliff (coral) up to the enough point, then flat plateau (mint), then flat (silver) */}
      <path d="M40 255 L120 250 L180 70 L300 55" fill="none" stroke={CORAL} strokeWidth={6} strokeLinecap="round" />
      <path d="M300 55 L470 55" fill="none" stroke={MINT} strokeWidth={6} strokeLinecap="round" strokeDasharray="2 0" />
      {/* 'enough' marker */}
      <line x1={300} y1={55} x2={300} y2={270} stroke={MINT} strokeWidth={2} strokeDasharray="5 6" />
      <circle cx={300} cy={55} r={9} fill={MINT} />
    </svg>
    <span style={{ position: "absolute", left: 90, top: 40, fontFamily: fontStack.mono, fontSize: 17, color: CORAL }}>too little →</span>
    <span style={{ position: "absolute", left: 90, top: 60, fontFamily: fontStack.mono, fontSize: 17, color: CORAL }}>swap cliff</span>
    <span style={{ position: "absolute", right: 24, top: 44, fontFamily: fontStack.mono, fontSize: 17, color: SILVER }}>more = wasted</span>
    <span style={{ position: "absolute", left: 18, bottom: 6, fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>RAM installed →</span>
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
    <div style={{ position: "absolute", top: 130, left: 90, width: 980 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>RAM</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: CORAL, color: "#fff", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(CORAL, 0.6) }}>
        MORE ISN'T FASTER
      </div>
    </div>
    <div style={{ position: "absolute", right: 110, top: 340 }}>
      <Curve />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 170, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        16GB vs <span style={{ color: SILVER, textShadow: `0 0 50px ${SILVER}` }}>32GB</span>
        <br />
        does it matter?
      </div>
      <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>RAM is desk space, not horsepower</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
