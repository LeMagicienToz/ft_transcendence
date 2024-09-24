import React, { Suspense } from "react";
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";

const AstronautModel = () => {
  const { scene } = useGLTF("../public/astronaut/scene.gltf"); // Path to your GLTF model
  return <primitive object={scene} />;
};

const AstronautAvatar = () => {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
      <ambientLight intensity={0.5} />
      <directionalLight position={[10, 10, 10]} intensity={1} />
      <Suspense fallback={null}>
        <AstronautModel />
      </Suspense>
      <OrbitControls />
    </Canvas>
  );
};

export default AstronautAvatar;
  