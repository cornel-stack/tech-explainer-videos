import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";
import type { Word } from "../schema";

// Big, word-synced caption band. Shows the chunk of narration around the word
// being spoken right now and lifts the active word in the stage accent.
const CHUNK = 7;

export const Caption: React.FC<{ words: Word[]; accent: string }> = ({
  words,
  accent,
}) => {
  const frame = useCurrentFrame();
  if (!words.length) return null;

  // Active word = last word whose start has passed.
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
        bottom: 118,
        display: "flex",
        justifyContent: "center",
        gap: 16,
        flexWrap: "wrap",
        padding: "0 160px",
      }}
    >
      {slice.map((w, i) => {
        const idx = group * CHUNK + i;
        const isActive = idx === active;
        return (
          <span
            key={idx}
            style={{
              fontFamily: fontStack.sans,
              fontWeight: 800,
              fontSize: 46,
              letterSpacing: -0.5,
              color: isActive ? theme.onAccent : theme.inkSoft,
              background: isActive ? accent : "transparent",
              padding: isActive ? "2px 16px" : "2px 4px",
              borderRadius: 12,
              transform: isActive ? "translateY(-2px)" : "none",
              boxShadow: isActive ? theme.shadowSoft : "none",
              transition: "none",
            }}
          >
            {w.text}
          </span>
        );
      })}
    </div>
  );
};
