import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack } from "../theme";
import { CallPattern } from "../components/CallPattern";
import { CodeCard } from "../components/CodeCard";
import { pop } from "../lib/anim";

// One API style. Frame supplies the badge (name), spec strip, caption, verdict
// and rail; here we draw the animated call pattern, the real code, and origin.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = seg.accent ?? theme.accents.amber;
  const tagIn = pop(frame, 14, fps);
  const floatA = Math.sin(frame / 26) * 5;
  const floatB = Math.cos(frame / 30) * 6;

  return (
    <AbsoluteFill>
      {/* call-pattern diagram, upper-left band */}
      <div style={{ position: "absolute", left: 50, top: 10, width: 1180 }}>
        <CallPattern pattern={seg.pattern ?? "reqres"} accent={accent} />
      </div>

      {/* code example, lower-left */}
      <div style={{ position: "absolute", left: 60, top: 392, transform: `translateY(${floatA}px)` }}>
        <CodeCard code={seg.code ?? []} accent={accent} title={`${seg.name} · example`} width={880} />
      </div>

      {/* origin tag */}
      <div
        style={{
          position: "absolute",
          left: 990,
          top: 420,
          opacity: tagIn,
          transform: `translateY(${(1 - tagIn) * 20 + floatB}px)`,
          background: theme.paper,
          borderRadius: 16,
          border: `1px solid ${accent}44`,
          padding: "18px 24px",
          maxWidth: 380,
        }}
      >
        <div style={{ fontFamily: fontStack.mono, fontSize: 16, letterSpacing: 1.5, color: theme.inkFaint, textTransform: "uppercase" }}>
          Since {seg.year}
        </div>
        <div style={{ fontFamily: fontStack.sans, fontSize: 30, fontWeight: 800, color: theme.ink }}>{seg.who}</div>
      </div>
    </AbsoluteFill>
  );
};
