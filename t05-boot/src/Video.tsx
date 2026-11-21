import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import type { VideoInput } from "./schema";
import { InputCtx } from "./lib/ctx";
import { theme, phaseColor } from "./theme";
import { Frame } from "./components/Frame";
import { Reveal } from "./components/Reveal";
import { Intro } from "./scenes/Intro";
import { Outro } from "./scenes/Outro";
import { StageScene } from "./scenes/StageScene";

export const Video: React.FC<VideoInput> = (input) => {
  const stages = input.segments.filter((s) => s.kind === "stage");
  const steps = stages.map((s) => ({ icon: s.icon ?? "server", accent: s.accent ?? phaseColor(s.phase) }));
  const stageIndex = new Map(stages.map((s, i) => [s, i] as const));

  return (
    <InputCtx.Provider value={input}>
      <AbsoluteFill style={{ background: theme.bg }}>
        {input.segments.map((seg, i) => {
          let node: React.ReactNode;
          switch (seg.kind) {
            case "intro":
              node = <Intro seg={seg} />;
              break;
            case "outro":
              node = <Outro seg={seg} />;
              break;
            case "stage":
            default:
              node = (
                <Frame stage={seg} sources={input.sources} steps={steps} index={stageIndex.get(seg) ?? 0} fps={input.fps}>
                  <StageScene seg={seg} />
                </Frame>
              );
          }
          return (
            <Sequence key={i} from={seg.startFrame} durationInFrames={seg.durationInFrames}>
              <Reveal dur={seg.durationInFrames}>{node}</Reveal>
            </Sequence>
          );
        })}
      </AbsoluteFill>
    </InputCtx.Provider>
  );
};
