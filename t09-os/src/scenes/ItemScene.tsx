import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack } from "../theme";
import { ScreenShot } from "../components/ScreenShot";
import { MechFlow } from "../components/MechFlow";
import { Badge, legalColor } from "../components/Badge";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// One illegal (or "illegal") operating system. Frame supplies the chapter badge,
// caption, verdict and progress rail. LEFT: a REAL desktop screenshot of the OS
// (top) + its animated mechanism diagram (bottom); when no free screenshot exists
// (pirated Windows, Phantom Secure) the mechanism fills the whole panel. RIGHT:
// the big RED/AMBER/GREEN legal-status badge, origin + year, then the sourced specs.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const accent = legalColor(seg.status);
  const specs = seg.specs ?? [];
  const headIn = pop(frame, 6, fps);
  const shot = seg.id ? input.images?.[seg.id] : undefined;
  const mech = seg.mech ?? [];

  return (
    <AbsoluteFill>
      {/* LEFT: screenshot + mechanism (or mechanism full if no screenshot) */}
      <div style={{ position: "absolute", left: 40, top: 36 }}>
        {shot ? (
          <>
            <ScreenShot img={shot} name={seg.name ?? ""} accent={accent} width={1030} height={358} />
            {mech.length ? (
              <div style={{ marginTop: 20, width: 1030, height: 180, background: "#070809", borderRadius: 14, border: `1px solid ${accent}33`, padding: "6px 8px" }}>
                <MechFlow nodes={mech} accent={accent} width={1014} height={168} title="HOW IT WORKS" />
              </div>
            ) : null}
          </>
        ) : (
          <div style={{ width: 1030, height: 558, background: "#070809", borderRadius: 14, border: `1px solid ${accent}44`, padding: 16, display: "flex", flexDirection: "column", justifyContent: "center" }}>
            <div style={{ fontFamily: fontStack.mono, fontSize: 16, color: accent, letterSpacing: 2, margin: "4px 0 14px 10px" }}>⚑ NO PUBLISHABLE SCREENSHOT — HOW IT WORKS</div>
            <MechFlow nodes={mech} accent={accent} width={998} height={300} />
          </div>
        )}
      </div>

      {/* RIGHT: legal badge + origin + specs */}
      <div style={{ position: "absolute", left: 1110, top: 56, width: 770 }}>
        <Badge status={(seg.status as any) ?? "green"} />
        <div style={{ opacity: headIn, transform: `translateY(${(1 - headIn) * 14}px)`, display: "flex", flexWrap: "wrap", alignItems: "center", gap: 12, margin: "20px 0 20px" }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, fontWeight: 700, color: theme.ink, border: `1px solid ${theme.line}`, borderRadius: 8, padding: "5px 13px", letterSpacing: 1 }}>{seg.cat ?? ""}</span>
          <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkFaint, letterSpacing: 1 }}>{seg.launched}</span>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 14 }}>
          {specs.slice(0, 4).map((sp, i) => {
            const s = pop(frame, sp.atFrame, fps);
            if (s < 0.001) return null;
            return (
              <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "12px 16px" }}>
                <div style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
                <div style={{ fontFamily: fontStack.sans, fontSize: 21, fontWeight: 800, color: theme.ink, lineHeight: 1.12 }}>{sp.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
