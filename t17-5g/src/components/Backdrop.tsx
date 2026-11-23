import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import { theme } from "../theme";

// Living backdrop: an orbiting accent glow, slow-drifting dot grid, and soft
// floating orbs — so every frame has gentle motion behind the content.
const ORBS = [
  { c: "amber", x: 18, y: 30, r: 320, sx: 0.17, sy: 0.23, ph: 0 },
  { c: "magenta", x: 78, y: 24, r: 380, sx: 0.21, sy: 0.15, ph: 1.4 },
  { c: "mint", x: 62, y: 74, r: 300, sx: 0.15, sy: 0.2, ph: 2.6 },
  { c: "violet", x: 30, y: 78, r: 340, sx: 0.19, sy: 0.17, ph: 3.9 },
  { c: "coral", x: 90, y: 62, r: 260, sx: 0.23, sy: 0.19, ph: 5.1 },
] as const;

export const Backdrop: React.FC<{ accent: string }> = ({ accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const gx = 80 + Math.sin(t * 0.22) * 16;
  const gy = -8 + Math.cos(t * 0.18) * 12;
  const grid = (t * 6) % 44;

  return (
    <AbsoluteFill style={{ background: theme.bg, overflow: "hidden" }}>
      {/* drifting dot grid */}
      <AbsoluteFill
        style={{
          backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`,
          backgroundSize: "44px 44px",
          backgroundPosition: `${grid}px ${grid * 0.6}px`,
          opacity: 0.5,
        }}
      />
      {/* floating orbs */}
      {ORBS.map((o, i) => {
        const dx = Math.sin(t * o.sx + o.ph) * 60;
        const dy = Math.cos(t * o.sy + o.ph) * 48;
        const pulse = 0.14 + Math.sin(t * 0.5 + o.ph) * 0.05;
        const col = (theme.accents as Record<string, string>)[o.c];
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: `${o.x}%`,
              top: `${o.y}%`,
              width: o.r,
              height: o.r,
              marginLeft: -o.r / 2,
              marginTop: -o.r / 2,
              borderRadius: "50%",
              background: `radial-gradient(circle, ${col} 0%, transparent 70%)`,
              opacity: pulse,
              filter: "blur(40px)",
              transform: `translate(${dx}px, ${dy}px)`,
            }}
          />
        );
      })}
      {/* orbiting primary glow in the stage accent */}
      <AbsoluteFill
        style={{
          background: `radial-gradient(1100px 760px at ${gx}% ${gy}%, ${accent}26, transparent 60%)`,
        }}
      />
      <AbsoluteFill
        style={{
          background: `radial-gradient(900px 600px at 0% 112%, ${theme.bgDeep}, transparent 55%)`,
        }}
      />
    </AbsoluteFill>
  );
};
