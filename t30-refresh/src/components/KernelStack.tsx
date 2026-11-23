import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";

// The channel's recurring OS schematic: user space → (this OS's distinctive
// layer) → system calls → kernel/ring 0 → hardware, with the distinctive layer
// lit in the family colour and a data packet flowing down/up on a loop.
export const KernelStack: React.FC<{ highlight: string; accent: string; width?: number; height?: number }> = ({
  highlight,
  accent,
  width = 1030,
  height = 460,
}) => {
  const frame = useCurrentFrame();
  const layers = [
    { label: "USER SPACE · your apps", lit: false },
    { label: highlight || "runtime", lit: true },
    { label: "SYSTEM CALLS", lit: false, thin: true },
    { label: "KERNEL · ring 0", lit: false, kernel: true },
    { label: "HARDWARE · CPU · RAM · disk", lit: false },
  ];
  const n = layers.length;
  const gap = 14;
  const lh = (height - gap * (n - 1)) / n;

  // packet goes top→bottom then bottom→top, looping
  const period = 150;
  const p = (frame % period) / period;
  const tt = p < 0.5 ? p / 0.5 : 1 - (p - 0.5) / 0.5; // 0..1..0
  const packetY = tt * (height - 16) + 8;

  return (
    <div style={{ position: "relative", width, height }}>
      {layers.map((L, i) => {
        const top = i * (lh + gap);
        const h = L.thin ? lh * 0.5 : lh;
        const pulse = L.lit ? 0.5 + Math.sin(frame / 10) * 0.25 : 0;
        const col = L.lit ? accent : L.kernel ? theme.accents.magenta : theme.inkSoft;
        return (
          <div
            key={i}
            style={{
              position: "absolute",
              left: 60,
              right: 0,
              top: top + (L.thin ? lh * 0.25 : 0),
              height: h,
              borderRadius: 12,
              background: L.lit ? `${accent}1c` : theme.paper,
              border: `1.5px solid ${L.lit ? accent : theme.line}`,
              boxShadow: L.lit ? `0 0 ${20 + pulse * 30}px ${accent}66` : "none",
              display: "flex",
              alignItems: "center",
              paddingLeft: 26,
              gap: 14,
            }}
          >
            {L.lit ? <span style={{ color: accent, fontSize: 22 }}>★</span> : null}
            <span
              style={{
                fontFamily: L.thin ? fontStack.mono : fontStack.sans,
                fontWeight: L.lit ? 800 : 600,
                fontSize: L.thin ? 20 : 26,
                color: L.lit ? theme.ink : col,
                letterSpacing: L.thin ? 2 : 0,
              }}
            >
              {L.label}
            </span>
          </div>
        );
      })}
      {/* data-flow packet on the left rail */}
      <div style={{ position: "absolute", left: 24, top: 0, bottom: 0, width: 4, background: theme.line, borderRadius: 2 }} />
      <div style={{ position: "absolute", left: 14, top: packetY - 9, width: 24, height: 24, borderRadius: 999, background: accent, boxShadow: `0 0 16px ${accent}` }} />
    </div>
  );
};
