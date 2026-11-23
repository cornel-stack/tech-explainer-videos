import React from "react";
import { AbsoluteFill, OffthreadVideo, Loop, staticFile, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, glow } from "../theme";
import { CodeCard } from "../components/CodeCard";
import { useInput } from "../lib/ctx";
import { pop } from "../lib/anim";

// One Kubernetes stage of the ONE growing diagram. LEFT: the animated Manim
// diagram for this stage (the cluster building, the control plane, the request
// path, the reconciliation loop, a rolling update, the trade-offs). RIGHT: either
// the Deployment YAML (the one artefact you actually write) or the sourced specs
// — each popping in at the exact frame its number is spoken.
export const StageScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const input = useInput();
  const accent = seg.accent ?? theme.accents.mint;
  const clip = seg.manim ? input.manim?.[seg.manim] : undefined;
  const specs = seg.specs ?? [];
  const code = seg.code;

  const Spec: React.FC<{ sp: (typeof specs)[number] }> = ({ sp }) => {
    const s = pop(frame, sp.atFrame, fps);
    if (s < 0.001) return null;
    return (
      <div style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "12px 16px" }}>
        <div style={{ fontFamily: fontStack.mono, fontSize: 14, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
        <div style={{ fontFamily: fontStack.sans, fontSize: 24, fontWeight: 800, color: theme.ink, lineHeight: 1.12 }}>{sp.value}</div>
      </div>
    );
  };

  return (
    <AbsoluteFill>
      {/* LEFT: the animated diagram */}
      <div style={{ position: "absolute", left: 40, top: 150 }}>
        {clip ? (
          <div style={{ width: 1030, height: 505, borderRadius: 14, overflow: "hidden", border: `1px solid ${accent}44`, boxShadow: glow(accent, 0.25) }}>
            <Loop durationInFrames={Math.max(1, clip.durationInFrames)}>
              <OffthreadVideo src={staticFile(clip.file)} muted style={{ width: "100%", height: "100%", objectFit: "cover" }} />
            </Loop>
          </div>
        ) : (
          <div style={{ width: 1030, height: 505, background: "#070809", borderRadius: 14, border: `1px solid ${accent}44`, display: "grid", placeItems: "center" }}>
            <span style={{ fontFamily: fontStack.mono, fontSize: 90, color: `${accent}44` }}>⎈</span>
          </div>
        )}
      </div>

      {/* RIGHT: YAML (deploy stage) + specs, or a taller spec stack */}
      <div style={{ position: "absolute", left: 1110, top: 150, width: 770, display: "flex", flexDirection: "column", gap: 14 }}>
        {code ? (
          <>
            <CodeCard code={code} accent={accent} title="deployment.yaml" width={770} />
            <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12 }}>
              {specs.slice(0, 2).map((sp, i) => <Spec key={i} sp={sp} />)}
            </div>
          </>
        ) : (
          <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
            {specs.slice(0, 4).map((sp, i) => <Spec key={i} sp={sp} />)}
          </div>
        )}
      </div>
    </AbsoluteFill>
  );
};
