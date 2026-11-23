import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T20: a drawn granite MEMORIAL for each dead OS — a headstone
// with R.I.P., the OS name, born–died dates and an epitaph, beside a flickering "dead"
// screen in the OS's device form (crt / desktop / pda / phone) that boots then dies.
const STONE = "#1b1d22";
const STONE_HI = "#2a2d34";
const GRASS = "#0c140e";

// a cheap deterministic flicker — screens of the dead don't rest
const flick = (f: number, seed: number) => {
  const x = Math.sin(f * 0.9 + seed) + Math.sin(f * 0.37 + seed * 2.1);
  return x > 1.4 ? 0.25 : 0.55 + 0.45 * (0.5 + 0.5 * Math.sin(f / 18 + seed));
};

const DeadScreen: React.FC<{ form: string; accent: string; frame: number; name: string }> = ({ form, accent, frame, name }) => {
  // the screen "dies" late in each item: after ~frame 150 it mostly goes to static/black
  const alive = frame < 150 ? 1 : Math.max(0.12, 1 - (frame - 150) / 120);
  const lit = flick(frame, name.length) * alive;
  const scan = (frame * 3) % 100;

  const Glass = (
    <div style={{ position: "relative", width: "100%", height: "100%", background: "#060a07", overflow: "hidden", borderRadius: form === "phone" ? 18 : 4 }}>
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 120% at 50% 40%, ${accent}${Math.round(lit * 90).toString(16).padStart(2, "0")}, transparent 70%)` }} />
      <div style={{ position: "absolute", left: 0, right: 0, top: `${scan}%`, height: 3, background: `${accent}55`, opacity: alive }} />
      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: form === "phone" ? 22 : 30, color: accent, opacity: lit, letterSpacing: 2, textAlign: "center", lineHeight: 1.4 }}>
          {frame < 150 ? name : "— no signal —"}
        </div>
      </div>
      {/* dead static speckle after death */}
      {frame >= 150 ? <div style={{ position: "absolute", inset: 0, backgroundImage: `repeating-linear-gradient(0deg, #ffffff10 0 1px, transparent 1px 3px)`, opacity: 0.4 * (1 - alive) + 0.1 }} /> : null}
    </div>
  );

  if (form === "phone")
    return (
      <div style={{ width: 230, height: 440, background: "#0b0d10", border: `5px solid ${STONE_HI}`, borderRadius: 30, padding: 12, boxShadow: "0 18px 50px #000b" }}>
        <div style={{ width: "100%", height: "100%", borderRadius: 18, overflow: "hidden", border: `2px solid ${accent}44` }}>{Glass}</div>
      </div>
    );
  if (form === "pda")
    return (
      <div style={{ width: 300, height: 400, background: "#15110c", border: `5px solid ${STONE_HI}`, borderRadius: 18, padding: "20px 24px 60px", boxShadow: "0 18px 50px #000b", position: "relative" }}>
        <div style={{ width: "100%", height: "100%", borderRadius: 6, overflow: "hidden", border: `2px solid ${accent}44` }}>{Glass}</div>
        <div style={{ position: "absolute", bottom: 18, left: "50%", transform: "translateX(-50%)", width: 70, height: 26, borderRadius: 999, border: `2px solid ${STONE_HI}` }} />
      </div>
    );
  // crt + desktop share a monitor shell
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center" }}>
      <div style={{ width: 460, height: 330, background: "#101216", border: `14px solid #16181d`, borderRadius: form === "crt" ? 24 : 10, padding: 10, boxShadow: `0 20px 50px #000b, inset 0 0 0 2px ${accent}33` }}>
        <div style={{ width: "100%", height: "100%", overflow: "hidden", borderRadius: form === "crt" ? 20 : 4 }}>{Glass}</div>
      </div>
      <div style={{ width: form === "crt" ? 160 : 120, height: 40, background: "#16181d", borderRadius: "0 0 10px 10px" }} />
    </div>
  );
};

export const Tombstone: React.FC<{ grave: { form?: string; born?: string; died?: string; epitaph?: string }; name: string; accent: string; width?: number; height?: number }> = ({ grave, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const form = grave.form ?? "crt";
  const sway = Math.sin(frame / 40) * 0.4;
  const candle = 0.6 + 0.4 * (0.5 + 0.5 * Math.sin(frame / 6) + 0.2 * Math.sin(frame / 2.3));

  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "linear-gradient(180deg,#07090b,#0b0f0c)", border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.18) }}>
      {/* moonlight + fog */}
      <div style={{ position: "absolute", inset: 0, background: `radial-gradient(900px 500px at 70% -10%, ${accent}1c, transparent 60%)` }} />
      {/* ground */}
      <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 120, background: GRASS, borderTop: `1px solid ${accent}33` }} />

      {/* LEFT: the headstone */}
      <div style={{ position: "absolute", left: 60, bottom: 70, transform: `rotate(${sway}deg)`, transformOrigin: "50% 100%" }}>
        <div style={{ width: 360, height: 420, background: `linear-gradient(180deg, ${STONE_HI}, ${STONE})`, borderRadius: "180px 180px 14px 14px", border: `2px solid #33363d`, boxShadow: "0 20px 50px #000c, inset 0 2px 0 #3a3d44", display: "flex", flexDirection: "column", alignItems: "center", padding: "46px 30px 0" }}>
          <div style={{ fontFamily: fontStack.mono, fontSize: 30, letterSpacing: 8, color: theme.inkFaint }}>R·I·P</div>
          <div style={{ marginTop: 14, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, color: theme.ink, textAlign: "center", lineHeight: 1.0 }}>{name}</div>
          <div style={{ marginTop: 14, fontFamily: fontStack.mono, fontSize: 24, color: accent }}>{grave.born} — {grave.died}</div>
          <div style={{ marginTop: 18, width: 70, height: 2, background: "#44474e" }} />
          <div style={{ marginTop: 16, fontFamily: fontStack.sans, fontStyle: "italic", fontSize: 18, color: theme.inkSoft, textAlign: "center", lineHeight: 1.3 }}>“{grave.epitaph}”</div>
        </div>
      </div>

      {/* candle glow at the base of the stone */}
      <div style={{ position: "absolute", left: 250, bottom: 66, width: 26, height: 40 }}>
        <div style={{ position: "absolute", bottom: 0, left: 6, width: 14, height: 22, background: "#d8d2c4", borderRadius: 3 }} />
        <div style={{ position: "absolute", bottom: 20, left: 11, width: 6, height: 14, borderRadius: "50% 50% 50% 50% / 70% 70% 30% 30%", background: `radial-gradient(${theme.accents.amber}, ${theme.accents.coral})`, opacity: candle, boxShadow: `0 0 26px ${theme.accents.amber}${Math.round(candle * 255).toString(16).padStart(2, "0")}` }} />
      </div>

      {/* RIGHT: the device, screen flickering then dying */}
      <div style={{ position: "absolute", right: 70, top: 0, bottom: 0, display: "flex", alignItems: "center" }}>
        <DeadScreen form={form} accent={accent} frame={frame} name={name} />
      </div>

      <div style={{ position: "absolute", right: 18, top: 14, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.inkFaint, border: `1px solid ${accent}55`, borderRadius: 6, padding: "4px 9px" }}>† DISCONTINUED</div>
    </div>
  );
};
