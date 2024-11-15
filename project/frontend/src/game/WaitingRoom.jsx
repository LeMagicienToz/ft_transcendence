import './WaitingRoom.css';
import 'bootstrap/dist/css/bootstrap.min.css';
import { useGLTF, PresentationControls, Stage } from '@react-three/drei';
import { Canvas } from '@react-three/fiber';
import React, { useRef, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const PlayerOne = () => {
	const { scene } = useGLTF('/gltf_files/avatar.gltf');
	const avatarRef = useRef();
	const [position, setPosition] = useState([0, 0.3, -21]);

	// Appliquer la position initiale au modèle GLTF
	useEffect(() => {
		if (avatarRef.current) {
			avatarRef.current.position.set(...position);
		}
	}, [position]);

	return (
		<PresentationControls speed={1.5} global zoom={0.7} polar={[-0.1, Math.PI / 4]}>
			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
				<primitive ref={avatarRef} object={scene} />
			</Stage>
		</PresentationControls>
	);
};


const PlayerTwo = () => {
	const { scene } = useGLTF('/gltf_files/playertwo.gltf');
	const avatarRef = useRef();
	const [position, setPosition] = useState([0, 0.3, 7.4]);
	const initialRotation = [0, Math.PI, 0];

	// Appliquer la position initiale au modèle GLTF
	useEffect(() => {
		if (avatarRef.current) {
			avatarRef.current.position.set(...position);
			avatarRef.current.rotation.set(...initialRotation);
		}
	}, [position]);

	return (
		<PresentationControls speed={1.5} global zoom={0.7} polar={[-0.1, Math.PI / 4]}>
		<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
			<primitive ref={avatarRef} object={scene} />
		</Stage>
	</PresentationControls>
	);
};

const Board = () => {
	const { scene } = useGLTF('/gltf_files/onlyboardfinished.gltf');
	const boardRef = useRef();

	useEffect(() => {
		if (boardRef.current) {
			boardRef.current.position.set(0, 0, 0);
		}
	}, []);

	return (
		<PresentationControls speed={1.5} global zoom={0.7} polar={[-0.1, Math.PI / 4]}>
			<Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
				<primitive ref={boardRef} object={scene} />
			</Stage>
		</PresentationControls>
	);
};

const SockCreator = ({gameid, token, token42}) => {
	const [response, setResponse] = useState('');
	let socket;

	useEffect(() => {
		// Connexion au WebSocket
		socket = new WebSocket(`ws://localhost:8001/ws/game/${gameid}/?token=${token}`);

		// Quand la connexion est ouverte
		socket.onopen = () => {
			console.log('WebSocket is open now.');
		};
	}, []);
}  

const WaitingRoom = () => {
	const location = useLocation();
	const gameData = location.state?.gameData;
	// console.log(gameData);
	// console.log("dwadwa");

	// toke42={gameData.token42}

	return (
		<div className="game-container">
			<Canvas style={{ touchAction: 'none' }}>
				<ambientLight intensity={0.5} />
				<directionalLight position={[5, 5, 5]} />
				<SockCreator gameid={gameData.game_id} token={gameData.token}/>
				<PlayerOne />
				<PlayerTwo/>
				<Board/>
			</Canvas>
		</div>
	);
};

export default WaitingRoom;
useGLTF.preload('/gltf_files/onlyboardfinished.gltf');
useGLTF.preload('/gltf_files/playertwo.gltf');
useGLTF.preload('/gltf_files/avatar.gltf');
