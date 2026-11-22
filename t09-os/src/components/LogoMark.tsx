import React from "react";
import { staticFile } from "remotion";
import { theme, fontStack } from "../theme";
import { useInput } from "../lib/ctx";

// Shows a real brand logo (fetched CC0 Simple Icons SVG), tinted to `color` via a
// CSS mask so the monochrome mark reads on the dark panel. Falls back to a typeset
// wordmark (never a redrawn logo) when no licensed mark was fetched.
export const LogoMark: React.FC<{
  logoKey?: string;
  name: string;
  color: string;
  size?: number;
}> = ({ logoKey, name, color, size = 120 }) => {
  const input = useInput();
  const lg = logoKey ? input.logos?.[logoKey] : undefined;

  if (lg) {
    const url = staticFile(lg.file);
    return (
      <div
        style={{
          width: size,
          height: size,
          backgroundColor: color,
          WebkitMaskImage: `url(${url})`,
          maskImage: `url(${url})`,
          WebkitMaskRepeat: "no-repeat",
          maskRepeat: "no-repeat",
          WebkitMaskSize: "contain",
          maskSize: "contain",
          WebkitMaskPosition: "center",
          maskPosition: "center",
          filter: `drop-shadow(0 0 16px ${color}66)`,
        }}
      />
    );
  }

  // wordmark fallback
  return (
    <div
      style={{
        height: size,
        minWidth: size,
        padding: "0 18px",
        display: "flex",
        alignItems: "center",
        justifyContent: "center",
        borderRadius: 16,
        border: `2px solid ${color}`,
        color,
        fontFamily: fontStack.mono,
        fontWeight: 700,
        fontSize: size * 0.3,
        letterSpacing: 1,
        background: theme.paper,
      }}
    >
      {name}
    </div>
  );
};
