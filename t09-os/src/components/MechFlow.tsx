import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";

// A drawn, continuously-animated mechanism diagram: 3–5 labelled nodes in a row,
// connected by arrows, with a glowing packet that travels the whole chain on a
// loop (so it never freezes). This is how each OS's trick is explained —
// Red Star's USB tagging, Whonix's two-VM isolation, Tails' RAM wipe, the
// clipboard clipper, Phantom Secure's remote wipe.
export const MechFlow: React.FC<{
  nodes: string[];
  accent: string;
  width?: number;
  height?: number;
  title?: string;
}> = ({ nodes, accent, width = 1030, height = 180, title }) => {
  const frame = useCurrentFrame();
  const n = Math.max(2, nodes.length);
  const padX = 24;
  const gap = 26;
  const nodeW = (width - padX * 2 - gap * (n - 1)) / n;
  const nodeH = 92;
  const cy = height / 2 + (title ? 12 : 0);
  const centers = nodes.map((_, i) => padX + i * (nodeW + gap) + nodeW / 2);

  // one packet travelling the whole chain, looping.
  const perHop = 34;
  const period = perHop * (n - 1) + 24;
  const pf = frame % period;
  const seg = Math.min(n - 2, Math.floor(pf / perHop));
  const local = Math.min(1, (pf - seg * perHop) / perHop);
  const px = centers[seg] + (centers[seg + 1] - centers[seg]) * local;

  return (
    <svg viewBox={`0 0 ${width} ${height}`} width="100%" height="100%" style={{ display: "block" }}>
      {title ? (
        <text x={padX} y={16} fontFamily={fontStack.mono} fontSize={15} fill={theme.inkFaint} letterSpacing={2}>{title}</text>
      ) : null}

      {/* wires + arrowheads */}
      {centers.slice(0, -1).map((cx, i) => {
        const x1 = cx + nodeW / 2;
        const x2 = centers[i + 1] - nodeW / 2;
        return (
          <g key={`w${i}`}>
            <line x1={x1} y1={cy} x2={x2 - 10} y2={cy} stroke={`${accent}66`} strokeWidth={3} />
            <path d={`M ${x2 - 12} ${cy - 7} L ${x2 - 2} ${cy} L ${x2 - 12} ${cy + 7}`} fill="none" stroke={`${accent}aa`} strokeWidth={3} strokeLinecap="round" strokeLinejoin="round" />
          </g>
        );
      })}

      {/* nodes */}
      {nodes.map((label, i) => {
        const cx = centers[i];
        const breathe = 0.5 + 0.5 * Math.sin(frame / 14 + i * 0.9);
        return (
          <g key={`n${i}`}>
            <rect x={cx - nodeW / 2} y={cy - nodeH / 2} width={nodeW} height={nodeH} rx={12}
              fill={theme.paper} stroke={accent} strokeWidth={2} opacity={0.96} />
            <rect x={cx - nodeW / 2} y={cy - nodeH / 2} width={nodeW} height={nodeH} rx={12}
              fill="none" stroke={accent} strokeWidth={6} opacity={0.08 + breathe * 0.14} />
            {wrap(label).map((line, li, arr) => (
              <text key={li} x={cx} y={cy + (li - (arr.length - 1) / 2) * 22 + 7} textAnchor="middle"
                fontFamily={fontStack.sans} fontWeight={700} fontSize={19} fill={theme.ink}>{line}</text>
            ))}
            <text x={cx} y={cy - nodeH / 2 - 10} textAnchor="middle" fontFamily={fontStack.mono}
              fontSize={13} fill={`${accent}`} opacity={0.7}>{i + 1}</text>
          </g>
        );
      })}

      {/* travelling packet */}
      <g>
        <circle cx={px} cy={cy} r={16} fill={accent} opacity={0.2} />
        <circle cx={px} cy={cy} r={8} fill={accent} />
      </g>
    </svg>
  );
};

// crude 2-line wrap so longer labels fit a node box.
function wrap(s: string): string[] {
  if (s.length <= 15) return [s];
  const words = s.split(" ");
  const lines: string[] = [];
  let cur = "";
  for (const w of words) {
    if ((cur + " " + w).trim().length > 15 && cur) {
      lines.push(cur.trim());
      cur = w;
    } else {
      cur = (cur + " " + w).trim();
    }
  }
  if (cur) lines.push(cur);
  return lines.slice(0, 2);
}
