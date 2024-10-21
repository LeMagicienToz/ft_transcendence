import React, { useRef, useEffect } from 'react';
import { useGLTF } from '@react-three/drei';
import * as THREE from 'three';
import { useNavigate } from 'react-router-dom';

const easeInOutQuad = (t) => {
	return t < 0.5 ? 2 * t * t : -1 + (4 - 2 * t) * t;
};

const Spaceship = () => {
  const { scene } = useGLTF('/spaceship/spaceship.gltf'); // Replace with your GLTF file path
  const ref = useRef();
  const navigate = useNavigate();

  useEffect(() => {
    if (ref.current) {
      // Set initial position, rotation, and scale
	  ref.current.position.set(6.5, 0.5, -10); // Start far from the camera
	  ref.current.rotation.set(-Math.PI / 3, Math.PI / 8, 0.4); // Initial tilt and rotation
	  ref.current.scale.set(0.3, 0.3, 0.3); // Start small to simulate distance
    }

    const animationDuration = 30000; // Duration in milliseconds for the approach animation 15000
    const endPosition = new THREE.Vector3(2.2, -5, 4.5);
	const endRotation = new THREE.Vector3(Math.PI / 12, Math.PI / 4, 0.4);
    const endScale = new THREE.Vector3(2, 2, 2);

    const startTime = Date.now();

    // Function for position and scale animation
	const animate = () => {
		const elapsedTime = Date.now() - startTime;
		const progress = Math.min(elapsedTime / animationDuration, 1);
		const easedProgress = easeInOutQuad(progress); // Apply easing
  
		// Interpolate position and scale
		ref.current.position.lerp(endPosition, easedProgress);
		ref.current.scale.lerp(endScale, easedProgress);
  
		// Update rotation during the animation
		ref.current.rotation.x = THREE.MathUtils.lerp(ref.current.rotation.x, endRotation.x, easedProgress);
		ref.current.rotation.y = THREE.MathUtils.lerp(ref.current.rotation.y, endRotation.y, easedProgress);
		ref.current.rotation.z = THREE.MathUtils.lerp(ref.current.rotation.z, endRotation.z, easedProgress);
  
		// If the animation is complete, set final values
		if (progress < 0.17) {
		  requestAnimationFrame(animate);
		} else {
			// Set final position and rotation when done
			ref.current.position.copy(endPosition);
			ref.current.scale.copy(endScale);
			ref.current.rotation.copy(endRotation);
			console.log("abcdefg");
			setTimeout(() => {
				navigate('/Homepage');
			}, 0);
		}
	  };
  
	  animate(); // Start the animation
  
	}, [navigate]);

  return (
    <primitive
      object={scene}
      ref={ref}
      position={[0, -2, 0]} // Initial position of the spaceship
      scale={[1, 1, 1]} // Adjust scale as necessary
    />
  );
};

export default Spaceship;
