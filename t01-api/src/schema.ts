import { z } from "zod";

export const zWord = z.object({
  text: z.string(),
  startFrame: z.number(),
  endFrame: z.number(),
});

export const zBeat = z.object({ mark: z.string(), atFrame: z.number() });

export const zSpec = z.object({
  label: z.string(),
  value: z.string(),
  atFrame: z.number(),
  source: z.string().optional(),
});

export const zSource = z.object({
  id: z.string(),
  label: z.string(),
  url: z.string(),
});

const timed = {
  narration: z.string(),
  audioFile: z.string(),
  startFrame: z.number(),
  durationInFrames: z.number(),
  words: z.array(zWord),
  beats: z.array(zBeat),
};

export const zStage = z.object({
  ...timed,
  id: z.string(),
  scene: z.string(),
  chapter: z.string(),
  icon: z.string(),
  accent: z.string(),
  specs: z.array(zSpec),
  verdict: z.string(),
  request: z.any().optional(),
  styles: z.any().optional(),
});

export const zIntro = z.object({ ...timed });
export const zOutro = z.object({
  ...timed,
  nextVideo: z.string(),
  question: z.string(),
});

export const zManimClip = z.object({
  file: z.string(),
  durationInFrames: z.number(),
});

export const zInput = z.object({
  id: z.string(),
  title: z.string(),
  series: z.string(),
  keyNoun: z.string(),
  promise: z.string(),
  accent: z.string(),
  fps: z.number(),
  width: z.number(),
  height: z.number(),
  totalFrames: z.number(),
  sources: z.array(zSource),
  intro: zIntro,
  stages: z.array(zStage),
  outro: zOutro,
  manim: z.record(z.string(), zManimClip).default({}),
  coco: z.record(z.string(), z.string()).default({}),
  chapters: z.array(z.object({ title: z.string(), startSeconds: z.number() })),
});

export type Word = z.infer<typeof zWord>;
export type BeatT = z.infer<typeof zBeat>;
export type Spec = z.infer<typeof zSpec>;
export type Source = z.infer<typeof zSource>;
export type Stage = z.infer<typeof zStage>;
export type Intro = z.infer<typeof zIntro>;
export type Outro = z.infer<typeof zOutro>;
export type VideoInput = z.infer<typeof zInput>;

// Minimal valid props so Studio / typecheck work before the synth has run.
// Real renders always pass --props=render-input.json.
export const demoInput: VideoInput = {
  id: "t01-api",
  title: "What Is an API?",
  series: "How It Works",
  keyNoun: "API",
  promise: "Watch a real API call happen.",
  accent: "#2563EB",
  fps: 60,
  width: 1920,
  height: 1080,
  totalFrames: 300,
  sources: [],
  intro: {
    narration: "demo",
    audioFile: "",
    startFrame: 0,
    durationInFrames: 120,
    words: [],
    beats: [],
  },
  stages: [
    {
      id: "what",
      scene: "what",
      chapter: "What an API is",
      icon: "messenger",
      accent: "#2563EB",
      narration: "demo",
      audioFile: "",
      startFrame: 120,
      durationInFrames: 120,
      words: [],
      beats: [],
      specs: [],
      verdict: "An API is a contract.",
    },
  ],
  outro: {
    narration: "demo",
    audioFile: "",
    startFrame: 240,
    durationInFrames: 60,
    words: [],
    beats: [],
    nextVideo: "Every API Style Explained",
    question: "Which style first?",
  },
  manim: {},
  coco: {},
  chapters: [],
};
