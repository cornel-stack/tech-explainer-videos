import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Icon } from "../components/Icon";
import { ManimFull, useHasClip } from "../components/ManimClip";
import { pop, beatAt } from "../lib/anim";

// Stage 3 — take a call apart. Request = address + method going out.
// Response = status + headers + body coming back. Each part pops on its word.
const Part: React.FC<{
  frame: number;
  fps: number;
  at: number;
  kicker: string;
  value: string;
  color: string;
}> = ({ frame, fps, at, kicker, value, color }) => {
  const s = pop(frame, at, fps);
  return (
    <div
      style={{
        opacity: s,
        transform: `translateY(${(1 - s) * 26}px)`,
        background: theme.paper,
        borderRadius: 18,
        boxShadow: theme.shadowSoft,
        padding: "16px 24px",
        borderLeft: `8px solid ${color}`,
        minWidth: 300,
      }}
    >
      <div
        style={{
          fontFamily: fontStack.mono,
          fontSize: 16,
          fontWeight: 600,
          letterSpacing: 1.5,
          color: theme.inkFaint,
          textTransform: "uppercase",
        }}
      >
        {kicker}
      </div>
      <div
        style={{
          fontFamily: fontStack.mono,
          fontSize: 28,
          fontWeight: 600,
          color: theme.ink,
        }}
      >
        {value}
      </div>
    </div>
  );
};

export const AnatomyScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hasClip = useHasClip("anatomy");
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);

  if (hasClip) return <ManimFull name="anatomy" />;

  const Col: React.FC<{ title: string; color: string; dir: string; children: React.ReactNode }> = ({
    title,
    color,
    dir,
    children,
  }) => (
    <div style={{ display: "flex", flexDirection: "column", gap: 18, width: 620 }}>
      <div style={{ display: "flex", alignItems: "center", gap: 12 }}>
        <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34, color }}>{title}</span>
        <span style={{ color }}>
          <Icon name="arrow" size={34} color={color} />
        </span>
        <span style={{ fontFamily: fontStack.mono, fontSize: 20, color: theme.inkFaint }}>{dir}</span>
      </div>
      {children}
    </div>
  );

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ display: "flex", gap: 90 }}>
        <Col title="REQUEST" color={theme.client} dir="going out">
          <Part frame={frame} fps={fps} at={b("endpoint", 40)} kicker="Address · endpoint" value="api.weather.gov/points" color={theme.client} />
          <Part frame={frame} fps={fps} at={b("method", 90)} kicker="Method · the verb" value="GET · POST · PUT · DELETE" color={theme.client} />
        </Col>
        <div style={{ width: 2, background: theme.line, alignSelf: "stretch" }} />
        <Col title="RESPONSE" color={theme.ok} dir="coming back">
          <Part frame={frame} fps={fps} at={b("status", 150)} kicker="Status · how it went" value="200 · 404 · 429" color={theme.ok} />
          <Part frame={frame} fps={fps} at={b("headers", 190)} kicker="Headers · labels" value="content-type: json" color={theme.ok} />
          <Part frame={frame} fps={fps} at={b("body", 230)} kicker="Body · the data" value="{ forecast: … }" color={theme.ok} />
        </Col>
      </div>
    </AbsoluteFill>
  );
};
