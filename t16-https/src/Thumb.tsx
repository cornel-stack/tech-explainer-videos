import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;

// A flat drawn padlock — our own mark, no logos.
const Lock: React.FC<{ s?: number; c?: string }> = ({ s = 240, c = MINT }) => (
  <div style={{ position: "relative", width: s, height: s * 1.15 }}>
    <div style={{ position: "absolute", left: "50%", top: s * 0.02, width: s * 0.56, height: s * 0.5, transform: "translateX(-50%)", border: `${s * 0.09}px solid ${c}`, borderBottom: "none", borderRadius: `${s * 0.3}px ${s * 0.3}px 0 0`, boxShadow: glow(c, 0.4) }} />
    <div style={{ position: "absolute", left: "50%", bottom: 0, width: s * 0.86, height: s * 0.62, transform: "translateX(-50%)", background: `${c}1a`, border: `${s * 0.045}px solid ${c}`, borderRadius: s * 0.11, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", boxShadow: glow(c, 0.5) }}>
      <div style={{ width: s * 0.13, height: s * 0.13, borderRadius: 999, background: c }} />
      <div style={{ width: s * 0.07, height: s * 0.16, background: c, marginTop: -s * 0.01 }} />
    </div>
  </div>
);

const Bar: React.FC<{ domain: string; c: string; w?: number }> = ({ domain, c, w = 480 }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 14, width: w, background: theme.paper, border: `2px solid ${c}`, borderRadius: 12, padding: "12px 18px", boxShadow: glow(c, 0.35) }}>
    <span style={{ fontSize: 30, color: c }}>🔒</span>
    <span style={{ fontFamily: fontStack.mono, fontSize: 30, fontWeight: 800, color: theme.ink }}>{domain}</span>
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
    <div style={{ position: "absolute", top: 130, left: 90, width: 1000 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        WHAT THE<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>PADLOCK</span><br />PROVES
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: CORAL, color: "#fff", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(CORAL, 0.6) }}>
        (it's not "safe")
      </div>
    </div>
    <div style={{ position: "absolute", right: 200, top: 290 }}>
      <Lock s={420} c={MINT} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        both have a <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>🔒</span>
        <br />
        one is a <span style={{ color: CORAL, textShadow: `0 0 50px ${CORAL}` }}>scam</span>
      </div>
      <div style={{ display: "flex", flexDirection: "column", gap: 18, marginTop: 36 }}>
        <Bar domain="yourbank.com" c={MINT} />
        <Bar domain="your-bank-login.com" c={CORAL} />
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
