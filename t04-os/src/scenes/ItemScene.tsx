import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Segment } from "../schema";
import { theme, fontStack, familyColor } from "../theme";
import { LogoMark } from "../components/LogoMark";
import { KernelStack } from "../components/KernelStack";
import { ScreenCard } from "../components/ScreenCard";
import { pop } from "../lib/anim";

// One operating system. Frame supplies badge/caption/verdict/rail (specs hidden —
// rendered here). Left: real logo + origin + the kernel/userland schematic with
// this OS's distinctive layer lit. Right: a real context image + spec grid.
export const ItemScene: React.FC<{ seg: Segment }> = ({ seg }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const accent = familyColor(seg.family);
  const specs = seg.specs ?? [];
  const head = pop(frame, 4, fps);

  return (
    <AbsoluteFill>
      {/* LEFT: logo + origin + schematic */}
      <div style={{ position: "absolute", left: 40, top: 8, display: "flex", alignItems: "center", gap: 22, opacity: head, transform: `translateY(${(1 - head) * 16}px)` }}>
        <LogoMark logoKey={seg.logo} name={seg.name ?? ""} color={accent} size={92} />
        <div>
          <div style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkFaint, letterSpacing: 2 }}>
            {seg.year} · {seg.maker}
          </div>
          <div style={{ fontFamily: fontStack.sans, fontSize: 46, fontWeight: 900, color: theme.ink, lineHeight: 1 }}>
            {seg.name}
          </div>
        </div>
      </div>
      <div style={{ position: "absolute", left: 40, top: 150 }}>
        <KernelStack highlight={seg.highlight ?? "runtime"} accent={accent} width={1010} height={470} />
      </div>

      {/* RIGHT: real image + specs */}
      <div style={{ position: "absolute", left: 1110, top: 8 }}>
        <ScreenCard caseKey={seg.image} caseName={seg.maker ?? ""} header="IN THE WILD" accent={accent} width={770} height={360} />
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: 12, marginTop: 14, width: 770 }}>
          {specs.slice(0, 4).map((sp, i) => {
            const s = pop(frame, sp.atFrame, fps);
            if (s < 0.001) return null;
            return (
              <div key={i} style={{ opacity: s, transform: `translateY(${(1 - s) * 14}px)`, background: theme.paper, borderLeft: `4px solid ${accent}`, borderRadius: 8, padding: "9px 14px" }}>
                <div style={{ fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint, letterSpacing: 1, textTransform: "uppercase" }}>{sp.label}</div>
                <div style={{ fontFamily: fontStack.sans, fontSize: 21, fontWeight: 800, color: theme.ink, lineHeight: 1.1 }}>{sp.value}</div>
              </div>
            );
          })}
        </div>
      </div>
    </AbsoluteFill>
  );
};
