import './Tableone.css';
import React, { useState } from 'react';
import 'bootstrap/dist/css/bootstrap.min.css';

// Game Mode Switcher Component
const GameModeSwitcher = ({ gameMode, setGameMode }) => {
    // Switch to the previous mode
    const handleLeftArrowClick = () => {
        setGameMode((prevMode) => (prevMode === '1v1' ? '2v2' : '1v1'));
    };

    // Switch to the next mode
    const handleRightArrowClick = () => {
        setGameMode((prevMode) => (prevMode === '1v1' ? '2v2' : '1v1'));
    };

    return (
        <div className="game-mode-container">
            <h2>Game Mode</h2>
            <div className="game-mode-switcher">
                <button className="arrow-button" onClick={handleLeftArrowClick}>
                    ←
                </button>
                <div className="game-mode-display">{gameMode}</div>
                <button className="arrow-button" onClick={handleRightArrowClick}>
                    →
                </button>
            </div>
        </div>
    );
};

// Create Form Component
const CreateForm = ({ gameMode }) => {
    const [Rname, setRName] = useState('');

    return (
        <>
            <div className="title-gamemenu">Create Game ({gameMode})</div>
            <div className="Create-gamemenu">
                <div className="create-setting">
                    <fieldset>
                        <input
                            type="text"
                            placeholder="Room Name"
                            value={Rname}
                            onChange={(e) => setRName(e.target.value)}
                        />
						 <input
                            type="text"
                            placeholder="Nickname"
                            value={name}
                            onChange={(e) => setName(e.target.value)}
                        />
                        <div>
                            <input type="checkbox" name="Tournament" id="Tournament" />
                            <label htmlFor="Tournament">Tournament</label>
                        </div>
                        <input type="number" placeholder="Max Players" min="1" max="4" />
                    </fieldset>
                </div>
            </div>
        </>
    );
};

// Join Form Component
const JoinForm = () => {
    return (
        <div className="Join-gamemenu">
            <h3>Join Game</h3>
            <form>
                <input type="text" placeholder="Search..." />
                <button type="submit">Search</button>
            </form>
        </div>
    );
};

// Main Tableone Component
const Tableone = () => {
    const [create, setCreate] = useState(true);
    const [gameMode, setGameMode] = useState('1v1');

    // Toggle between Create and Join forms
    const toggleForm = () => {
        setCreate(!create);
    };

    return (
        <div className="Box-gamemenu">
            <GameModeSwitcher gameMode={gameMode} setGameMode={setGameMode} />
            {create ? <CreateForm gameMode={gameMode} /> : <JoinForm />}
        </div>
    );
};

export default Tableone;
