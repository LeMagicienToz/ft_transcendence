import React from 'react';
import OverlayTrigger from 'react-bootstrap/OverlayTrigger';
import { Tooltip as BootstrapTooltip } from 'react-bootstrap';

import './Tooltip.css';

const Tooltip = ({ text='', placement = 'top', children }) => {

    const render = (props) => (
        <BootstrapTooltip {...props} >
            {text}
        </BootstrapTooltip>
      );

    return (
        <OverlayTrigger
            placement={placement}
            overlay={(props) => render(props)}
        >
        {children}
        </OverlayTrigger>
    );
}

export default Tooltip;
