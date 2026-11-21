import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Peep, CAST } from "../characters/Peep";
import { Machine } from "../characters/Machine";
import { Icon } from "../components/Icon";
import { Wire, Pulse } from "../components/Flow";
import { ManimFull, useHasClip } from "../components/ManimClip";
import { pop, beatAt } from "../lib/anim";

// Stage 1 — the messenger. Your app (Open Peeps) talks to another system
// (DiceBear bottts) only through the API pill in the middle.
export const WhatScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const hasClip = useHasClip("messenger");
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);

  if (hasClip) return <ManimFull name="messenger" />;

  const youIn = pop(frame, 0, fps);
  const sysIn = pop(frame, 10, fps);
  const apiIn = pop(frame, b("messenger", 40), fps);
  const doors = pop(frame, b("doors", 9999), fps);
  const hidden = pop(frame, b("hidden", 9999), fps);

  return (
    <AbsoluteFill>
      {/* wires + travelling packets */}
      <svg viewBox="0 0 1920 720" style={{ position: "absolute", inset: 0 }}>
        <Wire from={{ x: 470, y: 360 }} to={{ x: 830, y: 360 }} at={14} width={5} />
        <Wire from={{ x: 1090, y: 360 }} to={{ x: 1450, y: 360 }} at={18} width={5} />
        <Pulse
          from={{ x: 470, y: 360 }}
          to={{ x: 1450, y: 360 }}
          at={b("sendRequest", 70)}
          dur={34}
          color={theme.client}
          label="request"
        />
        <Pulse
          from={{ x: 1450, y: 360 }}
          to={{ x: 470, y: 360 }}
          at={b("getResponse", 120)}
          dur={34}
          color={theme.ok}
          label="response"
        />
      </svg>

      {/* You / your app */}
      <div style={{ position: "absolute", left: 180, top: 210, opacity: youIn, transform: `scale(${youIn})` }}>
        <Peep seed={CAST.you} size={300} bob={Math.sin(frame / 22) * 5} />
        <Label text="Your app" sub="the client" color={theme.client} />
      </div>

      {/* API messenger pill */}
      <div
        style={{
          position: "absolute",
          left: 960,
          top: 300,
          transform: `translate(-50%,0) scale(${apiIn})`,
          opacity: apiIn,
        }}
      >
        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 14,
            background: theme.api,
            color: "#fff",
            padding: "18px 30px",
            borderRadius: 999,
            boxShadow: theme.shadow,
            fontFamily: fontStack.sans,
            fontWeight: 900,
            fontSize: 40,
          }}
        >
          <Icon name="messenger" size={44} color="#fff" />
          API
        </div>
        {/* "only the doors it opens" */}
        <div style={{ opacity: doors, marginTop: 14, display: "flex", justifyContent: "center", gap: 10 }}>
          <Icon name="doors" size={46} color={theme.api} />
          <span style={{ fontFamily: fontStack.mono, fontSize: 20, color: theme.inkSoft, alignSelf: "center" }}>
            only the doors it opens
          </span>
        </div>
      </div>

      {/* The other system */}
      <div style={{ position: "absolute", left: 1470, top: 250, opacity: sysIn, transform: `scale(${sysIn})` }}>
        <Machine seed="another-system-weather" kind="server" size={230} bg="#8B5CF6" />
        <Label text="Another system" sub="database · servers" color={theme.server} center />
        {/* private data, hidden from you */}
        <div
          style={{
            position: "absolute",
            top: -70,
            left: "50%",
            transform: `translateX(-50%) scale(${hidden})`,
            opacity: hidden,
            display: "flex",
            alignItems: "center",
            gap: 8,
            background: theme.paper,
            border: `2px dashed ${theme.err}`,
            color: theme.err,
            padding: "8px 16px",
            borderRadius: 12,
            fontFamily: fontStack.mono,
            fontSize: 20,
            fontWeight: 600,
            whiteSpace: "nowrap",
          }}
        >
          <Icon name="cross" size={22} color={theme.err} /> private data hidden
        </div>
      </div>
    </AbsoluteFill>
  );
};

const Label: React.FC<{ text: string; sub?: string; color: string; center?: boolean }> = ({
  text,
  sub,
  color,
  center,
}) => (
  <div style={{ textAlign: center ? "center" : "center", marginTop: 8 }}>
    <div style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 30, color: theme.ink }}>
      {text}
    </div>
    {sub ? (
      <div style={{ fontFamily: fontStack.mono, fontSize: 18, color }}>{sub}</div>
    ) : null}
  </div>
);
