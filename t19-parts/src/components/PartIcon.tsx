import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T19: an ORIGINAL drawn icon of each PC part, animated —
// spinning fans, glowing screens, pulsing chips. One <Part> switch per component.
const CHIP = "#16181e";
const PCB = "#10281c";

const Fan: React.FC<{ s: number; c: string; frame: number; speed?: number }> = ({ s, c, frame, speed = 6 }) => (
  <div style={{ width: s, height: s, borderRadius: 999, border: `2px solid ${c}`, background: "#0c0e12", display: "grid", placeItems: "center", boxShadow: glow(c, 0.3) }}>
    <div style={{ width: s * 0.82, height: s * 0.82, transform: `rotate(${frame * speed}deg)`, position: "relative" }}>
      {[0, 60, 120, 180, 240, 300].map((a) => (
        <div key={a} style={{ position: "absolute", left: "50%", top: "50%", width: s * 0.36, height: s * 0.14, background: `${c}99`, borderRadius: s * 0.07, transformOrigin: "0 50%", transform: `rotate(${a}deg)` }} />
      ))}
      <div style={{ position: "absolute", left: "50%", top: "50%", width: s * 0.2, height: s * 0.2, background: c, borderRadius: 999, transform: "translate(-50%,-50%)" }} />
    </div>
  </div>
);

export const PartIcon: React.FC<{ part: string; name: string; accent: string; width?: number; height?: number }> = ({ part, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#070809", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.24) }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${accent}10 1px, transparent 1px), linear-gradient(90deg, ${accent}10 1px, transparent 1px)`, backgroundSize: "46px 46px", opacity: 0.5 }} />
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        <Part part={part} accent={accent} frame={frame} />
      </div>
      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>◉ DRAWN</div>
      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 80, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>
    </div>
  );
};

const Chip: React.FC<{ s: number; c: string; frame: number; label?: string }> = ({ s, c, frame, label }) => {
  const pins = 10;
  return (
    <div style={{ position: "relative", width: s, height: s }}>
      {[["top", "left"], ["bottom", "left"], ["left", "top"], ["right", "top"]].map(([side, cross], si) => (
        <div key={si} style={{ position: "absolute", [side]: -10, [cross as string]: 0, width: side === "left" || side === "right" ? 10 : s, height: side === "left" || side === "right" ? s : 10, display: "flex", flexDirection: side === "left" || side === "right" ? "column" : "row", justifyContent: "space-around", padding: side === "left" || side === "right" ? "14px 0" : "0 14px" } as any}>
          {Array.from({ length: pins }).map((_, i) => <div key={i} style={{ width: 4, height: 4, background: "#C9A64B" }} />)}
        </div>
      ))}
      <div style={{ width: s, height: s, background: CHIP, border: `2px solid ${c}`, borderRadius: 10, display: "grid", placeItems: "center", boxShadow: glow(c, 0.4) }}>
        <div style={{ width: s * 0.5, height: s * 0.5, border: `2px solid ${c}`, borderRadius: 6, opacity: 0.5 + 0.5 * Math.sin(frame / 10), display: "grid", placeItems: "center", fontFamily: fontStack.mono, fontSize: 18, color: c }}>{label}</div>
      </div>
    </div>
  );
};

const Part: React.FC<{ part: string; accent: string; frame: number }> = ({ part, accent, frame }) => {
  if (part === "cpu") return <Chip s={230} c={accent} frame={frame} label="CPU" />;

  if (part === "mobo")
    return (
      <div style={{ width: 460, height: 380, background: PCB, border: `3px solid ${accent}66`, borderRadius: 10, padding: 24, position: "relative", boxShadow: "0 16px 40px #000a" }}>
        <div style={{ position: "absolute", left: 30, top: 30, width: 90, height: 90, background: CHIP, border: `2px solid ${accent}`, borderRadius: 8, display: "grid", placeItems: "center", fontFamily: fontStack.mono, fontSize: 16, color: accent }}>CPU</div>
        <div style={{ position: "absolute", right: 26, top: 24, display: "flex", gap: 8 }}>{[0, 1, 2, 3].map((i) => <div key={i} style={{ width: 12, height: 150, background: `${accent}33`, border: `1px solid ${accent}`, borderRadius: 3 }} />)}</div>
        <div style={{ position: "absolute", left: 26, bottom: 24, width: 300, height: 22, background: "#0c0e12", border: `1px solid ${accent}99`, borderRadius: 3 }} />
        <span style={{ position: "absolute", right: 30, bottom: 16, fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint }}>RAM slots →</span>
      </div>
    );

  if (part === "ram")
    return (
      <div style={{ width: 620, background: PCB, border: `2px solid ${accent}66`, borderRadius: 8, padding: "16px 12px 8px", boxShadow: "0 14px 34px #000a" }}>
        <div style={{ display: "flex", gap: 8 }}>{Array.from({ length: 8 }).map((_, i) => <div key={i} style={{ flex: 1, height: 70, background: CHIP, border: `1px solid ${accent}55`, borderRadius: 3, opacity: 0.5 + 0.5 * Math.sin(frame / 10 + i) }} />)}</div>
        <div style={{ display: "flex", gap: 2, marginTop: 10 }}>{Array.from({ length: 40 }).map((_, i) => <div key={i} style={{ flex: 1, height: 18, background: "#C9A64B" }} />)}</div>
      </div>
    );

  if (part === "gpu")
    return (
      <div style={{ width: 560, height: 230, background: "#14171f", border: `3px solid ${accent}66`, borderRadius: 10, padding: 20, display: "flex", alignItems: "center", gap: 30, boxShadow: "0 16px 40px #000a" }}>
        <Fan s={150} c={accent} frame={frame} speed={8} />
        <Fan s={150} c={accent} frame={frame} speed={8} />
        <div style={{ marginLeft: "auto", writingMode: "vertical-rl", fontFamily: fontStack.mono, fontSize: 16, color: theme.inkFaint }}>graphics card</div>
      </div>
    );

  if (part === "storage")
    return (
      <div style={{ display: "flex", gap: 40, alignItems: "center" }}>
        <div style={{ width: 240, height: 150, background: "#14171f", border: `2px solid ${accent}`, borderRadius: 8, display: "grid", gridTemplateColumns: "1fr 1fr", gap: 10, padding: 18, boxShadow: glow(accent, 0.3) }}>
          {[0, 1, 2, 3].map((i) => <div key={i} style={{ background: CHIP, border: `1px solid ${accent}66`, borderRadius: 3 }} />)}
          <span style={{ position: "absolute", fontFamily: fontStack.mono, fontSize: 0 }} />
        </div>
        <div style={{ width: 200, height: 200, background: "#14171f", border: `2px solid ${accent}66`, borderRadius: 8, display: "grid", placeItems: "center", boxShadow: "0 12px 30px #000a" }}>
          <div style={{ width: 150, height: 150, borderRadius: 999, background: "conic-gradient(#2a2e38, #15171c, #2a2e38)", transform: `rotate(${frame * 10}deg)`, border: `2px solid ${accent}55`, display: "grid", placeItems: "center" }}>
            <div style={{ width: 30, height: 30, borderRadius: 999, background: accent }} />
          </div>
        </div>
      </div>
    );

  if (part === "psu")
    return (
      <div style={{ width: 360, height: 260, background: "#14171f", border: `3px solid ${accent}66`, borderRadius: 10, padding: 24, position: "relative", boxShadow: "0 16px 40px #000a" }}>
        <Fan s={180} c={accent} frame={frame} speed={5} />
        {[0, 1, 2, 3].map((i) => <div key={i} style={{ position: "absolute", right: -40, top: 40 + i * 44, width: 60, height: 8, background: i % 2 ? "#444" : accent, borderRadius: 4 }} />)}
        <span style={{ position: "absolute", left: 24, bottom: 12, fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>AC → DC</span>
      </div>
    );

  if (part === "cooler")
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 14 }}>
        <Fan s={150} c={accent} frame={frame} speed={9} />
        <div style={{ display: "flex", gap: 4 }}>{Array.from({ length: 16 }).map((_, i) => <div key={i} style={{ width: 10, height: 150, background: "#2a2e38", border: `1px solid ${accent}44`, borderRadius: 2 }} />)}</div>
        <span style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>heatsink fins</span>
      </div>
    );

  if (part === "case")
    return (
      <div style={{ width: 280, height: 420, background: "#0c0e12", border: `3px solid ${accent}66`, borderRadius: 12, padding: 18, position: "relative", boxShadow: "0 16px 40px #000a" }}>
        <div style={{ position: "absolute", left: 18, top: 18, bottom: 18, width: 50, display: "flex", flexDirection: "column", gap: 10 }}>
          {[0, 1, 2].map((i) => <Fan key={i} s={50} c={accent} frame={frame} speed={6} />)}
        </div>
        <div style={{ position: "absolute", right: 24, top: 40, display: "flex", flexDirection: "column", gap: 12 }}>
          <div style={{ width: 150, height: 90, background: PCB, border: `1px solid ${accent}` }} />
          <div style={{ width: 150, height: 40, background: "#14171f", border: `1px solid ${accent}66` }} />
        </div>
        <span style={{ position: "absolute", bottom: 10, right: 20, fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint }}>airflow →</span>
      </div>
    );

  if (part === "monitor")
    return (
      <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
        <div style={{ width: 460, height: 280, background: "#0c2a1e", border: `4px solid ${accent}`, borderRadius: 10, boxShadow: `inset 0 0 40px ${accent}44, ${glow(accent, 0.4)}`, display: "grid", placeItems: "center" }}>
          <div style={{ fontFamily: fontStack.mono, fontSize: 30, color: accent, opacity: 0.5 + 0.5 * Math.sin(frame / 12) }}>▦ image</div>
        </div>
        <div style={{ width: 24, height: 50, background: "#2a2e38" }} />
        <div style={{ width: 180, height: 16, background: "#2a2e38", borderRadius: 4 }} />
      </div>
    );

  // peripherals: keyboard + mouse
  return (
    <div style={{ display: "flex", alignItems: "flex-end", gap: 40 }}>
      <div style={{ width: 420, background: "#14171f", border: `2px solid ${accent}66`, borderRadius: 10, padding: 14, display: "grid", gridTemplateColumns: "repeat(10,1fr)", gap: 6, boxShadow: "0 12px 30px #000a" }}>
        {Array.from({ length: 40 }).map((_, i) => <div key={i} style={{ height: 24, background: CHIP, border: `1px solid ${accent}44`, borderRadius: 3, opacity: (frame + i * 7) % 90 < 8 ? 1 : 0.6 }} />)}
      </div>
      <div style={{ width: 120, height: 180, background: "#14171f", border: `2px solid ${accent}66`, borderRadius: "60px 60px 50px 50px", position: "relative", boxShadow: "0 12px 30px #000a" }}>
        <div style={{ position: "absolute", left: "50%", top: 14, width: 3, height: 60, background: `${accent}66`, transform: "translateX(-50%)" }} />
        <div style={{ position: "absolute", left: "50%", top: 70, width: 20, height: 24, background: accent, borderRadius: 6, transform: "translateX(-50%)", opacity: 0.5 + 0.5 * Math.sin(frame / 8) }} />
      </div>
    </div>
  );
};
