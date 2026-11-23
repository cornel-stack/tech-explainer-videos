import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T18: an ORIGINAL drawn phone from each mobile era — the
// 1G brick with its pull-up antenna, the 2G/3G candybar with a keypad, the 4G/5G
// smartphone slab, the 6G foldable — beside a LOG-scaled peak-speed bar and the one
// thing that generation unlocked. The screen glows, signal bars pulse.
type Gen = { era?: string; speed?: number; unlocked?: string };

const SCREEN = "#0c2a1e";

export const GenPhone: React.FC<{ gen: Gen; name: string; accent: string; width?: number; height?: number }> = ({ gen, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const era = gen.era ?? "smartphone";
  const speed = gen.speed ?? 1; // Mbps
  // log scale: 0.002 Mbps (1G) → 100000 Mbps (6G)  →  bar fraction
  const frac = Math.min(1, Math.max(0.04, (Math.log10(speed) + 3) / (5 + 3)));
  const glowPulse = 0.5 + Math.sin(frame / 12) * 0.5;

  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#070809", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.24) }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${accent}10 1px, transparent 1px), linear-gradient(90deg, ${accent}10 1px, transparent 1px)`, backgroundSize: "46px 46px", opacity: 0.5 }} />

      {/* the phone, centred-left */}
      <div style={{ position: "absolute", left: 120, top: 0, bottom: 0, display: "flex", alignItems: "center" }}>
        <Phone era={era} accent={accent} frame={frame} />
      </div>

      {/* right: speed bar (log) + unlocked */}
      <div style={{ position: "absolute", right: 48, top: 110, width: 420 }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 1 }}>PEAK SPEED (log scale)</div>
        <div style={{ marginTop: 10, height: 38, borderRadius: 8, background: "#111318", border: `1px solid ${accent}44`, overflow: "hidden" }}>
          <div style={{ width: `${frac * 100}%`, height: "100%", background: `linear-gradient(90deg, ${accent}66, ${accent})`, boxShadow: glow(accent, 0.4) }} />
        </div>
        <div style={{ marginTop: 26, fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 1 }}>WHAT IT UNLOCKED</div>
        <div style={{ marginTop: 8, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, color: accent, lineHeight: 1.05, textShadow: `0 0 ${glowPulse * 18}px ${accent}66` }}>{gen.unlocked ?? ""}</div>
      </div>

      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>◉ DRAWN</div>
      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 80, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>
    </div>
  );
};

const Signal: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => (
  <div style={{ display: "flex", alignItems: "flex-end", gap: 3, height: 20 }}>
    {[0.4, 0.6, 0.8, 1].map((h, i) => {
      const on = (Math.sin(frame / 9 + i) + 1) / 2 > 0.3;
      return <div key={i} style={{ width: 6, height: `${h * 100}%`, background: on ? accent : `${accent}33`, borderRadius: 1 }} />;
    })}
  </div>
);

const Phone: React.FC<{ era: string; accent: string; frame: number }> = ({ era, accent, frame }) => {
  const scr = <div style={{ background: SCREEN, border: `2px solid ${accent}55`, borderRadius: 6, boxShadow: `inset 0 0 20px ${accent}33` }} />;

  if (era === "brick") {
    return (
      <div style={{ position: "relative" }}>
        {/* antenna */}
        <div style={{ position: "absolute", top: -90, right: 24, width: 8, height: 100, background: "#888", borderRadius: 4 }} />
        <div style={{ position: "absolute", top: -98, right: 20, width: 16, height: 16, borderRadius: 999, background: "#aaa" }} />
        <div style={{ width: 190, height: 400, background: "#1a1d24", border: `3px solid ${accent}66`, borderRadius: 18, padding: 16, display: "flex", flexDirection: "column", gap: 12, boxShadow: "0 18px 40px #000a" }}>
          <div style={{ display: "flex", justifyContent: "flex-end" }}><Signal accent={accent} frame={frame} /></div>
          <div style={{ height: 80, ...( {} ), background: SCREEN, border: `2px solid ${accent}55`, borderRadius: 6 }} />
          <div style={{ flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 8 }}>
            {Array.from({ length: 12 }).map((_, i) => <div key={i} style={{ background: "#2a2e38", borderRadius: 5 }} />)}
          </div>
        </div>
      </div>
    );
  }
  if (era === "candybar") {
    return (
      <div style={{ width: 170, height: 360, background: "#1a1d24", border: `3px solid ${accent}66`, borderRadius: 22, padding: 14, display: "flex", flexDirection: "column", gap: 10, boxShadow: "0 18px 40px #000a" }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}><Signal accent={accent} frame={frame} /><div style={{ width: 18, height: 6, background: "#555", borderRadius: 3 }} /></div>
        <div style={{ height: 150, background: SCREEN, border: `2px solid ${accent}55`, borderRadius: 6, boxShadow: `inset 0 0 18px ${accent}33` }} />
        <div style={{ flex: 1, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gap: 7 }}>
          {Array.from({ length: 12 }).map((_, i) => <div key={i} style={{ background: "#2a2e38", borderRadius: 4 }} />)}
        </div>
      </div>
    );
  }
  if (era === "foldable") {
    return (
      <div style={{ display: "flex", boxShadow: "0 18px 40px #000a" }}>
        {[0, 1].map((p) => (
          <div key={p} style={{ width: 150, height: 380, background: "#14171f", border: `3px solid ${accent}66`, borderLeft: p ? `1px solid ${accent}44` : undefined, borderRadius: p ? "0 20px 20px 0" : "20px 0 0 20px", padding: 10 }}>
            <div style={{ width: "100%", height: "100%", background: SCREEN, border: `2px solid ${accent}55`, borderRadius: 6, boxShadow: `inset 0 0 22px ${accent}44` }} />
          </div>
        ))}
      </div>
    );
  }
  // smartphone slab
  return (
    <div style={{ width: 210, height: 420, background: "#14171f", border: `3px solid ${accent}66`, borderRadius: 30, padding: 12, display: "flex", flexDirection: "column", gap: 8, boxShadow: "0 18px 40px #000a" }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", padding: "0 8px" }}><Signal accent={accent} frame={frame} /><span style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint }}>{9 + (Math.floor(frame / 120) % 3)}:4{Math.floor(frame / 6) % 10}</span></div>
      <div style={{ flex: 1, background: SCREEN, border: `2px solid ${accent}55`, borderRadius: 16, boxShadow: `inset 0 0 28px ${accent}44`, display: "grid", gridTemplateColumns: "1fr 1fr 1fr", gridTemplateRows: "repeat(4,1fr)", gap: 10, padding: 16 }}>
        {Array.from({ length: 12 }).map((_, i) => {
          const pulse = 0.4 + Math.sin(frame / 10 + i * 0.6) * 0.5;
          return <div key={i} style={{ background: `${accent}${i % 3 === 0 ? "55" : "22"}`, borderRadius: 8, opacity: 0.4 + pulse * 0.5 }} />;
        })}
      </div>
    </div>
  );
};
