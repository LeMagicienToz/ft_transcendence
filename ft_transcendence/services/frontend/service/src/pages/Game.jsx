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
	const { isLoading, gameId, isTournament, playerIndex, setCameraPosition, setBallPosition, setPlayerOnePosition, setPlayerTwoPosition, players, lCommand, rCommand, clear } = useContext(GameContext);

	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);
	const navigate = useNavigate();

	const sendMovement = (direction) => {
			socketRef.current.send(`{"action": "move", "direction": "${direction}"}`);
	};

	useEffect(() => {
		const handleKeyDown = (event) => {
			if (!currentKeyPressedRef.current) {
				currentKeyPressedRef.current = event.key;
				if (event.key === 'ArrowLeft') sendMovement(lCommand);
				else if (event.key === 'ArrowRight') sendMovement(rCommand);
			}
		};

		const handleKeyUp = (event) => {
			if (currentKeyPressedRef.current === event.key) {
				currentKeyPressedRef.current = null;
				sendMovement('off');
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
					//setBallPosition([ballPosition[1] / 9.9 - 15.2 + 0.5, 0.6, ballPosition[0] / 9.9 - 20.2 + 0.5]);
					//setPlayerOnePosition([playerPositions['1'][1] / 9.9 - 15 + 3.5, -1, -20.2]); //21
					//setPlayerTwoPosition([playerPositions['2'][1] / 9.9 - 15 + 3.5, -1, +20.2]); //7.4
					setBallPosition(prev => {
						const newPosition = [ballPosition[1] / 9.9 - 15.2 + 0.5, 0.6, ballPosition[0] / 9.9 - 20.2 + 0.5];
						return prev[0] !== newPosition[0] || prev[1] !== newPosition[1] || prev[2] !== newPosition[2] ? newPosition : prev;
					});
					setPlayerOnePosition(prev => {
						const newPosition = [playerPositions['1'][1] / 9.9 - 15 + 3.5, -1, -20.2];
						return prev[0] !== newPosition[0] || prev[1] !== newPosition[1] || prev[2] !== newPosition[2] ? newPosition : prev;
					});
					setPlayerTwoPosition(prev => {
						const newPosition = [playerPositions['2'][1] / 9.9 - 15 + 3.5, -1, +20.2];
						return prev[0] !== newPosition[0] || prev[1] !== newPosition[1] || prev[2] !== newPosition[2] ? newPosition : prev;
					});
					break;
				case 'ready_to_play':
					setTimeout(() => {
						setCameraPosition(playerIndex == 1 ? [0, 10, -35] : [0, 10, +35]);
					}, 1000);
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

