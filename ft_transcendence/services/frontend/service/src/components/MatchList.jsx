import React, { useEffect, useState } from 'react';

import BaseButton from './Buttons/BaseButton';
import MatchListCard from './MatchListCard';

import './MatchList.css';

const MatchList = ({ tournamentId = 0 }) => {
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
        <div className='match-list col' >
            <header>
                <h3>Matches</h3>
                <BaseButton
                    onClick={refresh}
                    className='secondary round refresh'
                >
                    <i class="bi bi-arrow-clockwise"></i>
                </BaseButton>
            </header>
            <div className={`col content`}>
                {games.map((game, index) => (
                    <MatchListCard game={game} />
                ))}
            </div>
        </div>
    );
}

export default MatchList;
