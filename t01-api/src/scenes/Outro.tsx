import React from "react";
import { AbsoluteFill, Audio, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";
import { Backdrop } from "../components/Backdrop";
import { Caption } from "../components/Caption";
import { Icon } from "../components/Icon";
import { useInput } from "../lib/ctx";
import { pop, beatAt } from "../lib/anim";

export const Outro: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const outro = input.outro;
  const b = (m: string, f = 0) => beatAt(outro.beats, m, f);

  const recap = [
    { mark: "recapMessenger", word: "a messenger", icon: "messenger", color: theme.accents.amber },
    { mark: "recapMenu", word: "a menu", icon: "doors", color: theme.accents.coral },
    { mark: "recapContract", word: "a contract", icon: "check", color: theme.accents.mint },
  ];
  const nextIn = pop(frame, b("recapContract", 60) + 20, fps);
  const subIn = pop(frame, b("cta", 150), fps);
  const subPulse = 1 + Math.sin(frame / 9) * 0.03 * (subIn > 0.5 ? 1 : 0);

  return (
    <AbsoluteFill>
      <Backdrop accent={theme.accents.magenta} />
      {outro.audioFile ? <Audio src={staticFile(outro.audioFile)} /> : null}

      <div style={{ position: "absolute", top: 96, left: 0, right: 0, textAlign: "center" }}>
        <div style={{ fontFamily: fontStack.sans, fontSize: 60, fontWeight: 900, color: theme.ink, letterSpacing: -2 }}>
          An API is…
        </div>
      </div>

      {/* recap chips */}
      <div style={{ position: "absolute", top: 220, left: 0, right: 0, display: "flex", justifyContent: "center", gap: 22 }}>
        {recap.map((r) => {
          const s = pop(frame, b(r.mark, 20), fps);
          if (s < 0.001) return null;
          return (
            <div
              key={r.mark}
              style={{
                opacity: s,
                transform: `scale(${s})`,
                display: "flex",
                alignItems: "center",
                gap: 14,
                background: theme.paper,
                borderRadius: 999,
                boxShadow: glow(r.color, 0.4),
                border: `1px solid ${r.color}55`,
                padding: "16px 28px",
              }}
            >
              <Icon name={r.icon} size={36} color={r.color} />
              <span style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 38, color: theme.ink }}>{r.word}</span>
            </div>
          );
        })}
      </div>

      {/* next video card */}
      <div
        style={{
          position: "absolute",
          top: 380,
          left: 0,
          right: 0,
          display: "flex",
          justifyContent: "center",
          opacity: nextIn,
          transform: `translateY(${(1 - nextIn) * 26}px)`,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            background: theme.paper,
            color: theme.ink,
            borderRadius: 22,
            padding: "20px 32px",
            border: `1px solid ${theme.accents.violet}55`,
            boxShadow: glow(theme.accents.violet, 0.35),
          }}
        >
          <span style={{ fontFamily: fontStack.mono, fontSize: 20, color: theme.accents.violet }}>NEXT →</span>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40 }}>{outro.nextVideo}</span>
        </div>
      </div>

      {/* SUBSCRIBE CTA */}
      <div
        style={{
          position: "absolute",
          top: 500,
          left: 0,
          right: 0,
          display: "flex",
          flexDirection: "column",
          alignItems: "center",
          gap: 14,
          opacity: subIn,
          transform: `scale(${(0.8 + subIn * 0.2) * subPulse})`,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 18,
            background: theme.accents.magenta,
            color: theme.onAccent,
            borderRadius: 999,
            padding: "22px 46px",
            boxShadow: glow(theme.accents.magenta, 0.8),
          }}
        >
          <span style={{ width: 0, height: 0, borderTop: "16px solid transparent", borderBottom: "16px solid transparent", borderLeft: `26px solid ${theme.onAccent}` }} />
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 52, letterSpacing: 1 }}>SUBSCRIBE</span>
        </div>
        <span style={{ fontFamily: fontStack.sans, fontSize: 28, fontWeight: 700, color: theme.inkSoft }}>
          it genuinely helps the channel 🙏
        </span>
      </div>

      {/* sources footer */}
      <div
        style={{
          position: "absolute",
          bottom: 150,
          left: 72,
          right: 72,
          display: "flex",
          flexWrap: "wrap",
          gap: "6px 18px",
          justifyContent: "center",
        }}
      >
        {input.sources.map((src) => (
          <span key={src.id} style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>
            ↳ {src.label}
          </span>
        ))}
      </div>

      <Caption words={outro.words} accent={theme.accents.magenta} />
    </AbsoluteFill>
  );
};
