import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Icon } from "../components/Icon";
import { Machine } from "../characters/Machine";
import { Wire, Pulse } from "../components/Flow";
import { ManimClip, useHasClip } from "../components/ManimClip";
import { pop, beatAt } from "../lib/anim";

// Stage 5 — why build this way: reuse what you'd never build. Three app→API
// rows, then the flight-search fan-out (Manim clip, native fallback).
export const WhyScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);
  const fanoutAt = b("fanout", 99999);
  const hasClip = useHasClip("fanout");

  const rowsFade = interpolate(frame, [fanoutAt - 18, fanoutAt], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const fanFade = interpolate(frame, [fanoutAt, fanoutAt + 18], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const rows = [
    { app: "Weather app", icon: "cloud", api: "Weather API", seed: "weather-provider", mark: "weatherApi", bg: theme.accents.mint },
    { app: "Translate", icon: "messenger", api: "Translation API", seed: "translate-svc", mark: "translateApi", bg: theme.accents.gold },
    { app: "Checkout", icon: "check", api: "Payments API", seed: "payments-svc", mark: "paymentsApi", bg: theme.accents.violet },
  ];

  return (
    <AbsoluteFill>
      {/* phase A: app -> API rows */}
      <AbsoluteFill style={{ opacity: rowsFade, alignItems: "center", justifyContent: "center" }}>
        <div style={{ display: "flex", flexDirection: "column", gap: 34 }}>
          {rows.map((r, i) => {
            const at = b(r.mark, 20 + i * 40);
            const s = pop(frame, at, fps);
            if (s < 0.001) return null;
            return (
              <div key={r.app} style={{ opacity: s, display: "flex", alignItems: "center", gap: 10 }}>
                <div
                  style={{
                    display: "flex",
                    alignItems: "center",
                    gap: 16,
                    background: theme.paper,
                    borderRadius: 18,
                    boxShadow: theme.shadowSoft,
                    padding: "18px 26px",
                    width: 420,
                  }}
                >
                  <div style={{ width: 64, height: 64, borderRadius: 14, background: r.bg, display: "grid", placeItems: "center" }}>
                    <Icon name={r.icon} size={38} color={theme.onAccent} />
                  </div>
                  <span style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 32, color: theme.ink }}>{r.app}</span>
                </div>
                <svg width="220" height="80" viewBox="0 0 220 80">
                  <Wire from={{ x: 6, y: 40 }} to={{ x: 190, y: 40 }} at={at} width={5} dash />
                  <Pulse from={{ x: 6, y: 40 }} to={{ x: 190, y: 40 }} at={at + 10} dur={26} color={r.bg} r={9} />
                </svg>
                <Machine seed={r.seed} kind="api" size={120} bg={r.bg} label={r.api} />
              </div>
            );
          })}
        </div>
      </AbsoluteFill>

      {/* phase B: the fan-out */}
      {frame >= fanoutAt - 20 ? (
        <AbsoluteFill style={{ opacity: fanFade, alignItems: "center", justifyContent: "center" }}>
          {hasClip ? (
            <ManimClip name="fanout" from={fanoutAt} width={1500} style={{ borderRadius: 18, boxShadow: theme.shadow }} />
          ) : (
            <NativeFanout frame={frame} fps={fps} start={fanoutAt} />
          )}
        </AbsoluteFill>
      ) : null}
    </AbsoluteFill>
  );
};

// Fallback fan-out if the Manim clip is unavailable: one client → five airline
// APIs, result chips returning into a merged list.
const NativeFanout: React.FC<{ frame: number; fps: number; start: number }> = ({ frame, start }) => {
  const airlines = ["Airline A", "Airline B", "Airline C", "Airline D", "Airline E"];
  const prices = ["$420", "$510", "sold out", "$390", "$455"];
  const cx = 360;
  const cy = 360;
  return (
    <svg viewBox="0 0 1920 720" style={{ width: 1600 }}>
      <g>
        <rect x={cx - 150} y={cy - 46} width={300} height={92} rx={18} fill={theme.paper} stroke={theme.client} strokeWidth={3} />
        <text x={cx} y={cy + 8} textAnchor="middle" fontFamily="Inter" fontWeight={800} fontSize={30} fill={theme.ink}>
          Flight Search
        </text>
      </g>
      {airlines.map((name, i) => {
        const ty = 120 + i * 120;
        const at = start + 10 + i * 10;
        return (
          <g key={name}>
            <Wire from={{ x: cx + 150, y: cy }} to={{ x: 1360, y: ty }} at={at} width={3} dash />
            <Pulse from={{ x: cx + 150, y: cy }} to={{ x: 1360, y: ty }} at={at} dur={24} color={theme.api} r={8} />
            <Pulse from={{ x: 1360, y: ty }} to={{ x: cx + 150, y: cy }} at={at + 34} dur={26} color={theme.ok} r={8} label={prices[i]} />
            <rect x={1360} y={ty - 36} width={220} height={72} rx={14} fill={theme.paper} stroke={theme.api} strokeWidth={2.5} />
            <text x={1470} y={ty + 8} textAnchor="middle" fontFamily="Inter" fontWeight={700} fontSize={26} fill={theme.ink}>
              {name}
            </text>
          </g>
        );
      })}
    </svg>
  );
};
