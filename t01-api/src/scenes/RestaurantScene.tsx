import React from "react";
import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";
import type { Stage } from "../schema";
import { theme, fontStack } from "../theme";
import { Peep, CAST } from "../characters/Peep";
import { Machine } from "../characters/Machine";
import { Icon } from "../components/Icon";
import { Wire, Pulse } from "../components/Flow";
import { Coco } from "../components/Coco";
import { pop, beatAt } from "../lib/anim";

// Stage 2 — the restaurant. You (diner) ↔ waiter (the API) ↔ kitchen (the
// server). On the right, the mapping table fills in as each word is spoken.
export const RestaurantScene: React.FC<{ stage: Stage }> = ({ stage }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const b = (m: string, f = 0) => beatAt(stage.beats, m, f);

  const youIn = pop(frame, b("youSit", 4), fps);
  const kitchenIn = pop(frame, b("kitchen", 30), fps);
  const waiterIn = pop(frame, b("waiter", 60), fps);

  const rows = [
    { k: "You", v: "the application", mark: "youSit", color: theme.client },
    { k: "Waiter", v: "the API", mark: "waiter", color: theme.api },
    { k: "Kitchen", v: "the server", mark: "kitchen", color: theme.server },
    { k: "Menu", v: "the documentation", mark: "menu", color: theme.ink },
    { k: "Order", v: "the request", mark: "order", color: theme.client },
    { k: "Plate", v: "the response", mark: "plate", color: theme.ok },
  ];

  return (
    <AbsoluteFill style={{ flexDirection: "row", alignItems: "center" }}>
      {/* left: the staged scene */}
      <div style={{ position: "relative", width: 1080, height: 720 }}>
        {/* soft Coco Material "dining" illustration as set dressing */}
        <div style={{ position: "absolute", right: 20, bottom: 0, opacity: 0.16 }}>
          <Coco name="restaurant" width={520} />
        </div>
        <svg viewBox="0 0 1080 720" style={{ position: "absolute", inset: 0 }}>
          <Wire from={{ x: 250, y: 420 }} to={{ x: 520, y: 420 }} at={b("waiter", 60)} width={5} dash />
          <Wire from={{ x: 620, y: 420 }} to={{ x: 880, y: 420 }} at={b("waiter", 60)} width={5} dash />
          <Pulse from={{ x: 250, y: 420 }} to={{ x: 880, y: 420 }} at={b("order", 150)} dur={34} color={theme.client} label="order" />
          <Pulse from={{ x: 880, y: 420 }} to={{ x: 250, y: 420 }} at={b("plate", 230)} dur={34} color={theme.ok} label="plate" />
        </svg>

        {/* you (diner) */}
        <div style={{ position: "absolute", left: 80, top: 260, opacity: youIn, transform: `scale(${youIn})` }}>
          <Peep seed={CAST.you} size={260} bob={Math.sin(frame / 20) * 5} />
          <Cap text="You" color={theme.client} />
        </div>

        {/* waiter = API */}
        <div style={{ position: "absolute", left: 430, top: 230, opacity: waiterIn, transform: `scale(${waiterIn})` }}>
          <Peep seed={CAST.waiter} size={250} bob={Math.sin(frame / 16) * 6} />
          <div style={{ display: "flex", justifyContent: "center", marginTop: -6 }}>
            <span
              style={{
                background: theme.api,
                color: theme.onAccent,
                fontFamily: fontStack.sans,
                fontWeight: 900,
                fontSize: 24,
                padding: "6px 18px",
                borderRadius: 999,
              }}
            >
              API
            </span>
          </div>
        </div>

        {/* kitchen = server */}
        <div style={{ position: "absolute", left: 790, top: 280, opacity: kitchenIn, transform: `scale(${kitchenIn})` }}>
          <Machine seed="kitchen-server-01" kind="server" size={210} bg="#8B5CF6" />
          <Cap text="Kitchen" color={theme.server} />
        </div>
      </div>

      {/* right: the mapping table */}
      <div style={{ width: 760, display: "flex", flexDirection: "column", gap: 16, paddingRight: 30 }}>
        {rows.map((r) => {
          const s = pop(frame, b(r.mark, 99999), fps);
          if (s < 0.001) return null;
          return (
            <div
              key={r.k}
              style={{
                opacity: s,
                transform: `translateX(${(1 - s) * 50}px)`,
                display: "flex",
                alignItems: "center",
                gap: 16,
                background: theme.paper,
                borderRadius: 16,
                boxShadow: theme.shadowSoft,
                padding: "16px 22px",
              }}
            >
              <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 30, color: r.color, width: 150 }}>
                {r.k}
              </span>
              <Icon name="arrow" size={28} color={theme.inkFaint} />
              <span style={{ fontFamily: fontStack.sans, fontWeight: 700, fontSize: 30, color: theme.ink }}>
                {r.v}
              </span>
            </div>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};

const Cap: React.FC<{ text: string; color: string }> = ({ text, color }) => (
  <div style={{ textAlign: "center", marginTop: 6 }}>
    <span style={{ fontFamily: fontStack.sans, fontWeight: 800, fontSize: 28, color }}>{text}</span>
  </div>
);
