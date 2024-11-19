// import './WaitingRoom.css';
// import 'bootstrap/dist/css/bootstrap.min.css';
// import { useGLTF, PresentationControls, Stage } from '@react-three/drei';
// import { Canvas, useThree } from '@react-three/fiber';
// import React, { useRef, useEffect, useState } from 'react';
// import { useLocation } from 'react-router-dom';

// const CameraFollowPlayer = ({ playerPosition }) => {
// 	const { camera } = useThree();

// 	useEffect(() => {
// 		// Placer la caméra derrière PlayerOne (vue à la 3ème personne)
// 		// Légère élévation en Y, à 10 unités derrière le joueur en Z
// 		camera.position.set(playerPosition[0], playerPosition[1] + 3, playerPosition[2] + 10); // Monte un peu la caméra et la place derrière
// 		camera.lookAt(playerPosition[0], playerPosition[1], playerPosition[2]); // Faire en sorte que la caméra regarde vers PlayerOne
// 	}, [camera, playerPosition]);

// 	return null; // Pas d'UI, la caméra est configurée en direct
// };

// const PlayerOne = ({ position }) => {
// 	const { scene } = useGLTF('/gltf_files/avatar.gltf');
// 	const avatarRef = useRef();

// 	// Appliquez la position à chaque mise à jour
// 	useEffect(() => {
// 		if (avatarRef.current) {
// 			avatarRef.current.position.set(...position);
// 		}
// 	}, [position]);

// 	return (
// 			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
// 				<primitive ref={avatarRef} object={scene} />
// 			</Stage>
// 	);
// };

// const PlayerTwo = ({ position }) => {
// 	const { scene } = useGLTF('/gltf_files/playertwo.gltf');
// 	const avatarRef = useRef();
// 	const initialRotation = [0, Math.PI, 0];

// 	// Appliquez la position à chaque mise à jour
// 	useEffect(() => {
// 		if (avatarRef.current) {
// 			avatarRef.current.position.set(...position);
// 			avatarRef.current.rotation.set(...initialRotation);
// 		}
// 	}, [position]);

// 	return (
// 		//<PresentationControls speed={1.5} global zoom={0.7} polar={[-0.1, Math.PI / 4]}>
// 			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
// 				<primitive ref={avatarRef} object={scene} />
// 			</Stage>
// 		// </PresentationControls>
// 	);
// };

// const Board = () => {
// 	const { scene } = useGLTF('/gltf_files/onlyboardfinished.gltf');
// 	const boardRef = useRef();

// 	useEffect(() => {
// 		if (boardRef.current) {
// 			boardRef.current.position.set(0, 0, 0);
// 		}
// 	}, []);

// 	return (
// 			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
// 				<primitive ref={boardRef} object={scene} />
// 			</Stage>
// 	);
// };

// const SockCreator = ({ gameid, token, setPlayerOnePosition, setPlayerTwoPosition }) => {
// 	const socketRef = useRef(null);

// 	// Fonction pour envoyer les commandes de mouvement
// 	const sendMovement = (direction) => {
// 		if (socketRef.current && socketRef.current.readyState === WebSocket.OPEN) {
// 			const message = JSON.stringify({
// 				action: 'move',
// 				direction,
// 			});
// 			socketRef.current.send(message);
// 			console.log('Sent message:', message); // Log the message sent to the socket
// 		}
// 	};

// 	// Gestion des événements clavier
// 	useEffect(() => {
// 		const handleKeyDown = (event) => {
// 			if (event.key === 'ArrowRight') {
// 				console.log('Player pressed: ArrowRight'); // Log when the right arrow is pressed
// 				sendMovement('right');
// 			} else if (event.key === 'ArrowLeft') {
// 				console.log('Player pressed: ArrowLeft'); // Log when the left arrow is pressed
// 				sendMovement('left');
// 			}
// 		};

// 		window.addEventListener('keydown', handleKeyDown);

// 		return () => {
// 			window.removeEventListener('keydown', handleKeyDown);
// 		};
// 	}, []);

// 	// Gestion des WebSocket
// 	useEffect(() => {
// 		// Création de la connexion WebSocket
// 		const socket = new WebSocket(`ws://localhost:8001/ws/game/${gameid}/?token=${token}`);
// 		socketRef.current = socket;

// 		// Gestion des messages reçus
// 		socket.onmessage = (event) => {
// 			const data = JSON.parse(event.data);

// 			// Vérifiez si le message contient des positions
// 			if (data.game_data?.status === 'playing') {
// 				console.log('Message from server: ', data);

// 				const playerPositions = data.game_data.player_positions;
// 				if (playerPositions) {
// 					// Met à jour les positions des joueurs
// 					setPlayerOnePosition([playerPositions['1'][1] / 11.7 - 11.5, 0.3, -21]);
// 					setPlayerTwoPosition([playerPositions['2'][1] / 11.7 - 11.5, 0.3, 7.4]);
// 				}
// 			}
// 		};

// 		// Gestion des erreurs de WebSocket
// 		socket.onerror = (error) => {
// 			console.error('WebSocket Error: ', error);
// 		};

// 		// Nettoyage lors du démontage du composant
// 		return () => {
// 			if (socketRef.current) {
// 				socketRef.current.close(); // Ferme la connexion WebSocket
// 			}
// 		};
// 	}, [gameid, token, setPlayerOnePosition, setPlayerTwoPosition]);

// 	return null; // Pas d'interface utilisateur pour ce composant
// };


// const WaitingRoom = () => {
// 	const location = useLocation();
// 	const gameData = location.state?.gameData;
// 	const [playerOnePosition, setPlayerOnePosition] = useState([0, 0.3, -21]);
// 	const [playerTwoPosition, setPlayerTwoPosition] = useState([0, 0.3, 7.4]);

// 	return (
// 		<div className="game-container">
// 			<Canvas style={{ touchAction: 'none' }}>
// 				<ambientLight intensity={0.5} />
// 				<directionalLight position={[5, 5, 5]} />
// 				<SockCreator 
// 					gameid={gameData.game_id} 
// 					token={gameData.token}
// 					setPlayerOnePosition={setPlayerOnePosition}
// 					setPlayerTwoPosition={setPlayerTwoPosition}
// 				/>
// 				<PlayerOne position={playerOnePosition} />
// 				<PlayerTwo position={playerTwoPosition} />
// 				<Board/>
// 				<CameraFollowPlayer playerPosition={playerOnePosition} />
// 			</Canvas>
// 		</div>
// 	);
// };

// export default WaitingRoom;
// useGLTF.preload('/gltf_files/onlyboardfinished.gltf');
// useGLTF.preload('/gltf_files/playertwo.gltf');
// useGLTF.preload('/gltf_files/avatar.gltf');
