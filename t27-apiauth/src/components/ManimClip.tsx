import React from "react";
import { OffthreadVideo, Sequence, staticFile } from "remotion";
import { useInput } from "../lib/ctx";

// Drops a pre-rendered Manim clip into the scene, starting at `from` (frames,
// scene-relative). Renders nothing if the clip wasn't produced — scenes always
// supply a native fallback so the frame is never blank.
export const ManimClip: React.FC<{
  name: string;
  from: number;
  width?: number;
  style?: React.CSSProperties;
}> = ({ name, from, width, style }) => {
  const input = useInput();
  const clip = input.manim?.[name];
  if (!clip) return null;
  return (
    <Sequence from={from} layout="none">
      <OffthreadVideo
        src={staticFile(clip.file)}
        style={{ width: width ?? "100%", ...style }}
        muted
      />
    </Sequence>
  );
};

// Whether a named Manim clip is available this render.
export const useHasClip = (name: string) => {
  const input = useInput();
  return Boolean(input.manim?.[name]);
};

// A Manim clip as a seamless FULL-FRAME centerpiece. The clip's own background
// is the exact scene background, so it blends; the stage chrome overlays it.
// The negative offsets cancel the Frame's central-band insets to fill 1920x1080.
export const ManimFull: React.FC<{ name: string }> = ({ name }) => (
  <div style={{ position: "absolute", top: -150, bottom: -210, left: 0, right: 0 }}>
    <ManimClip
      name={name}
      from={0}
      style={{ width: "100%", height: "100%", objectFit: "cover" }}
    />
  </div>
);
