import React, { useEffect, useState } from 'react';

import GameListCard from './GameListCard';
import Loader from './Loader';
import BaseButton from './Buttons/BaseButton';
import GameCreateWindow from './Windows/GameCreateWindow';

import './MatchesList.css';

const MatchesList = ({ tournamentId = 0 }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [games, setGames] = useState([]);

    useEffect(() => {
        refresh();
        const interval = setInterval(refresh, 5000);
        return () => clearInterval(interval);
    }, [tournamentId]);

    const refresh = async () => {
        setIsLoading(true);
        try {
            const response = await fetch(`/api/game/tournament/details/${tournamentId}/`, {
            method: 'GET',
            credentials: 'include'
            });
            const json = await response.json();
            if (response.ok) {
                if (json?.success == true) {
                    setGames(json?.data.games);
                }
            }
        } catch (error) {}
        setIsLoading(false);
    };

    return (
        <div className='matches-list col'>
            <header>
                <h3>Matches</h3>
                <BaseButton
                    onClick={refresh}
                    className='secondary round refresh'
                >
                    <i class="bi bi-arrow-clockwise"></i>
                </BaseButton>
            </header>
            <div className={`content col`} >
                {games.map((game, index) => (
                    <p>{game.players[0].nickname} VS {game.players[1].nickname}</p>
                ))}
            </div>
        </div>
    );
}

export default MatchesList;
