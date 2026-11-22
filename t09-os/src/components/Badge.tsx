import React from "react";
import { useCurrentFrame, useVideoConfig } from "remotion";
import { fontStack, glow } from "../theme";
import { pop } from "../lib/anim";

// The signature device of this video: a three-colour LEGAL-STATUS badge.
//   red   = illegal to distribute or possess (piracy builds, Phantom Secure)
//   amber = legal to own, illegal to MISUSE (Kali, Parrot, Tails, Whonix)
//   green = legal, but state-controlled or banned somewhere (Red Star, Astra…)
export type Legal = "red" | "amber" | "green";

export const LEGAL: Record<Legal, { tag: string; sub: string; color: string }> = {
  red: { tag: "ILLEGAL", sub: "to distribute / possess", color: "#FF5C47" },
  amber: { tag: "DUAL-USE", sub: "legal to own · illegal to misuse", color: "#FFB020" },
  green: { tag: "LEGAL*", sub: "*state-controlled / banned somewhere", color: "#35E08A" },
};

export const legalColor = (s?: string): string => LEGAL[(s as Legal) ?? "green"]?.color ?? LEGAL.green.color;

// Small pill used on the grid / thumbnail.
export const BadgePill: React.FC<{ status: Legal; size?: number }> = ({ status, size = 16 }) => {
  const l = LEGAL[status] ?? LEGAL.green;
  return (
    <span style={{ display: "inline-flex", alignItems: "center", gap: 7, background: `${l.color}22`, border: `1.5px solid ${l.color}`, borderRadius: 999, padding: `${size * 0.25}px ${size * 0.6}px` }}>
      <span style={{ width: size * 0.5, height: size * 0.5, borderRadius: 999, background: l.color, boxShadow: `0 0 ${size * 0.5}px ${l.color}` }} />
      <span style={{ fontFamily: fontStack.mono, fontWeight: 800, fontSize: size, color: l.color, letterSpacing: 1 }}>{l.tag}</span>
    </span>
  );
};

// Big badge for the item's right column — a traffic-light chip that pulses.
export const Badge: React.FC<{ status: Legal; at?: number }> = ({ status, at = 6 }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const l = LEGAL[status] ?? LEGAL.green;
  const s = pop(frame, at, fps);
  const pulse = 0.55 + Math.sin(frame / 9) * 0.45;
  return (
    <div style={{ opacity: s, transform: `translateY(${(1 - s) * 16}px)` }}>
      <div style={{ display: "flex", alignItems: "center", gap: 16, background: `${l.color}1a`, border: `2px solid ${l.color}`, borderRadius: 16, padding: "16px 22px", boxShadow: glow(l.color, 0.3) }}>
        <span style={{ width: 26, height: 26, borderRadius: 999, background: l.color, boxShadow: `0 0 ${10 + pulse * 20}px ${l.color}`, flex: "none" }} />
        <div style={{ display: "flex", flexDirection: "column" }}>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 34, color: l.color, lineHeight: 1, letterSpacing: 0.5 }}>{l.tag}</span>
          <span style={{ fontFamily: fontStack.mono, fontSize: 15, color: l.color, opacity: 0.8, marginTop: 4 }}>{l.sub}</span>
        </div>
      </div>
    </div>
  );
};
