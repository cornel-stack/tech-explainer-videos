import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";

const VIOLET = theme.accents.violet;
const GOLD = theme.accents.gold;

const STONES: { n: string; d: string; h: number }[] = [
  { n: "OS/2", d: "2006", h: 300 },
  { n: "BeOS", d: "2001", h: 360 },
  { n: "Symbian", d: "2012", h: 320 },
  { n: "webOS", d: "2012", h: 280 },
  { n: "Win\nPhone", d: "2017", h: 340 },
];

const Stone: React.FC<{ n: string; d: string; h: number }> = ({ n, d, h }) => (
  <div style={{ width: 200, height: h, background: "linear-gradient(180deg,#2a2d34,#1b1d22)", borderRadius: "100px 100px 10px 10px", border: "2px solid #33363d", boxShadow: "0 18px 40px #000c, inset 0 2px 0 #3a3d44", display: "flex", flexDirection: "column", alignItems: "center", paddingTop: 34 }}>
    <div style={{ fontFamily: fontStack.mono, fontSize: 18, letterSpacing: 5, color: theme.inkFaint }}>R·I·P</div>
    <div style={{ marginTop: 10, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34, color: theme.ink, textAlign: "center", lineHeight: 0.95, whiteSpace: "pre-line" }}>{n}</div>
    <div style={{ marginTop: 8, fontFamily: fontStack.mono, fontSize: 20, color: VIOLET }}>† {d}</div>
  </div>
);

const Bg: React.FC = () => (
  <>
    <AbsoluteFill style={{ background: "linear-gradient(180deg,#07090b,#0b0f0c)" }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 800px at 50% -10%, ${VIOLET}22, transparent 60%)` }} />
    <AbsoluteFill style={{ top: "auto", bottom: 0, height: 180, background: "#0c140e", borderTop: `1px solid ${VIOLET}33` }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 70, left: 0, right: 0, textAlign: "center", zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 32, letterSpacing: 8, color: VIOLET, fontWeight: 700 }}>◢ EVERY X</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 112, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 4, textShadow: `0 0 50px ${VIOLET}aa` }}>
        EVERY <span style={{ color: VIOLET }}>DEAD</span> OS
      </div>
      <div style={{ display: "inline-block", marginTop: 18, background: GOLD, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38, padding: "10px 24px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(GOLD, 0.5) }}>
        why they died
      </div>
    </div>
    <div style={{ position: "absolute", left: 0, right: 0, bottom: 70, display: "flex", justifyContent: "center", alignItems: "flex-end", gap: 26 }}>
      {STONES.map((s) => <Stone key={s.n} {...s} />)}
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1050, zIndex: 2 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 104, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        some were <span style={{ color: GOLD, textShadow: `0 0 50px ${GOLD}` }}>better</span>
        <br />
        than what <span style={{ color: VIOLET, textShadow: `0 0 50px ${VIOLET}` }}>killed them</span>
      </div>
      <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 36, fontWeight: 700, color: theme.inkSoft }}>10 operating systems · gone but not forgotten</div>
    </div>
    <div style={{ position: "absolute", right: 90, bottom: 70, display: "flex", alignItems: "flex-end", gap: 24 }}>
      <Stone n={"BeOS"} d={"2001"} h={360} />
      <Stone n={"Win\nPhone"} d={"2017"} h={300} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
