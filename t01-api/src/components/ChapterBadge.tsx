import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { theme, fontStack } from "../theme";
import { Icon } from "./Icon";
import { pop } from "../lib/anim";

// Stays in the top-left for the whole stage: step number, icon, chapter name.
export const ChapterBadge: React.FC<{
  index: number;
  total: number;
  icon: string;
  title: string;
  accent: string;
}> = ({ index, total, icon, title, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const s = pop(frame, 4, fps);
  return (
    <div
      style={{
        position: "absolute",
        top: 64,
        left: 72,
        display: "flex",
        alignItems: "center",
        gap: 18,
        transform: `translateX(${(1 - s) * -40}px)`,
        opacity: s,
      }}
    >
      <div
        style={{
          width: 72,
          height: 72,
          borderRadius: 20,
          background: theme.paper,
          boxShadow: theme.shadowSoft,
          display: "grid",
          placeItems: "center",
          border: `2px solid ${accent}`,
        }}
      >
        <Icon name={icon} size={40} color={accent} />
      </div>
      <div>
        <div
          style={{
            fontFamily: fontStack.mono,
            fontSize: 20,
            fontWeight: 600,
            color: accent,
            letterSpacing: 2,
          }}
        >
          STEP {index} / {total}
        </div>
        <div
          style={{
            fontFamily: fontStack.sans,
            fontSize: 34,
            fontWeight: 800,
            color: theme.ink,
            letterSpacing: -0.5,
          }}
        >
          {title}
        </div>
      </div>
    </div>
  );
};
