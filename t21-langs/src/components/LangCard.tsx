import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T21: a code editor window that TYPES each language's real
// "Hello World" in its own syntax, then "runs" it and prints the output. A tiny
// keyword/string/comment highlighter keeps it readable without pulling in a lib.
const KEYWORDS = new Set([
  "include", "int", "main", "void", "return", "class", "public", "static", "new",
  "using", "func", "package", "import", "fn", "const", "let", "var", "echo", "puts",
  "print", "println", "def", "std", "cout", "endl", "System", "Console", "void",
  "string", "String", "printf", "fmt", "require",
]);

const tokColor = (tok: string, accent: string): string => {
  if (/^".*"?$|^'.*'?$/.test(tok) || tok.startsWith('"')) return theme.accents.mint; // strings
  if (/^(\/\/|#|<\?php|\?>)/.test(tok)) return theme.inkFaint; // comments / php tags
  if (/^[0-9]+$/.test(tok)) return theme.accents.amber;
  if (KEYWORDS.has(tok.replace(/[^A-Za-z]/g, ""))) return accent;
  if (/^[A-Za-z_][A-Za-z0-9_]*\(/.test(tok)) return theme.accents.violet; // call
  return theme.ink;
};

const Line: React.FC<{ text: string; accent: string }> = ({ text, accent }) => {
  // split but keep quoted strings whole
  const parts = text.match(/("[^"]*"|'[^']*'|\s+|[^\s]+)/g) ?? [text];
  return (
    <div style={{ whiteSpace: "pre", minHeight: 34 }}>
      {parts.map((p, i) =>
        /^\s+$/.test(p) ? (
          <span key={i}>{p}</span>
        ) : (
          <span key={i} style={{ color: tokColor(p, accent) }}>{p}</span>
        )
      )}
    </div>
  );
};

export const LangCard: React.FC<{ lang: { code?: string; ext?: string; run?: string }; name: string; accent: string; width?: number; height?: number }> = ({ lang, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const code = lang.code ?? 'print("Hello, World!")';
  const ext = lang.ext ?? "hello";
  const run = lang.run ?? "Hello, World!";

  // typewriter: reveal `code` char-by-char, then show the run output
  const typeStart = 14;
  const cps = 2.1; // chars per frame
  const shown = Math.max(0, Math.floor((frame - typeStart) * cps));
  const typed = code.slice(0, shown);
  const doneTyping = shown >= code.length;
  const runAt = typeStart + code.length / cps + 18;
  const running = frame > runAt;
  const caret = Math.floor(frame / 15) % 2 === 0;

  const lines = (typed + (doneTyping || running ? "" : caret ? "▋" : " ")).split("\n");

  return (
    <div style={{ position: "relative", width, height, borderRadius: 16, overflow: "hidden", background: "#0c0e13", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22), display: "flex", flexDirection: "column" }}>
      {/* title bar */}
      <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "14px 20px", background: "#121419", borderBottom: `1px solid ${accent}33` }}>
        <span style={{ display: "flex", gap: 8 }}>
          {["#FF5C47", "#FFB020", "#35E08A"].map((c) => <span key={c} style={{ width: 14, height: 14, borderRadius: 999, background: c }} />)}
        </span>
        <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkSoft }}>{ext}</span>
        <span style={{ marginLeft: "auto", fontFamily: fontStack.mono, fontSize: 15, letterSpacing: 2, color: accent, border: `1px solid ${accent}66`, borderRadius: 6, padding: "3px 10px" }}>{name}</span>
      </div>

      {/* code area */}
      <div style={{ flex: 1, display: "flex", padding: "22px 0", fontFamily: fontStack.mono, fontSize: 28, lineHeight: 1.32 }}>
        <div style={{ color: theme.inkFaint, textAlign: "right", padding: "0 18px", userSelect: "none", borderRight: `1px solid ${theme.line}` }}>
          {lines.map((_, i) => <div key={i} style={{ minHeight: 34 }}>{i + 1}</div>)}
        </div>
        <div style={{ padding: "0 24px", flex: 1 }}>
          {lines.map((ln, i) => <Line key={i} text={ln} accent={accent} />)}
        </div>
      </div>

      {/* run / output console */}
      <div style={{ background: "#07080b", borderTop: `1px solid ${accent}44`, padding: "12px 24px", minHeight: 74, fontFamily: fontStack.mono, fontSize: 24 }}>
        <div style={{ display: "flex", alignItems: "center", gap: 12, color: theme.inkFaint, fontSize: 16 }}>
          <span style={{ color: running ? theme.accents.mint : theme.inkFaint }}>▸ run</span>
          <span>{ext.includes(".") ? `$ ./${ext.split(".")[0]}` : "$ run"}</span>
        </div>
        {running ? (
          <div style={{ marginTop: 6, color: theme.accents.mint, opacity: Math.min(1, (frame - runAt) / 10) }}>
            {run}
            <span style={{ opacity: caret ? 1 : 0, color: theme.inkSoft }}> ▋</span>
          </div>
        ) : (
          <div style={{ marginTop: 6, color: theme.inkFaint }}>…</div>
        )}
      </div>
    </div>
  );
};
