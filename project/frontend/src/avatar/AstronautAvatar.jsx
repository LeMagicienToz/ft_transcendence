import React, { Suspense } from "react";
import * as THREE from 'three';
import { Canvas } from "@react-three/fiber";
import { OrbitControls, useGLTF } from "@react-three/drei";
import { GLTFLoader } from 'three/addons/loaders/GLTFLoader.js';

const AstronautModel = () => {

// Import necessary Three.js components
const loader = new GLTFLoader();

// Set up the renderer
const renderer = new THREE.WebGLRenderer();
renderer.setSize(window.innerWidth, window.innerHeight);
document.body.appendChild(renderer.domElement);

// Add a camera
const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
camera.position.set(0, 1, 5); // Adjust camera position

// Add a scene
const scene = new THREE.Scene();

// Add lighting
const ambientLight = new THREE.AmbientLight(0xffffff, 0.6); // Soft white light for global illumination
scene.add(ambientLight);

const directionalLight = new THREE.DirectionalLight(0xffffff, 0.8); // Brighter directional light
directionalLight.position.set(5, 5, 5).normalize();
scene.add(directionalLight);


const material_chibi = new THREE.MeshBasicMaterial({ color: 0x3333ff });
// Load the chibi model with textures
loader.load('../../public/astronaut/scene.gltf', function (gltf) {

    // Traverse the model to make sure all materials are opaque
    gltf.scene.traverse(function (child) {
        if (child.isMesh) {
            // Set material transparency to false and opacity to 1
            if (child.material) {
              child.material = material_chibi;
                child.material.transparent = false; // Disable transparency
                child.material.opacity = 1;        // Set full opacity
                child.material.needsUpdate = true; // Apply changes
            }
        }
    });

    // Add the loaded scene (including its textures)
    scene.add(gltf.scene);

    // Set initial scale and position
    gltf.scene.scale.set(1, 1, 1); // Adjust scale if needed
    gltf.scene.position.set(0, 0, 0);

    // Animate the model (rotation)
    const animate = function () {
        requestAnimationFrame(animate);

        // Basic rotation animation
        gltf.scene.rotation.y += 0.02; // Rotate around Y-axis

        renderer.render(scene, camera);
    };

    animate(); // Start animation loop

}, undefined, function (error) {
    console.error(error);
});
}

const AstronautAvatar = () => {
  return (
    <Canvas>
        <AstronautModel />
    </Canvas>
  );
};

export default AstronautAvatar;
  