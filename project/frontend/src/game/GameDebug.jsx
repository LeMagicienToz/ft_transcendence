import './GameDebug.css';
import React, { useRef, useEffect, useState } from 'react';
import { useLocation } from 'react-router-dom';

const SockCreator = ({ p1, gameid, gameStatus, token, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition, setPlayerOneScore, setPlayerTwoScore, setGameStatus }) => {
	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);

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
				setGameStatus(data.game_data.status)
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
	}, [gameid, token, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition]);

	useEffect(() => {
		if (gameStatus === 'finished' && socketRef.current) {
			socketRef.current.close();
			return;
		}
	}, [gameStatus])

	return null; // Pas d'interface utilisateur pour ce composant
};

const GameDebug = () => {
	const boardWidth = 400;
	const boardHeight = 300;
	const paddleSize = 70;
	const ballSize = 10;
	const location = useLocation();
	const [playerOnePosition, setPlayerOnePosition] = useState({ x: 0, y: (boardHeight / 2 - paddleSize / 2) });
	const [ballPosition, setBallPosition] = useState({ x: boardWidth / 2, y: boardHeight / 2 });
	const [playerTwoPosition, setPlayerTwoPosition] = useState({ x: boardWidth - 1, y: (boardHeight / 2 - paddleSize / 2) });
	const [playerOneScore, setPlayerOneScore] = useState(0);
	const [playerTwoScore, setPlayerTwoScore] = useState(0);
	const [gameStatus, setGameStatus] = useState("waiting");
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
				gameStatus={gameStatus}
				gameid={gameData.game_id}
				token={gameData.token}
				setPlayerOnePosition={setPlayerOnePosition}
				setPlayerTwoPosition={setPlayerTwoPosition}
				setBallPosition={setBallPosition}
				setPlayerOneScore={setPlayerOneScore}
				setPlayerTwoScore={setPlayerTwoScore}
				setGameStatus={setGameStatus}
			/>
			<div className="game-debug-board">
				<div className="game-debug-player-score">
					{playerOneScore}
				</div>
				<div className="game-debug-game-status">
					{gameStatus}
				</div>
				<div className="game-debug-player-score player-two">
					{playerTwoScore}
				</div>
				<div className="game-debug-ball" style={{
					left: getHorizontalPercentage(ballPosition.x),
					bottom: getVerticalPercentage(ballPosition.y),
					height: getVerticalPercentage(ballSize),
					width: getHorizontalPercentage(ballSize),
				}}></div>
				<div className="game-debug-player" style={{
					left: getHorizontalPercentage(playerOnePosition.x),
					bottom: getVerticalPercentage(playerOnePosition.y),
					height: getVerticalPercentage(paddleSize),
					width: getHorizontalPercentage(1),
				}}></div>
				<div className="game-debug-player" style={{
					left: getHorizontalPercentage(playerTwoPosition.x),
					bottom: getVerticalPercentage(playerTwoPosition.y),
					height: getVerticalPercentage(paddleSize),
					width: getHorizontalPercentage(1),
				}}></div>
			</div>
		</div>
	);
};

export default GameDebug;
