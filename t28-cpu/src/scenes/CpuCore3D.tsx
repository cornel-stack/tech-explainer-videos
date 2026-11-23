import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A 3D CPU die: a square silicon chip with a grid of glowing core cells that pulse
// in waves (the clock), a raised heat-spreader frame, and bright pins. Pure shapes,
// no logos. Renders on CI via swangle.
const GREEN = "#35E08A";
const TEAL = "#2DD4BF";
const GOLD = "#E8C24A";

const GRID = 6;

const Cell: React.FC<{ x: number; z: number; i: number; j: number }> = ({ x, z, i, j }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  // a clock wave sweeping diagonally across the die
  const wave = 0.5 + 0.5 * Math.sin(t * 3 - (i + j) * 0.6);
  const h = 0.12 + wave * 0.5;
  const color = (i + j) % 5 === 0 ? TEAL : GREEN;
  return (
    <mesh position={[x, h / 2, z]}>
      <boxGeometry args={[0.52, h, 0.52]} />
      <meshStandardMaterial color="#10161c" emissive={color} emissiveIntensity={0.25 + wave * 1.1} roughness={0.4} metalness={0.5} />
    </mesh>
  );
};

export const CpuCore3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const cells: { x: number; z: number; i: number; j: number }[] = [];
  const step = 0.62;
  for (let i = 0; i < GRID; i++) for (let j = 0; j < GRID; j++) {
    cells.push({ x: (i - (GRID - 1) / 2) * step, z: (j - (GRID - 1) / 2) * step, i, j });
  }
  const half = (GRID * step) / 2 + 0.25;
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [3.2, 4.2, 4.6], fov: 42 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 9, 4]} intensity={1.0} />
      <pointLight position={[0, 4, 2]} intensity={3} color={GREEN} distance={22} />
      <group rotation={[0, frame / 240, 0]}>
        {/* substrate */}
        <mesh position={[0, -0.18, 0]}>
          <boxGeometry args={[half * 2 + 0.5, 0.22, half * 2 + 0.5]} />
          <meshStandardMaterial color="#0c0f13" roughness={0.7} metalness={0.3} />
        </mesh>
        {/* metal frame (heat spreader lip) */}
        {[[-half, 0], [half, 0], [0, -half], [0, half]].map(([fx, fz], k) => (
          <mesh key={k} position={[fx, 0.05, fz]}>
            <boxGeometry args={fz === 0 ? [0.12, 0.3, half * 2] : [half * 2, 0.3, 0.12]} />
            <meshStandardMaterial color="#C9CDD4" roughness={0.35} metalness={0.85} />
          </mesh>
        ))}
        {/* the core grid */}
        {cells.map((c, k) => <Cell key={k} {...c} />)}
        {/* gold pins underneath the edge */}
        {Array.from({ length: GRID }).map((_, i) => (
          <mesh key={`p${i}`} position={[(i - (GRID - 1) / 2) * step, -0.4, half + 0.1]}>
            <boxGeometry args={[0.16, 0.16, 0.3]} />
            <meshStandardMaterial color={GOLD} emissive={GOLD} emissiveIntensity={0.5} roughness={0.3} metalness={0.9} />
          </mesh>
        ))}
      </group>
    </ThreeCanvas>
  );
};
