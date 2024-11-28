import React, { useContext, useEffect, useState } from 'react';

import GameHistoryCard from './GameHistoryCard';
import Loader from './Loader';
import BaseButton from './Buttons/BaseButton';

import './GameHistoryList.css';

//import { UserContext } from '../contexts/UserContext' //CHANGE

const GameHistoryList = ({ targetId = 0 }) => {
    const [isLoading, setisLoading] = useState(false);
    const [history, setHistory] = useState([]);

    useEffect(() => {
        refresh();
    }, [targetId]);

    const refresh = async () => {
        setisLoading(true);
        try {
            const response = await fetch(`/api/game/user-history/${targetId}/`, {
                method: 'GET',
                credentials: 'include'
            });
            const json = await response.json();
            if (response.ok) {
                if (json?.success == true) {
                    setHistory(json?.games);
                }
            }
        } catch (error) {}
        setisLoading(false);
    };

    return (
        <div className='game-history col'>
            <header>
                <h3>History</h3>
                <BaseButton
                    onClick={refresh}
                    className='secondary round refresh'
                >
                    <i class="bi bi-arrow-clockwise"></i>
                </BaseButton>
            </header>
            <div className={`col content`}>
                <table>
                    <tbody>
                        {history.map((game) => (
                            <GameHistoryCard
                                key={game.id}
                                game={game}
                            />
                        ))}
                    </tbody>
                </table>
            </div>
        </div>
    );
}

export default GameHistoryList;
