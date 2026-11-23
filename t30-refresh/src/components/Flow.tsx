import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { theme } from "../theme";

export type Pt = { x: number; y: number };

// A connecting wire that draws itself on between two points.
export const Wire: React.FC<{
  from: Pt;
  to: Pt;
  at: number;
  color?: string;
  width?: number;
  dash?: boolean;
}> = ({ from, to, at, color = theme.line, width = 4, dash }) => {
  const frame = useCurrentFrame();
  const draw = interpolate(frame, [at, at + 16], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const len = Math.hypot(to.x - from.x, to.y - from.y);
  return (
    <line
      x1={from.x}
      y1={from.y}
      x2={to.x}
      y2={to.y}
      stroke={color}
      strokeWidth={width}
      strokeLinecap="round"
      strokeDasharray={dash ? "2 14" : `${len}`}
      strokeDashoffset={dash ? 0 : len * (1 - draw)}
    />
  );
};

// A glowing packet that travels from -> to over `dur` frames starting at `at`.
export const Pulse: React.FC<{
  from: Pt;
  to: Pt;
  at: number;
  dur?: number;
  color?: string;
  r?: number;
  label?: string;
}> = ({ from, to, at, dur = 26, color = theme.client, r = 12, label }) => {
  const frame = useCurrentFrame();
  const t = interpolate(frame, [at, at + dur], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  if (frame < at || t >= 1) return null;
  const x = from.x + (to.x - from.x) * t;
  const y = from.y + (to.y - from.y) * t;
  const glow = Math.sin(t * Math.PI); // fade in/out along the path
  return (
    <g opacity={glow}>
      <circle cx={x} cy={y} r={r + 8} fill={color} opacity={0.18} />
      <circle cx={x} cy={y} r={r} fill={color} />
      {label ? (
        <text
          x={x}
          y={y - r - 10}
          textAnchor="middle"
          fontFamily="'IBM Plex Mono', monospace"
          fontSize={22}
          fontWeight={700}
          fill={color}
        >
          {label}
        </text>
      ) : null}
    </g>
  );
};
