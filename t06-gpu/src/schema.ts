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
  kind: z.enum(["intro", "stage", "outro"]),
  narration: z.string(),
  audioFile: z.string(),
  startFrame: z.number(),
  durationInFrames: z.number(),
  words: z.array(zWord),
  beats: z.array(zBeat),
  // a Manim clip name for this segment (intro + diagram stages)
  manim: z.string().optional(),
  // stage-only
  id: z.string().optional(),
  name: z.string().optional(),
  phase: z.string().optional(),
  msStart: z.number().optional(),
  msEnd: z.number().optional(),
  chainStep: z.number().optional(),
  stepDetail: z.array(z.string()).optional(),
  image: z.string().optional(),
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
  id: "t05-boot",
  title: "How an Operating System Works",
  series: "How It Works",
  keyNoun: "Boot",
  promise: "demo",
  accent: "#FFB020",
  fps: 60,
  width: 1920,
  height: 1080,
  totalFrames: 360,
  sources: [],
  segments: [
    seg("intro", { startFrame: 0 }),
    seg("stage", {
      startFrame: 120,
      id: "post",
      name: "Power & POST",
      phase: "firmware",
      msStart: 0,
      msEnd: 200,
      chainStep: 0,
      accent: "#FFB020",
      icon: "clock",
      stepDetail: ["check CPU", "check RAM", "find boot device"],
      specs: [],
      verdict: "The hardware is awake.",
    }),
    seg("outro", { startFrame: 240, nextVideo: "How the Internet Actually Works", question: "What next?" }),
  ],
  manim: {},
  coco: {},
  images: {},
  logos: {},
  chapters: [],
};
