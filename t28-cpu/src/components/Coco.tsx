import React from "react";
import { Img, staticFile } from "remotion";
import { useInput } from "../lib/ctx";

// A Coco Material "figure doing an activity" illustration. Renders only if the
// fetcher pulled it (input.coco[name]); otherwise nothing, so scenes never blank.
export const Coco: React.FC<{
  name: string;
  width?: number;
  style?: React.CSSProperties;
}> = ({ name, width = 420, style }) => {
  const input = useInput();
  const file = input.coco?.[name];
  if (!file) return null;
  return <Img src={staticFile(file)} style={{ width, ...style }} />;
};
