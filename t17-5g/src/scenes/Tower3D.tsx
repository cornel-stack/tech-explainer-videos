import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A 3D cell TOWER emitting expanding signal rings, with phones catching the beams.
// Pure shapes, no logos. Renders on CI via the swangle software-GL backend.
const MINT = "#35E08A";
const VIOLET = "#B06BFF";

// An expanding ring that rises and fades, on a staggered loop.
const Ring: React.FC<{ i: number; n: number }> = ({ i, n }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (frame / fps + (i / n) * 2.4) % 2.4;
  const p = t / 2.4;
  const r = 0.3 + p * 3.6;
  const y = 2.2 + p * 1.2;
  const op = Math.max(0, 1 - p) * 0.8;
  return (
    <mesh position={[0, y, 0]} rotation={[Math.PI / 2, 0, 0]}>
      <torusGeometry args={[r, 0.045, 10, 48]} />
      <meshStandardMaterial color={MINT} emissive={MINT} emissiveIntensity={op * 1.4} transparent opacity={op} roughness={0.5} />
    </mesh>
  );
};

const Phone: React.FC<{ a: number }> = ({ a }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const r = 3.6;
  const x = Math.cos(a + t * 0.25) * r;
  const z = Math.sin(a + t * 0.25) * r;
  const lit = (Math.sin(t * 2 + a * 3) + 1) / 2;
  return (
    <mesh position={[x, -1.4, z]} rotation={[0, -a - t * 0.25, 0]}>
      <boxGeometry args={[0.4, 0.8, 0.08]} />
      <meshStandardMaterial color="#14181f" emissive={VIOLET} emissiveIntensity={0.3 + lit * 0.8} roughness={0.4} metalness={0.5} />
    </mesh>
  );
};

export const Tower3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const rings = Array.from({ length: 5 });
  const phones = [0, 1.4, 2.9, 4.3, 5.6];
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 1.4, 8.4], fov: 42 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.55} />
      <directionalLight position={[5, 8, 6]} intensity={1.1} />
      <pointLight position={[0, 3, 2]} intensity={3} color={MINT} distance={18} />
      <group rotation={[0.05, frame / 220, 0]}>
        {/* mast */}
        <mesh position={[0, 0.2, 0]}>
          <cylinderGeometry args={[0.12, 0.2, 4.4, 12]} />
          <meshStandardMaterial color="#C9CDD4" roughness={0.4} metalness={0.8} />
        </mesh>
        {/* antenna panels near the top */}
        {[0, 2.09, 4.18].map((a, i) => (
          <mesh key={i} position={[Math.cos(a) * 0.5, 2.1, Math.sin(a) * 0.5]} rotation={[0, -a, 0.1]}>
            <boxGeometry args={[0.18, 0.9, 0.3]} />
            <meshStandardMaterial color="#14181f" emissive={MINT} emissiveIntensity={0.5} roughness={0.4} />
          </mesh>
        ))}
        {/* base */}
        <mesh position={[0, -2.1, 0]}>
          <boxGeometry args={[1.1, 0.3, 1.1]} />
          <meshStandardMaterial color="#1a1d24" roughness={0.6} />
        </mesh>
        {rings.map((_, i) => <Ring key={i} i={i} n={rings.length} />)}
        {phones.map((a, i) => <Phone key={i} a={a} />)}
      </group>
    </ThreeCanvas>
  );
};
