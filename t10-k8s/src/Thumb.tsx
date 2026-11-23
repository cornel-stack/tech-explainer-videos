import React from "react";
import { AbsoluteFill } from "remotion";
import type { VideoInput } from "./schema";
import { theme, fontStack, glow } from "./theme";
import { Peep, CAST } from "./characters/Peep";

const MINT = theme.accents.mint;
const VIOLET = theme.accents.violet;
const TEAL = "#2DD4BF";

// A little drawn pod (rounded hexish) — our own mark, no Kubernetes logo.
const Pod: React.FC<{ s?: number; c?: string }> = ({ s = 26, c = TEAL }) => (
  <div style={{ width: s, height: s * 0.9, background: `${c}22`, border: `2px solid ${c}`, borderRadius: s * 0.3, boxShadow: glow(c, 0.4) }} />
);

const NodeBox: React.FC<{ pods?: number; w?: number }> = ({ pods = 3, w = 150 }) => (
  <div style={{ width: w, background: theme.paper, border: `2px solid ${MINT}`, borderRadius: 12, padding: 12, boxShadow: glow(MINT, 0.3) }}>
    <div style={{ fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint, marginBottom: 8, letterSpacing: 1 }}>NODE</div>
    <div style={{ display: "flex", gap: 8, flexWrap: "wrap" }}>{Array.from({ length: pods }).map((_, i) => <Pod key={i} />)}</div>
  </div>
);

// A compact cluster diagram for the thumbnail: control plane over two nodes.
const MiniCluster: React.FC = () => (
  <div style={{ position: "relative", padding: 22, border: `3px dashed ${MINT}`, borderRadius: 20, background: "#0b0d0c" }}>
    <div style={{ position: "absolute", top: -16, left: 20, background: theme.bg, padding: "0 10px", fontFamily: fontStack.mono, fontSize: 18, color: MINT, letterSpacing: 2 }}>CLUSTER</div>
    <div style={{ background: `${VIOLET}1a`, border: `2px solid ${VIOLET}`, borderRadius: 12, padding: "12px 18px", marginBottom: 18, textAlign: "center", fontFamily: fontStack.sans, fontWeight: 800, fontSize: 24, color: VIOLET, boxShadow: glow(VIOLET, 0.3) }}>CONTROL PLANE</div>
    <div style={{ display: "flex", gap: 18 }}>
      <NodeBox pods={3} />
      <NodeBox pods={2} />
    </div>
  </div>
);

const Bg: React.FC<{ corner?: "tr" | "tl" }> = ({ corner = "tr" }) => (
  <>
    <AbsoluteFill style={{ background: theme.bg }} />
    <AbsoluteFill style={{ background: `radial-gradient(1400px 900px at ${corner === "tr" ? "100% 0%" : "0% 0%"}, ${MINT}22, transparent 60%)` }} />
    <AbsoluteFill style={{ backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`, backgroundSize: "46px 46px", opacity: 0.4 }} />
  </>
);

export const ThumbA: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tr" />
    <div style={{ position: "absolute", top: 130, left: 90, width: 980 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 34, letterSpacing: 8, color: MINT, fontWeight: 700 }}>▦ HOW IT WORKS</div>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.9, color: theme.ink, letterSpacing: -4, marginTop: 6 }}>
        HOW<br /><span style={{ color: MINT, textShadow: `0 0 50px ${MINT}` }}>KUBERNETES</span><br />WORKS
      </div>
      <div style={{ display: "inline-block", marginTop: 24, background: VIOLET, color: theme.onAccent, fontFamily: fontStack.sans, fontWeight: 900, fontSize: 40, padding: "12px 26px", borderRadius: 12, transform: "rotate(-3deg)", boxShadow: glow(VIOLET, 0.6) }}>
        THE DIAGRAM THAT MAKES IT OBVIOUS
      </div>
    </div>
    <div style={{ position: "absolute", right: 70, top: 300, transform: "scale(1.15)" }}>
      <MiniCluster />
    </div>
  </AbsoluteFill>
);

export const ThumbB: React.FC<VideoInput> = () => (
  <AbsoluteFill>
    <Bg corner="tl" />
    <div style={{ position: "absolute", top: 150, left: 90, width: 1050 }}>
      <div style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 118, lineHeight: 0.92, color: theme.ink, letterSpacing: -4 }}>
        DESIRED <span style={{ color: MINT }}>10</span>
        <br />
        ACTUAL <span style={{ color: theme.accents.coral }}>8</span> <span style={{ color: MINT }}>→ 10</span>
      </div>
      <div style={{ marginTop: 24, fontFamily: fontStack.mono, fontSize: 40, fontWeight: 700, color: theme.inkSoft }}>self-healing, explained</div>
      <div style={{ display: "flex", gap: 10, marginTop: 28 }}>
        {Array.from({ length: 10 }).map((_, i) => <Pod key={i} s={44} c={i < 8 ? TEAL : theme.accents.coral} />)}
      </div>
    </div>
    <div style={{ position: "absolute", right: 150, bottom: 40 }}>
      <div style={{ position: "absolute", right: -10, top: -10, width: 500, height: 500, borderRadius: 999, border: `12px solid ${MINT}`, boxShadow: glow(MINT, 0.5) }} />
      <Peep seed={CAST.dev} size={460} />
    </div>
  </AbsoluteFill>
);

export const Thumb = ThumbA;
