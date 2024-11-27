import React from 'react';

const Tab = ({ onClick = () => {}, name = 'Tab', disabled = false, children }) => {
    return (
        <>
            {children}
        </>
    );
}

export default Tab;
