import React from "react";
import { AbsoluteFill, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow, tierColor } from "../theme";
import { DieTiles } from "../components/DieTiles";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// One Intel CPU. Frame supplies badge/caption/verdict/rail (specs hidden). LEFT:
// the die schematic (or a Manim clip for binning, or a feature list for vPro).
// RIGHT: launch/tier header + compact spec grid.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const accent = tierColor(seg.tier) ?? seg.accent ?? theme.accents.amber;
  const clip = seg.manim ? input.manim?.[seg.manim] : undefined;
  const specs = seg.specs ?? [];
  const headIn = pop(frame, 6, fps);

  return (
    <AbsoluteFill>
      {/* LEFT visual */}
      <div style={{ position: "absolute", left: 40, top: 150 }}>
        {clip ? (
          <div style={{ width: 1030, height: 505, borderRadius: 14, overflow: "hidden", border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.25) }}>
            <Loop durationInFrames={Math.max(1, clip.durationInFrames)}>
              <OffthreadVideo src={staticFile(clip.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </Loop>
          </div>
        ) : seg.features ? (
          <div style={{ width: 1030, height: 505, background: "#090A0D", borderRadius: 14, border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.22), padding: 40, display: "flex", flexDirection: "column", gap: 22, justifyContent: "center" }}>
            <div style={{ fontFamily: fontStack.mono, fontSize: 18, color: accent, letterSpacing: 2 }}>◆ NOT A CHIP — A FEATURE PLATFORM</div>
            {seg.features.map((f, i) => {
              const s = pop(frame, 20 + i * 18, fps);
              return (
                <div key={i} style={{ opacity: s, transform: `translateX(${(1 - s) * 30}px)`, display: "flex", alignItems: "center", gap: 18 }}>
                  <div style={{ width: 44, height: 44, borderRadius: 10, background: accent, color: theme.onAccent, display: "grid", placeItems: "center", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 22 }}>{i + 1}</div>
                  <span style={{ fontFamily: fontStack.sans, fontSize: 32, fontWeight: 700, color: theme.ink }}>{f}</span>
                </div>
              );
            })}
          </div>
        ) : (
          <DieTiles die={seg.die ?? {}} accent={accent} width={1030} height={505} />
        )}
      </div>

      {/* RIGHT header + specs */}
      <div style={{ position: "absolute", left: 1110, top: 150, width: 770 }}>
        <div style={{ opacity: headIn, transform: `translateY(${(1 - headIn) * 14}px)`, display: "flex", alignItems: "center", gap: 14, marginBottom: 18 }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkFaint, letterSpacing: 1 }}>SINCE {seg.launched}</span>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, fontWeight: 700, color: accent, border: `1px solid ${accent}`, borderRadius: 8, padding: "4px 12px", letterSpacing: 1, textTransform: "uppercase" }}>{seg.tier}</span>
        </div>
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
          {specs.slice(0, 4).map((sp, i) => {
            const s = pop(frame, sp.atFrame, fps);
            if (s < 0.001) return null;
            return (
              <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "10px 14px" }}>
                <div style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
                <div style={{ fontFamily: fontStack.sans, fontSize: 22, fontWeight: 800, color: theme.ink, lineHeight: 1.1 }}>{sp.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
