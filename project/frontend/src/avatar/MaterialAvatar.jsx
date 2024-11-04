import React from 'react';
import { useGLTF, PresentationControls, Stage } from '@react-three/drei';
// import "./AstronautAvatar.css";
import * as THREE from 'three';


const MaterialAvatar = ({ suitColor, visColor, ringsColor, bpColor, flatness, horizontalPosition, verticalPosition }) => {

	const { scene } = useGLTF('/scene.gltf');
	const textureLoader = new THREE.TextureLoader();
	const visTexture = textureLoader.load('https://cdn.intra.42.fr/users/df0b59b389617dbb05954acb33173422/muteza.jpg', (texture) => {
		// Ajustez la répétition pour réduire la taille de la texture
		texture.repeat.set(2, flatness); // augmente le deuxieme pour applatir la texture
		texture.wrapS = THREE.RepeatWrapping; // Permet à la texture de se répéter horizontalement
		texture.wrapT = THREE.RepeatWrapping; // Permet à la texture de se répéter verticalement
	
		texture.rotation = -Math.PI / 2; // 90 degrés en radians
	    texture.center.set(0.5, 0.5); // Centre de rotation pour éviter un décalage
        texture.offset.set(horizontalPosition, verticalPosition); // change plutot ca pour decaler la texture ( augmente le premier pour aller a gauche, augmente le deuxieme pour aller en bas)
    texture.image.onload = () => {
        const textureWidth = texture.image.width;
        const textureHeight = texture.image.height;

        // Ajuster la taille et centrer la texture
        adjustTextureSizeAndPosition(child, textureWidth, textureHeight);
    };
});

scene.traverse((child) => {
        if (child.isMesh) 
			{
                // console.log(child.name)
				if (child.name.includes('Object_4')) // Object_4 = suit
				{
                    if (child.material instanceof THREE.MeshStandardMaterial) {
                        child.material.color.setRGB(suitColor[0], suitColor[1], suitColor[2]);
					}
				}
				if (child.name.includes('Object_6')) { // Object_6 = visiere
					if (child.material instanceof THREE.MeshStandardMaterial) {
						child.material.map = visTexture;
						child.material.needsUpdate = true;
				
						child.material.metalness = 0;
						child.material.roughness = 1;
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

export default MaterialAvatar;

useGLTF.preload('/scene.gltf');
