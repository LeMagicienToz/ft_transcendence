import React from 'react';
import './Swap_button.css';

function SwapButton({ isLogin, onToggle }) {
	return (
		<div className="swap-button-container">
			<div className={`background-slider ${isLogin ? 'left' : 'right'}`} />
			<span 
		className={`option ${isLogin ? 'active' : ''}`} 
			onClick={isLogin ? null : onToggle} 
		>
			Login
		</span>
		
		{/* Bouton Register */}
		<span 
			className={`option ${!isLogin ? 'active' : ''}`} 
			onClick={!isLogin ? null : onToggle} 
		>
			Register
	</span>
		</div>
	);
}

export default SwapButton;