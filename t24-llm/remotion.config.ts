import { Config } from "@remotion/cli/config";

Config.setVideoImageFormat("jpeg");
Config.setOverwriteOutput(true);
// three.js scenes need a GL backend in headless Chromium. On CI runners with no
// GPU, "angle" fails ("WebGL context could not be created"); "swangle" (software
// ANGLE / SwiftShader) is Remotion's recommended headless WebGL backend.
Config.setChromiumOpenGlRenderer("swangle");
// Public assets (audio, coco svgs, manim clips) live here.
Config.setPublicDir("public");

export default Config;
