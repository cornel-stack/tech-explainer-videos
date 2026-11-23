import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A 3D NEURAL LATTICE: stacked layers of glowing nodes with signals pulsing upward —
// an abstract Transformer. Pure shapes, no logos. Renders on CI via swangle.
const VIOLET = "#B06BFF";
const TEAL = "#2DD4BF";
const AMBER = "#FFB020";

const LAYERS = 5;
const PER = 5;
const SPAN = 4.2;

const Node: React.FC<{ x: number; y: number; z: number; color: string; seed: number }> = ({ x, y, z, color, seed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  // a pulse that rises through the layers over time
  const wave = 0.5 + 0.5 * Math.sin(t * 1.6 - y * 0.9 + seed * 0.3);
  return (
    <mesh position={[x, y, z]}>
      <sphereGeometry args={[0.16, 16, 16]} />
      <meshStandardMaterial color="#14181f" emissive={color} emissiveIntensity={0.3 + wave * 1.1} roughness={0.35} metalness={0.4} />
    </mesh>
  );
};

const Edge: React.FC<{ a: [number, number, number]; b: [number, number, number]; color: string; seed: number }> = ({ a, b, color, seed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const flow = 0.15 + 0.85 * Math.max(0, Math.sin(t * 1.6 - a[1] * 0.9 + seed * 0.2));
  const dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
  const len = Math.sqrt(dx * dx + dy * dy + dz * dz);
  const mid: [number, number, number] = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2];
  const ry = Math.atan2(dx, dz);
  const rx = -Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)) + Math.PI / 2;
  return (
    <mesh position={mid} rotation={[rx, ry, 0]}>
      <cylinderGeometry args={[0.018, 0.018, len, 6]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={flow} transparent opacity={0.25 + flow * 0.5} roughness={0.6} />
    </mesh>
  );
};

export const Neural3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  // build node grid: layers along Y, nodes spread along X, slight Z scatter
  const nodes: { pos: [number, number, number]; color: string }[] = [];
  for (let l = 0; l < LAYERS; l++) {
    for (let i = 0; i < PER; i++) {
      const x = (i - (PER - 1) / 2) * (SPAN / PER) * 1.4;
      const y = (l - (LAYERS - 1) / 2) * 1.15;
      const z = Math.sin(i * 1.7 + l) * 0.5;
      const color = l === 0 ? TEAL : l === LAYERS - 1 ? AMBER : VIOLET;
      nodes.push({ pos: [x, y, z], color });
    }
  }
  const edges: { a: [number, number, number]; b: [number, number, number] }[] = [];
  for (let l = 0; l < LAYERS - 1; l++) {
    for (let i = 0; i < PER; i++) {
      const from = nodes[l * PER + i].pos;
      // connect to a couple of nodes in the next layer
      for (const j of [i, (i + 1) % PER]) {
        edges.push({ a: from, b: nodes[(l + 1) * PER + j].pos });
      }
    }
  }
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 0, 9.5], fov: 44 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 8, 6]} intensity={0.9} />
      <pointLight position={[0, 0, 4]} intensity={3} color={VIOLET} distance={22} />
      <group rotation={[0.1, Math.sin(frame / 240) * 0.55, 0]}>
        {edges.map((e, i) => <Edge key={`e${i}`} a={e.a} b={e.b} color={VIOLET} seed={i} />)}
        {nodes.map((n, i) => <Node key={`n${i}`} x={n.pos[0]} y={n.pos[1]} z={n.pos[2]} color={n.color} seed={i} />)}
      </group>
    </ThreeCanvas>
  );
};
