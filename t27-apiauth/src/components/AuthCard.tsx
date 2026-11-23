import React from "react";
import { useCurrentFrame } from "remotion";
import { theme, fontStack, glow } from "../theme";

// The signature visual of T27: a drawn HTTP request card with the credential line
// highlighted, plus a "lock strength" security meter that fills to the method's level.
export const AuthCard: React.FC<{ auth: { header?: string; sec?: number; tag?: string }; name: string; accent: string; width?: number; height?: number }> = ({ auth, name, accent, width = 1030, height = 560 }) => {
  const frame = useCurrentFrame();
  const sec = Math.max(0, Math.min(1, auth.sec ?? 0));
  const headerLines = (auth.header ?? "").split("\n");
  // meter fills in
  const fill = sec * Math.min(1, Math.max(0, (frame - 10) / 30));
  const typed = Math.min(1, Math.max(0, (frame - 6) / 24));
  const lockColor = sec < 0.33 ? theme.accents.coral : sec < 0.7 ? theme.accents.amber : theme.accents.mint;
  const level = sec < 0.1 ? "OPEN" : sec < 0.33 ? "WEAK" : sec < 0.7 ? "MODERATE" : sec < 0.9 ? "STRONG" : "MAXIMUM";

  return (
    <div style={{ position: "relative", width, height, borderRadius: 16, overflow: "hidden", background: "#06080b", border: `1px solid ${accent}55`, boxShadow: glow(accent, 0.22), display: "flex", flexDirection: "column" }}>
      {/* title bar */}
      <div style={{ display: "flex", alignItems: "center", gap: 14, padding: "14px 20px", background: "#0f1217", borderBottom: `1px solid ${accent}33` }}>
        <span style={{ fontFamily: fontStack.mono, fontSize: 18, color: theme.inkSoft }}>→ HTTP request</span>
        <span style={{ marginLeft: "auto", fontFamily: fontStack.mono, fontSize: 15, letterSpacing: 2, color: accent, border: `1px solid ${accent}66`, borderRadius: 6, padding: "3px 10px" }}>{name}</span>
      </div>

      {/* the request with credential highlighted */}
      <div style={{ flex: 1, padding: "28px 30px", fontFamily: fontStack.mono, fontSize: 30, lineHeight: 1.5, opacity: typed }}>
        <div style={{ color: theme.inkFaint, fontSize: 24, marginBottom: 14 }}>POST /api/resource · HTTPS</div>
        <div style={{ display: "inline-block", background: `${accent}1c`, border: `2px solid ${accent}`, borderRadius: 10, padding: "14px 20px", boxShadow: glow(accent, 0.3) }}>
          {headerLines.map((l, i) => (
            <div key={i} style={{ color: i === 0 ? theme.ink : accent, whiteSpace: "pre-wrap", fontSize: l.length > 34 ? 24 : 30 }}>{l}</div>
          ))}
        </div>
        {auth.tag ? <div style={{ marginTop: 20, fontFamily: fontStack.sans, fontSize: 24, fontWeight: 700, color: theme.inkSoft }}>↳ {auth.tag}</div> : null}
      </div>

      {/* security strength meter */}
      <div style={{ background: "#0b0e13", borderTop: `1px solid ${accent}44`, padding: "16px 30px" }}>
        <div style={{ display: "flex", alignItems: "center", justifyContent: "space-between", marginBottom: 10 }}>
          <span style={{ fontFamily: fontStack.mono, fontSize: 17, color: theme.inkFaint, letterSpacing: 1 }}>LOCK STRENGTH</span>
          <span style={{ fontFamily: fontStack.sans, fontWeight: 900, fontSize: 22, color: lockColor }}>{level}</span>
        </div>
        <div style={{ height: 20, background: "#14171f", borderRadius: 999, overflow: "hidden", border: `1px solid ${lockColor}44` }}>
          <div style={{ height: "100%", width: `${fill * 100}%`, background: `linear-gradient(90deg, ${theme.accents.coral}, ${theme.accents.amber} 55%, ${theme.accents.mint})`, borderRadius: 999, boxShadow: glow(lockColor, 0.5) }} />
        </div>
      </div>
    </div>
  );
};
