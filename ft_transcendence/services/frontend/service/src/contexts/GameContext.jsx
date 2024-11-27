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

    const [ballPosition, setBallPosition] = useState([0, 0.8, 0]);
    const [playerOnePosition, setPlayerOnePosition] = useState([0, -1, -20.2]);
    const [playerTwoPosition, setPlayerTwoPosition] = useState([0, -1, +20.2]);

    const [playerOneScore, setPlayerOneScore] = useState(0);
    const [PlayerOneNickname, setPlayerOneNickanem] = useState('');

    const [playerTwoScore, setPlayerTwoScore] = useState(0);
    const [PlayerTwoNickname, setPlayerTwoNickanem] = useState('');

    const [ballColor, setBallColor] = useState('#e48d2d');
    const [wallColor, setWallColor] = useState('#e48d2d');
    const [floorColor, setFloorColor] = useState('#ffffff');
    const [paddleColor, setPaddleColor] = useState('#ffffff');

    const [p1ProfilePicture, setP1ProfilePicture] = useState('');
    const [p1SuitColor, setP1SuitColor] = useState('#ffffff');
    const [p1RingsColor, setP1RingsColor] = useState('#ffffff');
    const [p1VisColor, setP1VisColor] = useState('#ffffff');
    const [p1BpColor, setP1BpColor] = useState('#ffffff');
    const [p1Flatness, setP1Flatness] = useState(2.8);
    const [p1HorizontalPosition, setP1HorizontalPosition] = useState(7.5);
    const [p1VerticalPosition, setP1VerticalPosition] = useState(0.0);

    const [p2ProfilePicture, setP2ProfilePicture] = useState('');
    const [p2SuitColor, setP2SuitColor] = useState('#ffffff');
    const [p2RingsColor, setP2RingsColor] = useState('#ffffff');
    const [p2VisColor, setP2VisColor] = useState('#ffffff');
    const [p2BpColor, setP2BpColor] = useState('#ffffff');
    const [p2Flatness, setP2Flatness] = useState(2.8);
    const [p2HorizontalPosition, setP2HorizontalPosition] = useState(7.5);
    const [p2VerticalPosition, setP2VerticalPosition] = useState(0.0);

    const fetchGameData = async (gameId) => {
        try {
            const response = await fetch(`/api/game/game-details/${gameId}/`, {
            method: 'GET',
            credentials: 'include'
            });
            if (response.ok) {
                const json = await response.json();
                if (json?.success == true) {
                    setGameName(json.game.game_custom_name);
                    setIsTournament(json.game.tournament_id > 0 ? true : false);
                    setPlayersCount(json.game.players.length);
                    setIsPlayerOne((playersCount == 0 || json.game.players[0].player_index == 0) ? true : false);
                    setIsPlayerTwo(!isPlayerOne);
                    setCameraPosition(isPlayerOne ? [0, 5, -15] : [0, 5, +15]);

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

    const fetchPlayerData = async () => {
        try {
            const response = await fetch(`/api/auth/user/${gameId}`, {
            method: 'GET',
            credentials: 'include'
            });
            if (response.ok) {
                const json = await response.json();
                if (json?.success == true) {
                    
                }
            } else {
            }
        } catch (error) {
        }
    };


    const create = (id) => {
        setIsLoading(true);
        setGameId(id);
        fetchGameData(id);
        setCameraPosition([0, 5, -15]);
        setIsLoading(false);
    };

    const join = (id) => {
        setIsLoading(true);
        setGameId(id);
        fetchGameData(id);
        setCameraPosition([0, 5, +15]);
        setIsLoading(false);
    };

    const start = async () => {
    };

    const clear = async () => {
        setIsPlayerOne(false);
    };

    return (
        <GameContext.Provider value={{
            isLoading, setIsLoading,
            gameId, setGameId,
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

            p1ProfilePicture, setP1ProfilePicture,
            p1SuitColor, setP1SuitColor,
            p1RingsColor, setP1RingsColor,
            p1VisColor, setP1VisColor,
            p1BpColor, setP1BpColor,
            p1Flatness, setP1Flatness,
            p1HorizontalPosition, setP1HorizontalPosition,
            p1VerticalPosition, setP1VerticalPosition,

            p2ProfilePicture, setP2ProfilePicture,
            p2SuitColor, setP2SuitColor,
            p2RingsColor, setP2RingsColor,
            p2VisColor, setP2VisColor,
            p2BpColor, setP2BpColor,
            p2Flatness, setP2Flatness,
            p2HorizontalPosition, setP2HorizontalPosition,
            p2VerticalPosition, setP2VerticalPosition,

            create, join,
            start, clear
        }} >
            {children}
        </GameContext.Provider>
    );
};
