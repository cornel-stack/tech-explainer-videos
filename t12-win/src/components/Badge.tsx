import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { fontStack, glow } from "../theme";
import { pop } from "../lib/anim";

// The signature device of T12: a REPUTATION badge — history's verdict on each
// Windows. Loved (the legends), Meh (the forgettable), or Hated (the duds — ME,
// Vista, 8). Same three-light system, recoloured green / amber / red.
export type Rep = "loved" | "meh" | "hated";

export const REP: Record<Rep, { tag: string; sub: string; color: string }> = {
  loved: { tag: "👑 LOVED", sub: "a classic people kept for years", color: "#35E08A" },
  meh: { tag: "😐 MEH", sub: "fine, forgettable, or divisive", color: "#FFB020" },
  hated: { tag: "💀 HATED", sub: "the one everyone skipped", color: "#FF5C47" },
};

export const repColor = (s?: string): string => REP[(s as Rep) ?? "meh"]?.color ?? REP.meh.color;

export const BadgePill: React.FC<{ status: Rep; size?: number }> = ({ status, size = 16 }) => {
  const l = REP[status] ?? REP.meh;
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 7, background: `${l.color}22`, border: `1.5px solid ${l.color}`, borderRadius: 999, padding: `${size * 0.25}px ${size * 0.6}px` }}>
      <span style={{ width: size * 0.5, height: size * 0.5, borderRadius: 999, background: l.color, boxShadow: `0 0 ${size * 0.5}px ${l.color}` }} />
      <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: l.color, letterSpacing: 1 }}>{l.tag}</span>
    </span>
  );
};

// Big badge for the item's right column — history's verdict, pulsing.
export const Badge: React.FC<{ status: Rep; at?: number }> = ({ status, at = 6 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const l = REP[status] ?? REP.meh;
  const s = pop(frame, at, fps);
  const pulse = 0.55 + Math.sin(frame / 9) * 0.45;
  return (
    <div style={{ opacity: s, transform: `translateY(${(1 - s) * 16}px)` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16, background: `${l.color}1a`, border: `2px solid ${l.color}`, borderRadius: 16, padding: "16px 22px", boxShadow: glow(l.color, 0.3) }}>
        <span style={{ width: 26, height: 26, borderRadius: 999, background: l.color, boxShadow: `0 0 ${10 + pulse * 20}px ${l.color}`, flex: "none" }} />
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 32, color: l.color, lineHeight: 1, letterSpacing: 0.5 }}>{l.tag}</span>
          <span style={{ fontFamily: fontStack.mono, fontSize: 15, color: l.color, opacity: 0.8, marginTop: 4 }}>{l.sub}</span>
        </div>
      </div>
    </div>
  );
};
