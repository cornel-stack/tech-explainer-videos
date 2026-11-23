import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack } from "../theme";
import { WinChrome } from "../components/WinChrome";
import { Badge, repColor } from "../components/Badge";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// One version of Windows. Frame supplies the chapter badge, caption, verdict and
// progress rail. LEFT: an original drawn homage of that era's desktop (WinChrome).
// RIGHT: history's reputation badge (Loved / Meh / Hated), the release year, and
// the sourced spec grid, each popping on the frame its number is spoken.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = seg.accent ?? repColor(seg.status);
  const specs = seg.specs ?? [];
  const headIn = pop(frame, 6, fps);
  const skin = (seg.skin as any) ?? "flat";

  return (
    <AbsoluteFill>
      {/* LEFT: the drawn desktop homage */}
      <div style={{ position: "absolute", left: 40, top: 40 }}>
        <WinChrome skin={skin} name={seg.name ?? ""} accent={accent} width={1030} height={560} />
      </div>

      {/* RIGHT: reputation badge + year + specs */}
      <div style={{ position: "absolute", left: 1110, top: 56, width: 770 }}>
        <Badge status={(seg.status as any) ?? "meh"} />
        <div style={{ opacity: headIn, transform: `translateY(${(1 - headIn) * 14}px)`, display: "flex", flexWrap: "wrap", alignItems: "center", gap: 12, margin: "20px 0 20px" }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, fontWeight: 700, color: accent, border: `1px solid ${accent}`, borderRadius: 8, padding: "5px 13px", letterSpacing: 1 }}>{seg.cat ?? ""}</span>
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
