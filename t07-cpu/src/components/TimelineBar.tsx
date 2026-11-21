import React from "react";
import { theme, fontStack } from "../theme";

// The signature chrome: a running 0–1000 ms telemetry bar + the firmware→user
// hand-off chain. During the boot stages a cursor sweeps the stage's ms window;
// once booted it flips to a "SYSTEM RUNNING" readout with the whole chain lit.
const CHAIN = ["FIRMWARE", "BOOTLOADER", "KERNEL", "PID 1", "USER SPACE"];

export const TimelineBar: React.FC<{
  phase?: string;
  msStart?: number;
  msEnd?: number;
  chainStep: number;
  accent: string;
  progress: number; // 0..1 within the stage
}> = ({ phase, msStart, msEnd, chainStep, accent, progress }) => {
  const booted = msStart == null || msEnd == null;
  const curMs = booted ? 1000 : Math.round(msStart + (msEnd - msStart) * Math.min(1, progress));

  return (
    <div style={{ width: "100%", display: "flex", flexDirection: "column", gap: 12 }}>
      {/* readout row */}
      <div style={{ display: "flex", alignItems: "baseline", gap: 18 }}>
        <span style={{ fontFamily: fontStack.mono, fontSize: 56, fontWeight: 700, color: accent, letterSpacing: 2, textShadow: `0 0 24px ${accent}88` }}>
          {booted ? "RUNNING" : `${String(curMs).padStart(4, "0")} ms`}
        </span>
        <span style={{ fontFamily: fontStack.mono, fontSize: 22, color: theme.inkSoft, letterSpacing: 3, textTransform: "uppercase" }}>
          {booted ? "· kernel at work, forever" : `· phase: ${phase}`}
        </span>
      </div>

      {/* 0–1000 ms track */}
      {!booted ? (
        <div style={{ position: "relative", height: 26 }}>
          <div style={{ position: "absolute", left: 0, right: 0, top: 10, height: 6, background: theme.line, borderRadius: 3 }} />
          {/* elapsed up to window start (dim) */}
          <div style={{ position: "absolute", left: 0, width: `${(msStart! / 1000) * 100}%`, top: 10, height: 6, background: theme.inkFaint, borderRadius: 3 }} />
          {/* this stage's window */}
          <div style={{ position: "absolute", left: `${(msStart! / 1000) * 100}%`, width: `${((msEnd! - msStart!) / 1000) * 100}%`, top: 8, height: 10, background: accent, borderRadius: 3, boxShadow: `0 0 16px ${accent}` }} />
          {/* cursor */}
          <div style={{ position: "absolute", left: `${(curMs / 1000) * 100}%`, top: 0, width: 3, height: 26, background: theme.ink, boxShadow: `0 0 10px ${theme.ink}` }} />
          {[0, 250, 500, 750, 1000].map((t) => (
            <span key={t} style={{ position: "absolute", left: `${(t / 1000) * 100}%`, top: 26, transform: "translateX(-50%)", fontFamily: fontStack.mono, fontSize: 13, color: theme.inkFaint }}>{t}</span>
          ))}
        </div>
      ) : (
        <div style={{ height: 26 }} />
      )}

      {/* hand-off chain */}
      <div style={{ display: "flex", alignItems: "center", gap: 8, marginTop: booted ? 0 : 14 }}>
        {CHAIN.map((c, i) => {
          const active = booted || i === chainStep;
          const done = !booted && i < chainStep;
          const col = active ? accent : done ? theme.inkSoft : theme.inkFaint;
          return (
            <React.Fragment key={c}>
              <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "6px 14px", borderRadius: 8, background: active ? `${accent}1a` : "transparent", border: `1px solid ${active ? accent : theme.line}` }}>
                <span style={{ width: 8, height: 8, borderRadius: 999, background: col, boxShadow: active ? `0 0 8px ${col}` : "none" }} />
                <span style={{ fontFamily: fontStack.mono, fontSize: 16, fontWeight: active ? 700 : 500, color: active ? theme.ink : col, letterSpacing: 1 }}>{c}</span>
              </div>
              {i < CHAIN.length - 1 ? <span style={{ color: theme.inkFaint, fontSize: 18 }}>→</span> : null}
            </React.Fragment>
          );
        })}
      </div>
    </div>
  );
};
