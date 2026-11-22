import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The recurring GPU motif: a dense grid of tiny "cores" that light up in parallel
// waves — the visual shorthand for thousands of workers computing at once. Used
// as the native panel for stages without a dedicated Manim clip.
export const ParallelGrid: React.FC<{ accent: string; width?: number; height?: number; label?: string }> = ({
  accent,
  width = 1030,
  height = 505,
  label = "10,000+ CORES · IN PARALLEL",
}) => {
  const frame = useCurrentFrame();
  const cols = 30;
  const rows = 15;
  const cells: React.ReactNode[] = [];
  for (let r = 0; r < rows; r++) {
    for (let c = 0; c < cols; c++) {
      // diagonal wave + per-cell twinkle
      const wave = Math.sin((c + r) * 0.45 - frame * 0.16);
      const tw = Math.sin((c * 7 + r * 13) * 1.1 + frame * 0.2);
      const b = Math.max(0.06, (wave * 0.5 + 0.5) * 0.7 + tw * 0.15);
      cells.push(
        <div key={`${r}-${c}`} style={{ background: accent, opacity: b, borderRadius: 3 }} />,
      );
    }
  }
  return (
    <div style={{ position: "relative", width, height, background: "#090B0D", borderRadius: 14, border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.22), padding: 26, overflow: "hidden" }}>
      <div style={{ display: "grid", gridTemplateColumns: `repeat(${cols}, 1fr)`, gridAutoRows: "1fr", gap: 8, width: "100%", height: "100%" }}>
        {cells}
      </div>
      <div style={{ position: "absolute", left: 24, bottom: 16, fontFamily: fontStack.mono, fontSize: 18, color: theme.ink, letterSpacing: 2, background: "#090B0Dcc", padding: "4px 10px", borderRadius: 6 }}>
        ◉ {label}
      </div>
    </div>
  );
};
