import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

// A REAL desktop screenshot of the operating system (fetched CC-licensed at build
// time) with a slow Ken-Burns push so the frame is never static, an accent frame,
// a subtle scanline sheen, an "ACTUAL DESKTOP" tag and the CC credit. If the fetch
// found nothing (e.g. a copyrighted or non-existent OS), the caller shows the
// mechanism diagram full-size instead — never a fake screenshot.
type ImgMeta = { file: string; credit?: string; source?: string };

export const ScreenShot: React.FC<{
  img?: ImgMeta;
  name: string;
  accent: string;
  width?: number;
  height?: number;
}> = ({ img, name, accent, width = 1030, height = 360 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const t = durationInFrames > 1 ? frame / durationInFrames : 0;
  const scale = 1.05 + 0.08 * t;
  const tx = interpolate(t, [0, 1], [-10, 10]);
  const intro = interpolate(frame, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });

  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#050506", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.26), opacity: intro }}>
      {img ? (
        <Img
          src={staticFile(img.file)}
          style={{ position: "absolute", inset: 0, width: "100%", height: "100%", objectFit: "cover", transform: `scale(${scale}) translateX(${tx}px)`, filter: "saturate(1.03) contrast(1.03)" }}
        />
      ) : (
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
          <div style={{ fontFamily: fontStack.mono, fontSize: 90, color: `${accent}44` }}>▚</div>
        </div>
      )}

      {/* faint scanlines + vignette so a bright desktop sits in the dark layout */}
      <div style={{ position: "absolute", inset: 0, backgroundImage: "repeating-linear-gradient(0deg, #0000, #0000 2px, #0003 3px)", opacity: 0.35 }} />
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(0deg, ${theme.bg}cc 0%, transparent 40%)` }} />

      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>
        ◉ ACTUAL DESKTOP
      </div>

      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 76, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>

      {img?.credit ? (
        <div style={{ position: "absolute", left: 18, bottom: 2, fontFamily: fontStack.mono, fontSize: 10, color: theme.inkFaint, maxWidth: width - 220, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
          {img.credit}
        </div>
      ) : null}
    </div>
  );
};
