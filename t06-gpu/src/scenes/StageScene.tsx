import React from "react";
import { AbsoluteFill, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { ParallelGrid } from "../components/ParallelGrid";
import { ScreenCard } from "../components/ScreenCard";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// One GPU stage. Frame supplies badge/caption/verdict/rail (specs hidden — shown
// here). LEFT: the diagram (a Manim clip, or the native parallel-core grid).
// RIGHT: an optional real silicon/data-centre image + a compact spec grid.
export const StageScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const accent = seg.accent ?? theme.accents.mint;
  const clip = seg.manim ? input.manim?.[seg.manim] : undefined;
  const hasImg = Boolean(seg.image && input.images?.[seg.image]);
  const specs = seg.specs ?? [];

  return (
    <AbsoluteFill>
      {/* LEFT diagram */}
      <div style={{ position: "absolute", left: 40, top: 150 }}>
        {clip ? (
          <div style={{ width: 1030, height: 505, borderRadius: 14, overflow: "hidden", border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.25) }}>
            <Loop durationInFrames={Math.max(1, clip.durationInFrames)}>
              <OffthreadVideo src={staticFile(clip.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </Loop>
          </div>
        ) : (
          <ParallelGrid accent={accent} width={1030} height={505} />
        )}
      </div>

      {/* RIGHT: image (optional) + specs */}
      <div style={{ position: "absolute", left: 1110, top: 150 }}>
        {hasImg ? (
          <ScreenCard caseKey={seg.image} caseName={seg.name ?? ""} header="IN SILICON" accent={accent} width={770} height={330} />
        ) : (
          <div style={{ width: 770, height: 330, borderRadius: 12, overflow: "hidden" }}>
            <ParallelGrid accent={accent} width={770} height={330} label="SAME WORKER · ×10,000" />
          </div>
        )}
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 14, width: 770 }}>
          {specs.slice(0, 4).map((sp, i) => {
            const s = pop(frame, sp.atFrame, fps);
            if (s < 0.001) return null;
            return (
              <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "9px 14px" }}>
                <div style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
                <div style={{ fontFamily: fontStack.sans, fontSize: 21, fontWeight: 800, color: theme.ink, lineHeight: 1.1 }}>{sp.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
