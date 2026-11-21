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

export const zSource = z.object({ id: z.string(), label: z.string(), url: z.string() });

// One timeline segment. `kind` picks the scene; item-only fields are optional.
export const zSegment = z.object({
  kind: z.enum(["intro", "axis", "item", "compare", "decision", "outro"]),
  narration: z.string(),
  audioFile: z.string(),
  startFrame: z.number(),
  durationInFrames: z.number(),
  words: z.array(zWord),
  beats: z.array(zBeat),
  // item-only
  id: z.string().optional(),
  name: z.string().optional(),
  year: z.string().optional(),
  who: z.string().optional(),
  pattern: z.string().optional(),
  accent: z.string().optional(),
  icon: z.string().optional(),
  specs: z.array(zSpec).optional(),
  code: z.array(z.string()).optional(),
  verdict: z.string().optional(),
  // outro-only
  nextVideo: z.string().optional(),
  question: z.string().optional(),
});

export const zManimClip = z.object({ file: z.string(), durationInFrames: z.number() });

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
  segments: z.array(zSegment),
  manim: z.record(z.string(), zManimClip).default({}),
  coco: z.record(z.string(), z.string()).default({}),
  chapters: z.array(z.object({ title: z.string(), startSeconds: z.number() })),
});

export type Word = z.infer<typeof zWord>;
export type BeatT = z.infer<typeof zBeat>;
export type Spec = z.infer<typeof zSpec>;
export type Source = z.infer<typeof zSource>;
export type Segment = z.infer<typeof zSegment>;
export type VideoInput = z.infer<typeof zInput>;

const seg = (kind: Segment["kind"], extra: Partial<Segment> = {}): Segment => ({
  kind,
  narration: "demo",
  audioFile: "",
  startFrame: 0,
  durationInFrames: 120,
  words: [],
  beats: [],
  ...extra,
});

export const demoInput: VideoInput = {
  id: "t02-styles",
  title: "Every API Style Explained",
  series: "Every X",
  keyNoun: "API Style",
  promise: "demo",
  accent: "#FF3E7F",
  fps: 60,
  width: 1920,
  height: 1080,
  totalFrames: 360,
  sources: [],
  segments: [
    seg("intro", { startFrame: 0 }),
    seg("item", {
      startFrame: 120,
      id: "rest",
      name: "REST",
      year: "2000",
      who: "Roy Fielding",
      pattern: "reqres",
      accent: "#FFC24B",
      icon: "arrow",
      specs: [],
      code: ["GET /users/1", "200 OK"],
      verdict: "Use it for public, cacheable APIs.",
    }),
    seg("outro", { startFrame: 240, nextVideo: "Every API Authentication Method", question: "Which does your app use?" }),
  ],
  manim: {},
  coco: {},
  chapters: [],
};
