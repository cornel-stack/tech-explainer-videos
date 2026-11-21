import React from "react";
import { AbsoluteFill, Audio, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { useInput } from "../lib/ctx";
import { pop, beatAt } from "../lib/anim";

// Shutdown is the boot in reverse — a tidy mirror recap, then subscribe.
const STEPS = ["SIGTERM — ask to stop", "SIGKILL — force the rest", "flush to disk", "unmount drives", "cut power"];

export const Outro: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const b = (m: string, f = 0) => beatAt(seg.beats, m, f);
  const bg = input.manim?.bootchain;

  const shutIn = pop(frame, b("shut", 10), fps);
  const nextIn = pop(frame, b("next", 150), fps);
  const subIn = pop(frame, b("cta", 220), fps);
  const subPulse = 1 + Math.sin(frame / 9) * 0.03 * (subIn > 0.5 ? 1 : 0);

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.coral} />
      {seg.audioFile ? <Audio src={staticFile(seg.audioFile)} /> : null}
      {bg ? (
        <AbsoluteFill style={{ opacity: 0.18 }}>
          <Loop durationInFrames={Math.max(1, bg.durationInFrames)}>
            <OffthreadVideo src={staticFile(bg.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover", transform: "scaleY(-1)" }} />
          </Loop>
        </AbsoluteFill>
      ) : null}

      <div style={{ position: "absolute", top: 70, left: 0, right: 0, textAlign: "center", opacity: shutIn }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 24, letterSpacing: 6, color: theme.accents.coral, fontWeight: 700 }}>▸ SHUTDOWN — THE BOOT IN REVERSE</div>
      </div>

      {/* reverse chain */}
      <div style={{ position: "absolute", top: 150, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 10, flexWrap: "wrap", padding: "0 120px" }}>
        {STEPS.map((s, i) => {
          const si = pop(frame, b("shut", 10) + i * 12, fps);
          if (si < 0.001) return null;
          return (
            <div key={i} style={{ opacity: si, transform: `translateY(${(1 - si) * 16}px)`, display: "flex", alignItems: "center", gap: 10, background: theme.paper, border: `1px solid ${theme.accents.coral}44`, borderRadius: 10, padding: "12px 20px", fontFamily: fontStack.mono, fontSize: 22, color: theme.ink }}>
              <span style={{ color: theme.accents.coral }}>{i + 1}</span> {s}
            </div>
          );
        })}
      </div>

      <div style={{ position: "absolute", top: 320, left: 0, right: 0, textAlign: "center", opacity: nextIn }}>
        <div style={{ fontFamily: fontStack.sans, fontSize: 48, fontWeight: 900, color: theme.ink }}>{seg.question}</div>
      </div>

      <div style={{ position: "absolute", top: 420, left: 0, right: 0, display: "flex", justifyContent: "center", opacity: nextIn, transform: `translateY(${(1 - nextIn) * 22}px)` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, background: theme.paper, color: theme.ink, borderRadius: 16, padding: "18px 30px", border: `1px solid ${theme.accents.violet}55`, boxShadow: glow(theme.accents.violet, 0.4) }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 20, color: theme.accents.violet }}>NEXT ▸</span>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38 }}>{seg.nextVideo}</span>
        </div>
      </div>

      <div style={{ position: "absolute", top: 540, left: 0, right: 0, display: "flex", flexDirection: "column", alignItems: "center", gap: 12, opacity: subIn, transform: `scale(${(0.8 + subIn * 0.2) * subPulse})` }}>
        <div style={{ display: "flex", alignItems: "center", gap: 18, background: theme.accents.amber, color: theme.onAccent, borderRadius: 999, padding: "20px 44px", boxShadow: glow(theme.accents.amber, 0.85) }}>
          <span style={{ width: 0, height: 0, borderTop: "16px solid transparent", borderBottom: "16px solid transparent", borderLeft: `26px solid ${theme.onAccent}` }} />
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 50, letterSpacing: 1 }}>SUBSCRIBE</span>
        </div>
        <span style={{ fontFamily: fontStack.sans, fontSize: 26, fontWeight: 700, color: theme.ink }}>we take apart one black box a week 🙏</span>
      </div>

      <div style={{ position: "absolute", bottom: 150, left: 72, right: 72, display: "flex", flexWrap: "wrap", gap: "6px 18px", justifyContent: "center" }}>
        {input.sources.map((src) => (
          <span key={src.id} style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>↳ {src.label}</span>
        ))}
      </div>

      <Caption words={seg.words} accent={theme.accents.coral} />
    </AbsoluteFill>
  );
};
