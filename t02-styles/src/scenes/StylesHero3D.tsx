import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Eight API styles orbiting a glowing core in 3D — "eight ways to talk."
// Renders on CI via the swangle software-GL backend (remotion.config.ts).
const COLORS = ["#FFC24B", "#B06BFF", "#FF3E7F", "#3DE0B0", "#FF6B4A", "#E8C24A", "#FFC24B", "#B06BFF"];

const Orb: React.FC<{ i: number }> = ({ i }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const a = (i / 8) * Math.PI * 2;
  const R = 3.3;
  const x = Math.cos(a) * R;
  const z = Math.sin(a) * R;
  const y = Math.sin(frame / fps + i) * 0.35;
  return (
    <mesh position={[x, y, z]}>
      <sphereGeometry args={[0.42, 24, 24]} />
      <meshStandardMaterial color={COLORS[i]} emissive={COLORS[i]} emissiveIntensity={0.6} roughness={0.35} />
    </mesh>
  );
};

export const StylesHero3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{ position: [0, 2.4, 8], fov: 48 }}
      gl={{ antialias: true }}
      style={{ background: "transparent" }}
    >
      <ambientLight intensity={0.7} />
      <directionalLight position={[4, 6, 5]} intensity={1.0} />
      <pointLight position={[0, 0, 0]} intensity={2.2} color="#FF3E7F" distance={6} />
      <group rotation={[0.25, frame / 90, 0]}>
        {/* glowing core */}
        <mesh>
          <icosahedronGeometry args={[1.05, 0]} />
          <meshStandardMaterial color="#FF3E7F" emissive="#FF3E7F" emissiveIntensity={0.9} roughness={0.3} wireframe />
        </mesh>
        {COLORS.map((_, i) => <Orb key={i} i={i} />)}
      </group>
    </ThreeCanvas>
  );
};
