import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Abstract 3D "ignition": a glowing chip core with energy rings pulsing outward
// and a few orbiting fragments — power surging into silicon. Pure shapes, no
// logos/characters. Renders on CI via the swangle software-GL backend.
const Ring: React.FC<{ i: number }> = ({ i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const phase = (t * 0.6 + i / 3) % 1; // 0..1 expanding
  const r = 1.4 + phase * 3.2;
  const op = Math.max(0, 1 - phase) * 0.9;
  return (
    <mesh rotation={[Math.PI / 2, 0, 0]}>
      <torusGeometry args={[r, 0.035, 8, 64]} />
      <meshStandardMaterial color="#FFB020" emissive="#FFB020" emissiveIntensity={1.2} transparent opacity={op} />
    </mesh>
  );
};

const Frag: React.FC<{ i: number }> = ({ i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const a = (i / 6) * Math.PI * 2 + t * 0.5;
  const R = 2.6;
  const c = i % 2 === 0 ? "#35FF9E" : "#2DD4BF";
  return (
    <mesh position={[Math.cos(a) * R, Math.sin(t + i) * 0.6, Math.sin(a) * R]} rotation={[t + i, t, 0]}>
      <boxGeometry args={[0.28, 0.28, 0.28]} />
      <meshStandardMaterial color={c} emissive={c} emissiveIntensity={0.6} roughness={0.4} />
    </mesh>
  );
};

export const IgnitionHero3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const pulse = 1 + Math.sin(frame / 8) * 0.05;
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 2, 8], fov: 46 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[4, 6, 5]} intensity={0.9} />
      <pointLight position={[0, 0, 2]} intensity={3} color="#FFB020" distance={9} />
      <group rotation={[0.3, frame / 120, 0]}>
        {/* chip core */}
        <mesh scale={[pulse, pulse, pulse]}>
          <boxGeometry args={[1.6, 1.6, 0.4]} />
          <meshStandardMaterial color="#1a1206" emissive="#FFB020" emissiveIntensity={0.5} roughness={0.5} metalness={0.4} />
        </mesh>
        <mesh>
          <boxGeometry args={[0.7, 0.7, 0.5]} />
          <meshStandardMaterial color="#FFB020" emissive="#FFB020" emissiveIntensity={1} roughness={0.3} />
        </mesh>
        {[0, 1, 2].map((i) => <Ring key={i} i={i} />)}
        {Array.from({ length: 6 }).map((_, i) => <Frag key={i} i={i} />)}
      </group>
    </ThreeCanvas>
  );
};
