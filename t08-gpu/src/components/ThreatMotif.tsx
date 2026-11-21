import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";
import { Icon } from "./Icon";

// Animated "live specimen" panel for items without a dedicated Manim clip: the
// threat's glyph pulsing in its family colour over falling hex streams and a
// sweeping scan line. Keeps native items moving.
const COLS = 14;
const glyphs = "01ABCDEF8#$%&".split("");

export const ThreatMotif: React.FC<{ icon: string; accent: string; label: string; width: number; height: number }> = ({
  icon,
  accent,
  label,
  width,
  height,
}) => {
  const frame = useCurrentFrame();
  const pulse = 1 + Math.sin(frame / 12) * 0.05;
  const scanY = (frame * 3) % (height + 80) - 40;

  return (
    <div style={{ position: "relative", width, height, background: "#070709", borderRadius: 12, border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.25), overflow: "hidden" }}>
      {/* falling hex streams */}
      {Array.from({ length: COLS }).map((_, c) => {
        const x = (c + 0.5) * (width / COLS);
        const speed = 40 + ((c * 37) % 60);
        const offset = (frame * speed + c * 120) % (height + 200);
        return (
          <div key={c} style={{ position: "absolute", left: x - 6, top: offset - 200, display: "flex", flexDirection: "column", gap: 6, opacity: 0.18, color: accent, fontFamily: fontStack.mono, fontSize: 18 }}>
            {Array.from({ length: 9 }).map((__, r) => (
              <span key={r}>{glyphs[(c * 7 + r * 13 + Math.floor(frame / 6)) % glyphs.length]}</span>
            ))}
          </div>
        );
      })}

      {/* center glyph */}
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        <div style={{ transform: `scale(${pulse})`, filter: `drop-shadow(0 0 26px ${accent})` }}>
          <Icon name={icon} size={Math.min(width, height) * 0.42} color={accent} strokeWidth={5} />
        </div>
      </div>

      {/* scan line */}
      <div style={{ position: "absolute", left: 0, right: 0, top: scanY, height: 2, background: `linear-gradient(90deg, transparent, ${accent}, transparent)`, opacity: 0.6 }} />

      {/* label */}
      <div style={{ position: "absolute", left: 16, bottom: 14, fontFamily: fontStack.mono, fontSize: 18, color: theme.inkSoft, letterSpacing: 2 }}>
        ◉ LIVE SPECIMEN · {label.toUpperCase()}
      </div>
    </div>
  );
};
