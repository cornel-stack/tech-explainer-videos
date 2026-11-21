import React from "react";

// Flat, hand-built line glyphs — our own marks, no vendor logos.
// viewBox 0 0 100 100, stroke-based so they tint to any accent.
const PATHS: Record<string, React.ReactNode> = {
  messenger: <path d="M12 50 L88 18 L66 86 L50 60 L30 70 Z" />,
  waiter: (
    <>
      <circle cx="50" cy="30" r="7" />
      <path d="M50 37 V54 M28 60 H72 M34 60 l-6 22 M66 60 l6 22" />
      <ellipse cx="50" cy="56" rx="26" ry="6" />
    </>
  ),
  envelope: (
    <>
      <rect x="14" y="26" width="72" height="48" rx="6" />
      <path d="M16 30 L50 54 L84 30" />
    </>
  ),
  terminal: (
    <>
      <rect x="12" y="20" width="76" height="60" rx="8" />
      <path d="M26 44 L38 54 L26 64 M48 66 H70" />
    </>
  ),
  fanout: (
    <>
      <circle cx="20" cy="50" r="9" />
      <circle cx="82" cy="24" r="7" />
      <circle cx="82" cy="50" r="7" />
      <circle cx="82" cy="76" r="7" />
      <path d="M29 48 L73 26 M29 50 H73 M29 52 L73 74" />
    </>
  ),
  hub: (
    <>
      <circle cx="50" cy="50" r="12" />
      <circle cx="50" cy="16" r="6" />
      <circle cx="84" cy="50" r="6" />
      <circle cx="50" cy="84" r="6" />
      <circle cx="16" cy="50" r="6" />
      <path d="M50 38 V22 M62 50 H78 M50 62 V78 M38 50 H22" />
    </>
  ),
  laptop: (
    <>
      <rect x="22" y="24" width="56" height="38" rx="4" />
      <path d="M12 74 H88 L82 62 H18 Z" />
    </>
  ),
  server: (
    <>
      <rect x="22" y="20" width="56" height="18" rx="4" />
      <rect x="22" y="42" width="56" height="18" rx="4" />
      <rect x="22" y="64" width="56" height="18" rx="4" />
      <circle cx="33" cy="29" r="2.5" />
      <circle cx="33" cy="51" r="2.5" />
      <circle cx="33" cy="73" r="2.5" />
    </>
  ),
  cloud: (
    <path d="M30 70 a18 18 0 0 1 0-36 a22 22 0 0 1 42 6 a15 15 0 0 1 -4 30 Z" />
  ),
  phone: (
    <>
      <rect x="32" y="12" width="36" height="76" rx="8" />
      <path d="M44 78 H56" />
    </>
  ),
  check: <path d="M24 52 L44 72 L78 30" />,
  cross: <path d="M30 30 L70 70 M70 30 L30 70" />,
  clock: (
    <>
      <circle cx="50" cy="50" r="34" />
      <path d="M50 30 V50 L66 60" />
    </>
  ),
  arrow: <path d="M18 50 H78 M60 32 L82 50 L60 68" />,
  doors: (
    <>
      <rect x="24" y="20" width="24" height="60" rx="3" />
      <rect x="52" y="20" width="24" height="60" rx="3" />
      <circle cx="43" cy="50" r="2.5" />
      <circle cx="57" cy="50" r="2.5" />
    </>
  ),
};

export const Icon: React.FC<{
  name: string;
  size?: number;
  color?: string;
  strokeWidth?: number;
  fill?: string;
}> = ({ name, size = 48, color = "#EDE7DB", strokeWidth = 7, fill = "none" }) => (
  <svg
    width={size}
    height={size}
    viewBox="0 0 100 100"
    fill={fill}
    stroke={color}
    strokeWidth={strokeWidth}
    strokeLinecap="round"
    strokeLinejoin="round"
  >
    {PATHS[name] ?? PATHS.hub}
  </svg>
);
