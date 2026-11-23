import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const VIOLET = theme.accents.violet;
const TEAL = theme.accents.magenta;
const AMBER = theme.accents.amber;

// A drawn "predict the next word" strip — the whole idea in one picture.
const Pill: React.FC<{ t: string; c: string }> = ({ t, c }) => (
  <span style={{ fontFamily: fontStack.mono, fontSize: 40, fontWeight: 700, color: c, border: `3px solid ${c}`, borderRadius: 10, padding: "8px 18px", background: "#0c0e13" }}>{t}</span>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 100% 0%, ${VIOLET}26, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 130, left: 90, width: 1740, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: VIOLET, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW <span style={{ color: VIOLET, textShadow: `0 0 50px ${VIOLET}` }}>LLMs</span> WORK
      </div>
    </div>
    <div style={{ position: "absolute", left: 90, top: 470, display: "flex", alignItems: "center", gap: 20, flexWrap: "wrap" }}>
      <Pill t="The" c={TEAL} />
      <Pill t="sky" c={TEAL} />
      <Pill t="is" c={TEAL} />
      <span style={{ fontFamily: fontStack.mono, fontSize: 48, color: theme.inkSoft }}>→</span>
      <Pill t="blue" c={AMBER} />
      <span style={{ fontFamily: fontStack.mono, fontSize: 30, color: theme.inkFaint }}>87%</span>
    </div>
    <div style={{ position: "absolute", left: 90, bottom: 90 }}>
      <div style={{ display: "inline-block", background: AMBER, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 44, padding: "12px 28px", borderRadius: 12, transform: "rotate(-2deg)", boxShadow: glow(AMBER, 0.6) }}>
        it just predicts the next word
      </div>
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1250, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        it doesn't <span style={{ color: theme.accents.coral, textShadow: `0 0 50px ${theme.accents.coral}` }}>think</span>
        <br />
        it <span style={{ color: VIOLET, textShadow: `0 0 50px ${VIOLET}` }}>predicts</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 38, fontWeight: 700, color: theme.inkSoft }}>tokens · attention · the Transformer</div>
    </div>
    <div style={{ position: "absolute", right: 120, bottom: 90, display: "flex", alignItems: "center", gap: 16 }}>
      <Pill t="river" c={TEAL} />
      <span style={{ fontFamily: fontStack.mono, fontSize: 40, color: AMBER }}>↘</span>
      <Pill t="bank" c={AMBER} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
