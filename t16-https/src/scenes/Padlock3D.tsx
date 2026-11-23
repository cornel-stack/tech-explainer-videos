import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A slowly rotating, glowing 3D PADLOCK — the icon of HTTPS. A rounded body, a metal
// U-shackle (half-torus) on top, and a dark keyhole on the face. Pure shapes, no
// logos. Renders on CI via the swangle software-GL backend. A ring of little
// "packet" cubes orbits it (the encrypted traffic it protects).
const MINT = "#35E08A";

const Orbiter: React.FC<{ i: number; n: number }> = ({ i, n }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const a = (i / n) * Math.PI * 2 + t * 0.6;
  const r = 3.4;
  const x = Math.cos(a) * r;
  const z = Math.sin(a) * r;
  const y = Math.sin(a * 2 + t) * 0.5;
  const lit = (Math.sin(a * 3 - t * 2) + 1) / 2;
  return (
    <mesh position={[x, y, z]} rotation={[t + i, t, 0]}>
      <boxGeometry args={[0.28, 0.28, 0.28]} />
      <meshStandardMaterial color={MINT} emissive={MINT} emissiveIntensity={0.4 + lit * 0.9} roughness={0.5} />
    </mesh>
  );
};

export const Padlock3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const spin = frame / 150;
  const bob = Math.sin(t * 1.2) * 0.12;
  const orbiters = Array.from({ length: 10 });

  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 1.2, 8], fov: 42 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.55} />
      <directionalLight position={[5, 8, 6]} intensity={1.1} />
      <pointLight position={[0, 2, 3]} intensity={3} color={MINT} distance={16} />
      <group rotation={[0.08, spin, 0]} position={[0, bob, 0]}>
        {/* body */}
        <mesh position={[0, -0.6, 0]}>
          <boxGeometry args={[2.6, 2.3, 1.2]} />
          <meshStandardMaterial color="#14181f" emissive={MINT} emissiveIntensity={0.18} roughness={0.35} metalness={0.7} />
        </mesh>
        {/* keyhole */}
        <mesh position={[0, -0.7, 0.62]}>
          <cylinderGeometry args={[0.26, 0.26, 0.2, 24]} />
          <meshStandardMaterial color="#05060a" roughness={0.6} />
        </mesh>
        <mesh position={[0, -1.05, 0.62]}>
          <boxGeometry args={[0.18, 0.5, 0.2]} />
          <meshStandardMaterial color="#05060a" roughness={0.6} />
        </mesh>
        {/* U-shackle (half torus) */}
        <mesh position={[0, 0.85, 0]} rotation={[0, 0, 0]}>
          <torusGeometry args={[0.9, 0.2, 20, 40, Math.PI]} />
          <meshStandardMaterial color="#C9CDD4" emissive={MINT} emissiveIntensity={0.15} roughness={0.25} metalness={0.9} />
        </mesh>
        {/* shackle legs */}
        <mesh position={[-0.9, 0.2, 0]}>
          <cylinderGeometry args={[0.2, 0.2, 1.3, 20]} />
          <meshStandardMaterial color="#C9CDD4" roughness={0.25} metalness={0.9} />
        </mesh>
        <mesh position={[0.9, 0.2, 0]}>
          <cylinderGeometry args={[0.2, 0.2, 1.3, 20]} />
          <meshStandardMaterial color="#C9CDD4" roughness={0.25} metalness={0.9} />
        </mesh>
      </group>
      {orbiters.map((_, i) => <Orbiter key={i} i={i} n={orbiters.length} />)}
    </ThreeCanvas>
  );
};
