import React from "react";
import { AbsoluteFill, Sequence } from "remotion";
import type { VideoInput, Stage } from "./schema";
import { InputCtx } from "./lib/ctx";
import { Frame } from "./components/Frame";
import { Intro } from "./scenes/Intro";
import { Outro } from "./scenes/Outro";
import { WhatScene } from "./scenes/WhatScene";
import { RestaurantScene } from "./scenes/RestaurantScene";
import { AnatomyScene } from "./scenes/AnatomyScene";
import { RealCallScene } from "./scenes/RealCallScene";
import { WhyScene } from "./scenes/WhyScene";
import { StylesScene } from "./scenes/StylesScene";

const SCENES: Record<string, React.FC<{ stage: Stage }>> = {
  what: WhatScene,
  restaurant: RestaurantScene,
  anatomy: AnatomyScene,
  realcall: RealCallScene,
  why: WhyScene,
  styles: StylesScene,
};

export const Video: React.FC<VideoInput> = (input) => {
  const steps = input.stages.map((s) => ({ icon: s.icon, accent: s.accent }));
  return (
    <InputCtx.Provider value={input}>
      <AbsoluteFill style={{ background: "#F2F4F6" }}>
        <Sequence from={input.intro.startFrame} durationInFrames={input.intro.durationInFrames}>
          <Intro />
        </Sequence>

        {input.stages.map((stage, i) => {
          const Scene = SCENES[stage.scene] ?? WhatScene;
          return (
            <Sequence key={stage.id} from={stage.startFrame} durationInFrames={stage.durationInFrames}>
              <Frame stage={stage} sources={input.sources} steps={steps} index={i} fps={input.fps}>
                <Scene stage={stage} />
              </Frame>
            </Sequence>
          );
        })}

        <Sequence from={input.outro.startFrame} durationInFrames={input.outro.durationInFrames}>
          <Outro />
        </Sequence>
      </AbsoluteFill>
    </InputCtx.Provider>
  );
};
