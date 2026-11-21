import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";

// The signature visual: a chip die drawn as an animated ISOMETRIC "silicon city".
// P-cores = tall glowing towers (two hyperthread elevators), E-cores = low blocks,
// NPU = a violet spire, Xe = a gold graphics district, disabled cores (binning)
// go dark. Counts come from the chip's die config, so every tier looks different.
type Die = { p?: number; e?: number; npu?: boolean; xe?: number; gray?: number };

// mix a hex colour toward black (f<1) — for shaded iso faces.
function shade(hex: string, f: number) {
  const n = parseInt(hex.slice(1), 16);
  const r = Math.round(((n >> 16) & 255) * f);
  const g = Math.round(((n >> 8) & 255) * f);
  const b = Math.round((n & 255) * f);
  return `rgb(${r},${g},${b})`;
}

const HW = 34; // iso tile half-width
const HH = 17; // iso tile half-height (2:1 iso)

type TileDef = { type: "P" | "E" | "NPU" | "XE"; color: string; h: number; dark: boolean };

const IsoBox: React.FC<{ cx: number; cy: number; h: number; color: string; dark: boolean; glow: number; threads: number }> = ({
  cx,
  cy,
  h,
  color,
  dark,
  glow,
  threads,
}) => {
  const base = dark ? "#17171C" : color;
  const top = dark ? "#202026" : shade(color, 1);
  const left = dark ? "#101014" : shade(color, 0.42);
  const right = dark ? "#0C0C10" : shade(color, 0.6);
  const bN = `${cx},${cy - HH}`, bE = `${cx + HW},${cy}`, bS = `${cx},${cy + HH}`, bW = `${cx - HW},${cy}`;
  const tN = `${cx},${cy - HH - h}`, tE = `${cx + HW},${cy - h}`, tS = `${cx},${cy + HH - h}`, tW = `${cx - HW},${cy - h}`;
  return (
    <g>
      <polygon points={`${bW} ${bS} ${tS} ${tW}`} fill={left} />
      <polygon points={`${bS} ${bE} ${tE} ${tS}`} fill={right} />
      <polygon points={`${tN} ${tE} ${tS} ${tW}`} fill={top} stroke={dark ? "#2a2a30" : shade(color, 1)} strokeWidth={1} />
      {!dark ? <polygon points={`${tN} ${tE} ${tS} ${tW}`} fill={color} opacity={0.25 + glow * 0.4} /> : null}
      {/* hyperthread "elevators" climbing P towers */}
      {!dark && threads ? (
        <>
          <line x1={cx - 8} y1={cy} x2={cx - 8} y2={cy - h} stroke="#ffffff" strokeWidth={2} opacity={0.3 + glow * 0.5} />
          <line x1={cx + 8} y1={cy} x2={cx + 8} y2={cy - h} stroke="#ffffff" strokeWidth={2} opacity={0.3 + (1 - glow) * 0.5} />
        </>
      ) : null}
      {dark ? <text x={cx} y={cy - h / 2} textAnchor="middle" fontSize={22} fill={theme.accents.coral} fontWeight={800}>✕</text> : null}
    </g>
  );
};

export const IsoDieCity: React.FC<{ die: Die; accent: string; width?: number; height?: number }> = ({ die, accent, width = 1030, height = 505 }) => {
  const frame = useCurrentFrame();
  const p = die.p ?? 0, e = die.e ?? 0, gray = die.gray ?? 0, xe = die.xe ?? 0;

  // build the tile list
  const tiles: TileDef[] = [];
  const pShown = Math.min(p, 20);
  for (let i = 0; i < pShown; i++) tiles.push({ type: "P", color: accent, h: 72, dark: i < gray });
  const eShown = Math.min(e, 24);
  for (let i = 0; i < eShown; i++) tiles.push({ type: "E", color: theme.accents.magenta, h: 26, dark: p + i < gray });
  if (die.npu) tiles.push({ type: "NPU", color: theme.accents.violet, h: 88, dark: false });
  for (let i = 0; i < Math.min(xe, 10); i++) tiles.push({ type: "XE", color: theme.accents.gold, h: 40, dark: false });

  // place row-major on a grid
  const cols = Math.max(4, Math.ceil(Math.sqrt(tiles.length * 1.5)));
  const placed = tiles.map((t, i) => ({ ...t, gx: i % cols, gy: Math.floor(i / cols), idx: i }));
  const rows = Math.ceil(tiles.length / cols);

  // centre the iso grid
  const originX = width / 2 - ((cols - rows) * HW) / 2;
  const originY = height / 2 - ((cols + rows) * HH) / 2 + 60;

  // painter's order: smaller (gx+gy) first
  placed.sort((a, b) => a.gx + a.gy - (b.gx + b.gy));

  return (
    <div style={{ position: "relative", width, height, background: "#070809", borderRadius: 14, border: `1px solid ${accent}44`, overflow: "hidden", boxShadow: `0 0 30px ${accent}22` }}>
      {/* circuit grid floor */}
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${accent}14 1px, transparent 1px), linear-gradient(90deg, ${accent}14 1px, transparent 1px)`, backgroundSize: "44px 44px", opacity: 0.5 }} />
      <svg viewBox={`0 0 ${width} ${height}`} style={{ position: "absolute", inset: 0 }}>
        {placed.map((t) => {
          const cx = originX + (t.gx - t.gy) * HW;
          const cy = originY + (t.gx + t.gy) * HH;
          const glow = 0.5 + Math.sin(frame / 11 + t.idx * 0.8) * 0.5;
          return <IsoBox key={t.idx} cx={cx} cy={cy} h={t.h} color={t.color} dark={t.dark} glow={glow} threads={t.type === "P" ? 2 : 0} />;
        })}
      </svg>
      {/* legend */}
      <div style={{ position: "absolute", left: 20, bottom: 16, display: "flex", gap: 18, fontFamily: fontStack.mono, fontSize: 16 }}>
        {p > 0 ? <span style={{ color: accent }}>▮ {p}× P-core</span> : null}
        {e > 0 ? <span style={{ color: theme.accents.magenta }}>▪ {e}× E-core</span> : null}
        {die.npu ? <span style={{ color: theme.accents.violet }}>▲ NPU</span> : null}
        {xe > 0 ? <span style={{ color: theme.accents.gold }}>◆ {xe}× Xe</span> : null}
      </div>
      <div style={{ position: "absolute", right: 20, top: 14, fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 2 }}>◢ SILICON DIE</div>
    </div>
  );
};
