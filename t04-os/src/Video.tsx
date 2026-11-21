import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import type { VideoInput } from "./schema";
import { InputCtx } from "./lib/ctx";
import { theme, familyColor } from "./theme";
import { Frame } from "./components/Frame";
import { Reveal } from "./components/Reveal";
import { Intro } from "./scenes/Intro";
import { Outro } from "./scenes/Outro";
import { ItemScene } from "./scenes/ItemScene";
import { InterludeScene } from "./scenes/InterludeScene";

export const Video: React.FC<VideoInput> = (input) => {
  const items = input.segments.filter((s) => s.kind === "item");
  const steps = items.map((s) => ({ icon: s.icon ?? "server", accent: familyColor(s.family) }));
  const itemIndex = new Map(items.map((s, i) => [s, i] as const));

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
            case "primer":
              node = <InterludeScene seg={seg} title="WHAT AN OS ACTUALLY DOES" accent={theme.accents.mint} />;
              break;
            case "timeline":
              node = <InterludeScene seg={seg} title="THE FAMILY TREE" accent={theme.accents.magenta} />;
              break;
            case "compare":
              node = <InterludeScene seg={seg} title="WHO ACTUALLY WINS" accent={theme.accents.violet} />;
              break;
            case "item":
            default:
              node = (
                <Frame stage={seg} sources={input.sources} steps={steps} index={itemIndex.get(seg) ?? 0} fps={input.fps} hideSpecs>
                  <ItemScene seg={seg} />
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
