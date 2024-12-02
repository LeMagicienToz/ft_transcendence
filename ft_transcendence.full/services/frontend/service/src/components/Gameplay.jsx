import React, { useContext, useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { GameContext } from '../contexts/GameContext';
import { useToast } from '../contexts/ToastContext';

import Loader from './Loader';
import BaseButton from './Buttons/BaseButton';
import GameScene from '../scenes/GameScene';

import './Gameplay.css';

const Gameplay = () => {
	const { addToast } = useToast();
	const { gameId, listId, isStarted, setIsStarted, setBallPosition, setPlayerOnePosition, setPlayerTwoPosition, lCommand, rCommand, setScore, update, join, clear } = useContext(GameContext);

	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);
	const navigate = useNavigate();

	const send = (direction) => {
			socketRef.current.send(`{"action": "move", "direction": "${direction}"}`);
	};

	useEffect(() => {
		const handleKeyDown = (event) => {
			if (!currentKeyPressedRef.current) {
				currentKeyPressedRef.current = event.key;
				if (event.key === 'ArrowLeft') send(lCommand);
				else if (event.key === 'ArrowRight') send(rCommand);
			}
		};

		const handleKeyUp = (event) => {
			if (currentKeyPressedRef.current === event.key) {
				currentKeyPressedRef.current = null;
				if (event.key === 'ArrowLeft' || event.key === 'ArrowRight') send('off');
			}
		};

		window.addEventListener('keydown', handleKeyDown);
		window.addEventListener('keyup', handleKeyUp);

		return () => {
			window.removeEventListener('keydown', handleKeyDown);
			window.removeEventListener('keyup', handleKeyUp);
		};
	}, [lCommand, rCommand]);

	useEffect(() => {
		const socket = new WebSocket(`/wss/game/${gameId}/`);
		socketRef.current = socket;

		socket.onopen = () => {
			addToast('Connected.', 'success', 5000);
		};

		const normalize = (value, offset) => value / 9.9 + offset;

		socket.onmessage = (event) => {

			const data = JSON.parse(event.data);

			switch (data.game_data.status) {
				case 'playing':
					const playerPositions = data.game_data.player_positions;
					const ballPosition = data.game_data.ball_position;
					const dscore = data.game_data.scores;
					const ballX = normalize(ballPosition[1], -15.2) + 0.5;
					const ballZ = normalize(ballPosition[0], -20.2) + 0.5;
					setBallPosition([ballX, 0.6, ballZ]);
					const playerOneX = normalize(playerPositions['1'][1], -15) + 3.5;
					setPlayerOnePosition([playerOneX, -1, -20.2]);
					const playerTwoX = normalize(playerPositions['2'][1], -15) + 3.5;
					setPlayerTwoPosition([playerTwoX, -1, 20.2]);
					setScore([dscore['1'], dscore['2']]);
					break;
				case 'ready_to_play':
					update();
					setIsStarted(true);
					break;
				case 'finished':
					socket.close();
					setIsStarted(false);
					if (listId && listId.length > 0) {
						join(listId[0], listId)
					} else {
						clear();
						navigate('/home');
					}
					break;
				case 'abandoned':
					socket.close();
					setIsStarted(false);
					clear();
					addToast('The game was abandoned by a player.', 'failure', 5000);
					navigate('/home');
					break;
			}
		};

		socket.onerror = (error) => {
			addToast('Connection lost.', 'failure', 5000);
			navigate('/home');
		};

		return () => {
			if (socketRef.current) {
				socketRef.current.close();
			}
		};
	}, [gameId]);

	return (
		<div className={`gameplay`} >
			{!isStarted &&
				<div className={`loading`} >
					<Loader size='128px' />
					<p>Waiting for players...</p>
				</div>
			}
			<div className="game">
				<GameScene />
			</div>
			<div className="controls row">
				<div className="col">
					<BaseButton
						onTouchStart={() => send(lCommand)}
						onTouchEnd={() => send('off')}
						className='secondary round'
						icon='arrow-left'
					/>
				</div>
				<div className="col">
					<BaseButton
						onTouchStart={() => send(rCommand)}
						onTouchEnd={() => send('off')}
						className='secondary round'
						icon='arrow-right'
					/>
				</div>
			</div>
		</div>
	);
};

export default Gameplay;

