import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;
const GOLD = "#C9A64B";
const PCB = "#10281c";

// A little drawn RAM stick with chips and a gold pin edge + notch — our own mark.
const Stick: React.FC<{ w?: number; notch?: number; accent?: string }> = ({ w = 420, notch = 0.5, accent = MINT }) => (
  <div style={{ width: w, background: PCB, border: `2px solid ${accent}66`, borderRadius: 8, padding: "12px 10px 6px", boxShadow: "0 10px 26px #000a" }}>
    <div style={{ display: "flex", gap: 6, justifyContent: "center" }}>
      {Array.from({ length: 8 }).map((_, i) => (
        <div key={i} style={{ flex: 1, height: 44, background: "#16181e", border: "1px solid #333", borderRadius: 3 }} />
      ))}
    </div>
    <div style={{ position: "relative", height: 22, marginTop: 8, display: "flex", gap: 2, borderRadius: "0 0 4px 4px", overflow: "hidden" }}>
      {Array.from({ length: 60 }).map((_, i) => <div key={i} style={{ flex: 1, background: GOLD, opacity: 0.85 }} />)}
      <div style={{ position: "absolute", left: `calc(${notch * 100}% - 11px)`, bottom: 0, width: 22, height: 22, background: PCB }} />
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
    <div style={{ position: "absolute", top: 120, left: 90, width: 980, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 134, lineHeight: 0.88, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />TYPE OF <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>RAM</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 42, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        DDR1 → DDR5
      </div>
    </div>
    <div style={{ position: "absolute", right: 90, top: 300, display: "flex", flexDirection: "column", gap: 26, alignItems: "flex-end" }}>
      <Stick w={460} notch={0.38} accent={"#2DD4BF"} />
      <Stick w={460} notch={0.52} accent={MINT} />
      <div style={{ fontFamily: fontStack.mono, fontSize: 28, color: CORAL, fontWeight: 700 }}>↑ the notch moves every gen</div>
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1080 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 116, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        why won't my
        <br />
        <span style={{ color: CORAL, textShadow: `0 0 50px ${CORAL}` }}>RAM fit?</span>
      </div>
      <div style={{ marginTop: 28 }}>
        <Stick w={520} notch={0.5} accent={MINT} />
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
