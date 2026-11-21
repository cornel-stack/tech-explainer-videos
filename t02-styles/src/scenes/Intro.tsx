import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { StylesHero3D } from "./StylesHero3D";
import { Safe3D } from "../components/Safe3D";
import { FEATURES } from "../features";
import { pop, beatAt } from "../lib/anim";

export const Intro: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = (m: string, f = 0) => beatAt(seg.beats, m, f);
  const titleIn = pop(frame, 2, fps);
  const qIn = pop(frame, b("promise", 150), fps);
  const floatY = Math.sin(frame / 28) * 7;
  const titleGlow = 44 + Math.sin(frame / 16) * 30;

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.magenta} />
      {seg.audioFile ? <Audio src={staticFile(seg.audioFile)} /> : null}

      {/* 3D hero behind the title */}
      <AbsoluteFill style={{ top: 120 }}>
        {FEATURES.hero3D ? (
          <Safe3D fallback={<Fallback2D frame={frame} />}>
            <StylesHero3D width={1920} height={840} />
          </Safe3D>
        ) : (
          <Fallback2D frame={frame} />
        )}
      </AbsoluteFill>

      <div style={{ position: "absolute", top: 120, left: 0, right: 0, textAlign: "center", transform: `translateY(${floatY}px) scale(${0.75 + titleIn * 0.25})`, opacity: titleIn }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 26, letterSpacing: 8, color: theme.accents.mint, fontWeight: 700 }}>
          SERIES · EVERY X
        </div>
        <div style={{ fontFamily: fontStack.sans, fontSize: 126, fontWeight: 900, color: theme.ink, letterSpacing: -3, lineHeight: 1, textShadow: `0 0 ${titleGlow}px ${theme.accents.magenta}` }}>
          EVERY API STYLE
        </div>
      </div>

      {/* the framing question */}
      <div style={{ position: "absolute", bottom: 230, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: qIn, transform: `translateY(${(1 - qIn) * 24 + Math.sin(frame / 22) * 5}px)` }}>
        <div style={{ background: theme.paper, border: `1px solid ${theme.accents.magenta}55`, borderRadius: 999, padding: "16px 34px", boxShadow: glow(theme.accents.magenta, 0.4), fontFamily: fontStack.sans, fontWeight: 800, fontSize: 34, color: theme.ink }}>
          one question → the right style
        </div>
      </div>

      <Caption words={seg.words} accent={theme.accents.magenta} />
    </AbsoluteFill>
  );
};

const Fallback2D: React.FC<{ frame: number }> = ({ frame }) => {
  const C = ["#FFC24B", "#B06BFF", "#FF3E7F", "#3DE0B0", "#FF6B4A", "#E8C24A", "#FFC24B", "#B06BFF"];
  return (
    <svg viewBox="0 0 1920 840" style={{ width: "100%", height: "100%" }}>
      {C.map((c, i) => {
        const a = (i / 8) * Math.PI * 2 + frame / 60;
        return <circle key={i} cx={960 + Math.cos(a) * 320} cy={420 + Math.sin(a) * 180} r={34} fill={c} />;
      })}
      <circle cx={960} cy={420} r={70} fill="none" stroke="#FF3E7F" strokeWidth={4} opacity={0.6} />
    </svg>
  );
};
