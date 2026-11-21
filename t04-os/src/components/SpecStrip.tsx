import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { theme, fontStack } from "../theme";
import type { Spec, Source } from "../schema";
import { pop } from "../lib/anim";

// Fact rows that pop in on the exact frame the number is spoken (atFrame), each
// carrying a tiny source tag — the channel's signature "every number is sourced".
export const SpecStrip: React.FC<{
  specs: Spec[];
  sources: Source[];
  accent: string;
}> = ({ specs, sources, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  return (
    <div
      style={{
        position: "absolute",
        top: 64,
        right: 72,
        display: "flex",
        flexDirection: "column",
        gap: 14,
        alignItems: "flex-end",
      }}
    >
      {specs.map((spec, i) => {
        const s = pop(frame, spec.atFrame, fps);
        if (s < 0.001) return null;
        const src = sources.find((x) => x.id === spec.source);
        return (
          <div
            key={i}
            style={{
              transform: `translate(${(1 - s) * 60}px, ${Math.sin(frame / 24 + i) * 4 * s}px)`,
              opacity: s,
              background: theme.paper,
              borderRadius: 16,
              boxShadow: `0 10px 30px rgba(0,0,0,0.5), 0 0 ${18 * s}px ${accent}44`,
              padding: "14px 20px",
              minWidth: 320,
              borderRight: `6px solid ${accent}`,
            }}
          >
            <div
              style={{
                fontFamily: fontStack.mono,
                fontSize: 16,
                fontWeight: 600,
                color: theme.inkFaint,
                letterSpacing: 1.5,
                textTransform: "uppercase",
              }}
            >
              {spec.label}
            </div>
            <div
              style={{
                fontFamily: fontStack.sans,
                fontSize: 27,
                fontWeight: 800,
                color: theme.ink,
              }}
            >
              {spec.value}
            </div>
            {src ? (
              <div
                style={{
                  fontFamily: fontStack.mono,
                  fontSize: 13,
                  color: theme.inkFaint,
                  marginTop: 4,
                }}
              >
                ↳ {src.label}
              </div>
            ) : null}
          </div>
        );
      })}
    </div>
  );
};
