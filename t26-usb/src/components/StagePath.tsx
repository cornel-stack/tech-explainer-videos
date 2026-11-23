import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";

// A native infection-path flow: the named steps as stage boxes with a glowing
// payload packet that travels across them on a continuous loop (the stage it's
// passing through flares). Used for items without a dedicated Manim clip.
export const StagePath: React.FC<{ steps: string[]; accent: string }> = ({ steps, accent }) => {
  const frame = useCurrentFrame();
  const n = Math.max(1, steps.length);
  const W = 1180;
  const H = 150;
  const pad = 30;
  const slot = (W - pad * 2) / n;
  const boxW = slot - 26;
  const centerX = (i: number) => pad + slot * i + slot / 2;

  const period = n * 54;
  const ph = (frame % period) / period; // 0..1 across the whole path
  const packetX = pad + (W - pad * 2) * ph;
  const activeIdx = Math.min(n - 1, Math.floor(ph * n));

  return (
    <svg viewBox={`0 0 ${W} ${H}`} style={{ width: "100%" }}>
      {/* connectors */}
      {steps.slice(0, -1).map((_, i) => (
        <line key={i} x1={centerX(i) + boxW / 2} y1={H / 2} x2={centerX(i + 1) - boxW / 2} y2={H / 2} stroke={theme.line} strokeWidth={3} strokeDasharray="2 10" />
      ))}
      {/* stage boxes */}
      {steps.map((s, i) => {
        const active = i === activeIdx;
        return (
          <g key={i}>
            <rect
              x={centerX(i) - boxW / 2}
              y={H / 2 - 42}
              width={boxW}
              height={84}
              rx={12}
              fill={theme.paper}
              stroke={active ? accent : `${accent}44`}
              strokeWidth={active ? 3 : 1.5}
              style={{ filter: active ? `drop-shadow(0 0 14px ${accent})` : "none" }}
            />
            <text x={centerX(i)} y={H / 2 + 7} textAnchor="middle" fontFamily={fontStack.mono} fontSize={23} fontWeight={active ? 700 : 500} fill={active ? theme.ink : theme.inkSoft}>
              {s}
            </text>
            <text x={centerX(i)} y={H / 2 - 54} textAnchor="middle" fontFamily={fontStack.mono} fontSize={15} fill={theme.inkFaint}>
              {String(i + 1).padStart(2, "0")}
            </text>
          </g>
        );
      })}
      {/* travelling payload */}
      <circle cx={packetX} cy={H / 2} r={16} fill={accent} opacity={0.2} />
      <circle cx={packetX} cy={H / 2} r={8} fill={accent} style={{ filter: `drop-shadow(0 0 8px ${accent})` }} />
    </svg>
  );
};
