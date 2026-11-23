import React from "react";
import { useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T12: an ORIGINAL, drawn homage of each Windows era's
// desktop — the gray 95 taskbar, XP's blue Luna + green hill, Vista/7 frosted Aero
// glass, Win8's flat Start-screen tiles, Win10/11's flat chrome. No Microsoft
// screenshots, no four-colour flag logo — our own flat marks, animated (a window
// opens, the cursor drifts, clouds/aurora move, the clock ticks).
type Skin = "retro" | "win9x" | "nt" | "luna" | "aero" | "metro" | "flat" | "flat11";

const SANS = fontStack.sans;
const MONO = fontStack.mono;

// a neutral 4-pane "window" glyph — deliberately NOT the Microsoft colours.
const Panes: React.FC<{ s: number; c: string }> = ({ s, c }) => (
  <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gridTemplateRows: "1fr 1fr", gap: s * 0.12, width: s, height: s }}>
    {[0, 1, 2, 3].map((i) => <div key={i} style={{ background: c, borderRadius: s * 0.06 }} />)}
  </div>
);

const Cursor: React.FC<{ x: number; y: number }> = ({ x, y }) => (
  <svg width={26} height={26} viewBox="0 0 26 26" style={{ position: "absolute", left: x, top: y, filter: "drop-shadow(0 1px 1px #0008)" }}>
    <path d="M2 2 L2 20 L7 15 L11 24 L14 22 L10 14 L17 14 Z" fill="#fff" stroke="#000" strokeWidth={1.4} />
  </svg>
);

export const WinChrome: React.FC<{
  skin: Skin;
  name: string;
  accent: string;
  width?: number;
  height?: number;
}> = ({ skin, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const { durationInFrames } = useVideoConfig();
  const open = interpolate(frame, [8, 26], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const intro = interpolate(frame, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  // drifting cursor
  const cx = width * 0.5 + Math.sin(frame / 34) * width * 0.28;
  const cy = height * 0.46 + Math.cos(frame / 27) * height * 0.22;
  const caret = Math.floor(frame / 18) % 2 === 0;
  const clock = `${9 + (Math.floor(frame / 120) % 3)}:${String(Math.floor(frame / 2) % 60).padStart(2, "0")}`;

  return (
    <div style={{ position: "relative", width, height, borderRadius: 14, overflow: "hidden", background: "#050506", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.26), opacity: intro }}>
      <Desktop skin={skin} w={width} h={height} open={open} frame={frame} clock={clock} caret={caret} accent={accent} />
      <Cursor x={cx} y={cy} />

      {/* framing chrome */}
      <div style={{ position: "absolute", right: 14, top: 12, fontFamily: MONO, fontSize: 13, letterSpacing: 2, color: theme.ink, background: "#0009", border: `1px solid ${accent}66`, borderRadius: 6, padding: "4px 9px" }}>◉ DRAWN HOMAGE</div>
      <div style={{ position: "absolute", left: 18, bottom: 14 }}>
        <div style={{ fontFamily: SANS, fontWeight: 900, fontSize: 34, color: theme.ink, textShadow: "0 2px 16px #000", lineHeight: 1 }}>{name}</div>
        <div style={{ marginTop: 7, height: 4, width: 76, background: accent, borderRadius: 2, boxShadow: glow(accent, 0.5) }} />
      </div>
    </div>
  );
};

const Win: React.FC<{ title: string; titleBg: string; titleInk?: string; body: string; children?: React.ReactNode; style?: React.CSSProperties; radius?: number; glass?: boolean }> = ({ title, titleBg, titleInk = "#fff", body, children, style, radius = 0, glass }) => (
  <div style={{ background: glass ? "rgba(236,240,255,0.1)" : body, border: glass ? "1px solid rgba(255,255,255,0.25)" : "2px solid #000", borderRadius: radius, overflow: "hidden", boxShadow: "0 18px 40px #000a", backdropFilter: glass ? "blur(2px)" : undefined, ...style }}>
    <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", background: titleBg, padding: "6px 10px" }}>
      <span style={{ fontFamily: SANS, fontWeight: 700, fontSize: 18, color: titleInk }}>{title}</span>
      <div style={{ display: "flex", gap: 5 }}>{["–", "□", "✕"].map((s, i) => <span key={i} style={{ width: 22, height: 18, background: "#d9d9d9", border: "1px solid #000", fontSize: 12, textAlign: "center", color: "#000", lineHeight: "16px" }}>{s}</span>)}</div>
    </div>
    <div style={{ padding: 14 }}>{children}</div>
  </div>
);

const Taskbar: React.FC<{ bg: string; start: React.ReactNode; clock: string; center?: boolean; ink?: string }> = ({ bg, start, clock, center, ink = "#fff" }) => (
  <div style={{ position: "absolute", left: 0, right: 0, bottom: 0, height: 44, background: bg, display: "flex", alignItems: "center", justifyContent: center ? "center" : "space-between", padding: "0 10px", borderTop: "1px solid #0006" }}>
    <div style={{ display: "flex", alignItems: "center", gap: 8 }}>{start}</div>
    {!center ? <span style={{ fontFamily: MONO, fontSize: 15, color: ink }}>{clock}</span> : null}
  </div>
);

const Desktop: React.FC<{ skin: Skin; w: number; h: number; open: number; frame: number; clock: string; caret: boolean; accent: string }> = ({ skin, w, h, open, frame, clock, caret, accent }) => {
  const winT = `scale(${0.9 + open * 0.1})`;
  const winOp = open;

  if (skin === "retro") {
    return (
      <div style={{ position: "absolute", inset: 0, background: "#0b3a3a" }}>
        <div style={{ position: "absolute", left: 40, top: 40, width: 360, opacity: winOp, transform: winT }}>
          <Win title="MS-DOS Executive" titleBg="#000" body="#c9c9c9">
            <div style={{ fontFamily: MONO, fontSize: 15, color: "#111" }}>C:\&gt;{caret ? "_" : " "}<br />DIR<br />WIN.COM  CALC.EXE<br />PAINT.EXE  CLOCK.EXE</div>
          </Win>
        </div>
        <div style={{ position: "absolute", right: 60, bottom: 70, width: 300, opacity: winOp, transform: winT }}>
          <Win title="Clock" titleBg="#000" body="#c9c9c9"><div style={{ fontFamily: MONO, fontSize: 26, color: "#111", textAlign: "center" }}>🕘 {clock}</div></Win>
        </div>
      </div>
    );
  }

  if (skin === "win9x" || skin === "nt") {
    const desk = skin === "nt" ? "#2a4a6a" : "#0e6b6b";
    return (
      <div style={{ position: "absolute", inset: 0, background: desk }}>
        {/* desktop icons */}
        <div style={{ position: "absolute", left: 18, top: 18, display: "flex", flexDirection: "column", gap: 18 }}>
          {["My Computer", "Recycle Bin", "Network"].map((t) => (
            <div key={t} style={{ width: 92, textAlign: "center" }}>
              <div style={{ margin: "0 auto", width: 40, height: 34 }}><Panes s={34} c={accent} /></div>
              <span style={{ fontFamily: SANS, fontSize: 13, color: "#fff", textShadow: "1px 1px 0 #000" }}>{t}</span>
            </div>
          ))}
        </div>
        <div style={{ position: "absolute", left: w * 0.3, top: 50, width: 440, opacity: winOp, transform: winT }}>
          <Win title="Welcome" titleBg="linear-gradient(90deg,#000080,#1080d0)" body="#c0c4c8">
            <div style={{ fontFamily: SANS, fontSize: 17, color: "#111" }}>Click the <b>Start</b> button to begin.</div>
            <div style={{ marginTop: 10, display: "flex", gap: 8 }}>
              <span style={{ background: "#d9d9d9", border: "2px outset #fff", padding: "5px 16px", fontFamily: SANS, fontSize: 15 }}>OK</span>
              <span style={{ background: "#d9d9d9", border: "2px outset #fff", padding: "5px 16px", fontFamily: SANS, fontSize: 15 }}>Cancel</span>
            </div>
          </Win>
        </div>
        <Taskbar bg="#bfc3c9" ink="#111"
          start={<span style={{ display: "flex", alignItems: "center", gap: 6, background: "#d9d9d9", border: "2px outset #fff", padding: "4px 12px", fontFamily: SANS, fontWeight: 800, fontSize: 16, color: "#111" }}><Panes s={16} c="#555" /> Start</span>}
          clock={clock} />
      </div>
    );
  }

  if (skin === "luna") {
    return (
      <div style={{ position: "absolute", inset: 0, background: "linear-gradient(#4a90e2,#8fc7f2 55%,#bfe0a8 55%,#6bbf4a)" }}>
        {/* bliss-style hill + clouds */}
        <div style={{ position: "absolute", left: -40, bottom: 44, width: w + 80, height: h * 0.4, background: "radial-gradient(120% 100% at 30% 100%, #7ec85a, #4f9e3a)", borderRadius: "60% 40% 0 0 / 100% 100% 0 0" }} />
        {[0, 1, 2].map((i) => <div key={i} style={{ position: "absolute", top: 40 + i * 30, left: ((frame * 0.3 + i * 300) % (w + 200)) - 100, width: 120, height: 34, background: "#ffffffcc", borderRadius: 999, filter: "blur(2px)" }} />)}
        <div style={{ position: "absolute", left: w * 0.32, top: 60, width: 440, opacity: winOp, transform: winT }}>
          <Win title="My Documents" titleBg="linear-gradient(#2a6fd6,#1d4ea8)" body="#eef3fb" radius={8}>
            <div style={{ fontFamily: SANS, fontSize: 17, color: "#123" }}>Luna theme — rounded, blue, and friendly. The one that stayed for 13 years.</div>
          </Win>
        </div>
        <Taskbar bg="linear-gradient(#3a6ea5,#245088)"
          start={<span style={{ display: "flex", alignItems: "center", gap: 7, background: "linear-gradient(#5cb85c,#3d8b3d)", borderRadius: "0 12px 12px 0", padding: "5px 20px 5px 12px", fontFamily: SANS, fontStyle: "italic", fontWeight: 900, fontSize: 17, color: "#fff" }}><Panes s={16} c="#fff" /> start</span>}
          clock={clock} />
      </div>
    );
  }

  if (skin === "aero") {
    return (
      <div style={{ position: "absolute", inset: 0, background: "#0a0d18" }}>
        {/* aurora ribbon */}
        <div style={{ position: "absolute", inset: 0, background: `radial-gradient(120% 80% at ${50 + Math.sin(frame / 40) * 20}% 20%, ${accent}44, transparent 60%), radial-gradient(100% 70% at 70% 60%, #2a6fd655, transparent 60%)` }} />
        <div style={{ position: "absolute", left: w * 0.3, top: 60, width: 450, opacity: winOp, transform: winT }}>
          <Win title="Aero" titleBg="rgba(255,255,255,0.14)" titleInk="#eef" body="#0000" glass radius={10}>
            <div style={{ fontFamily: SANS, fontSize: 17, color: "#eaf0ff" }}>Frosted glass, live thumbnails, and a translucent taskbar. Gorgeous — if your PC could run it.</div>
          </Win>
        </div>
        <Taskbar bg="rgba(12,16,28,0.72)"
          start={<span style={{ width: 38, height: 38, borderRadius: 999, background: `radial-gradient(circle at 35% 35%, #fff6, ${accent})`, border: "1px solid #fff4", display: "grid", placeItems: "center" }}><Panes s={16} c="#fff" /></span>}
          clock={clock} />
      </div>
    );
  }

  if (skin === "metro") {
    const tiles = [
      { c: accent, w: 2, label: "Start" }, { c: "#2d9e4b", w: 1 }, { c: "#e8731c", w: 1 },
      { c: "#8a3ffc", w: 1 }, { c: "#1aa0c4", w: 2 }, { c: "#c4305a", w: 1 },
      { c: "#3d8b3d", w: 1 }, { c: "#d8a300", w: 1 }, { c: "#5b6b7a", w: 2 },
    ];
    return (
      <div style={{ position: "absolute", inset: 0, background: "#1b1f2a", padding: 30 }}>
        <div style={{ fontFamily: SANS, fontWeight: 300, fontSize: 30, color: "#fff", marginBottom: 16 }}>Start</div>
        <div style={{ display: "flex", flexWrap: "wrap", gap: 12, width: 560, opacity: winOp }}>
          {tiles.map((t, i) => {
            const pulse = 0.85 + Math.sin(frame / 12 + i) * 0.15;
            return <div key={i} style={{ width: t.w === 2 ? 236 : 112, height: 112, background: t.c, opacity: pulse, display: "grid", placeItems: "center", fontFamily: SANS, fontWeight: 700, fontSize: 22, color: "#fff" }}>{t.label ?? <Panes s={34} c="#ffffffcc" />}</div>;
          })}
        </div>
        <div style={{ position: "absolute", right: 40, bottom: 40, fontFamily: SANS, fontSize: 20, color: "#fff9" }}>…where did the Start button go?</div>
      </div>
    );
  }

  // flat (10) + flat11
  const center = skin === "flat11";
  const wall = center
    ? "radial-gradient(120% 100% at 50% 10%, #2a3a66, #0c1020 70%)"
    : "linear-gradient(135deg,#0f2747,#123b6b)";
  return (
    <div style={{ position: "absolute", inset: 0, background: wall }}>
      <div style={{ position: "absolute", left: center ? w * 0.34 : w * 0.3, top: 56, width: 450, opacity: winOp, transform: winT }}>
        <Win title={center ? "Settings" : "This PC"} titleBg="#f3f3f3" titleInk="#111" body="#fafafa" radius={center ? 12 : 4}>
          <div style={{ fontFamily: SANS, fontSize: 17, color: "#111" }}>{center ? "Centred taskbar, rounded corners, Mica material." : "Flat chrome, tiles live in the Start menu — and \"the last Windows ever.\""}</div>
          <div style={{ marginTop: 10, height: 10, borderRadius: 5, background: `${accent}` }} />
        </Win>
      </div>
      <Taskbar bg="rgba(20,22,28,0.9)" center={center}
        start={<span style={{ width: 34, height: 34, borderRadius: 8, background: accent, display: "grid", placeItems: "center" }}><Panes s={16} c="#fff" /></span>}
        clock={clock} />
    </div>
  );
};
