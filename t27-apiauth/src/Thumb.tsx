import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const AMBER = theme.accents.amber;
const MINT = theme.accents.mint;
const CORAL = theme.accents.coral;
const VIOLET = theme.accents.violet;

const LADDER: { n: string; c: string }[] = [
  { n: "No Auth", c: CORAL },
  { n: "API Key", c: CORAL },
  { n: "Bearer", c: AMBER },
  { n: "JWT", c: theme.accents.magenta },
  { n: "OAuth 2.0", c: VIOLET },
  { n: "HMAC", c: MINT },
  { n: "mTLS", c: MINT },
];

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 100% 0%, ${AMBER}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 120, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: AMBER, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 104, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY API<br /><span style={{ color: AMBER, textShadow: `0 0 50px ${AMBER}` }}>AUTH</span> METHOD
      </div>
      <div style={{ marginTop: 24, fontFamily: fontStack.mono, fontSize: 30, color: theme.inkSoft, background: "#0c0e13", border: `2px solid ${AMBER}66`, borderRadius: 10, padding: "12px 18px", display: "inline-block" }}>
        Authorization: <span style={{ color: AMBER }}>Bearer •••</span>
      </div>
    </div>
    <div style={{ position: "absolute", right: 110, top: 120, bottom: 120, display: "flex", flexDirection: "column-reverse", justifyContent: "space-between" }}>
      {LADDER.map((r, i) => (
        <div key={r.n} style={{ fontFamily: fontStack.mono, fontSize: 30, fontWeight: 800, color: r.c, border: `3px solid ${r.c}`, borderRadius: 10, padding: "8px 18px", marginLeft: i * 26, background: "#0c0e13", boxShadow: glow(r.c, 0.35) }}>{r.n}</div>
      ))}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1250, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 116, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        API keys to
        <br />
        <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>mutual TLS</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>OAuth · JWT · HMAC · and which to use</div>
    </div>
    <div style={{ position: "absolute", right: 120, bottom: 90, display: "flex", gap: 20 }}>
      {["🔓", "🔑", "🪙", "🛡"].map((_, i) => (
        <div key={i} style={{ width: 90, height: 90, borderRadius: 16, border: `3px solid ${[CORAL, AMBER, VIOLET, MINT][i]}`, background: "#0c0e13", display: "grid", placeItems: "center", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, color: [CORAL, AMBER, VIOLET, MINT][i], boxShadow: glow([CORAL, AMBER, VIOLET, MINT][i], 0.4) }}>{["0", "1", "2", "3"][i]}</div>
      ))}
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
