import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// Our OWN flat "silicon die" schematic (no brand die shots): big P-core tiles
// (each with two hyperthread cells), small E-core tiles, an optional NPU tile and
// Xe GPU tiles. `gray` disables the first N cores (binning). Counts change per chip.
type Die = { p?: number; e?: number; npu?: boolean; xe?: number; gray?: number };

const Tile: React.FC<{ size: number; label: string; color: string; gray?: boolean; threads?: number; frame: number; i: number }> = ({
  size,
  label,
  color,
  gray,
  threads,
  frame,
  i,
}) => {
  const pulse = gray ? 0.22 : 0.6 + Math.sin(frame / 12 + i * 0.7) * 0.25;
  return (
    <div style={{ width: size, height: size, borderRadius: Math.max(6, size * 0.12), background: gray ? "#15151A" : `${color}1f`, border: `1.5px solid ${gray ? theme.inkFaint : color}`, boxShadow: gray ? "none" : `0 0 ${10 + pulse * 14}px ${color}55`, display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center", gap: size * 0.08, position: "relative", opacity: gray ? 0.6 : 1 }}>
      <span style={{ fontFamily: fontStack.mono, fontWeight: 700, fontSize: size * 0.3, color: gray ? theme.inkFaint : color }}>{label}</span>
      {threads ? (
        <div style={{ display: "flex", gap: size * 0.06 }}>
          {Array.from({ length: threads }).map((_, t) => (
            <div key={t} style={{ width: size * 0.26, height: size * 0.11, borderRadius: 3, background: color, opacity: 0.5 + Math.sin(frame / 7 + t + i) * 0.4 }} />
          ))}
        </div>
      ) : null}
      {gray ? <span style={{ position: "absolute", fontSize: size * 0.5, color: theme.accents.coral, fontWeight: 800 }}>✕</span> : null}
    </div>
  );
};

export const DieTiles: React.FC<{ die: Die; accent: string; width?: number; height?: number }> = ({ die, accent, width = 1030, height = 505 }) => {
  const frame = useCurrentFrame();
  const p = die.p ?? 0;
  const e = die.e ?? 0;
  const gray = die.gray ?? 0;
  const pSize = p <= 8 ? 96 : p <= 16 ? 66 : 48;
  const eSize = e <= 10 ? 54 : 40;

  return (
    <div style={{ position: "relative", width, height, background: "#090A0D", borderRadius: 14, border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.2), padding: "20px 28px", display: "flex", flexDirection: "column", gap: 14, overflow: "hidden" }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 2 }}>◢ SILICON DIE</div>

      {p > 0 ? (
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: accent, marginBottom: 6 }}>{p}× P-CORE · performance · hyperthreaded</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 10 }}>
            {Array.from({ length: Math.min(p, 32) }).map((_, i) => (
              <Tile key={i} size={pSize} label="P" color={accent} threads={2} gray={i < gray} frame={frame} i={i} />
            ))}
          </div>
        </div>
      ) : null}

      {e > 0 ? (
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.accents.magenta, marginBottom: 6 }}>{e}× E-CORE · efficiency</div>
          <div style={{ display: "flex", flexWrap: "wrap", gap: 8 }}>
            {Array.from({ length: Math.min(e, 24) }).map((_, i) => (
              <Tile key={i} size={eSize} label="E" color={theme.accents.magenta} gray={p + i < gray} frame={frame} i={i + 50} />
            ))}
          </div>
        </div>
      ) : null}

      {die.npu || (die.xe ?? 0) > 0 ? (
        <div style={{ display: "flex", gap: 16, alignItems: "center", marginTop: "auto" }}>
          {die.npu ? <Tile size={64} label="NPU" color={theme.accents.violet} frame={frame} i={7} /> : null}
          {(die.xe ?? 0) > 0 ? (
            <div>
              <div style={{ fontFamily: fontStack.mono, fontSize: 14, color: theme.accents.gold, marginBottom: 4 }}>{die.xe}× Xe · GPU</div>
              <div style={{ display: "flex", gap: 6 }}>
                {Array.from({ length: Math.min(die.xe ?? 0, 12) }).map((_, i) => (
                  <Tile key={i} size={32} label="" color={theme.accents.gold} frame={frame} i={i + 20} />
                ))}
              </div>
            </div>
          ) : null}
        </div>
      ) : null}
    </div>
  );
};
