import './WaitingRoom.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useGLTF, PresentationControls, Stage } from '@react-three/drei';
import { Canvas, useThree } from "@react-three/fiber";
import React, { useRef, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';
import * as THREE from 'three';
import { useNavigate } from 'react-router-dom';


const hexToRgb = (hex) => {
	if (typeof hex === 'string') {
		const bigint = parseInt(hex.replace('#', ''), 16);
		const r = (bigint >> 16) & 255;
		const g = (bigint >> 8) & 255;
		const b = bigint & 255;
		return [r / 255, g / 255, b / 255];
	} else {
		return [1, 1, 1]; // Valeur par défaut pour éviter les erreurs
	}
};


const CameraControl = ({ isCreator }) => {
	const { camera } = useThree();

	useEffect(() => {
	  // Adjust camera position when `isCreator` changes
	  if (isCreator) {
		camera.position.set(0, 0.8, -16); // Position when user is creator
		camera.rotation.y = 90 * Math.PI / 180;
	  } else {
		camera.position.set(0, 0.8, 12.4); // Position when user is not creator
	  }
	  camera.updateProjectionMatrix(); // Update projection matrix after changing position
	}, [isCreator, camera]);

	return null;
  };

const fetchUserData = async () => {
		try {
			const response = await fetch('/api/auth/get_user/', {
				method: 'GET',
				headers: {
					'Content-Type': 'application/json',
				},
				credentials: 'include'
			});

			if (response.ok) {
				return await response.json();
			} else {
				const errorData = await response.json();
				console.log(errorData.error);
				return null;
			}
		} catch (error) {
			console.error("Erreur lors de la requête : ", error);
			return null;
		}
};

//IS CREATOR == TRUE

const PlayerOne = ({ position, suitColor, visColor, ringsColor, bpColor, flatness, horizontalPosition, verticalPosition, visTexture }) => {
	const { scene } = useGLTF('/gltf_files/playertwo.gltf');
	if (visTexture)
		{
			const textureLoader = new THREE.TextureLoader();
			visTexture = textureLoader.load(visTexture, (texture) => {
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
		}


	scene.traverse((child) => {
			if (child.isMesh)
				{
					// console.log("Player Two : ", child.name)
					if (child.name.includes('Cube002')) // Object_4 = suit
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(suitColor[0], suitColor[1], suitColor[2]);
						}
					}
					if (child.name.includes('Cube001')) { // Object_6 = visiere
						if (child.material instanceof THREE.MeshStandardMaterial) {
								if(visTexture)
								{
									child.material.map = visTexture;
									child.material.needsUpdate = true;

									child.material.metalness = 0;
									child.material.roughness = 1;
								}
							child.material.color.setRGB(visColor[0], visColor[1], visColor[2]);
						}
					}
					if (child.name.includes('Cube004') || child.name.includes('Torus')) // Object_8 rings
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(ringsColor[0], ringsColor[1], ringsColor[2]);
						}
					}
					if (child.name.includes('Cube007')) //Object_20 backpack
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(bpColor[0], bpColor[1], bpColor[2]);
						}
					}
				}
			});
			const avatarRef = useRef();

			useEffect(() => {
			  if (avatarRef.current) {
				// Directly set the position once when the component mounts
				avatarRef.current.position.set(position[0], -1, -20.2);
			  }
			}, [position]); // Re-run if the position prop changes

			return (
				<primitive ref={avatarRef} object={scene}/>
			);
		  };

const PlayerTwo = ({ position, suitColor, visColor, ringsColor, bpColor, flatness, horizontalPosition, verticalPosition, visTexture }) => {
	const { scene } = useGLTF('/gltf_files/avatar.gltf');
	if (visTexture)
		{
			const textureLoader = new THREE.TextureLoader();
			visTexture = textureLoader.load(visTexture, (texture) => {
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
		}


	scene.traverse((child) => {
			if (child.isMesh)
				{
					// console.log("Player Two : ", child.name)
					if (child.name.includes('Cube002')) // Object_4 = suit
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(suitColor[0], suitColor[1], suitColor[2]);
						}
					}
					if (child.name.includes('Cube001')) { // Object_6 = visiere
						if (child.material instanceof THREE.MeshStandardMaterial) {
								if(visTexture)
								{
									child.material.map = visTexture;
									child.material.needsUpdate = true;

									child.material.metalness = 0;
									child.material.roughness = 1;
								}
							child.material.color.setRGB(visColor[0], visColor[1], visColor[2]);
						}
					}
					if (child.name.includes('Cube004') || child.name.includes('Torus')) // Object_8 rings
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(ringsColor[0], ringsColor[1], ringsColor[2]);
						}
					}
					if (child.name.includes('Cube007')) //Object_20 backpack
					{
						if (child.material instanceof THREE.MeshStandardMaterial) {
							child.material.color.setRGB(bpColor[0], bpColor[1], bpColor[2]);
						}
					}
				}
			});
	const avatarRef = useRef();

	// Stocke la position actuelle
	const currentPosition = useRef(new THREE.Vector3(...position));

	useEffect(() => {
		if (avatarRef.current) {
			// Initialise la rotation

			const targetPosition = new THREE.Vector3(...position);

			// Animation frame loop pour interpoler la position
			const updatePosition = () => {
				// Lerp vers la nouvelle position
				currentPosition.current.lerp(targetPosition, 0.1);
				avatarRef.current.position.copy(currentPosition.current);

				// Continue le rendu
				requestAnimationFrame(updatePosition);
			};

			updatePosition();
		}
	}, [position]);

	return (
				<primitive ref={avatarRef} object={scene} />

	);
};

const Ball= ({position}) => {
	const { scene } = useGLTF('/ball/scene.gltf');
	const ballRef = useRef();

	// Stocke la position actuelle
	const currentPosition = useRef(new THREE.Vector3(...position));
	const distance = position[2] - currentPosition.z;
	useEffect(() => {
		if (ballRef.current) {
			const targetPosition = new THREE.Vector3(...position);
			// Animation frame loop pour interpoler la position
			const updatePosition = () => {
				// Lerp vers la nouvelle position
				if (distance < 10) {
					currentPosition.current.lerp(targetPosition, 0.1);
				} else {
					//no animation when distance is very big (most likely reset initial position)
					currentPosition.current = targetPosition;
				}
				ballRef.current.position.copy(currentPosition.current);

				// Continue le rendu
				requestAnimationFrame(updatePosition);
			};

			updatePosition();
		}
	}, [position]);

	return (
				<primitive ref={ballRef} object={scene} />
	);
};


const Board = ({ isCreator }) => {
	const { scene } = useGLTF('/gltf_files/onlyboardfinished.gltf');
	const boardRef = useRef();

	useEffect(() => {
	  // Ensure that the ref is properly initialized before setting the position
	  if (boardRef.current) {
		boardRef.current.position.set(0, 0, 0); // Set position to (0, 0, 0)
	  }
	}, []); // Empty dependency array to run only once after the initial render

	return (
		<primitive ref={boardRef} object={scene} />
	);
  };

const SockCreator = ({p1, gameid, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition }) => {
	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);
	const navigate = useNavigate();

	const sendMovement = (direction) => {
		if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
			const message = JSON.stringify({
				action: 'move',
				direction,
			});
			socketRef.current.send(message);
		}
	};

	// Gestion des événements clavier
	useEffect(() => {
		const handleKeyDown = (event) => {
			if (currentKeyPressedRef.current) {
				return ;
			}
			currentKeyPressedRef.current = event.key;
			if (p1) {
				if (event.key === 'ArrowRight') {
					sendMovement('right-on');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('left-on');
				}
			}
			else {
				if (event.key === 'ArrowRight') {
					sendMovement('left-on');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('right-on');
				}
			}
		};

		const handleKeyUp = (event) => {
			currentKeyPressedRef.current = null;
			if (p1) {
				if (event.key === 'ArrowRight') {
					sendMovement('right-off');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('left-off');
				}
			}
			else {
				if (event.key === 'ArrowRight') {
					sendMovement('left-off');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('right-off');
				}
			}
		};

		window.addEventListener('keydown', handleKeyDown);
		window.addEventListener('keyup', handleKeyUp);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
		};
	}, []);

	// Gestion des WebSocket
	let socket;
	useEffect(() => {
		const socket = new WebSocket(`wss://localhost:8443/ws/game/${gameid}/`);
		socketRef.current = socket;

		socket.onopen = () => {
			console.log('WebSocket connected');
		};

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			// console.log(data);

			// Vérifiez le statut de la partie
			if (data.game_data?.status) {
				const gameStatus = data.game_data.status;

				if (gameStatus === 'finished') {
					console.log('Game finished, closing WebSocket...');
					socket.close();
					return; // Sortir pour éviter toute gestion supplémentaire après la fermeture
				}

				if (gameStatus === 'playing') {
					const playerPositions = data.game_data.player_positions;
					const ballPosition = data.game_data.ball_position;
					if (playerPositions) {
						// Met à jour les positions des joueurs et de la balle
						setBallPosition([ballPosition[1] / 9.9 - 15.2 + 0.5, 0.2, ballPosition[0] / 9.9 - 20.2 + 0.5]);
						setPlayerOnePosition([playerPositions['1'][1] / 9.9 - 15 + 3.5, -1, -20.2]);//21
						setPlayerTwoPosition([playerPositions['2'][1] / 9.9 - 15 + 3.5, -1, 20.2]);//7.4
					}
				}
			}
		};

		socket.onerror = (error) => {
			console.error('WebSocket Error: ', error);
		};

		socket.onclose = () => {
			console.log('WebSocket closed');
			// setTimeout(() => {
			// 	navigate('/homepage');
			// }, 5000); // 2000 ms = 2 secondes
		};

		// Nettoyage lors du démontage
		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, [gameid, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition]);

	return null; // Pas d'interface utilisateur pour ce composant
};

const WaitingRoom = () => {
	const location = useLocation();
	const [userData, setUserData] = useState(null);
	const [userDataTwo, setUserDataTwo] = useState(null);
	const [playerOnePosition, setPlayerOnePosition] = useState([0, -1, -20.2]);
	const [ballPosition, setBallPosition] = useState([0, 0.2, 0]);
	const [playerTwoPosition, setPlayerTwoPosition] = useState([0, -1, 20.2]);
	const { gameData, isCreator } = location.state;

	useEffect(() => {
	  const getUserData = async () => {
		try {
		  const data = await fetchUserData();
		  if (data) {
			if (isCreator) {
			  setUserData(data); // If the player is the creator
			} else {
			  setUserDataTwo(data); // If not the creator
			}
		  } else {
			setError("Impossible de récupérer les données utilisateur");
		  }
		} catch (error) {
		  setError("Erreur lors de la récupération des données utilisateur");
		}
	  };

	  getUserData();
	}, [isCreator]);

	return (
	  <div className="game-container">
		<Canvas style={{ touchAction: 'none' }}>
		  <CameraControl isCreator={isCreator} />

		  <ambientLight intensity={0.5} />
		  <directionalLight position={[5, 5, 5]} />

		  <SockCreator
			p1={isCreator}
			gameid={gameData.game_id}
			setPlayerOnePosition={setPlayerOnePosition}
			setPlayerTwoPosition={setPlayerTwoPosition}
			setBallPosition={setBallPosition}
		  />

		  {/* Render both avatars in the same Canvas */}

		<PresentationControls speed={1.5} global zoom={0.7} polar={[0, 0]}>
			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
				<PlayerOne
					position={playerOnePosition}
					suitColor={hexToRgb(userData?.suitColor || '#FFFFFF')}
					visColor={hexToRgb(userData?.visColor || '#FFFFFF')}
					ringsColor={hexToRgb(userData?.ringsColor || '#FFFFFF')}
					bpColor={hexToRgb(userData?.bpColor || '#FFFFFF')}
					flatness={userData?.flatness || 2.8}
					horizontalPosition={userData?.horizontalPosition || 0.73}
					verticalPosition={userData?.verticalPosition || 0.08}
					visTexture={userData?.visTexture || null}
					/>

				<PlayerTwo
					position={playerTwoPosition}
					suitColor={hexToRgb(userDataTwo?.suitColor || '#FFFFFF')}
					visColor={hexToRgb(userDataTwo?.visColor || '#FFFFFF')}
					ringsColor={hexToRgb(userDataTwo?.ringsColor || '#FFFFFF')}
					bpColor={hexToRgb(userDataTwo?.bpColor || '#FFFFFF')}
					flatness={userDataTwo?.flatness || 2.8}
					horizontalPosition={userDataTwo?.horizontalPosition || 0.73}
					verticalPosition={userDataTwo?.verticalPosition || 0.08}
					visTexture={userDataTwo?.visTexture || null}
					/>

				<Ball position={ballPosition} />
				<Board isCreator={isCreator} />
			</Stage>
		</PresentationControls>

		</Canvas>
	  </div>
	);
  };

export default WaitingRoom;
useGLTF.preload('/gltf_files/onlyboardfinished.gltf');
useGLTF.preload('/gltf_files/playertwo.gltf');
useGLTF.preload('/gltf_files/avatar.gltf');
