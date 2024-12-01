import React, { useEffect, useState } from 'react';

import GameListCard from './GameListCard';
import Loader from './Loader';
import BaseButton from './Buttons/BaseButton';
import GameCreateWindow from './Windows/GameCreateWindow';

import './MatchListCard.css';

const MatchListCard = ({ game = {} }) => {

    return (
        <div className={`match-list-card ${game.status}`} >
            <div className="player one">
                <div className="avatar" style={{backgroundImage: `url("${game.players[0]?.user_info?.profile_picutre_url}")` }} ></div>
            </div>
            <div className="score">
                <p>{game.players[0].score}</p>
                <p>{game.players[1].score}</p>
            </div>
            <div className="player two">
                <div className="avatar" style={{backgroundImage: `url("${game.players[1]?.user_info?.profile_picutre_url}")` }} ></div>
            </div>
            <p>{game.players[0].nickname} VS {game.players[1].nickname}</p>
        </div>
    );
}

export default MatchListCard;
