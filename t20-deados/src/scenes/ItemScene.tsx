import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack } from "../theme";
import { Tombstone } from "../components/Tombstone";
import { pop } from "../lib/anim";

// One dead OS. Frame supplies the chapter badge, caption, verdict and progress rail.
// LEFT: the drawn memorial — a headstone (R.I.P. + born–died + epitaph) beside the OS's
// device, its screen flickering then dying. RIGHT: the cause-of-death tag + sourced specs.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = seg.accent ?? theme.accents.violet;
  const specs = seg.specs ?? [];
  const headIn = pop(frame, 6, fps);

  return (
    <AbsoluteFill>
      {/* LEFT: the drawn memorial */}
      <div style={{ position: "absolute", left: 40, top: 40 }}>
        <Tombstone grave={seg.grave ?? {}} name={seg.name ?? ""} accent={accent} width={1030} height={560} />
      </div>

      {/* RIGHT: use-case tag + specs */}
      <div style={{ position: "absolute", left: 1110, top: 60, width: 770 }}>
        <div style={{ opacity: headIn, transform: `translateY(${(1 - headIn) * 14}px)`, display: "flex", flexWrap: "wrap", alignItems: "center", gap: 12, marginBottom: 22 }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, fontWeight: 700, color: accent, border: `1px solid ${accent}`, borderRadius: 8, padding: "5px 13px", letterSpacing: 1, textTransform: "uppercase" }}>{seg.cat ?? ""}</span>
          <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkFaint, letterSpacing: 1 }}>{seg.launched}</span>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {specs.slice(0, 4).map((sp, i) => {
            const s = pop(frame, sp.atFrame, fps);
            if (s < 0.001) return null;
            return (
              <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "12px 16px" }}>
                <div style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
                <div style={{ fontFamily: fontStack.sans, fontSize: 22, fontWeight: 800, color: theme.ink, lineHeight: 1.12 }}>{sp.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
