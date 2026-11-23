import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";
import { Icon } from "./Icon";

// The main visual for boot stages without a dedicated Manim clip (kernel / init
// / user space): the stage glyph plus its internal sub-steps, which light up in
// a continuous loop so the stage always reads as "in progress".
export const StepDetail: React.FC<{ steps: string[]; icon: string; accent: string; width?: number; height?: number }> = ({
  steps,
  icon,
  accent,
  width = 1010,
  height = 505,
}) => {
  const frame = useCurrentFrame();
  const n = Math.max(1, steps.length);
  const period = n * 50;
  const active = Math.floor((frame % period) / 50) % n;
  const pulse = 1 + Math.sin(frame / 10) * 0.05;

  return (
    <div style={{ position: "relative", width, height, background: "#0A0A0E", borderRadius: 14, border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.22), overflow: "hidden", display: "flex", alignItems: "center" }}>
      {/* big stage glyph */}
      <div style={{ width: height, height, display: "grid", placeItems: "center", flex: "none" }}>
        <div style={{ transform: `scale(${pulse})`, filter: `drop-shadow(0 0 30px ${accent})` }}>
          <Icon name={icon} size={height * 0.42} color={accent} strokeWidth={5} />
        </div>
      </div>

      {/* sub-steps */}
      <div style={{ flex: 1, display: "flex", flexDirection: "column", gap: 20, paddingRight: 48 }}>
        {steps.map((s, i) => {
          const on = i === active;
          const done = i < active;
          return (
            <div key={i} style={{ display: "flex", alignItems: "center", gap: 18, opacity: on ? 1 : done ? 0.8 : 0.4, transform: on ? "translateX(6px)" : "none" }}>
              <div style={{ width: 46, height: 46, borderRadius: 10, display: "grid", placeItems: "center", background: on ? accent : theme.paper, border: `1.5px solid ${accent}`, color: on ? theme.onAccent : accent, fontFamily: fontStack.mono, fontWeight: 700, fontSize: 22, boxShadow: on ? `0 0 18px ${accent}` : "none" }}>
                {i + 1}
              </div>
              <span style={{ fontFamily: fontStack.sans, fontSize: 34, fontWeight: on ? 800 : 600, color: on ? theme.ink : theme.inkSoft }}>{s}</span>
            </div>
          );
        })}
      </div>
    </div>
  );
};
