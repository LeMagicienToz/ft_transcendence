import React, { useState } from 'react';

import ProfileCard from './ProfileCard';
import PlayersList from './PlayersList';
import BaseButton from './Buttons/BaseButton';
import CustomAstronautButton from './Buttons/CustomAstronautButton';
import LogoutButton from './Buttons/LogoutButton'
import AstronautScene from '../scenes/AstronautScene';

import './BurgerMenu.css';

const BurgerMenu = () => {
    const [isOpen, setIsOpen] = useState(false);

    const toggleMenu = () => {
        setIsOpen(!isOpen);
    };

    return (
        <div className='burger'>
            <BaseButton onClick={toggleMenu} text={isOpen ? '⛌' : '☰'} className='burger secondary round' />
            <nav className={`menu col ${isOpen ? 'open' : ''}`}>
                <ProfileCard />
                <div>
                    <div className='col astronaut-preview'>
                        <AstronautScene />
                        <CustomAstronautButton />
                    </div>
                </div>
                <div className='players'>
                    <PlayersList />
                </div>
                <LogoutButton className='alert end' />
            </nav>
        </div>
    );
}

export default BurgerMenu;