import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { theme, fontStack, glow } from "../theme";
import { pop } from "../lib/anim";

// One-sentence takeaway that lands at the end of each stage.
export const Verdict: React.FC<{ text: string; accent: string; at: number }> = ({
  text,
  accent,
  at,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = pop(frame, at, fps);
  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 108,
        display: "flex",
        justifyContent: "center",
        opacity: s,
        transform: `translateY(${(1 - s) * 30}px)`,
      }}
    >
      <div
        style={{
          display: "flex",
          alignItems: "center",
          gap: 18,
          background: theme.paper,
          color: theme.ink,
          padding: "20px 34px",
          borderRadius: 999,
          boxShadow: glow(accent, 0.4),
          border: `1px solid ${accent}55`,
          maxWidth: 1400,
        }}
      >
        <span
          style={{
            width: 14,
            height: 14,
            borderRadius: 999,
            background: accent,
            flex: "none",
          }}
        />
        <span
          style={{
            fontFamily: fontStack.sans,
            fontWeight: 700,
            fontSize: 34,
            letterSpacing: -0.4,
          }}
        >
          {text}
        </span>
      </div>
    </div>
  );
};
