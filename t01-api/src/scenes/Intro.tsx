import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { Hero3D } from "./Hero3D";
import { Safe3D } from "../components/Safe3D";
import { FEATURES } from "../features";
import { useInput } from "../lib/ctx";
import { pop, beatAt } from "../lib/anim";

export const Intro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const intro = input.intro;
  const b = (m: string, f = 0) => beatAt(intro.beats, m, f);

  const titleIn = pop(frame, 2, fps);
  const nameIn = pop(frame, b("nameReveal", 120), fps);

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.magenta} />
      {intro.audioFile ? <Audio src={staticFile(intro.audioFile)} /> : null}

      {/* title */}
      <div
        style={{
          position: "absolute",
          top: 108,
          left: 0,
          right: 0,
          textAlign: "center",
          transform: `scale(${0.72 + titleIn * 0.28})`,
          opacity: titleIn,
        }}
      >
        <div style={{ fontFamily: fontStack.mono, fontSize: 26, letterSpacing: 8, color: theme.accents.magenta, fontWeight: 700 }}>
          HOW IT WORKS
        </div>
        <div
          style={{
            fontFamily: fontStack.sans,
            fontSize: 132,
            fontWeight: 900,
            color: theme.ink,
            letterSpacing: -3,
            lineHeight: 1,
            textShadow: `0 0 50px ${theme.accents.magenta}55`,
          }}
        >
          What is an API?
        </div>
      </div>

      {/* 3D hero */}
      <div style={{ position: "absolute", top: 320, left: 0, right: 0, height: 470, display: "grid", placeItems: "center" }}>
        {FEATURES.hero3D ? (
          <Safe3D fallback={<Fallback2D frame={frame} />}>
            <Hero3D width={1500} height={460} />
          </Safe3D>
        ) : (
          <Fallback2D frame={frame} />
        )}
        {/* "this is an API call" */}
        <div
          style={{
            position: "absolute",
            bottom: -6,
            transform: `scale(${nameIn})`,
            opacity: nameIn,
            background: theme.paper,
            color: theme.ink,
            padding: "14px 30px",
            borderRadius: 999,
            border: `1px solid ${theme.accents.mint}66`,
            fontFamily: fontStack.sans,
            fontWeight: 800,
            fontSize: 32,
            boxShadow: glow(theme.accents.mint, 0.5),
          }}
        >
          this is <span style={{ color: theme.accents.mint }}>an API call</span>
        </div>
      </div>

      <Caption words={intro.words} accent={theme.accents.magenta} />
    </AbsoluteFill>
  );
};

const Fallback2D: React.FC<{ frame: number }> = ({ frame }) => {
  const t = (Math.sin(frame / 30) + 1) / 2;
  return (
    <svg viewBox="0 0 1500 460" style={{ width: 1500 }}>
      <rect x={200} y={170} width={160} height={160} rx={24} fill={theme.client} />
      <rect x={1140} y={150} width={180} height={200} rx={24} fill={theme.server} />
      <circle cx={360 + t * 780} cy={250} r={26} fill={theme.accents.mint} />
    </svg>
  );
};
