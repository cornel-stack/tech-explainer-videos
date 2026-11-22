import React from "react";
import { AbsoluteFill, Img, staticFile } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const RED = "#FF5C47";
const AMBER = "#FFB020";
const GREEN = "#35E08A";

// OS tiles, each tinted by its legal status (red/amber/green) — our own flat marks.
const OSES: { n: string; c: string }[] = [
  { n: "Red Star", c: GREEN },
  { n: "Kali", c: AMBER },
  { n: "Tails", c: AMBER },
  { n: "Whonix", c: AMBER },
  { n: "Phantom", c: RED },
  { n: "Astra", c: GREEN },
];

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${RED}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

// An OS tile — a flat panel with the name and a legal-status dot.
const OSChip: React.FC<{ n: string; c: string; size?: number }> = ({ n, c, size = 40 }) => (
  <div style={{ position: "relative", display: "flex", alignItems: "center", gap: size * 0.3, padding: `${size * 0.35}px ${size * 0.6}px`, background: theme.paper, border: `2px solid ${c}`, borderRadius: 12, boxShadow: glow(c, 0.4) }}>
    <span style={{ width: size * 0.45, height: size * 0.45, borderRadius: 999, background: c, boxShadow: `0 0 ${size * 0.5}px ${c}`, flex: "none" }} />
    <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: theme.ink }}>{n}</span>
  </div>
);

export const ThumbA: React.FC<VideoInput> = ({ images }) => {
  const hero = images?.kali || images?.redstar || images?.tails || images?.templeos;
  return (
    <AbsoluteFill>
      <Bg corner="tr" />
      <div style={{ position: "absolute", top: 108, left: 90, zIndex: 2, width: 1040 }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: RED, fontWeight: 700 }}>◢ EVERY X</div>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.88, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
          EVERY <span style={{ color: RED, textShadow: `0 0 50px ${RED}` }}>ILLEGAL</span><br />OPERATING<br />SYSTEM
        </div>
        <div style={{ display: "flex", gap: 14, marginTop: 26 }}>
          <span style={{ background: RED, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, padding: "10px 20px", borderRadius: 10, transform: "rotate(-3deg)", boxShadow: glow(RED, 0.6) }}>ARRESTED?</span>
          <span style={{ background: GREEN, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, padding: "10px 20px", borderRadius: 10, transform: "rotate(2deg)", boxShadow: glow(GREEN, 0.6) }}>OR FINE?</span>
        </div>
      </div>
      {hero ? (
        <div style={{ position: "absolute", right: 70, top: 150, width: 680, height: 780, borderRadius: 24, overflow: "hidden", border: `3px solid ${RED}`, boxShadow: glow(RED, 0.6) }}>
          <Img src={staticFile(hero.file)} style={{ width: "100%", height: "100%", objectFit: "cover", filter: "saturate(1.08) contrast(1.05)" }} />
          <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 100% at 60% 40%, transparent 35%, ${theme.bg}dd 100%)` }} />
          <div style={{ position: "absolute", left: 18, bottom: 18, display: "flex", gap: 10, flexWrap: "wrap", width: 320 }}>
            {OSES.map((s) => <OSChip key={s.n} n={s.n} c={s.c} size={22} />)}
          </div>
        </div>
      ) : (
        <div style={{ position: "absolute", right: 90, top: 150, display: "flex", flexDirection: "column", gap: 20, width: 600, alignItems: "flex-end", justifyContent: "center", height: 780 }}>
          {OSES.map((s) => <OSChip key={s.n} n={s.n} c={s.c} size={46} />)}
        </div>
      )}
    </AbsoluteFill>
  );
};

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1180 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.95, color: theme.ink, letterSpacing: -4 }}>
        is <span style={{ color: AMBER, textShadow: `0 0 50px ${AMBER}` }}>Kali Linux</span>
        <br />
        illegal?
      </div>
      <div style={{ display: "flex", gap: 16, marginTop: 36, flexWrap: "wrap" }}>
        {OSES.slice(0, 4).map((s) => <OSChip key={s.n} n={s.n} c={s.c} size={34} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${RED}`, boxShadow: glow(RED, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
