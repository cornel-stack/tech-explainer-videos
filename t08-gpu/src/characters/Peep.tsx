import React from "react";
import { peepSvg } from "../lib/dicebear";

// A member of the human cast, drawn with Open Peeps. Seeds are fixed per role
// (see cast below) so "You" and "the Waiter" stay the same person throughout.
export const Peep: React.FC<{
  seed: string;
  size?: number;
  flip?: boolean;
  bob?: number; // vertical bob offset in px (idle-breathing feel)
  tilt?: number; // degrees
  style?: React.CSSProperties;
}> = ({ seed, size = 260, flip = false, bob = 0, tilt = 0, style }) => {
  const html = peepSvg(seed);
  return (
    <div
      style={{
        width: size,
        height: size,
        transform: `translateY(${bob}px) rotate(${tilt}deg) scaleX(${flip ? -1 : 1})`,
        filter: "drop-shadow(0 14px 22px rgba(17,19,24,0.14))",
        ...style,
      }}
      dangerouslySetInnerHTML={{ __html: html }}
    />
  );
};

// The recurring cast. One seed per role keeps faces consistent across scenes.
export const CAST = {
  you: "Nova-client-2025",
  waiter: "Milo-waiter-77",
  dev: "Ada-dev-404",
  traveler: "Kai-traveler-9",
} as const;
