import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { InputCtx } from "./lib/ctx";
import { LogoMark } from "./components/LogoMark";
import { Peep, CAST } from "./characters/Peep";

const LOGOS: { key: string; name: string; c: string }[] = [
  { key: "windows", name: "Windows", c: theme.families.ms },
  { key: "linux", name: "Linux", c: theme.families.linux },
  { key: "android", name: "Android", c: theme.families.google },
  { key: "macos", name: "macOS", c: theme.families.apple },
  { key: "freebsd", name: "FreeBSD", c: theme.families.unix },
  { key: "steamos", name: "SteamOS", c: theme.families.other },
  { key: "chromeos", name: "ChromeOS", c: theme.families.google },
  { key: "ios", name: "iOS", c: theme.families.apple },
];

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${theme.accents.mint}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

const Tile: React.FC<{ k: string; name: string; c: string; size?: number }> = ({ k, name, c, size = 110 }) => (
  <div style={{ width: size + 60, height: size + 36, display: "grid", placeItems: "center", background: theme.paper, borderRadius: 18, border: `1px solid ${c}55`, boxShadow: glow(c, 0.3) }}>
    <LogoMark logoKey={k} name={name} color={c} size={size} />
  </div>
);

export const ThumbA: React.FC<VideoInput> = (props) => (
  <InputCtx.Provider value={props}>
    <AbsoluteFill>
      <Bg corner="tr" />
      <div style={{ position: "absolute", top: 110, left: 90 }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 32, letterSpacing: 8, color: theme.accents.mint, fontWeight: 700 }}>EVERY X</div>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
          EVERY<br />OPERATING<br /><span style={{ color: theme.accents.mint, textShadow: `0 0 50px ${theme.accents.mint}` }}>SYSTEM</span>
        </div>
        <div style={{ display: "inline-block", marginTop: 24, background: theme.accents.violet, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 38, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(theme.accents.violet, 0.6) }}>
          INCLUDING THE ONES YOU CAN'T BUY
        </div>
      </div>
      <div style={{ position: "absolute", right: 70, top: 150, width: 720, display: "flex", flexWrap: "wrap", gap: 22, justifyContent: "flex-end", alignContent: "center", height: 800 }}>
        {LOGOS.map((l) => <Tile key={l.key} k={l.key} name={l.name} c={l.c} size={100} />)}
      </div>
    </AbsoluteFill>
  </InputCtx.Provider>
);

export const ThumbB: React.FC<VideoInput> = (props) => (
  <InputCtx.Provider value={props}>
    <AbsoluteFill>
      <Bg corner="tl" />
      <div style={{ position: "absolute", top: 130, left: 90, width: 1100 }}>
        <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 130, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
          WHICH ONE
          <br />
          ARE YOU
          <br />
          <span style={{ color: theme.accents.mint, textShadow: `0 0 50px ${theme.accents.mint}` }}>RUNNING?</span>
        </div>
        <div style={{ display: "flex", gap: 18, marginTop: 34 }}>
          {LOGOS.slice(0, 4).map((l) => <Tile key={l.key} k={l.key} name={l.name} c={l.c} size={72} />)}
        </div>
      </div>
      <div style={{ position: "absolute", right: 150, bottom: 40 }}>
        <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${theme.accents.mint}`, boxShadow: glow(theme.accents.mint, 0.5) }} />
        <Peep seed={CAST.dev} size={460} />
      </div>
    </AbsoluteFill>
  </InputCtx.Provider>
);

export const Thumb = ThumbA;
