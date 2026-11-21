import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack } from "../theme";

// Signature chrome: a horizontal power ladder placing this chip in the whole
// lineup (budget → flagship → server), with a glowing marker that slides to it.
const RUNGS = [
  { label: "BUDGET", at: 0.06 },
  { label: "ENTRY", at: 0.26 },
  { label: "MAINSTREAM", at: 0.46 },
  { label: "ENTHUSIAST", at: 0.66 },
  { label: "FLAGSHIP", at: 0.83 },
  { label: "SERVER", at: 0.97 },
];
const POS: Record<string, number> = { low: 0.07, i3: 0.27, i5: 0.46, i7: 0.66, i9: 0.83, ultra: 0.57, xeon: 0.97 };

export const TierLadder: React.FC<{ tier?: string; accent: string; note?: string }> = ({ tier, accent, note }) => {
  const frame = useCurrentFrame();
  const target = tier && POS[tier] != null ? POS[tier] : -1; // -1 = off-scale (vPro)
  const slide = Math.min(1, frame / 24);
  const pos = target < 0 ? 0.5 : target * slide + 0.02;
  const pulse = 0.6 + Math.sin(frame / 8) * 0.4;

  return (
    <div style={{ width: "100%", position: "relative", paddingTop: 10 }}>
      <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkFaint, letterSpacing: 2, marginBottom: 10 }}>◂ WHERE IT SITS IN THE LINEUP ▸</div>
      <div style={{ position: "relative", height: 54 }}>
        {/* track */}
        <div style={{ position: "absolute", left: 0, right: 0, top: 10, height: 6, borderRadius: 3, background: `linear-gradient(90deg, ${theme.accents.magenta}, ${theme.accents.mint}, ${theme.accents.amber}, ${theme.accents.coral}, ${theme.accents.gold})`, opacity: 0.35 }} />
        {/* rung ticks + labels */}
        {RUNGS.map((r) => (
          <div key={r.label} style={{ position: "absolute", left: `${r.at * 100}%`, top: 0 }}>
            <div style={{ width: 2, height: 26, background: theme.line, transform: "translateX(-1px)" }} />
            <div style={{ position: "absolute", top: 30, left: 0, transform: "translateX(-50%)", fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, whiteSpace: "nowrap" }}>{r.label}</div>
          </div>
        ))}
        {/* marker */}
        {target >= 0 ? (
          <div style={{ position: "absolute", left: `${pos * 100}%`, top: -4 }}>
            <div style={{ width: 20, height: 20, borderRadius: 999, background: accent, transform: "translateX(-50%)", boxShadow: `0 0 ${10 + pulse * 18}px ${accent}` }} />
            <div style={{ position: "absolute", top: 24, left: 0, transform: "translateX(-50%)", fontFamily: fontStack.sans, fontWeight: 900, fontSize: 18, color: accent, whiteSpace: "nowrap" }}>▲ YOU</div>
          </div>
        ) : (
          <div style={{ position: "absolute", right: 0, top: 2, fontFamily: fontStack.mono, fontSize: 16, color: accent }}>⚑ a PLATFORM — off the power ladder</div>
        )}
      </div>
      {note ? <div style={{ fontFamily: fontStack.mono, fontSize: 15, color: theme.inkSoft, marginTop: 24 }}>{note}</div> : null}
    </div>
  );
};
