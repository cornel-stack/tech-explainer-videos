import React from "react";
import { Img, staticFile, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The item visual, redone with REAL photography: an actual photograph of the Intel
// chip (fetched CC-licensed at build time) shown in the left panel with a slow
// Ken-Burns push so the frame is never static, an accent frame + vignette, the
// chip name, and the attribution. If the fetch missed this chip we fall back to a
// generic Intel-silicon photo (`hero`); if even that is absent we draw a clean
// framed placeholder — never a synthetic "silicon die" diagram.
type ImgMeta = { file: string; credit?: string; source?: string };

export const ChipPhoto: React.FC<{
  img?: ImgMeta;
  name: string;
  accent: string;
  width?: number;
  height?: number;
}> = ({ img, name, accent, width = 1030, height = 490 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();

  // continuous slow push-in + drift (Ken Burns) — keeps the shot alive.
  const t = durationInFrames > 1 ? frame / durationInFrames : 0;
  const scale = 1.06 + 0.1 * t;
  const tx = interpolate(t, [0, 1], [-14, 14]);
  const ty = interpolate(t, [0, 1], [10, -10]);
  const intro = interpolate(frame, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const sweep = ((frame * 2) % (width + 400)) - 200; // moving sheen across the glass

  return (
    <div
      style={{
        position: "relative",
        width,
        height,
        borderRadius: 14,
        overflow: "hidden",
        background: "#050506",
        border: `1px solid ${accent}55`,
        boxShadow: glow(accent, 0.26),
        opacity: intro,
      }}
    >
      {img ? (
        <Img
          src={staticFile(img.file)}
          style={{
            position: "absolute",
            inset: 0,
            width: "100%",
            height: "100%",
            objectFit: "cover",
            transform: `scale(${scale}) translate(${tx}px, ${ty}px)`,
            filter: "saturate(1.05) contrast(1.04)",
          }}
        />
      ) : (
        // last-resort placeholder — a clean framed chip glyph, never a die diagram.
        <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
          <div style={{ fontFamily: fontStack.mono, fontSize: 120, color: `${accent}55` }}>▚</div>
        </div>
      )}

      {/* vignette so white product backdrops don't blow out the dark layout */}
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 100% at 50% 40%, transparent 45%, ${theme.bg}cc 100%)` }} />
      <div style={{ position: "absolute", inset: 0, background: `linear-gradient(0deg, ${theme.bg}dd 0%, transparent 38%)` }} />

      {/* moving sheen */}
      <div style={{ position: "absolute", top: 0, bottom: 0, left: sweep, width: 160, background: `linear-gradient(90deg, transparent, ${accent}1f, transparent)`, transform: "skewX(-18deg)" }} />

      {/* "real photo" tag */}
      <div style={{ position: "absolute", right: 16, top: 14, fontFamily: fontStack.mono, fontSize: 14, letterSpacing: 2, color: theme.ink, background: "#0008", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 10px" }}>
        ◉ REAL PHOTO
      </div>

      {/* chip name plate */}
      <div style={{ position: "absolute", left: 20, bottom: 18 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, color: theme.ink, textShadow: "0 2px 18px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 8, height: 4, width: 90, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>

      {/* attribution (CC credit) */}
      {img?.credit ? (
        <div style={{ position: "absolute", left: 20, bottom: 4, fontFamily: fontStack.mono, fontSize: 10, color: theme.inkFaint, maxWidth: width - 220, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}>
          {img.credit}
        </div>
      ) : null}
    </div>
  );
};
