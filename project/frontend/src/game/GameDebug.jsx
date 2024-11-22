import './GameDebug.css';
import React, { useRef, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const SockCreator = ({ p1, gameid, token, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition, setPlayerOneScore, setPlayerTwoScore }) => {
	const socketRef = useRef(null);

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
			if (p1) {
				if (event.key === 'ArrowRight') {
					sendMovement('right');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('left');
				}
			}
			else {
				if (event.key === 'ArrowRight') {
					sendMovement('left');
				} else if (event.key === 'ArrowLeft') {
					sendMovement('right');
				}
			}
		};

		window.addEventListener('keydown', handleKeyDown);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);
		};
	}, []);

	// Gestion des WebSocket
	useEffect(() => {
		const socket = new WebSocket(`ws://localhost:8001/ws/game/${gameid}/?token=${token}`);
		socketRef.current = socket;

		socket.onopen = () => {
			console.log('WebSocket connected');
		};

		socket.onmessage = (event) => {
			const data = JSON.parse(event.data);
			console.log(data);

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
						setBallPosition({
							x: ballPosition[0],
							y: ballPosition[1],
						});
						setPlayerOnePosition({
							x: playerPositions['1'][0],
							y: playerPositions['1'][1],
						});
						setPlayerTwoPosition({
							x: playerPositions['2'][0],
							y: playerPositions['2'][1],
						});
						setPlayerOneScore(data.game_data.scores['1'])
						setPlayerTwoScore(data.game_data.scores['2'])
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
	}, [gameid, token, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition]);

	return null; // Pas d'interface utilisateur pour ce composant
};

const GameDebug = () => {
	const location = useLocation();
	const [playerOnePosition, setPlayerOnePosition] = useState([0, -1, -20.2]);
	const [ballPosition, setBallPosition] = useState([0, 0.2, 0]);
	const [playerTwoPosition, setPlayerTwoPosition] = useState([0, -1, 20.2]);
	const [playerOneScore, setPlayerOneScore] = useState(0);
	const [playerTwoScore, setPlayerTwoScore] = useState(0);
	const { gameData, isCreator } = location.state;

	const getHorizontalPercentage = (x) => {
		return (x / 400 * 100) + "%"
	}
	const getVerticalPercentage = (y) => {
		return (y / 300 * 100) + "%"
	}

	return (
		<div className="game-debug-container">
			<SockCreator
				p1={isCreator}
				gameid={gameData.game_id}
				token={gameData.token}
				setPlayerOnePosition={setPlayerOnePosition}
				setPlayerTwoPosition={setPlayerTwoPosition}
				setBallPosition={setBallPosition}
				setPlayerOneScore={setPlayerOneScore}
				setPlayerTwoScore={setPlayerTwoScore}
			/>
			<div className="game-debug-board">
				<div className="game-debug-player-score">
					{playerOneScore}
				</div>
				<div className="game-debug-player-score player-two">
					{playerTwoScore}
				</div>
				<div className="game-debug-ball" style={{
					left: getHorizontalPercentage(ballPosition.x),
					bottom: getVerticalPercentage(ballPosition.y),
					height: getVerticalPercentage(10),
					width: getHorizontalPercentage(10),
				}}></div>
				<div className="game-debug-player" style={{
					left: getHorizontalPercentage(playerOnePosition.x),
					bottom: getVerticalPercentage(playerOnePosition.y),
					height: getVerticalPercentage(70),
					width: getHorizontalPercentage(1),
				}}></div>
				<div className="game-debug-player" style={{
					left: getHorizontalPercentage(playerTwoPosition.x),
					bottom: getVerticalPercentage(playerTwoPosition.y),
					height: getVerticalPercentage(70),
					width: getHorizontalPercentage(1),
				}}></div>
			</div>
		</div>
	);
};

export default GameDebug;
