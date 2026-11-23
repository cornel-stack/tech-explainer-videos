import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";
import { Icon } from "./Icon";

// Animated diagram of one style's call pattern. Loops so it reads at any point
// in the (variable-length) narration. Two nodes — client left, server right —
// and packets that move the way that style actually moves.
const VB_W = 1200;
const VB_H = 360;
const LX = 170; // client x
const RX = 1030; // server x
const CY = 185; // line y
const PERIOD = 150;

type Dot = { t: number; color: string; r?: number; label?: string };

function dotXY(t: number) {
  return { x: LX + 40 + (RX - 40 - (LX + 40)) * t, y: CY };
}

const Packet: React.FC<{ d: Dot }> = ({ d }) => {
  const { x, y } = dotXY(d.t);
  const glow = Math.sin(Math.min(1, Math.max(0, d.t)) * Math.PI);
  return (
    <g opacity={glow}>
      <circle cx={x} cy={y} r={(d.r ?? 11) + 8} fill={d.color} opacity={0.18} />
      <circle cx={x} cy={y} r={d.r ?? 11} fill={d.color} />
      {d.label ? (
        <text x={x} y={y - 22} textAnchor="middle" fontFamily={fontStack.mono} fontSize={21} fontWeight={700} fill={d.color}>
          {d.label}
        </text>
      ) : null}
    </g>
  );
};

const Node: React.FC<{ x: number; label: string; icon: string; color: string }> = ({ x, label, icon, color }) => (
  <g>
    <rect x={x - 95} y={CY - 70} width={190} height={140} rx={22} fill={theme.paper} stroke={`${color}66`} strokeWidth={2} />
    <g transform={`translate(${x - 26}, ${CY - 48})`}>
      <Icon name={icon} size={52} color={color} />
    </g>
    <text x={x} y={CY + 46} textAnchor="middle" fontFamily={fontStack.sans} fontSize={26} fontWeight={800} fill={theme.ink}>
      {label}
    </text>
  </g>
);

export const CallPattern: React.FC<{ pattern: string; accent: string }> = ({ pattern, accent }) => {
  const frame = useCurrentFrame();
  const p = (frame % PERIOD) / PERIOD; // 0..1 loop phase
  const A = theme.accents;

  const dots: Dot[] = [];
  let note = "";
  let persistent = false;

  const fwd = (t: number) => Math.min(1, Math.max(0, t));
  const rev = (t: number) => 1 - fwd(t);

  switch (pattern) {
    case "reqres":
    case "envelope": {
      if (p < 0.5) dots.push({ t: fwd(p / 0.5), color: accent, label: pattern === "envelope" ? "envelope" : "request" });
      else dots.push({ t: rev((p - 0.5) / 0.5), color: A.mint, label: "response" });
      break;
    }
    case "oneQuery": {
      if (p < 0.45) dots.push({ t: fwd(p / 0.45), color: accent, label: "one query" });
      else dots.push({ t: rev((p - 0.45) / 0.55), color: A.mint, r: 15, label: "exact shape" });
      break;
    }
    case "streams": {
      persistent = true;
      note = "bi-directional streaming · HTTP/2";
      for (let k = 0; k < 3; k++) {
        const pk = (p + k / 3) % 1;
        dots.push({ t: fwd(pk), color: accent, r: 9 });
        dots.push({ t: 1 - fwd((p + k / 3 + 0.16) % 1), color: A.mint, r: 9 });
      }
      break;
    }
    case "handshake": {
      persistent = true;
      note = "101 Switching Protocols → line stays open";
      // two-way traffic on a now-permanent connection
      dots.push({ t: fwd((p * 2) % 1), color: accent, r: 10 });
      dots.push({ t: 1 - fwd((p * 2 + 0.5) % 1), color: A.mint, r: 10 });
      break;
    }
    case "serverStream": {
      persistent = true;
      note = "server pushes · one-way";
      for (let k = 0; k < 3; k++) {
        const pk = (p + k / 3) % 1;
        dots.push({ t: 1 - fwd(pk), color: accent, r: 10 });
      }
      break;
    }
    case "callback": {
      // event fires on the server, which POSTs to you
      if (p < 0.5) {
        // event pulse glowing on the server
      } else {
        dots.push({ t: 1 - fwd((p - 0.5) / 0.5), color: accent, label: "POST event" });
      }
      break;
    }
    default:
      dots.push({ t: p < 0.5 ? fwd(p / 0.5) : rev((p - 0.5) / 0.5), color: accent });
  }

  // peer-to-peer is drawn specially
  if (pattern === "peer") {
    return <PeerDiagram accent={accent} frame={frame} />;
  }

  const clientLabel = pattern === "callback" ? "your URL" : "Client";
  const serverEvent = pattern === "callback" && p < 0.5;

  return (
    <svg viewBox={`0 0 ${VB_W} ${VB_H}`} style={{ width: "100%" }}>
      {/* connection line */}
      <line x1={LX + 95} y1={CY} x2={RX - 95} y2={CY} stroke={persistent ? `${accent}` : theme.line} strokeWidth={persistent ? 5 : 4} strokeDasharray={persistent ? "0" : "2 16"} strokeLinecap="round" opacity={persistent ? 0.5 : 1} />
      {dots.map((d, i) => <Packet key={i} d={d} />)}
      <Node x={LX} label={clientLabel} icon="laptop" color={theme.accents.amber} />
      <g>
        <Node x={RX} label="Server" icon="server" color={theme.accents.violet} />
        {serverEvent ? (
          <circle cx={RX} cy={CY - 70} r={14 + Math.sin(frame / 5) * 4} fill={accent} opacity={0.9} />
        ) : null}
      </g>
      {note ? (
        <text x={VB_W / 2} y={CY + 120} textAnchor="middle" fontFamily={fontStack.mono} fontSize={22} fill={theme.inkSoft}>
          {note}
        </text>
      ) : null}
    </svg>
  );
};

// WebRTC — two peers talk directly; a signalling server only introduces them.
const PeerDiagram: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => {
  const p = (frame % PERIOD) / PERIOD;
  const ax = 230, bx = 970, py = 250, sx = 600, sy = 70;
  const introDone = frame > 50;
  const t = (p * 2) % 1;
  const back = 1 - ((p * 2 + 0.5) % 1);
  const pt = (t: number) => ({ x: ax + 60 + (bx - 60 - (ax + 60)) * t, y: py });
  const d1 = pt(t), d2 = pt(back);
  return (
    <svg viewBox={`0 0 ${VB_W} ${VB_H}`} style={{ width: "100%" }}>
      {/* signalling (dotted, fades after intro) */}
      <line x1={ax} y1={py - 40} x2={sx} y2={sy + 30} stroke={theme.line} strokeWidth={3} strokeDasharray="2 12" opacity={introDone ? 0.3 : 1} />
      <line x1={bx} y1={py - 40} x2={sx} y2={sy + 30} stroke={theme.line} strokeWidth={3} strokeDasharray="2 12" opacity={introDone ? 0.3 : 1} />
      <rect x={sx - 95} y={sy - 24} width={190} height={56} rx={14} fill={theme.paper} stroke={`${theme.inkFaint}`} strokeWidth={1.5} />
      <text x={sx} y={sy + 12} textAnchor="middle" fontFamily={fontStack.mono} fontSize={20} fill={theme.inkSoft}>signalling</text>
      {/* direct peer line */}
      <line x1={ax + 60} y1={py} x2={bx - 60} y2={py} stroke={accent} strokeWidth={5} opacity={0.5} strokeLinecap="round" />
      <circle cx={d1.x} cy={d1.y} r={11} fill={accent} />
      <circle cx={d2.x} cy={d2.y} r={11} fill={theme.accents.mint} />
      <Node x={ax} label="Peer A" icon="phone" color={accent} />
      <Node x={bx} label="Peer B" icon="phone" color={accent} />
      <text x={VB_W / 2} y={py + 110} textAnchor="middle" fontFamily={fontStack.mono} fontSize={22} fill={theme.inkSoft}>media flows peer ↔ peer, directly</text>
    </svg>
  );
};
