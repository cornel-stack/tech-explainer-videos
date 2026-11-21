import React from "react";
import { AbsoluteFill } from "remotion";
import { theme } from "../theme";

// Soft paper backdrop with a faint dot grid and a tinted corner glow.
export const Backdrop: React.FC<{ accent: string }> = ({ accent }) => (
  <AbsoluteFill style={{ background: theme.bg }}>
    <AbsoluteFill
      style={{
        backgroundImage: `radial-gradient(${theme.line} 1.5px, transparent 1.5px)`,
        backgroundSize: "40px 40px",
        opacity: 0.6,
      }}
    />
    <AbsoluteFill
      style={{
        background: `radial-gradient(1200px 700px at 85% -10%, ${accent}1f, transparent 60%)`,
      }}
    />
    <AbsoluteFill
      style={{
        background: `radial-gradient(900px 600px at 0% 110%, ${theme.bgDeep}, transparent 55%)`,
      }}
    />
  </AbsoluteFill>
);
