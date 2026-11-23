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

// A CPU die tile configuration (original schematic — not a brand die shot).
export const zDie = z.object({
  p: z.number().optional(),
  e: z.number().optional(),
  npu: z.boolean().optional(),
  xe: z.number().optional(),
  gray: z.number().optional(),
});

// One timeline segment. `kind` picks the scene; item-only fields are optional.
export const zSegment = z.object({
  kind: z.enum(["intro", "interlude", "item", "outro"]),
  narration: z.string(),
  audioFile: z.string(),
  startFrame: z.number(),
  durationInFrames: z.number(),
  words: z.array(zWord),
  beats: z.array(zBeat),
  // a Manim clip name (intro + interludes + item overrides like binning)
  manim: z.string().optional(),
  // item-only
  id: z.string().optional(),
  name: z.string().optional(),
  launched: z.string().optional(),
  tier: z.string().optional(),
  cat: z.string().optional(),
  status: z.string().optional(),
  mech: z.array(z.string()).optional(),
  px: z.array(z.number()).optional(),
  stick: z.object({
    form: z.string().optional(),
    pins: z.number().optional(),
    notch: z.number().optional(),
    chips: z.number().optional(),
    ecc: z.boolean().optional(),
    pmic: z.boolean().optional(),
    curved: z.boolean().optional(),
  }).optional(),
  die: zDie.optional(),
  features: z.array(z.string()).optional(),
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
  id: "t07-cpu",
  title: "Every Intel CPU Explained",
  series: "Every X",
  keyNoun: "Intel CPU",
  promise: "demo",
  accent: "#FFB020",
  fps: 60,
  width: 1920,
  height: 1080,
  totalFrames: 360,
  sources: [],
  segments: [
    seg("intro", { startFrame: 0 }),
    seg("item", {
      startFrame: 120,
      id: "i5",
      name: "Core 5 / i5",
      launched: "2009",
      tier: "i5",
      die: { p: 6, e: 8 },
      accent: "#35E08A",
      icon: "server",
      specs: [],
      verdict: "Buy it if: you want the best all-round value.",
    }),
    seg("outro", { startFrame: 240, nextVideo: "Every AMD CPU Explained", question: "Which Intel chip do you run?" }),
  ],
  manim: {},
  coco: {},
  images: {},
  logos: {},
  chapters: [],
};
