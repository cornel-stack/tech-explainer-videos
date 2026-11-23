import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const MINT = theme.accents.mint;
const GOLD = theme.accents.gold;
const AMBER = theme.accents.amber;
const VIOLET = theme.accents.violet;

const CMDS: { c: string; col: string }[] = [
  { c: "git init", col: MINT },
  { c: "git clone", col: MINT },
  { c: "git add", col: AMBER },
  { c: "git commit", col: AMBER },
  { c: "git push", col: GOLD },
  { c: "git pull", col: GOLD },
  { c: "git branch", col: VIOLET },
  { c: "git merge", col: VIOLET },
];

const Term: React.FC<{ w?: number }> = ({ w = 760 }) => (
  <div style={{ width: w, background: "#06080b", border: `2px solid ${MINT}66`, borderRadius: 14, overflow: "hidden", boxShadow: glow(MINT, 0.4) }}>
    <div style={{ display: "flex", gap: 8, padding: "12px 16px", background: "#0f1217" }}>
      {["#FF5C47", "#FFB020", "#35E08A"].map((c) => <span key={c} style={{ width: 14, height: 14, borderRadius: 999, background: c }} />)}
    </div>
    <div style={{ padding: "18px 24px", fontFamily: fontStack.mono, fontSize: 30, lineHeight: 1.5 }}>
      {CMDS.map((x) => (
        <div key={x.c}><span style={{ color: MINT }}>$</span> <span style={{ color: x.col, fontWeight: 700 }}>{x.c}</span></div>
      ))}
    </div>
  </div>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at 0% 0%, ${MINT}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1000, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        EVERY<br />GIT <span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>COMMAND</span>
      </div>
      <div style={{ display: "inline-block", marginTop: 22, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        the 12 you actually need
      </div>
    </div>
    <div style={{ position: "absolute", right: 90, top: 150 }}>
      <Term w={760} />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 180, left: 90, width: 1050, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 116, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        stop <span style={{ color: theme.accents.coral, textShadow: `0 0 50px ${theme.accents.coral}` }}>googling</span>
        <br />
        git commands
      </div>
      <div style={{ marginTop: 28, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>12 commands · 99% of your day</div>
    </div>
    <div style={{ position: "absolute", right: 90, bottom: 80 }}>
      <Term w={720} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
