import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T26: a drawn USB connector silhouette for each physical
// type, or an animated speed/power GAUGE for the standard/spec items. No logos.
const METAL = "#C9CDD4";

const Plug: React.FC<{ shape: string; accent: string; frame: number }> = ({ shape, accent, frame }) => {
  // a gentle insert bob
  const bob = Math.sin(frame / 20) * 10;
  const shell = (w: number, h: number, radius: string, inner?: React.ReactNode) => (
    <div style={{ transform: `translateX(${bob}px)` }}>
      <div style={{ width: w, height: h, background: "#14171f", border: `4px solid ${METAL}`, borderRadius: radius, display: "grid", placeItems: "center", boxShadow: glow(accent, 0.3) }}>
        <div style={{ width: w - 34, height: h - 30, background: "#0a0c10", borderRadius: 6, display: "flex", alignItems: "center", justifyContent: "center" }}>{inner}</div>
      </div>
      {/* cable tail */}
      <div style={{ width: 90, height: 26, background: "#1a1d24", borderRadius: 8, margin: "0 auto", marginTop: -2 }} />
    </div>
  );
  if (shape === "usba") return shell(360, 150, "8px", <div style={{ width: "72%", height: 20, background: accent, borderRadius: 3 }} />);
  if (shape === "usbb") return shell(210, 210, "14px 14px 8px 8px", <div style={{ width: "60%", height: "55%", border: `3px solid ${accent}`, borderRadius: 4 }} />);
  if (shape === "mini") return shell(220, 120, "10px 10px 22px 22px", <div style={{ width: "66%", height: 16, background: accent, borderRadius: 3 }} />);
  if (shape === "micro") return shell(240, 96, "8px 8px 20px 20px", <div style={{ width: "70%", height: 12, background: accent, borderRadius: 3 }} />);
  if (shape === "lightning") return shell(300, 96, "999px", <div style={{ display: "flex", gap: 8 }}>{Array.from({ length: 8 }).map((_, i) => <div key={i} style={{ width: 14, height: 30, background: accent, borderRadius: 3, opacity: 0.6 }} />)}</div>);
  // usbc: reversible oval, with a flip indicator
  return (
    <div style={{ transform: `translateX(${bob}px)`, textAlign: "center" }}>
      <div style={{ width: 300, height: 120, background: "#14171f", border: `4px solid ${METAL}`, borderRadius: 999, display: "grid", placeItems: "center", boxShadow: glow(accent, 0.45) }}>
        <div style={{ width: 230, height: 54, background: "#0a0c10", borderRadius: 999, display: "grid", placeItems: "center" }}>
          <div style={{ width: 180, height: 14, background: accent, borderRadius: 999 }} />
        </div>
      </div>
      <div style={{ width: 90, height: 26, background: "#1a1d24", borderRadius: 8, margin: "6px auto 0" }} />
      <div style={{ marginTop: 14, fontFamily: fontStack.mono, fontSize: 22, color: accent, letterSpacing: 2, opacity: 0.6 + 0.4 * Math.sin(frame / 8) }}>↔ reversible</div>
    </div>
  );
};

const Gauge: React.FC<{ value: string; frac: number; accent: string; frame: number }> = ({ value, frac, accent, frame }) => {
  const fill = Math.max(0, Math.min(1, frac)) * (0.6 + 0.4 * Math.min(1, frame / 40));
  return (
    <div style={{ width: 760, textAlign: "center" }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 92, color: theme.ink, letterSpacing: -2, textShadow: `0 0 40px ${accent}88` }}>{value}</div>
      <div style={{ marginTop: 26, height: 40, background: "#14171f", borderRadius: 999, border: `2px solid ${accent}55`, overflow: "hidden", position: "relative" }}>
        <div style={{ position: "absolute", inset: 0, width: `${fill * 100}%`, background: `linear-gradient(90deg, ${accent}66, ${accent})`, borderRadius: 999, boxShadow: glow(accent, 0.5) }} />
        {/* tick marks */}
        {[0.08, 0.25, 0.5, 0.85, 1].map((p, i) => <div key={i} style={{ position: "absolute", left: `${p * 100}%`, top: 0, bottom: 0, width: 2, background: "#0a0c1088" }} />)}
      </div>
      <div style={{ marginTop: 10, display: "flex", justifyContent: "space-between", fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint }}>
        <span>slow</span><span>480Mbps</span><span>5G</span><span>20G</span><span>40G+</span>
      </div>
    </div>
  );
};

export const UsbIcon: React.FC<{ usb: { kind?: string; shape?: string; value?: string; frac?: number }; name: string; accent: string; width?: number; height?: number }> = ({ usb, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const kind = usb.kind ?? "connector";
  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#070809", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22) }}>
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${accent}0f 1px, transparent 1px), linear-gradient(90deg, ${accent}0f 1px, transparent 1px)`, backgroundSize: "46px 46px", opacity: 0.5 }} />
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        {kind === "connector" ? <Plug shape={usb.shape ?? "usba"} accent={accent} frame={frame} /> : <Gauge value={usb.value ?? ""} frac={usb.frac ?? 0} accent={accent} frame={frame} />}
      </div>
      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>{kind === "connector" ? "◉ CONNECTOR" : "◈ SPEED / POWER"}</div>
      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 80, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>
    </div>
  );
};
