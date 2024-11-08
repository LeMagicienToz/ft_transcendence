import React from 'react';
import './Modal_composant.css';

const Modal_composant = ({onClosedModal , children}) => {
	const click = (e) => {
		if (e.target.id === 'modal') {
			onClosedModal()
		}
	}

	return (
		<div className="blur-container" onClick={click} id="modal">
			{children}
		</div>
	)
};


export default Modal_composant;
