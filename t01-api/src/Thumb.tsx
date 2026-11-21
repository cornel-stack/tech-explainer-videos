import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";
import { Machine } from "./characters/Machine";

// Shared dark backdrop with a big accent glow in one corner.
const ThumbBg: React.FC<{ accent: string; corner?: "tr" | "tl" }> = ({ accent, corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill
      style={{
        background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${accent}33, transparent 60%)`,
      }}
    />
    <AbsoluteFill
      style={{
        backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`,
        backgroundSize: "46px 46px",
        opacity: 0.5,
      }}
    />
  </>
);

// ── Thumbnail A — the bold question + "finally explained" + the cast ─────────
export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <ThumbBg accent={theme.accents.magenta} corner="tr" />

    {/* giant question "?" ghost */}
    <div
      style={{
        position: "absolute",
        right: -40,
        top: -120,
        fontFamily: fontStack.sans,
        fontSize: 1100,
        fontWeight: 900,
        color: theme.accents.magenta,
        opacity: 0.08,
      }}
    >
      ?
    </div>

    <div style={{ position: "absolute", top: 150, left: 96 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: theme.accents.mint, fontWeight: 700 }}>
        HOW IT WORKS
      </div>
      <div
        style={{
          fontFamily: fontStack.sans,
          fontWeight: 900,
          fontSize: 230,
          lineHeight: 0.9,
          color: theme.ink,
          letterSpacing: -8,
          marginTop: 6,
        }}
      >
        WHAT IS<br />
        AN{" "}
        <span style={{ color: theme.accents.magenta, textShadow: `0 0 50px ${theme.accents.magenta}` }}>API?</span>
      </div>
      <div
        style={{
          display: "inline-block",
          marginTop: 30,
          background: theme.accents.mint,
          color: theme.onAccent,
          fontFamily: fontStack.sans,
          fontWeight: 900,
          fontSize: 46,
          padding: "14px 30px",
          borderRadius: 16,
          transform: "rotate(-3deg)",
          boxShadow: glow(theme.accents.mint, 0.6),
        }}
      >
        FINALLY EXPLAINED
      </div>
    </div>

    {/* cast: you → API → server, glowing */}
    <div style={{ position: "absolute", right: 90, bottom: 70, display: "flex", alignItems: "center", gap: 18 }}>
      <Peep seed={CAST.you} size={340} />
      <div
        style={{
          background: theme.accents.magenta,
          color: theme.onAccent,
          fontFamily: fontStack.sans,
          fontWeight: 900,
          fontSize: 50,
          padding: "16px 30px",
          borderRadius: 999,
          boxShadow: glow(theme.accents.magenta, 0.7),
        }}
      >
        API
      </div>
      <Machine seed="kitchen-server-01" kind="server" size={240} bg={theme.accents.violet} />
    </div>
  </AbsoluteFill>
);

// ── Thumbnail B — the curiosity hook: "you're using one RIGHT NOW" ──────────
export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <ThumbBg accent={theme.accents.coral} corner="tl" />

    <div style={{ position: "absolute", top: 110, left: 96, width: 1060 }}>
      <div
        style={{
          fontFamily: fontStack.sans,
          fontWeight: 900,
          fontSize: 150,
          lineHeight: 0.92,
          color: theme.ink,
          letterSpacing: -5,
        }}
      >
        YOU'RE USING
        <br />
        <span style={{ color: theme.accents.amber, textShadow: `0 0 50px ${theme.accents.amber}` }}>AN API</span>
        <br />
        RIGHT NOW
      </div>
      <div
        style={{
          display: "inline-block",
          marginTop: 28,
          background: theme.paper,
          color: theme.ink,
          border: `2px solid ${theme.accents.coral}`,
          fontFamily: fontStack.mono,
          fontWeight: 700,
          fontSize: 40,
          padding: "12px 26px",
          borderRadius: 14,
        }}
      >
        …here's what that means
      </div>
    </div>

    {/* shocked peep with phone + red ring */}
    <div style={{ position: "absolute", right: 150, bottom: 60 }}>
      <div
        style={{
          position: "absolute",
          right: -30,
          top: -30,
          width: 540,
          height: 540,
          borderRadius: 999,
          border: `12px solid ${theme.accents.coral}`,
          boxShadow: glow(theme.accents.coral, 0.6),
        }}
      />
      <Peep seed={CAST.traveler} size={480} />
      <div
        style={{
          position: "absolute",
          left: -70,
          bottom: 90,
          background: theme.accents.coral,
          color: theme.onAccent,
          fontFamily: fontStack.sans,
          fontWeight: 900,
          fontSize: 54,
          padding: "14px 26px",
          borderRadius: 16,
          transform: "rotate(-6deg)",
          boxShadow: glow(theme.accents.coral, 0.7),
        }}
      >
        100× / DAY
      </div>
    </div>
  </AbsoluteFill>
);

// Default export kept as ThumbA for any single-still callers.
export const Thumb = ThumbA;
