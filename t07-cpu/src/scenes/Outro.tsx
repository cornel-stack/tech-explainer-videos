import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { useInput } from "../lib/ctx";
import { pop, beatAt } from "../lib/anim";

export const Outro: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const b = (m: string, f = 0) => beatAt(seg.beats, m, f);
  const bg = input.manim?.decoder;

  const qIn = pop(frame, 8, fps);
  const nextIn = pop(frame, b("next", 150), fps);
  const subIn = pop(frame, b("cta", 220), fps);
  const subPulse = 1 + Math.sin(frame / 9) * 0.03 * (subIn > 0.5 ? 1 : 0);

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.amber} />
      {seg.audioFile ? <Audio src={staticFile(seg.audioFile)} /> : null}
      {bg ? (
        <AbsoluteFill style={{ opacity: 0.2 }}>
          <Loop durationInFrames={Math.max(1, bg.durationInFrames)}>
            <OffthreadVideo src={staticFile(bg.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
          </Loop>
        </AbsoluteFill>
      ) : null}

      <div style={{ position: "absolute", top: 120, left: 0, right: 0, textAlign: "center", opacity: qIn }}>
        <div style={{ fontFamily: fontStack.sans, fontSize: 54, fontWeight: 900, color: theme.ink, letterSpacing: -2, textShadow: `0 0 40px ${theme.bg}` }}>
          two rules: <span style={{ color: theme.accents.amber }}>decode the name</span>, and generation beats tier.
        </div>
      </div>

      <div style={{ position: "absolute", top: 320, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: nextIn, transform: `translateY(${(1 - nextIn) * 24}px)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, background: theme.paper, color: theme.ink, borderRadius: 16, padding: "20px 32px", border: `1px solid ${theme.accents.coral}55`, boxShadow: glow(theme.accents.coral, 0.4) }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 20, color: theme.accents.coral }}>NEXT ▸</span>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40 }}>{seg.nextVideo}</span>
        </div>
      </div>

      <div style={{ position: "absolute", top: 470, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 14, opacity: subIn, transform: `scale(${(0.8 + subIn * 0.2) * subPulse})` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, background: theme.accents.amber, color: theme.onAccent, borderRadius: 999, padding: "22px 46px", boxShadow: glow(theme.accents.amber, 0.85) }}>
          <span style={{ width: 0, height: 0, borderTop: "16px solid transparent", borderBottom: "16px solid transparent", borderLeft: `26px solid ${theme.onAccent}` }} />
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 52, letterSpacing: 1 }}>SUBSCRIBE</span>
        </div>
        <span style={{ fontFamily: fontStack.sans, fontSize: 28, fontWeight: 700, color: theme.ink }}>'Every AMD CPU' is next 🙏</span>
      </div>

      <div style={{ position: "absolute", bottom: 150, left: 72, right: 72, display: "flex", flexWrap: "wrap", gap: "6px 18px", justifyContent: "center" }}>
        {input.sources.map((src) => (
          <span key={src.id} style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>↳ {src.label}</span>
        ))}
      </div>

      <Caption words={seg.words} accent={theme.accents.amber} />
    </AbsoluteFill>
  );
};
