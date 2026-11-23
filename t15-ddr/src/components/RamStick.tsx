import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T15: an ORIGINAL drawn RAM module, rendered to match each
// type — a DIMM/SO-DIMM stick with chips and a gold pin edge whose NOTCH shifts
// position every generation (the physical "key" that stops you mixing DDR gens), or
// a soldered LPDDR package, GDDR around a GPU die, a 3D HBM stack, or SRAM cache
// cells inside a CPU. Animated: a light sweeps the gold pins, chips breathe.
export type Stick = {
  form?: string; // "dimm" | "sodimm" | "soldered" | "gpu" | "stack" | "onchip"
  pins?: number;
  notch?: number; // 0..1 position of the key notch along the pin edge
  chips?: number;
  ecc?: boolean;
  pmic?: boolean;
  curved?: boolean;
};

const GOLD = "#C9A64B";
const PCB = "#10281c";
const CHIP = "#16181e";

export const RamStick: React.FC<{ stick: Stick; name: string; accent: string; width?: number; height?: number }> = ({ stick, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const intro = interpolate(frame, [0, 16], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const form = stick.form ?? "dimm";

  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#070809", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.24), opacity: intro }}>
      {/* circuit-grid floor */}
      <div style={{ position: "absolute", inset: 0, backgroundImage: `linear-gradient(${accent}10 1px, transparent 1px), linear-gradient(90deg, ${accent}10 1px, transparent 1px)`, backgroundSize: "46px 46px", opacity: 0.5 }} />

      <div style={{ position: "absolute", inset: 0, display: "grid", placeItems: "center" }}>
        {form === "dimm" || form === "sodimm" ? <Dimm stick={stick} accent={accent} frame={frame} sodimm={form === "sodimm"} /> : null}
        {form === "soldered" ? <Soldered accent={accent} frame={frame} chips={stick.chips ?? 2} /> : null}
        {form === "gpu" ? <GpuMem accent={accent} frame={frame} /> : null}
        {form === "stack" ? <Stack accent={accent} frame={frame} /> : null}
        {form === "onchip" ? <OnChip accent={accent} frame={frame} /> : null}
      </div>

      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: fontStack.mono, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>◉ DRAWN TO SCALE</div>
      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 36, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 80, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>
    </div>
  );
};

// A gold pin edge with a key notch; a light sweeps across it.
const PinEdge: React.FC<{ w: number; notch: number; accent: string; frame: number; pins: number }> = ({ w, notch, accent, frame, pins }) => {
  const sweep = ((frame * 6) % (w + 200)) - 100;
  const notchX = notch * w;
  const notchW = 26;
  return (
    <div style={{ position: "relative", width: w, height: 40, marginTop: 6 }}>
      {/* pins */}
      <div style={{ position: "absolute", inset: 0, display: "flex", gap: 2, overflow: "hidden", borderRadius: "0 0 4px 4px" }}>
        {Array.from({ length: Math.min(90, Math.round(pins / 3)) }).map((_, i) => (
          <div key={i} style={{ flex: 1, background: GOLD, opacity: 0.85 }} />
        ))}
      </div>
      {/* shimmer */}
      <div style={{ position: "absolute", top: 0, bottom: 0, left: sweep, width: 90, background: "linear-gradient(90deg, transparent, #fff8, transparent)", transform: "skewX(-20deg)" }} />
      {/* notch (the key) */}
      <div style={{ position: "absolute", left: notchX - notchW / 2, bottom: 0, width: notchW, height: 40, background: "#070809" }} />
      <div style={{ position: "absolute", left: notchX, bottom: -34, transform: "translateX(-50%)", display: "flex", flexDirection: "column", alignItems: "center" }}>
        <span style={{ color: accent, fontSize: 22, lineHeight: 1 }}>▲</span>
        <span style={{ fontFamily: fontStack.mono, fontSize: 14, color: accent, letterSpacing: 1 }}>KEY</span>
      </div>
    </div>
  );
};

const Dimm: React.FC<{ stick: Stick; accent: string; frame: number; sodimm: boolean }> = ({ stick, accent, frame, sodimm }) => {
  const w = sodimm ? 560 : 840;
  const chips = stick.chips ?? 8;
  const notch = stick.notch ?? 0.5;
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", transform: "translateY(-6px)" }}>
      <div style={{ width: w, background: PCB, border: `2px solid ${accent}55`, borderRadius: stick.curved ? "8px 8px 18px 18px" : 8, padding: "16px 14px 8px", boxShadow: "0 14px 34px #000a" }}>
        {/* chips */}
        <div style={{ display: "flex", gap: 8, justifyContent: "center" }}>
          {Array.from({ length: chips }).map((_, i) => {
            const pulse = 0.6 + Math.sin(frame / 10 + i) * 0.4;
            const isEcc = stick.ecc && i === chips - 1;
            return (
              <div key={i} style={{ flex: 1, height: 72, background: CHIP, border: `1.5px solid ${isEcc ? accent : "#333"}`, borderRadius: 3, display: "grid", placeItems: "center", boxShadow: isEcc ? glow(accent, 0.4) : undefined }}>
                <div style={{ width: "66%", height: "50%", background: `${accent}${isEcc ? "55" : "22"}`, borderRadius: 2, opacity: 0.4 + pulse * 0.5 }} />
              </div>
            );
          })}
        </div>
        {/* label strip + optional PMIC */}
        <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", margin: "10px 4px 6px" }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint }}>{sodimm ? "SO-DIMM" : "DIMM"} · {stick.pins}-pin</span>
          {stick.pmic ? <span style={{ fontFamily: fontStack.mono, fontSize: 13, color: accent, border: `1px solid ${accent}`, borderRadius: 4, padding: "1px 6px" }}>PMIC on-board</span> : null}
          {stick.ecc ? <span style={{ fontFamily: fontStack.mono, fontSize: 13, color: accent, border: `1px solid ${accent}`, borderRadius: 4, padding: "1px 6px" }}>+ECC chip</span> : null}
        </div>
        <PinEdge w={w - 28} notch={notch} accent={accent} frame={frame} pins={stick.pins ?? 240} />
      </div>
      <span style={{ marginTop: 40, fontFamily: fontStack.mono, fontSize: 15, color: theme.inkSoft }}>notch sits at a unique spot each generation → gens don't interchange</span>
    </div>
  );
};

const Soldered: React.FC<{ accent: string; frame: number; chips: number }> = ({ accent, frame, chips }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 20 }}>
    <div style={{ width: 640, height: 220, background: "#0c1017", border: `2px solid ${accent}44`, borderRadius: 10, display: "flex", alignItems: "center", justifyContent: "center", gap: 40, position: "relative" }}>
      <span style={{ position: "absolute", left: 16, top: 10, fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint }}>mainboard</span>
      {Array.from({ length: chips }).map((_, i) => {
        const pulse = 0.6 + Math.sin(frame / 10 + i) * 0.4;
        return <div key={i} style={{ width: 130, height: 130, background: CHIP, border: `2px solid ${accent}`, borderRadius: 6, display: "grid", placeItems: "center", boxShadow: glow(accent, 0.3) }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 16, color: accent, opacity: 0.5 + pulse * 0.5 }}>LPDDR</span>
        </div>;
      })}
    </div>
    <span style={{ fontFamily: fontStack.mono, fontSize: 16, color: theme.accents.coral }}>soldered down — no slot, cannot be upgraded</span>
  </div>
);

const GpuMem: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => {
  const seats = [[0, -1], [1, -1], [1, 0], [1, 1], [0, 1], [-1, 1], [-1, 0], [-1, -1]];
  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
      <div style={{ position: "relative", width: 420, height: 420 }}>
        <div style={{ position: "absolute", left: "50%", top: "50%", width: 150, height: 150, transform: "translate(-50%,-50%)", background: "#14171f", border: `2px solid ${accent}`, borderRadius: 10, display: "grid", placeItems: "center", boxShadow: glow(accent, 0.4) }}>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 24, color: accent }}>GPU</span>
        </div>
        {seats.map(([dx, dy], i) => {
          const flow = 0.4 + Math.sin(frame / 7 + i) * 0.6;
          return <div key={i} style={{ position: "absolute", left: `calc(50% + ${dx * 150}px)`, top: `calc(50% + ${dy * 150}px)`, width: 72, height: 72, transform: "translate(-50%,-50%)", background: CHIP, border: `1.5px solid ${accent}99`, borderRadius: 4, opacity: 0.5 + flow * 0.5 }} />;
        })}
      </div>
      <span style={{ fontFamily: fontStack.mono, fontSize: 16, color: theme.inkSoft }}>memory soldered around the GPU · a very wide bus</span>
    </div>
  );
};

const Stack: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
    <div style={{ display: "flex", alignItems: "flex-end", gap: 30 }}>
      <div style={{ display: "flex", flexDirection: "column-reverse", gap: 4 }}>
        {Array.from({ length: 5 }).map((_, i) => {
          const pulse = 0.5 + Math.sin(frame / 9 + i * 0.6) * 0.5;
          return <div key={i} style={{ width: 150, height: 34, background: CHIP, border: `1.5px solid ${accent}`, borderRadius: 3, opacity: 0.55 + pulse * 0.45, boxShadow: glow(accent, 0.2) }} />;
        })}
        <span style={{ fontFamily: fontStack.mono, fontSize: 13, color: accent, textAlign: "center", marginTop: 6 }}>HBM stack</span>
      </div>
      <div style={{ width: 150, height: 150, background: "#14171f", border: `2px solid ${accent}`, borderRadius: 8, display: "grid", placeItems: "center" }}>
        <span style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 20, color: accent }}>die</span>
      </div>
    </div>
    <div style={{ width: 420, height: 16, background: `${accent}33`, border: `1px solid ${accent}66`, borderRadius: 3 }} />
    <span style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkSoft }}>dies stacked in 3D on a shared interposer · terabytes/sec</span>
  </div>
);

const OnChip: React.FC<{ accent: string; frame: number }> = ({ accent, frame }) => (
  <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 18 }}>
    <div style={{ width: 460, height: 300, background: "#101217", border: `2px solid ${accent}`, borderRadius: 12, padding: 20, position: "relative", boxShadow: glow(accent, 0.3) }}>
      <span style={{ position: "absolute", left: 16, top: 10, fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint }}>inside the CPU</span>
      <div style={{ display: "grid", gridTemplateColumns: "repeat(10, 1fr)", gap: 5, marginTop: 24 }}>
        {Array.from({ length: 60 }).map((_, i) => {
          const pulse = 0.4 + Math.sin(frame / 6 + i * 0.5) * 0.6;
          return <div key={i} style={{ height: 20, background: accent, opacity: 0.3 + pulse * 0.5, borderRadius: 2 }} />;
        })}
      </div>
      <span style={{ position: "absolute", right: 16, bottom: 10, fontFamily: fontStack.sans, fontWeight: 800, fontSize: 20, color: accent }}>L1 · L2 · L3 cache</span>
    </div>
    <span style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkSoft }}>6 transistors per bit · no capacitor · no refresh · blazing fast</span>
  </div>
);
