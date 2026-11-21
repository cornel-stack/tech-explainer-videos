import React from "react";
import { AbsoluteFill, Audio, staticFile, OffthreadVideo, Loop, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// A full-frame Manim interlude (axis / nplus1 / decision) with a title chip and
// word-synced caption. Falls back to a simple titled card if the clip is absent.
export const InterludeScene: React.FC<{ seg: Segment; clip: string; title: string; accent: string }> = ({
  seg,
  clip,
  title,
  accent,
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const clipObj = input.manim?.[clip];
  const titleIn = pop(frame, 4, fps);

  return (
    <AbsoluteFill>
      <Backdrop accent={accent} />
      {seg.audioFile ? <Audio src={staticFile(seg.audioFile)} /> : null}

      {clipObj ? (
        <AbsoluteFill>
          <Loop durationInFrames={Math.max(1, clipObj.durationInFrames)}>
            <OffthreadVideo src={staticFile(clipObj.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </Loop>
        </AbsoluteFill>
      ) : (
        <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
          <div style={{ fontFamily: fontStack.sans, fontSize: 60, fontWeight: 900, color: theme.ink }}>{title}</div>
        </AbsoluteFill>
      )}

      {/* title chip */}
      <div style={{ position: "absolute", top: 64, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: titleIn, transform: `translateY(${(1 - titleIn) * -20 + Math.sin(frame / 22) * 5}px)` }}>
        <div style={{ background: theme.paper, border: `1px solid ${accent}66`, borderRadius: 999, padding: "12px 30px", boxShadow: glow(accent, 0.4), fontFamily: fontStack.sans, fontWeight: 800, fontSize: 32, color: theme.ink }}>
          {title}
        </div>
      </div>

      <Caption words={seg.words} accent={accent} />
    </AbsoluteFill>
  );
};
