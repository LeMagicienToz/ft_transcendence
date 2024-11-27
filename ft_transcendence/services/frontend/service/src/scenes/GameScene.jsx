import React, { useContext } from 'react';
import { Canvas } from '@react-three/fiber';
import { Stage } from '@react-three/drei';

import { GameContext } from '../contexts/GameContext';

import Ball from '../assets/Ball';
import Board from '../assets/Board';
import PlayerOne from '../assets/PlayerOne';
import PlayerTwo from '../assets/PlayerTwo';

const GameScene = () => {

    const { cameraPosition, ballPosition, playerOnePosition, playerTwoPosition, paddleColor, ballColor, wallColor, floorColor,
            p1SuitColor, p1VisColor, p1RingsColor, p1BpColor, p1Flatness, p1HorizontalPosition, p1VerticalPosition, p1ProfilePicture,
            p2SuitColor, p2VisColor, p2RingsColor, p2BpColor, p2Flatness, p2HorizontalPosition, p2VerticalPosition, p2ProfilePicture,} = useContext(GameContext);

    return (
        <Canvas style={{ touchAction: 'none' }} camera={{ position: cameraPosition }} >
            <ambientLight intensity={0.5} />
            <directionalLight position={[5, 5, 5]} />
                <Stage contactShadow shadows adjustCamera intensity={1} preset="rembrandt" environment="forest">
                <Board
                    wallColor={wallColor}
                    floorColor={floorColor}
                />
                <Ball
                    position={ballPosition}
                    color={ballColor}
                />
                <PlayerOne
                    position={playerOnePosition}
                    suitColor={p1SuitColor}
                    visColor={p1VisColor}
                    ringsColor={p1RingsColor}
                    bpColor={p1BpColor}
                    paddleColor={paddleColor}
                    flatness={p1Flatness}
                    horizontalPosition={p1HorizontalPosition}
                    verticalPosition={p1VerticalPosition}
                    visTexture={p1ProfilePicture}
                />
                <PlayerTwo
                    position={playerTwoPosition}
                    suitColor={p2SuitColor}
                    visColor={p2VisColor}
                    ringsColor={p2RingsColor}
                    bpColor={p2BpColor}
                    paddleColor={paddleColor}
                    flatness={p2Flatness}
                    horizontalPosition={p2HorizontalPosition}
                    verticalPosition={p2VerticalPosition}
                    visTexture={p2ProfilePicture}
                />
            </Stage>
        </Canvas>
    );
};

export default GameScene;
