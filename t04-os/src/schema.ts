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
  kind: z.enum(["intro", "primer", "timeline", "item", "compare", "outro"]),
  narration: z.string(),
  audioFile: z.string(),
  startFrame: z.number(),
  durationInFrames: z.number(),
  words: z.array(zWord),
  beats: z.array(zBeat),
  // a Manim clip name for this segment (intro/primer/timeline/compare)
  manim: z.string().optional(),
  // item-only
  id: z.string().optional(),
  name: z.string().optional(),
  family: z.string().optional(),
  year: z.string().optional(),
  maker: z.string().optional(),
  logo: z.string().optional(),
  image: z.string().optional(),
  highlight: z.string().optional(),
  accent: z.string().optional(),
  icon: z.string().optional(),
  specs: z.array(zSpec).optional(),
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
  images: z
    .record(z.string(), z.object({ file: z.string(), credit: z.string().optional(), source: z.string().optional() }))
    .default({}),
  logos: z
    .record(z.string(), z.object({ file: z.string(), slug: z.string().optional(), license: z.string().optional() }))
    .default({}),
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
  id: "t04-os",
  title: "Every Operating System Explained",
  series: "Every X",
  keyNoun: "Operating System",
  promise: "demo",
  accent: "#35FF9E",
  fps: 60,
  width: 1920,
  height: 1080,
  totalFrames: 360,
  sources: [],
  segments: [
    seg("intro", { startFrame: 0 }),
    seg("item", {
      startFrame: 120,
      id: "linux",
      name: "Linux",
      family: "linux",
      year: "1991",
      maker: "Linus Torvalds",
      logo: "linux",
      image: "torvalds",
      highlight: "Monolithic kernel",
      accent: "#35FF9E",
      icon: "server",
      specs: [],
      verdict: "Found on: most of the internet.",
    }),
    seg("outro", { startFrame: 240, nextVideo: "Every Dead Operating System Explained", question: "Which one are you on?" }),
  ],
  manim: {},
  coco: {},
  images: {},
  logos: {},
  chapters: [],
};
