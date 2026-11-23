import React from "react";
import { AbsoluteFill, useCurrentFrame, interpolate, Easing } from "remotion";

// Gives every segment a motion in/out so cuts never feel like static slides:
// the scene scales + slides + fades in, and fades out at the end (a quick dip
// to background between segments). Timing is unchanged (no overlap).
export const Reveal: React.FC<{ dur: number; children: React.ReactNode }> = ({ dur, children }) => {
  const frame = useCurrentFrame();
  const inO = interpolate(frame, [0, 14], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  const inScale = interpolate(frame, [0, 18], [1.06, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const inY = interpolate(frame, [0, 18], [40, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp", easing: Easing.out(Easing.cubic) });
  const outO = interpolate(frame, [dur - 9, dur], [1, 0], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
  return (
    <AbsoluteFill style={{ opacity: Math.min(inO, outO), transform: `translateY(${inY}px) scale(${inScale})`, transformOrigin: "center" }}>
      {children}
    </AbsoluteFill>
  );
};
