import React from 'react';

import Loader from '../Loader';

import './BaseButton.css';

const BaseButton = ({ onClick = () => {}, isLoading = false, id, className = '', text, disabled = false, children }) => {
    return (
        <div className={`button ${className}`} >
            {isLoading && (
                <div className={`loading`} >
                    <Loader size='16px' />
                </div>
            )}
            <button
                onClick={onClick}
                id={id}
                disabled={disabled}
            >
                {text || children}
            </button>
        </div>
    );
}

export default BaseButton;
