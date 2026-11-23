import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual: a resolution drawn as a pixel rectangle sized to its REAL
// share of 8K (so 480p is a postage stamp and 8K fills the frame), with a scanline
// sweep and a representative pixel grid. Shows W×H, megapixels, and the share of 8K
// — so you SEE how much more 4K is than 1080p, and how little 8K adds on top.
const REF_W = 7680; // 8K width = the reference ceiling
const REF_H = 4320;

export const ResGrid: React.FC<{
  w: number;
  h: number;
  accent: string;
  width?: number;
  height?: number;
}> = ({ w, h, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // the 8K reference box, fit inside the panel with margins
  const pad = 40;
  const availW = width - pad * 2;
  const availH = height - pad * 2 - 70; // leave room for labels
  const refScale = Math.min(availW / REF_W, availH / REF_H);
  const refBoxW = REF_W * refScale;
  const refBoxH = REF_H * refScale;
  const ox = (width - refBoxW) / 2;
  const oy = pad + 10;

  // this resolution's box (same scale → true relative size), grows in
  const grow = interpolate(frame, [0, 22], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const boxW = w * refScale * grow;
  const boxH = h * refScale * grow;
  // anchor bottom-left of the ref box so smaller resolutions nest in a corner
  const bx = ox;
  const by = oy + refBoxH - boxH;

  // representative grid lines (not literal pixels): density ~ sqrt of pixel share
  const cols = Math.max(4, Math.round((w / REF_W) * 28));
  const rows = Math.max(3, Math.round((h / REF_H) * 28));
  const mp = (w * h) / 1e6;
  const sharePct = ((w * h) / (REF_W * REF_H)) * 100;

  // scanline sweep across this box
  const t = durationInFrames > 1 ? (frame % 90) / 90 : 0;
  const scanY = by + boxH * t;

  return (
    <div style={{ position: "relative", width, height, background: "#070809", borderRadius: 14, border: `1px solid ${accent}44`, overflow: "hidden", boxShadow: glow(accent, 0.22) }}>
      <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="100%" style={{ position: "absolute", inset: 0 }}>
        {/* 8K reference outline */}
        <rect x={ox} y={oy} width={refBoxW} height={refBoxH} fill="none" stroke={theme.line} strokeWidth={2} strokeDasharray="6 8" />
        <text x={ox + refBoxW - 6} y={oy - 8} textAnchor="end" fontFamily={fontStack.mono} fontSize={14} fill={theme.inkFaint}>8K frame</text>

        {/* this resolution's filled box */}
        <rect x={bx} y={by} width={boxW} height={boxH} fill={`${accent}1f`} stroke={accent} strokeWidth={2.5} />
        {/* representative grid */}
        {grow > 0.98 && Array.from({ length: cols - 1 }).map((_, i) => (
          <line key={`c${i}`} x1={bx + (boxW / cols) * (i + 1)} y1={by} x2={bx + (boxW / cols) * (i + 1)} y2={by + boxH} stroke={`${accent}33`} strokeWidth={1} />
        ))}
        {grow > 0.98 && Array.from({ length: rows - 1 }).map((_, i) => (
          <line key={`r${i}`} x1={bx} y1={by + (boxH / rows) * (i + 1)} x2={bx + boxW} y2={by + (boxH / rows) * (i + 1)} stroke={`${accent}33`} strokeWidth={1} />
        ))}
        {/* scanline */}
        {grow > 0.98 && boxH > 10 ? <line x1={bx} y1={scanY} x2={bx + boxW} y2={scanY} stroke={accent} strokeWidth={2} opacity={0.6} /> : null}
      </svg>

      {/* readouts */}
      <div style={{ position: "absolute", left: 24, bottom: 18, display: "flex", alignItems: "flex-end", gap: 26 }}>
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 1 }}>RESOLUTION</div>
          <div style={{ fontFamily: fontStack.sans, fontSize: 40, fontWeight: 900, color: theme.ink, lineHeight: 1 }}>{w.toLocaleString()} × {h.toLocaleString()}</div>
        </div>
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 1 }}>PIXELS</div>
          <div style={{ fontFamily: fontStack.sans, fontSize: 32, fontWeight: 800, color: accent, lineHeight: 1 }}>{mp.toFixed(mp < 1 ? 2 : 1)} MP</div>
        </div>
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 1 }}>OF 8K</div>
          <div style={{ fontFamily: fontStack.sans, fontSize: 32, fontWeight: 800, color: theme.ink, lineHeight: 1 }}>{sharePct < 10 ? sharePct.toFixed(1) : Math.round(sharePct)}%</div>
        </div>
      </div>
    </div>
  );
};
