import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { theme, fontStack } from "../theme";
import type { Word } from "../schema";
import { pop } from "../lib/anim";

// Word-synced caption that BUILDS as it's spoken — each word springs up on its
// own timestamp, and the current word lifts into the accent. Short chunks keep
// it light instead of a wall of text.
const CHUNK = 5;

export const Caption: React.FC<{ words: Word[]; accent: string }> = ({ words, accent }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  if (!words.length) return null;

  let active = 0;
  for (let i = 0; i < words.length; i++) {
    if (frame >= words[i].startFrame) active = i;
  }
  const group = Math.floor(active / CHUNK);
  const slice = words.slice(group * CHUNK, group * CHUNK + CHUNK);

  return (
    <div
      style={{
        position: "absolute",
        left: 0,
        right: 0,
        bottom: 120,
        display: "flex",
        justifyContent: "center",
        alignItems: "flex-end",
        gap: 16,
        padding: "0 160px",
        height: 80,
      }}
    >
      {slice.map((w, i) => {
        const idx = group * CHUNK + i;
        const s = pop(frame, w.startFrame, fps); // springs in as spoken
        if (s < 0.001) return null;
        const isActive = idx === active;
        const since = frame - w.startFrame;
        const bounce = isActive ? 1 + Math.max(0, Math.sin(since / 3)) * 0.06 * Math.max(0, 1 - since / 12) : 1;
        return (
          <span
            key={idx}
            style={{
              fontFamily: fontStack.sans,
              fontWeight: 800,
              fontSize: 50,
              letterSpacing: -0.5,
              color: isActive ? theme.onAccent : theme.ink,
              background: isActive ? accent : "transparent",
              padding: isActive ? "2px 18px" : "2px 4px",
              borderRadius: 12,
              opacity: s,
              transform: `translateY(${(1 - s) * 26}px) scale(${bounce})`,
              boxShadow: isActive ? `0 0 28px ${accent}99` : "none",
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
