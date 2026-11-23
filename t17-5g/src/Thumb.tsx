import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;
const SILVER = "#C9CDD4";

// A drawn cell tower with signal arcs — our own mark, no logos.
const Tower: React.FC<{ s?: number }> = ({ s = 300 }) => (
  <div style={{ position: "relative", width: s, height: s * 1.2 }}>
    {[1, 2, 3].map((i) => (
      <div key={i} style={{ position: "absolute", left: "50%", top: s * 0.1, width: i * s * 0.34, height: i * s * 0.34, transform: "translateX(-50%)", borderRadius: "50%", border: `${s * 0.02}px solid ${i < 2 ? MINT : i < 3 ? theme.accents.amber : CORAL}`, borderBottomColor: "transparent", borderLeftColor: "transparent", borderRightColor: "transparent", opacity: 0.8 - i * 0.14 }} />
    ))}
    <div style={{ position: "absolute", left: "50%", top: s * 0.1, width: s * 0.06, height: s, transform: "translateX(-50%)", background: SILVER, clipPath: "polygon(35% 0, 65% 0, 80% 100%, 20% 100%)" }} />
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
    <div style={{ position: "absolute", top: 140, left: 90, width: 1000 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>5G</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: CORAL, color: "#fff", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(CORAL, 0.6) }}>
        SLOWER THAN PROMISED
      </div>
    </div>
    <div style={{ position: "absolute", right: 200, top: 300 }}>
      <Tower s={420} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 170, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        promised <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>2 Gbps</span>
        <br />
        you get <span style={{ color: CORAL, textShadow: `0 0 50px ${CORAL}` }}>~200?</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>mmWave · mid-band · the 5G lie</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
