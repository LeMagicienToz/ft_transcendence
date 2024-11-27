import React, { useContext, useState } from 'react';

import { UserContext } from '../contexts/UserContext';

import './GameListCard.css';
import GameJoinWindow from './Windows/GameJoinWindow'

const GameListCard = ({ game = {} }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [joinGameWindowState, setJoinGameWindowState] = useState(false);

    const { username } = useContext(UserContext);

    const handleClick = async () => {
        setIsLoading(true);
        /*try {
            const response = await fetch(
                `${game?.tournament_id === 0 ? `/api/game/join${game?.tournament_id}/` : `/api/game/tournament/join${game?.tournament_id}/`}`, {
                method: 'PUT',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ nickname: player?.user_id }),
                credentials: 'include'
            });
            const json = await response.json();
            if (response.ok) {
                return { ...player, ...json };
            }
        } catch (error) {}*/
        setIsLoading(false);
    };

    return (
        <>
            <GameJoinWindow
                onClose={() => setJoinGameWindowState(false)}
                isOpen={joinGameWindowState}
                game={game}
            />
            <tr className='game-list-card' onClick={() => setJoinGameWindowState(true)} >
                <td className='elem' >
                    <div className={`status ${game?.status || ''}`} ></div>
                </td>
                <td className='elem' >
                    <p className={`main`} >{game?.custom_name || 'N/A'}</p>
                    <p className={`sub`} >{game?.players[0].nickname || 'N/A'}</p>
                </td>
                <td className='elem' >
                    <p className={`main`} >{(game?.type === 'game' ? 'Normal' : 'Tournament') || 'N/A'}</p>
                    <p className={`sub`} >{game?.match_type || 'N/A'}</p>
                </td>
                <td className='elem score' >
                    <p className={`main`} >Score: {game?.score_to_win}</p>
                </td>
                <td className='elem' >
                    <p className={`main`} >{game?.players.length}/{game?.type === 'tournament' ? game?.player_count : (game?.match_type === '1v1' ? '2' : '4') }</p>
                </td>
            </tr>
        </>
    );
}

export default GameListCard;
