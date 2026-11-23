import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const GREEN = theme.accents.mint;
const VIOLET = theme.accents.violet;
const TEAL = theme.accents.magenta;
const AMBER = theme.accents.amber;

const Bubble: React.FC<{ t: string; c: string; align?: "l" | "r" }> = ({ t, c, align = "l" }) => (
  <div style={{ alignSelf: align === "r" ? "flex-end" : "flex-start", maxWidth: 560, background: "#0c0e13", border: `3px solid ${c}`, borderRadius: align === "r" ? "16px 16px 4px 16px" : "16px 16px 16px 4px", padding: "16px 22px", fontFamily: fontStack.sans, fontSize: 32, fontWeight: 700, color: theme.ink, boxShadow: glow(c, 0.4) }}>{t}</div>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 0% 0%, ${GREEN}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 130, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: GREEN, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 120, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW<br /><span style={{ color: GREEN, textShadow: `0 0 50px ${GREEN}` }}>CHATGPT</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 20, background: AMBER, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, padding: "10px 24px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(AMBER, 0.5) }}>
        predictor → assistant
      </div>
    </div>
    <div style={{ position: "absolute", right: 90, top: 210, width: 640, display: "flex", flexDirection: "column", gap: 22 }}>
      <Bubble t="What is the capital of France?" c={TEAL} align="r" />
      <Bubble t="Paris. Want more about it?" c={GREEN} align="l" />
      <div style={{ alignSelf: "center", fontFamily: fontStack.mono, fontSize: 26, color: AMBER, border: `2px solid ${AMBER}`, borderRadius: 999, padding: "8px 18px" }}>★ trained on human feedback</div>
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1200, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        why it feels
        <br />
        so <span style={{ color: GREEN, textShadow: `0 0 50px ${GREEN}` }}>human</span>
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>RLHF · system prompt · tools</div>
    </div>
    <div style={{ position: "absolute", right: 110, bottom: 90, width: 600, display: "flex", flexDirection: "column", gap: 20 }}>
      <Bubble t="Fix this bug for me →" c={TEAL} align="r" />
      <Bubble t="Here's the fix, and why it broke." c={GREEN} align="l" />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
