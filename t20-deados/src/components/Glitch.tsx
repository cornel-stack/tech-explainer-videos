import React from "react";
import { useCurrentFrame } from "remotion";

// Cyber glitch text: two chromatic-offset copies (red/green) that jitter, with
// occasional slice displacement. Pseudo-random from frame (deterministic).
const rand = (n: number) => {
  const x = Math.sin(n * 12.9898) * 43758.5453;
  return x - Math.floor(x);
};

export const GlitchText: React.FC<{
  text: string;
  size: number;
  color?: string;
  weight?: number;
  intensity?: number;
  style?: React.CSSProperties;
}> = ({ text, size, color = "#E6E4DE", weight = 900, intensity = 1, style }) => {
  const frame = useCurrentFrame();
  const burst = rand(Math.floor(frame / 5)) > 0.72 ? 1 : 0.25; // occasional spikes
  const dx = (rand(frame) - 0.5) * 6 * intensity * burst;
  const base: React.CSSProperties = {
    fontFamily: "Inter, sans-serif",
    fontWeight: weight,
    fontSize: size,
    letterSpacing: -1,
    lineHeight: 1,
    whiteSpace: "pre",
  };
  return (
    <div style={{ position: "relative", display: "inline-block", ...style }}>
      <span style={{ ...base, position: "absolute", left: dx, top: 0, color: "#FF3B4E", opacity: 0.55 * burst, mixBlendMode: "screen" }}>{text}</span>
      <span style={{ ...base, position: "absolute", left: -dx, top: 0, color: "#35FF9E", opacity: 0.55 * burst, mixBlendMode: "screen" }}>{text}</span>
      <span style={{ ...base, position: "relative", color }}>{text}</span>
    </div>
  );
};
