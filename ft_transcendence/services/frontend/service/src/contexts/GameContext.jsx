import React, { createContext, useState } from 'react';

export const GameContext = createContext();

export const GameProvider = ({ children }) => {
    const [isLoading, setIsLoading] = useState(false);
    const [gameId, setGameId] = useState(0);

    const [gameName, setGameName] = useState('');
    const [isTournament, setIsTournament] = useState(false);

    const [playersCount, setPlayersCount] = useState(0);

    const [isPlayerOne, setIsPlayerOne] = useState(false);
    const [isPlayerTwo, setIsPlayerTwo] = useState(false);

    const [isStarted, setIsStarted] = useState(false);

    const [cameraPosition, setCameraPosition] = useState([0, 0, 0]);

    const [ballPosition, setBallPosition] = useState([0, 0.6, 0]);
    const [playerOnePosition, setPlayerOnePosition] = useState([0, -1, -20.2]);
    const [playerTwoPosition, setPlayerTwoPosition] = useState([0, -1, +20.2]);

    const [players, setPlayers] = useState({});

    const [playerOneScore, setPlayerOneScore] = useState(0);
    const [PlayerOneNickname, setPlayerOneNickname] = useState('');

    const [playerTwoScore, setPlayerTwoScore] = useState(0);
    const [PlayerTwoNickname, setPlayerTwoNickname] = useState('');

    const [ballColor, setBallColor] = useState('#e48d2d');
    const [wallColor, setWallColor] = useState('#e48d2d');
    const [floorColor, setFloorColor] = useState('#ffffff');
    const [paddleColor, setPaddleColor] = useState('#ffffff');

    const fetchGameData = async (gameId) => {
        try {
            const response = await fetch(`/api/game/game-details/${gameId}/`, {
            method: 'GET',
            credentials: 'include'
            });
            if (response.ok) {
                const json = await response.json();
                if (json?.success == true) {
                    setGameName(json.game.custom_name);
                    setIsTournament(json.game.tournament_id > 0 ? true : false);
                    setPlayers(json.game.players);
                    setIsPlayerOne(json.game.players.length == 1 ? true : false);
                    setFloorColor(json.game.color_board);
                    setWallColor(json.game.color_wall);
                    setBallColor(json.game.color_ball);
                    setPaddleColor(json.game.color_paddle);
                }
            } else {
            }
        } catch (error) {
        }
    };

    const update = async () => {
        fetchGameData(gameId);
    }

    const join = async (id, index) => {
        setIsLoading(true);
        setGameId(id);
        fetchGameData(id);
        setCameraPosition(index === 1 ? [0, 5, -15] : [0, 5, +15]);
        setIsLoading(false);
    };

    const clear = async () => {
        setGameId(0);
        setGameName('');
        setIsTournament(false);
        setPlayersCount(0);
        setIsPlayerOne(false);
        setIsPlayerTwo(false);
        setIsStarted(false);
        setCameraPosition([0, 0, 0]);
        setBallPosition([0, 0.6, 0]);
        setPlayerOnePosition([0, -1, -20.2]);
        setPlayerTwoPosition([0, -1, +20.2]);
        setPlayers({});
        setPlayerOneScore(0);
        setPlayerOneNickname('');
        setPlayerTwoScore(0);
        setPlayerTwoNickname('');
        setFloorColor('#ffffff');
        setWallColor('#ffffff');
        setBallColor('#ffffff');
        setPaddleColor('#ffffff');
    };

    return (
        <GameContext.Provider value={{
            isLoading, setIsLoading,
            gameId, setGameId,

            isTournament, setIsTournament,

            players, setPlayers,
            isPlayerOne, setIsPlayerOne,
            isPlayerTwo, setIsPlayerTwo,
            isStarted, setIsStarted,
            cameraPosition, setCameraPosition,
            ballPosition, setBallPosition,
            playerOnePosition, setPlayerOnePosition,
            playerTwoPosition, setPlayerTwoPosition,

            ballColor, setBallColor,
            wallColor, setWallColor,
            floorColor, setFloorColor,
            paddleColor, setPaddleColor,

            join,
            clear
        }} >
            {children}
        </GameContext.Provider>
    );
};
