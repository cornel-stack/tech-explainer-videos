import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Machine } from "../characters/Machine";
import { Wire } from "../components/Flow";
import { ManimFull, useHasClip } from "../components/ManimClip";
import { pop, beatAt } from "../lib/anim";

// Stage 6 — the styles hub. Same contract in the middle; five styles orbit it,
// each popping in (with its DiceBear mark) as it's named.
const POINTS = [
  { x: 960, y: 92 },
  { x: 1493, y: 250 },
  { x: 1289, y: 560 },
  { x: 631, y: 560 },
  { x: 427, y: 250 },
];

export const StylesScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hasClip = useHasClip("styles_hub");
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);

  if (hasClip) return <ManimFull name="styles_hub" />;
  const styles = (stage.styles ?? []) as {
    name: string;
    note: string;
    seed: string;
    source?: string;
  }[];
  const hub = pop(frame, 0, fps);
  const accents = [theme.accents.amber, theme.accents.violet, theme.accents.magenta, theme.accents.mint, theme.accents.coral];

  return (
    <AbsoluteFill>
      <svg viewBox="0 0 1920 720" style={{ position: "absolute", inset: 0 }}>
        {styles.map((s, i) => {
          const p = POINTS[i] ?? POINTS[0];
          return (
            <Wire
              key={s.name}
              from={{ x: 960, y: 360 }}
              to={{ x: p.x, y: p.y }}
              at={b(s.name.toLowerCase(), 20 + i * 20)}
              width={4}
              dash
            />
          );
        })}
      </svg>

      {/* hub */}
      <div
        style={{
          position: "absolute",
          left: 960,
          top: 360,
          transform: `translate(-50%,-50%) scale(${hub})`,
          width: 260,
          height: 260,
          borderRadius: 999,
          background: theme.ink,
          color: "#fff",
          display: "grid",
          placeItems: "center",
          textAlign: "center",
          boxShadow: theme.shadow,
        }}
      >
        <div>
          <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34 }}>Same<br />contract</div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 18, color: "#A8B0BD", marginTop: 8 }}>
            request → response
          </div>
        </div>
      </div>

      {/* style cards */}
      {styles.map((s, i) => {
        const p = POINTS[i] ?? POINTS[0];
        const sp = pop(frame, b(s.name.toLowerCase(), 20 + i * 20), fps);
        if (sp < 0.001) return null;
        const accent = accents[i % accents.length];
        return (
          <div
            key={s.name}
            style={{
              position: "absolute",
              left: p.x,
              top: p.y,
              transform: `translate(-50%,-50%) scale(${sp})`,
              opacity: sp,
              width: 300,
              background: theme.paper,
              borderRadius: 18,
              boxShadow: theme.shadow,
              padding: "16px 18px",
              display: "flex",
              alignItems: "center",
              gap: 14,
              borderTop: `6px solid ${accent}`,
            }}
          >
            <div style={{ width: 70, height: 70, borderRadius: 14, overflow: "hidden", flex: "none" }}>
              <Machine seed={s.seed} kind="api" size={70} bg={accent} />
            </div>
            <div>
              <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 30, color: theme.ink }}>{s.name}</div>
              <div style={{ fontFamily: fontStack.sans, fontSize: 19, color: theme.inkSoft, lineHeight: 1.2 }}>{s.note}</div>
            </div>
          </div>
        );
      })}
    </AbsoluteFill>
  );
};
