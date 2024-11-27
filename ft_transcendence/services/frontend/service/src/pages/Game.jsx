import React, { useContext, useRef, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { GameContext } from '../contexts/GameContext';
import { useToast } from '../contexts/ToastContext';

import Loading from './Loading';
import SpaceBackground from '../components/SpaceBackground';
import GameScene from '../scenes/GameScene';

import './Game.css';

const SockCreator = ({p1, gameid, setPlayerOnePosition, setPlayerTwoPosition, setBallPosition }) => {
	const socketRef = useRef(null);
	const currentKeyPressedRef = useRef(null);
	const navigate = useNavigate();

	const sendMovement = (direction) => {
			const message = JSON.stringify({
				action: 'move',
				direction,
			});
			socketRef.current.send(message);
	};

	// Gestion des événements clavier
	useEffect(() => {
		const handleKeyDown = (event) => {
			if (currentKeyPressedRef.current) {
				return ;
			}
			currentKeyPressedRef.current = event.key;
			if (event.key === 'ArrowRight') {
				sendMovement('left-on');
			} else if (event.key === 'ArrowLeft') {
				sendMovement('right-on');
			}
		};

		const handleKeyUp = (event) => {
			currentKeyPressedRef.current = null;
			if (event.key === 'ArrowRight') {
				sendMovement('left-off');
			} else if (event.key === 'ArrowLeft') {
				sendMovement('right-off');
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
		const socket = new WebSocket(`/wss/game/${gameid}/`);
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

				if (gameStatus === 'playing') {
					const playerPositions = data.game_data.player_positions;
					const ballPosition = data.game_data.ball_position;
					if (playerPositions) {
						// Met à jour les positions des joueurs et de la balle
						setBallPosition([ballPosition[1] / 9.9 - 15.2 + 0.5, 0.8, ballPosition[0] / 9.9 - 20.2 + 0.5]);
						setPlayerOnePosition([playerPositions['1'][1] / 9.9 - 15 + 3.5, -1, -20.2]);//21
						setPlayerTwoPosition([playerPositions['2'][1] / 9.9 - 15 + 3.5, -1, +20.2]);//7.4
					}
				}

				if (gameStatus === 'finished') {
					console.log('Game finished, closing WebSocket...');
					socket.close();
					return; // Sortir pour éviter toute gestion supplémentaire après la fermeture
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

const Game = () => {

	const { addToast } = useToast();
	const { isLoading, gameId, isPlayerOne, setBallPosition, setPlayerOnePosition, setPlayerTwoPosition } = useContext(GameContext);

	const sockRef = useRef(null);
	/*const location = useLocation();
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
	}, [isCreator]);*/

	return (
		<>
		{isLoading ? (
			<Loading />
		) : (
			<div className={`page`} id={`page-game`}>
				<SpaceBackground />
				<section className={`view`}>
				<SockCreator
					p1={isPlayerOne}
					gameid={gameId}
					setPlayerOnePosition={setPlayerOnePosition}
					setPlayerTwoPosition={setPlayerTwoPosition}
					setBallPosition={setBallPosition}
				/>
					<GameScene />
				</section>
			</div>
		)}
		</>
	);

	/*return (
		
	  <div className="game-container">
		<Canvas style={{ touchAction: 'none' }}>
		  <CameraControl isCreator={isCreator} />

		  <ambientLight intensity={0.5} />
		  <directionalLight position={[5, 5, 5]} />

		  <SockCreator
			p1={isCreator}
			gameid={gameData.game_id}
			token={gameData.token || gameData.token42}
			setPlayerOnePosition={setPlayerOnePosition}
			setPlayerTwoPosition={setPlayerTwoPosition}
			setBallPosition={setBallPosition}
		  />

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
	*/
  };

export default Game;

