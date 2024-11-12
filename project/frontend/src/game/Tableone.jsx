import './Tableone.css';
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import MyButton from '../Theme/MyButton';

// Game Mode Switcher Component
const GameModeSwitcher = ({ match_type, setGameMode }) => {
	// Switch to the previous mode
	const handleLeftArrowClick = () => {
		setGameMode((prevMode) => (prevMode === '1v1' ? '2v2' : '1v1'));
	};

	// Switch to the next mode
	const handleRightArrowClick = () => {
		setGameMode((prevMode) => (prevMode === '1v1' ? '2v2' : '1v1'));
	};

	return (
		<div className="game-mode-container">
			<h2>Game Mode</h2>
			<div className="game-mode-switcher">
				<button className="arrow-button" onClick={handleLeftArrowClick}>
					←
				</button>
				<div className="game-mode-display">{match_type}</div>
				<button className="arrow-button" onClick={handleRightArrowClick}>
					→
				</button>
			</div>
		</div>
	);
};

// Create Form Component

const CreateForm = ({ match_type }) => {

	const [game_type, setGameType] = useState('pong');
	const [game_custom_name, setRName] = useState('');
	const [nickname, setNickname] = useState('');
	const [score_to_win, setwinPoints] = useState('');
	const [tournament, setTournament] = useState(false);
	const [numPlayers, setNumPlayers] = useState(match_type === '1v1' ? 3 : 6);
	
	// Determine the minimum number of players based on the game mode
	const minPlayers = match_type === '1v1' ? 3 : 6;
	
	// Update numPlayers when the game mode changes
	useEffect(() => {
		setNumPlayers(minPlayers);
	}, [match_type]);
	
	// Toggle the tournament state
	const handleTournamentChange = () => {
		setTournament(!tournament);
	};
	
	// Ensure the number of players does not go below the minimum
	const handleNumPlayersChange = (e) => {
		const value = parseInt(e.target.value, 10);
		if (value >= minPlayers) {
			setNumPlayers(value);
		}
	};

	const handleClick = async (e) => {
		e.preventDefault();

		try {
			const response = await fetch('/api/game/create/', {
				method: 'POST',
				headers: {
					'Content-Type': 'application/json',
				},
				body: JSON.stringify({ game_type, game_custom_name, score_to_win, nickname, match_type}),
				credentials: 'include',
			});

			if (response.ok) {
				// const data = await response.json();
				console.log("OOOOOOOOOKKK");
				// navigate('/waitingroom');
			} else {
				console.log("Non-200 response", response.status, response.statusText);
			}
		} catch (err) {
			console.error("Fetch error:", err);
		}
	};
	
	return (
		<>
			<div className="title-gamemenu">Create Game ({match_type})</div>
			<div className="Create-gamemenu">
				<div className="create-setting">
					<MyButton onClick={handleClick} text="create"></MyButton>
					<fieldset>
						<input
							type="text"
							placeholder="Room Name"
							value={game_custom_name}
							onChange={(e) => setRName(e.target.value)}
						/>
						<input
							type="text"
							placeholder="Nickname"
							value={nickname}
							onChange={(e) => setNickname(e.target.value)}
						/>
						<div>
							<input
								type="checkbox"
								name="Tournament"
								id="Tournament"
								checked={tournament}
								onChange={handleTournamentChange}
							/>
							<label htmlFor="Tournament">Tournament</label>
						</div>
						<input
							type="number"
							placeholder="Number of players"
							min={minPlayers}
							max='40'
							value={numPlayers}
							onChange={handleNumPlayersChange}
							disabled={!tournament}
						/>
						<small>Players: {minPlayers} to 40</small>
						<input
							type="number"
							placeholder="Points to Win"
							min='1'
							max='10'
							value={score_to_win}
							onChange={(e) => setwinPoints(e.target.value)}
						/>
						<small>Points: 1 to 10</small>
					</fieldset>
				</div>
			</div>
		</>
	);
};

// Join Form Component
const JoinForm = () => {
	const data = fetchUserData();
	return (
		<div className="Join-gamemenu">
			<h3>Join Game</h3>
			<form>
				<input type="text" placeholder="Search..." />
				<button type="submit">Search</button>
			</form>
		</div>
	);
};

// Main Tableone Component
const Tableone = ({create}) => {
	const [match_type, setGameMode] = useState('1v1');

	return (
		<div className="Box-gamemenu">
			<GameModeSwitcher match_type={match_type} setGameMode={setGameMode} />
			{create ? <CreateForm match_type={match_type} /> : <JoinForm />}
		</div>
	);
};



const fetchUserData = async () => {
	try {
	  const response = await fetch('/api/game/list/', {
		method: 'GET',
		headers: {
		  'Content-Type': 'application/json',
		},
		credentials: 'include'
	  });
  
	  if (response.ok) {
		const data = await response.json();
		console.log(data);
		return(data);
	  } else {
		  const errorData = await response.json();
		  console.log(errorData.error);
		}
	} catch (error) {
	  console.error("Erreur lors de la requête : ", error);
	  console.log("Une erreur est survenue");
	}
  };

export default Tableone;
