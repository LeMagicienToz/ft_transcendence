import React from 'react';
import { useGLTF, PresentationControls, Stage } from '@react-three/drei';
import * as THREE from 'three';

const Avatarhp = ({ suitColor, visColor, ringsColor, bpColor }) => {

	const { scene } = useGLTF('/scene.gltf');
	scene.traverse((child) => {
        if (child.isMesh) 
			{
				if (child.name.includes('Object_4')) // Object_4 = suit
				{
                    if (child.material instanceof THREE.MeshStandardMaterial) {
                        child.material.color.setRGB(suitColor[0], suitColor[1], suitColor[2]);
					}
				}
				if (child.name.includes('Object_6')) // Object_6 = visiere
				{
                    if (child.material instanceof THREE.MeshStandardMaterial) {
                        child.material.color.setRGB(visColor[0], visColor[1], visColor[2]);
					}
				}
				if (child.name.includes('Object_8')) // Object_8 rings
				{
                    if (child.material instanceof THREE.MeshStandardMaterial) {
                        child.material.color.setRGB(ringsColor[0], ringsColor[1], ringsColor[2]);
					}
				}  
				if (child.name.includes('Object_20')) //Object_20 backpack
				{
                    if (child.material instanceof THREE.MeshStandardMaterial) {
                        child.material.color.setRGB(bpColor[0], bpColor[1], bpColor[2]);
					}
				} 
			}
		});
		return(
        <PresentationControls speed={1.5} global zoom={0.7} polar={[-0.1,Math.PI / 4]}>
            <Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environement="forest">
            <primitive object={scene} />;
         </Stage>
        </PresentationControls>
        )
	};

export default Avatarhp;

useGLTF.preload('/scene.gltf');
