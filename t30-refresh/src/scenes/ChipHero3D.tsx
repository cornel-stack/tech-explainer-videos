import React from "react";
import { ThreeCanvas } from "@remotion/three";
import { useCurrentFrame, useVideoConfig } from "remotion";

// Abstract 3D "chip": a flat package with a raised grid of core-tiles that pulse
// in waves. Pure shapes, no brand marks/logos. Renders on CI via swangle.
const G = 6; // G x G cores

const CoreTile: React.FC<{ ix: number; iz: number }> = ({ ix, iz }) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const t = frame / fps;
  const x = (ix - (G - 1) / 2) * 0.46;
  const z = (iz - (G - 1) / 2) * 0.46;
  const wave = Math.sin((ix + iz) * 0.7 - t * 2.4);
  const h = 0.12 + (wave * 0.5 + 0.5) * 0.18;
  const lit = wave * 0.5 + 0.5;
  const c = lit > 0.55 ? "#FFB020" : "#8a6a28";
  return (
    <mesh position={[x, 0.18 + h / 2, z]}>
      <boxGeometry args={[0.34, h, 0.34]} />
      <meshStandardMaterial color={c} emissive="#FFB020" emissiveIntensity={lit * 0.8} roughness={0.4} metalness={0.3} />
    </mesh>
  );
};

export const ChipHero3D: React.FC<{ width: number; height: number }> = ({ width, height }) => {
  const frame = useCurrentFrame();
  const tiles: React.ReactNode[] = [];
  for (let ix = 0; ix < G; ix++) for (let iz = 0; iz < G; iz++) tiles.push(<CoreTile key={`${ix}-${iz}`} ix={ix} iz={iz} />);
  return (
    <ThreeCanvas width={width} height={height} camera={{ position: [0, 3.6, 5.6], fov: 46 }} gl={{ antialias: true }} style={{ background: "transparent" }}>
      <ambientLight intensity={0.6} />
      <directionalLight position={[4, 8, 4]} intensity={1} />
      <pointLight position={[0, 3, 0]} intensity={2} color="#FFB020" distance={12} />
      <group rotation={[0.2, frame / 140, 0]}>
        {/* package substrate */}
        <mesh position={[0, 0, 0]}>
          <boxGeometry args={[3.2, 0.3, 3.2]} />
          <meshStandardMaterial color="#1a1a1f" emissive="#FFB020" emissiveIntensity={0.08} roughness={0.5} metalness={0.5} />
        </mesh>
        {/* heat-spreader rim */}
        <mesh position={[0, 0.02, 0]}>
          <boxGeometry args={[2.9, 0.34, 2.9]} />
          <meshStandardMaterial color="#C9CDD4" emissive="#C9CDD4" emissiveIntensity={0.05} roughness={0.3} metalness={0.8} />
        </mesh>
        {tiles}
      </group>
    </ThreeCanvas>
  );
};
