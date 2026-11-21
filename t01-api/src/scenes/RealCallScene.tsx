import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig, interpolate } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Typewriter } from "../components/Typewriter";
import { pop, beatAt } from "../lib/anim";

// Stage 4 — the thing none of the reference videos show: a real call, typed
// and answered. Uses stage.request (a genuine public weather-API exchange).
export const RealCallScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);
  const req = stage.request ?? {};
  const res = req.response ?? {};

  const cardIn = pop(frame, 0, fps);
  const okIn = pop(frame, b("ok200", 150), fps);
  const headersIn = interpolate(frame, [b("ok200", 150) + 8, b("ok200", 150) + 24], [0, 1], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  const errCard = (at: number, code: string, text: string, color: string) => {
    const s = pop(frame, at, fps);
    if (s < 0.001) return null;
    return (
      <div
        style={{
          opacity: s,
          transform: `translateX(${(1 - s) * 50}px)`,
          background: theme.paper,
          borderRadius: 16,
          boxShadow: theme.shadowSoft,
          borderLeft: `8px solid ${color}`,
          padding: "16px 22px",
        }}
      >
        <div style={{ fontFamily: fontStack.mono, fontSize: 34, fontWeight: 700, color }}>{code}</div>
        <div style={{ fontFamily: fontStack.sans, fontSize: 20, color: theme.inkSoft }}>{text}</div>
      </div>
    );
  };

  return (
    <AbsoluteFill style={{ alignItems: "center", justifyContent: "center" }}>
      <div style={{ display: "flex", gap: 40, alignItems: "flex-start" }}>
        {/* terminal */}
        <div
          style={{
            width: 1180,
            transform: `scale(${cardIn})`,
            opacity: cardIn,
            background: "#0E1116",
            borderRadius: 20,
            boxShadow: theme.shadow,
            overflow: "hidden",
            fontFamily: fontStack.mono,
          }}
        >
          <div
            style={{
              display: "flex",
              alignItems: "center",
              gap: 10,
              padding: "14px 20px",
              background: "#171B22",
            }}
          >
            <Dot c="#FF5F57" /><Dot c="#FEBC2E" /><Dot c="#28C840" />
            <span style={{ color: "#8B93A1", fontSize: 18, marginLeft: 10 }}>
              api.weather.gov — live request
            </span>
          </div>
          <div style={{ padding: "26px 30px", fontSize: 27, lineHeight: 1.6 }}>
            {/* request */}
            <div>
              <span style={{ color: theme.ok }}>$ </span>
              <span style={{ color: theme.accents.amber, fontWeight: 700 }}>{req.method} </span>
              <Typewriter
                text={req.url ?? ""}
                at={b("typeRequest", 10)}
                cps={34}
                caretColor="#EDE7DB"
                style={{ color: "#EDE7DB" }}
              />
            </div>
            {/* response */}
            <div style={{ opacity: okIn, marginTop: 20 }}>
              <span style={{ color: theme.ok, fontWeight: 700, fontSize: 30 }}>{res.status}</span>
              <span style={{ color: "#5B6472" }}> ← it worked</span>
            </div>
            <div style={{ opacity: headersIn, color: "#6B7484", marginTop: 8, fontSize: 21 }}>
              {(res.headers ?? []).map((h: string, i: number) => (
                <div key={i}>{h}</div>
              ))}
            </div>
            <JsonBody
              text={res.body ?? ""}
              at={b("showBody", 200)}
              fps={fps}
              frame={frame}
            />
          </div>
        </div>

        {/* the two "the API talks back" error cards */}
        <div style={{ display: "flex", flexDirection: "column", gap: 20, width: 440, marginTop: 40 }}>
          {errCard(b("err404", 99999), "404", "Not Found — ask for something that isn't there", theme.err)}
          {errCard(b("err429", 99999), "429", "Too Many Requests — rate limiting: slow down", theme.warn)}
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Dot: React.FC<{ c: string }> = ({ c }) => (
  <span style={{ width: 14, height: 14, borderRadius: 999, background: c, display: "inline-block" }} />
);

// JSON body typed on, with a very light syntax tint for keys vs values.
const JsonBody: React.FC<{ text: string; at: number; fps: number; frame: number }> = ({
  text,
  at,
  frame,
}) => {
  const reveal = interpolate(frame, [at, at + 70], [0, text.length], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });
  const shown = text.slice(0, Math.floor(reveal));
  return (
    <pre
      style={{
        margin: "14px 0 0",
        color: "#A8E6CF",
        fontSize: 23,
        lineHeight: 1.5,
        whiteSpace: "pre-wrap",
      }}
    >
      {shown}
    </pre>
  );
};
