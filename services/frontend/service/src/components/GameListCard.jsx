import React, { useContext, useState } from 'react';

import GameJoinWindow from './Windows/GameJoinWindow'

import './GameListCard.css';

const GameListCard = ({ game = {} }) => {
    const [joinGameWindowState, setJoinGameWindowState] = useState(false);

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
                <td className='elem type' >
                    <p className={`main`} >{(game?.type === 'game' ? 'Normal' : 'Tournament') || 'N/A'}</p>
                    <p className={`sub`} >{game?.match_type || 'N/A'}</p>
                </td>
                <td className='elem score' >
                    <p className={`main`} >Score: {game?.score_to_win}</p>
                </td>
                <td className='elem count' >
                    <p className={`main`} >{game?.joined_players_count}/{game?.player_count}</p>
                </td>
            </tr>
        </>
    );
}

export default GameListCard;
