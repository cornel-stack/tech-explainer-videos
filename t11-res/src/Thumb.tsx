import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;
const CORAL = theme.accents.coral;
const VIOLET = theme.accents.violet;

// Nested resolution rectangles (drawn to rough relative scale) — our own marks.
const TIERS: { n: string; w: number; h: number; c: string }[] = [
  { n: "720p", w: 1280, h: 720, c: CORAL },
  { n: "1080p", w: 1920, h: 1080, c: MINT },
  { n: "1440p", w: 2560, h: 1440, c: MINT },
  { n: "4K", w: 3840, h: 2160, c: VIOLET },
  { n: "8K", w: 7680, h: 4320, c: GOLD },
];

const Nested: React.FC<{ scale?: number }> = ({ scale = 0.1 }) => (
  <div style={{ position: "relative", width: 7680 * scale, height: 4320 * scale }}>
    {TIERS.map((t) => (
      <div key={t.n} style={{ position: "absolute", left: 0, bottom: 0, width: t.w * scale, height: t.h * scale, border: `3px solid ${t.c}`, borderRadius: 6, background: `${t.c}14`, boxShadow: glow(t.c, 0.3) }}>
        <span style={{ position: "absolute", left: 8, top: 6, fontFamily: fontStack.mono, fontSize: 22, fontWeight: 800, color: t.c }}>{t.n}</span>
      </div>
    ))}
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
    <div style={{ position: "absolute", top: 120, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 130, lineHeight: 0.88, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>RESOLUTION</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 42, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.6) }}>
        IS 8K A LIE?
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, top: 300 }}>
      <Nested scale={0.1} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 122, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        4K vs <span style={{ color: GOLD, textShadow: `0 0 50px ${GOLD}` }}>8K</span>
        <br />
        can you tell?
      </div>
      <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>where your eyes give up</div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
