import React, { useContext, useEffect, useState } from 'react';

import GameHistoryCard from './GameHistoryCard';
import Loader from './Loader';
import BaseButton from './Buttons/BaseButton';

import './GameHistoryList.css';

//import { UserContext } from '../contexts/UserContext' //CHANGE

const GameHistoryList = ({ targetId = 0 }) => {
    const [isLoading, setisLoading] = useState(false);
    const [history, setHistory] = useState([]);

    //const {userId} = useContext(UserContext) //CHANGE

    /*const fakeHistory = [ //CHANGE
        {
            'id': 1,
            'game_custom_name': 'Game 1',
            'status': 'completed',
            'game_type': 'Tournament',
            'match_type': '1v1',
            'score_to_win': 10,
            'tournament_id': 101,
            'creation_time': '2023-10-01T10:00:00Z',
            'start_time': '2023-10-01T10:05:00Z',
            'end_time': '2023-10-01T10:30:00Z',
            'has_won': true,
            'players': [
                {
                    'user_id': userId,
                    'user_name': 'Player1',
                    'score': 10,
                    'nickname': 'P1',
                    'player_index': 0,
                },
                {
                    'user_id': userId,
                    'user_name': 'Player2',
                    'score': 8,
                    'nickname': 'P2',
                    'player_index': 1,
                }
            ]
        },
        {
            'id': 2,
            'game_custom_name': 'Game 2',
            'status': 'completed',
            'game_type': 'Normal',
            'match_type': '2v2',
            'score_to_win': 15,
            'tournament_id': 102,
            'creation_time': '2023-10-02T11:00:00Z',
            'start_time': '2023-10-02T11:10:00Z',
            'end_time': '2023-10-02T11:50:00Z',
            'has_won': false,
            'players': [
                {
                    'user_id': userId,
                    'user_name': 'Player3',
                    'score': 12,
                    'nickname': 'P3',
                    'player_index': 0,
                },
                {
                    'user_id': userId,
                    'user_name': 'Player4',
                    'score': 15,
                    'nickname': 'P4',
                    'player_index': 1,
                },
                {
                    'user_id': userId,
                    'user_name': 'Player3',
                    'score': 12,
                    'nickname': 'P3',
                    'player_index': 0,
                },
                {
                    'user_id': userId,
                    'user_name': 'Player4',
                    'score': 15,
                    'nickname': 'P4',
                    'player_index': 1,
                }
            ]
        }
    ];*/

    useEffect(() => {
        //setHistory(prevHistory => [...prevHistory, ...fakeHistory]); //CHANGE
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
                    text='⟳'
                />
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
