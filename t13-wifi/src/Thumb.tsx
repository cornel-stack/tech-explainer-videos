import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;
const AMBER = theme.accents.amber;

// A compact top-down house: a router with signal rings fading green→amber→red, and
// a bedroom in the dead zone — our own drawn mark, no logos.
const MiniHouse: React.FC = () => (
  <div style={{ position: "relative", width: 480, height: 360, border: `3px solid ${theme.line}`, borderRadius: 10, background: "#0b0d10", overflow: "hidden" }}>
    {/* rooms */}
    <div style={{ position: "absolute", left: "50%", top: 0, bottom: 0, width: 3, background: theme.line }} />
    <div style={{ position: "absolute", left: 0, right: 0, top: "50%", height: 3, background: theme.line }} />
    {/* signal rings from router (top-left room) */}
    {[1, 2, 3, 4].map((i) => (
      <div key={i} style={{ position: "absolute", left: 120, top: 100, width: i * 150, height: i * 150, transform: "translate(-50%,-50%)", borderRadius: 999, border: `3px solid ${i < 2 ? MINT : i < 3 ? AMBER : CORAL}`, opacity: 0.8 - i * 0.14 }} />
    ))}
    {/* router */}
    <div style={{ position: "absolute", left: 120, top: 100, width: 44, height: 30, transform: "translate(-50%,-50%)", background: theme.paper, border: `2px solid ${MINT}`, borderRadius: 6, boxShadow: glow(MINT, 0.5) }} />
    <span style={{ position: "absolute", left: 40, top: 20, fontFamily: fontStack.mono, fontSize: 15, color: MINT }}>router</span>
    {/* bedroom dead zone (bottom-right) */}
    <div style={{ position: "absolute", right: 16, bottom: 16, width: 200, height: 140, background: `${CORAL}18`, border: `2px dashed ${CORAL}`, borderRadius: 8, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
      <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 28, color: CORAL }}>BEDROOM</span>
      <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: CORAL }}>▂▁ 2 bars</span>
    </div>
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
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 132, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>WI-FI</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: CORAL, color: "#fff", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(CORAL, 0.6) }}>
        WHY THE BEDROOM DIES
      </div>
    </div>
    <div style={{ position: "absolute", right: 90, top: 330, transform: "scale(1.1)" }}>
      <MiniHouse />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1080 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 120, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        full bars.
        <br />
        <span style={{ color: CORAL, textShadow: `0 0 50px ${CORAL}` }}>still slow?</span>
      </div>
      <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>2.4 vs 5 vs 6 GHz · walls · dead zones</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
