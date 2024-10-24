import React, { useState } from 'react';
import { Canvas } from '@react-three/fiber';
import "./AstronautAvatar.css";
import MaterialAvatar from './MaterialAvatar.jsx';
import MyButton from '../Theme/MyButton.jsx';

// Utility function to convert hex color to RGB array
const hexToRgb = (hex) => {
	const bigint = parseInt(hex.replace('#', ''), 16);
	const r = (bigint >> 16) & 255;
	const g = (bigint >> 8) & 255;
	const b = bigint & 255;
	return [r / 255, g / 255, b / 255];
};
	
	function Show_Avatar() {
		const [suitColor, setSuitColor] = useState('#FFFFFF'); // Default color in hex
		const [visColor, setVisColor] = useState('#FFFFFF'); // Default color in hex ringsColor
		const [ringsColor, setRingsColor] = useState('#FFFFFF');
		const [bpColor, setBpColor] = useState('#FFFFFF');

		const handleSuitChange = (e) => setSuitColor(e.target.value);
		const handleVisChange = (e) => setVisColor(e.target.value);
		const handleRingsChange = (e) => setRingsColor(e.target.value);
		const handleBpChange = (e) => setBpColor(e.target.value);

		return (
			<div id="stage">
			<Canvas style={{ touchAction: 'none' }}>
					<ambientLight intensity={0.5} />	
					<directionalLight position={[5, 5, 5]} />
					<MaterialAvatar 
						suitColor={hexToRgb(suitColor)} 
						visColor={hexToRgb(visColor)} 
						ringsColor={hexToRgb(ringsColor)} 
						bpColor={hexToRgb(bpColor)}
					/>
			</Canvas>
			<div className="input-container">
					<div className="input-group">
					<label htmlFor="suitColor">Suit Color</label>
					<input
						id="suitColor"
						type="color"
						value={suitColor}
						onChange={handleSuitChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="visColor">Visor Color</label>
					<input
						id="visColor"
						type="color"
						value={visColor}
						onChange={handleVisChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="ringsColor">Rings Color</label>
					<input
						id="ringsColor"
						type="color"
						value={ringsColor}
						onChange={handleRingsChange}
					/>
					</div>
					<div className="input-group">
					<label htmlFor="bpColor">Backpack Color</label>
					<input
						id="bpColor"
						type="color"
						value={bpColor}
						onChange={handleBpChange}
					/>
					</div>
				</div>
				<div className="button-container">
				<MyButton to="home" text="Save & Quit"/>
				</div>
		</div>
	);
}

export default Show_Avatar;
