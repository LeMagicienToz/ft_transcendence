import React, { Suspense } from "react";
import * as THREE from 'three';
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";

const AstronautModel = () => {
  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera( 75, window.innerWidth / window.innerHeight, 0.1, 1000 );

  const renderer = new THREE.WebGLRenderer();
  renderer.setSize( window.innerWidth, window.innerHeight );
  document.body.appendChild( renderer.domElement );
  // const { scene } = useGLTF("../public/astronaut/scene.gltf"); // Path to your GLTF model
  // return <primitive object={scene} />;
};

const AstronautAvatar = () => {
  return (
    <Canvas camera={{ position: [0, 2, 5], fov: 50 }}>
      <ambientLight intensity={1} />
      <directionalLight position={[10, 10, 10]} intensity={3} />
      <Suspense fallback={null}>
        {/* <AstronautModel /> */}
      </Suspense>
      <OrbitControls />
    </Canvas>
  );
};

export default AstronautAvatar;
  