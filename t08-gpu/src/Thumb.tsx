import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const GREEN = "#76D64A";

// Our own GPU "tiles" — flat labels, no vendor logos.
const CHIPS: { n: string; c: string }[] = [
  { n: "RTX", c: GREEN },
  { n: "RX", c: "#FF5C47" },
  { n: "Arc", c: "#5AA9FF" },
  { n: "APU", c: "#FFB020" },
  { n: "NPU", c: "#B06BFF" },
  { n: "TPU", c: "#2DD4BF" },
];

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${GREEN}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

// Our own "chip tile" — a flat package rectangle with the name (no logos).
const Chip: React.FC<{ n: string; c: string; size?: number }> = ({ n, c, size = 60 }) => (
  <div style={{ position: "relative", padding: `${size * 0.4}px ${size * 0.7}px`, background: theme.paper, border: `2px solid ${c}`, borderRadius: 14, boxShadow: glow(c, 0.45) }}>
    <div style={{ position: "absolute", inset: 6, borderRadius: 8, border: `1px solid ${c}55` }} />
    <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: theme.ink }}>{n}</span>
  </div>
);

export const ThumbA: React.FC<VideoInput> = ({ images }) => {
  const hero = images?.hero || images?.nvidia || images?.amd;
  return (
    <AbsoluteFill>
      <Bg corner="tr" />
      <div style={{ position: "absolute", top: 120, left: 90, zIndex: 2 }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: GREEN, fontWeight: 700 }}>◢ EVERY X</div>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 168, lineHeight: 0.9, color: theme.ink, letterSpacing: -5, marginTop: 6 }}>
          EVERY<br /><span style={{ color: GREEN, textShadow: `0 0 50px ${GREEN}` }}>GPU</span>
        </div>
        <div style={{ display: "inline-block", marginTop: 24, background: "#FFB020", color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 44, padding: "12px 28px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow("#FFB020", 0.6) }}>
          WHICH DO YOU NEED?
        </div>
      </div>
      {hero ? (
        <div style={{ position: "absolute", right: 70, top: 150, width: 720, height: 780, borderRadius: 24, overflow: "hidden", border: `3px solid ${GREEN}`, boxShadow: glow(GREEN, 0.6) }}>
          <Img src={staticFile(hero.file)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "saturate(1.1) contrast(1.05)" }} />
          <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 100% at 60% 40%, transparent 40%, ${theme.bg}cc 100%)` }} />
          <div style={{ position: "absolute", left: 20, bottom: 20, display: "flex", gap: 12, flexWrap: "wrap", width: 360 }}>
            {CHIPS.map((s) => <Chip key={s.n} n={s.n} c={s.c} size={30} />)}
          </div>
        </div>
      ) : (
        <div style={{ position: "absolute", right: 110, top: 150, display: "flex", flexWrap: "wrap", gap: 22, width: 560, justifyContent: "flex-end", alignContent: "center", height: 780 }}>
          {CHIPS.map((s) => <Chip key={s.n} n={s.n} c={s.c} size={58} />)}
        </div>
      )}
    </AbsoluteFill>
  );
};

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 160, left: 90, width: 1180 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 128, lineHeight: 0.95, color: theme.ink, letterSpacing: -4 }}>
        RTX vs RX
        <br />
        vs <span style={{ color: "#5AA9FF", textShadow: `0 0 50px #5AA9FF` }}>Arc?</span>
      </div>
      <div style={{ display: "flex", gap: 18, marginTop: 36, flexWrap: "wrap" }}>
        {CHIPS.slice(0, 4).map((s) => <Chip key={s.n} n={s.n} c={s.c} size={42} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${GREEN}`, boxShadow: glow(GREEN, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
