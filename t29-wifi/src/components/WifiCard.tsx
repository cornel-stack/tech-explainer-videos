import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T29: a Wi-Fi generation card — a radiating signal arc, the
// dual name (brand + 802.11 code), a log-scaled speed gauge, and 2.4/5/6 GHz band chips.
const BANDS = ["2.4", "5", "6"];

const SignalArcs: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => (
  <div style={{ position: "relative", width: 240, height: 200 }}>
    {[1, 2, 3, 4].map((i) => {
      const lit = (frame / 8 + i) % 4 < 2;
      return (
        <div key={i} style={{ position: "absolute", left: "50%", bottom: 10, width: i * 56, height: i * 56, transform: "translateX(-50%)", borderRadius: "50%", border: `7px solid ${accent}`, borderBottomColor: "transparent", borderLeftColor: "transparent", borderRightColor: "transparent", opacity: lit ? 0.9 - i * 0.12 : 0.18, boxShadow: lit ? glow(accent, 0.3) : "none" }} />
      );
    })}
    <div style={{ position: "absolute", left: "50%", bottom: 4, width: 20, height: 20, borderRadius: 999, background: accent, transform: "translateX(-50%)", boxShadow: glow(accent, 0.6) }} />
  </div>
);

export const WifiCard: React.FC<{ wifi: { code?: string; brand?: string; speed?: string; bands?: string; frac?: number }; name: string; accent: string; width?: number; height?: number }> = ({ wifi, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const active = (wifi.bands ?? "").split("+").map((b) => b.trim());
  const fill = Math.max(0.03, Math.min(1, wifi.frac ?? 0)) * Math.min(1, Math.max(0, (frame - 8) / 30));

  return (
    <div style={{ position: "relative", width, height, borderRadius: 16, overflow: "hidden", background: "#070a0b", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22), padding: 40, display: "flex", flexDirection: "column" }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `radial-gradient(${accent}12 1.5px, transparent 1.5px)`, backgroundSize: "44px 44px", opacity: 0.5 }} />

      {/* top: signal + names */}
      <div style={{ display: "flex", alignItems: "center", gap: 36, zIndex: 1 }}>
        <SignalArcs accent={accent} frame={frame} />
        <div>
          <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 64, color: theme.ink, letterSpacing: -2, lineHeight: 1 }}>{wifi.brand}</div>
          <div style={{ marginTop: 8, fontFamily: fontStack.mono, fontSize: 30, color: accent, letterSpacing: 1 }}>{wifi.code}</div>
        </div>
      </div>

      {/* speed gauge */}
      <div style={{ marginTop: "auto", zIndex: 1 }}>
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "baseline", marginBottom: 10 }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkFaint, letterSpacing: 1 }}>MAX SPEED</span>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34, color: theme.ink }}>{wifi.speed}</span>
        </div>
        <div style={{ height: 28, background: "#12161a", borderRadius: 999, overflow: "hidden", border: `1px solid ${accent}44` }}>
          <div style={{ height: "100%", width: `${fill * 100}%`, background: `linear-gradient(90deg, ${accent}66, ${accent})`, borderRadius: 999, boxShadow: glow(accent, 0.5) }} />
        </div>
        {/* band chips */}
        <div style={{ marginTop: 20, display: "flex", gap: 14 }}>
          {BANDS.map((b) => {
            const on = active.includes(b);
            return (
              <div key={b} style={{ flex: 1, textAlign: "center", padding: "12px 0", borderRadius: 10, border: `2px solid ${on ? accent : theme.line}`, background: on ? `${accent}1c` : "#0e1114", color: on ? theme.ink : theme.inkFaint, fontFamily: fontStack.mono, fontSize: 22, fontWeight: 700, boxShadow: on ? glow(accent, 0.25) : "none" }}>
                {b} GHz {on ? "●" : "○"}
              </div>
            );
          })}
        </div>
      </div>

      <div style={{ position: "absolute", right: 16, top: 14, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.inkFaint, border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>◂ {name} ▸</div>
    </div>
  );
};
