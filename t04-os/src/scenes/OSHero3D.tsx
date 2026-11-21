import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Abstract 3D "constellation of operating systems": rounded tiles in the six
// family colours orbiting a core. No logos/characters — pure shapes. Renders on
// CI via the swangle software-GL backend.
const FAM = ["#2DD4BF", "#35FF9E", "#9B8CFF", "#FFB020", "#C9CDD4", "#FF6B4A"];
const N = 14;

const Tile: React.FC<{ i: number }> = ({ i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const a = (i / N) * Math.PI * 2 + t * 0.25;
  const R = 3.5;
  const y = Math.sin(t * 0.8 + i * 0.6) * 0.9;
  const c = FAM[i % FAM.length];
  return (
    <mesh position={[Math.cos(a) * R, y, Math.sin(a) * R]} rotation={[t * 0.3 + i, t * 0.4, 0]}>
      <boxGeometry args={[0.9, 0.9, 0.16]} />
      <meshStandardMaterial color={c} emissive={c} emissiveIntensity={0.55} roughness={0.35} metalness={0.2} />
    </mesh>
  );
};

export const OSHero3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 1.6, 9], fov: 46 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.7} />
      <directionalLight position={[4, 6, 5]} intensity={1} />
      <pointLight position={[0, 0, 0]} intensity={2.4} color="#35FF9E" distance={8} />
      <group rotation={[0.25, frame / 110, 0]}>
        <mesh>
          <icosahedronGeometry args={[1.25, 0]} />
          <meshStandardMaterial color="#35FF9E" emissive="#35FF9E" emissiveIntensity={0.85} roughness={0.3} wireframe />
        </mesh>
        {Array.from({ length: N }).map((_, i) => <Tile key={i} i={i} />)}
      </group>
    </ThreeCanvas>
  );
};
