import React, { useContext, useState } from 'react';

import BaseButton from './BaseButton';
import AstronautWindow from '../Windows/AstronautWindow';

import './CustomAstronautButton.css';

const CustomAstronautButton = ({ id, text = '', className = '', disabled = false }) => {
    const [astronautWindowState, setAstronautWindowState] = useState(false);

    return (
        <div>
            <AstronautWindow
                isOpen={astronautWindowState}
                onClose={() => setAstronautWindowState(false)}
            />
            <BaseButton
                onClick={() => setAstronautWindowState(true)}
                text='Customize'
                className='secondary'
                disabled={disabled}
            />
        </div>
    );
}

export default CustomAstronautButton;
