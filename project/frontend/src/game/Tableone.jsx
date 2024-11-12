import './Tableone.css';
import React, { useState, useEffect } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';
import MyButton from '../Theme/MyButton';

// Game Mode Switcher Component
const GameModeSwitcher = ({ gameMode, setGameMode }) => {
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
				<MyButton text="Create"></MyButton>
				<button className="arrow-button" onClick={handleLeftArrowClick}>
					←
				</button>
				<div className="game-mode-display">{gameMode}</div>
				<button className="arrow-button" onClick={handleRightArrowClick}>
					→
				</button>
			</div>
		</div>
	);
};

// Create Form Component

const CreateForm = ({ gameMode }) => {
	const [Rname, setRName] = useState('');
	const [nickname, setNickname] = useState('');
	const [winPoints, setwinPoints] = useState('');
	const [tournament, setTournament] = useState(false);
	const [numPlayers, setNumPlayers] = useState(gameMode === '1v1' ? 3 : 6);
	
	// Determine the minimum number of players based on the game mode
	const minPlayers = gameMode === '1v1' ? 3 : 6;
	
	// Update numPlayers when the game mode changes
	useEffect(() => {
		setNumPlayers(minPlayers);
	}, [gameMode]);
	
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
	
	return (
		<>
			<div className="title-gamemenu">Create Game ({gameMode})</div>
			<div className="Create-gamemenu">
				<div className="create-setting">
					<fieldset>
						<input
							type="text"
							placeholder="Room Name"
							value={Rname}
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
							value={winPoints}
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
	const [gameMode, setGameMode] = useState('1v1');

	return (
		<div className="Box-gamemenu">
			<GameModeSwitcher gameMode={gameMode} setGameMode={setGameMode} />
			{create ? <CreateForm gameMode={gameMode} /> : <JoinForm />}
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
