import React from "react";
import { AbsoluteFill, OffthreadVideo, Loop, staticFile, useCurrentFrame } from "remotion";
import type { Segment } from "../schema";
import { glow, phaseColor } from "../theme";
import { TimelineBar } from "../components/TimelineBar";
import { StepDetail } from "../components/StepDetail";
import { useInput } from "../lib/ctx";

// One boot/kernel stage. Frame supplies badge/spec-strip/caption/verdict/rail.
// Here: the running ms telemetry + hand-off chain on top, and the stage's main
// diagram below (a Manim clip, or the native StepDetail flow).
export const StageScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const input = useInput();
  const accent = seg.accent ?? phaseColor(seg.phase);
  const clip = seg.manim ? input.manim?.[seg.manim] : undefined;
  const progress = seg.durationInFrames ? frame / seg.durationInFrames : 0;

  return (
    <AbsoluteFill>
      {/* telemetry + chain */}
      <div style={{ position: "absolute", left: 40, top: 2, width: 1370 }}>
        <TimelineBar phase={seg.phase} msStart={seg.msStart} msEnd={seg.msEnd} chainStep={seg.chainStep ?? 5} accent={accent} progress={progress} />
      </div>

      {/* main diagram */}
      <div style={{ position: "absolute", left: 40, top: 212 }}>
        {clip ? (
          <div style={{ width: 1030, height: 505, borderRadius: 14, overflow: "hidden", border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.25) }}>
            <Loop durationInFrames={Math.max(1, clip.durationInFrames)}>
              <OffthreadVideo src={staticFile(clip.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </Loop>
          </div>
        ) : (
          <StepDetail steps={seg.stepDetail ?? []} icon={seg.icon ?? "server"} accent={accent} width={1030} height={505} />
        )}
      </div>
    </AbsoluteFill>
  );
};
