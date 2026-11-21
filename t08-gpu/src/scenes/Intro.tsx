import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { ChipHero3D } from "./ChipHero3D";
import { Safe3D } from "../components/Safe3D";
import { FEATURES } from "../features";
import { useInput } from "../lib/ctx";
import { pop, beatAt } from "../lib/anim";

export const Intro: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const bg = seg.manim ? input.manim?.[seg.manim] : undefined;
  const b = (m: string, f = 0) => beatAt(seg.beats, m, f);
  const titleIn = pop(frame, 2, fps);
  const subIn = pop(frame, b("dec", 70), fps);
  const titleGlow = 38 + Math.sin(frame / 16) * 24;

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.amber} />
      {seg.audioFile ? <Audio src={staticFile(seg.audioFile)} /> : null}

      {bg ? (
        <AbsoluteFill style={{ opacity: 0.24 }}>
          <Loop durationInFrames={Math.max(1, bg.durationInFrames)}>
            <OffthreadVideo src={staticFile(bg.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </Loop>
        </AbsoluteFill>
      ) : null}

      <AbsoluteFill style={{ top: 150 }}>
        {FEATURES.hero3D ? (
          <Safe3D fallback={<div />}>
            <ChipHero3D width={1920} height={720} />
          </Safe3D>
        ) : null}
      </AbsoluteFill>

      <div style={{ position: "absolute", top: 120, left: 0, right: 0, textAlign: "center", opacity: titleIn, transform: `scale(${0.82 + titleIn * 0.18})` }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 24, letterSpacing: 10, color: theme.accents.amber, fontWeight: 700 }}>◢ SERIES · EVERY X</div>
        <div style={{ fontFamily: fontStack.sans, fontSize: 150, fontWeight: 900, color: theme.ink, letterSpacing: -3, lineHeight: 1, textShadow: `0 0 ${titleGlow}px ${theme.accents.amber}aa` }}>
          EVERY GPU
        </div>
      </div>

      <div style={{ position: "absolute", bottom: 232, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: subIn, transform: `translateY(${(1 - subIn) * 22 + Math.sin(frame / 22) * 4}px)` }}>
        <div style={{ background: theme.paper, border: `1px solid ${theme.accents.amber}66`, borderRadius: 8, padding: "14px 30px", boxShadow: glow(theme.accents.amber, 0.4), fontFamily: fontStack.mono, fontWeight: 700, fontSize: 30, color: theme.ink, letterSpacing: 1 }}>
          decode every name · <span style={{ color: theme.accents.mint }}>pick the right card</span>
        </div>
      </div>

      <Caption words={seg.words} accent={theme.accents.amber} />
    </AbsoluteFill>
  );
};
