
import { useGLTF } from '@react-three/drei';
import { useLoader } from '@react-three/fiber';
import React, { useRef } from 'react';

import * as THREE from 'three';

const Earth = () => {
	const texture = useLoader(THREE.TextureLoader, '/earth/textures/Material.002_diffuse.jpeg');
	const ref = useRef();
	useGLTF('/earth/earth.gltf');
	return(
				<mesh ref={ref} position={[7, -2, -11]}>
					<sphereGeometry args={[3, 32, 32]} />
					<meshStandardMaterial map={texture} />
				</mesh>
	)
}

export default Earth