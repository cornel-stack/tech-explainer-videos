import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T23: a terminal window that TYPES each git command at a
// prompt, prints its realistic output, then surfaces a one-line "what just happened".
export const CmdCard: React.FC<{ cmd: { line?: string; out?: string; note?: string }; name: string; accent: string; width?: number; height?: number }> = ({ cmd, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const line = cmd.line ?? "git status";
  const out = cmd.out ?? "";
  const note = cmd.note ?? "";

  // 1) type the command, 2) print output, 3) reveal the note
  const typeStart = 12;
  const cps = 1.6;
  const shown = Math.max(0, Math.floor((frame - typeStart) * cps));
  const typed = line.slice(0, shown);
  const doneTyping = shown >= line.length;
  const outAt = typeStart + line.length / cps + 14;
  const showOut = frame > outAt;
  const noteAt = outAt + 26;
  const showNote = frame > noteAt;
  const caret = Math.floor(frame / 15) % 2 === 0;

  const outLines = out.split("\n");

  return (
    <div style={{ position: "relative", width, height, borderRadius: 16, overflow: "hidden", background: "#06080b", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22), display: "flex", flexDirection: "column" }}>
      {/* title bar */}
      <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "14px 20px", background: "#0f1217", borderBottom: `1px solid ${accent}33` }}>
        <span style={{ display: "flex", gap: 8 }}>
          {["#FF5C47", "#FFB020", "#35E08A"].map((c) => <span key={c} style={{ width: 14, height: 14, borderRadius: 999, background: c }} />)}
        </span>
        <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkSoft }}>bash — ~/project</span>
        <span style={{ marginLeft: "auto", fontFamily: fontStack.mono, fontSize: 15, letterSpacing: 2, color: accent, border: `1px solid ${accent}66`, borderRadius: 6, padding: "3px 10px" }}>{name}</span>
      </div>

      {/* terminal body */}
      <div style={{ flex: 1, padding: "26px 30px", fontFamily: fontStack.mono, fontSize: 30, lineHeight: 1.4 }}>
        {/* prompt + typed command */}
        <div style={{ whiteSpace: "pre-wrap", color: theme.ink }}>
          <span style={{ color: accent, fontWeight: 700 }}>~/project</span>
          <span style={{ color: theme.inkSoft }}> $ </span>
          <span>{typed}</span>
          {!doneTyping || (!showOut && caret) ? <span style={{ color: accent }}>▋</span> : null}
        </div>

        {/* output */}
        {showOut ? (
          <div style={{ marginTop: 14, opacity: Math.min(1, (frame - outAt) / 10) }}>
            {outLines.map((l, i) => (
              <div key={i} style={{ whiteSpace: "pre-wrap", color: l.trim().startsWith("(") ? theme.inkFaint : theme.inkSoft, fontSize: 26 }}>{l}</div>
            ))}
          </div>
        ) : null}
      </div>

      {/* what-just-happened banner */}
      <div style={{ background: "#0b0e13", borderTop: `1px solid ${accent}44`, padding: "14px 30px", minHeight: 66, display: "flex", alignItems: "center", gap: 14, opacity: showNote ? Math.min(1, (frame - noteAt) / 10) : 0 }}>
        <span style={{ fontFamily: fontStack.mono, fontSize: 17, color: accent, border: `1px solid ${accent}`, borderRadius: 6, padding: "3px 10px", letterSpacing: 1 }}>WHAT IT DOES</span>
        <span style={{ fontFamily: fontStack.sans, fontSize: 24, fontWeight: 700, color: theme.ink }}>{note}</span>
      </div>
    </div>
  );
};
