import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";
import * as THREE from "three";

// A stylised 3D request: a glowing packet shuttles between a client cube (left)
// and a server stack (right). Toon-ish, flat-lit — matches the drawn look, and
// renders on CI via the ANGLE/SwiftShader GL backend (see remotion.config.ts).
const Packet: React.FC = () => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = (Math.sin((frame / fps) * 1.4) + 1) / 2; // 0..1..0
  const x = -2.6 + t * 5.2;
  const y = Math.sin((frame / fps) * 4) * 0.25;
  return (
    <mesh position={[x, y, 0.4]}>
      <sphereGeometry args={[0.28, 24, 24]} />
      <meshStandardMaterial color="#3DE0B0" emissive="#3DE0B0" emissiveIntensity={0.9} />
    </mesh>
  );
};

const ClientCube: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <mesh position={[-2.9, 0, 0]} rotation={[0.3, frame / 120, 0]}>
      <boxGeometry args={[1.5, 1.5, 1.5]} />
      <meshStandardMaterial color="#FFC24B" emissive="#FFC24B" emissiveIntensity={0.25} roughness={0.4} metalness={0.2} />
    </mesh>
  );
};

const ServerStack: React.FC = () => {
  const frame = useCurrentFrame();
  return (
    <group position={[2.9, 0, 0]} rotation={[0.2, -frame / 150, 0]}>
      {[-0.95, 0, 0.95].map((y, i) => (
        <mesh key={i} position={[0, y, 0]}>
          <boxGeometry args={[1.8, 0.7, 1.3]} />
          <meshStandardMaterial color="#B06BFF" emissive="#B06BFF" emissiveIntensity={0.25} roughness={0.4} metalness={0.2} />
        </mesh>
      ))}
    </group>
  );
};

export const Hero3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  return (
    <ThreeCanvas
      width={width}
      height={height}
      camera={{ position: [0, 0.4, 7.4], fov: 48 }}
      gl={{ antialias: true }}
      style={{ background: "transparent" }}
    >
      <ambientLight intensity={0.85} />
      <directionalLight position={[4, 6, 5]} intensity={1.15} />
      <directionalLight position={[-4, -2, 2]} intensity={0.3} color="#EC4899" />
      <group rotation={[0, Math.sin(frame / 90) * 0.18, 0]}>
        <ClientCube />
        <ServerStack />
        <Packet />
      </group>
    </ThreeCanvas>
  );
};
