import React from "react";
import { serverSvg, apiMarkSvg, endpointSvg } from "../lib/dicebear";

// The machine / code layer. Everything that isn't a person is drawn by DiceBear:
//   kind="server"   -> a bottts robot (a backend / kitchen)
//   kind="api"      -> an abstract shapes mark (a service's public face)
//   kind="endpoint" -> an identicon (one address)
export const Machine: React.FC<{
  seed: string;
  kind?: "server" | "api" | "endpoint";
  size?: number;
  bg?: string;
  label?: string;
  style?: React.CSSProperties;
}> = ({ seed, kind = "server", size = 200, bg, label, style }) => {
  const html =
    kind === "server"
      ? serverSvg(seed, bg ?? "#8B5CF6")
      : kind === "api"
        ? apiMarkSvg(seed, bg ?? "#F59E0B")
        : endpointSvg(seed);

  return (
    <div style={{ display: "flex", flexDirection: "column", alignItems: "center", gap: 10, ...style }}>
      <div
        style={{
          width: size,
          height: size,
          borderRadius: 28,
          overflow: "hidden",
          boxShadow: "0 16px 40px rgba(17,19,24,0.16)",
        }}
        dangerouslySetInnerHTML={{ __html: html }}
      />
      {label ? (
        <div style={{ fontWeight: 800, fontSize: 24, color: "#EDE7DB" }}>{label}</div>
      ) : null}
    </div>
  );
};
