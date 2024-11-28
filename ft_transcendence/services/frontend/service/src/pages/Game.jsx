import React, { useContext, useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { GameContext } from '../contexts/GameContext';
import { useToast } from '../contexts/ToastContext';

import Loading from './Loading';
import SpaceBackground from '../components/SpaceBackground';
import GameScene from '../scenes/GameScene';

import './Game.css';

const Game = () => {

	const { addToast } = useToast();
	const { isLoading, gameId, setCameraPosition, setBallPosition, setPlayerOnePosition, setPlayerTwoPosition, players, isTournament, isPlayerOne, clear } = useContext(GameContext);

	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);
	const navigate = useNavigate();

	const sendMovement = (direction) => {
			socketRef.current.send(`{"action": "move", "direction": "${direction}"}`);
	};

	useEffect(() => {
		const handleKeyDown = (event) => {
			if (!currentKeyPressedRef.current && (event.key === 'ArrowRight' || event.key === 'ArrowLeft')) {
				currentKeyPressedRef.current = event.key;
				sendMovement(event.key === 'ArrowRight' ? 'left-on' : 'right-on');
			}
		};

		const handleKeyUp = (event) => {
			if (currentKeyPressedRef.current === event.key) {
				currentKeyPressedRef.current = null;
				sendMovement(event.key === 'ArrowRight' ? 'left-off' : 'right-off');
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
	useEffect(() => {
		const socket = new WebSocket(`/wss/game/${gameId}/`);
		socketRef.current = socket;

		socket.onopen = () => {
			console.log('WebSocket connected');
		};

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			console.log(data);

			// Vérifiez le statut de la partie

			const playerPositions = data.game_data.player_positions;
			const ballPosition = data.game_data.ball_position;

			switch (data.game_data.status) {
				case 'playing':
					setBallPosition([ballPosition[1] / 9.9 - 15.2 + 0.5, 0.6, ballPosition[0] / 9.9 - 20.2 + 0.5]);
					setPlayerOnePosition([playerPositions['1'][1] / 9.9 - 15 + 3.5, -1, -20.2]); //21
					setPlayerTwoPosition([playerPositions['2'][1] / 9.9 - 15 + 3.5, -1, +20.2]); //7.4
					break;
				case 'ready_to_play':
					console.log('ready', isTournament);
					break;
				case 'finished':
					socket.close();
					clear();
					navigate('/home');
					return;
			}
		};

		socket.onerror = (error) => {
			console.error('WebSocket Error: ', error);
		};

		socket.onclose = () => {
			console.log('WebSocket closed');
		};

		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, []);

	return (
		<>
		{isLoading ? (
			<Loading />
		) : (
			<div className={`page`} id={`page-game`}>
				<SpaceBackground />
				<section className={`view`}>
					<GameScene />
				</section>
			</div>
		)}
		</>
	);
};

export default Game;

