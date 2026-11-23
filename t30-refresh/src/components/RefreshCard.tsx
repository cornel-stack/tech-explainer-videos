import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T30: a big Hz readout + frame time, a live "motion demo"
// where a dot steps across at this rate (low Hz strobes, high Hz glides), and a
// smoothness gauge. For VRR/truth items (hz <= 0) it shows a concept badge instead.
export const RefreshCard: React.FC<{ rate: { hz?: number; ms?: string; frac?: number; use?: string }; name: string; accent: string; width?: number; height?: number }> = ({ rate, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const hz = rate.hz ?? 60;
  const frac = Math.max(0.05, Math.min(1, rate.frac ?? 0.1));
  const fill = frac * Math.min(1, Math.max(0, (frame - 8) / 28));

  // motion demo: a dot crosses the track; position quantised to `steps` per loop so
  // higher Hz => finer steps => smoother. Use ghost trail to show strobing on low Hz.
  const period = 90; // frames per sweep
  const p = (frame % period) / period;
  const steps = hz > 0 ? Math.max(4, Math.round(hz / 6)) : 48;
  const quant = Math.floor(p * steps) / steps;
  const trackW = width - 160;
  const isConcept = hz <= 0;

  return (
    <div style={{ position: "relative", width, height, borderRadius: 16, overflow: "hidden", background: "#08070c", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22), padding: 40, display: "flex", flexDirection: "column" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `radial-gradient(${accent}12 1.5px, transparent 1.5px)`, backgroundSize: "44px 44px", opacity: 0.5 }} />

      {/* big readout */}
      <div style={{ display: "flex", alignItems: "baseline", gap: 20, zIndex: 1 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: isConcept ? 72 : 120, color: theme.ink, letterSpacing: -4, lineHeight: 0.9, textShadow: `0 0 40px ${accent}88` }}>
          {isConcept ? (rate.use ?? name) : hz}
          {!isConcept ? <span style={{ fontSize: 48, color: accent }}> Hz</span> : null}
        </div>
        {!isConcept ? <div style={{ fontFamily: fontStack.mono, fontSize: 30, color: accent }}>{rate.ms}</div> : null}
      </div>
      {rate.use && !isConcept ? <div style={{ fontFamily: fontStack.sans, fontSize: 26, fontWeight: 700, color: theme.inkSoft, zIndex: 1, marginTop: 4 }}>{rate.use}</div> : null}

      {/* motion demo track */}
      <div style={{ marginTop: "auto", zIndex: 1 }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 16, color: theme.inkFaint, letterSpacing: 1, marginBottom: 10 }}>{isConcept ? "SYNC" : "MOTION"}</div>
        <div style={{ position: "relative", height: 70, background: "#100e16", borderRadius: 12, border: `1px solid ${accent}33`, overflow: "hidden" }}>
          {/* ghost trail (strobe effect — visible on low Hz because steps are coarse) */}
          {[0.05, 0.1, 0.16].map((d, i) => (
            <div key={i} style={{ position: "absolute", top: 23, left: 20 + Math.max(0, quant - d) * trackW, width: 24, height: 24, borderRadius: 999, background: accent, opacity: 0.18 - i * 0.04 }} />
          ))}
          <div style={{ position: "absolute", top: 20, left: 20 + quant * trackW, width: 30, height: 30, borderRadius: 999, background: accent, boxShadow: glow(accent, 0.6) }} />
        </div>

        {/* smoothness gauge */}
        <div style={{ display: "flex", alignItems: "center", gap: 14, marginTop: 20 }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, color: theme.inkFaint, width: 130 }}>{isConcept ? "BENEFIT" : "SMOOTHNESS"}</span>
          <div style={{ flex: 1, height: 20, background: "#14121a", borderRadius: 999, overflow: "hidden", border: `1px solid ${accent}44` }}>
            <div style={{ height: "100%", width: `${fill * 100}%`, background: `linear-gradient(90deg, ${theme.accents.coral}, ${theme.accents.amber} 50%, ${theme.accents.mint})`, borderRadius: 999, boxShadow: glow(accent, 0.4) }} />
          </div>
        </div>
      </div>

      <div style={{ position: "absolute", right: 16, top: 14, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.inkFaint, border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>▭ {name}</div>
    </div>
  );
};
