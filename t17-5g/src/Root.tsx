import React from "react";
import { Composition } from "remotion";
import { Video } from "./Video";
import { ThumbA, ThumbB } from "./Thumb";
import { zInput, demoInput } from "./schema";
import "./fonts";

export const RemotionRoot: React.FC = () => (
  <>
    <Composition
      id="Video"
      component={Video as any}
      schema={zInput}
      defaultProps={demoInput as any}
      fps={60}
      width={1920}
      height={1080}
      durationInFrames={demoInput.totalFrames}
      calculateMetadata={({ props }) => ({
        durationInFrames: props.totalFrames,
        fps: props.fps,
        width: props.width,
        height: props.height,
      })}
    />
    <Composition
      id="ThumbA"
      component={ThumbA as any}
      schema={zInput}
      defaultProps={demoInput as any}
      fps={60}
      width={1920}
      height={1080}
      durationInFrames={1}
    />
    <Composition
      id="ThumbB"
      component={ThumbB as any}
      schema={zInput}
      defaultProps={demoInput as any}
      fps={60}
      width={1920}
      height={1080}
      durationInFrames={1}
    />
  </>
);
