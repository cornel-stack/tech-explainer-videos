import React from "react";
import {
  AbsoluteFill,
  Audio,
  staticFile,
  useCurrentFrame,
  interpolate,
} from "remotion";
import type { Segment, Source } from "../schema";
import { Backdrop } from "./Backdrop";
import { ChapterBadge } from "./ChapterBadge";
import { SpecStrip } from "./SpecStrip";
import { Caption } from "./Caption";
import { Verdict } from "./Verdict";
import { ProgressRail } from "./ProgressRail";

const VERDICT_SECS = 2.8;

// Wraps a scene with all the persistent chrome and plays the stage audio.
export const Frame: React.FC<{
  stage: Segment;
  sources: Source[];
  steps: { icon: string; accent: string }[];
  index: number; // 0-based
  fps: number;
  hideSpecs?: boolean;
  children: React.ReactNode;
}> = ({ stage, sources, steps, index, fps, hideSpecs, children }) => {
  const frame = useCurrentFrame();
  const accent = stage.accent ?? "#FFC24B";
  const dur = stage.durationInFrames;
  const verdictAt = Math.max(0, dur - Math.round(VERDICT_SECS * fps));
  const showVerdict = frame >= verdictAt;
  const captionFade = interpolate(
    frame,
    [verdictAt - 10, verdictAt],
    [1, 0],
    { extrapolateLeft: "clamp", extrapolateRight: "clamp" },
  );

  return (
    <AbsoluteFill>
      <Backdrop accent={accent} />
      {stage.audioFile ? <Audio src={staticFile(stage.audioFile)} /> : null}

      {/* The scene's own visual lives in the central band. */}
      <AbsoluteFill style={{ top: 150, bottom: 210 }}>{children}</AbsoluteFill>

      <ChapterBadge
        index={index + 1}
        total={steps.length}
        icon={stage.icon ?? "hub"}
        title={stage.name ?? ""}
        accent={accent}
      />
      {hideSpecs ? null : <SpecStrip specs={stage.specs ?? []} sources={sources} accent={accent} />}

      <div style={{ opacity: captionFade }}>
        <Caption words={stage.words} accent={accent} />
      </div>
      {showVerdict && stage.verdict ? (
        <Verdict text={stage.verdict} accent={accent} at={verdictAt} />
      ) : null}

      <ProgressRail
        steps={steps}
        current={index}
        progress={interpolate(frame, [0, dur], [0, 1], {
          extrapolateRight: "clamp",
        })}
        accent={accent}
      />
    </AbsoluteFill>
  );
};
