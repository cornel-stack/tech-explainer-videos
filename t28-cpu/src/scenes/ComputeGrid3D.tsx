import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Abstract 3D compute lattice: a grid of small cores that pulse in waves — the
// "thousands of workers in parallel" idea in 3D. Pure shapes, no logos. Renders
// on CI via the swangle software-GL backend.
const N = 9; // N x N grid

const Core: React.FC<{ ix: number; iz: number }> = ({ ix, iz }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const x = (ix - (N - 1) / 2) * 0.62;
  const z = (iz - (N - 1) / 2) * 0.62;
  const wave = Math.sin((ix + iz) * 0.6 - t * 2.2);
  const y = wave * 0.22;
  const lit = wave * 0.5 + 0.5;
  const c = lit > 0.6 ? "#39FF88" : "#1f8f5a";
  return (
    <mesh position={[x, y, z]}>
      <boxGeometry args={[0.42, 0.42, 0.42]} />
      <meshStandardMaterial color={c} emissive="#39FF88" emissiveIntensity={lit * 0.9} roughness={0.4} metalness={0.2} />
    </mesh>
  );
};

export const ComputeGrid3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const cores: React.ReactNode[] = [];
  for (let ix = 0; ix < N; ix++) for (let iz = 0; iz < N; iz++) cores.push(<Core key={`${ix}-${iz}`} ix={ix} iz={iz} />);
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 4.2, 6.2], fov: 46 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[4, 8, 4]} intensity={1} />
      <pointLight position={[0, 3, 0]} intensity={2.2} color="#39FF88" distance={12} />
      <group rotation={[0.1, frame / 150, 0]}>{cores}</group>
    </ThreeCanvas>
  );
};
