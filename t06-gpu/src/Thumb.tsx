import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

// Static core grid (no logos) — the parallel-compute motif.
const CoreGrid: React.FC<{ cols: number; rows: number; accent: string; cell?: number }> = ({ cols, rows, accent, cell = 26 }) => {
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++)
    for (let c = 0; c < cols; c++) {
      const b = Math.max(0.12, Math.sin((c + r) * 0.5) * 0.5 + 0.5);
      cells.push(<div key={`${r}-${c}`} style={{ width: cell, height: cell, background: accent, opacity: b, borderRadius: 4 }} />);
    }
  return <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, ${cell}px)`, gap: 8 }}>{cells}</div>;
};

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${theme.accents.mint}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 120, left: 90 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: theme.accents.mint, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 150, lineHeight: 0.9, color: theme.ink, letterSpacing: -5, marginTop: 6 }}>
        HOW A<br /><span style={{ color: theme.accents.mint, textShadow: `0 0 50px ${theme.accents.mint}` }}>GPU</span> WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: theme.accents.violet, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 44, padding: "12px 28px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(theme.accents.violet, 0.6) }}>
        & WHY AI NEEDS IT
      </div>
    </div>
    <div style={{ position: "absolute", right: 110, top: 220, display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
      <CoreGrid cols={12} rows={12} accent={theme.accents.mint} cell={34} />
      <div style={{ fontFamily: fontStack.mono, fontSize: 40, fontWeight: 700, color: theme.ink }}>10,000+ CORES</div>
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 130, left: 90, width: 1120 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 126, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        WHY AI
        <br />
        RUNS ON
        <br />
        <span style={{ color: theme.accents.mint, textShadow: `0 0 50px ${theme.accents.mint}` }}>THIS</span>
      </div>
      <div style={{ display: "flex", alignItems: "center", gap: 28, marginTop: 36 }}>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
          <CoreGrid cols={2} rows={2} accent={theme.accents.coral} cell={34} />
          <span style={{ fontFamily: fontStack.mono, fontSize: 22, color: theme.accents.coral }}>CPU</span>
        </div>
        <span style={{ fontFamily: fontStack.sans, fontSize: 46, fontWeight: 900, color: theme.inkSoft }}>vs</span>
        <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 8 }}>
          <CoreGrid cols={9} rows={4} accent={theme.accents.mint} cell={22} />
          <span style={{ fontFamily: fontStack.mono, fontSize: 22, color: theme.accents.mint }}>GPU</span>
        </div>
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${theme.accents.mint}`, boxShadow: glow(theme.accents.mint, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
