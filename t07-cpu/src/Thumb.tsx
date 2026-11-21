import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const CHIPS: { n: string; c: string }[] = [
  { n: "i3", c: theme.tiers.i3 },
  { n: "i5", c: theme.tiers.i5 },
  { n: "i7", c: theme.tiers.i7 },
  { n: "i9", c: theme.tiers.i9 },
  { n: "Ultra", c: theme.tiers.ultra },
  { n: "Xeon", c: theme.tiers.xeon },
];

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${theme.accents.amber}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

// Our own "chip tile" — a flat package rectangle with the tier name (no logos).
const Chip: React.FC<{ n: string; c: string; size?: number }> = ({ n, c, size = 60 }) => (
  <div style={{ position: "relative", padding: `${size * 0.4}px ${size * 0.7}px`, background: theme.paper, border: `2px solid ${c}`, borderRadius: 14, boxShadow: glow(c, 0.45) }}>
    <div style={{ position: "absolute", inset: 6, borderRadius: 8, border: `1px solid ${c}55` }} />
    <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: theme.ink }}>{n}</span>
  </div>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 120, left: 90 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: theme.accents.amber, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 132, lineHeight: 0.9, color: theme.ink, letterSpacing: -5, marginTop: 6 }}>
        EVERY<br /><span style={{ color: theme.accents.amber, textShadow: `0 0 50px ${theme.accents.amber}` }}>INTEL</span> CPU
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: theme.accents.mint, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 44, padding: "12px 28px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(theme.accents.mint, 0.6) }}>
        WHICH DO YOU NEED?
      </div>
    </div>
    <div style={{ position: "absolute", right: 110, top: 150, display: "flex", flexWrap: "wrap", gap: 22, width: 560, justifyContent: "flex-end", alignContent: "center", height: 780 }}>
      {CHIPS.map((s) => <Chip key={s.n} n={s.n} c={s.c} size={58} />)}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.95, color: theme.ink, letterSpacing: -4 }}>
        i3 vs i5 vs
        <br />
        i7 vs <span style={{ color: theme.accents.coral, textShadow: `0 0 50px ${theme.accents.coral}` }}>i9?</span>
      </div>
      <div style={{ display: "flex", gap: 18, marginTop: 36, flexWrap: "wrap" }}>
        {CHIPS.slice(0, 4).map((s) => <Chip key={s.n} n={s.n} c={s.c} size={42} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${theme.accents.amber}`, boxShadow: glow(theme.accents.amber, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
