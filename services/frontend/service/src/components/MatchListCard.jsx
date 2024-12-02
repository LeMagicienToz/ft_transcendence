import React from 'react';


import './MatchListCard.css';

const MatchListCard = ({ game = {} }) => {

    return (
        <div className={`match-list-card col ${game.status}`} >
            <div className={`player one row ${game.players[0]?.score > game.players[1]?.score ? 'winner' : 'loser'}`} >
                <div className="avatar" style={{backgroundImage: `url("${game.players[0]?.user_info?.profile_picture_url}")` }} ></div>
                <p>{game.players[0]?.nickname}</p>
                <p className="score end" >
                    <div className="badge" >
                        <i class="bi bi-trophy-fill"></i>
                    </div>
                    {game.players[0]?.score}
                </p>
            </div>
            <div className={`player two row ${game.players[1]?.score > game.players[0]?.score ? 'winner' : 'loser'}`} >
                <div className="avatar" style={{backgroundImage: `url("${game.players[1]?.user_info?.profile_picture_url}")` }} ></div>
                <p>{game.players[1]?.nickname}</p>
                <p className="score end" >
                    {game.status == 'finished' && game.players[1]?.score > game.players[0]?.score ? (
                        <div className="badge" >
                            <i class="bi bi-trophy-fill"></i>
                        </div>
                    ) : null}
                    {game.players[1]?.score}
                </p>
            </div>
        </div>
    );
}

export default MatchListCard;
