import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Reveals text character-by-character from frame `at`, with a blinking caret.
export const Typewriter: React.FC<{
  text: string;
  at: number;
  cps?: number; // characters per second
  style?: React.CSSProperties;
  caret?: boolean;
  caretColor?: string;
}> = ({ text, at, cps = 32, style, caret = true, caretColor = "#EDE7DB" }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const elapsed = Math.max(0, frame - at);
  const shown = Math.min(text.length, Math.floor((elapsed / fps) * cps));
  const done = shown >= text.length;
  const blink = Math.floor(frame / 16) % 2 === 0;
  return (
    <span style={style}>
      {text.slice(0, shown)}
      {caret && (!done || blink) && frame >= at ? (
        <span style={{ color: caretColor, opacity: done && !blink ? 0 : 1 }}>▋</span>
      ) : null}
    </span>
  );
};
