import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// A 3D assistant ORB: a glowing core (the model) orbited by chat-bubble cubes
// (user teal / assistant green) with an amber reward star circling. Pure shapes,
// no logos. Renders on CI via swangle.
const VIOLET = "#B06BFF";
const TEAL = "#2DD4BF";
const GREEN = "#35E08A";
const AMBER = "#FFB020";

const Bubble: React.FC<{ a: number; r: number; y: number; color: string; speed: number }> = ({ a, r, y, color, speed }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const ang = a + t * speed;
  const x = Math.cos(ang) * r;
  const z = Math.sin(ang) * r;
  const lit = 0.4 + 0.5 * (0.5 + 0.5 * Math.sin(t * 2 + a * 3));
  return (
    <mesh position={[x, y + Math.sin(t + a) * 0.3, z]} rotation={[0, -ang, 0]}>
      <boxGeometry args={[0.7, 0.5, 0.14]} />
      <meshStandardMaterial color="#14181f" emissive={color} emissiveIntensity={0.3 + lit} roughness={0.4} metalness={0.4} />
    </mesh>
  );
};

export const ChatOrb3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const core = 0.6 + 0.4 * (0.5 + 0.5 * Math.sin(t * 1.8));
  const bubbles = [
    { a: 0, r: 3.4, y: 0.6, color: TEAL, speed: 0.4 },
    { a: 1.6, r: 3.4, y: -0.4, color: GREEN, speed: 0.4 },
    { a: 3.1, r: 3.4, y: 0.9, color: TEAL, speed: 0.4 },
    { a: 4.7, r: 3.4, y: -0.7, color: GREEN, speed: 0.4 },
    { a: 2.3, r: 4.2, y: 1.4, color: TEAL, speed: -0.3 },
    { a: 5.4, r: 4.2, y: -1.3, color: GREEN, speed: -0.3 },
  ];
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 1.2, 9] }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[5, 8, 6]} intensity={0.9} />
      <pointLight position={[0, 0, 3]} intensity={3.4} color={VIOLET} distance={24} />
      <group rotation={[0.08, Math.sin(frame / 240) * 0.5, 0]}>
        {/* the model core */}
        <mesh position={[0, 0, 0]} rotation={[t * 0.2, t * 0.3, 0]}>
          <icosahedronGeometry args={[1.5, 1]} />
          <meshStandardMaterial color="#1a1030" emissive={VIOLET} emissiveIntensity={0.5 + core} roughness={0.3} metalness={0.5} flatShading />
        </mesh>
        {/* orbiting chat bubbles */}
        {bubbles.map((b, i) => <Bubble key={i} {...b} />)}
        {/* amber reward star on a tilted orbit */}
        <mesh position={[Math.cos(t * 0.8) * 5, Math.sin(t * 0.8) * 2.2, Math.sin(t * 0.8) * 5]} rotation={[t, t * 1.3, 0]}>
          <octahedronGeometry args={[0.4]} />
          <meshStandardMaterial color={AMBER} emissive={AMBER} emissiveIntensity={1.3} roughness={0.3} />
        </mesh>
      </group>
    </ThreeCanvas>
  );
};
