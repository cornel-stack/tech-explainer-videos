import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A 3D GIT COMMIT GRAPH: a chain of glowing commit cubes linked by edges, with a
// branch that forks off, orbiting label-less pointer gems. Pure shapes, no logos.
// Renders on CI via the swangle software-GL backend.
const MINT = "#35E08A";
const AMBER = "#FFB020";
const VIOLET = "#B06BFF";

const Commit: React.FC<{ pos: [number, number, number]; color: string; i: number }> = ({ pos, color, i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const pulse = 0.5 + 0.5 * Math.sin(t * 2 + i * 0.9);
  return (
    <mesh position={pos} rotation={[t * 0.3 + i, t * 0.4, 0]}>
      <boxGeometry args={[0.62, 0.62, 0.62]} />
      <meshStandardMaterial color="#14181f" emissive={color} emissiveIntensity={0.35 + pulse * 0.9} roughness={0.35} metalness={0.5} />
    </mesh>
  );
};

// a thin edge (cylinder) between two points
const Edge: React.FC<{ a: [number, number, number]; b: [number, number, number]; color: string }> = ({ a, b, color }) => {
  const dx = b[0] - a[0], dy = b[1] - a[1], dz = b[2] - a[2];
  const len = Math.sqrt(dx * dx + dy * dy + dz * dz);
  const mid: [number, number, number] = [(a[0] + b[0]) / 2, (a[1] + b[1]) / 2, (a[2] + b[2]) / 2];
  // rotation to align the cylinder (default +Y) with the edge direction
  const ry = Math.atan2(dx, dz);
  const rx = -Math.atan2(dy, Math.sqrt(dx * dx + dz * dz)) + Math.PI / 2;
  return (
    <mesh position={mid} rotation={[rx, ry, 0]}>
      <cylinderGeometry args={[0.045, 0.045, len, 8]} />
      <meshStandardMaterial color={color} emissive={color} emissiveIntensity={0.7} roughness={0.5} />
    </mesh>
  );
};

export const CommitGraph3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  // main chain along X, plus a forked branch going up-right
  const main: [number, number, number][] = [
    [-3.2, 0, 0], [-1.6, 0, 0], [0, 0, 0], [1.6, 0, 0], [3.2, 0, 0],
  ];
  const branch: [number, number, number][] = [
    [1.6, 0, 0], [2.6, 1.5, -0.4], [4.0, 1.5, -0.4],
  ];
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 1.6, 8.6], fov: 42 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.55} />
      <directionalLight position={[5, 8, 6]} intensity={1.0} />
      <pointLight position={[0, 2, 3]} intensity={3} color={MINT} distance={20} />
      <group rotation={[0.08, Math.sin(frame / 240) * 0.5, 0]}>
        {/* main chain edges + nodes */}
        {main.slice(1).map((p, i) => <Edge key={`me${i}`} a={main[i]} b={p} color={MINT} />)}
        {main.map((p, i) => <Commit key={`mc${i}`} pos={p} color={MINT} i={i} />)}
        {/* forked branch */}
        {branch.slice(1).map((p, i) => <Edge key={`be${i}`} a={branch[i]} b={p} color={AMBER} />)}
        {branch.slice(1).map((p, i) => <Commit key={`bc${i}`} pos={p} color={AMBER} i={i + 10} />)}
        {/* branch-pointer gems orbiting the tips */}
        <mesh position={[3.2, 0.9, 0]} rotation={[frame / 60, frame / 50, 0]}>
          <octahedronGeometry args={[0.28]} />
          <meshStandardMaterial color={MINT} emissive={MINT} emissiveIntensity={1.2} roughness={0.3} />
        </mesh>
        <mesh position={[4.0, 2.4, -0.4]} rotation={[frame / 55, frame / 45, 0]}>
          <octahedronGeometry args={[0.28]} />
          <meshStandardMaterial color={VIOLET} emissive={VIOLET} emissiveIntensity={1.2} roughness={0.3} />
        </mesh>
      </group>
    </ThreeCanvas>
  );
};
