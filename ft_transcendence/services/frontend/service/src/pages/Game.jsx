import React, { useContext, useEffect, useState } from 'react';

import { GameContext } from '../contexts/GameContext';

import Gameplay from '../components/Gameplay';
import GameScore from '../components/GameScore';
import MatchesList from '../components/MatchesList';
import SpaceBackground from '../components/SpaceBackground';


import './Game.css';

const Game = () => {

	const { tournamentId, isStarted, players, score, clear } = useContext(GameContext);

	return (
		<div className={`page`} id={`page-game`} >
			<SpaceBackground />
			<section className={`view`} >
				<div className='info col'>
					<div className='score'>
						<GameScore
							players={players}
							score={score}
						/>
					</div>
					{tournamentId > 0 &&
						<div className='overview'>
							<MatchesList tournamentId={tournamentId} />
						</div>
					}
				</div>
				<Gameplay />
			</section>
		</div>
	);
};

export default Game;

