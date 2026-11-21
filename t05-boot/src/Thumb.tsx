import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const CHAIN = [
  { n: "FIRMWARE", c: theme.phases.firmware },
  { n: "BOOTLOADER", c: theme.phases.bootloader },
  { n: "KERNEL", c: theme.phases.kernel },
  { n: "PID 1", c: theme.phases.init },
  { n: "USER SPACE", c: theme.phases.userspace },
];

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${theme.accents.amber}26, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

const Chain: React.FC<{ scale?: number }> = ({ scale = 1 }) => (
  <div style={{ display: "flex", alignItems: "center", gap: 10 * scale, flexWrap: "wrap" }}>
    {CHAIN.map((s, i) => (
      <React.Fragment key={s.n}>
        <div style={{ background: theme.paper, border: `2px solid ${s.c}`, borderRadius: 10, padding: `${10 * scale}px ${18 * scale}px`, fontFamily: fontStack.mono, fontWeight: 700, fontSize: 30 * scale, color: theme.ink, boxShadow: glow(s.c, 0.4) }}>{s.n}</div>
        {i < CHAIN.length - 1 ? <span style={{ color: s.c, fontSize: 30 * scale }}>→</span> : null}
      </React.Fragment>
    ))}
  </div>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 120, left: 90 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: theme.accents.amber, fontWeight: 700 }}>⏻ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -5, marginTop: 6 }}>
        THE FIRST<br /><span style={{ color: theme.accents.amber, textShadow: `0 0 50px ${theme.accents.amber}` }}>SECOND</span>
      </div>
      <div style={{ fontFamily: fontStack.sans, fontSize: 44, fontWeight: 800, color: theme.inkSoft, marginTop: 8 }}>after you press power</div>
    </div>
    <div style={{ position: "absolute", right: 80, top: 220, fontFamily: fontStack.mono, fontSize: 150, fontWeight: 700, color: theme.accents.mint, textShadow: `0 0 50px ${theme.accents.mint}` }}>1000<span style={{ fontSize: 70 }}>ms</span></div>
    <div style={{ position: "absolute", bottom: 120, left: 90, right: 90, display: "flex", justifyContent: "center" }}>
      <Chain scale={1.2} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 140, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        WHAT HAPPENS
        <br />
        WHEN YOU PRESS
        <br />
        <span style={{ color: theme.accents.amber, textShadow: `0 0 50px ${theme.accents.amber}` }}>POWER?</span>
      </div>
      <div style={{ marginTop: 40 }}>
        <Chain scale={0.9} />
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${theme.accents.amber}`, boxShadow: glow(theme.accents.amber, 0.5) }} />
      <Peep seed={CAST.you} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
