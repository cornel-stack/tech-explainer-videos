import React from "react";
import { useCurrentFrame, interpolate } from "remotion";
import { theme, fontStack, glow } from "../theme";

const KEYWORDS = /\b(GET|POST|PUT|DELETE|HTTP\/1\.1|HTTP\/2|query|mutation|service|message|rpc|returns|const|new|Upgrade|Connection|Host)\b/g;

// Light-touch syntax tint: quoted strings mint, keywords accent, status 101/200 gold.
function tint(line: string, accent: string): React.ReactNode[] {
  const out: React.ReactNode[] = [];
  // split on quoted strings first
  const parts = line.split(/("[^"]*")/g);
  parts.forEach((part, i) => {
    if (part.startsWith('"') && part.endsWith('"')) {
      out.push(<span key={i} style={{ color: theme.accents.mint }}>{part}</span>);
      return;
    }
    // within non-string parts, tint keywords + status codes
    const sub = part.split(/(\b(?:GET|POST|PUT|DELETE|HTTP\/1\.1|HTTP\/2|query|mutation|service|message|rpc|returns|const|new|Upgrade|Connection|Host|101|200)\b)/g);
    sub.forEach((tok, j) => {
      if (/^(GET|POST|PUT|DELETE|query|mutation|service|message|rpc|returns|const|new|Upgrade|Connection|Host)$/.test(tok))
        out.push(<span key={`${i}-${j}k`} style={{ color: accent, fontWeight: 700 }}>{tok}</span>);
      else if (/^(101|200|HTTP\/1\.1|HTTP\/2)$/.test(tok))
        out.push(<span key={`${i}-${j}s`} style={{ color: theme.accents.gold }}>{tok}</span>);
      else out.push(<span key={`${i}-${j}`}>{tok}</span>);
    });
  });
  return out;
}

export const CodeCard: React.FC<{
  code: string[];
  accent: string;
  title?: string;
  width?: number;
}> = ({ code, accent, title, width = 900 }) => {
  const frame = useCurrentFrame();
  return (
    <div
      style={{
        width,
        background: "#121216",
        borderRadius: 18,
        overflow: "hidden",
        border: `1px solid ${accent}33`,
        boxShadow: glow(accent, 0.25),
        fontFamily: fontStack.mono,
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: 9, padding: "12px 18px", background: "#1A1A20" }}>
        <Dot c="#FF5F57" /><Dot c="#FEBC2E" /><Dot c="#28C840" />
        {title ? <span style={{ color: theme.inkFaint, fontSize: 17, marginLeft: 8 }}>{title}</span> : null}
      </div>
      <div style={{ padding: "18px 24px", fontSize: 25, lineHeight: 1.5 }}>
        {code.map((line, i) => {
          const op = interpolate(frame, [i * 5, i * 5 + 10], [0, 1], { extrapolateLeft: "clamp", extrapolateRight: "clamp" });
          return (
            <div key={i} style={{ opacity: op, color: theme.ink, whiteSpace: "pre", minHeight: line ? undefined : "0.9em" }}>
              {tint(line, accent)}
            </div>
          );
        })}
      </div>
    </div>
  );
};

const Dot: React.FC<{ c: string }> = ({ c }) => (
  <span style={{ width: 13, height: 13, borderRadius: 999, background: c, display: "inline-block" }} />
);
