import React from "react";
import { theme, fontStack } from "../theme";

// Thin rail along the bottom showing all six steps and where we are.
export const ProgressRail: React.FC<{
  steps: { icon: string; accent: string }[];
  current: number; // 0-based
  progress: number; // 0..1 within the current step
  accent: string;
}> = ({ steps, current, progress, accent }) => {
  return (
    <div
      style={{
        position: "absolute",
        left: 72,
        right: 72,
        bottom: 54,
        display: "flex",
        alignItems: "center",
        gap: 12,
      }}
    >
      {steps.map((s, i) => {
        const done = i < current;
        const active = i === current;
        const fill = done ? 1 : active ? progress : 0;
        return (
          <React.Fragment key={i}>
            <div
              style={{
                fontFamily: fontStack.mono,
                fontSize: 18,
                fontWeight: 700,
                color: done || active ? accent : theme.inkFaint,
                width: 22,
                textAlign: "center",
              }}
            >
              {i + 1}
            </div>
            <div
              style={{
                flex: 1,
                height: 6,
                borderRadius: 3,
                background: theme.line,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${fill * 100}%`,
                  height: "100%",
                  background: active ? accent : done ? theme.inkSoft : "transparent",
                  borderRadius: 3,
                }}
              />
            </div>
          </React.Fragment>
        );
      })}
    </div>
  );
};
